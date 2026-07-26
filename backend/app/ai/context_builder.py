#!/usr/bin/env python3
"""Context Builder — enriches AIContext with patient clinical data."""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.ai.provider import AIContext, PatientClinicalProfile
from app.db.models import (
    Allergy,
    ChronicCondition,
    ClinicalNote,
    Diagnosis,
    ImagingResult,
    LaboratoryResult,
    MedicalRecord,
    Medication,
    Patient,
    Visit,
)


def _calculate_age(dob: date | datetime | None) -> int | None:
    """Return age in years from a date/datetime of birth."""
    if dob is None:
        return None
    if isinstance(dob, datetime):
        dob = dob.date()
    today = date.today()
    return (
        today.year
        - dob.year
        - ((today.month, today.day) < (dob.month, dob.day))
    )


def _format_allergy(a: Allergy) -> dict:
    return {
        "allergen": a.allergen,
        "reaction": a.reaction,
        "severity": a.severity,
    }


def _format_chronic_condition(c: ChronicCondition) -> dict:
    return {
        "name": c.condition_name,
        "status": c.status,
    }


def _format_medication(m: Medication) -> dict:
    return {
        "name": m.name,
        "dosage": m.dosage,
        "frequency": m.frequency,
        "duration": m.duration,
        "instructions": m.instructions,
        "start_date": m.start_date.isoformat() if m.start_date else None,
        "end_date": m.end_date.isoformat() if m.end_date else None,
    }


def _format_diagnosis(d: Diagnosis) -> dict:
    return {
        "name": d.diagnosis_name,
        "icd10_code": d.icd10_code,
        "primary": d.primary_diagnosis,
        "confidence": float(d.confidence) if d.confidence is not None else None,
        "notes": d.notes,
    }


def _format_lab_result(lr: LaboratoryResult) -> dict:
    return {
        "test_name": lr.test_name,
        "result": lr.result,
        "reference_range": lr.reference_range,
        "status": lr.status,
        "performed_at": lr.performed_at.isoformat() if lr.performed_at else None,
    }


def _format_imaging_result(ir: ImagingResult) -> dict:
    return {
        "modality": ir.modality,
        "study_name": ir.study_name,
        "report": ir.report,
        "performed_at": ir.performed_at.isoformat() if ir.performed_at else None,
    }


def _format_clinical_note(cn: ClinicalNote) -> dict:
    return {
        "subjective": cn.subjective,
        "objective": cn.objective,
        "assessment": cn.assessment,
        "plan": cn.plan,
        "is_finalized": cn.is_finalized,
        "created_at": cn.created_at.isoformat() if cn.created_at else None,
    }


def _format_visit(v: Visit) -> dict:
    return {
        "visit_id": str(v.id),
        "visit_date": v.visit_date.isoformat() if v.visit_date else None,
        "status": v.status,
        "reason": v.reason,
        "chief_complaint": v.chief_complaint,
        "summary": v.summary,
        "ai_summary": v.ai_summary,
        "follow_up_required": v.follow_up_required,
        "medications": [_format_medication(m) for m in v.medications],
        "diagnoses": [_format_diagnosis(d) for d in v.diagnoses],
        "laboratory_results": [_format_lab_result(lr) for lr in v.laboratory_results],
        "imaging_results": [_format_imaging_result(ir) for ir in v.imaging_results],
        "clinical_notes": [_format_clinical_note(cn) for cn in v.clinical_notes],
    }


async def enrich_context_with_patient_data(
    db: AsyncSession,
    context: AIContext,
) -> AIContext:
    """Populate *clinical_profile* on *context* from the database.

    - Returns the original context unchanged when *patient_id* is missing.
    - In **patient mode** (*doctor_id* is ``None``) the full profile is built.
    - In **doctor mode** fields are included only when the corresponding consent
      scope is present in *available_data*.
    """
    if context.patient_id is None:
        return context

    # ------------------------------------------------------------------
    # Load patient and eagerly fetch the entire clinical graph
    # ------------------------------------------------------------------
    stmt = (
        select(Patient)
        .options(joinedload(Patient.user))
        .options(
            selectinload(Patient.medical_record).selectinload(MedicalRecord.allergies)
        )
        .options(
            selectinload(Patient.medical_record).selectinload(
                MedicalRecord.chronic_conditions
            )
        )
        .options(
            selectinload(Patient.medical_record)
            .selectinload(MedicalRecord.visits)
            .selectinload(Visit.medications)
        )
        .options(
            selectinload(Patient.medical_record)
            .selectinload(MedicalRecord.visits)
            .selectinload(Visit.diagnoses)
        )
        .options(
            selectinload(Patient.medical_record)
            .selectinload(MedicalRecord.visits)
            .selectinload(Visit.laboratory_results)
        )
        .options(
            selectinload(Patient.medical_record)
            .selectinload(MedicalRecord.visits)
            .selectinload(Visit.imaging_results)
        )
        .options(
            selectinload(Patient.medical_record)
            .selectinload(MedicalRecord.visits)
            .selectinload(Visit.clinical_notes)
        )
        .options(selectinload(Patient.ai_sessions))
        .where(Patient.id == context.patient_id)
    )
    result = await db.execute(stmt)
    patient = result.unique().scalar_one_or_none()

    if patient is None:
        return context

    # ------------------------------------------------------------------
    # Determine which scopes are available
    # ------------------------------------------------------------------
    scopes = set(context.available_data or [])
    is_patient_mode = context.doctor_id is None

    def _allowed(scope: str) -> bool:
        return is_patient_mode or scope in scopes

    # ------------------------------------------------------------------
    # Demographics
    # ------------------------------------------------------------------
    demographics: dict | None = None
    if _allowed("medical_record") or _allowed("demographics"):
        demographics = {
            "age": _calculate_age(patient.date_of_birth),
            "gender": patient.gender,
            "blood_type": patient.blood_type,
        }

    # ------------------------------------------------------------------
    # Allergies & Chronic Conditions
    # ------------------------------------------------------------------
    allergies: list[dict] = []
    chronic_conditions: list[dict] = []
    record = patient.medical_record
    if record is not None:
        if _allowed("medical_record") or _allowed("allergies"):
            allergies = [_format_allergy(a) for a in record.allergies]
        if _allowed("medical_record") or _allowed("chronic_conditions"):
            chronic_conditions = [
                _format_chronic_condition(c) for c in record.chronic_conditions
            ]

    # ------------------------------------------------------------------
    # Visits & derived data (medications, diagnoses, labs, imaging, notes)
    # ------------------------------------------------------------------
    recent_visits: list[dict] = []
    current_medications: list[dict] = []
    if record is not None and (
        is_patient_mode
        or scopes.intersection(
            {
                "medical_record",
                "visits",
                "timeline",
                "medications",
                "diagnoses",
                "lab_results",
                "imaging",
                "clinical_notes",
            }
        )
    ):
        visits = sorted(record.visits, key=lambda v: v.visit_date or datetime.min)
        for visit in visits:
            visit_dict = _format_visit(visit)
            # Filter nested visit data by scope in doctor mode
            if not is_patient_mode:
                if not _allowed("medications"):
                    visit_dict["medications"] = []
                if not _allowed("diagnoses"):
                    visit_dict["diagnoses"] = []
                if not _allowed("lab_results"):
                    visit_dict["laboratory_results"] = []
                if not _allowed("imaging"):
                    visit_dict["imaging_results"] = []
                if not _allowed("clinical_notes"):
                    visit_dict["clinical_notes"] = []
            recent_visits.append(visit_dict)
            current_medications.extend(visit_dict["medications"])

    # ------------------------------------------------------------------
    # Previous AI sessions
    # ------------------------------------------------------------------
    previous_ai_sessions: list[dict] = []
    if _allowed("ai_history") or is_patient_mode:
        previous_ai_sessions = [
            {
                "session_id": str(s.id),
                "started_at": s.started_at.isoformat() if s.started_at else None,
                "status": s.status,
                "conversation_summary": s.conversation_summary,
            }
            for s in patient.ai_sessions
            if s.id != context.session_id
        ]

    # ------------------------------------------------------------------
    # Assemble profile
    # ------------------------------------------------------------------
    context.clinical_profile = PatientClinicalProfile(
        demographics=demographics,
        allergies=allergies,
        chronic_conditions=chronic_conditions,
        current_medications=current_medications,
        recent_visits=recent_visits,
        previous_ai_sessions=previous_ai_sessions,
    )
    return context
