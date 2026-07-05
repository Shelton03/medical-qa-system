#!/usr/bin/env python3
"""Mirage Patient service layer — business logic and authorization."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.auth.password import hash_password
from app.core.exceptions import ForbiddenException, NotFoundException
from app.models import User, Patient
from app.models.patient_record import MedicalRecord
from app.patient import repository
from app.patient.schemas import (
    PatientCreate,
    PatientResponse,
    PatientUpdate,
    PatientFullProfileResponse,
    MedicalRecordSummaryResponse,
    AllergySummaryResponse,
    ChronicConditionSummaryResponse,
    MedicationSummaryResponse,
)


async def search_patients(
    db: AsyncSession,
    query: str,
    limit: int,
    offset: int,
    requesting_user: User,
) -> tuple[list[PatientResponse], int]:
    """Search patients with authorization check."""
    if requesting_user.role not in ("doctor", "admin"):
        raise ForbiddenException("Only doctors and admins can search patients.")
    patients, total = await repository.search_patients(db, query, limit, offset)
    return [_to_response(p) for p in patients], total


async def get_patient_profile(
    db: AsyncSession,
    patient_id: uuid.UUID,
    requesting_user: User,
) -> PatientFullProfileResponse:
    """Return full patient profile with authorization enforcement."""
    patient = await repository.get_patient_full_profile(db, patient_id)
    if not patient:
        raise NotFoundException("Patient not found.", error_code="PATIENT_NOT_FOUND")

    if requesting_user.role == "patient":
        if not patient.user or patient.user.id != requesting_user.id:
            raise ForbiddenException("You can only view your own profile.")

    return _to_full_profile(patient)


async def register_patient(db: AsyncSession, data: PatientCreate) -> PatientResponse:
    """Create a new patient, linked user, and medical record in a transaction."""
    async with db.begin():
        user = User(
            id=uuid.uuid4(),
            email=f"{data.national_id}@mirage.local",
            password_hash=hash_password(uuid.uuid4().hex),
            role="patient",
            first_name=data.first_name,
            last_name=data.last_name,
            phone_number=data.phone,
            is_active=True,
        )
        db.add(user)
        await db.flush()

        patient = await repository.create_patient(db, data, user.id)

        record = MedicalRecord(
            id=uuid.uuid4(),
            patient_id=patient.id,
            record_status="active",
        )
        db.add(record)
        await db.flush()

        result = await db.execute(
            select(Patient)
            .options(joinedload(Patient.user))
            .where(Patient.id == patient.id)
        )
        patient = result.unique().scalar_one()

    return _to_response(patient)


async def update_patient_record(
    db: AsyncSession,
    patient_id: uuid.UUID,
    data: PatientUpdate,
    requesting_user: User,
) -> PatientResponse:
    """Apply a partial update to a patient. Only doctors and admins may update."""
    if requesting_user.role == "patient":
        raise ForbiddenException("Patients cannot modify their own records.")
    if requesting_user.role not in ("doctor", "admin"):
        raise ForbiddenException("Insufficient permissions.")

    async with db.begin():
        patient = await repository.update_patient(db, patient_id, data)
        if not patient:
            raise NotFoundException("Patient not found.", error_code="PATIENT_NOT_FOUND")
        response = _to_response(patient)

    return response


async def get_patient_records_summary(
    db: AsyncSession,
    patient_id: uuid.UUID,
    requesting_user: User,
) -> MedicalRecordSummaryResponse:
    """Return medical record summary with ownership checks."""
    patient = await repository.get_patient_by_id(db, patient_id)
    if not patient:
        raise NotFoundException("Patient not found.", error_code="PATIENT_NOT_FOUND")

    if requesting_user.role == "patient":
        if not patient.user or patient.user.id != requesting_user.id:
            raise ForbiddenException("You can only view your own records.")

    record = await repository.get_patient_records(db, patient_id)
    if not record:
        raise NotFoundException("Medical record not found.", error_code="RECORD_NOT_FOUND")

    return MedicalRecordSummaryResponse(
        id=record.id,
        patient_id=record.patient_id,
        primary_physician_id=record.primary_physician_id,
        record_status=record.record_status,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )


# ---------------------------------------------------------------------------
# Private mappers
# ---------------------------------------------------------------------------
def _to_response(patient: Patient) -> PatientResponse:
    return PatientResponse(
        id=patient.id,
        user_id=patient.user_id,
        medical_record_number=patient.medical_record_number,
        first_name=patient.user.first_name if patient.user else None,
        last_name=patient.user.last_name if patient.user else None,
        national_identifier=patient.national_identifier,
        phone=patient.user.phone_number if patient.user else None,
        date_of_birth=patient.date_of_birth,
        gender=patient.gender,
        blood_type=patient.blood_type,
        address=patient.address,
        emergency_contact_name=patient.emergency_contact_name,
        emergency_contact_phone=patient.emergency_contact_phone,
        preferred_language=patient.preferred_language,
        created_at=patient.created_at,
        updated_at=patient.updated_at,
    )


def _to_full_profile(patient: Patient) -> PatientFullProfileResponse:
    record = None
    if patient.medical_record:
        record = MedicalRecordSummaryResponse(
            id=patient.medical_record.id,
            patient_id=patient.medical_record.patient_id,
            primary_physician_id=patient.medical_record.primary_physician_id,
            record_status=patient.medical_record.record_status,
            created_at=patient.medical_record.created_at,
            updated_at=patient.medical_record.updated_at,
        )

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

    medications = [
        MedicationSummaryResponse(
            id=m.id,
            medical_record_id=m.medical_record_id,
            name=m.name,
            dosage=m.dosage,
            frequency=m.frequency,
            duration=m.duration,
            instructions=m.instructions,
            start_date=m.start_date,
            end_date=m.end_date,
            created_at=m.created_at,
        )
        for m in (patient.medical_record.medications if patient.medical_record else [])
    ]

    return PatientFullProfileResponse(
        id=patient.id,
        user_id=patient.user_id,
        medical_record_number=patient.medical_record_number,
        first_name=patient.user.first_name if patient.user else None,
        last_name=patient.user.last_name if patient.user else None,
        national_identifier=patient.national_identifier,
        phone=patient.user.phone_number if patient.user else None,
        date_of_birth=patient.date_of_birth,
        gender=patient.gender,
        blood_type=patient.blood_type,
        address=patient.address,
        emergency_contact_name=patient.emergency_contact_name,
        emergency_contact_phone=patient.emergency_contact_phone,
        preferred_language=patient.preferred_language,
        created_at=patient.created_at,
        updated_at=patient.updated_at,
        medical_record=record,
        allergies=allergies,
        chronic_conditions=conditions,
        medications=medications,
    )
