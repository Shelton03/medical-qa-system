"""MockSymptomCheckerProvider — returns predefined questions and a mock assessment."""

from __future__ import annotations

import uuid
from typing import Any

from app.providers.interfaces.symptom_checker import SymptomCheckerProvider


class MockSymptomCheckerProvider(SymptomCheckerProvider):
    """Synthetic symptom-checker for local development and testing."""

    async def initialize(self) -> None:
        """No-op initialization."""

    async def validate(self, **params: Any) -> bool:
        return True

    async def execute(self, **params: Any) -> dict[str, Any]:
        return params

    async def begin_session(self, patient_id: str, context: dict[str, Any] | None = None) -> str:
        return str(uuid.uuid4())

    async def submit_answer(self, session_id: str, question_id: str, answer: Any) -> dict[str, Any]:
        return {
            "session_id": session_id,
            "done": question_id.startswith("q3"),
            "next_question": None if question_id.startswith("q3") else {
                "id": f"q{int(question_id[1:]) + 1}",
                "text": "Have you experienced any shortness of breath?",
                "choices": ["Yes", "No", "Sometimes"],
            },
        }

    async def get_assessment(self, session_id: str) -> dict[str, Any]:
        return {
            "session_id": session_id,
            "triage_level": "low",
            "assessment": (
                "Based on your symptoms, your condition appears mild. "
                "If symptoms worsen, please seek medical attention."
            ),
            "recommended_actions": ["Rest", "Hydrate", "Monitor symptoms"],
            "confidence": 0.72,
        }
