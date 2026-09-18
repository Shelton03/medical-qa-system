"""Appointment booking REST API router."""

from __future__ import annotations

import uuid
from typing import Optional
from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.auth.dependencies import get_current_user, get_current_patient, get_current_doctor, require_role
from app.core.database import get_db
from app.db.models import User, Patient, Appointment, Doctor, DoctorSchedule, DoctorTimeOff, Facility
from app.appointment.service import appointment_service
from app.appointment.schemas import (
    AppointmentCreateRequest,
    AppointmentCancelRequest,
    AppointmentResponse,
    AppointmentListResponse,
    AppointmentAdminItemResponse,
    AdminAppointmentListResponse,
    DoctorScheduleCreate,
    DoctorScheduleResponse,
    TimeOffRequest,
    TimeOffResponse,
)
from app.schemas.envelope import Envelope

router = APIRouter()


@router.get(
    "/consultations",
    response_model=Envelope[list[dict]],
    summary="List consultations (patient-friendly alias)",
)
async def list_consultations_alias(
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[list[dict]]:
    """Patient-friendly alias for listing consultations (visits)."""
    from app.doctor import service as doctor_service
    from app.doctor.router import _resolve_patient_id, _resolve_doctor_id

    if current_user.role == "doctor":
        doctor_id = await _resolve_doctor_id(db, current_user.id)
        visits, _ = await doctor_service.list_visits_for_doctor(
            db, doctor_id, limit=limit, offset=offset, status=status
        )
    else:
        patient_id = await _resolve_patient_id(db, current_user.id)
        visits, _ = await doctor_service.list_visits_for_patient(
            db, patient_id, limit=limit, offset=offset, status=status
        )

    return Envelope.ok([
        {
            "id": str(v.id),
            "patient_id": str(v.patient_id) if v.patient_id else None,
            "doctor_id": str(v.doctor_id),
            "facility_id": str(v.facility_id) if v.facility_id else None,
            "visit_date": v.visit_date.isoformat() if v.visit_date else None,
            "status": v.status,
            "reason": v.reason,
            "chief_complaint": v.chief_complaint,
        }
        for v in visits
    ])


# ------------------------------------------------------------------
# Patient Endpoints
# ------------------------------------------------------------------

@router.post(
    "",
    response_model=Envelope[AppointmentResponse],
    summary="Create appointment",
    description="Book an appointment at a facility. Doctor is auto-assigned.",
    status_code=201,
)
async def create_appointment(
    body: AppointmentCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_patient),
) -> Envelope[AppointmentResponse]:
    """Patient books an appointment."""
    from datetime import date as dt_date

    facility_id = uuid.UUID(body.facility_id) if isinstance(body.facility_id, str) else body.facility_id
    appointment_date = dt_date.fromisoformat(body.appointment_date) if isinstance(body.appointment_date, str) else body.appointment_date
    preferred_doctor_id = uuid.UUID(body.preferred_doctor_id) if isinstance(body.preferred_doctor_id, str) else body.preferred_doctor_id

    appointment = await appointment_service.create_booking(
        db,
        patient_id=current_user.id,  # type: ignore[arg-type]
        facility_id=facility_id,
        appointment_date=appointment_date,
        symptoms=body.symptoms,
        desired_duration_minutes=body.desired_duration_minutes,
        reason=body.reason,
        is_emergency=body.is_emergency,
        preferred_doctor_id=preferred_doctor_id,
    )

    return Envelope.ok(_to_response(appointment))


@router.get(
    "/my",
    response_model=Envelope[AppointmentListResponse],
    summary="List my appointments",
)
async def list_my_appointments(
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_patient),
) -> Envelope[AppointmentListResponse]:
    """Patient lists their appointments."""
    items, total = await appointment_service.get_patient_appointments(
        db, current_user.id, status=status, limit=limit, offset=offset  # type: ignore[arg-type]
    )

    return Envelope.ok(
        AppointmentListResponse(
            items=[_to_response(a) for a in items],
            total=total,
            limit=limit,
            offset=offset,
        )
    )





# ------------------------------------------------------------------
# Doctor Endpoints
# ------------------------------------------------------------------

@router.get(
    "/doctor/schedule",
    response_model=Envelope[list[AppointmentResponse]],
    summary="View doctor schedule",
)
async def get_doctor_schedule(
    date: Optional[date] = Query(None, description="Date to view (default: today)"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[list[AppointmentResponse]]:
    """Doctor views their schedule for a specific date."""
    from app.doctor.repository import _resolve_doctor_id

    doctor_id = await _resolve_doctor_id(db, current_user.id)
    appointments = await appointment_service.get_doctor_schedule(
        db, doctor_id, query_date=date
    )

    return Envelope.ok([_to_response(a) for a in appointments])


@router.put(
    "/doctor/appointments/{appointment_id}/status",
    response_model=Envelope[AppointmentResponse],
    summary="Update appointment status",
)
async def update_appointment_status(
    appointment_id: uuid.UUID,
    status: str = Query(..., description="New status: CONFIRMED, COMPLETED, CANCELLED"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[AppointmentResponse]:
    """Doctor updates appointment status."""
    from sqlalchemy import select
    from app.db.models import Appointment

    result = await db.execute(
        select(Appointment).where(
            Appointment.id == appointment_id,
            Appointment.doctor_id == current_user.id,
        )
    )
    appointment = result.scalar_one_or_none()
    if not appointment:
        from app.shared.exceptions import NotFoundException
        raise NotFoundException("Appointment not found.")

    appointment.status = status
    if status == "CONFIRMED":
        appointment.doctor_confirmed_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(appointment)

    return Envelope.ok(_to_response(appointment))


# ------------------------------------------------------------------
# Facility Endpoints
# ------------------------------------------------------------------

@router.get(
    "/facilities",
    response_model=Envelope[dict],
    summary="List facilities",
)
async def list_facilities(
    q: Optional[str] = Query(None, description="Search query"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[dict]:
    """List/search facilities."""
    stmt = select(Facility).order_by(Facility.name).offset(offset).limit(limit)
    if q:
        stmt = select(Facility).where(
            Facility.name.ilike(f"%{q}%") | Facility.city.ilike(f"%{q}%")
        ).order_by(Facility.name).offset(offset).limit(limit)
    
    result = await db.execute(stmt)
    facilities = result.scalars().all()

    # Count total for pagination metadata
    count_stmt = select(func.count(Facility.id))
    if q:
        count_stmt = count_stmt.where(
            Facility.name.ilike(f"%{q}%") | Facility.city.ilike(f"%{q}%")
        )
    count_result = await db.execute(count_stmt)
    total = count_result.scalar() or 0

    return Envelope.ok({
        "items": [
            {
                "id": str(f.id),
                "name": f.name,
                "address": f.address,
                "city": f.city,
                "country": f.country,
                "phone": f.phone,
            }
            for f in facilities
        ],
        "total": total,
        "limit": limit,
        "offset": offset,
    })


@router.get(
    "/facilities/{facility_id}/doctors",
    response_model=Envelope[list[dict]],
    summary="List doctors at facility",
)
async def list_facility_doctors(
    facility_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[list[dict]]:
    """List doctors at a specific facility."""
    result = await db.execute(
        select(Doctor).options(
            selectinload(Doctor.user),
        ).where(
            Doctor.facility_id == facility_id,
            Doctor.is_accepting_appointments == True,
        )
    )
    doctors = result.scalars().all()
    
    return Envelope.ok([
        {
            "id": str(d.id),
            "name": f"Dr. {d.user.first_name or ''} {d.user.last_name or ''}".strip() if d.user else f"Dr. {str(d.id)}",
            "specialty": d.specialty,
        }
        for d in doctors
    ])


# ------------------------------------------------------------------
# Admin Endpoints
# ------------------------------------------------------------------

@router.get(
    "/admin/dashboard",
    response_model=Envelope[dict],
    summary="Admin dashboard stats",
)
async def admin_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
) -> Envelope[dict]:
    """Admin dashboard statistics."""
    today = date.today()
    
    # Count today's appointments
    appt_result = await db.execute(
        select(func.count(Appointment.id)).where(
            Appointment.appointment_date == today,
            Appointment.status.in_(["PENDING", "CONFIRMED"]),
        )
    )
    total_appointments_today = appt_result.scalar() or 0
    
    # Pending confirmations
    pending_result = await db.execute(
        select(func.count(Appointment.id)).where(
            Appointment.status == "PENDING",
        )
    )
    pending_confirmations = pending_result.scalar() or 0
    
    # Doctors on leave today
    leave_result = await db.execute(
        select(func.count(DoctorTimeOff.id)).where(
            DoctorTimeOff.start_date <= today,
            DoctorTimeOff.end_date >= today,
            DoctorTimeOff.status == "APPROVED",
        )
    )
    doctors_on_leave = leave_result.scalar() or 0
    
    # Facility occupancy (simplified: appointments / total capacity)
    capacity_result = await db.execute(
        select(func.sum(Doctor.max_daily_appointments)).where(
            Doctor.is_accepting_appointments == True,
        )
    )
    total_capacity = capacity_result.scalar() or 1
    occupancy_rate = min(100, round((total_appointments_today / max(total_capacity, 1)) * 100))
    
    return Envelope.ok({
        "total_appointments_today": total_appointments_today,
        "pending_confirmations": pending_confirmations,
        "doctors_on_leave": doctors_on_leave,
        "facility_occupancy_rate": occupancy_rate,
        "recent_activity": [],
    })


@router.get(
    "/admin/doctors",
    response_model=Envelope[list[dict]],
    summary="List all doctors (admin)",
)
async def admin_list_doctors(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
) -> Envelope[list[dict]]:
    """List all doctors with schedule summary."""
    result = await db.execute(
        select(Doctor).options(
            selectinload(Doctor.user),
            selectinload(Doctor.facility),
            selectinload(Doctor.schedules),
        ).offset(offset).limit(limit)
    )
    doctors = result.scalars().all()
    
    items = []
    for d in doctors:
        working_days = [s.day_of_week for s in d.schedules if s.is_working_day]
        start_times = [s.start_time for s in d.schedules if s.is_working_day]
        end_times = [s.end_time for s in d.schedules if s.is_working_day]
        items.append({
            "id": str(d.id),
            "first_name": d.user.first_name if d.user else "",
            "last_name": d.user.last_name if d.user else "",
            "specialty": d.specialty,
            "facility_name": d.facility.name if d.facility else "—",
            "working_days": working_days,
            "schedule_start_time": str(min(start_times)) if start_times else "—",
            "schedule_end_time": str(max(end_times)) if end_times else "—",
        })
    
    return Envelope.ok(items)


@router.get(
    "/admin/doctors/{doctor_id}/schedule",
    response_model=Envelope[list[DoctorScheduleResponse]],
    summary="View doctor schedule (admin)",
)
async def admin_get_doctor_schedule(
    doctor_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
) -> Envelope[list[DoctorScheduleResponse]]:
    """Get a doctor's weekly schedule."""
    result = await db.execute(
        select(DoctorSchedule).where(DoctorSchedule.doctor_id == doctor_id)
    )
    schedules = result.scalars().all()
    
    # Ensure all days are represented
    existing_days = {s.day_of_week: s for s in schedules}
    all_days = []
    for day in range(7):
        if day in existing_days:
            s = existing_days[day]
            all_days.append(DoctorScheduleResponse(
                id=s.id,
                doctor_id=s.doctor_id,
                day_of_week=s.day_of_week,
                start_time=s.start_time,
                end_time=s.end_time,
                is_working_day=s.is_working_day,
                default_slot_duration=s.default_slot_duration,
                max_daily_appointments=s.max_daily_appointments,
            ))
        else:
            # Default schedule for missing day
            all_days.append(DoctorScheduleResponse(
                id=uuid.UUID(int=0),
                doctor_id=doctor_id,
                day_of_week=day,
                start_time=datetime.strptime("08:00", "%H:%M").time(),
                end_time=datetime.strptime("17:00", "%H:%M").time(),
                is_working_day=day < 5,  # Mon-Fri default
                default_slot_duration=30,
                max_daily_appointments=20,
            ))
    
    return Envelope.ok(sorted(all_days, key=lambda x: x.day_of_week))


@router.put(
    "/admin/doctors/{doctor_id}/schedule",
    response_model=Envelope[list[DoctorScheduleResponse]],
    summary="Update doctor schedule (admin)",
)
async def admin_update_doctor_schedule(
    doctor_id: uuid.UUID,
    schedules: list[DoctorScheduleCreate],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
) -> Envelope[list[DoctorScheduleResponse]]:
    """Update a doctor's weekly schedule. Admin only."""
    # Delete existing schedules
    await db.execute(
        select(DoctorSchedule).where(DoctorSchedule.doctor_id == doctor_id)
    )
    
    # Insert new schedules
    for s in schedules:
        schedule = DoctorSchedule(
            doctor_id=doctor_id,
            day_of_week=s.day_of_week,
            start_time=s.start_time,
            end_time=s.end_time,
            is_working_day=s.is_working_day,
            default_slot_duration=s.default_slot_duration,
            max_daily_appointments=s.max_daily_appointments,
        )
        db.add(schedule)
    
    await db.commit()
    
    # Return updated schedules
    result = await db.execute(
        select(DoctorSchedule).where(DoctorSchedule.doctor_id == doctor_id)
    )
    updated = result.scalars().all()
    
    return Envelope.ok([
        DoctorScheduleResponse(
            id=s.id,
            doctor_id=s.doctor_id,
            day_of_week=s.day_of_week,
            start_time=s.start_time,
            end_time=s.end_time,
            is_working_day=s.is_working_day,
            default_slot_duration=s.default_slot_duration,
            max_daily_appointments=s.max_daily_appointments,
        )
        for s in updated
    ])


@router.post(
    "/admin/doctors/{doctor_id}/time-off",
    response_model=Envelope[TimeOffResponse],
    summary="Add doctor time-off (admin)",
)
async def admin_add_time_off(
    doctor_id: uuid.UUID,
    body: TimeOffRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
) -> Envelope[TimeOffResponse]:
    """Add time-off for a doctor. Admin only."""
    from datetime import date as dt_date
    
    time_off = DoctorTimeOff(
        doctor_id=doctor_id,
        start_date=body.start_date if isinstance(body.start_date, dt_date) else dt_date.fromisoformat(body.start_date),
        end_date=body.end_date if isinstance(body.end_date, dt_date) else dt_date.fromisoformat(body.end_date),
        type=body.type,
        reason=body.reason,
        status="APPROVED",
        requested_by=current_user.id,
        approved_by=current_user.id,
    )
    db.add(time_off)
    await db.commit()
    await db.refresh(time_off)
    
    return Envelope.ok(TimeOffResponse(
        id=time_off.id,
        doctor_id=time_off.doctor_id,
        start_date=time_off.start_date,
        end_date=time_off.end_date,
        type=time_off.type,
        reason=time_off.reason,
        status=time_off.status,
        created_at=time_off.created_at,
    ))


def _to_admin_item(a: Appointment) -> AppointmentAdminItemResponse:
    from datetime import datetime
    dt = None
    if a.appointment_date and a.allocated_start_time:
        dt = datetime.combine(a.appointment_date, a.allocated_start_time)

    patient_name = "Unknown"
    if a.patient and a.patient.user:
        patient_name = f"{a.patient.user.first_name or ''} {a.patient.user.last_name or ''}".strip()

    doctor_name = "Dr. Unknown"
    if a.doctor and a.doctor.user:
        doctor_name = f"{a.doctor.user.first_name or 'Dr.'} {a.doctor.user.last_name or ''}".strip()

    facility_name = a.facility.name if a.facility else "—"

    return AppointmentAdminItemResponse(
        id=a.id,
        date_time=dt,
        patient_id=a.patient_id,
        patient_name=patient_name,
        doctor_id=a.doctor_id,
        doctor_name=doctor_name,
        facility_id=a.facility_id,
        facility_name=facility_name,
        status=a.status,
        priority=a.priority or "NORMAL",
        reason=a.reason,
    )


@router.get(
    "/admin/appointments",
    response_model=Envelope[AdminAppointmentListResponse],
    summary="List all appointments (admin)",
)
async def admin_list_appointments(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
) -> Envelope[AdminAppointmentListResponse]:
    """List all appointments with filters. Admin only."""
    query = select(Appointment)
    
    if date_from:
        query = query.where(Appointment.appointment_date >= date_from)
    if date_to:
        query = query.where(Appointment.appointment_date <= date_to)
    if status:
        query = query.where(Appointment.status == status)
    if priority:
        query = query.where(Appointment.priority == priority)
    
    count_result = await db.execute(
        select(func.count()).select_from(query.subquery())
    )
    total = count_result.scalar() or 0
    
    query = (
        query
        .options(
            selectinload(Appointment.doctor).selectinload(Doctor.user),
            selectinload(Appointment.patient).selectinload(Patient.user),
            selectinload(Appointment.facility),
        )
        .order_by(Appointment.appointment_date.desc(), Appointment.allocated_start_time.asc())
        .offset(offset)
        .limit(limit)
    )
    
    result = await db.execute(query)
    appointments = result.scalars().all()
    
    return Envelope.ok(
        AdminAppointmentListResponse(
            items=[_to_admin_item(a) for a in appointments],
            total=total,
            limit=limit,
            offset=offset,
        )
    )

@router.get(
    "/{appointment_id}",
    response_model=Envelope[AppointmentResponse],
    summary="Get appointment details",
)
async def get_appointment(
    appointment_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[AppointmentResponse]:
    """Get appointment details (patient or doctor)."""
    from sqlalchemy import select
    from app.db.models import Appointment

    result = await db.execute(
        select(Appointment)
        .where(Appointment.id == appointment_id)
        .options(
            selectinload(Appointment.facility),
            selectinload(Appointment.doctor).selectinload(Doctor.user),
        )
    )
    appointment = result.scalar_one_or_none()
    if not appointment:
        from app.shared.exceptions import NotFoundException
        raise NotFoundException("Appointment not found.")

    # Verify access
    if current_user.role == "patient" and appointment.patient_id != current_user.id:
        from app.shared.exceptions import ForbiddenException
        raise ForbiddenException("Access denied.")
    elif current_user.role == "doctor" and appointment.doctor_id != current_user.id:
        from app.shared.exceptions import ForbiddenException
        raise ForbiddenException("Access denied.")

    return Envelope.ok(_to_response(appointment))


@router.put(
    "/{appointment_id}/cancel",
    response_model=Envelope[AppointmentResponse],
    summary="Cancel appointment",
)
async def cancel_appointment(
    appointment_id: uuid.UUID,
    body: AppointmentCancelRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[AppointmentResponse]:
    """Cancel an appointment (patient or doctor)."""
    cancelled_by = "PATIENT" if current_user.role == "patient" else "DOCTOR"

    appointment = await appointment_service.cancel_appointment(
        db,
        appointment_id=appointment_id,
        cancelled_by=cancelled_by,
        user_id=current_user.id,  # type: ignore[arg-type]
        reason=body.reason,
    )

    return Envelope.ok(_to_response(appointment))


@router.post(
    "/{appointment_id}/start-consultation",
    response_model=Envelope[dict],
    summary="Start day-of consultation",
)
async def start_consultation_from_appointment(
    appointment_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_patient),
) -> Envelope[dict]:
    """Patient starts their consultation on the appointment day."""
    visit = await appointment_service.start_consultation_from_appointment(
        db,
        appointment_id=appointment_id,
        patient_id=current_user.id,  # type: ignore[arg-type]
    )

    return Envelope.ok({
        "visit_id": str(visit.id),
        "status": visit.status,
        "message": "Consultation started successfully.",
    })



# ------------------------------------------------------------------
# Helper
# ------------------------------------------------------------------

def _to_response(appointment) -> AppointmentResponse:
    """Convert Appointment ORM to response DTO (without nested lazy loading)."""
    return AppointmentResponse(
        id=appointment.id,
        patient_id=appointment.patient_id,
        facility_id=appointment.facility_id,
        facility_name=appointment.facility.name if appointment.facility else None,
        doctor_id=appointment.doctor_id,
        doctor_name=appointment.doctor.user.last_name if appointment.doctor and appointment.doctor.user else None,
        doctor_specialty=appointment.doctor.specialty if appointment.doctor else None,
        visit_id=appointment.visit_id,
        appointment_date=appointment.appointment_date,
        desired_duration_minutes=appointment.desired_duration_minutes,
        allocated_start_time=appointment.allocated_start_time,
        allocated_end_time=appointment.allocated_end_time,
        status=appointment.status,
        reason=appointment.reason,
        symptoms=appointment.symptoms,
        priority=appointment.priority,
        is_emergency=appointment.is_emergency,
        triage_score=appointment.triage_score,
        preferred_doctor_id=appointment.preferred_doctor_id,
        created_at=appointment.created_at,
    )
