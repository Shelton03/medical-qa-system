"""Appointment service with auto-routing algorithm."""

from __future__ import annotations

import uuid
from datetime import date, datetime, time, timedelta, timezone
from typing import Optional, Tuple, List

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import (
    Appointment,
    AppointmentSlotAllocation,
    Doctor,
    DoctorSchedule,
    DoctorTimeOff,
    Patient,
    Facility,
    Visit,
    User,
    MedicalRecord,
)
from app.appointment.enums import AppointmentStatus, Priority, CancellationBy
from app.doctor.repository import create_visit
from app.shared.exceptions import (
    NotFoundException,
    ValidationException,
    ForbiddenException,
)

# ------------------------------------------------------------------
# Specialty keyword mapping for symptom matching
# ------------------------------------------------------------------
SPECIALTY_KEYWORDS = {
    "cardiology": [
        "heart", "chest pain", "chest", "blood pressure", "hypertension",
        "cardiac", "palpitations", "arrhythmia", "heart attack",
    ],
    "pediatrics": [
        "child", "baby", "infant", "toddler", "fever", "cough",
        "vaccination", "growth", "development",
    ],
    "obstetrics and gynaecology": [
        "pregnancy", "pregnant", "menstrual", "period", "ovary",
        "gynaecology", "fertility", "birth", "antenatal",
    ],
    "internal medicine": [
        "diabetes", "thyroid", "hormone", "chronic", "fatigue",
        "weight loss", "general", "unspecified",
    ],
    "general practice": [
        "cold", "flu", "headache", "rash", "checkup", "review",
    ],
    "dermatology": [
        "skin", "rash", "acne", "eczema", "psoriasis", "lesion",
        "mole", "itching", "dermatitis",
    ],
    "orthopedics": [
        "bone", "fracture", "joint", "knee", "back pain", "shoulder",
        "sprain", "arthritis", "muscle",
    ],
    "neurology": [
        "headache", "migraine", "seizure", "tremor", "numbness",
        "memory", "dizziness", "stroke",
    ],
    "psychiatry": [
        "anxiety", "depression", "stress", "insomnia", "mood",
        "mental health", "panic", "trauma",
    ],
    "gastroenterology": [
        "stomach", "abdominal pain", "nausea", "vomiting", "diarrhea",
        "constipation", "liver", "digestion",
    ],
    "urology": [
        "urinary", "kidney", "bladder", "prostate", "urination",
    ],
    "pulmonology": [
        "cough", "breathing", "asthma", "pneumonia", "tb",
        "tuberculosis", "shortness of breath", "chest tightness",
    ],
    "endocrinology": [
        "diabetes", "thyroid", "hormone", "metabolism", "weight",
        "growth", "pituitary",
    ],
    "nephrology": [
        "kidney", "renal", "dialysis", "proteinuria", "creatinine",
    ],
    "hematology": [
        "anemia", "bleeding", "clotting", "blood", "transfusion",
    ],
    "infectious disease": [
        "infection", "fever", "malaria", "hiv", "tb", "sepsis",
    ],
    "oncology": [
        "cancer", "tumor", "mass", "chemotherapy", "radiation",
    ],
    "ophthalmology": [
        "eye", "vision", "blurred", "cataract", "glaucoma", "retinopathy",
    ],
    "ent": [
        "ear", "nose", "throat", "sinus", "hearing", "tonsils",
    ],
}


# ------------------------------------------------------------------
# Auto-Routing Service
# ------------------------------------------------------------------
class AutoRoutingService:
    """Intelligent doctor assignment based on history, specialty, and workload."""

    async def find_optimal_doctor(
        self,
        db: AsyncSession,
        facility_id: uuid.UUID,
        patient_id: uuid.UUID,
        symptoms: str,
        appointment_date: date,
        desired_duration: int = 30,
        is_emergency: bool = False,
        preferred_doctor_id: Optional[uuid.UUID] = None,
    ) -> uuid.UUID | None:
        """Find the best doctor for an appointment. Returns doctor_id or None."""
        
        doctors = await self._get_available_doctors(db, facility_id, appointment_date)
        if not doctors:
            return None

        # Emergency: bypass scoring, pick first available
        if is_emergency:
            for doctor in doctors:
                if await self._has_capacity(db, doctor.id, appointment_date, desired_duration):
                    return doctor.id
            return None

        # Score each doctor
        scored: List[Tuple[Doctor, int]] = []
        for doctor in doctors:
            if not await self._has_capacity(db, doctor.id, appointment_date, desired_duration):
                continue

            score = 0
            score += await self._calculate_history_score(db, patient_id, doctor.id)
            score += self._calculate_specialty_score(symptoms, doctor.specialty)
            score += await self._calculate_workload_score(db, doctor.id, appointment_date)

            if preferred_doctor_id and doctor.id == preferred_doctor_id:
                score += 15

            scored.append((doctor, score))

        if not scored:
            return None

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[0][0].id

    async def _get_available_doctors(
        self, db: AsyncSession, facility_id: uuid.UUID, appointment_date: date
    ) -> List[Doctor]:
        """Get doctors at facility who are working and not on leave."""
        
        # Get doctors at facility who accept appointments
        result = await db.execute(
            select(Doctor)
            .where(
                Doctor.facility_id == facility_id,
                Doctor.is_accepting_appointments == True,
            )
        )
        doctors = result.scalars().all()

        available = []
        for doctor in doctors:
            # Check if working on this day
            day_of_week = appointment_date.weekday()
            schedule_result = await db.execute(
                select(DoctorSchedule).where(
                    DoctorSchedule.doctor_id == doctor.id,
                    DoctorSchedule.day_of_week == day_of_week,
                    DoctorSchedule.is_working_day == True,
                )
            )
            if not schedule_result.scalar_one_or_none():
                continue

            # Check if on leave
            leave_result = await db.execute(
                select(DoctorTimeOff).where(
                    DoctorTimeOff.doctor_id == doctor.id,
                    DoctorTimeOff.start_date <= appointment_date,
                    DoctorTimeOff.end_date >= appointment_date,
                    DoctorTimeOff.status == "APPROVED",
                )
            )
            if leave_result.scalar_one_or_none():
                continue

            available.append(doctor)

        return available

    async def _has_capacity(
        self, db: AsyncSession, doctor_id: uuid.UUID, appointment_date: date, desired_duration: int
    ) -> bool:
        """Check if doctor has capacity for the appointment date."""
        
        # Get doctor's max appointments
        result = await db.execute(
            select(Doctor.max_daily_appointments).where(Doctor.id == doctor_id)
        )
        max_appointments = result.scalar_one_or_none() or 20

        # Count existing confirmed appointments
        count_result = await db.execute(
            select(func.count(Appointment.id)).where(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_date == appointment_date,
                Appointment.status.in_(["PENDING", "CONFIRMED"]),
            )
        )
        current_count = count_result.scalar() or 0

        return current_count < max_appointments

    async def _calculate_history_score(
        self, db: AsyncSession, patient_id: uuid.UUID, doctor_id: uuid.UUID
    ) -> int:
        """Calculate history match score (0-35)."""
        
        # Check if patient has seen this doctor before
        result = await db.execute(
            select(Visit)
            .join(MedicalRecord)
            .where(
                MedicalRecord.patient_id == patient_id,
                Visit.doctor_id == doctor_id,
            )
            .limit(1)
        )
        if result.scalar_one_or_none():
            return 35

        # Check if same specialty as previous visits
        result = await db.execute(
            select(Doctor.specialty)
            .join(Visit, Visit.doctor_id == Doctor.id)
            .join(MedicalRecord)
            .where(
                MedicalRecord.patient_id == patient_id,
            )
            .limit(1)
        )
        previous_specialty = result.scalar_one_or_none()
        if previous_specialty:
            current_specialty_result = await db.execute(
                select(Doctor.specialty).where(Doctor.id == doctor_id)
            )
            current_specialty = current_specialty_result.scalar_one_or_none()
            if current_specialty and current_specialty.lower() == previous_specialty.lower():
                return 20

        return 0

    def _calculate_specialty_score(self, symptoms: str, specialty: Optional[str]) -> int:
        """Calculate specialty-symptom match score (0-25)."""
        
        if not specialty or not symptoms:
            return 0

        specialty_lower = specialty.lower()
        symptoms_lower = symptoms.lower()

        keywords = SPECIALTY_KEYWORDS.get(specialty_lower, [])
        if not keywords:
            return 0

        matches = sum(1 for kw in keywords if kw in symptoms_lower)
        if matches >= 3:
            return 25
        elif matches >= 1:
            return 15

        # Check related specialties
        related_map = {
            "general practice": ["internal medicine", "family medicine"],
            "internal medicine": ["general practice", "cardiology", "endocrinology"],
            "cardiology": ["internal medicine", "pulmonology"],
            "pulmonology": ["internal medicine", "cardiology"],
        }
        related = related_map.get(specialty_lower, [])
        for rel in related:
            rel_keywords = SPECIALTY_KEYWORDS.get(rel, [])
            if any(kw in symptoms_lower for kw in rel_keywords):
                return 5

        return 0

    async def _calculate_workload_score(
        self, db: AsyncSession, doctor_id: uuid.UUID, appointment_date: date
    ) -> int:
        """Calculate workload score (0-25). Lower workload = higher score."""
        
        result = await db.execute(
            select(func.count(Appointment.id)).where(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_date == appointment_date,
                Appointment.status.in_(["PENDING", "CONFIRMED"]),
            )
        )
        count = result.scalar() or 0

        # Get max appointments
        max_result = await db.execute(
            select(Doctor.max_daily_appointments).where(Doctor.id == doctor_id)
        )
        max_appointments = max_result.scalar_one_or_none() or 20

        if max_appointments == 0:
            return 0

        ratio = count / max_appointments
        if ratio < 0.3:
            return 25
        elif ratio < 0.6:
            return 15
        elif ratio < 0.8:
            return 5
        return 0


# ------------------------------------------------------------------
# Appointment Service
# ------------------------------------------------------------------
class AppointmentService:
    """Core appointment booking service."""

    def __init__(self) -> None:
        self.routing = AutoRoutingService()

    async def create_booking(
        self,
        db: AsyncSession,
        patient_id: uuid.UUID,
        facility_id: uuid.UUID,
        appointment_date: date,
        symptoms: str,
        desired_duration_minutes: int = 30,
        reason: Optional[str] = None,
        is_emergency: bool = False,
        preferred_doctor_id: Optional[uuid.UUID] = None,
    ) -> Appointment:
        """Create a new appointment with auto-routed doctor assignment."""
        
        # Validate date is not in the past
        if appointment_date < date.today():
            raise ValidationException("Appointment date cannot be in the past.")

        # Validate date is within 30 days
        if appointment_date > date.today() + timedelta(days=30):
            raise ValidationException("Appointments can only be booked up to 30 days in advance.")

        # Find optimal doctor
        doctor_id = await self.routing.find_optimal_doctor(
            db,
            facility_id,
            patient_id,
            symptoms,
            appointment_date,
            desired_duration_minutes,
            is_emergency,
            preferred_doctor_id,
        )

        if not doctor_id:
            raise ValidationException("No doctor is available for the selected date.")

        # Calculate triage score
        triage_score = 0
        if is_emergency:
            triage_score = 100
        else:
            # Simple keyword-based triage
            symptoms_lower = symptoms.lower()
            emergency_keywords = ["chest pain", "can't breathe", "unconscious", "severe bleeding", "heart attack"]
            urgent_keywords = ["high fever", "severe pain", "vomiting blood", "seizure"]
            
            if any(kw in symptoms_lower for kw in emergency_keywords):
                triage_score = 90
            elif any(kw in symptoms_lower for kw in urgent_keywords):
                triage_score = 70
            else:
                triage_score = 50

        # Determine priority
        priority = "EMERGENCY" if is_emergency else "NORMAL"
        if triage_score >= 90:
            priority = "URGENT"

        # Create appointment
        appointment = Appointment(
            patient_id=patient_id,
            facility_id=facility_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            desired_duration_minutes=desired_duration_minutes,
            status="CONFIRMED" if doctor_id else "PENDING",
            symptoms=symptoms,
            reason=reason,
            priority=priority,
            is_emergency=is_emergency,
            triage_score=triage_score,
            preferred_doctor_id=preferred_doctor_id,
        )

        db.add(appointment)
        await db.flush()

        # Allocate time slot
        slot = await self._allocate_time_slot(db, doctor_id, appointment_date, desired_duration_minutes)
        if slot:
            allocation = AppointmentSlotAllocation(
                appointment_id=appointment.id,
                doctor_id=doctor_id,
                slot_date=appointment_date,
                start_time=slot[0],
                end_time=slot[1],
            )
            db.add(allocation)
            appointment.allocated_start_time = slot[0]
            appointment.allocated_end_time = slot[1]

        await db.commit()
        await db.refresh(appointment)

        # TODO: Send notification to doctor

        return appointment

    async def _allocate_time_slot(
        self,
        db: AsyncSession,
        doctor_id: uuid.UUID,
        appointment_date: date,
        desired_duration: int,
        buffer_minutes: int = 3,
    ) -> Optional[Tuple[time, time]]:
        """Find and allocate a time slot for the appointment."""
        
        day_of_week = appointment_date.weekday()
        
        # Get doctor's schedule
        result = await db.execute(
            select(DoctorSchedule).where(
                DoctorSchedule.doctor_id == doctor_id,
                DoctorSchedule.day_of_week == day_of_week,
                DoctorSchedule.is_working_day == True,
            )
        )
        schedule = result.scalar_one_or_none()
        if not schedule:
            return None

        # Get existing allocations
        allocations_result = await db.execute(
            select(AppointmentSlotAllocation)
            .where(
                AppointmentSlotAllocation.doctor_id == doctor_id,
                AppointmentSlotAllocation.slot_date == appointment_date,
                AppointmentSlotAllocation.status == "ALLOCATED",
            )
            .order_by(AppointmentSlotAllocation.start_time)
        )
        existing = allocations_result.scalars().all()

        # Find available slot
        current_time = schedule.start_time
        total_needed = timedelta(minutes=desired_duration + buffer_minutes)

        for allocation in existing:
            gap = datetime.combine(appointment_date, allocation.start_time) - \
                  datetime.combine(appointment_date, current_time)
            
            if gap >= total_needed:
                end_time = (datetime.combine(appointment_date, current_time) + 
                           timedelta(minutes=desired_duration)).time()
                return (current_time, end_time)
            
            current_time = (datetime.combine(appointment_date, allocation.end_time) +
                           timedelta(minutes=buffer_minutes)).time()

        # Check remaining time
        end_datetime = datetime.combine(appointment_date, schedule.end_time)
        last_datetime = datetime.combine(appointment_date, current_time)
        
        if (end_datetime - last_datetime) >= total_needed:
            end_time = (datetime.combine(appointment_date, current_time) + 
                       timedelta(minutes=desired_duration)).time()
            return (current_time, end_time)

        return None

    async def cancel_appointment(
        self,
        db: AsyncSession,
        appointment_id: uuid.UUID,
        cancelled_by: str,
        user_id: uuid.UUID,
        reason: Optional[str] = None,
    ) -> Appointment:
        """Cancel an appointment with 3-day notice validation."""
        
        result = await db.execute(
            select(Appointment).where(Appointment.id == appointment_id)
        )
        appointment = result.scalar_one_or_none()
        if not appointment:
            raise NotFoundException("Appointment not found.")

        # Verify canceller is patient or assigned doctor
        if cancelled_by == "PATIENT":
            if appointment.patient_id != user_id:
                raise ForbiddenException("You can only cancel your own appointments.")
            
            # Check 3-day notice for patient cancellations
            days_until = (appointment.appointment_date - date.today()).days
            if days_until < 3:
                raise ValidationException(
                    "Cancellations require at least 3 days notice. "
                    f"Your appointment is in {days_until} day(s)."
                )
        elif cancelled_by == "DOCTOR":
            if appointment.doctor_id != user_id:
                raise ForbiddenException("You can only cancel your assigned appointments.")

        appointment.status = "CANCELLED"
        appointment.cancelled_at = datetime.now(timezone.utc)
        appointment.cancelled_by = cancelled_by
        appointment.cancellation_reason = reason

        # Release slot allocation
        if appointment.slot_allocation:
            appointment.slot_allocation.status = "RELEASED"

        await db.commit()
        await db.refresh(appointment)

        return appointment

    async def get_patient_appointments(
        self,
        db: AsyncSession,
        patient_id: uuid.UUID,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[Appointment], int]:
        """List appointments for a patient."""
        
        query = select(Appointment).where(Appointment.patient_id == patient_id)
        
        if status:
            query = query.where(Appointment.status == status)
        
        count_result = await db.execute(
            select(func.count()).select_from(query.subquery())
        )
        total = count_result.scalar() or 0

        query = (
            query
            .options(
                selectinload(Appointment.doctor),
                selectinload(Appointment.facility),
                selectinload(Appointment.slot_allocation),
            )
            .order_by(Appointment.appointment_date.desc())
            .offset(offset)
            .limit(limit)
        )
        
        result = await db.execute(query)
        appointments = result.scalars().all()
        
        return list(appointments), total

    async def get_doctor_schedule(
        self,
        db: AsyncSession,
        doctor_id: uuid.UUID,
        query_date: Optional[date] = None,
    ) -> List[Appointment]:
        """Get appointments for a doctor on a specific date."""
        
        query_date = query_date or date.today()
        
        result = await db.execute(
            select(Appointment)
            .where(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_date == query_date,
                Appointment.status.in_(["PENDING", "CONFIRMED"]),
            )
            .options(
                selectinload(Appointment.patient).selectinload(Patient.user),
                selectinload(Appointment.slot_allocation),
            )
            .order_by(Appointment.allocated_start_time)
        )
        
        return list(result.scalars().all())

    async def start_consultation_from_appointment(
        self,
        db: AsyncSession,
        appointment_id: uuid.UUID,
        patient_id: uuid.UUID,
    ) -> Visit:
        """Start a consultation from an appointment on the appointment day."""
        
        result = await db.execute(
            select(Appointment).where(Appointment.id == appointment_id)
        )
        appointment = result.scalar_one_or_none()
        if not appointment:
            raise NotFoundException("Appointment not found.")

        if appointment.patient_id != patient_id:
            raise ForbiddenException("This appointment belongs to another patient.")

        if appointment.appointment_date != date.today():
            raise ValidationException("You can only start the consultation on the appointment day.")

        if appointment.status != "CONFIRMED":
            raise ValidationException("Appointment must be confirmed to start consultation.")

        # Get medical record for patient
        mr_result = await db.execute(
            select(MedicalRecord.id).where(MedicalRecord.patient_id == appointment.patient_id)
        )
        medical_record_id = mr_result.scalar_one_or_none()
        if not medical_record_id:
            raise NotFoundException("Medical record not found for patient.")
        
        # Create visit
        visit = await create_visit(
            db,
            medical_record_id=medical_record_id,
            doctor_id=appointment.doctor_id,
            facility_id=appointment.facility_id,
            chief_complaint=appointment.symptoms,
            reason=appointment.reason,
        )
        
        # Link appointment to visit
        appointment.visit_id = visit.id
        appointment.status = "COMPLETED"
        await db.commit()

        return visit


# Singleton instance
appointment_service = AppointmentService()
