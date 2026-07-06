#!/usr/bin/env python3
"""Mirage patient module Pydantic schemas."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PatientCreate(BaseModel):
    """Request schema for registering a new patient."""

    model_config = ConfigDict(strict=True)
    first_name: str = Field(..., max_length=255)
    last_name: str = Field(..., max_length=255)
    national_id: str = Field(..., max_length=100)
    phone: str = Field(..., max_length=50)
    date_of_birth: date
    gender: str = Field(..., max_length=50)
    blood_type: str | None = Field(None, max_length=10)
    emergency_contact_name: str | None = Field(None, max_length=255)
    emergency_contact_phone: str | None = Field(None, max_length=50)


class PatientUpdate(BaseModel):
    """Partial update schema for patient demographics."""

    model_config = ConfigDict(strict=True)
    first_name: str | None = Field(None, max_length=255)
    last_name: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, max_length=50)
    address: str | None = None
    emergency_contact_name: str | None = Field(None, max_length=255)
    emergency_contact_phone: str | None = Field(None, max_length=50)
    preferred_language: str | None = Field(None, max_length=50)


class PatientResponse(BaseModel):
    """Basic patient information for list/search results."""

    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    medical_record_number: str
    first_name: str | None = None
    last_name: str | None = None
    national_identifier: str | None = None
    phone: str | None = None
    date_of_birth: date | None = None
    gender: str | None = None
    blood_type: str | None = None
    address: str | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    preferred_language: str | None = None
    created_at: datetime
    updated_at: datetime


class MedicalRecordSummaryResponse(BaseModel):
    """Lightweight medical record summary."""

    model_config = ConfigDict(from_attributes=True)
    id: UUID
    patient_id: UUID
    primary_physician_id: UUID | None = None
    record_status: str | None = None
    created_at: datetime
    updated_at: datetime


class AllergySummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    medical_record_id: UUID
    allergen: str
    reaction: str | None = None
    severity: str | None = None
    notes: str | None = None
    created_at: datetime


class ChronicConditionSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    medical_record_id: UUID
    condition_name: str
    diagnosed_date: date | None = None
    status: str | None = None
    notes: str | None = None
    created_at: datetime


class MedicationSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    medical_record_id: UUID | None = None
    name: str
    dosage: str | None = None
    frequency: str | None = None
    duration: str | None = None
    instructions: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    created_at: datetime


class PatientFullProfileResponse(BaseModel):
    """Complete patient profile with eagerly loaded medical record."""

    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    medical_record_number: str
    first_name: str | None = None
    last_name: str | None = None
    national_identifier: str | None = None
    phone: str | None = None
    date_of_birth: date | None = None
    gender: str | None = None
    blood_type: str | None = None
    address: str | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    preferred_language: str | None = None
    created_at: datetime
    updated_at: datetime
    medical_record: MedicalRecordSummaryResponse | None = None
    allergies: list[AllergySummaryResponse] = []
    chronic_conditions: list[ChronicConditionSummaryResponse] = []
    medications: list[MedicationSummaryResponse] = []
