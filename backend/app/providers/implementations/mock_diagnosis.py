"""MockDiagnosisProvider — returns mock differential diagnoses."""

from __future__ import annotations

import random
from typing import Any

from app.providers.interfaces.diagnosis import DiagnosisProvider


class MockDiagnosisProvider(DiagnosisProvider):
    """Synthetic diagnosis provider for local development and testing."""

    async def initialize(self) -> None:
        """No-op initialization."""

    async def validate(self, **params: Any) -> bool:
        return True

    async def execute(self, **params: Any) -> dict[str, Any]:
        return params

    async def generate_differential(
        self,
        symptoms: list[str],
        patient_context: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        diagnoses = [
            {
                "name": "Community-acquired pneumonia",
                "confidence": round(random.uniform(0.60, 0.85), 2),
                "reasoning": "Fever and productive cough support bacterial pneumonia.",
                "recommended_investigations": ["Chest X-ray", "CBC", "CRP"],
                "medication_warnings": ["Macrolide resistance rising in this region."],
            },
            {
                "name": "Viral upper respiratory infection",
                "confidence": round(random.uniform(0.55, 0.80), 2),
                "reasoning": "Symptoms are relatively mild and lack focal findings.",
                "recommended_investigations": ["Rapid flu test", "COVID PCR"],
                "medication_warnings": ["Antibiotics not indicated."],
            },
            {
                "name": "Acute bronchitis",
                "confidence": round(random.uniform(0.50, 0.75), 2),
                "reasoning": "Cough predominant with clear auscultation.",
                "recommended_investigations": ["Chest X-ray if fever persists >3 days"],
                "medication_warnings": [],
            },
            {
                "name": "Influenza",
                "confidence": round(random.uniform(0.40, 0.70), 2),
                "reasoning": "Sudden onset with myalgias and high fever.",
                "recommended_investigations": ["Rapid flu test"],
                "medication_warnings": ["Consider antiviral if within 48 hours."],
            },
            {
                "name": "COVID-19",
                "confidence": round(random.uniform(0.30, 0.65), 2),
                "reasoning": "Non-specific viral symptoms; local prevalence is moderate.",
                "recommended_investigations": ["COVID PCR", "Pulse oximetry"],
                "medication_warnings": ["Monitor for hypoxia."],
            },
        ]
        # Shuffle a bit so caller sees variety
        random.shuffle(diagnoses)
        return diagnoses[:5]
