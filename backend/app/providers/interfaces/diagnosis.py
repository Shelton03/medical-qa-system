"""DiagnosisProvider interface."""

from __future__ import annotations

import abc
from typing import Any

from app.providers.interfaces.base import BaseProvider


class DiagnosisProvider(BaseProvider, abc.ABC):
    """
    Interface for AI-assisted differential-diagnosis providers.

    Responsibilities:
    - Accept structured patient context + symptoms.
    - Return a ranked list of differential diagnoses with confidence.
    """

    @abc.abstractmethod
    async def generate_differential(
        self,
        symptoms: list[str],
        patient_context: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Return a ranked list of diagnoses with metadata."""
