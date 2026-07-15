"""Local AI provider implementations using llama-cpp-python."""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from app.providers.interfaces.diagnosis import DiagnosisProvider
from app.providers.interfaces.summary import ClinicalSummaryProvider

logger = logging.getLogger(__name__)

_LLAMA_INSTANCE = None


def _get_llama() -> Any:
    """Lazy-load and return the shared Llama model instance."""
    global _LLAMA_INSTANCE
    if _LLAMA_INSTANCE is None:
        try:
            from llama_cpp import Llama
        except ImportError as exc:
            raise RuntimeError(
                "llama-cpp-python is not installed. "
                "Install it to use the local AI provider."
            ) from exc

        _LLAMA_INSTANCE = Llama(
            model_path="/app/models/gemma-3-4b-it-Q4_K_M.gguf",
            n_ctx=4096,
            verbose=False,
        )
    return _LLAMA_INSTANCE


class LocalDiagnosisProvider(DiagnosisProvider):
    """Local differential-diagnosis provider powered by Gemma 3 4B."""

    async def initialize(self) -> None:
        """Eagerly load the model into memory."""
        _get_llama()

    async def validate(self, **params: Any) -> bool:
        return True

    async def execute(self, **params: Any) -> dict[str, Any]:
        return params

    async def generate_differential(
        self,
        symptoms: list[str],
        patient_context: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        patient_context = patient_context or {}
        age = patient_context.get("age", "unknown")
        gender = patient_context.get("gender", "unknown")

        prompt = (
            "You are a clinical assistant. A patient presents with the following symptoms: "
            f"{', '.join(symptoms)}. "
            f"Demographics: {age}y/o {gender}. "
            "Provide a differential diagnosis with confidence scores.\n\n"
            "Output one diagnosis per line in this exact format:\n"
            "Condition: <condition name> | Confidence: <0.0-1.0> | Reasoning: <brief reasoning>\n\n"
            "Diagnoses:"
        )

        llm = _get_llama()
        result = llm(
            prompt,
            max_tokens=512,
            temperature=0.3,
            stop=["\n\n"],
        )
        raw_text = result["choices"][0]["text"].strip() if result.get("choices") else ""

        return _parse_diagnoses(raw_text)


class LocalSummaryProvider(ClinicalSummaryProvider):
    """Local clinical-summary provider powered by Gemma 3 4B."""

    async def initialize(self) -> None:
        """Eagerly load the model into memory."""
        _get_llama()

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
        symptoms_str = ", ".join(symptoms) if symptoms else "None provided"
        diagnoses_str = json.dumps(diagnoses, indent=2) if diagnoses else "None provided"

        prompt = (
            "You are a clinical assistant. Generate a concise SOAP note from the following data.\n\n"
            f"Transcript: {transcript or 'N/A'}\n"
            f"Symptoms: {symptoms_str}\n"
            f"Diagnoses: {diagnoses_str}\n\n"
            "Return the SOAP note in this exact format:\n"
            "Subjective: <text>\n"
            "Objective: <text>\n"
            "Assessment: <text>\n"
            "Plan: <text>\n\n"
            "SOAP Note:"
        )

        llm = _get_llama()
        result = llm(
            prompt,
            max_tokens=1024,
            temperature=0.2,
        )
        raw_text = result["choices"][0]["text"].strip() if result.get("choices") else ""

        return _parse_soap(raw_text, diagnoses=diagnoses, symptoms=symptoms)


def _parse_diagnoses(text: str) -> list[dict[str, Any]]:
    """Heuristic parser for diagnosis lines."""
    diagnoses: list[dict[str, Any]] = []

    # Try JSON array first
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            for item in parsed:
                if isinstance(item, dict):
                    diagnoses.append(
                        {
                            "name": str(
                                item.get("condition")
                                or item.get("name")
                                or "Unknown"
                            ),
                            "confidence": _clamp_confidence(
                                float(item.get("confidence", 0.5))
                            ),
                            "reasoning": str(item.get("reasoning", "")),
                            "recommended_investigations": [],
                            "medication_warnings": [],
                        }
                    )
            if diagnoses:
                return diagnoses
    except (json.JSONDecodeError, ValueError):
        pass

    # Fallback to regex heuristic
    pattern = re.compile(
        r"Condition:\s*(.+?)\s*\|\s*Confidence:\s*([\d.]+)\s*\|\s*Reasoning:\s*(.*)",
        re.IGNORECASE,
    )
    for line in text.splitlines():
        match = pattern.search(line)
        if match:
            condition, confidence_str, reasoning = match.groups()
            diagnoses.append(
                {
                    "name": condition.strip(),
                    "confidence": _clamp_confidence(float(confidence_str)),
                    "reasoning": reasoning.strip(),
                    "recommended_investigations": [],
                    "medication_warnings": [],
                }
            )

    if not diagnoses:
        # Last resort: treat whole text as a single diagnosis
        diagnoses.append(
            {
                "name": "Unspecified diagnosis",
                "confidence": 0.5,
                "reasoning": text,
                "recommended_investigations": [],
                "medication_warnings": [],
            }
        )

    return diagnoses


def _clamp_confidence(value: float) -> float:
    """Clamp a confidence value to [0.0, 1.0]."""
    try:
        value = float(value)
    except (ValueError, TypeError):
        value = 0.5
    return min(max(value, 0.0), 1.0)


def _parse_soap(
    text: str,
    diagnoses: list[dict[str, Any]] | None,
    symptoms: list[str] | None,
) -> dict[str, Any]:
    """Heuristic parser for SOAP note output."""
    sections: dict[str, str] = {
        "subjective": "",
        "objective": "",
        "assessment": "",
        "plan": "",
    }

    for key in sections:
        pattern = re.compile(
            rf"(?i){key}:\s*(.*?)(?=(?:Subjective|Objective|Assessment|Plan):|$)",
            re.DOTALL,
        )
        match = pattern.search(text)
        if match:
            sections[key] = match.group(1).strip()

    if not any(sections.values()):
        sections["subjective"] = text

    return {
        "soap": sections,
        "diagnoses": diagnoses or [],
        "symptoms": symptoms or [],
    }
