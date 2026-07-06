from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class ConsentStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    declined = "declined"
    expired = "expired"
    revoked = "revoked"


class ConsentRequestCreate(BaseModel):
    """Schema for creating a new consent request (doctor-initiated)."""

    model_config = ConfigDict()
    doctor_id: uuid.UUID | None = None
    patient_id: uuid.UUID
    purpose: str
    shared_data: List[str]
    expiry_hours: int = Field(default=24, ge=1, le=168)


class ConsentRequestResponse(BaseModel):
    """Schema for a single consent request in API responses."""

    model_config = ConfigDict()
    id: uuid.UUID
    doctor_id: uuid.UUID
    patient_id: uuid.UUID
    doctor_name: str | None = None
    status: str
    purpose: str | None = None
    shared_data: List[str] | None = None
    created_at: datetime
    expiry_date: datetime | None = None
    approved_at: datetime | None = None
    declined_at: datetime | None = None


class ConsentStatusUpdate(BaseModel):
    """Schema for a patient updating the status of a consent request."""

    model_config = ConfigDict()
    status: ConsentStatus


class ConsentListMeta(BaseModel):
    """Pagination metadata for consent list responses."""

    model_config = ConfigDict()
    total: int
    limit: int
    offset: int


class ConsentListResponse(BaseModel):
    """Paginated list of consent requests."""

    model_config = ConfigDict()
    items: List[ConsentRequestResponse]
    meta: ConsentListMeta
