"""Appointment booking REST API router."""

from __future__ import annotations

import uuid
from typing import Optional
from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, get_current_patient, get_current_doctor
from app.core.database import get_db
from app.db.models import User
from app.appointment.service import appointment_service
from app.appointment.schemas import (
    AppointmentCreateRequest,
    AppointmentCancelRequest,
    AppointmentResponse,
    AppointmentListResponse,
)
from app.schemas.envelope import Envelope

router = APIRouter()


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
        select(Appointment).where(Appointment.id == appointment_id)
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
# Helper
# ------------------------------------------------------------------

def _to_response(appointment) -> AppointmentResponse:
    """Convert Appointment ORM to response DTO (without nested lazy loading)."""
    return AppointmentResponse(
        id=appointment.id,
        patient_id=appointment.patient_id,
        facility_id=appointment.facility_id,
        doctor_id=appointment.doctor_id,
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


