#!/usr/bin/env python3
"""Mirage Medical Records API router."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.dependencies import get_current_user, get_current_doctor
from app.core.database import get_db
from app.db.models import (
    MedicalRecord,
    MedicalRecordVersion,
    Patient,
    User,
    Visit,
)
from app.schemas.envelope import Envelope
from app.shared.exceptions import ForbiddenException, NotFoundException

router = APIRouter()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class RecordPatch(BaseModel):
    model_config = ConfigDict(strict=True)
    primary_physician_id: uuid.UUID | None = None
    record_status: str | None = Field(None, max_length=50)


class RecordPatientInfo(BaseModel):
    model_config = ConfigDict(strict=True)
    id: uuid.UUID
    medical_record_number: str
    full_name: str | None = None
    date_of_birth: str | None = None
    gender: str | None = None
    blood_type: str | None = None


class RecordVisitInfo(BaseModel):
    model_config = ConfigDict(strict=True)
    id: uuid.UUID
    visit_date: str
    status: str
    reason: str | None = None
    chief_complaint: str | None = None
    summary: str | None = None


class RecordAllergyInfo(BaseModel):
    model_config = ConfigDict(strict=True)
    id: uuid.UUID
    allergen: str
    reaction: str | None = None
    severity: str | None = None


class RecordConditionInfo(BaseModel):
    model_config = ConfigDict(strict=True)
    id: uuid.UUID
    condition_name: str
    diagnosed_date: str | None = None
    status: str | None = None


class RecordResponse(BaseModel):
    model_config = ConfigDict(strict=True)
    id: uuid.UUID
    patient: RecordPatientInfo
    primary_physician_id: uuid.UUID | None = None
    record_status: str | None = None
    visits: list[RecordVisitInfo]
    allergies: list[RecordAllergyInfo]
    conditions: list[RecordConditionInfo]
    created_at: str
    updated_at: str


class RecordVersionResponse(BaseModel):
    model_config = ConfigDict(strict=True)
    id: uuid.UUID
    version_number: int
    changed_by: uuid.UUID | None = None
    change_summary: str | None = None
    snapshot: dict | None = None
    created_at: str


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
async def _resolve_patient_id(db: AsyncSession, user_id: uuid.UUID) -> uuid.UUID:
    result = await db.execute(
        select(Patient.id).where(Patient.user_id == user_id)
    )
    patient_id = result.scalar_one_or_none()
    if not patient_id:
        raise NotFoundException("Patient profile not found.")
    return patient_id


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@router.get(
    "/{record_id}",
    response_model=Envelope[RecordResponse],
    summary="Get medical record",
)
async def get_record(
    record_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[RecordResponse]:
    result = await db.execute(
        select(MedicalRecord)
        .options(selectinload(MedicalRecord.patient).selectinload(Patient.user))
        .options(selectinload(MedicalRecord.visits))
        .options(selectinload(MedicalRecord.allergies))
        .options(selectinload(MedicalRecord.chronic_conditions))
        .where(MedicalRecord.id == record_id)
    )
    record = result.unique().scalar_one_or_none()
    if not record:
        raise NotFoundException("Record not found.", error_code="RECORD_NOT_FOUND")

    # Authorization
    if current_user.role == "patient":
        patient_id = await _resolve_patient_id(db, current_user.id)
        if record.patient_id != patient_id:
            raise ForbiddenException("You can only view your own record.")
    # Doctors and admins allowed

    patient = record.patient
    patient_info = RecordPatientInfo(
        id=patient.id,
        medical_record_number=patient.medical_record_number,
        full_name=f"{patient.user.first_name or ''} {patient.user.last_name or ''}".strip()
        if patient.user
        else None,
        date_of_birth=patient.date_of_birth.isoformat() if patient.date_of_birth else None,
        gender=patient.gender,
        blood_type=patient.blood_type,
    )

    visits = [
        RecordVisitInfo(
            id=v.id,
            visit_date=v.visit_date.isoformat() if v.visit_date else "",
            status=v.status,
            reason=v.reason,
            chief_complaint=v.chief_complaint,
            summary=v.summary,
        )
        for v in record.visits
    ]

    allergies = [
        RecordAllergyInfo(
            id=a.id,
            allergen=a.allergen,
            reaction=a.reaction,
            severity=a.severity,
        )
        for a in record.allergies
    ]

    conditions = [
        RecordConditionInfo(
            id=c.id,
            condition_name=c.condition_name,
            diagnosed_date=c.diagnosed_date.isoformat() if c.diagnosed_date else None,
            status=c.status,
        )
        for c in record.chronic_conditions
    ]

    return Envelope.ok(
        RecordResponse(
            id=record.id,
            patient=patient_info,
            primary_physician_id=record.primary_physician_id,
            record_status=record.record_status,
            visits=visits,
            allergies=allergies,
            conditions=conditions,
            created_at=record.created_at.isoformat() if record.created_at else "",
            updated_at=record.updated_at.isoformat() if record.updated_at else "",
        )
    )


@router.patch(
    "/{record_id}",
    response_model=Envelope[RecordResponse],
    summary="Update record metadata",
)
async def patch_record(
    record_id: uuid.UUID,
    body: RecordPatch,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[RecordResponse]:
    result = await db.execute(
        select(MedicalRecord)
        .options(selectinload(MedicalRecord.patient).selectinload(Patient.user))
        .options(selectinload(MedicalRecord.visits))
        .options(selectinload(MedicalRecord.allergies))
        .options(selectinload(MedicalRecord.chronic_conditions))
        .where(MedicalRecord.id == record_id)
    )
    record = result.unique().scalar_one_or_none()
    if not record:
        raise NotFoundException("Record not found.", error_code="RECORD_NOT_FOUND")

    if body.primary_physician_id is not None:
        record.primary_physician_id = body.primary_physician_id
    if body.record_status is not None:
        record.record_status = body.record_status

    await db.flush()
    await db.refresh(record)

    # Build response (same as GET)
    patient = record.patient
    patient_info = RecordPatientInfo(
        id=patient.id,
        medical_record_number=patient.medical_record_number,
        full_name=f"{patient.user.first_name or ''} {patient.user.last_name or ''}".strip()
        if patient.user
        else None,
        date_of_birth=patient.date_of_birth.isoformat() if patient.date_of_birth else None,
        gender=patient.gender,
        blood_type=patient.blood_type,
    )

    visits = [
        RecordVisitInfo(
            id=v.id,
            visit_date=v.visit_date.isoformat() if v.visit_date else "",
            status=v.status,
            reason=v.reason,
            chief_complaint=v.chief_complaint,
            summary=v.summary,
        )
        for v in record.visits
    ]

    allergies = [
        RecordAllergyInfo(
            id=a.id,
            allergen=a.allergen,
            reaction=a.reaction,
            severity=a.severity,
        )
        for a in record.allergies
    ]

    conditions = [
        RecordConditionInfo(
            id=c.id,
            condition_name=c.condition_name,
            diagnosed_date=c.diagnosed_date.isoformat() if c.diagnosed_date else None,
            status=c.status,
        )
        for c in record.chronic_conditions
    ]

    return Envelope.ok(
        RecordResponse(
            id=record.id,
            patient=patient_info,
            primary_physician_id=record.primary_physician_id,
            record_status=record.record_status,
            visits=visits,
            allergies=allergies,
            conditions=conditions,
            created_at=record.created_at.isoformat() if record.created_at else "",
            updated_at=record.updated_at.isoformat() if record.updated_at else "",
        )
    )


@router.get(
    "/{record_id}/versions",
    response_model=Envelope[list[RecordVersionResponse]],
    summary="Get version history",
)
async def get_record_versions(
    record_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[list[RecordVersionResponse]]:
    # Verify record exists and user has access
    record_result = await db.execute(
        select(MedicalRecord).where(MedicalRecord.id == record_id)
    )
    record = record_result.scalar_one_or_none()
    if not record:
        raise NotFoundException("Record not found.", error_code="RECORD_NOT_FOUND")

    if current_user.role == "patient":
        patient_id = await _resolve_patient_id(db, current_user.id)
        if record.patient_id != patient_id:
            raise ForbiddenException("You can only view your own record.")

    versions_result = await db.execute(
        select(MedicalRecordVersion)
        .where(MedicalRecordVersion.medical_record_id == record_id)
        .order_by(MedicalRecordVersion.version_number.desc())
    )
    versions = versions_result.scalars().all()

    return Envelope.ok(
        [
            RecordVersionResponse(
                id=v.id,
                version_number=v.version_number,
                changed_by=v.changed_by,
                change_summary=v.change_summary,
                snapshot=v.snapshot or {},
                created_at=v.created_at.isoformat() if v.created_at else "",
            )
            for v in versions
        ]
    )
