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
You are a compassionate medical intake assistant chatting with a patient.

Current missing information:
{missing_info}

Risk flags:
{risk_flags}

Conversation history:
{history}

Your job is to generate ONE concise follow-up question to gather the most important missing information. Prioritize safety (address risk flags first if present).

Rules:
- Return ONLY the question text.
- Do NOT include any analysis, explanation, reasoning, lists, headings, or commentary.
- Do NOT say "Based on...", "The most important...", or "I need to ask...".
- The output must be a single question a patient can read and answer.
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
        cleaned = self._clean_question(question)
        if not cleaned:
            logger.warning("QuestionGenerator: empty question from LLM; returning fallback.")
            return "Could you tell me more about your symptoms?"
        return cleaned

    @staticmethod
    def _clean_question(text: str) -> str:
        """Strip reasoning leaks and formatting artifacts from a question."""
        text = text.strip()
        if not text:
            return ""

        # Remove markdown fences
        text = text.replace("```", "").strip()

        # Take only the first paragraph if multiple exist
        first_para = text.split("\n\n")[0].strip()

        # If the first paragraph has multiple lines, try to find the line that is a question
        lines = [line.strip() for line in first_para.splitlines() if line.strip()]
        if len(lines) > 1:
            # Prefer the line that ends with a question mark
            questions = [line for line in lines if line.endswith("?")]
            if questions:
                first_para = questions[0]
            else:
                first_para = lines[0]

        # Strip common reasoning prefixes
        lower = first_para.lower()
        prefixes = (
            "based on",
            "the most important",
            "the most critical",
            "the key safety",
            "i need to ask",
            "i should ask",
            "follow-up question:",
            "question:",
            "next question:",
            "recommended question:",
            "clinical reasoning",
            "reasoning:",
            "analysis:",
            "answer:",
            "note:",
        )
        for prefix in prefixes:
            if lower.startswith(prefix):
                # Remove up to first colon or first sentence
                if ":" in first_para:
                    first_para = first_para.split(":", 1)[1].strip()
                else:
                    # remove first sentence if short
                    first_para = first_para.split(".", 1)[-1].strip()
                break

        return first_para.strip('"').strip("'")
