#!/usr/bin/env python3
"""Decision Engine — self-consistency loop that decides ASK or ANSWER."""

from __future__ import annotations

import asyncio
import json
import logging

from app.ai.local_llm import clean_json_response, query_llm
from app.core.config import settings
from app.db.models import AISession

logger = logging.getLogger(__name__)

_DECISION_PROMPT = """\
You are a clinical decision assistant.

Given the current assessment state, decide whether to:
- ASK another clarifying question
- ANSWER with a preliminary assessment

Assessment state:
- Candidate domains: {candidate_domains}
- Key symptoms: {key_symptoms}
- Missing information: {missing_info}
- Risk flags: {risk_flags}
- Conversation turns so far: {turn_count}

Return ONLY valid JSON matching this schema:
{{
  "decision": "ASK|ANSWER",
  "confidence": 0.0 to 1.0,
  "rationale": "brief reasoning"
}}
"""


class DecisionEngine:
    """Run multiple LLM decision calls in parallel and aggregate via voting.

    Override rules:
        - If average confidence < threshold → force ASK.
        - If gaps_remaining > 0 → force ASK.
    """

    def __init__(self) -> None:
        self._runs: int = settings.self_consistency_runs
        self._threshold: float = settings.confidence_threshold

    async def decide(self, session: AISession, turn_count: int = 0) -> str:
        """Return ``"ASK"`` or ``"ANSWER"`` and update *session.confidence*.

        Args:
            session: Current AISession with populated assessment fields.
            turn_count: Number of back-and-forth turns already completed.

        Returns:
            ``"ASK"`` or ``"ANSWER"``.
        """
        prompt = _DECISION_PROMPT.format(
            candidate_domains=session.candidate_domains,
            key_symptoms=session.key_symptoms,
            missing_info=session.missing_info,
            risk_flags=session.risk_flags,
            turn_count=turn_count,
        )

        coros = [query_llm(prompt, max_tokens=256, temperature=0.4) for _ in range(self._runs)]
        responses = await asyncio.gather(*coros)

        votes: dict[str, int] = {"ASK": 0, "ANSWER": 0}
        confidences: list[float] = []

        for raw in responses:
            cleaned = clean_json_response(raw)
            try:
                data = json.loads(cleaned)
            except json.JSONDecodeError:
                logger.warning("DecisionEngine: failed to parse decision JSON; counting as ASK.")
                votes["ASK"] += 1
                continue

            decision = (data.get("decision") or "ASK").upper()
            if decision not in votes:
                decision = "ASK"
            votes[decision] += 1

            try:
                confidences.append(float(data.get("confidence", 0.0)))
            except (TypeError, ValueError):
                confidences.append(0.0)

        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        winning = "ANSWER" if votes["ANSWER"] > votes["ASK"] else "ASK"

        # Override rules
        if avg_confidence < self._threshold:
            winning = "ASK"
        if session.gaps_remaining > 0:
            winning = "ASK"

        session.confidence = round(avg_confidence, 4)
        logger.info(
            "DecisionEngine: votes=%s avg_conf=%.2f → %s",
            votes,
            avg_confidence,
            winning,
        )
        return winning
