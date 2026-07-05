from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Generic, TypeVar, List

from pydantic import BaseModel, Field, ConfigDict

T = TypeVar("T")


class ErrorDetail(BaseModel):
    """Standard error detail used in API responses."""

    model_config = ConfigDict(strict=True)
    code: str
    message: str
    field: str | None = None


class Meta(BaseModel):
    """Metadata wrapper for API responses."""

    model_config = ConfigDict(strict=True)
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Envelope(BaseModel, Generic[T]):
    """Standard API response envelope."""

    model_config = ConfigDict(strict=True)
    success: bool = True
    data: T | None = None
    errors: List[ErrorDetail] = Field(default_factory=list)
    meta: Meta = Field(default_factory=Meta)

    @classmethod
    def ok(cls, data: T | None = None) -> Envelope[T]:
        return cls(success=True, data=data, errors=[])

    @classmethod
    def fail(cls, *errors: ErrorDetail) -> Envelope[Any]:
        return cls(success=False, data=None, errors=list(errors))
