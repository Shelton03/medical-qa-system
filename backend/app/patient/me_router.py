#!/usr/bin/env python3
"""Mirage Patient 'me' API router — patient-scoped endpoints."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.auth.dependencies import get_current_user, get_current_patient
from app.core.database import get_db
from app.db.models import (
    Allergy,
    ChronicCondition,
    ConsentRequest,
    Diagnosis,
    Doctor,
    Facility,
    MedicalRecord,
    Medication,
    Notification,
    Patient,
    User,
    Visit,
    AISession,
)
from app.doctor.schemas import (
    ClinicalNoteResponse,
    DiagnosisResponse,
    MedicationResponse,
    VisitResponse,
    VisitWithDetailsResponse,
)
from app.doctor import service as doctor_service
from app.notifications import service as notification_service
from app.notifications.schemas import NotificationListResponse, NotificationResponse
from app.patient import repository as patient_repository
from app.patient.schemas import PatientFullProfileResponse, PatientResponse
from app.schemas.envelope import Envelope
from app.shared.exceptions import ForbiddenException, NotFoundException

router = APIRouter()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class PatientMeUpdate(BaseModel):
    """Patient-editable fields."""

    model_config = ConfigDict(strict=True)
    phone: str | None = Field(None, max_length=50)
    address: str | None = None
    emergency_contact_name: str | None = Field(None, max_length=255)
    emergency_contact_phone: str | None = Field(None, max_length=50)
    preferred_language: str | None = Field(None, max_length=50)


class TimelineEvent(BaseModel):
    model_config = ConfigDict(strict=True)
    event_id: uuid.UUID
    event_type: str
    date: datetime
    title: str
    description: str | None = None
    facility_name: str | None = None
    doctor_name: str | None = None
    status: str | None = None


class AccessHistoryEntry(BaseModel):
    model_config = ConfigDict(strict=True)
    consent_id: uuid.UUID
    doctor_name: str | None = None
    facility_name: str | None = None
    purpose: str | None = None
    status: str
    requested_at: datetime
    approved_at: datetime | None = None
    expires_at: datetime | None = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
async def _resolve_patient_id(db: AsyncSession, user_id: uuid.UUID) -> uuid.UUID:
    result = await db.execute(select(Patient.id).where(Patient.user_id == user_id))
    patient_id = result.scalar_one_or_none()
    if patient_id is None:
        raise NotFoundException("Patient profile not found.", error_code="PATIENT_NOT_FOUND")
    return patient_id


def _patient_response(patient: Patient) -> PatientResponse:
    return PatientResponse(
        id=patient.id,
        user_id=patient.user_id,
        medical_record_number=patient.medical_record_number,
        first_name=patient.user.first_name if patient.user else None,
        last_name=patient.user.last_name if patient.user else None,
        national_identifier=patient.national_identifier,
        phone=patient.user.phone_number if patient.user else None,
        date_of_birth=patient.date_of_birth,
        gender=patient.gender,
        blood_type=patient.blood_type,
        address=patient.address,
        emergency_contact_name=patient.emergency_contact_name,
        emergency_contact_phone=patient.emergency_contact_phone,
        preferred_language=patient.preferred_language,
        created_at=patient.created_at,
        updated_at=patient.updated_at,
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@router.get(
    "/",
    response_model=Envelope[PatientFullProfileResponse],
    summary="Current patient profile",
)
async def get_me(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_patient),
) -> Envelope[PatientFullProfileResponse]:
    patient_id = await _resolve_patient_id(db, current_user.id)
    patient = await patient_repository.get_patient_full_profile(db, patient_id)
    if not patient:
        raise NotFoundException("Patient not found.", error_code="PATIENT_NOT_FOUND")

    # Build profile manually to avoid ORM relationship issues
    from app.patient.schemas import (
        AllergySummaryResponse,
        ChronicConditionSummaryResponse,
        MedicalRecordSummaryResponse,
    )

    record = None
    if patient.medical_record:
        record = MedicalRecordSummaryResponse(
            id=patient.medical_record.id,
            patient_id=patient.medical_record.patient_id,
            primary_physician_id=patient.medical_record.primary_physician_id,
            record_status=patient.medical_record.record_status,
            created_at=patient.medical_record.created_at,
            updated_at=patient.medical_record.updated_at,
        )

    allergies = [
        AllergySummaryResponse(
            id=a.id,
            medical_record_id=a.medical_record_id,
            allergen=a.allergen,
            reaction=a.reaction,
            severity=a.severity,
            notes=a.notes,
            created_at=a.created_at,
        )
        for a in (patient.medical_record.allergies if patient.medical_record else [])
    ]

    conditions = [
        ChronicConditionSummaryResponse(
            id=c.id,
            medical_record_id=c.medical_record_id,
            condition_name=c.condition_name,
            diagnosed_date=c.diagnosed_date,
            status=c.status,
            notes=c.notes,
            created_at=c.created_at,
        )
        for c in (patient.medical_record.chronic_conditions if patient.medical_record else [])
    ]

    # Medications: traverse through visits since MedicalRecord lacks direct medications relationship
    medications = []
    if patient.medical_record:
        for visit in patient.medical_record.visits:
            for m in visit.medications:
                medications.append(
                    {
                        "id": m.id,
                        "visit_id": m.visit_id,
                        "name": m.name,
                        "dosage": m.dosage,
                        "frequency": m.frequency,
                        "duration": m.duration,
                        "instructions": m.instructions,
                        "start_date": m.start_date,
                        "end_date": m.end_date,
                        "created_at": m.created_at,
                    }
                )

    profile = PatientFullProfileResponse(
        id=patient.id,
        user_id=patient.user_id,
        medical_record_number=patient.medical_record_number,
        first_name=patient.user.first_name if patient.user else None,
        last_name=patient.user.last_name if patient.user else None,
        national_identifier=patient.national_identifier,
        phone=patient.user.phone_number if patient.user else None,
        date_of_birth=patient.date_of_birth,
        gender=patient.gender,
        blood_type=patient.blood_type,
        address=patient.address,
        emergency_contact_name=patient.emergency_contact_name,
        emergency_contact_phone=patient.emergency_contact_phone,
        preferred_language=patient.preferred_language,
        created_at=patient.created_at,
        updated_at=patient.updated_at,
        medical_record=record,
        allergies=allergies,
        chronic_conditions=conditions,
        medications=medications,
    )
    return Envelope.ok(profile)


@router.put(
    "/",
    response_model=Envelope[PatientResponse],
    summary="Update current patient profile",
)
async def update_me(
    data: PatientMeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_patient),
) -> Envelope[PatientResponse]:
    patient_id = await _resolve_patient_id(db, current_user.id)
    patient = await patient_repository.get_patient_by_id(db, patient_id)
    if not patient:
        raise NotFoundException("Patient not found.", error_code="PATIENT_NOT_FOUND")

    if data.address is not None:
        patient.address = data.address
    if data.emergency_contact_name is not None:
        patient.emergency_contact_name = data.emergency_contact_name
    if data.emergency_contact_phone is not None:
        patient.emergency_contact_phone = data.emergency_contact_phone
    if data.preferred_language is not None:
        patient.preferred_language = data.preferred_language
    if data.phone is not None and patient.user:
        patient.user.phone_number = data.phone

    await db.flush()
    await db.refresh(patient)
    return Envelope.ok(_patient_response(patient))


@router.get(
    "/timeline",
    response_model=Envelope[list[TimelineEvent]],
    summary="Full patient timeline",
)
async def get_timeline(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_patient),
) -> Envelope[list[TimelineEvent]]:
    patient_id = await _resolve_patient_id(db, current_user.id)

    result = await db.execute(
        select(MedicalRecord)
        .options(selectinload(MedicalRecord.allergies))
        .options(selectinload(MedicalRecord.chronic_conditions))
        .where(MedicalRecord.patient_id == patient_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        return Envelope.ok([])

    events: list[TimelineEvent] = []

    # Visits
    visit_result = await db.execute(
        select(Visit)
        .options(selectinload(Visit.doctor).selectinload(Doctor.user))
        .options(selectinload(Visit.facility))
        .where(Visit.medical_record_id == record.id)
        .order_by(Visit.visit_date.desc())
    )
    for visit in visit_result.scalars().all():
        events.append(
            TimelineEvent(
                event_id=visit.id,
                event_type="VISIT",
                date=visit.visit_date,
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
            TimelineEvent(
                event_id=d.id,
                event_type="DIAGNOSIS",
                date=d.created_at,
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
            TimelineEvent(
                event_id=m.id,
                event_type="PRESCRIPTION",
                date=m.created_at,
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
            TimelineEvent(
                event_id=a.id,
                event_type="ALLERGY_UPDATE",
                date=a.created_at,
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
            TimelineEvent(
                event_id=c.id,
                event_type="CONDITION",
                date=c.created_at,
                title=f"Condition: {c.condition_name}",
                description=c.notes,
                facility_name=None,
                doctor_name=None,
                status=c.status,
            )
        )

    # AI Sessions
    ai_result = await db.execute(
        select(AISession)
        .where(AISession.patient_id == patient_id)
        .order_by(AISession.started_at.desc())
    )
    for ai_session in ai_result.scalars().all():
        initiated_by = ai_session.provider_metadata.get("initiated_by") if ai_session.provider_metadata else None
        events.append(
            TimelineEvent(
                event_id=ai_session.id,
                event_type="AI_SESSION",
                date=ai_session.started_at,
                title=f"AI Symptom Check ({initiated_by or 'self-initiated'})",
                description=ai_session.conversation_summary or "AI-assisted symptom assessment",
                facility_name=None,
                doctor_name=None,
                status=ai_session.status,
            )
        )

    events.sort(key=lambda e: e.date, reverse=True)
    return Envelope.ok(events)


@router.get(
    "/visits",
    response_model=Envelope[list[VisitResponse]],
    summary="List all visits for this patient",
)
async def list_my_visits(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_patient),
) -> Envelope[list[VisitResponse]]:
    patient_id = await _resolve_patient_id(db, current_user.id)
    visits, _ = await doctor_service.list_visits_for_patient(db, patient_id, limit, offset)
    return Envelope.ok([doctor_service._visit_response(v) for v in visits])


@router.get(
    "/visit/{visit_id}",
    response_model=Envelope[VisitWithDetailsResponse],
    summary="Get single visit detail",
)
async def get_my_visit(
    visit_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_patient),
) -> Envelope[VisitWithDetailsResponse]:
    patient_id = await _resolve_patient_id(db, current_user.id)

    # Verify the visit belongs to this patient
    visit = await db.execute(
        select(Visit)
        .options(selectinload(Visit.medical_record))
        .where(Visit.id == visit_id)
    )
    visit = visit.unique().scalar_one_or_none()
    if not visit:
        raise NotFoundException("Visit not found.", error_code="VISIT_NOT_FOUND")
    if visit.medical_record.patient_id != patient_id:
        raise ForbiddenException("You can only view your own visits.")

    details = await doctor_service.get_consultation_details(db, visit_id, current_user)
    return Envelope.ok(details)


@router.get(
    "/notifications",
    response_model=Envelope[NotificationListResponse],
    summary="List notifications for this patient",
)
async def list_my_notifications(
    unread_only: bool = Query(False),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_patient),
) -> Envelope[NotificationListResponse]:
    items, total = await notification_service.get_user_notifications(
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
    "/access-history",
    response_model=Envelope[list[AccessHistoryEntry]],
    summary="Access history for this patient",
)
async def get_access_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_patient),
) -> Envelope[list[AccessHistoryEntry]]:
    patient_id = await _resolve_patient_id(db, current_user.id)

    result = await db.execute(
        select(ConsentRequest)
        .options(selectinload(ConsentRequest.doctor).selectinload(Doctor.user))
        .options(selectinload(ConsentRequest.doctor).selectinload(Doctor.facility))
        .where(ConsentRequest.patient_id == patient_id)
        .order_by(ConsentRequest.requested_at.desc())
    )
    consents = result.scalars().all()

    entries = []
    for c in consents:
        doctor_name = None
        facility_name = None
        if c.doctor:
            if c.doctor.user:
                doctor_name = f"{c.doctor.user.first_name or ''} {c.doctor.user.last_name or ''}".strip()
            if c.doctor.facility:
                facility_name = c.doctor.facility.name
        entries.append(
            AccessHistoryEntry(
                consent_id=c.id,
                doctor_name=doctor_name,
                facility_name=facility_name,
                purpose=c.purpose,
                status=c.status,
                requested_at=c.requested_at,
                approved_at=c.approved_at,
                expires_at=c.expires_at,
            )
        )

    return Envelope.ok(entries)
