from __future__ import annotations

import uuid
from datetime import datetime, timezone, timedelta
from typing import Sequence, Tuple

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ConsentRequest


async def create_consent_request(
    db: AsyncSession,
    data: "ConsentRequestCreate",
) -> ConsentRequest:
    """Persist a new consent request."""
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(hours=data.expiry_hours)
    consent = ConsentRequest(
        patient_id=data.patient_id,
        doctor_id=data.doctor_id,
        purpose=data.purpose,
        scope=data.shared_data,
        status="pending",
        requested_at=now,
        expires_at=expires_at,
    )
    db.add(consent)
    await db.flush()
    await db.refresh(consent)
    return consent


async def get_consent_request_by_id(
    db: AsyncSession,
    consent_id: uuid.UUID,
) -> ConsentRequest | None:
    """Fetch a single consent request by primary key."""
    result = await db.execute(
        select(ConsentRequest).where(ConsentRequest.id == consent_id)
    )
    return result.scalar_one_or_none()


async def get_consent_requests_for_patient(
    db: AsyncSession,
    patient_id: uuid.UUID,
    status: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> Tuple[Sequence[ConsentRequest], int]:
    """Return consent requests where the patient is the subject, plus total count."""
    stmt = select(ConsentRequest).where(ConsentRequest.patient_id == patient_id)
    count_stmt = (
        select(func.count())
        .select_from(ConsentRequest)
        .where(ConsentRequest.patient_id == patient_id)
    )
    if status:
        stmt = stmt.where(ConsentRequest.status == status)
        count_stmt = count_stmt.where(ConsentRequest.status == status)
    stmt = (
        stmt.order_by(ConsentRequest.requested_at.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await db.execute(stmt)
    total_result = await db.execute(count_stmt)
    return result.scalars().all(), total_result.scalar_one()


async def get_consent_requests_by_doctor(
    db: AsyncSession,
    doctor_id: uuid.UUID,
    status: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> Tuple[Sequence[ConsentRequest], int]:
    """Return consent requests created by a doctor, plus total count."""
    stmt = select(ConsentRequest).where(ConsentRequest.doctor_id == doctor_id)
    count_stmt = (
        select(func.count())
        .select_from(ConsentRequest)
        .where(ConsentRequest.doctor_id == doctor_id)
    )
    if status:
        stmt = stmt.where(ConsentRequest.status == status)
        count_stmt = count_stmt.where(ConsentRequest.status == status)
    stmt = (
        stmt.order_by(ConsentRequest.requested_at.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await db.execute(stmt)
    total_result = await db.execute(count_stmt)
    return result.scalars().all(), total_result.scalar_one()


async def update_consent_status(
    db: AsyncSession,
    consent_id: uuid.UUID,
    status: str,
    approved_at: datetime | None = None,
) -> ConsentRequest | None:
    """Update the status of a consent request. Returns None if not found."""
    consent = await get_consent_request_by_id(db, consent_id)
    if consent is None:
        return None
    consent.status = status
    if approved_at:
        consent.approved_at = approved_at
    if status == "declined":
        consent.declined_at = datetime.now(timezone.utc)
    db.add(consent)
    await db.flush()
    await db.refresh(consent)
    return consent


async def revoke_consent(
    db: AsyncSession,
    consent_id: uuid.UUID,
) -> ConsentRequest | None:
    """Mark an approved consent as revoked. Returns None if not found."""
    consent = await get_consent_request_by_id(db, consent_id)
    if consent is None:
        return None
    consent.status = "revoked"
    consent.revoked_at = datetime.now(timezone.utc)
    db.add(consent)
    await db.flush()
    await db.refresh(consent)
    return consent


async def get_active_consent_for_doctor_patient(
    db: AsyncSession,
    doctor_id: uuid.UUID,
    patient_id: uuid.UUID,
) -> ConsentRequest | None:
    """Fetch the newest approved, non-expired consent between a doctor and patient."""
    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(ConsentRequest)
        .where(
            ConsentRequest.doctor_id == doctor_id,
            ConsentRequest.patient_id == patient_id,
            ConsentRequest.status == "approved",
            ConsentRequest.expires_at > now,
        )
        .order_by(ConsentRequest.expires_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def expire_old_consents(db: AsyncSession) -> None:
    """Mark all pending consents whose expiry_date has passed as expired."""
    now = datetime.now(timezone.utc)
    await db.execute(
        ConsentRequest.__table__.update()
        .where(
            ConsentRequest.status == "pending",
            ConsentRequest.expires_at < now,
        )
        .values(status="expired")
    )
    await db.flush()
