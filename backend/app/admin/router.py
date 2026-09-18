"""Admin router for facility and user management."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import require_role
from app.core.database import get_db
from app.db.models import Doctor, Facility, SystemConfig, User
from app.schemas.envelope import Envelope
from app.shared.exceptions import ConflictException, NotFoundException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class FacilityCreateRequest(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None


class FacilityUpdateRequest(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None


class FacilityResponse(BaseModel):
    id: uuid.UUID
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None
    doctor_count: int = 0


# ---------------------------------------------------------------------------
# Facilities
# ---------------------------------------------------------------------------


@router.get("/facilities", response_model=Envelope[list[FacilityResponse]])
async def list_facilities(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
) -> Envelope[list[FacilityResponse]]:
    result = await db.execute(select(Facility).order_by(Facility.name))
    facilities = result.scalars().all()

    # Count doctors per facility in a single grouped query
    count_result = await db.execute(
        select(Doctor.facility_id, func.count(Doctor.id)).group_by(Doctor.facility_id)
    )
    doctor_counts = {fid: cnt for fid, cnt in count_result.all()}

    return Envelope.ok(
        [
            FacilityResponse(
                id=f.id,
                name=f.name,
                address=f.address,
                phone=f.phone,
                email=f.email,
                city=f.city,
                country=f.country,
                timezone=f.timezone,
                doctor_count=doctor_counts.get(f.id, 0),
            )
            for f in facilities
        ]
    )


@router.post("/facilities", response_model=Envelope[FacilityResponse], status_code=201)
async def create_facility(
    body: FacilityCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
) -> Envelope[FacilityResponse]:
    facility = Facility(
        id=uuid.uuid4(),
        name=body.name,
        address=body.address,
        phone=body.phone,
        email=body.email,
        city=body.city,
        country=body.country,
        timezone=body.timezone,
    )
    db.add(facility)
    await db.commit()
    await db.refresh(facility)
    return Envelope.ok(
        FacilityResponse(
            id=facility.id,
            name=facility.name,
            address=facility.address,
            phone=facility.phone,
            email=facility.email,
            city=facility.city,
            country=facility.country,
            timezone=facility.timezone,
            doctor_count=0,
        )
    )


@router.get("/facilities/{facility_id}", response_model=Envelope[FacilityResponse])
async def get_facility(
    facility_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
) -> Envelope[FacilityResponse]:
    result = await db.execute(select(Facility).where(Facility.id == facility_id))
    facility = result.scalar_one_or_none()
    if not facility:
        raise NotFoundException("Facility not found.")

    count_result = await db.execute(
        select(func.count(Doctor.id)).where(Doctor.facility_id == facility.id)
    )
    doctor_count = count_result.scalar() or 0

    return Envelope.ok(
        FacilityResponse(
            id=facility.id,
            name=facility.name,
            address=facility.address,
            phone=facility.phone,
            email=facility.email,
            city=facility.city,
            country=facility.country,
            timezone=facility.timezone,
            doctor_count=doctor_count,
        )
    )


@router.put("/facilities/{facility_id}", response_model=Envelope[FacilityResponse])
async def update_facility(
    facility_id: uuid.UUID,
    body: FacilityUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
) -> Envelope[FacilityResponse]:
    result = await db.execute(select(Facility).where(Facility.id == facility_id))
    facility = result.scalar_one_or_none()
    if not facility:
        raise NotFoundException("Facility not found.")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(facility, field, value)

    await db.commit()
    await db.refresh(facility)

    count_result = await db.execute(
        select(func.count(Doctor.id)).where(Doctor.facility_id == facility.id)
    )
    doctor_count = count_result.scalar() or 0

    return Envelope.ok(
        FacilityResponse(
            id=facility.id,
            name=facility.name,
            address=facility.address,
            phone=facility.phone,
            email=facility.email,
            city=facility.city,
            country=facility.country,
            timezone=facility.timezone,
            doctor_count=doctor_count,
        )
    )


@router.delete("/facilities/{facility_id}")
async def delete_facility(
    facility_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
) -> None:
    result = await db.execute(select(Facility).where(Facility.id == facility_id))
    facility = result.scalar_one_or_none()
    if not facility:
        raise NotFoundException("Facility not found.")

    count_result = await db.execute(
        select(func.count(Doctor.id)).where(Doctor.facility_id == facility.id)
    )
    doctor_count = count_result.scalar() or 0

    if doctor_count > 0:
        raise ConflictException("Cannot delete facility with assigned doctors.")

    await db.delete(facility)
    await db.commit()


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

class SystemConfigItem(BaseModel):
    key: str
    value: str
    description: Optional[str] = None
    updated_at: Optional[datetime] = None


class SystemConfigUpdateRequest(BaseModel):
    value: str


DEFAULT_CONFIGS = {
    "facility_open_time": ("08:00", "Default facility opening time (HH:MM)"),
    "facility_close_time": ("17:00", "Default facility closing time (HH:MM)"),
    "default_slot_duration": ("30", "Default appointment slot duration in minutes"),
    "auto_reminder_hours": ("24", "Hours before appointment to send reminder"),
    "emergency_triage_threshold": ("80", "Triage score threshold for auto-escalation to emergency"),
    "max_daily_appointments_per_doctor": ("20", "Maximum appointments a doctor can have per day"),
}


@router.get("/settings", response_model=Envelope[list[SystemConfigItem]])
async def list_settings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    # Seed defaults if table is empty
    result = await db.execute(select(SystemConfig))
    existing = {c.key: c for c in result.scalars().all()}

    if not existing:
        for key, (value, desc) in DEFAULT_CONFIGS.items():
            db.add(SystemConfig(key=key, value=value, description=desc))
        await db.commit()
        result = await db.execute(select(SystemConfig))
        existing = {c.key: c for c in result.scalars().all()}

    return Envelope.ok([
        SystemConfigItem(
            key=c.key,
            value=c.value,
            description=c.description,
            updated_at=c.updated_at,
        )
        for c in existing.values()
    ])


@router.put("/settings/{key}", response_model=Envelope[SystemConfigItem])
async def update_setting(
    key: str,
    body: SystemConfigUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    result = await db.execute(select(SystemConfig).where(SystemConfig.key == key))
    config = result.scalar_one_or_none()
    if not config:
        raise NotFoundException(f"Setting '{key}' not found.")
    config.value = body.value
    config.updated_by = current_user.id
    await db.commit()
    await db.refresh(config)
    return Envelope.ok(SystemConfigItem(
        key=config.key,
        value=config.value,
        description=config.description,
        updated_at=config.updated_at,
    ))
