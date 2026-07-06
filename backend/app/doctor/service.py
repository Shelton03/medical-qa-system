#!/usr/bin/env python3
"""Mirage Consultation service layer — business logic, consent checks, and audit logging."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import (
    AuditLog,
    ClinicalNote,
    Diagnosis,
    Doctor as DoctorModel,
    MedicalRecord,
    Patient,
    Visit,
)
from app.db.models import Medication as LegacyMedication
from app.db.models import User
from app.consent.service import check_record_access
from app.doctor import repository
from app.doctor.schemas import (
    AISessionBriefResponse,
    ClinicalNoteResponse,
    DiagnosisCreate,
    DiagnosisResponse,
    MedicationCreate,
    MedicationResponse,
    VisitCreate,
    VisitResponse,
    VisitWithDetailsResponse,
)
from app.shared.exceptions import ConflictException, ForbiddenException, NotFoundException
from app.websocket.events import WSEventType
from app.websocket.publisher import emit_ws_event


# ---------------------------------------------------------------------------
# Audit helper
# ---------------------------------------------------------------------------
async def _write_audit_log(
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


# ---------------------------------------------------------------------------
# Visit / Consultation
# ---------------------------------------------------------------------------
async def start_consultation(
    db: AsyncSession,
    doctor_id: uuid.UUID,
    data: VisitCreate,
) -> Visit:
    """Validate consent, resolve medical record, and create visit with status 'in_progress'."""
    await check_record_access(db, doctor_id, data.patient_id)

    mr_result = await db.execute(
        select(MedicalRecord.id).where(MedicalRecord.patient_id == data.patient_id)
    )
    medical_record_id = mr_result.scalar_one_or_none()
    if not medical_record_id:
        raise NotFoundException(
            "Medical record not found for patient.", error_code="RECORD_NOT_FOUND"
        )

    async with db.begin():
        visit = await repository.create_visit(
            db,
            medical_record_id=medical_record_id,
            doctor_id=doctor_id,
            facility_id=data.facility_id,
            chief_complaint=data.chief_complaint,
            reason=data.reason,
        )
        await _write_audit_log(
            db,
            user_id=doctor_id,
            action="CONSULTATION_STARTED",
            resource_type="Visit",
            resource_id=visit.id,
            metadata={
                "patient_id": str(data.patient_id),
                "chief_complaint": data.chief_complaint,
            },
        )
    await emit_ws_event(
        f"patient:{data.patient_id}",
        WSEventType.CONSULTATION_STARTED,
        {
            "visit_id": str(visit.id),
            "patient_id": str(data.patient_id),
            "doctor_id": str(doctor_id),
            "status": visit.status,
        },
    )
    return visit


async def get_consultation_details(
    db: AsyncSession,
    visit_id: uuid.UUID,
    requesting_user: User,
) -> VisitWithDetailsResponse:
    """Return full visit details with authorization enforcement."""
    visit = await repository.get_visit_by_id(db, visit_id)
    if not visit:
        raise NotFoundException("Visit not found.", error_code="VISIT_NOT_FOUND")

    patient_id = visit.medical_record.patient_id if visit.medical_record else None

    if requesting_user.role == "patient":
        patient_result = await db.execute(
            select(Patient.id).where(Patient.user_id == requesting_user.id)
        )
        user_patient_id = patient_result.scalar_one_or_none()
        if patient_id != user_patient_id:
            raise ForbiddenException("You can only view your own visits.")
    elif requesting_user.role == "doctor":
        doctor_result = await db.execute(
            select(DoctorModel.id).where(DoctorModel.user_id == requesting_user.id)
        )
        user_doctor_id = doctor_result.scalar_one_or_none()
        if visit.doctor_id != user_doctor_id:
            if patient_id:
                await check_record_access(db, user_doctor_id, patient_id)
            else:
                raise ForbiddenException(
                    "You are not authorized to view this visit."
                )
    # Admins bypass additional checks

    notes = await repository.get_clinical_notes_for_visit(db, visit_id)
    diagnoses = await repository.list_diagnoses_for_visit(db, visit_id)
    medications = await repository.list_medications_for_visit(db, visit_id)

    return _visit_with_details(visit, notes, diagnoses, medications)


async def list_visits_for_doctor(
    db: AsyncSession,
    doctor_id: uuid.UUID,
    limit: int,
    offset: int,
    status: str | None = None,
) -> tuple[list[Visit], int]:
    """Return paginated visits for a doctor."""
    return await repository.list_visits_for_doctor(
        db, doctor_id, limit, offset, status
    )


async def list_visits_for_patient(
    db: AsyncSession,
    patient_id: uuid.UUID,
    limit: int,
    offset: int,
    status: str | None = None,
) -> tuple[list[Visit], int]:
    """Return paginated visits for a patient."""
    return await repository.list_visits_for_patient(
        db, patient_id, limit, offset, status
    )


async def complete_consultation(
    db: AsyncSession,
    visit_id: uuid.UUID,
    doctor_id: uuid.UUID,
) -> Visit:
    """Mark visit 'completed' and write audit log."""
    visit = await repository.get_visit_by_id(db, visit_id)
    if not visit:
        raise NotFoundException("Visit not found.", error_code="VISIT_NOT_FOUND")
    if visit.doctor_id != doctor_id:
        raise ForbiddenException("You are not the doctor for this visit.")
    if visit.status not in ("scheduled", "in_progress"):
        raise ConflictException(
            f"Cannot complete a visit with status {visit.status}."
        )

    async with db.begin():
        visit = await repository.update_visit_status(db, visit_id, "completed")
        if not visit:
            raise NotFoundException("Visit not found.", error_code="VISIT_NOT_FOUND")
        await _write_audit_log(
            db,
            user_id=doctor_id,
            action="CONSULTATION_COMPLETED",
            resource_type="Visit",
            resource_id=visit.id,
        )
    if visit.medical_record:
        await emit_ws_event(
            f"patient:{visit.medical_record.patient_id}",
            WSEventType.CONSULTATION_COMPLETED,
            {
                "visit_id": str(visit.id),
                "patient_id": str(visit.medical_record.patient_id),
                "doctor_id": str(doctor_id),
                "status": visit.status,
            },
        )
    return visit


async def cancel_consultation(
    db: AsyncSession,
    visit_id: uuid.UUID,
    doctor_id: uuid.UUID,
) -> Visit:
    """Mark visit 'cancelled' if still scheduled or in_progress."""
    visit = await repository.get_visit_by_id(db, visit_id)
    if not visit:
        raise NotFoundException("Visit not found.", error_code="VISIT_NOT_FOUND")
    if visit.doctor_id != doctor_id:
        raise ForbiddenException("You are not the doctor for this visit.")
    if visit.status not in ("scheduled", "in_progress"):
        raise ConflictException(
            f"Cannot cancel a visit with status {visit.status}."
        )

    async with db.begin():
        visit = await repository.update_visit_status(db, visit_id, "cancelled")
        if not visit:
            raise NotFoundException("Visit not found.", error_code="VISIT_NOT_FOUND")
        await _write_audit_log(
            db,
            user_id=doctor_id,
            action="CONSULTATION_CANCELLED",
            resource_type="Visit",
            resource_id=visit.id,
        )
    return visit


# ---------------------------------------------------------------------------
# Clinical Notes
# ---------------------------------------------------------------------------
async def add_clinical_note(
    db: AsyncSession,
    visit_id: uuid.UUID,
    doctor_id: uuid.UUID,
    note_type: str,
    content: str,
) -> ClinicalNote:
    """Add a clinical note to a visit."""
    visit = await repository.get_visit_by_id(db, visit_id)
    if not visit:
        raise NotFoundException("Visit not found.", error_code="VISIT_NOT_FOUND")
    if visit.doctor_id != doctor_id:
        raise ForbiddenException("You are not the doctor for this visit.")
    if note_type not in ("subjective", "objective", "assessment", "plan"):
        raise ConflictException(f"Invalid note type: {note_type}.")

    return await repository.create_clinical_note(
        db, visit_id, doctor_id, note_type, content
    )


async def update_clinical_note(
    db: AsyncSession,
    note_id: uuid.UUID,
    doctor_id: uuid.UUID,
    note_type: str,
    content: str,
) -> ClinicalNote:
    """Update an existing clinical note."""
    note = await repository.update_clinical_note(db, note_id, note_type, content)
    if not note:
        raise NotFoundException("Clinical note not found.", error_code="NOT_FOUND")
    if note.doctor_id != doctor_id:
        raise ForbiddenException("You are not the doctor for this note.")
    return note


# ---------------------------------------------------------------------------
# Diagnosis
# ---------------------------------------------------------------------------
async def add_diagnosis(
    db: AsyncSession,
    visit_id: uuid.UUID,
    doctor_id: uuid.UUID,
    data: DiagnosisCreate,
) -> Diagnosis:
    """Add a diagnosis to a visit."""
    visit = await repository.get_visit_by_id(db, visit_id)
    if not visit:
        raise NotFoundException("Visit not found.", error_code="VISIT_NOT_FOUND")
    if visit.doctor_id != doctor_id:
        raise ForbiddenException("You are not the doctor for this visit.")

    return await repository.create_diagnosis(db, visit_id, data)


# ---------------------------------------------------------------------------
# Medication
# ---------------------------------------------------------------------------
async def prescribe_medication(
    db: AsyncSession,
    visit_id: uuid.UUID,
    doctor_id: uuid.UUID,
    data: MedicationCreate,
) -> LegacyMedication:
    """Prescribe a medication for a visit."""
    visit = await repository.get_visit_by_id(db, visit_id)
    if not visit:
        raise NotFoundException("Visit not found.", error_code="VISIT_NOT_FOUND")
    if visit.doctor_id != doctor_id:
        raise ForbiddenException("You are not the doctor for this visit.")

    return await repository.create_medication(db, visit_id, data)


async def update_medication_status(
    db: AsyncSession,
    medication_id: uuid.UUID,
    doctor_id: uuid.UUID,
    status: str,
) -> LegacyMedication:
    """Update medication status (active, discontinued, completed)."""
    medication = await repository.update_medication_status(db, medication_id, status)
    if not medication:
        raise NotFoundException("Medication not found.", error_code="NOT_FOUND")
    return medication


# ---------------------------------------------------------------------------
# Response mappers
# ---------------------------------------------------------------------------
def _visit_response(visit: Visit) -> VisitResponse:
    patient_id = visit.medical_record.patient_id if visit.medical_record else None
    return VisitResponse(
        id=visit.id,
        patient_id=patient_id,
        doctor_id=visit.doctor_id,
        facility_id=visit.facility_id,
        visit_date=visit.visit_date,
        status=visit.status,
        reason=visit.reason,
        chief_complaint=visit.chief_complaint,
        summary=visit.summary,
        ai_summary=visit.ai_summary,
        follow_up_required=visit.follow_up_required or False,
        created_at=visit.created_at,
        updated_at=visit.updated_at,
    )


def _note_response(note: ClinicalNote) -> ClinicalNoteResponse:
    return ClinicalNoteResponse(
        id=note.id,
        visit_id=note.visit_id,
        doctor_id=note.doctor_id,
        subjective=note.subjective,
        objective=note.objective,
        assessment=note.assessment,
        plan=note.plan,
        is_finalized=note.is_finalized,
        created_at=note.created_at,
        updated_at=note.updated_at,
    )


def _diagnosis_response(d: Diagnosis) -> DiagnosisResponse:
    return DiagnosisResponse(
        id=d.id,
        visit_id=d.visit_id,
        diagnosis_name=d.diagnosis_name,
        icd10_code=d.icd10_code,
        confidence=d.confidence,
        primary_diagnosis=d.primary_diagnosis or False,
        notes=d.notes,
        created_at=d.created_at,
    )


def _medication_response(
    m: LegacyMedication,
    visit_id: uuid.UUID | None = None,
) -> MedicationResponse:
    import re

    instructions = m.instructions or ""
    status: str | None = None
    match = re.match(r"^\[(active|discontinued|completed)\]\s*", instructions, re.IGNORECASE)
    if match:
        status = match.group(1).lower()
        instructions = instructions[match.end() :].strip()

    return MedicationResponse(
        id=m.id,
        visit_id=visit_id,
        name=m.name,
        dosage=m.dosage,
        frequency=m.frequency,
        duration=m.duration,
        instructions=instructions,
        status=status,
        start_date=m.start_date,
        end_date=m.end_date,
        created_at=m.created_at,
    )


def _visit_with_details(
    visit: Visit,
    notes: list[ClinicalNote],
    diagnoses: list[Diagnosis],
    medications: list[LegacyMedication],
) -> VisitWithDetailsResponse:
    patient_id = visit.medical_record.patient_id if visit.medical_record else None
    ai_sessions = [
        AISessionBriefResponse(
            id=s.id,
            provider_name=s.provider_name,
            status=s.status,
            started_at=s.started_at,
        )
        for s in (visit.ai_sessions or [])
    ]
    return VisitWithDetailsResponse(
        id=visit.id,
        patient_id=patient_id,
        doctor_id=visit.doctor_id,
        facility_id=visit.facility_id,
        visit_date=visit.visit_date,
        status=visit.status,
        reason=visit.reason,
        chief_complaint=visit.chief_complaint,
        summary=visit.summary,
        ai_summary=visit.ai_summary,
        follow_up_required=visit.follow_up_required or False,
        created_at=visit.created_at,
        updated_at=visit.updated_at,
        clinical_notes=[_note_response(n) for n in notes],
        diagnoses=[_diagnosis_response(d) for d in diagnoses],
        medications=[_medication_response(m, visit.id) for m in medications],
        ai_sessions=ai_sessions,
    )
