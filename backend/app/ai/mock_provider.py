#!/usr/bin/env python3
"""Mock AI Provider — concrete implementation of AIProvider for development and testing."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator

from app.ai.provider import AIContext, AIMessage, AIProvider
from app.shared.schemas import MedicalRecordResponse

_CLINICAL_DISCLAIMER = (
    "This is an AI-generated suggestion for clinical decision support. "
    "Final diagnoses and treatment plans must be confirmed by the attending physician."
)


def _build_diagnosis_response(context: AIContext) -> str:
    data_list = ", ".join(context.available_data) if context.available_data else "none"
    return (
        f"Based on the available patient data [{data_list}], here is the differential diagnosis:\n\n"
        "1. Community-acquired pneumonia (Confidence: 0.83)\n"
        "   - Rationale: Productive cough, fever, and focal chest signs.\n"
        "2. Acute bronchitis (Confidence: 0.72)\n"
        "   - Rationale: Viral prodrome with persistent cough.\n"
        "3. COVID-19 (Confidence: 0.65)\n"
        "   - Rationale: Fever, cough, and recent exposure risk.\n\n"
        f"{_CLINICAL_DISCLAIMER}"
    )


def _build_medication_response(context: AIContext) -> str:
    data_list = ", ".join(context.available_data) if context.available_data else "none"
    return (
        f"Based on the available patient data [{data_list}], here is the medication analysis:\n\n"
        "- Current medications appear appropriate for the documented chronic conditions.\n"
        "- No major drug-drug interactions detected in the available records.\n"
        "- Monitor renal function given ongoing metformin therapy.\n\n"
        f"{_CLINICAL_DISCLAIMER}"
    )


def _build_generic_response(context: AIContext) -> str:
    data_list = ", ".join(context.available_data) if context.available_data else "none"
    return (
        "I am your clinical assistant. How can I help you today?\n\n"
        f"Available patient context: [{data_list}].\n\n"
        f"{_CLINICAL_DISCLAIMER}"
    )


class MockAIProvider(AIProvider):
    """
    Mock AI provider that returns canned, context-aware responses.

    Useful for development, testing, and when no external AI vendor is configured.
    All responses include the required clinical disclaimer.
    """

    async def generate_response(
        self,
        conversation_history: list[AIMessage],
        context: AIContext,
    ) -> str:
        last_user_message = ""
        for msg in reversed(conversation_history):
            if msg.role == "user":
                last_user_message = msg.content.lower()
                break

        if "diagnosis" in last_user_message or "symptoms" in last_user_message:
            return _build_diagnosis_response(context)
        if "medication" in last_user_message:
            return _build_medication_response(context)
        return _build_generic_response(context)

    async def generate_stream(
        self,
        conversation_history: list[AIMessage],
        context: AIContext,
    ) -> AsyncIterator[str]:
        full_text = await self.generate_response(conversation_history, context)
        chunk_size = 16
        for i in range(0, len(full_text), chunk_size):
            yield full_text[i : i + chunk_size]
            await asyncio.sleep(0.05)

    async def analyze_medical_record(
        self,
        record: MedicalRecordResponse,
        query: str,
    ) -> str:
        return (
            f"Medical Record Analysis (Record ID: {record.id})\n"
            f"Patient ID: {record.patient_id}\n"
            f"Record Status: {record.record_status or 'N/A'}\n"
            f"Query: {query}\n\n"
            "This is a structured analysis placeholder referencing the patient's "
            "medical record conditions, allergies, and medications.\n\n"
            f"{_CLINICAL_DISCLAIMER}"
        )
