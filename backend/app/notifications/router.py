"""REST router for the notifications domain."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.core.database import get_db
from app.db.models import User
from app.notifications import service
from app.notifications.schemas import (
    CountResponse,
    NotificationListResponse,
    NotificationResponse,
    UnreadCountResponse,
)
from app.schemas.envelope import Envelope

router = APIRouter()


@router.get(
    "",
    response_model=Envelope[NotificationListResponse],
    summary="List notifications",
)
async def list_notifications(
    unread_only: bool = Query(False, description="Filter unread only"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[NotificationListResponse]:
    """Return paginated notifications for the authenticated user."""
    items, total = await service.get_user_notifications(
        db,
        current_user.id,
        {"unread_only": unread_only, "limit": limit, "offset": offset},
    )
    return Envelope.ok(
        NotificationListResponse(
            items=[NotificationResponse.model_validate(n) for n in items],
            total=total,
            limit=limit,
            offset=offset,
        )
    )


@router.get(
    "/unread-count",
    response_model=Envelope[UnreadCountResponse],
    summary="Get unread notification count",
)
async def unread_count(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[UnreadCountResponse]:
    """Return the number of unread notifications for the current user."""
    count = await service.get_unread_count_for_user(db, current_user.id)
    return Envelope.ok(UnreadCountResponse(count=count))


@router.post(
    "/{notification_id}/read",
    response_model=Envelope[NotificationResponse],
    summary="Mark notification as read",
)
async def read_notification(
    notification_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[NotificationResponse]:
    """Mark a single notification as read after verifying ownership."""
    notification = await service.mark_read(db, notification_id, current_user.id)
    await db.commit()
    return Envelope.ok(NotificationResponse.model_validate(notification))


@router.post(
    "/read-all",
    response_model=Envelope[CountResponse],
    summary="Mark all notifications as read",
)
async def read_all_notifications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[CountResponse]:
    """Mark every unread notification for the current user as read."""
    count = await service.mark_all_read(db, current_user.id)
    await db.commit()
    return Envelope.ok(CountResponse(count=count))
