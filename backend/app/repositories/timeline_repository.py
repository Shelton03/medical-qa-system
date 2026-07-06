"""TimelineRepository — query timeline events across visits, diagnoses, etc."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Visit, Diagnosis, Medication, LaboratoryResult, ImagingResult, ClinicalNote, ConsentRequest


async def get_timeline_for_patient(
    db: AsyncSession,
    patient_id: uuid.UUID,
    limit: int = 50,
    offset: int = 0,
) -> list[dict]:
    """
    Build a chronological timeline for a patient from visits and related entities.

    Returns a list of lightweight event dicts ordered by date descending.
    """
    # Fetch visits for this patient via medical_records
    from app.db.models import MedicalRecord
    mr_result = await db.execute(
        select(MedicalRecord.id).where(MedicalRecord.patient_id == patient_id)
    )
    medical_record_ids = [row for row in mr_result.scalars().all()]

    if not medical_record_ids:
        return []

    visit_stmt = (
        select(Visit)
        .where(Visit.medical_record_id.in_(medical_record_ids))
        .order_by(Visit.visit_date.desc())
        .offset(offset)
        .limit(limit)
    )
    visit_result = await db.execute(visit_stmt)
    visits = visit_result.scalars().all()

    events: list[dict] = []
    for visit in visits:
        events.append({
            "event_id": str(visit.id),
            "event_type": "VISIT",
            "date": visit.visit_date.isoformat() if visit.visit_date else None,
            "facility": visit.facility.name if visit.facility else None,
            "doctor": (
                f"{visit.doctor.user.first_name} {visit.doctor.user.last_name}".strip()
                if visit.doctor and visit.doctor.user else None
            ),
            "summary": visit.summary,
            "status": visit.status,
            "metadata": {
                "chief_complaint": visit.chief_complaint,
                "reason": visit.reason,
            },
        })

        for diagnosis in (visit.diagnoses or []):
            events.append({
                "event_id": str(diagnosis.id),
                "event_type": "DIAGNOSIS",
                "date": visit.visit_date.isoformat() if visit.visit_date else None,
                "facility": visit.facility.name if visit.facility else None,
                "doctor": None,
                "summary": diagnosis.diagnosis_name,
                "status": "confirmed" if diagnosis.primary_diagnosis else "suspected",
                "metadata": {
                    "icd10_code": diagnosis.icd10_code,
                    "confidence": float(diagnosis.confidence) if diagnosis.confidence else None,
                },
            })

        for med in (visit.medications or []):
            events.append({
                "event_id": str(med.id),
                "event_type": "PRESCRIPTION",
                "date": visit.visit_date.isoformat() if visit.visit_date else None,
                "facility": None,
                "doctor": None,
                "summary": med.name,
                "status": "active",
                "metadata": {
                    "dosage": med.dosage,
                    "frequency": med.frequency,
                    "duration": med.duration,
                },
            })

    # Sort all events by date descending
    events.sort(
        key=lambda e: datetime.fromisoformat(e["date"]) if e["date"] else datetime.min,
        reverse=True,
    )
    return events
