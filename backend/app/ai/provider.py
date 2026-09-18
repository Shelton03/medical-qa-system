#!/usr/bin/env python3
"""AI Provider Interface — abstract contract for all AI vendor integrations."""

from __future__ import annotations

import abc
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from app.shared.schemas import MedicalRecordResponse


@dataclass
class AIMessage:
    """A single message in an AI conversation."""

    role: str  # "system" | "user" | "assistant"
    content: str
    timestamp: datetime
    metadata: dict | None = None


@dataclass
class PatientClinicalProfile:
    """Structured clinical snapshot for AI context enrichment."""

    demographics: dict | None = None
    allergies: list[dict] = field(default_factory=list)
    chronic_conditions: list[dict] = field(default_factory=list)
    current_medications: list[dict] = field(default_factory=list)
    recent_visits: list[dict] = field(default_factory=list)
    previous_ai_sessions: list[dict] = field(default_factory=list)


@dataclass
class AIContext:
    """Context provided to an AI provider for a given session."""

    patient_id: UUID | None = None
    doctor_id: UUID | None = None
    session_id: UUID | None = None
    available_data: list[str] = field(default_factory=list)
    clinical_profile: PatientClinicalProfile | None = None


class AIProvider(abc.ABC):
    """
    Abstract base class for AI providers.

    All AI vendor integrations (OpenAI, Anthropic, Mock, etc.) must implement
    this interface. Business logic must never depend on concrete implementations.
    """

    @abc.abstractmethod
    async def generate_response(
        self,
        conversation_history: list[AIMessage],
        context: AIContext,
    ) -> str:
        """Generate a complete response given conversation history and context."""

    @abc.abstractmethod
    async def generate_stream(
        self,
        conversation_history: list[AIMessage],
        context: AIContext,
    ) -> AsyncIterator[str]:
        """Yield text chunks for a streaming response."""

    @abc.abstractmethod
    async def analyze_medical_record(
        self,
        record: MedicalRecordResponse,
        query: str,
    ) -> str:
        """Analyze a medical record and return a structured analysis."""
