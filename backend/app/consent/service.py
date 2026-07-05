from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenException
from app.db.models import ConsentRequest, Doctor, User, AuditLog
from app.shared.exceptions import NotFoundException, ConflictException
from app.consent.repository import (
    create_consent_request,
    get_consent_request_by_id,
    get_consent_requests_for_patient,
    get_consent_requests_by_doctor,
    update_consent_status as repo_update_status,
    revoke_consent as repo_revoke,
    get_active_consent_for_doctor_patient,
    expire_old_consents,
)
from app.consent.schemas import ConsentRequestCreate, ConsentRequestResponse
from app.notifications.service import broadcast_consent_notification


async def _create_audit_log(
    db: AsyncSession,
    user_id: uuid.UUID | None,
    action: str,
    resource_type: str,
    resource_id: uuid.UUID,
    metadata: dict | None = None,
) -> None:
    """Write an immutable audit log entry."""
    log = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        audit_metadata=metadata or {},
    )
    db.add(log)
    await db.flush()


def _to_response(
    consent: ConsentRequest, doctor_name: str | None = None
) -> ConsentRequestResponse:
    """Map a ConsentRequest ORM object to the API response schema."""
    return ConsentRequestResponse(
        id=consent.id,
        doctor_id=consent.doctor_id,
        patient_id=consent.patient_id,
        doctor_name=doctor_name,
        status=consent.status,
        purpose=consent.purpose,
        shared_data=consent.scope or [],
        created_at=consent.requested_at,
        expiry_date=consent.expires_at,
        approved_at=consent.approved_at,
        declined_at=consent.declined_at,
    )


async def _get_doctor_name(db: AsyncSession, doctor_id: uuid.UUID) -> str | None:
    """Resolve a doctor's display name via the linked user profile."""
    result = await db.execute(
        select(User.first_name, User.last_name)
        .join(Doctor, Doctor.user_id == User.id)
        .where(Doctor.id == doctor_id)
    )
    row = result.one_or_none()
    if row:
        return f"{row.first_name or ''} {row.last_name or ''}".strip()
    return None


# ---------------------------------------------------------------------------
# Public service methods
# ---------------------------------------------------------------------------

async def request_consent(
    db: AsyncSession,
    doctor_id: uuid.UUID,
    patient_id: uuid.UUID,
    purpose: str,
    shared_data: list[str],
    expiry_hours: int,
) -> ConsentRequestResponse:
    """Doctor creates a consent request and notifies the patient."""
    data = ConsentRequestCreate(
        doctor_id=doctor_id,
        patient_id=patient_id,
        purpose=purpose,
        shared_data=shared_data,
        expiry_hours=expiry_hours,
    )
    consent = await create_consent_request(db, data)
    doctor_name = await _get_doctor_name(db, consent.doctor_id)
    await _create_audit_log(
        db,
        user_id=doctor_id,
        action="CONSENT_REQUESTED",
        resource_type="ConsentRequest",
        resource_id=consent.id,
        metadata={"patient_id": str(patient_id), "purpose": purpose},
    )
    await broadcast_consent_notification(db, consent, "CONSENT_REQUESTED")
    return _to_response(consent, doctor_name)


async def approve_consent(
    db: AsyncSession,
    consent_id: uuid.UUID,
    patient_id: uuid.UUID,
) -> ConsentRequestResponse:
    """Patient approves a pending consent request."""
    consent = await get_consent_request_by_id(db, consent_id)
    if consent is None:
        raise NotFoundException("Consent request not found.")
    if consent.patient_id != patient_id:
        raise ForbiddenException("You are not authorized to approve this consent.")
    if consent.status == "expired" or (
        consent.expires_at and consent.expires_at < datetime.now(timezone.utc)
    ):
        raise ConflictException("Consent request has expired.")
    if consent.status != "pending":
        raise ConflictException(
            f"Cannot approve a consent that is already {consent.status}."
        )

    updated = await repo_update_status(
        db, consent_id, "approved", approved_at=datetime.now(timezone.utc)
    )
    if updated is None:
        raise NotFoundException("Consent request not found.")
    doctor_name = await _get_doctor_name(db, updated.doctor_id)
    await _create_audit_log(
        db,
        user_id=patient_id,
        action="CONSENT_APPROVED",
        resource_type="ConsentRequest",
        resource_id=updated.id,
        metadata={"doctor_id": str(updated.doctor_id)},
    )
    await broadcast_consent_notification(db, updated, "CONSENT_APPROVED")
    return _to_response(updated, doctor_name)


async def decline_consent(
    db: AsyncSession,
    consent_id: uuid.UUID,
    patient_id: uuid.UUID,
) -> ConsentRequestResponse:
    """Patient declines a pending consent request."""
    consent = await get_consent_request_by_id(db, consent_id)
    if consent is None:
        raise NotFoundException("Consent request not found.")
    if consent.patient_id != patient_id:
        raise ForbiddenException("You are not authorized to decline this consent.")
    if consent.status == "expired" or (
        consent.expires_at and consent.expires_at < datetime.now(timezone.utc)
    ):
        raise ConflictException("Consent request has expired.")
    if consent.status != "pending":
        raise ConflictException(
            f"Cannot decline a consent that is already {consent.status}."
        )

    updated = await repo_update_status(db, consent_id, "declined")
    if updated is None:
        raise NotFoundException("Consent request not found.")
    doctor_name = await _get_doctor_name(db, updated.doctor_id)
    await _create_audit_log(
        db,
        user_id=patient_id,
        action="CONSENT_DECLINED",
        resource_type="ConsentRequest",
        resource_id=updated.id,
        metadata={"doctor_id": str(updated.doctor_id)},
    )
    await broadcast_consent_notification(db, updated, "CONSENT_DECLINED")
    return _to_response(updated, doctor_name)


async def revoke_consent(
    db: AsyncSession,
    consent_id: uuid.UUID,
    patient_id: uuid.UUID,
) -> ConsentRequestResponse:
    """Patient revokes a previously approved consent."""
    consent = await get_consent_request_by_id(db, consent_id)
    if consent is None:
        raise NotFoundException("Consent request not found.")
    if consent.patient_id != patient_id:
        raise ForbiddenException("You are not authorized to revoke this consent.")
    if consent.status != "approved":
        raise ConflictException("Only an approved consent can be revoked.")

    updated = await repo_revoke(db, consent_id)
    if updated is None:
        raise NotFoundException("Consent request not found.")
    doctor_name = await _get_doctor_name(db, updated.doctor_id)
    await _create_audit_log(
        db,
        user_id=patient_id,
        action="CONSENT_REVOKED",
        resource_type="ConsentRequest",
        resource_id=updated.id,
        metadata={"doctor_id": str(updated.doctor_id)},
    )
    await broadcast_consent_notification(db, updated, "CONSENT_REVOKED")
    return _to_response(updated, doctor_name)


async def list_consents_for_patient(
    db: AsyncSession,
    patient_id: uuid.UUID,
    status: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[ConsentRequestResponse], int]:
    """Return paginated consent requests for a patient with doctor names."""
    items, total = await get_consent_requests_for_patient(
        db, patient_id, status, limit, offset
    )
    doctor_ids = {c.doctor_id for c in items}
    names: dict[uuid.UUID, str] = {}
    if doctor_ids:
        result = await db.execute(
            select(Doctor.id, User.first_name, User.last_name)
            .join(User, Doctor.user_id == User.id)
            .where(Doctor.id.in_(doctor_ids))
        )
        for row in result.all():
            names[row.id] = f"{row.first_name or ''} {row.last_name or ''}".strip()
    responses = [_to_response(c, names.get(c.doctor_id)) for c in items]
    return responses, total


async def list_consents_for_doctor(
    db: AsyncSession,
    doctor_id: uuid.UUID,
    status: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[ConsentRequestResponse], int]:
    """Return paginated consent requests created by a doctor."""
    items, total = await get_consent_requests_by_doctor(
        db, doctor_id, status, limit, offset
    )
    doctor_name = await _get_doctor_name(db, doctor_id)
    responses = [_to_response(c, doctor_name) for c in items]
    return responses, total


async def check_record_access(
    db: AsyncSession,
    doctor_id: uuid.UUID,
    patient_id: uuid.UUID,
) -> None:
    """Verify an active, non-expired consent exists; raise ForbiddenException if not."""
    await expire_old_consents(db)
    consent = await get_active_consent_for_doctor_patient(db, doctor_id, patient_id)
    if consent is None:
        raise ForbiddenException("No active consent found for this patient.")


async def get_consent_with_doctor_name(
    db: AsyncSession,
    consent_id: uuid.UUID,
) -> ConsentRequestResponse | None:
    """Fetch a single consent enriched with the doctor's display name."""
    consent = await get_consent_request_by_id(db, consent_id)
    if consent is None:
        return None
    doctor_name = await _get_doctor_name(db, consent.doctor_id)
    return _to_response(consent, doctor_name)
