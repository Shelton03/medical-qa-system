"""Appointment booking system Pydantic schemas."""

from __future__ import annotations

import uuid
from datetime import date, time, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.appointment.enums import AppointmentStatus, Priority


# ------------------------------------------------------------------
# Request Schemas
# ------------------------------------------------------------------
class AppointmentCreateRequest(BaseModel):
    facility_id: str
    appointment_date: str
    desired_duration_minutes: int = Field(default=30, ge=15, le=120)
    symptoms: str = Field(..., min_length=10, max_length=2000)
    reason: Optional[str] = Field(default=None, max_length=500)
    is_emergency: bool = False
    preferred_doctor_id: Optional[uuid.UUID] = None


class AppointmentCancelRequest(BaseModel):
    model_config = ConfigDict(strict=True)

    reason: str = Field(..., min_length=5, max_length=500)


# ------------------------------------------------------------------
# Response Schemas (Nested)
# ------------------------------------------------------------------
class DoctorBrief(BaseModel):
    model_config = ConfigDict(strict=True)

    id: uuid.UUID
    name: str
    specialty: Optional[str] = None


class FacilityBrief(BaseModel):
    model_config = ConfigDict(strict=True)

    id: uuid.UUID
    name: str
    city: Optional[str] = None


class SlotAllocationResponse(BaseModel):
    model_config = ConfigDict(strict=True)

    start_time: time
    end_time: time
    buffer_after_minutes: int


# ------------------------------------------------------------------
# Response Schemas
# ------------------------------------------------------------------
class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    patient_id: uuid.UUID
    facility_id: uuid.UUID
    doctor_id: Optional[uuid.UUID] = None
    visit_id: Optional[uuid.UUID] = None

    appointment_date: date
    desired_duration_minutes: int
    allocated_start_time: Optional[time] = None
    allocated_end_time: Optional[time] = None

    status: str
    reason: Optional[str] = None
    symptoms: Optional[str] = None
    priority: str
    is_emergency: bool
    triage_score: int

    preferred_doctor_id: Optional[uuid.UUID] = None

    created_at: datetime


class AppointmentListResponse(BaseModel):
    model_config = ConfigDict(strict=True)

    items: list[AppointmentResponse]
    total: int
    limit: int
    offset: int


# ------------------------------------------------------------------
# Doctor Schedule Schemas
# ------------------------------------------------------------------
class DoctorScheduleCreate(BaseModel):
    model_config = ConfigDict(strict=True)

    day_of_week: int = Field(..., ge=0, le=6)
    start_time: time
    end_time: time
    is_working_day: bool = True
    default_slot_duration: int = Field(default=30, ge=15, le=120)
    max_daily_appointments: int = Field(default=20, ge=1, le=50)


class DoctorScheduleResponse(BaseModel):
    model_config = ConfigDict(strict=True)

    id: uuid.UUID
    doctor_id: uuid.UUID
    day_of_week: int
    start_time: time
    end_time: time
    is_working_day: bool
    default_slot_duration: int
    max_daily_appointments: int


# ------------------------------------------------------------------
# Time Off Schemas
# ------------------------------------------------------------------
class TimeOffRequest(BaseModel):
    model_config = ConfigDict(strict=True)

    doctor_id: uuid.UUID
    start_date: date
    end_date: date
    type: str = "LEAVE"
    reason: Optional[str] = None


class TimeOffResponse(BaseModel):
    model_config = ConfigDict(strict=True)

    id: uuid.UUID
    doctor_id: uuid.UUID
    start_date: date
    end_date: date
    type: str
    reason: Optional[str] = None
    status: str
    created_at: datetime
