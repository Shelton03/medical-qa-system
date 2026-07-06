"""MockClinicalSummaryProvider — returns a SOAP note structure."""

from __future__ import annotations

from typing import Any

from app.providers.interfaces.summary import ClinicalSummaryProvider


class MockClinicalSummaryProvider(ClinicalSummaryProvider):
    """Synthetic clinical-summary provider for local development and testing."""

    async def initialize(self) -> None:
        """No-op initialization."""

    async def validate(self, **params: Any) -> bool:
        return True

    async def execute(self, **params: Any) -> dict[str, Any]:
        return params

    async def generate_soap_note(
        self,
        transcript: str | None = None,
        symptoms: list[str] | None = None,
        diagnoses: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        return {
            "soap": {
                "subjective": (
                    "Patient reports a 3-day history of productive cough, "
                    "fever to 38.5 C, and fatigue. No known sick contacts."
                ),
                "objective": (
                    "Vitals stable. Chest clear to auscultation bilaterally. "
                    "No wheeze or crackles. Oropharynx mildly erythematous."
                ),
                "assessment": (
                    "Likely viral upper respiratory infection. "
                    "Differential includes influenza and COVID-19."
                ),
                "plan": (
                    "Supportive care with acetaminophen, fluids, and rest. "
                    "Return precautions given. Consider rapid flu and COVID testing "
                    "if symptoms persist beyond 48 hours."
                ),
            },
            "diagnoses": diagnoses or [],
            "symptoms": symptoms or [],
        }
