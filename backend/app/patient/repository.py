#!/usr/bin/env python3
"""Mirage Patient repository — async CRUD for Patient entities."""

from __future__ import annotations

import uuid
from typing import Sequence

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.models import Patient, User
from app.models.patient_record import Allergy, ChronicCondition, MedicalRecord, Medication
from app.patient.schemas import PatientCreate, PatientUpdate


async def get_patient_by_id(db: AsyncSession, patient_id: uuid.UUID) -> Patient | None:
    """Fetch a single patient by primary key with eager user load."""
    result = await db.execute(
        select(Patient)
        .options(joinedload(Patient.user))
        .where(Patient.id == patient_id)
    )
    return result.unique().scalar_one_or_none()


async def get_patient_by_national_id(db: AsyncSession, national_id: str) -> Patient | None:
    """Fetch a patient by national identifier with eager user load."""
    result = await db.execute(
        select(Patient)
        .options(joinedload(Patient.user))
        .where(Patient.national_identifier == national_id)
    )
    return result.unique().scalar_one_or_none()


async def get_patient_by_phone(db: AsyncSession, phone: str) -> Patient | None:
    """Fetch a patient by the linked user's phone number."""
    result = await db.execute(
        select(Patient)
        .join(User, Patient.user_id == User.id)
        .options(joinedload(Patient.user))
        .where(User.phone_number == phone)
    )
    return result.unique().scalar_one_or_none()


async def search_patients(
    db: AsyncSession,
    query: str,
    limit: int = 20,
    offset: int = 0,
) -> tuple[Sequence[Patient], int]:
    """Case-insensitive partial search across name, national_id, and phone."""
    pattern = f"%{query}%"
    filters = or_(
        func.lower(User.first_name).like(func.lower(pattern)),
        func.lower(User.last_name).like(func.lower(pattern)),
        func.lower(Patient.national_identifier).like(func.lower(pattern)),
        func.lower(User.phone_number).like(func.lower(pattern)),
    )

    stmt = (
        select(Patient)
        .join(User, Patient.user_id == User.id)
        .options(joinedload(Patient.user))
        .where(filters)
        .order_by(User.last_name, User.first_name)
        .offset(offset)
        .limit(limit)
    )
    count_stmt = (
        select(func.count(Patient.id))
        .join(User, Patient.user_id == User.id)
        .where(filters)
    )

    result = await db.execute(stmt)
    patients = result.unique().scalars().all()

    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    return patients, total


async def create_patient(
    db: AsyncSession,
    data: PatientCreate,
    user_id: uuid.UUID,
) -> Patient:
    """Persist a new Patient row linked to the provided user_id."""
    patient = Patient(
        user_id=user_id,
        medical_record_number=_generate_mrn(),
        national_identifier=data.national_id,
        date_of_birth=data.date_of_birth,
        gender=data.gender,
        blood_type=data.blood_type,
        emergency_contact_name=data.emergency_contact_name,
        emergency_contact_phone=data.emergency_contact_phone,
    )
    db.add(patient)
    await db.flush()
    await db.refresh(patient)
    return patient


async def update_patient(
    db: AsyncSession,
    patient_id: uuid.UUID,
    data: PatientUpdate,
) -> Patient | None:
    """Apply partial updates to a Patient and its linked User fields."""
    patient = await get_patient_by_id(db, patient_id)
    if patient is None:
        return None

    # Patient fields
    if data.address is not None:
        patient.address = data.address
    if data.emergency_contact_name is not None:
        patient.emergency_contact_name = data.emergency_contact_name
    if data.emergency_contact_phone is not None:
        patient.emergency_contact_phone = data.emergency_contact_phone
    if data.preferred_language is not None:
        patient.preferred_language = data.preferred_language

    # User fields
    if patient.user:
        if data.first_name is not None:
            patient.user.first_name = data.first_name
        if data.last_name is not None:
            patient.user.last_name = data.last_name
        if data.phone is not None:
            patient.user.phone_number = data.phone

    await db.flush()
    await db.refresh(patient)
    return patient


async def get_patient_records(
    db: AsyncSession,
    patient_id: uuid.UUID,
) -> MedicalRecord | None:
    """Fetch the medical record for a patient with nested safety data."""
    result = await db.execute(
        select(MedicalRecord)
        .options(selectinload(MedicalRecord.allergies))
        .options(selectinload(MedicalRecord.chronic_conditions))
        .options(selectinload(MedicalRecord.medications))
        .where(MedicalRecord.patient_id == patient_id)
    )
    return result.scalar_one_or_none()


async def get_patient_full_profile(
    db: AsyncSession,
    patient_id: uuid.UUID,
) -> Patient | None:
    """Fetch a patient with eagerly loaded medical_record, allergies, conditions, medications."""
    result = await db.execute(
        select(Patient)
        .options(joinedload(Patient.user))
        .options(
            selectinload(Patient.medical_record).selectinload(MedicalRecord.allergies)
        )
        .options(
            selectinload(Patient.medical_record).selectinload(MedicalRecord.chronic_conditions)
        )
        .options(
            selectinload(Patient.medical_record).selectinload(MedicalRecord.medications)
        )
        .where(Patient.id == patient_id)
    )
    return result.unique().scalar_one_or_none()


def _generate_mrn() -> str:
    """Generate a unique medical record number."""
    return f"MRN-{uuid.uuid4().hex[:8].upper()}"
