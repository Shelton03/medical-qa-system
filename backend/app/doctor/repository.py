#!/usr/bin/env python3
"""Mirage Consultation repository — async CRUD for Visit, ClinicalNote, Diagnosis, Medication."""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import (
    ClinicalNote,
    Diagnosis,
    MedicalRecord,
    Visit,
)
from app.db.models import Medication as LegacyMedication
from app.doctor.schemas import (
    DiagnosisCreate,
    MedicationCreate,
)


# ---------------------------------------------------------------------------
# Visit
# ---------------------------------------------------------------------------
async def create_visit(
    db: AsyncSession,
    *,
    medical_record_id: uuid.UUID,
    doctor_id: uuid.UUID,
    facility_id: uuid.UUID | None,
    chief_complaint: str | None,
    reason: str | None,
) -> Visit:
    """Persist a new Visit with status 'in_progress'."""
    visit = Visit(
        medical_record_id=medical_record_id,
        doctor_id=doctor_id,
        facility_id=facility_id,
        visit_date=datetime.now(timezone.utc),
        status="in_progress",
        chief_complaint=chief_complaint,
        reason=reason,
    )
    db.add(visit)
    await db.flush()
    await db.refresh(visit)
    result = await db.execute(
        select(Visit)
        .options(selectinload(Visit.medical_record))
        .where(Visit.id == visit.id)
    )
    return result.scalar_one()


async def get_visit_by_id(db: AsyncSession, visit_id: uuid.UUID) -> Visit | None:
    """Fetch a single visit with eagerly loaded relationships."""
    result = await db.execute(
        select(Visit)
        .options(selectinload(Visit.medical_record))
        .options(selectinload(Visit.clinical_notes))
        .options(selectinload(Visit.diagnoses))
        .options(selectinload(Visit.ai_sessions))
        .options(selectinload(Visit.doctor))
        .options(selectinload(Visit.facility))
        .where(Visit.id == visit_id)
    )
    return result.unique().scalar_one_or_none()


async def list_visits_for_doctor(
    db: AsyncSession,
    doctor_id: uuid.UUID,
    limit: int,
    offset: int,
    status: str | None = None,
) -> tuple[list[Visit], int]:
    """Return paginated visits for a doctor."""
    stmt = select(Visit).options(selectinload(Visit.medical_record)).where(Visit.doctor_id == doctor_id)
    count_stmt = (
        select(func.count()).select_from(Visit).where(Visit.doctor_id == doctor_id)
    )
    if status:
        stmt = stmt.where(Visit.status == status)
        count_stmt = count_stmt.where(Visit.status == status)
    stmt = stmt.order_by(Visit.visit_date.desc()).offset(offset).limit(limit)
    result = await db.execute(stmt)
    total_result = await db.execute(count_stmt)
    return list(result.scalars().all()), total_result.scalar_one()


async def list_visits_for_patient(
    db: AsyncSession,
    patient_id: uuid.UUID,
    limit: int,
    offset: int,
    status: str | None = None,
) -> tuple[list[Visit], int]:
    """Return paginated visits for a patient (resolved via medical_record)."""
    mr_result = await db.execute(
        select(MedicalRecord.id).where(MedicalRecord.patient_id == patient_id)
    )
    medical_record_id = mr_result.scalar_one_or_none()
    if not medical_record_id:
        return [], 0

    stmt = select(Visit).options(selectinload(Visit.medical_record)).where(Visit.medical_record_id == medical_record_id)
    count_stmt = (
        select(func.count())
        .select_from(Visit)
        .where(Visit.medical_record_id == medical_record_id)
    )
    if status:
        stmt = stmt.where(Visit.status == status)
        count_stmt = count_stmt.where(Visit.status == status)
    stmt = stmt.order_by(Visit.visit_date.desc()).offset(offset).limit(limit)
    result = await db.execute(stmt)
    total_result = await db.execute(count_stmt)
    return list(result.scalars().all()), total_result.scalar_one()


async def update_visit_status(
    db: AsyncSession,
    visit_id: uuid.UUID,
    status: str,
) -> Visit | None:
    """Update the status of a visit."""
    visit = await get_visit_by_id(db, visit_id)
    if visit is None:
        return None
    visit.status = status
    db.add(visit)
    await db.flush()
    await db.refresh(visit)
    return visit


async def update_visit_transcript(
    db: AsyncSession,
    visit_id: uuid.UUID,
    transcript: str,
) -> Visit | None:
    """Update the transcript field of a visit."""
    visit = await get_visit_by_id(db, visit_id)
    if visit is None:
        return None
    visit.transcript = transcript
    db.add(visit)
    await db.flush()
    await db.refresh(visit)
    return visit


# ---------------------------------------------------------------------------
# Clinical Note
# ---------------------------------------------------------------------------
async def create_clinical_note(
    db: AsyncSession,
    visit_id: uuid.UUID,
    doctor_id: uuid.UUID,
    note_type: str,
    content: str,
) -> ClinicalNote:
    """Create a new ClinicalNote row populating the relevant SOAP field."""
    note = ClinicalNote(
        visit_id=visit_id,
        doctor_id=doctor_id,
        **{note_type: content},
    )
    db.add(note)
    await db.flush()
    await db.refresh(note)
    return note


async def get_clinical_notes_for_visit(
    db: AsyncSession,
    visit_id: uuid.UUID,
) -> list[ClinicalNote]:
    """Return all clinical notes for a visit, newest first."""
    result = await db.execute(
        select(ClinicalNote)
        .where(ClinicalNote.visit_id == visit_id)
        .order_by(ClinicalNote.created_at.desc())
    )
    return list(result.scalars().all())


async def update_clinical_note(
    db: AsyncSession,
    note_id: uuid.UUID,
    note_type: str,
    content: str,
) -> ClinicalNote | None:
    """Update a single SOAP field on an existing note."""
    note = await db.get(ClinicalNote, note_id)
    if note is None:
        return None
    setattr(note, note_type, content)
    db.add(note)
    await db.flush()
    await db.refresh(note)
    return note


# ---------------------------------------------------------------------------
# Diagnosis
# ---------------------------------------------------------------------------
async def create_diagnosis(
    db: AsyncSession,
    visit_id: uuid.UUID,
    data: DiagnosisCreate,
) -> Diagnosis:
    """Persist a new Diagnosis linked to a visit."""
    notes = data.notes or ""
    if data.status:
        notes = f"[{data.status.upper()}] {notes}".strip()
    diagnosis = Diagnosis(
        visit_id=visit_id,
        diagnosis_name=data.diagnosis_name,
        icd10_code=data.icd10_code,
        primary_diagnosis=(data.type == "primary"),
        notes=notes,
    )
    db.add(diagnosis)
    await db.flush()
    await db.refresh(diagnosis)
    return diagnosis


async def list_diagnoses_for_visit(
    db: AsyncSession,
    visit_id: uuid.UUID,
) -> list[Diagnosis]:
    """Return all diagnoses for a visit, newest first."""
    result = await db.execute(
        select(Diagnosis)
        .where(Diagnosis.visit_id == visit_id)
        .order_by(Diagnosis.created_at.desc())
    )
    return list(result.scalars().all())


# ---------------------------------------------------------------------------
# Medication (LegacyMedication for DB compatibility with seeded data)
# ---------------------------------------------------------------------------
async def create_medication(
    db: AsyncSession,
    visit_id: uuid.UUID,
    data: MedicationCreate,
) -> LegacyMedication:
    """Persist a medication linked via the visit's medical_record_id."""
    visit_result = await db.execute(
        select(Visit.medical_record_id).where(Visit.id == visit_id)
    )
    medical_record_id = visit_result.scalar_one_or_none()
    if not medical_record_id:
        raise ValueError("Visit not found or missing medical record.")

    medication = LegacyMedication(
        medical_record_id=medical_record_id,
        name=data.name,
        dosage=data.dosage,
        frequency=data.frequency,
        duration=data.duration,
        instructions=data.instructions,
        start_date=data.start_date,
        end_date=data.end_date,
    )
    db.add(medication)
    await db.flush()
    await db.refresh(medication)
    return medication


async def list_medications_for_visit(
    db: AsyncSession,
    visit_id: uuid.UUID,
) -> list[LegacyMedication]:
    """Return medications prescribed during a specific visit."""
    result = await db.execute(
        select(LegacyMedication).where(LegacyMedication.visit_id == visit_id)
    )
    return list(result.scalars().all())


async def update_medication_status(
    db: AsyncSession,
    medication_id: uuid.UUID,
    status: str,
) -> LegacyMedication | None:
    """Encode status into the instructions field (no dedicated status column exists)."""
    medication = await db.get(LegacyMedication, medication_id)
    if medication is None:
        return None

    instructions = medication.instructions or ""
    # Strip any existing status prefix
    instructions = re.sub(
        r"^\[(active|discontinued|completed)\]\s*",
        "",
        instructions,
        flags=re.IGNORECASE,
    )
    instructions = f"[{status}] {instructions}".strip()
    medication.instructions = instructions
    db.add(medication)
    await db.flush()
    await db.refresh(medication)
    return medication
