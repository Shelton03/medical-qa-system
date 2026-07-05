from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Date, DateTime, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Patient(Base):
    """Patient demographic profile."""

    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    medical_record_number = Column(String(50), unique=True, nullable=False, index=True)
    national_identifier = Column(String(50), nullable=False, index=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum("Male", "Female", "Other", name="gender"), nullable=False)
    blood_type = Column(String(10), nullable=True)
    address = Column(Text, nullable=True)
    emergency_contact_name = Column(String(255), nullable=True)
    emergency_contact_phone = Column(String(50), nullable=True)
    preferred_language = Column(String(50), default="en", nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    medical_record = relationship("MedicalRecord", uselist=False, back_populates="patient")
    user = relationship("User", back_populates="patient", uselist=False)


class MedicalRecord(Base):
    """Root clinical record (one per patient)."""

    __tablename__ = "medical_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, unique=True)
    primary_physician_id = Column(UUID(as_uuid=True), ForeignKey("doctors.id", ondelete="SET NULL"), nullable=True)
    record_status = Column(String(50), default="active", nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    patient = relationship("Patient", back_populates="medical_record")
    allergies = relationship("Allergy", back_populates="medical_record")
    chronic_conditions = relationship("ChronicCondition", back_populates="medical_record")
    medications = relationship("Medication", back_populates="medical_record")


class Allergy(Base):
    """Critical allergy/safety information."""

    __tablename__ = "allergies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    medical_record_id = Column(UUID(as_uuid=True), ForeignKey("medical_records.id", ondelete="CASCADE"), nullable=False)
    allergen = Column(String(255), nullable=False)
    reaction = Column(Text, nullable=True)
    severity = Column(Enum("mild", "moderate", "severe", name="severity"), nullable=False)
    notes = Column(Text, nullable=True)

    medical_record = relationship("MedicalRecord", back_populates="allergies")


class ChronicCondition(Base):
    """Long-term medical history."""

    __tablename__ = "chronic_conditions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    medical_record_id = Column(UUID(as_uuid=True), ForeignKey("medical_records.id", ondelete="CASCADE"), nullable=False)
    condition_name = Column(String(255), nullable=False)
    diagnosed_date = Column(Date, nullable=True)
    status = Column(String(50), default="active", nullable=False)
    notes = Column(Text, nullable=True)

    medical_record = relationship("MedicalRecord", back_populates="chronic_conditions")


class Medication(Base):
    """Current and historical medications."""

    __tablename__ = "medications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    medical_record_id = Column(UUID(as_uuid=True), ForeignKey("medical_records.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    dosage = Column(String(100), nullable=True)
    frequency = Column(String(100), nullable=True)
    duration = Column(String(100), nullable=True)
    instructions = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    medical_record = relationship("MedicalRecord", back_populates="medications")
