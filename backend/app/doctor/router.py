#!/usr/bin/env python3
"""Mirage Consultation API router."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.auth.dependencies import get_current_user, get_current_doctor
from app.db.models import Doctor, Patient
from app.models.user import User
from app.schemas.envelope import Envelope
from app.shared.exceptions import NotFoundException, ForbiddenException
from app.doctor import service
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

router = APIRouter()


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
    status: Annotated[str | None, Query(None, description="Filter by status")] = None,
    limit: Annotated[int, Query(20, ge=1, le=100)] = 20,
    offset: Annotated[int, Query(0, ge=0)] = 0,
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
