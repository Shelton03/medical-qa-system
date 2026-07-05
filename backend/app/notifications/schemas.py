"""Pydantic schemas for the notifications domain."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class NotificationResponse(BaseModel):
    """Single notification representation."""

    model_config = ConfigDict(strict=True, from_attributes=True)

    id: uuid.UUID
    type: str
    title: str
    body: str | None = None
    is_read: bool
    created_at: datetime


class NotificationListResponse(BaseModel):
    """Paginated list of notifications."""

    model_config = ConfigDict(strict=True)

    items: list[NotificationResponse]
    total: int
    limit: int
    offset: int


class UnreadCountResponse(BaseModel):
    """Unread notification count payload."""

    model_config = ConfigDict(strict=True)

    count: int


class CountResponse(BaseModel):
    """Generic count payload."""

    model_config = ConfigDict(strict=True)

    count: int


class WebSocketMessage(BaseModel):
    """Standard envelope for every WebSocket event."""

    model_config = ConfigDict(strict=True)

    type: str
    payload: dict[str, Any]
    timestamp: str
