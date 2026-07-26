from __future__ import annotations

import random
import uuid
from datetime import date, datetime, time, timedelta
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.password import hash_password
from app.auth.demo import _DEMO_DOCTOR_UUID, _DEMO_PATIENT_UUID
from app.db.models import (
    User,
    Patient,
    Doctor,
    MedicalRecord,
    Visit,
    Diagnosis,
    Medication,
    Allergy,
    ChronicCondition,
    LaboratoryResult,
    ImagingResult,
    Facility,
    ConsentRequest,
    Notification,
    AuditLog,
    AISession,
    DoctorSchedule,
    Appointment,
)

DEMO_DOCTOR_EMAIL = "dr.sarah.mirage@mirage.health"
DEMO_DOCTOR_PASSWORD = "Healthathon2024!"
DEMO_PATIENT_NATIONAL_ID = "ZIM-89-4567234"
DEMO_PATIENT_PIN = "2024"

_FACILITIES = [
    {
        "name": "Harare General Hospital",
        "address": "122 Bassett Road, Harare",
        "city": "Harare",
        "country": "Zimbabwe",
        "phone": "+263-242-123456",
        "email": "info@hararegeneral.co.zw",
    },
    {
        "name": "Parirenyatwa Hospital",
        "address": "Mazowe Street, Harare",
        "city": "Harare",
        "country": "Zimbabwe",
        "phone": "+263-242-234567",
        "email": "info@parirenyatwa.co.zw",
    },
    {
        "name": "Chitungwiza Central",
        "address": "Chitungwiza Town Centre",
        "city": "Chitungwiza",
        "country": "Zimbabwe",
        "phone": "+263-242-345678",
        "email": "info@chitungwiza.co.zw",
    },
]

_DOCTORS = [
    {
        "first_name": "Sarah",
        "last_name": "Mirage",
        "email": "dr.sarah.mirage@mirage.health",
        "specialty": "General Practice",
        "reg": "MED12345",
        "user_id": _DEMO_DOCTOR_UUID,
    },
    {
        "first_name": "Rumbidzai",
        "last_name": "Moyo",
        "email": "dr.r.moyo@mirage.health",
        "specialty": "Cardiology",
        "reg": "MED23456",
        "user_id": None,
    },
    {
        "first_name": "Tafadzwa",
        "last_name": "Chitekete",
        "email": "dr.t.chitekete@mirage.health",
        "specialty": "Pediatrics",
        "reg": "MED34567",
        "user_id": None,
    },
    {
        "first_name": "Nyarai",
        "last_name": "Mupfumi",
        "email": "dr.n.mupfumi@mirage.health",
        "specialty": "Obstetrics and Gynaecology",
        "reg": "MED45678",
        "user_id": None,
    },
    {
        "first_name": "Simba",
        "last_name": "Guvamombe",
        "email": "dr.s.guvamombe@mirage.health",
        "specialty": "Internal Medicine",
        "reg": "MED56789",
        "user_id": None,
    },
    {
        "first_name": "Farai",
        "last_name": "Dube",
        "email": "dr.f.dube@mirage.health",
        "specialty": "Dermatology",
        "reg": "MED67890",
        "user_id": None,
    },
    {
        "first_name": "Ruvimbo",
        "last_name": "Mucheka",
        "email": "dr.r.mucheka@mirage.health",
        "specialty": "Psychiatry",
        "reg": "MED78901",
        "user_id": None,
    },
    {
        "first_name": "Shingirai",
        "last_name": "Nkomo",
        "email": "dr.s.nkomo@mirage.health",
        "specialty": "Orthopedics",
        "reg": "MED89012",
        "user_id": None,
    },
    {
        "first_name": "Netsai",
        "last_name": "Mupfumi",
        "email": "dr.netsai.mupfumi@mirage.health",
        "specialty": "Radiology",
        "reg": "MED90123",
        "user_id": None,
    },
]

_PATIENTS = [
    {
        "first_name": "Tendai",
        "last_name": "Mutasa",
        "email": "tendai.mutasa@mirage.health",
        "national_id": "ZIM-89-4567234",
        "mrn": "MRN-000001",
        "dob": date(1989, 5, 14),
        "gender": "Male",
        "blood_type": "O+",
        "user_id": _DEMO_PATIENT_UUID,
    },
    {
        "first_name": "Memory",
        "last_name": "Mashumba",
        "email": "memory.mashumba@mirage.health",
        "national_id": "ZIM-91-1122334",
        "mrn": "MRN-000002",
        "dob": date(1991, 8, 22),
        "gender": "Female",
        "blood_type": "A+",
        "user_id": None,
    },
    {
        "first_name": "Chipo",
        "last_name": "Chiwenga",
        "email": "chipo.chiwenga@mirage.health",
        "national_id": "ZIM-85-9988776",
        "mrn": "MRN-000003",
        "dob": date(1985, 3, 10),
        "gender": "Female",
        "blood_type": "B+",
        "user_id": None,
    },
    {
        "first_name": "Farai",
        "last_name": "Dube",
        "email": "farai.dube@mirage.health",
        "national_id": "ZIM-95-5566778",
        "mrn": "MRN-000004",
        "dob": date(1995, 11, 2),
        "gender": "Male",
        "blood_type": "AB-",
        "user_id": None,
    },
    {
        "first_name": "Tatenda",
        "last_name": "Kambarami",
        "email": "tatenda.kambarami@mirage.health",
        "national_id": "ZIM-78-3344556",
        "mrn": "MRN-000005",
        "dob": date(1978, 1, 30),
        "gender": "Male",
        "blood_type": "O-",
        "user_id": None,
    },
    {
        "first_name": "Ruvimbo",
        "last_name": "Mucheka",
        "email": "ruvimbo.mucheka@mirage.health",
        "national_id": "ZIM-02-4455667",
        "mrn": "MRN-000006",
        "dob": date(2002, 7, 18),
        "gender": "Female",
        "blood_type": "A-",
        "user_id": None,
    },
    {
        "first_name": "Shingirai",
        "last_name": "Nkomo",
        "email": "shingirai.nkomo@mirage.health",
        "national_id": "ZIM-88-7788990",
        "mrn": "MRN-000007",
        "dob": date(1988, 12, 5),
        "gender": "Male",
        "blood_type": "B-",
        "user_id": None,
    },
    {
        "first_name": "Netsai",
        "last_name": "Mupfumi",
        "email": "netsai.mupfumi@mirage.health",
        "national_id": "ZIM-93-2233445",
        "mrn": "MRN-000008",
        "dob": date(1993, 4, 14),
        "gender": "Female",
        "blood_type": "O+",
        "user_id": None,
    },
    {
        "first_name": "Blessing",
        "last_name": "Mudzuri",
        "email": "blessing.mudzuri@mirage.health",
        "national_id": "ZIM-80-6677889",
        "mrn": "MRN-000009",
        "dob": date(1980, 9, 25),
        "gender": "Male",
        "blood_type": "AB+",
        "user_id": None,
    },
    {
        "first_name": "Munashe",
        "last_name": "Zvoma",
        "email": "munashe.zvoma@mirage.health",
        "national_id": "ZIM-99-5544332",
        "mrn": "MRN-000010",
        "dob": date(1999, 6, 8),
        "gender": "Male",
        "blood_type": "A+",
        "user_id": None,
    },
]

_CONDITIONS_POOL = [
    ("Hypertension", "active", "Managed with lifestyle changes and medication."),
    ("Type 2 Diabetes", "active", "Controlled with metformin."),
    ("Asthma", "active", "Inhaler as needed."),
    ("HIV", "active", "On ART, virally suppressed."),
    ("Epilepsy", "active", "Controlled with carbamazepine."),
    ("Chronic Kidney Disease", "active", "Stage 2, monitoring creatinine."),
]

_ALLERGIES_POOL = [
    ("Penicillin", "Rash and difficulty breathing", "severe", "Avoid all beta-lactam antibiotics."),
    ("Shellfish", "Hives", "moderate", "Avoid crustaceans."),
    ("Sulfa drugs", "Skin rash", "mild", "Monitor for reactions."),
    ("Latex", "Contact dermatitis", "mild", "Use latex-free gloves."),
    ("NSAIDs", "Stomach pain", "moderate", "Use acetaminophen instead."),
]

_DIAGNOSES_POOL = [
    ("Malaria", "B50", Decimal("0.95")),
    ("Upper Respiratory Tract Infection", "J06", Decimal("0.88")),
    ("Hypertension", "I10", Decimal("0.92")),
    ("Type 2 Diabetes Mellitus", "E11", Decimal("0.90")),
    ("Acute Gastroenteritis", "A09", Decimal("0.85")),
    ("Anemia", "D64", Decimal("0.80")),
    ("Pneumonia", "J18", Decimal("0.91")),
    ("Typhoid Fever", "A01", Decimal("0.87")),
    ("Peptic Ulcer Disease", "K27", Decimal("0.82")),
    ("Osteoarthritis", "M19", Decimal("0.78")),
]

_MEDICATIONS_POOL = [
    ("Metformin", "500 mg", "Twice daily", "Ongoing", "Take with meals"),
    ("Amlodipine", "5 mg", "Once daily", "Ongoing", "Take in the morning"),
    ("Lisinopril", "10 mg", "Once daily", "Ongoing", "Take at night"),
    ("Artemether/Lumefantrine", "1x6 tablets", "Twice daily for 3 days", "3 days", "Take with fatty meal"),
    ("Salbutamol inhaler", "100 mcg", "As needed", "Ongoing", "For wheezing"),
    ("Carbamazepine", "200 mg", "Twice daily", "Ongoing", "Monitor levels"),
    ("Insulin glargine", "20 units", "Once daily", "Ongoing", "Subcutaneous at bedtime"),
]

_LAB_TESTS_POOL = [
    ("Full Blood Count", "Pending"),
    ("Malaria Rapid Diagnostic Test", "Positive"),
    ("HIV Viral Load", "Suppressed"),
    ("Fasting Blood Glucose", "7.2 mmol/L"),
    ("Creatinine", "110 umol/L"),
    ("Liver Function Test", "Normal"),
    ("Urine Microalbumin", "Trace"),
    ("Chest X-ray", "Consolidation left lower lobe"),
]

_IMAGING_POOL = [
    ("X-ray", "Chest X-ray", "Normal cardiac silhouette."),
    ("X-ray", "Chest X-ray", "Mild fibrotic changes noted."),
    ("Ultrasound", "Abdominal USS", "Normal liver, spleen enlarged."),
    ("CT", "Head CT", "No acute intracranial hemorrhage."),
    ("MRI", "Brain MRI", "Small non-specific white matter changes."),
]

_NOTIFICATIONS_POOL = [
    ("Appointment Reminder", "You have an upcoming appointment tomorrow.", "info"),
    ("New Lab Result", "Your recent lab results are now available.", "info"),
    ("Medication Alert", "Time to take your evening medication.", "warning"),
    ("Consent Request", "A doctor has requested access to your records.", "info"),
    ("System Maintenance", "Scheduled maintenance tonight at 02:00.", "warning"),
    ("Welcome", "Welcome to Mirage Health Platform.", "info"),
]


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
    facility_id: uuid.UUID | None = None,
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
        facility_id=facility_id,
        is_accepting_appointments=True,
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
    count: int = 2,
) -> None:
    for _ in range(count):
        cond = random.choice(_CONDITIONS_POOL)
        exists = await db.execute(
            select(ChronicCondition).where(
                ChronicCondition.medical_record_id == medical_record.id,
                ChronicCondition.condition_name == cond[0],
            )
        )
        if exists.scalar_one_or_none():
            continue
        db.add(
            ChronicCondition(
                id=uuid.uuid4(),
                medical_record_id=medical_record.id,
                condition_name=cond[0],
                status=cond[1],
                notes=cond[2],
                diagnosed_date=date(
                    random.randint(2010, 2023),
                    random.randint(1, 12),
                    random.randint(1, 28),
                ),
            )
        )
    await db.flush()


async def _seed_allergies(
    db: AsyncSession,
    medical_record: MedicalRecord,
    count: int = 2,
) -> None:
    for _ in range(count):
        allergy = random.choice(_ALLERGIES_POOL)
        exists = await db.execute(
            select(Allergy).where(
                Allergy.medical_record_id == medical_record.id,
                Allergy.allergen == allergy[0],
            )
        )
        if exists.scalar_one_or_none():
            continue
        db.add(
            Allergy(
                id=uuid.uuid4(),
                medical_record_id=medical_record.id,
                allergen=allergy[0],
                reaction=allergy[1],
                severity=allergy[2],
                notes=allergy[3],
            )
        )
    await db.flush()


async def _seed_medications(
    db: AsyncSession,
    visit: Visit,
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
                Medication.visit_id == visit.id,
                Medication.name == med_data["name"],
            )
        )
        if exists.scalar_one_or_none():
            continue
        db.add(
            Medication(
                id=uuid.uuid4(),
                visit_id=visit.id,
                **med_data,
            )
        )
    await db.flush()


async def seed_demo_data(db: AsyncSession) -> None:
    """Seed the database with demonstration users and records if absent."""
    # Idempotency guard — skip re-seeding if patients already exist
    from sqlalchemy import func

    count_result = await db.execute(select(func.count(Patient.id)))
    if count_result.scalar_one() >= 10:
        return

    # Seed facilities first
    facilities = []
    for f_data in _FACILITIES:
        result = await db.execute(select(Facility).where(Facility.name == f_data["name"]))
        existing = result.scalar_one_or_none()
        if existing:
            facilities.append(existing)
            continue
        facility = Facility(id=uuid.uuid4(), **f_data)
        db.add(facility)
        await db.flush()
        facilities.append(facility)

    # Seed doctors (round-robin across facilities)
    doctors = []
    for idx, d_data in enumerate(_DOCTORS):
        user = await _get_or_create_user(
            db,
            email=d_data["email"],
            first_name=d_data["first_name"],
            last_name=d_data["last_name"],
            role="doctor",
            password_plain=DEMO_DOCTOR_PASSWORD,
            phone_number="+263-772-000000",
            user_id=d_data["user_id"],
        )
        facility = facilities[idx % len(facilities)]
        doctor = await _get_or_create_doctor(
            db,
            user=user,
            registration_number=d_data["reg"],
            specialty=d_data["specialty"],
            doctor_id=d_data["user_id"],
            facility_id=facility.id,
        )
        doctors.append(doctor)
    await db.flush()

    # Ensure every doctor has a schedule (Mon-Sun), idempotent per doctor
    for doctor in doctors:
        existing_days = set()
        result = await db.execute(
            select(DoctorSchedule.day_of_week).where(DoctorSchedule.doctor_id == doctor.id)
        )
        existing_days = {row[0] for row in result.all()}
        for day in range(7):
            if day in existing_days:
                continue
            if day in (5, 6):  # weekend half-day
                start = time(8, 0)
                end = time(13, 0)
            else:
                start = time(8, 0)
                end = time(17, 0)
            schedule = DoctorSchedule(
                id=uuid.uuid4(),
                doctor_id=doctor.id,
                day_of_week=day,
                start_time=start,
                end_time=end,
                max_daily_appointments=20,
                default_slot_duration=30,
                is_working_day=True,
            )
            db.add(schedule)
        await db.flush()

    # Seed patients
    patients = []
    for p_data in _PATIENTS:
        user = await _get_or_create_user(
            db,
            email=p_data["email"],
            first_name=p_data["first_name"],
            last_name=p_data["last_name"],
            role="patient",
            password_plain=DEMO_PATIENT_PIN,
            phone_number="+263-773-000000",
            user_id=p_data["user_id"],
        )
        patient = await _get_or_create_patient(
            db,
            user=user,
            medical_record_number=p_data["mrn"],
            national_id=p_data["national_id"],
            date_of_birth=p_data["dob"],
            gender=p_data["gender"],
            blood_type=p_data["blood_type"],
            patient_id=p_data["user_id"],
        )
        record = await _get_or_create_medical_record(db, patient)
        await _seed_conditions(db, record, count=random.randint(2, 5))
        await _seed_allergies(db, record, count=random.randint(2, 5))
        patients.append((patient, user, record))

    # Create at least one Visit for the demo patient before medications
    demo_patient, demo_user, demo_record = patients[0]
    demo_doctor = doctors[0]
    first_visit = Visit(
        id=uuid.uuid4(),
        medical_record_id=demo_record.id,
        doctor_id=demo_doctor.id,
        facility_id=facilities[0].id,
        visit_date=datetime(2024, 2, 15, 9, 30),
        status="COMPLETED",
        chief_complaint="Routine checkup",
    )
    db.add(first_visit)
    await db.flush()
    await _seed_medications(db, visit=first_visit)
    all_visits = [first_visit]

    # Targets for bulk data
    target_visits = 50
    target_diagnoses = 120
    target_medications = 150
    target_labs = 75
    target_imaging = 25
    target_consents = 20
    target_notifications = 100
    target_ai_sessions = 15
    target_audit_logs = 500

    visits_created = 1  # demo visit already created
    diagnoses_created = 0
    medications_created = 2  # two meds from demo visit
    labs_created = 0
    imaging_created = 0

    # Seed visits and per-visit data
    for patient, user, record in patients:
        num_visits = random.randint(3, 5)
        for _ in range(num_visits):
            if visits_created >= target_visits:
                break
            doctor = random.choice(doctors)
            facility = random.choice(facilities)
            visit_date = datetime(
                random.randint(2022, 2024),
                random.randint(1, 12),
                random.randint(1, 28),
                random.randint(8, 17),
                0,
            )
            visit = Visit(
                id=uuid.uuid4(),
                medical_record_id=record.id,
                doctor_id=doctor.id,
                facility_id=facility.id,
                visit_date=visit_date,
                status="COMPLETED",
                chief_complaint="Routine checkup",
            )
            db.add(visit)
            await db.flush()
            visits_created += 1
            all_visits.append(visit)

            # Diagnoses
            for _ in range(random.randint(1, 3)):
                if diagnoses_created >= target_diagnoses:
                    break
                diag = random.choice(_DIAGNOSES_POOL)
                db.add(
                    Diagnosis(
                        id=uuid.uuid4(),
                        visit_id=visit.id,
                        diagnosis_name=diag[0],
                        icd10_code=diag[1],
                        confidence=diag[2],
                    )
                )
                diagnoses_created += 1

            # Medications
            for _ in range(random.randint(1, 3)):
                if medications_created >= target_medications:
                    break
                med = random.choice(_MEDICATIONS_POOL)
                exists = await db.execute(
                    select(Medication).where(
                        Medication.visit_id == visit.id,
                        Medication.name == med[0],
                    )
                )
                if exists.scalar_one_or_none():
                    continue
                db.add(
                    Medication(
                        id=uuid.uuid4(),
                        visit_id=visit.id,
                        name=med[0],
                        dosage=med[1],
                        frequency=med[2],
                        duration=med[3],
                        instructions=med[4],
                        start_date=date(visit_date.year, visit_date.month, visit_date.day),
                        end_date=None,
                    )
                )
                medications_created += 1

            # Labs
            for _ in range(random.randint(1, 3)):
                if labs_created >= target_labs:
                    break
                lab = random.choice(_LAB_TESTS_POOL)
                db.add(
                    LaboratoryResult(
                        id=uuid.uuid4(),
                        visit_id=visit.id,
                        test_name=lab[0],
                        result=lab[1],
                        status="Completed",
                        performed_at=visit_date,
                    )
                )
                labs_created += 1

            # Imaging
            if random.random() < 0.4 and imaging_created < target_imaging:
                img = random.choice(_IMAGING_POOL)
                db.add(
                    ImagingResult(
                        id=uuid.uuid4(),
                        visit_id=visit.id,
                        modality=img[0],
                        study_name=img[1],
                        report=img[2],
                        performed_at=visit_date,
                    )
                )
                imaging_created += 1

    # Top-up visits to guarantee minimum target
    while visits_created < target_visits:
        patient, user, record = random.choice(patients)
        doctor = random.choice(doctors)
        facility = random.choice(facilities)
        visit_date = datetime(
            random.randint(2022, 2024),
            random.randint(1, 12),
            random.randint(1, 28),
            random.randint(8, 17),
            0,
        )
        visit = Visit(
            id=uuid.uuid4(),
            medical_record_id=record.id,
            doctor_id=doctor.id,
            facility_id=facility.id,
            visit_date=visit_date,
            status="COMPLETED",
            chief_complaint="Routine checkup",
        )
        db.add(visit)
        await db.flush()
        visits_created += 1
        all_visits.append(visit)

    # Top-up diagnoses to guarantee minimum target
    while diagnoses_created < target_diagnoses:
        visit = random.choice(all_visits)
        diag = random.choice(_DIAGNOSES_POOL)
        db.add(
            Diagnosis(
                id=uuid.uuid4(),
                visit_id=visit.id,
                diagnosis_name=diag[0],
                icd10_code=diag[1],
                confidence=diag[2],
            )
        )
        diagnoses_created += 1

    # Top-up medications to guarantee minimum target
    while medications_created < target_medications:
        visit = random.choice(all_visits)
        med = random.choice(_MEDICATIONS_POOL)
        db.add(
            Medication(
                id=uuid.uuid4(),
                visit_id=visit.id,
                name=med[0],
                dosage=med[1],
                frequency=med[2],
                duration=med[3],
                instructions=med[4],
                start_date=date(visit.visit_date.year, visit.visit_date.month, visit.visit_date.day),
                end_date=None,
            )
        )
        medications_created += 1

    # Top-up labs to guarantee minimum target
    while labs_created < target_labs:
        visit = random.choice(all_visits)
        lab = random.choice(_LAB_TESTS_POOL)
        db.add(
            LaboratoryResult(
                id=uuid.uuid4(),
                visit_id=visit.id,
                test_name=lab[0],
                result=lab[1],
                status="Completed",
                performed_at=visit.visit_date,
            )
        )
        labs_created += 1

    # Top-up imaging to guarantee minimum target
    while imaging_created < target_imaging:
        visit = random.choice(all_visits)
        img = random.choice(_IMAGING_POOL)
        db.add(
            ImagingResult(
                id=uuid.uuid4(),
                visit_id=visit.id,
                modality=img[0],
                study_name=img[1],
                report=img[2],
                performed_at=visit.visit_date,
            )
        )
        imaging_created += 1

    # Consent requests
    consent_statuses = ["pending", "approved", "declined", "expired"]
    for _ in range(target_consents):
        patient, user, record = random.choice(patients)
        doctor = random.choice(doctors)
        status = random.choice(consent_statuses)
        requested_at = datetime.now() - timedelta(days=random.randint(1, 60))
        approved_at = None
        expires_at = None
        denied_reason = None
        if status == "approved":
            approved_at = requested_at + timedelta(hours=random.randint(1, 24))
            expires_at = approved_at + timedelta(days=30)
        elif status == "declined":
            denied_reason = "Patient declined access."
        elif status == "expired":
            approved_at = requested_at + timedelta(hours=2)
            expires_at = datetime.now() - timedelta(days=1)
        db.add(
            ConsentRequest(
                id=uuid.uuid4(),
                patient_id=patient.id,
                doctor_id=doctor.id,
                facility_id=random.choice(facilities).id,
                purpose=f"Access for {doctor.specialty} consultation",
                scope=["medical_record", "visits", "lab_results"],
                status=status,
                requested_at=requested_at,
                approved_at=approved_at,
                expires_at=expires_at,
                denied_reason=denied_reason,
            )
        )

    # Notifications
    notif_count = 0
    for patient, user, record in patients:
        for _ in range(10):
            if notif_count >= target_notifications:
                break
            title, body, priority = random.choice(_NOTIFICATIONS_POOL)
            db.add(
                Notification(
                    id=uuid.uuid4(),
                    recipient_user_id=user.id,
                    type="system",
                    title=title,
                    body=body,
                    priority=priority,
                    is_read=random.choice([True, False]),
                )
            )
            notif_count += 1

    # AI sessions
    for _ in range(target_ai_sessions):
        patient, user, record = random.choice(patients)
        doctor = random.choice(doctors)
        db.add(
            AISession(
                id=uuid.uuid4(),
                patient_id=patient.id,
                doctor_id=doctor.id,
                status="COMPLETED",
                provider_name="mock",
                conversation_summary="AI-assisted consultation summary.",
            )
        )

    # Audit logs
    actions = [
        "LOGIN",
        "VIEW_RECORD",
        "UPDATE_RECORD",
        "CREATE_CONSENT",
        "APPROVE_CONSENT",
        "SEND_NOTIFICATION",
    ]
    resource_types = ["User", "Patient", "MedicalRecord", "Visit", "ConsentRequest", "Notification"]
    for _ in range(target_audit_logs):
        patient, user, record = random.choice(patients)
        db.add(
            AuditLog(
                id=uuid.uuid4(),
                user_id=user.id,
                action=random.choice(actions),
                resource_type=random.choice(resource_types),
                resource_id=record.id,
                ip_address=f"192.168.1.{random.randint(1, 255)}",
                user_agent="Mozilla/5.0",
            )
        )

    await db.commit()


async def seed_appointments(db: AsyncSession) -> None:
    """Seed demo appointments for doctors if absent."""
    from sqlalchemy import func

    count_result = await db.execute(select(func.count(Appointment.id)))
    if count_result.scalar_one() >= 10:
        return  # Already seeded

    # Load existing doctors and patients
    doctors_result = await db.execute(select(Doctor))
    doctors = doctors_result.scalars().all()
    if not doctors:
        return  # Cannot seed appointments without doctors

    patients_result = await db.execute(select(Patient))
    patients = patients_result.scalars().all()
    if not patients:
        return  # Cannot seed appointments without patients

    appointment_statuses = ["PENDING", "CONFIRMED"]
    for doctor in doctors:
        num_appts = random.randint(3, 8)
        for _ in range(num_appts):
            patient = random.choice(patients)
            appt_date = date.today() + timedelta(days=random.randint(-2, 14))
            start_hour = random.randint(8, 15)
            start_minute = random.choice([0, 30])
            start = time(start_hour, start_minute)
            end = time(start_hour, start_minute + 30) if start_minute == 0 else time(start_hour + 1, 0)

            appt = Appointment(
                id=uuid.uuid4(),
                patient_id=patient.id,
                doctor_id=doctor.id,
                facility_id=doctor.facility_id,
                appointment_date=appt_date,
                allocated_start_time=start,
                allocated_end_time=end,
                desired_duration_minutes=30,
                status=random.choice(appointment_statuses),
                symptoms=random.choice([
                    "Headache and dizziness",
                    "Chest pain on exertion",
                    "Skin rash with itching",
                    "Persistent cough",
                    "Abdominal pain",
                ]),
                reason=random.choice(["routine", "follow-up", "urgent"]),
                priority="NORMAL",
                triage_score=random.randint(40, 70),
            )
            db.add(appt)
    await db.commit()
