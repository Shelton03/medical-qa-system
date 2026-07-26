#!/usr/bin/env python3
"""Answer Generator — produces a final preliminary assessment response."""

from __future__ import annotations

import json
import logging
from dataclasses import asdict

from app.ai.local_llm import clean_json_response, query_llm
from app.ai.provider import AIContext
from app.db.models import AISession

logger = logging.getLogger(__name__)

_ANSWER_PROMPT = """\
You are a cautious medical information assistant. NEVER provide a definitive diagnosis. Always recommend seeing a qualified clinician.

Based on the following assessment, produce a preliminary summary.

Risk flags:
{risk_flags}

Confidence score: {confidence}

Conversation history:
{history}

Return ONLY valid JSON matching this schema:
{{
  "content": "preliminary assessment text for the patient",
  "explanation": "brief reasoning for the assessment",
  "disclaimer": "medical disclaimer",
  "confidence_level": "low|medium|high"
}}
"""

_FALLBACK_ANSWER = {
    "content": (
        "I'm not able to provide a definitive assessment based on the information provided. "
        "Your symptoms should be evaluated by a qualified healthcare professional."
    ),
    "explanation": "Insufficient information or LLM failure prevented a reliable assessment.",
    "disclaimer": (
        "This information is not medical advice. It does not replace a consultation with a "
        "licensed healthcare provider. If you are experiencing a medical emergency, call emergency services."
    ),
    "confidence_level": "low",
}


class AnswerGenerator:
    """Generate the final AI response once the DecisionEngine signals ANSWER."""

    async def generate(
        self,
        session: AISession,
        history: list[dict] | None = None,
        context: AIContext | None = None,
    ) -> dict:
        """Return a dict with ``content``, ``explanation``, ``disclaimer``, and ``confidence_level``.

        On JSON failure, returns a safe fallback with a strong medical disclaimer.
        """
        history_lines: list[str] = []
        for msg in history or []:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            history_lines.append(f"{role.capitalize()}: {content}")
        history_text = "\n".join(history_lines) if history_lines else "(none)"

        prompt = _ANSWER_PROMPT.format(
            risk_flags="\n".join(f"- {r}" for r in session.risk_flags) or "(none)",
            confidence=session.confidence,
            history=history_text,
        )
        if context and context.clinical_profile:
            prompt += "\nApproved clinical context:\n" + str(asdict(context.clinical_profile))

        response = await query_llm(prompt, max_tokens=768, temperature=0.3)
        cleaned = clean_json_response(response)

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            logger.warning("AnswerGenerator: failed to decode JSON from LLM response; returning fallback.")
            return _FALLBACK_ANSWER.copy()

        return {
            "content": data.get("content") or _FALLBACK_ANSWER["content"],
            "explanation": data.get("explanation") or _FALLBACK_ANSWER["explanation"],
            "disclaimer": data.get("disclaimer") or _FALLBACK_ANSWER["disclaimer"],
            "confidence_level": data.get("confidence_level") or _FALLBACK_ANSWER["confidence_level"],
        }
