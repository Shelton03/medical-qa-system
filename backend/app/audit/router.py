#!/usr/bin/env python3
"""Mirage Audit API router."""

from __future__ import annotations

import uuid
from datetime import date, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_role
from app.core.database import get_db
from app.db.models import AuditLog, User
from app.schemas.envelope import Envelope
from app.shared.exceptions import NotFoundException

router = APIRouter()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class AuditLogResponse(BaseModel):
    model_config = ConfigDict(strict=True)
    id: uuid.UUID
    user_id: uuid.UUID | None = None
    action: str
    resource_type: str | None = None
    resource_id: uuid.UUID | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    audit_metadata: dict | None = None
    created_at: str


class AuditListMeta(BaseModel):
    model_config = ConfigDict(strict=True)
    page: int
    page_size: int
    total: int
    total_pages: int


class AuditListResponse(BaseModel):
    model_config = ConfigDict(strict=True)
    items: list[AuditLogResponse]
    meta: AuditListMeta


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@router.get(
    "/",
    response_model=Envelope[AuditListResponse],
    summary="List audit logs with pagination and filtering",
)
async def list_audit_logs(
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=100),
    sort: str = Query("created_at"),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    user_id: uuid.UUID | None = Query(None),
    action: str | None = Query(None),
    resource_type: str | None = Query(None),
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
) -> Envelope[AuditListResponse]:
    stmt = select(AuditLog)
    count_stmt = select(AuditLog)

    if user_id:
        # Note: using Python-level filtering since SQLAlchemy 2.0 async select
        # doesn't support direct equality on UUID in all drivers the same way
        pass

    # Build filter conditions
    conditions = []
    if user_id:
        conditions.append(AuditLog.user_id == user_id)
    if action:
        conditions.append(AuditLog.action == action)
    if resource_type:
        conditions.append(AuditLog.resource_type == resource_type)
    if date_from:
        from_dt = datetime.combine(date_from, datetime.min.time())
        conditions.append(AuditLog.created_at >= from_dt)
    if date_to:
        to_dt = datetime.combine(date_to, datetime.max.time())
        conditions.append(AuditLog.created_at <= to_dt)

    if conditions:
        from sqlalchemy import and_
        stmt = stmt.where(and_(*conditions))
        count_stmt = count_stmt.where(and_(*conditions))

    # Sorting
    sort_col = getattr(AuditLog, sort, AuditLog.created_at)
    if order == "desc":
        stmt = stmt.order_by(sort_col.desc())
    else:
        stmt = stmt.order_by(sort_col.asc())

    # Pagination
    offset = (page - 1) * pageSize
    stmt = stmt.offset(offset).limit(pageSize)

    result = await db.execute(stmt)
    items = result.scalars().all()

    from sqlalchemy import func
    total_result = await db.execute(
        select(func.count()).select_from(count_stmt.subquery())
    )
    total = total_result.scalar_one()
    total_pages = (total + pageSize - 1) // pageSize

    return Envelope.ok(
        AuditListResponse(
            items=[
                AuditLogResponse(
                    id=log.id,
                    user_id=log.user_id,
                    action=log.action,
                    resource_type=log.resource_type,
                    resource_id=log.resource_id,
                    ip_address=log.ip_address,
                    user_agent=log.user_agent,
                    audit_metadata=log.audit_metadata or {},
                    created_at=log.created_at.isoformat() if log.created_at else "",
                )
                for log in items
            ],
            meta=AuditListMeta(
                page=page,
                page_size=pageSize,
                total=total,
                total_pages=total_pages,
            ),
        )
    )


@router.get(
    "/{audit_id}",
    response_model=Envelope[AuditLogResponse],
    summary="Get single audit log entry",
)
async def get_audit_log(
    audit_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
) -> Envelope[AuditLogResponse]:
    result = await db.execute(select(AuditLog).where(AuditLog.id == audit_id))
    log = result.scalar_one_or_none()
    if not log:
        raise NotFoundException("Audit log not found.", error_code="NOT_FOUND")

    return Envelope.ok(
        AuditLogResponse(
            id=log.id,
            user_id=log.user_id,
            action=log.action,
            resource_type=log.resource_type,
            resource_id=log.resource_id,
            ip_address=log.ip_address,
            user_agent=log.user_agent,
            audit_metadata=log.audit_metadata or {},
            created_at=log.created_at.isoformat() if log.created_at else "",
        )
    )
