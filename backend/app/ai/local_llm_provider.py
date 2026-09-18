#!/usr/bin/env python3
"""Local AI Provider — thin wrapper implementing the AIProvider interface."""

from __future__ import annotations

from collections.abc import AsyncIterator

from app.ai.provider import AIContext, AIProvider, AIMessage
from app.shared.schemas import MedicalRecordResponse


class LocalAIProvider(AIProvider):
    """Fallback provider backed by the local Gemma model."""

    async def generate_response(
        self,
        conversation_history: list[AIMessage],
        context: AIContext,
    ) -> str:
        """Generate a complete response given conversation history and context."""
        # This is a fallback — the real flow goes through chat_engine directly
        return "Local LLM response"

    async def generate_stream(
        self,
        conversation_history: list[AIMessage],
        context: AIContext,
    ) -> AsyncIterator[str]:
        """Yield text chunks for a streaming response."""
        text = await self.generate_response(conversation_history, context)
        for chunk in text.split():
            yield chunk + " "

    async def analyze_medical_record(
        self,
        record: MedicalRecordResponse,
        query: str,
    ) -> str:
        """Analyze a medical record and return a structured analysis."""
        return "Local LLM medical record analysis"
