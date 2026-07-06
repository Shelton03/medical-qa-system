#!/usr/bin/env python3
"""Pydantic schemas for AI session and message endpoints."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AISessionCreate(BaseModel):
    model_config = ConfigDict()
    patient_id: UUID | None = None


class AISessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    patient_id: UUID | None = None
    doctor_id: UUID | None = None
    consultation_id: UUID | None = None
    provider_name: str | None = None
    status: str
    started_at: datetime
    completed_at: datetime | None = None
    conversation_summary: str | None = None


class AIMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    session_id: UUID
    role: str
    content: str
    token_count: int | None = None
    created_at: datetime


class AISessionWithMessagesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    patient_id: UUID | None = None
    doctor_id: UUID | None = None
    consultation_id: UUID | None = None
    provider_name: str | None = None
    status: str
    started_at: datetime
    completed_at: datetime | None = None
    conversation_summary: str | None = None
    messages: list[AIMessageResponse] = Field(default_factory=list)


class AIMessageCreate(BaseModel):
    model_config = ConfigDict()
    content: str = Field(..., min_length=1)
