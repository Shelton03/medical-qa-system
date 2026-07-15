#!/usr/bin/env python3
"""SQLAlchemy 2.0 declarative models for Mirage."""

from __future__ import annotations

import uuid
from datetime import date, datetime, time
from decimal import Decimal
from typing import List

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    Time,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    type_annotation_map = {
        dict: JSONB,
        list: JSONB,
    }


# ---------------------------------------------------------------------------
# users
# ---------------------------------------------------------------------------
class User(Base):
    """Authentication and identity."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    patient: Mapped["Patient"] = relationship(
        "Patient", back_populates="user", uselist=False
    )
    doctor: Mapped["Doctor"] = relationship(
        "Doctor", back_populates="user", uselist=False
    )
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
        "RefreshToken", back_populates="user"
    )
    notifications: Mapped[List["Notification"]] = relationship(
        "Notification", back_populates="recipient"
    )
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog", back_populates="user"
    )

    __table_args__ = (
        Index("ix_users_email", email, unique=True),
        Index("ix_users_role", role),
        Index("ix_users_is_active", is_active),
    )


# ---------------------------------------------------------------------------
# patients
# ---------------------------------------------------------------------------
class Patient(Base):
    """Patient demographic profile. One-to-one with User."""

    __tablename__ = "patients"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    medical_record_number: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    national_identifier: Mapped[str | None] = mapped_column(String(100), nullable=True)
    date_of_birth: Mapped[datetime | None] = mapped_column(Date(), nullable=True)
    gender: Mapped[str | None] = mapped_column(String(50), nullable=True)
    blood_type: Mapped[str | None] = mapped_column(String(10), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    emergency_contact_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    emergency_contact_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    preferred_language: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="patient")
    medical_record: Mapped["MedicalRecord"] = relationship(
        "MedicalRecord", back_populates="patient", uselist=False
    )
    consent_requests: Mapped[List["ConsentRequest"]] = relationship(
        "ConsentRequest", back_populates="patient"
    )
    ai_sessions: Mapped[List["AISession"]] = relationship(
        "AISession", back_populates="patient"
    )
    appointments: Mapped[List["Appointment"]] = relationship(
        "Appointment", back_populates="patient"
    )

    __table_args__ = (
        Index("ix_patients_medical_record_number", medical_record_number, unique=True),
        Index("ix_patients_national_identifier", national_identifier),
        Index("ix_patients_date_of_birth", date_of_birth),
    )


# ---------------------------------------------------------------------------
# doctors
# ---------------------------------------------------------------------------
class Doctor(Base):
    """Doctor profile."""

    __tablename__ = "doctors"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    registration_number: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    specialty: Mapped[str | None] = mapped_column(String(255), nullable=True)
    facility_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("facilities.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=True,
    )
    department: Mapped[str | None] = mapped_column(String(255), nullable=True)
    license_expiry: Mapped[datetime | None] = mapped_column(Date(), nullable=True)
    years_experience: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_daily_appointments: Mapped[int | None] = mapped_column(Integer, default=20)
    is_accepting_appointments: Mapped[bool] = mapped_column(Boolean, default=True)
    next_available_date: Mapped[datetime | None] = mapped_column(Date(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="doctor")
    facility: Mapped["Facility"] = relationship("Facility", back_populates="doctors")
    visits: Mapped[List["Visit"]] = relationship("Visit", back_populates="doctor")
    consent_requests: Mapped[List["ConsentRequest"]] = relationship(
        "ConsentRequest", back_populates="doctor"
    )
    ai_sessions: Mapped[List["AISession"]] = relationship(
        "AISession", back_populates="doctor"
    )
    # Appointment-related relationships
    appointments: Mapped[List["Appointment"]] = relationship(
        "Appointment", foreign_keys="Appointment.doctor_id", back_populates="doctor"
    )
    schedules: Mapped[List["DoctorSchedule"]] = relationship("DoctorSchedule", back_populates="doctor")
    time_offs: Mapped[List["DoctorTimeOff"]] = relationship("DoctorTimeOff", back_populates="doctor")

    __table_args__ = (
        Index("ix_doctors_registration_number", registration_number, unique=True),
        Index("ix_doctors_facility_id", facility_id),
        Index("ix_doctors_specialty", specialty),
    )


# ---------------------------------------------------------------------------
# facilities
# ---------------------------------------------------------------------------
class Facility(Base):
    """Healthcare facility."""

    __tablename__ = "facilities"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str | None] = mapped_column(String(255), nullable=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    timezone: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    doctors: Mapped[List["Doctor"]] = relationship("Doctor", back_populates="facility")
    visits: Mapped[List["Visit"]] = relationship("Visit", back_populates="facility")
    appointments: Mapped[List["Appointment"]] = relationship("Appointment", back_populates="facility")

    __table_args__ = (
        Index("ix_facilities_name", name),
        Index("ix_facilities_city", city),
    )


# ---------------------------------------------------------------------------
# medical_records
# ---------------------------------------------------------------------------
class MedicalRecord(Base):
    """Root clinical record. Exactly one per patient."""

    __tablename__ = "medical_records"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    patient_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("patients.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    primary_physician_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("doctors.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=True,
    )
    record_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    patient: Mapped["Patient"] = relationship("Patient", back_populates="medical_record")
    visits: Mapped[List["Visit"]] = relationship("Visit", back_populates="medical_record")
    allergies: Mapped[List["Allergy"]] = relationship(
        "Allergy", back_populates="medical_record"
    )
    chronic_conditions: Mapped[List["ChronicCondition"]] = relationship(
        "ChronicCondition", back_populates="medical_record"
    )
    clinical_documents: Mapped[List["ClinicalDocument"]] = relationship(
        "ClinicalDocument", back_populates="medical_record"
    )

    __table_args__ = (
        Index("ix_medical_records_patient_id", patient_id, unique=True),
    )


# ---------------------------------------------------------------------------
# visits
# ---------------------------------------------------------------------------
class Visit(Base):
    """Every clinical encounter."""

    __tablename__ = "visits"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    medical_record_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("medical_records.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    doctor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("doctors.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    facility_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("facilities.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=True,
    )
    visit_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    chief_complaint: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    transcript: Mapped[str | None] = mapped_column(Text, nullable=True)
    follow_up_required: Mapped[bool | None] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    medical_record: Mapped["MedicalRecord"] = relationship(
        "MedicalRecord", back_populates="visits"
    )
    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="visits")
    facility: Mapped["Facility"] = relationship("Facility", back_populates="visits")
    diagnoses: Mapped[List["Diagnosis"]] = relationship(
        "Diagnosis", back_populates="visit"
    )
    medications: Mapped[List["Medication"]] = relationship(
        "Medication", back_populates="visit"
    )
    laboratory_results: Mapped[List["LaboratoryResult"]] = relationship(
        "LaboratoryResult", back_populates="visit"
    )
    imaging_results: Mapped[List["ImagingResult"]] = relationship(
        "ImagingResult", back_populates="visit"
    )
    clinical_notes: Mapped[List["ClinicalNote"]] = relationship(
        "ClinicalNote", back_populates="visit"
    )
    ai_sessions: Mapped[List["AISession"]] = relationship(
        "AISession", back_populates="visit"
    )
    appointment: Mapped["Appointment"] = relationship("Appointment", back_populates="visit", uselist=False)

    __table_args__ = (
        Index("ix_visits_visit_date", visit_date),
        Index("ix_visits_doctor_id", doctor_id),
        Index("ix_visits_facility_id", facility_id),
        Index("ix_visits_status", status),
    )


# ---------------------------------------------------------------------------
# diagnoses
# ---------------------------------------------------------------------------
class Diagnosis(Base):
    """Diagnoses linked to a visit."""

    __tablename__ = "diagnoses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    visit_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("visits.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    diagnosis_name: Mapped[str] = mapped_column(String(500), nullable=False)
    icd10_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    confidence: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 4), nullable=True
    )
    primary_diagnosis: Mapped[bool | None] = mapped_column(
        Boolean, default=False
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    visit: Mapped["Visit"] = relationship("Visit", back_populates="diagnoses")

    __table_args__ = (
        Index("ix_diagnoses_visit_id", visit_id),
        Index("ix_diagnoses_icd10_code", icd10_code),
    )


# ---------------------------------------------------------------------------
# medications
# ---------------------------------------------------------------------------
class Medication(Base):
    """Medications prescribed during a visit."""

    __tablename__ = "medications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    visit_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("visits.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    dosage: Mapped[str | None] = mapped_column(String(255), nullable=True)
    frequency: Mapped[str | None] = mapped_column(String(255), nullable=True)
    duration: Mapped[str | None] = mapped_column(String(255), nullable=True)
    instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[datetime | None] = mapped_column(Date(), nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(Date(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    visit: Mapped["Visit"] = relationship("Visit", back_populates="medications")

    __table_args__ = (
        Index("ix_medications_visit_id", visit_id),
        Index("ix_medications_name", name),
    )


# ---------------------------------------------------------------------------
# allergies
# ---------------------------------------------------------------------------
class Allergy(Base):
    """Critical safety allergies stored against a medical record."""

    __tablename__ = "allergies"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    medical_record_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("medical_records.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    allergen: Mapped[str] = mapped_column(String(255), nullable=False)
    reaction: Mapped[str | None] = mapped_column(Text, nullable=True)
    severity: Mapped[str | None] = mapped_column(String(50), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    medical_record: Mapped["MedicalRecord"] = relationship(
        "MedicalRecord", back_populates="allergies"
    )

    __table_args__ = (
        Index("ix_allergies_medical_record_id", medical_record_id),
        Index("ix_allergies_severity", severity),
    )


# ---------------------------------------------------------------------------
# chronic_conditions
# ---------------------------------------------------------------------------
class ChronicCondition(Base):
    """Long-term medical conditions attached to a medical record."""

    __tablename__ = "chronic_conditions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    medical_record_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("medical_records.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    condition_name: Mapped[str] = mapped_column(String(255), nullable=False)
    diagnosed_date: Mapped[datetime | None] = mapped_column(Date(), nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    medical_record: Mapped["MedicalRecord"] = relationship(
        "MedicalRecord", back_populates="chronic_conditions"
    )

    __table_args__ = (
        Index("ix_chronic_conditions_medical_record_id", medical_record_id),
    )


# ---------------------------------------------------------------------------
# laboratory_results
# ---------------------------------------------------------------------------
class LaboratoryResult(Base):
    """Lab results attached to a visit."""

    __tablename__ = "laboratory_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    visit_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("visits.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    test_name: Mapped[str] = mapped_column(String(255), nullable=False)
    result: Mapped[str | None] = mapped_column(Text, nullable=True)
    reference_range: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    performed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    visit: Mapped["Visit"] = relationship("Visit", back_populates="laboratory_results")

    __table_args__ = (
        Index("ix_laboratory_results_performed_at", performed_at),
        Index("ix_laboratory_results_visit_id", visit_id),
    )


# ---------------------------------------------------------------------------
# imaging_results
# ---------------------------------------------------------------------------
class ImagingResult(Base):
    """Imaging study results attached to a visit."""

    __tablename__ = "imaging_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    visit_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("visits.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    modality: Mapped[str] = mapped_column(String(100), nullable=False)
    study_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    report: Mapped[str | None] = mapped_column(Text, nullable=True)
    performed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    visit: Mapped["Visit"] = relationship("Visit", back_populates="imaging_results")

    __table_args__ = (
        Index("ix_imaging_results_visit_id", visit_id),
    )


# ---------------------------------------------------------------------------
# clinical_documents
# ---------------------------------------------------------------------------
class ClinicalDocument(Base):
    """Uploaded PDFs, scans, referrals, discharge summaries."""

    __tablename__ = "clinical_documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    medical_record_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("medical_records.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    storage_key: Mapped[str] = mapped_column(String(500), nullable=False)
    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    uploaded_by: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=True,
    )
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    medical_record: Mapped["MedicalRecord"] = relationship(
        "MedicalRecord", back_populates="clinical_documents"
    )

    __table_args__ = (
        Index("ix_clinical_documents_medical_record_id", medical_record_id),
        Index("ix_clinical_documents_uploaded_at", uploaded_at),
    )


# ---------------------------------------------------------------------------
# consent_requests
# ---------------------------------------------------------------------------
class ConsentRequest(Base):
    """Doctor request to access patient medical information."""

    __tablename__ = "consent_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    patient_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("patients.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    doctor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("doctors.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    facility_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("facilities.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=True,
    )
    purpose: Mapped[str | None] = mapped_column(Text, nullable=True)
    scope: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    denied_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    declined_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    patient: Mapped["Patient"] = relationship("Patient", back_populates="consent_requests")
    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="consent_requests")

    __table_args__ = (
        Index("ix_consent_requests_patient_id", patient_id),
        Index("ix_consent_requests_doctor_id", doctor_id),
        Index("ix_consent_requests_status", status),
        Index("ix_consent_requests_expires_at", expires_at),
    )


# ---------------------------------------------------------------------------
# ai_sessions
# ---------------------------------------------------------------------------
class AISession(Base):
    """Tracks AI-assisted consultations."""

    __tablename__ = "ai_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    patient_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("patients.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=True,
    )
    doctor_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("doctors.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=True,
    )
    consultation_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("visits.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=True,
    )
    provider_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    provider_metadata: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    conversation_summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="ai_sessions")
    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="ai_sessions")
    visit: Mapped["Visit"] = relationship("Visit", back_populates="ai_sessions")
    messages: Mapped[List["AIMessage"]] = relationship(
        "AIMessage", back_populates="session"
    )

    __table_args__ = (
        Index("ix_ai_sessions_patient_id", patient_id),
        Index("ix_ai_sessions_doctor_id", doctor_id),
        Index("ix_ai_sessions_status", status),
        Index("ix_ai_sessions_started_at", started_at),
    )


# ---------------------------------------------------------------------------
# ai_messages
# ---------------------------------------------------------------------------
class AIMessage(Base):
    """Conversation history for AI consultations. Immutable."""

    __tablename__ = "ai_messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ai_sessions.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    token_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    session: Mapped["AISession"] = relationship("AISession", back_populates="messages")

    __table_args__ = (
        Index("ix_ai_messages_session_id", session_id),
        Index("ix_ai_messages_created_at", created_at),
    )


# ---------------------------------------------------------------------------
# clinical_notes
# ---------------------------------------------------------------------------
class ClinicalNote(Base):
    """Doctor-authored consultation notes. Editable until finalized."""

    __tablename__ = "clinical_notes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    visit_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("visits.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    doctor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("doctors.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    subjective: Mapped[str | None] = mapped_column(Text, nullable=True)
    objective: Mapped[str | None] = mapped_column(Text, nullable=True)
    assessment: Mapped[str | None] = mapped_column(Text, nullable=True)
    plan: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_finalized: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    visit: Mapped["Visit"] = relationship("Visit", back_populates="clinical_notes")

    __table_args__ = (
        Index("ix_clinical_notes_visit_id", visit_id),
        Index("ix_clinical_notes_doctor_id", doctor_id),
    )


# ---------------------------------------------------------------------------
# notifications
# ---------------------------------------------------------------------------
class Notification(Base):
    """In-app notifications for users."""

    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    recipient_user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    priority: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    read_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    recipient: Mapped["User"] = relationship("User", back_populates="notifications")

    __table_args__ = (
        Index("ix_notifications_recipient_user_id", recipient_user_id),
        Index("ix_notifications_is_read", is_read),
        Index("ix_notifications_type", type),
        Index("ix_notifications_created_at", created_at),
    )


# ---------------------------------------------------------------------------
# refresh_tokens
# ---------------------------------------------------------------------------
class RefreshToken(Base):
    """Secure JWT refresh token rotation."""

    __tablename__ = "refresh_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    token_hash: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    last_used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")

    __table_args__ = (
        Index("ix_refresh_tokens_token_hash", token_hash, unique=True),
        Index("ix_refresh_tokens_user_id", user_id),
    )


# ---------------------------------------------------------------------------
# audit_logs
# ---------------------------------------------------------------------------
class AuditLog(Base):
    """Immutable record of every sensitive action."""

    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=True,
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    resource_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    audit_metadata: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="audit_logs")

    __table_args__ = (
        Index("ix_audit_logs_user_id", user_id),
        Index("ix_audit_logs_resource_type", resource_type),
        Index("ix_audit_logs_resource_id", resource_id),
        Index("ix_audit_logs_created_at", created_at),
        Index("ix_audit_logs_action", action),
    )


# ---------------------------------------------------------------------------
# medical_record_versions
# ---------------------------------------------------------------------------
class MedicalRecordVersion(Base):
    """Version history snapshots for patient records."""

    __tablename__ = "medical_record_versions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    medical_record_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("medical_records.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    changed_by: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=True,
    )
    change_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    snapshot: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        Index("ix_medical_record_versions_medical_record_id", medical_record_id),
        Index("ix_medical_record_versions_version_number", version_number),
    )


# ---------------------------------------------------------------------------
# appointments
# ---------------------------------------------------------------------------
class Appointment(Base):
    """Patient appointment booking with auto-routed doctor assignment."""

    __tablename__ = "appointments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("patients.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    facility_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("facilities.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    doctor_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("doctors.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )
    visit_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("visits.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )

    appointment_date: Mapped[date] = mapped_column(Date(), nullable=False)
    desired_duration_minutes: Mapped[int] = mapped_column(Integer, default=30)
    allocated_start_time: Mapped[time | None] = mapped_column(Time(), nullable=True)
    allocated_end_time: Mapped[time | None] = mapped_column(Time(), nullable=True)

    status: Mapped[str] = mapped_column(String(20), default="PENDING")
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    symptoms: Mapped[str | None] = mapped_column(Text, nullable=True)
    priority: Mapped[str] = mapped_column(String(20), default="NORMAL")
    is_emergency: Mapped[bool] = mapped_column(Boolean, default=False)
    triage_score: Mapped[int] = mapped_column(Integer, default=0)

    preferred_doctor_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("doctors.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )

    patient_confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    doctor_confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_by: Mapped[str | None] = mapped_column(String(20), nullable=True)
    cancellation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    patient: Mapped["Patient"] = relationship("Patient", back_populates="appointments")
    facility: Mapped["Facility"] = relationship("Facility", back_populates="appointments")
    doctor: Mapped["Doctor"] = relationship("Doctor", foreign_keys=[doctor_id], back_populates="appointments")
    visit: Mapped["Visit"] = relationship("Visit", back_populates="appointment")
    preferred_doctor: Mapped["Doctor"] = relationship("Doctor", foreign_keys=[preferred_doctor_id])
    slot_allocation: Mapped["AppointmentSlotAllocation"] = relationship(
        "AppointmentSlotAllocation", back_populates="appointment", uselist=False
    )

    __table_args__ = (
        Index("ix_appointments_patient_id", patient_id),
        Index("ix_appointments_facility_id", facility_id),
        Index("ix_appointments_doctor_id", doctor_id),
        Index("ix_appointments_date", appointment_date),
        Index("ix_appointments_status", status),
        Index("ix_appointments_priority", priority),
    )


class DoctorSchedule(Base):
    """Weekly schedule template for a doctor. Admin-managed."""

    __tablename__ = "doctor_schedules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("doctors.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[time] = mapped_column(Time(), nullable=False)
    end_time: Mapped[time] = mapped_column(Time(), nullable=False)
    is_working_day: Mapped[bool] = mapped_column(Boolean, default=True)
    default_slot_duration: Mapped[int] = mapped_column(Integer, default=30)
    max_daily_appointments: Mapped[int] = mapped_column(Integer, default=20)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="schedules")

    __table_args__ = (
        Index("ix_doctor_schedules_doctor_id", doctor_id),
    )


class DoctorTimeOff(Base):
    """Leave / unavailability records for doctors."""

    __tablename__ = "doctor_time_offs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("doctors.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    start_date: Mapped[date] = mapped_column(Date(), nullable=False)
    end_date: Mapped[date] = mapped_column(Date(), nullable=False)
    type: Mapped[str] = mapped_column(String(20), default="LEAVE")
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="APPROVED")
    requested_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    approved_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="time_offs")

    __table_args__ = (
        Index("ix_doctor_time_offs_doctor_id", doctor_id),
        Index("ix_doctor_time_offs_dates", start_date, end_date),
    )


class AppointmentSlotAllocation(Base):
    """Specific time slot allocated for an appointment."""

    __tablename__ = "appointment_slot_allocations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    appointment_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("appointments.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    doctor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("doctors.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    slot_date: Mapped[date] = mapped_column(Date(), nullable=False)
    start_time: Mapped[time] = mapped_column(Time(), nullable=False)
    end_time: Mapped[time] = mapped_column(Time(), nullable=False)
    buffer_after_minutes: Mapped[int] = mapped_column(Integer, default=3)
    status: Mapped[str] = mapped_column(String(20), default="ALLOCATED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    appointment: Mapped["Appointment"] = relationship("Appointment", back_populates="slot_allocation")

    __table_args__ = (
        Index("ix_slot_allocations_doctor_date", doctor_id, slot_date),
        Index("ix_slot_allocations_appointment", appointment_id),
    )

