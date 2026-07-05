#!/usr/bin/env python3
"""Mirage Consultation (Doctor) Pydantic schemas."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class MirageBaseModel(BaseModel):
    """Base schema with ORM mode enabled."""

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Visit
# ---------------------------------------------------------------------------
class VisitCreate(MirageBaseModel):
    patient_id: uuid.UUID
    chief_complaint: str | None = Field(None, description="Patient's primary complaint.")
    reason: str | None = Field(None, description="Reason for the consultation.")
    facility_id: uuid.UUID | None = Field(None, description="Optional facility ID.")


class VisitResponse(MirageBaseModel):
    id: uuid.UUID
    patient_id: uuid.UUID | None = Field(None, description="Resolved from medical record.")
    doctor_id: uuid.UUID
    facility_id: uuid.UUID | None = None
    visit_date: datetime
    status: str
    reason: str | None = None
    chief_complaint: str | None = None
    summary: str | None = None
    ai_summary: str | None = None
    follow_up_required: bool = False
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# Clinical Note
# ---------------------------------------------------------------------------
class ClinicalNoteCreate(MirageBaseModel):
    note_type: str = Field(
        ...,
        pattern="^(subjective|objective|assessment|plan)$",
        description="SOAP section to populate.",
    )
    content: str = Field(..., description="Note content (supports structured JSON for future AI parsing).")


class ClinicalNoteResponse(MirageBaseModel):
    id: uuid.UUID
    visit_id: uuid.UUID
    doctor_id: uuid.UUID
    subjective: str | None = None
    objective: str | None = None
    assessment: str | None = None
    plan: str | None = None
    is_finalized: bool = False
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# Diagnosis
# ---------------------------------------------------------------------------
class DiagnosisCreate(MirageBaseModel):
    diagnosis_name: str = Field(..., max_length=500)
    icd10_code: str | None = Field(None, max_length=20)
    type: str = Field("secondary", pattern="^(primary|secondary)$")
    status: str = Field("confirmed", pattern="^(confirmed|suspected|ruled_out)$")
    notes: str | None = None


class DiagnosisResponse(MirageBaseModel):
    id: uuid.UUID
    visit_id: uuid.UUID
    diagnosis_name: str
    icd10_code: str | None = None
    confidence: Decimal | None = None
    primary_diagnosis: bool = False
    notes: str | None = None
    created_at: datetime


# ---------------------------------------------------------------------------
# Medication
# ---------------------------------------------------------------------------
class MedicationCreate(MirageBaseModel):
    name: str = Field(..., max_length=255)
    dosage: str | None = Field(None, max_length=255)
    frequency: str | None = Field(None, max_length=255)
    duration: str | None = Field(None, max_length=255)
    instructions: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class MedicationResponse(MirageBaseModel):
    id: uuid.UUID
    visit_id: uuid.UUID | None = None
    name: str
    dosage: str | None = None
    frequency: str | None = None
    duration: str | None = None
    instructions: str | None = None
    status: str | None = Field(None, description="Derived from instructions prefix if present.")
    start_date: date | None = None
    end_date: date | None = None
    created_at: datetime


# ---------------------------------------------------------------------------
# AI Session (nested brief)
# ---------------------------------------------------------------------------
class AISessionBriefResponse(MirageBaseModel):
    id: uuid.UUID
    provider_name: str | None = None
    status: str
    started_at: datetime


# ---------------------------------------------------------------------------
# Visit with nested details
# ---------------------------------------------------------------------------
class VisitWithDetailsResponse(VisitResponse):
    clinical_notes: List[ClinicalNoteResponse] = Field(default_factory=list)
    diagnoses: List[DiagnosisResponse] = Field(default_factory=list)
    medications: List[MedicationResponse] = Field(default_factory=list)
    ai_sessions: List[AISessionBriefResponse] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Complete / Cancel
# ---------------------------------------------------------------------------
class ConsultationCompleteRequest(MirageBaseModel):
    pass


class ConsultationCancelRequest(MirageBaseModel):
    pass
