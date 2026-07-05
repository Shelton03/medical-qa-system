from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.password import hash_password
from app.auth.demo import _DEMO_DOCTOR_UUID, _DEMO_PATIENT_UUID
from app.models import User, Patient, MedicalRecord, Allergy, ChronicCondition, Medication
from app.models.doctor import Doctor
from app.core.database import AsyncSessionLocal

DEMO_DOCTOR_EMAIL = "dr.sarah.mirage@mirage.health"
DEMO_DOCTOR_PASSWORD = "Healthathon2024!"
DEMO_PATIENT_NATIONAL_ID = "ZIM-89-4567234"
DEMO_PATIENT_PIN = "2024"


async def _get_or_create_user(
    db: AsyncSession,
    email: str,
    first_name: str,
    last_name: str,
    role: str,
    password_plain: str,
    phone_number: str | None = None,
    user_id: uuid.UUID | None = None,
) -> User:
    result = await db.execute(select(User).where(User.email == email))
    existing = result.scalar_one_or_none()
    if existing:
        return existing
    user = User(
        id=user_id or uuid.uuid4(),
        email=email,
        password_hash=hash_password(password_plain),
        role=role,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        is_active=True,
    )
    db.add(user)
    await db.flush()
    return user


async def _get_or_create_patient(
    db: AsyncSession,
    user: User,
    medical_record_number: str,
    national_id: str,
    date_of_birth: date,
    gender: str,
    blood_type: str | None = None,
    patient_id: uuid.UUID | None = None,
) -> Patient:
    result = await db.execute(
        select(Patient).where(Patient.national_identifier == national_id)
    )
    existing = result.scalar_one_or_none()
    if existing:
        return existing
    patient = Patient(
        id=patient_id or uuid.uuid4(),
        user_id=user.id,
        medical_record_number=medical_record_number,
        national_identifier=national_id,
        date_of_birth=date_of_birth,
        gender=gender,
        blood_type=blood_type,
    )
    db.add(patient)
    await db.flush()
    return patient


async def _get_or_create_doctor(
    db: AsyncSession,
    user: User,
    registration_number: str,
    specialty: str | None = None,
    doctor_id: uuid.UUID | None = None,
) -> Doctor:
    result = await db.execute(select(Doctor).where(Doctor.user_id == user.id))
    existing = result.scalar_one_or_none()
    if existing:
        return existing
    doctor = Doctor(
        id=doctor_id or uuid.uuid4(),
        user_id=user.id,
        registration_number=registration_number,
        specialty=specialty,
    )
    db.add(doctor)
    await db.flush()
    return doctor


async def _get_or_create_medical_record(
    db: AsyncSession,
    patient: Patient,
) -> MedicalRecord:
    result = await db.execute(
        select(MedicalRecord).where(MedicalRecord.patient_id == patient.id)
    )
    existing = result.scalar_one_or_none()
    if existing:
        return existing
    record = MedicalRecord(
        id=uuid.uuid4(),
        patient_id=patient.id,
    )
    db.add(record)
    await db.flush()
    return record


async def _seed_conditions(
    db: AsyncSession,
    medical_record: MedicalRecord,
) -> None:
    conditions = [
        {
            "condition_name": "Hypertension",
            "diagnosed_date": date(2018, 3, 10),
            "status": "active",
            "notes": "Managed with lifestyle changes and medication.",
        },
        {
            "condition_name": "Type 2 Diabetes",
            "diagnosed_date": date(2020, 6, 22),
            "status": "active",
            "notes": "Controlled with metformin.",
        },
    ]
    for cond_data in conditions:
        exists = await db.execute(
            select(ChronicCondition).where(
                ChronicCondition.medical_record_id == medical_record.id,
                ChronicCondition.condition_name == cond_data["condition_name"],
            )
        )
        if exists.scalar_one_or_none():
            continue
        db.add(
            ChronicCondition(
                id=uuid.uuid4(),
                medical_record_id=medical_record.id,
                **cond_data,
            )
        )
    await db.flush()


async def _seed_allergies(
    db: AsyncSession,
    medical_record: MedicalRecord,
) -> None:
    allergies = [
        {
            "allergen": "Penicillin",
            "reaction": "Rash and difficulty breathing",
            "severity": "severe",
            "notes": "Avoid all beta-lactam antibiotics.",
        },
        {
            "allergen": "Shellfish",
            "reaction": "Hives",
            "severity": "moderate",
            "notes": "Avoid crustaceans.",
        },
    ]
    for allergy_data in allergies:
        exists = await db.execute(
            select(Allergy).where(
                Allergy.medical_record_id == medical_record.id,
                Allergy.allergen == allergy_data["allergen"],
            )
        )
        if exists.scalar_one_or_none():
            continue
        db.add(
            Allergy(
                id=uuid.uuid4(),
                medical_record_id=medical_record.id,
                **allergy_data,
            )
        )
    await db.flush()


async def _seed_medications(
    db: AsyncSession,
    medical_record: MedicalRecord,
) -> None:
    medications = [
        {
            "name": "Metformin",
            "dosage": "500 mg",
            "frequency": "Twice daily",
            "duration": "Ongoing",
            "instructions": "Take with meals",
            "start_date": date(2020, 6, 22),
            "end_date": None,
        },
        {
            "name": "Amlodipine",
            "dosage": "5 mg",
            "frequency": "Once daily",
            "duration": "Ongoing",
            "instructions": "Take in the morning",
            "start_date": date(2018, 3, 10),
            "end_date": None,
        },
    ]
    for med_data in medications:
        exists = await db.execute(
            select(Medication).where(
                Medication.medical_record_id == medical_record.id,
                Medication.name == med_data["name"],
            )
        )
        if exists.scalar_one_or_none():
            continue
        db.add(
            Medication(
                id=uuid.uuid4(),
                medical_record_id=medical_record.id,
                **med_data,
            )
        )
    await db.flush()


async def seed_demo_data(db: AsyncSession) -> None:
    """Seed the database with demonstration users and records if absent."""
    # Demo doctor
    doctor_user = await _get_or_create_user(
        db,
        email=DEMO_DOCTOR_EMAIL,
        first_name="Sarah",
        last_name="Mirage",
        role="doctor",
        password_plain=DEMO_DOCTOR_PASSWORD,
        phone_number="+263-772-123456",
        user_id=_DEMO_DOCTOR_UUID,
    )
    await _get_or_create_doctor(
        db,
        user=doctor_user,
        registration_number="MED12345",
        specialty="General Practice",
        doctor_id=_DEMO_DOCTOR_UUID,
    )

    # Demo patient
    patient_user = await _get_or_create_user(
        db,
        email="tendai.mutasa@mirage.health",
        first_name="Tendai",
        last_name="Mutasa",
        role="patient",
        password_plain=DEMO_PATIENT_PIN,
        phone_number="+263-773-654321",
        user_id=_DEMO_PATIENT_UUID,
    )

    patient = await _get_or_create_patient(
        db,
        user=patient_user,
        medical_record_number="MRN-000001",
        national_id=DEMO_PATIENT_NATIONAL_ID,
        date_of_birth=date(1989, 5, 14),
        gender="Male",
        blood_type="O+",
        patient_id=_DEMO_PATIENT_UUID,
    )

    record = await _get_or_create_medical_record(db, patient)
    await _seed_conditions(db, record)
    await _seed_allergies(db, record)
    await _seed_medications(db, record)

    await db.commit()
