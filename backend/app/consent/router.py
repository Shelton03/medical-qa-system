from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.auth.dependencies import get_current_user, get_current_doctor, get_current_patient
from app.db.models import Doctor, Patient
from app.schemas.envelope import Envelope
from app.shared.exceptions import NotFoundException, ForbiddenException
from app.consent.schemas import (
    ConsentRequestCreate,
    ConsentRequestResponse,
    ConsentListResponse,
    ConsentListMeta,
)
from app.consent import service

router = APIRouter()


async def _resolve_doctor_id(db: AsyncSession, user_id: uuid.UUID) -> uuid.UUID:
    result = await db.execute(select(Doctor.id).where(Doctor.user_id == user_id))
    doctor_id = result.scalar_one_or_none()
    if doctor_id is None:
        raise NotFoundException("Doctor profile not found.")
    return doctor_id


async def _resolve_patient_id(db: AsyncSession, user_id: uuid.UUID) -> uuid.UUID:
    result = await db.execute(select(Patient.id).where(Patient.user_id == user_id))
    patient_id = result.scalar_one_or_none()
    if patient_id is None:
        raise NotFoundException("Patient profile not found.")
    return patient_id


@router.post(
    "",
    response_model=Envelope[ConsentRequestResponse],
    summary="Create consent request",
    description="Doctor requests access to a patient's medical records.",
)
async def create_consent(
    body: ConsentRequestCreate,
    db: AsyncSession = Depends(get_db),
    current_doctor=Depends(get_current_doctor),
) -> Envelope[ConsentRequestResponse]:
    doctor_id = await _resolve_doctor_id(db, current_doctor.id)
    response = await service.request_consent(
        db,
        doctor_id=doctor_id,
        patient_id=body.patient_id,
        purpose=body.purpose,
        shared_data=body.shared_data,
        expiry_hours=body.expiry_hours,
    )
    await db.commit()
    return Envelope.ok(response)


@router.get(
    "",
    response_model=Envelope[ConsentListResponse],
    summary="List consent requests",
    description="Doctors see requests they created; patients see requests for them.",
)
async def list_consents(
    status: str | None = Query(None, description="Filter by status"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> Envelope[ConsentListResponse]:
    if current_user.role == "doctor":
        doctor_id = await _resolve_doctor_id(db, current_user.id)
        items, total = await service.list_consents_for_doctor(
            db, doctor_id, status=status, limit=limit, offset=offset
        )
    else:
        patient_id = await _resolve_patient_id(db, current_user.id)
        items, total = await service.list_consents_for_patient(
            db, patient_id, status=status, limit=limit, offset=offset
        )
    return Envelope.ok(
        ConsentListResponse(
            items=items,
            meta=ConsentListMeta(total=total, limit=limit, offset=offset),
        )
    )


@router.get(
    "/{consent_id}",
    response_model=Envelope[ConsentRequestResponse],
    summary="Get a single consent request",
)
async def get_consent(
    consent_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> Envelope[ConsentRequestResponse]:
    response = await service.get_consent_with_doctor_name(db, consent_id)
    if response is None:
        raise NotFoundException("Consent request not found.")
    if current_user.role == "patient":
        patient_id = await _resolve_patient_id(db, current_user.id)
        if response.patient_id != patient_id:
            raise ForbiddenException("Access denied.")
    elif current_user.role == "doctor":
        doctor_id = await _resolve_doctor_id(db, current_user.id)
        if response.doctor_id != doctor_id:
            raise ForbiddenException("Access denied.")
    return Envelope.ok(response)


@router.post(
    "/{consent_id}/approve",
    response_model=Envelope[ConsentRequestResponse],
    summary="Approve consent request",
    description="Patient approves a pending consent request.",
)
async def approve_consent(
    consent_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_patient=Depends(get_current_patient),
) -> Envelope[ConsentRequestResponse]:
    patient_id = await _resolve_patient_id(db, current_patient.id)
    response = await service.approve_consent(db, consent_id, patient_id)
    await db.commit()
    return Envelope.ok(response)


@router.post(
    "/{consent_id}/decline",
    response_model=Envelope[ConsentRequestResponse],
    summary="Decline consent request",
    description="Patient declines a pending consent request.",
)
async def decline_consent(
    consent_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_patient=Depends(get_current_patient),
) -> Envelope[ConsentRequestResponse]:
    patient_id = await _resolve_patient_id(db, current_patient.id)
    response = await service.decline_consent(db, consent_id, patient_id)
    await db.commit()
    return Envelope.ok(response)


@router.post(
    "/{consent_id}/revoke",
    response_model=Envelope[ConsentRequestResponse],
    summary="Revoke consent request",
    description="Patient revokes a previously approved consent.",
)
async def revoke_consent(
    consent_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_patient=Depends(get_current_patient),
) -> Envelope[ConsentRequestResponse]:
    patient_id = await _resolve_patient_id(db, current_patient.id)
    response = await service.revoke_consent(db, consent_id, patient_id)
    await db.commit()
    return Envelope.ok(response)
