"""SymptomCheckerProvider interface."""

from __future__ import annotations

import abc
from typing import Any

from app.providers.interfaces.base import BaseProvider


class SymptomCheckerProvider(BaseProvider, abc.ABC):
    """
    Interface for symptom-checking providers.

    Responsibilities:
    - Begin questionnaire sessions.
    - Receive patient answers and return next questions.
    - Return a structured assessment result.
    """

    @abc.abstractmethod
    async def begin_session(self, patient_id: str, context: dict[str, Any] | None = None) -> str:
        """Start a new symptom-checker session and return the session id."""

    @abc.abstractmethod
    async def submit_answer(self, session_id: str, question_id: str, answer: Any) -> dict[str, Any]:
        """Submit a patient answer and receive the next question or result."""

    @abc.abstractmethod
    async def get_assessment(self, session_id: str) -> dict[str, Any]:
        """Return the final structured assessment for a completed session."""
