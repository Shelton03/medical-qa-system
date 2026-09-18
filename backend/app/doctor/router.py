#!/usr/bin/env python3
"""Mirage Consultation API router."""

from __future__ import annotations

import uuid
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.auth.dependencies import get_current_user, get_current_doctor
from app.db.models import Doctor, Patient
from app.db.models import User
from app.schemas.envelope import Envelope
from app.shared.exceptions import NotFoundException, ForbiddenException
from app.doctor import service
from app.appointment.schemas import AppointmentResponse
from app.appointment.service import appointment_service
from app.doctor.schemas import (
    AISessionBriefResponse,
    ClinicalNoteCreate,
    ClinicalNoteResponse,
    ConsultationCancelRequest,
    ConsultationCompleteRequest,
    DiagnosisCreate,
    DiagnosisResponse,
    MedicationCreate,
    MedicationResponse,
    VisitCreate,
    VisitResponse,
    VisitWithDetailsResponse,
)
from app.patient import repository as patient_repository
from app.patient.schemas import (
    AllergySummaryResponse,
    ChronicConditionSummaryResponse,
    PatientResponse,
)
from app.notifications import service as notification_service
from app.db.models import (
    AIMessage,
    AISession,
    Allergy,
    Appointment,
    ChronicCondition,
    ConsentRequest,
    DoctorSchedule,
    DoctorTimeOff,
    Facility,
    MedicalRecord,
    Medication,
    Notification,
    Visit,
)
from app.consent.service import check_record_access
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter()


# ---------------------------------------------------------------------------
# Additional schemas for new endpoints
# ---------------------------------------------------------------------------
class DashboardStats(BaseModel):
    model_config = ConfigDict(strict=True)
    pending_consents: int
    today_consultations: int
    notifications_count: int
    recent_patients: list[PatientResponse]


class PatientSearchRequest(BaseModel):
    model_config = ConfigDict(strict=True)
    query: str = Field(..., min_length=1)


class PatientSearchResult(BaseModel):
    model_config = ConfigDict(strict=True)
    patient_id: uuid.UUID
    medical_record_number: str
    full_name: str
    date_of_birth: date | None = None
    gender: str | None = None
    consent_status: str | None = None


class PatientOverview(BaseModel):
    model_config = ConfigDict(strict=True)
    id: uuid.UUID
    medical_record_number: str
    full_name: str
    national_identifier: str | None = None
    date_of_birth: date | None = None
    gender: str | None = None
    blood_type: str | None = None
    phone: str | None = None
    email: str | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    allergies: list[AllergySummaryResponse]
    conditions: list[ChronicConditionSummaryResponse]
    current_medications: list[dict]
    recent_visits: list[VisitResponse]


class ConsultationStartRequest(BaseModel):
    model_config = ConfigDict(strict=True)
    reason: str | None = None
    chief_complaint: str | None = None
    facility_id: uuid.UUID | None = None


# ---------------------------------------------------------------------------
# Helpers to resolve profile IDs from authenticated user IDs
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Visit / Consultation
# ---------------------------------------------------------------------------
@router.post(
    "",
    response_model=Envelope[VisitResponse],
    summary="Start a consultation",
    description="Create a new visit with status 'in_progress'. Requires doctor role and active consent.",
    status_code=201,
)
async def start_consultation(
    body: VisitCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[VisitResponse]:
    doctor_id = await _resolve_doctor_id(db, current_user.id)
    visit = await service.start_consultation(db, doctor_id=doctor_id, data=body)
    return Envelope.ok(service._visit_response(visit))


@router.get(
    "",
    response_model=Envelope[list[VisitResponse]],
    summary="List consultations",
    description="Doctors see their own visits; patients see their own visits.",
)
async def list_consultations(
    status: Annotated[str | None, Query(description="Filter by status")] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[list[VisitResponse]]:
    if current_user.role == "doctor":
        doctor_id = await _resolve_doctor_id(db, current_user.id)
        visits, _ = await service.list_visits_for_doctor(
            db, doctor_id, limit=limit, offset=offset, status=status
        )
    else:
        patient_id = await _resolve_patient_id(db, current_user.id)
        visits, _ = await service.list_visits_for_patient(
            db, patient_id, limit=limit, offset=offset, status=status
        )
    return Envelope.ok([service._visit_response(v) for v in visits])


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
@router.get(
    "/dashboard",
    response_model=Envelope[DashboardStats],
    summary="Doctor dashboard stats",
)
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[DashboardStats]:
    doctor_id = await _resolve_doctor_id(db, current_user.id)

    # Pending consents
    consent_result = await db.execute(
        select(ConsentRequest)
        .where(ConsentRequest.doctor_id == doctor_id, ConsentRequest.status == "pending")
    )
    pending_consents = len(consent_result.scalars().all())

    # Today's consultations
    from datetime import date, datetime

    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = datetime.combine(date.today(), datetime.max.time())
    visit_result = await db.execute(
        select(Visit).where(
            Visit.doctor_id == doctor_id,
            Visit.visit_date >= today_start,
            Visit.visit_date <= today_end,
        )
    )
    today_consultations = len(visit_result.scalars().all())

    # Notifications count
    notifications_count = await notification_service.get_unread_count_for_user(
        db, current_user.id
    )

    # Recent patients (unique patients from recent visits)
    recent_visits_result = await db.execute(
        select(Visit)
        .options(selectinload(Visit.medical_record).selectinload(MedicalRecord.patient).selectinload(Patient.user))
        .where(Visit.doctor_id == doctor_id)
        .order_by(Visit.visit_date.desc())
        .limit(5)
    )
    recent_visits = recent_visits_result.unique().scalars().all()
    seen_patient_ids = set()
    recent_patients = []
    for v in recent_visits:
        p = v.medical_record.patient if v.medical_record else None
        if p and p.id not in seen_patient_ids:
            seen_patient_ids.add(p.id)
            recent_patients.append(
                PatientResponse(
                    id=p.id,
                    user_id=p.user_id,
                    medical_record_number=p.medical_record_number,
                    first_name=p.user.first_name if p.user else None,
                    last_name=p.user.last_name if p.user else None,
                    national_identifier=p.national_identifier,
                    phone=p.user.phone_number if p.user else None,
                    date_of_birth=p.date_of_birth,
                    gender=p.gender,
                    blood_type=p.blood_type,
                    address=p.address,
                    emergency_contact_name=p.emergency_contact_name,
                    emergency_contact_phone=p.emergency_contact_phone,
                    preferred_language=p.preferred_language,
                    created_at=p.created_at,
                    updated_at=p.updated_at,
                )
            )

    return Envelope.ok(
        DashboardStats(
            pending_consents=pending_consents,
            today_consultations=today_consultations,
            notifications_count=notifications_count,
            recent_patients=recent_patients,
        )
    )


# ---------------------------------------------------------------------------
# Search patients
# ---------------------------------------------------------------------------
@router.post(
    "/search",
    response_model=Envelope[list[PatientSearchResult]],
    summary="Search patients",
)
async def search_patients(
    body: PatientSearchRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[list[PatientSearchResult]]:
    doctor_id = await _resolve_doctor_id(db, current_user.id)
    patients, _ = await patient_repository.search_patients(db, body.query, limit=20, offset=0)

    # Fetch consent statuses for these patients
    patient_ids = [p.id for p in patients]
    consent_result = await db.execute(
        select(ConsentRequest).where(
            ConsentRequest.doctor_id == doctor_id,
            ConsentRequest.patient_id.in_(patient_ids),
        )
    )
    consents = consent_result.scalars().all()
    consent_map = {}
    for c in consents:
        # Keep the most recent status per patient
        if c.patient_id not in consent_map:
            consent_map[c.patient_id] = c.status

    results = []
    for p in patients:
        results.append(
            PatientSearchResult(
                patient_id=p.id,
                medical_record_number=p.medical_record_number,
                full_name=f"{p.user.first_name or ''} {p.user.last_name or ''}".strip(),
                date_of_birth=p.date_of_birth,
                gender=p.gender,
                consent_status=consent_map.get(p.id),
            )
        )
    return Envelope.ok(results)


@router.get(
    "/schedule",
    response_model=Envelope[dict],
    summary="Get doctor schedule configuration",
)
async def get_doctor_schedule_config(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[dict]:
    """Return the doctor's weekly schedule configuration and time-off requests."""

    doctor_id = await _resolve_doctor_id(db, current_user.id)

    # Query schedule rows
    schedule_result = await db.execute(
        select(DoctorSchedule).where(DoctorSchedule.doctor_id == doctor_id)
    )
    schedules = list(schedule_result.scalars().all())

    # Query time-off requests
    to_result = await db.execute(
        select(DoctorTimeOff)
        .where(DoctorTimeOff.doctor_id == doctor_id)
        .order_by(DoctorTimeOff.start_date.desc())
    )
    time_offs = list(to_result.scalars().all())

    # Build days array
    days = []
    working_days = []
    start_times = []
    end_times = []
    max_appointments_list = []
    slot_durations = []

    for s in schedules:
        days.append({
            "day_of_week": s.day_of_week,
            "is_working": s.is_working_day,
            "start_time": s.start_time.strftime("%H:%M") if s.start_time else "09:00",
            "end_time": s.end_time.strftime("%H:%M") if s.end_time else "17:00",
            "max_appointments": s.max_daily_appointments,
            "slot_duration_minutes": s.default_slot_duration,
        })
        if s.is_working_day:
            working_days.append(s.day_of_week)
            start_times.append(s.start_time)
            end_times.append(s.end_time)
            max_appointments_list.append(s.max_daily_appointments)
            slot_durations.append(s.default_slot_duration)

    # Compute aggregates
    daily_start = min(start_times).strftime("%H:%M") if start_times else "09:00"
    daily_end = max(end_times).strftime("%H:%M") if end_times else "17:00"
    max_daily_appts = max(max_appointments_list) if max_appointments_list else 20
    default_slot = slot_durations[0] if slot_durations else 30

    # Build time_off_requests
    time_off_requests = [
        {
            "id": str(t.id),
            "doctor_id": str(t.doctor_id),
            "start_date": t.start_date.isoformat(),
            "end_date": t.end_date.isoformat(),
            "type": t.type,
            "reason": t.reason,
            "status": t.status,
            "requested_at": t.created_at.isoformat() if t.created_at else None,
        }
        for t in time_offs
    ]

    return Envelope.ok({
        "id": str(doctor_id),
        "doctor_id": str(doctor_id),
        "working_days": working_days,
        "daily_start_time": daily_start,
        "daily_end_time": daily_end,
        "max_daily_appointments": max_daily_appts,
        "default_slot_duration_minutes": default_slot,
        "buffer_minutes": 5,
        "time_off_requests": time_off_requests,
        "appointments": [],
        "days": days,
    })


@router.get(
    "/appointments/today",
    response_model=Envelope[list[dict]],
    summary="Get doctor's appointments for today",
)
async def get_doctor_appointments_today(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[list[dict]]:
    """Return today's confirmed and pending appointments for the logged-in doctor."""

    doctor_id = await _resolve_doctor_id(db, current_user.id)
    appointments = await appointment_service.get_doctor_schedule(
        db, doctor_id, query_date=date.today()
    )
    return Envelope.ok([
        {
            "id": str(a.id),
            "patient_id": str(a.patient_id) if a.patient_id else None,
            "patient_name": (
                f"{a.patient.user.first_name} {a.patient.user.last_name}"
                if a.patient and a.patient.user else None
            ),
            "start_time": a.allocated_start_time.strftime("%H:%M") if a.allocated_start_time else "00:00",
            "end_time": a.allocated_end_time.strftime("%H:%M") if a.allocated_end_time else "00:00",
            "duration_minutes": a.desired_duration_minutes,
            "status": a.status,
            "reason": a.reason,
            "visit_id": str(a.visit_id) if a.visit_id else None,
        }
        for a in appointments
    ])


@router.get(
    "/appointments",
    response_model=Envelope[list[dict]],
    summary="Get doctor's upcoming appointments",
)
async def get_doctor_appointments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[list[dict]]:
    """Return all upcoming confirmed/pending appointments for the logged-in doctor."""
    from datetime import date

    doctor_id = await _resolve_doctor_id(db, current_user.id)

    result = await db.execute(
        select(Appointment)
        .where(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date >= date.today(),
            Appointment.status.in_(["PENDING", "CONFIRMED"]),
        )
        .options(
            selectinload(Appointment.patient).selectinload(Patient.user),
            selectinload(Appointment.facility),
        )
        .order_by(Appointment.appointment_date, Appointment.allocated_start_time)
    )
    appointments = result.unique().scalars().all()

    return Envelope.ok([
        {
            "id": str(a.id),
            "patient_id": str(a.patient_id) if a.patient_id else None,
            "patient_name": (
                f"{a.patient.user.first_name} {a.patient.user.last_name}"
                if a.patient and a.patient.user else None
            ),
            "start_time": a.allocated_start_time.strftime("%H:%M") if a.allocated_start_time else "00:00",
            "end_time": a.allocated_end_time.strftime("%H:%M") if a.allocated_end_time else "00:00",
            "appointment_date": a.appointment_date.isoformat() if a.appointment_date else None,
            "duration_minutes": a.desired_duration_minutes,
            "status": a.status,
            "reason": a.reason,
            "facility_name": a.facility.name if a.facility else None,
        }
        for a in appointments
    ])


@router.get(
    "/{visit_id}",
    response_model=Envelope[VisitWithDetailsResponse],
    summary="Get consultation details",
    description="Return full visit with notes, diagnoses, medications, and AI sessions.",
)
async def get_consultation(
    visit_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[VisitWithDetailsResponse]:
    details = await service.get_consultation_details(db, visit_id, current_user)
    return Envelope.ok(details)


@router.post(
    "/{visit_id}/notes",
    response_model=Envelope[ClinicalNoteResponse],
    summary="Add clinical note",
    description="Add a SOAP note section to a visit.",
)
async def add_clinical_note(
    visit_id: uuid.UUID,
    body: ClinicalNoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[ClinicalNoteResponse]:
    doctor_id = await _resolve_doctor_id(db, current_user.id)
    note = await service.add_clinical_note(
        db, visit_id, doctor_id, body.note_type, body.content
    )
    return Envelope.ok(service._note_response(note))


@router.post(
    "/{visit_id}/diagnoses",
    response_model=Envelope[DiagnosisResponse],
    summary="Add diagnosis",
    description="Record a diagnosis (primary or secondary) for a visit.",
)
async def add_diagnosis(
    visit_id: uuid.UUID,
    body: DiagnosisCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[DiagnosisResponse]:
    doctor_id = await _resolve_doctor_id(db, current_user.id)
    diagnosis = await service.add_diagnosis(db, visit_id, doctor_id, body)
    return Envelope.ok(service._diagnosis_response(diagnosis))


@router.post(
    "/{visit_id}/medications",
    response_model=Envelope[MedicationResponse],
    summary="Prescribe medication",
    description="Prescribe a medication linked to the visit's patient.",
)
async def prescribe_medication(
    visit_id: uuid.UUID,
    body: MedicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[MedicationResponse]:
    doctor_id = await _resolve_doctor_id(db, current_user.id)
    medication = await service.prescribe_medication(db, visit_id, doctor_id, body)
    return Envelope.ok(service._medication_response(medication, visit_id))


@router.post(
    "/{visit_id}/complete",
    response_model=Envelope[VisitResponse],
    summary="Complete consultation",
    description="Mark the visit as 'completed'.",
)
async def complete_consultation(
    visit_id: uuid.UUID,
    body: ConsultationCompleteRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[VisitResponse]:
    doctor_id = await _resolve_doctor_id(db, current_user.id)
    visit = await service.complete_consultation(db, visit_id, doctor_id)
    return Envelope.ok(service._visit_response(visit))


@router.post(
    "/{visit_id}/cancel",
    response_model=Envelope[VisitResponse],
    summary="Cancel consultation",
    description="Mark the visit as 'cancelled' if still scheduled or in_progress.",
)
async def cancel_consultation(
    visit_id: uuid.UUID,
    body: ConsultationCancelRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[VisitResponse]:
    doctor_id = await _resolve_doctor_id(db, current_user.id)
    visit = await service.cancel_consultation(db, visit_id, doctor_id)
    return Envelope.ok(service._visit_response(visit))


@router.patch(
    "/{visit_id}/transcript",
    response_model=Envelope[VisitResponse],
    summary="Update visit transcript",
    description="Append or overwrite the transcript for a given visit.",
)
async def update_visit_transcript(
    visit_id: uuid.UUID,
    body: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[VisitResponse]:
    doctor_id = await _resolve_doctor_id(db, current_user.id)
    visit = await service.update_visit_transcript(db, visit_id, doctor_id, body)
    return Envelope.ok(service._visit_response(visit))


# ---------------------------------------------------------------------------
# Patient overview
# ---------------------------------------------------------------------------
@router.get(
    "/patient/{patient_id}",
    response_model=Envelope[PatientOverview],
    summary="Get patient overview",
    description="Requires approved consent.",
)
async def get_patient_overview(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[PatientOverview]:
    doctor_id = await _resolve_doctor_id(db, current_user.id)
    await check_record_access(db, doctor_id, patient_id)

    patient = await patient_repository.get_patient_full_profile(db, patient_id)
    if not patient:
        raise NotFoundException("Patient not found.", error_code="PATIENT_NOT_FOUND")

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

    # Current medications via visits
    current_medications = []
    if patient.medical_record:
        for visit in patient.medical_record.visits:
            for m in visit.medications:
                current_medications.append(
                    {
                        "id": str(m.id),
                        "name": m.name,
                        "dosage": m.dosage,
                        "frequency": m.frequency,
                        "instructions": m.instructions,
                        "start_date": m.start_date.isoformat() if m.start_date else None,
                    }
                )

    # Recent visits
    visits, _ = await service.list_visits_for_patient(db, patient_id, limit=5, offset=0)
    recent_visits = [service._visit_response(v) for v in visits]

    return Envelope.ok(
        PatientOverview(
            id=patient.id,
            medical_record_number=patient.medical_record_number,
            full_name=f"{patient.user.first_name or ''} {patient.user.last_name or ''}".strip(),
            national_identifier=patient.national_identifier,
            date_of_birth=patient.date_of_birth,
            gender=patient.gender,
            blood_type=patient.blood_type,
            phone=patient.user.phone_number if patient.user else None,
            email=patient.user.email if patient.user else None,
            emergency_contact_name=patient.emergency_contact_name,
            emergency_contact_phone=patient.emergency_contact_phone,
            allergies=allergies,
            conditions=conditions,
            current_medications=current_medications,
            recent_visits=recent_visits,
        )
    )


# ---------------------------------------------------------------------------
# Patient timeline (doctor view)
# ---------------------------------------------------------------------------
@router.get(
    "/patient/{patient_id}/timeline",
    response_model=Envelope[list[dict]],
    summary="Full timeline for a specific patient",
    description="Requires valid consent.",
)
async def get_patient_timeline(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[list[dict]]:
    doctor_id = await _resolve_doctor_id(db, current_user.id)
    await check_record_access(db, doctor_id, patient_id)

    # Import the me_router timeline building logic
    from app.patient.me_router import TimelineEvent

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

    events.sort(key=lambda e: e.date, reverse=True)
    return Envelope.ok([e.model_dump() for e in events])


# ---------------------------------------------------------------------------
# Patient AI sessions
# ---------------------------------------------------------------------------
def _ai_session_to_dict(session: AISession) -> dict:
    return {
        "id": str(session.id),
        "started_at": session.started_at.isoformat(),
        "status": session.status,
        "assessment_done": session.assessment_done,
        "confidence": session.confidence,
        "gaps_remaining": session.gaps_remaining,
        "candidate_domains": session.candidate_domains,
        "key_symptoms": session.key_symptoms,
        "missing_info": session.missing_info,
        "risk_flags": session.risk_flags,
        "messages": [
            {
                "id": str(m.id),
                "role": m.role,
                "content": m.content,
                "message_type": getattr(m, "message_type", None),
                "created_at": m.created_at.isoformat(),
            }
            for m in sorted(session.messages, key=lambda msg: msg.created_at)
        ],
        "appointment": {
            "id": str(session.appointment_id),
            "date": session.appointment.appointment_date.isoformat() if session.appointment else None,
            "time": (
                session.appointment.allocated_start_time.strftime("%H:%M")
                if session.appointment and session.appointment.allocated_start_time
                else None
            ),
            "status": session.appointment.status if session.appointment else None,
        } if session.appointment else None,
    }


@router.get(
    "/patient/{patient_id}/ai-sessions",
    response_model=Envelope[list[dict]],
    summary="Get patient's AI assessment sessions",
    description="Return all AI session details for a patient after consent is granted.",
)
async def get_patient_ai_sessions(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[list[dict]]:
    doctor_id = await _resolve_doctor_id(db, current_user.id)
    await check_record_access(db, doctor_id, patient_id)

    result = await db.execute(
        select(AISession)
        .options(selectinload(AISession.messages))
        .options(selectinload(AISession.appointment))
        .where(
            AISession.patient_id == patient_id,
            (AISession.doctor_id == doctor_id) | (AISession.appointment_id.is_not(None)),
        )
        .order_by(AISession.started_at.desc())
    )
    sessions = result.unique().scalars().all()
    return Envelope.ok([_ai_session_to_dict(s) for s in sessions])


# ---------------------------------------------------------------------------
# Create consultation for patient
# ---------------------------------------------------------------------------
@router.post(
    "/patient/{patient_id}/consultation",
    response_model=Envelope[dict],
    summary="Create a new consultation",
    status_code=201,
)
async def create_consultation_for_patient(
    patient_id: uuid.UUID,
    body: ConsultationStartRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[dict]:
    doctor_id = await _resolve_doctor_id(db, current_user.id)

    mr_result = await db.execute(
        select(MedicalRecord.id).where(MedicalRecord.patient_id == patient_id)
    )
    medical_record_id = mr_result.scalar_one_or_none()
    if not medical_record_id:
        raise NotFoundException(
            "Medical record not found for patient.", error_code="RECORD_NOT_FOUND"
        )

    visit = Visit(
        medical_record_id=medical_record_id,
        doctor_id=doctor_id,
        facility_id=body.facility_id,
        visit_date=datetime.now(),
        status="in_progress",
        chief_complaint=body.chief_complaint,
        reason=body.reason,
    )
    db.add(visit)
    await db.flush()
    await db.refresh(visit)

    return Envelope.ok(
        {
            "consultation_id": str(visit.id),
            "status": "ACTIVE",
        }
    )


@router.get(
    "/consultations/{visit_id}/pre-assessment",
    response_model=Envelope[dict],
    summary="View patient pre-assessment",
    description="Retrieve the AI pre-assessment responses submitted by the patient for the appointment linked to this visit. Only the assigned doctor can view it.",
)
async def get_pre_assessment(
    visit_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[dict]:
    """Return patient-initiated AI pre-assessment for a visit's appointment."""
    doctor_id = await _resolve_doctor_id(db, current_user.id)

    result = await db.execute(
        select(Visit)
        .options(selectinload(Visit.appointment))
        .where(Visit.id == visit_id)
    )
    visit = result.scalar_one_or_none()
    if not visit:
        raise NotFoundException("Visit not found.", error_code="VISIT_NOT_FOUND")
    if visit.doctor_id != doctor_id:
        raise ForbiddenException("You are not assigned to this consultation.")

    if not visit.appointment:
        return Envelope.ok({"available": False, "reason": "No appointment is linked to this visit."})

    ai_result = await db.execute(
        select(AISession)
        .where(
            AISession.appointment_id == visit.appointment.id,
            AISession.provider_metadata["initiated_by"].as_string() == "patient",
        )
        .order_by(AISession.started_at.desc())
    )
    session = ai_result.scalars().first()
    if not session:
        return Envelope.ok({"available": False, "reason": "The patient has not submitted a pre-assessment yet."})

    msg_result = await db.execute(
        select(AIMessage)
        .where(AIMessage.session_id == session.id)
        .order_by(AIMessage.created_at.asc())
    )
    messages = msg_result.scalars().all()

    return Envelope.ok(
        {
            "available": True,
            "session_id": str(session.id),
            "status": session.status,
            "started_at": session.started_at.isoformat() if session.started_at else None,
            "summary": session.conversation_summary,
            "messages": [
                {
                    "id": str(m.id),
                    "role": m.role,
                    "content": m.content,
                    "created_at": m.created_at.isoformat() if m.created_at else None,
                }
                for m in messages
            ],
        }
    )
