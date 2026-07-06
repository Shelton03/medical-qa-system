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

    async def generate_differential_diagnosis(
        self,
        conversation_history: list[AIMessage],
        context: AIContext,
    ) -> dict:
        """Return a realistic differential diagnosis structure."""
        return {
            "diagnoses": [
                {
                    "name": "Community-acquired pneumonia",
                    "confidence": 0.83,
                    "reasoning": "Productive cough, fever, and focal chest signs consistent with bacterial pneumonia.",
                    "recommendedInvestigations": [
                        "Chest X-ray",
                        "CBC with differential",
                        "Sputum culture",
                        "Blood culture",
                    ],
                    "medicationWarnings": [
                        "Check penicillin allergy before prescribing amoxicillin-clavulanate.",
                    ],
                },
                {
                    "name": "Acute bronchitis",
                    "confidence": 0.72,
                    "reasoning": "Viral prodrome with persistent cough; no focal consolidation signs.",
                    "recommendedInvestigations": [
                        "Chest X-ray to rule out pneumonia",
                    ],
                    "medicationWarnings": [
                        "Avoid antibiotics unless bacterial infection confirmed.",
                    ],
                },
                {
                    "name": "COVID-19",
                    "confidence": 0.65,
                    "reasoning": "Fever, cough, and recent exposure risk; compatible symptom timeline.",
                    "recommendedInvestigations": [
                        "RT-PCR test",
                        "Pulse oximetry",
                    ],
                    "medicationWarnings": [
                        "Assess drug interactions with Paxlovid if indicated.",
                    ],
                },
            ]
        }

    async def generate_clinical_summary(
        self,
        conversation_history: list[AIMessage],
        context: AIContext,
    ) -> dict:
        """Return a realistic SOAP note structure."""
        return {
            "soap": {
                "subjective": (
                    "Patient reports productive cough for 3 days, associated with fever and pleuritic chest pain. "
                    "No hemoptysis. Recent URI symptoms. No known sick contacts."
                ),
                "objective": (
                    "Temp 38.5C, HR 96, RR 20, BP 122/78, SpO2 94% on room air. "
                    "Right lower lobe crackles on auscultation. No wheeze."
                ),
                "assessment": (
                    "Likely community-acquired pneumonia (RLL) vs acute bronchitis. "
                    "Oxygen saturation mildly reduced. No signs of respiratory failure."
                ),
                "plan": (
                    "1. Chest X-ray and labs (CBC, sputum culture).\n"
                    "2. Empiric antibiotics if consolidation confirmed.\n"
                    "3. Hydration, antipyretics, and reassess in 48 hours.\n"
                    "4. Return if worsening dyspnea or SpO2 < 92%."
                ),
            }
        }
