#!/usr/bin/env python3
"""Mirage Timeline API router."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.dependencies import get_current_user, get_current_doctor
from app.consent.service import check_record_access
from app.core.database import get_db
from app.db.models import (
    Allergy,
    ChronicCondition,
    Diagnosis,
    Doctor,
    Facility,
    MedicalRecord,
    Medication,
    Patient,
    User,
    Visit,
)
from app.doctor.router import _resolve_doctor_id
from app.schemas.envelope import Envelope
from app.shared.exceptions import ForbiddenException, NotFoundException

router = APIRouter()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class TimelineEventResponse(BaseModel):
    model_config = ConfigDict(strict=True)
    event_id: uuid.UUID
    event_type: str
    date: str
    title: str
    description: str | None = None
    facility_name: str | None = None
    doctor_name: str | None = None
    status: str | None = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@router.get(
    "/{patient_id}",
    response_model=Envelope[list[TimelineEventResponse]],
    summary="Chronological timeline for a patient",
)
async def get_timeline(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[list[TimelineEventResponse]]:
    # Authorization
    if current_user.role == "patient":
        from app.patient.me_router import _resolve_patient_id

        user_patient_id = await _resolve_patient_id(db, current_user.id)
        if patient_id != user_patient_id:
            raise ForbiddenException("You can only view your own timeline.")
    elif current_user.role == "doctor":
        doctor_id = await _resolve_doctor_id(db, current_user.id)
        await check_record_access(db, doctor_id, patient_id)
    # Admins bypass

    result = await db.execute(
        select(MedicalRecord).where(MedicalRecord.patient_id == patient_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        return Envelope.ok([])

    events: list[TimelineEventResponse] = []

    # Visits
    visit_result = await db.execute(
        select(Visit)
        .options(selectinload(Visit.doctor).selectinload(Doctor.user))
        .options(selectinload(Visit.facility))
        .where(Visit.medical_record_id == record.id)
        .order_by(Visit.visit_date.desc())
    )
    for visit in visit_result.unique().scalars().all():
        events.append(
            TimelineEventResponse(
                event_id=visit.id,
                event_type="VISIT",
                date=visit.visit_date.isoformat() if visit.visit_date else "",
                title=f"Visit: {visit.reason or visit.chief_complaint or 'Consultation'}",
                description=visit.summary,
                facility_name=visit.facility.name if visit.facility else None,
                doctor_name=(
                    f"{visit.doctor.user.first_name} {visit.doctor.user.last_name}".strip()
                    if visit.doctor and visit.doctor.user
                    else None
                ),
                status=visit.status,
            )
        )

    # Diagnoses
    diag_result = await db.execute(
        select(Diagnosis)
        .join(Visit)
        .where(Visit.medical_record_id == record.id)
        .order_by(Diagnosis.created_at.desc())
    )
    for d in diag_result.scalars().all():
        events.append(
            TimelineEventResponse(
                event_id=d.id,
                event_type="DIAGNOSIS",
                date=d.created_at.isoformat() if d.created_at else "",
                title=f"Diagnosis: {d.diagnosis_name}",
                description=d.notes,
                facility_name=None,
                doctor_name=None,
                status="confirmed" if d.primary_diagnosis else "suspected",
            )
        )

    # Medications
    med_result = await db.execute(
        select(Medication)
        .join(Visit)
        .where(Visit.medical_record_id == record.id)
        .order_by(Medication.created_at.desc())
    )
    for m in med_result.scalars().all():
        events.append(
            TimelineEventResponse(
                event_id=m.id,
                event_type="PRESCRIPTION",
                date=m.created_at.isoformat() if m.created_at else "",
                title=f"Medication: {m.name}",
                description=m.instructions,
                facility_name=None,
                doctor_name=None,
                status=None,
            )
        )

    # Allergies
    for a in record.allergies:
        events.append(
            TimelineEventResponse(
                event_id=a.id,
                event_type="ALLERGY_UPDATE",
                date=a.created_at.isoformat() if a.created_at else "",
                title=f"Allergy: {a.allergen}",
                description=a.reaction,
                facility_name=None,
                doctor_name=None,
                status=a.severity,
            )
        )

    # Conditions
    for c in record.chronic_conditions:
        events.append(
            TimelineEventResponse(
                event_id=c.id,
                event_type="CONDITION",
                date=c.created_at.isoformat() if c.created_at else "",
                title=f"Condition: {c.condition_name}",
                description=c.notes,
                facility_name=None,
                doctor_name=None,
                status=c.status,
            )
        )

    events.sort(key=lambda e: e.date, reverse=True)
    return Envelope.ok(events)


@router.get(
    "/event/{event_id}",
    response_model=Envelope[TimelineEventResponse],
    summary="Get a specific timeline event",
)
async def get_timeline_event(
    event_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[TimelineEventResponse]:
    # Try to find the event across all event types
    # First check visits
    visit_result = await db.execute(
        select(Visit)
        .options(selectinload(Visit.doctor).selectinload(Doctor.user))
        .options(selectinload(Visit.facility))
        .where(Visit.id == event_id)
    )
    visit = visit_result.unique().scalar_one_or_none()
    if visit:
        # Verify access
        if current_user.role == "patient":
            from app.patient.me_router import _resolve_patient_id

            user_patient_id = await _resolve_patient_id(db, current_user.id)
            if visit.medical_record.patient_id != user_patient_id:
                raise ForbiddenException("You can only view your own events.")
        return Envelope.ok(
            TimelineEventResponse(
                event_id=visit.id,
                event_type="VISIT",
                date=visit.visit_date.isoformat() if visit.visit_date else "",
                title=f"Visit: {visit.reason or visit.chief_complaint or 'Consultation'}",
                description=visit.summary,
                facility_name=visit.facility.name if visit.facility else None,
                doctor_name=(
                    f"{visit.doctor.user.first_name} {visit.doctor.user.last_name}".strip()
                    if visit.doctor and visit.doctor.user
                    else None
                ),
                status=visit.status,
            )
        )

    # Check diagnoses
    diag_result = await db.execute(
        select(Diagnosis)
        .options(selectinload(Diagnosis.visit))
        .where(Diagnosis.id == event_id)
    )
    diag = diag_result.scalar_one_or_none()
    if diag:
        if current_user.role == "patient":
            from app.patient.me_router import _resolve_patient_id

            user_patient_id = await _resolve_patient_id(db, current_user.id)
            # Need to check via visit's medical record patient_id
            # Since we didn't load medical_record, do another query
            mr_result = await db.execute(
                select(MedicalRecord.patient_id).where(
                    MedicalRecord.id == diag.visit.medical_record_id
                )
            )
            record_patient_id = mr_result.scalar_one_or_none()
            if record_patient_id != user_patient_id:
                raise ForbiddenException("You can only view your own events.")
        return Envelope.ok(
            TimelineEventResponse(
                event_id=diag.id,
                event_type="DIAGNOSIS",
                date=diag.created_at.isoformat() if diag.created_at else "",
                title=f"Diagnosis: {diag.diagnosis_name}",
                description=diag.notes,
                facility_name=None,
                doctor_name=None,
                status="confirmed" if diag.primary_diagnosis else "suspected",
            )
        )

    # Check medications
    med_result = await db.execute(
        select(Medication)
        .options(selectinload(Medication.visit))
        .where(Medication.id == event_id)
    )
    med = med_result.scalar_one_or_none()
    if med:
        if current_user.role == "patient":
            from app.patient.me_router import _resolve_patient_id

            user_patient_id = await _resolve_patient_id(db, current_user.id)
            mr_result = await db.execute(
                select(MedicalRecord.patient_id).where(
                    MedicalRecord.id == med.visit.medical_record_id
                )
            )
            record_patient_id = mr_result.scalar_one_or_none()
            if record_patient_id != user_patient_id:
                raise ForbiddenException("You can only view your own events.")
        return Envelope.ok(
            TimelineEventResponse(
                event_id=med.id,
                event_type="PRESCRIPTION",
                date=med.created_at.isoformat() if med.created_at else "",
                title=f"Medication: {med.name}",
                description=med.instructions,
                facility_name=None,
                doctor_name=None,
                status=None,
            )
        )

    # Check allergies
    allergy_result = await db.execute(
        select(Allergy)
        .options(selectinload(Allergy.medical_record))
        .where(Allergy.id == event_id)
    )
    allergy = allergy_result.scalar_one_or_none()
    if allergy:
        if current_user.role == "patient":
            from app.patient.me_router import _resolve_patient_id

            user_patient_id = await _resolve_patient_id(db, current_user.id)
            if allergy.medical_record.patient_id != user_patient_id:
                raise ForbiddenException("You can only view your own events.")
        return Envelope.ok(
            TimelineEventResponse(
                event_id=allergy.id,
                event_type="ALLERGY_UPDATE",
                date=allergy.created_at.isoformat() if allergy.created_at else "",
                title=f"Allergy: {allergy.allergen}",
                description=allergy.reaction,
                facility_name=None,
                doctor_name=None,
                status=allergy.severity,
            )
        )

    # Check conditions
    cond_result = await db.execute(
        select(ChronicCondition)
        .options(selectinload(ChronicCondition.medical_record))
        .where(ChronicCondition.id == event_id)
    )
    cond = cond_result.scalar_one_or_none()
    if cond:
        if current_user.role == "patient":
            from app.patient.me_router import _resolve_patient_id

            user_patient_id = await _resolve_patient_id(db, current_user.id)
            if cond.medical_record.patient_id != user_patient_id:
                raise ForbiddenException("You can only view your own events.")
        return Envelope.ok(
            TimelineEventResponse(
                event_id=cond.id,
                event_type="CONDITION",
                date=cond.created_at.isoformat() if cond.created_at else "",
                title=f"Condition: {cond.condition_name}",
                description=cond.notes,
                facility_name=None,
                doctor_name=None,
                status=cond.status,
            )
        )

    raise NotFoundException("Event not found.", error_code="NOT_FOUND")
