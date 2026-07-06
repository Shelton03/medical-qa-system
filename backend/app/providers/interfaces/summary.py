"""ClinicalSummaryProvider interface."""

from __future__ import annotations

import abc
from typing import Any

from app.providers.interfaces.base import BaseProvider


class ClinicalSummaryProvider(BaseProvider, abc.ABC):
    """
    Interface for clinical-note summarization providers.

    Responsibilities:
    - Generate a SOAP note from raw consultation data.
    """

    @abc.abstractmethod
    async def generate_soap_note(
        self,
        transcript: str | None = None,
        symptoms: list[str] | None = None,
        diagnoses: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Return a structured SOAP note."""
