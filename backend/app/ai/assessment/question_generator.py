#!/usr/bin/env python3
"""Question Generator — produces a single follow-up question based on assessment gaps."""

from __future__ import annotations

import logging
from dataclasses import asdict

from app.ai.local_llm import query_llm
from app.ai.provider import AIContext
from app.db.models import AISession

logger = logging.getLogger(__name__)

_QUESTION_PROMPT = """\
You are a compassionate medical intake assistant.

Current missing information:
{missing_info}

Risk flags:
{risk_flags}

Conversation history:
{history}

Generate ONE concise follow-up question to gather the most important missing information. Prioritize safety (address risk flags first if present). Return ONLY the question text with no extra commentary.
"""


class QuestionGenerator:
    """Create the next clarifying question for the patient."""

    async def generate(
        self,
        session: AISession,
        history: list[dict] | None = None,
        context: AIContext | None = None,
    ) -> str:
        """Return a single follow-up question string.

        Args:
            session: AISession with populated missing_info and risk_flags.
            history: Optional conversation history as list of {"role", "content"} dicts.
        """
        history_lines: list[str] = []
        for msg in history or []:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            history_lines.append(f"{role.capitalize()}: {content}")
        history_text = "\n".join(history_lines) if history_lines else "(none)"

        prompt = _QUESTION_PROMPT.format(
            missing_info="\n".join(f"- {m}" for m in session.missing_info) or "(none)",
            risk_flags="\n".join(f"- {r}" for r in session.risk_flags) or "(none)",
            history=history_text,
        )
        if context and context.clinical_profile:
            prompt += "\nApproved clinical context:\n" + str(asdict(context.clinical_profile))

        question = await query_llm(prompt, max_tokens=256, temperature=0.5)
        cleaned = question.strip().strip('"').strip("'")
        if not cleaned:
            logger.warning("QuestionGenerator: empty question from LLM; returning fallback.")
            return "Could you tell me more about your symptoms?"
        return cleaned
