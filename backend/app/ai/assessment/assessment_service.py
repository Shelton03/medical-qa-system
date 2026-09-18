#!/usr/bin/env python3
"""Assessment Service — performs initial AI triage and persists results to an AISession."""

from __future__ import annotations

import json
import logging
from dataclasses import asdict

from app.ai.local_llm import clean_json_response, query_llm
from app.ai.provider import AIContext
from app.db.models import AISession

logger = logging.getLogger(__name__)

_TRIAGE_PROMPT = """\
You are a clinical triage assistant. Based on the patient intake below, produce an initial assessment.

Symptoms: {symptoms}
Duration: {duration}
Severity: {severity}
Entities: {entities}

Return ONLY valid JSON matching this schema:
{{
  "candidate_domains": ["possible medical domains, e.g. Cardiology, Respiratory"],
  "key_symptoms": ["normalized symptom list"],
  "missing_info": ["specific follow-up questions or missing data points"],
  "risk_flags": ["any red flags or urgent concerns"]
}}
"""

_FOLLOW_UP_PROMPT = """\
You are a clinical triage assistant updating an assessment after the patient's latest answer.

Current assessment:
{current_assessment}

Approved clinical context:
{clinical_context}

Latest patient answer:
{latest_input}

Return ONLY valid JSON matching this schema:
{{
  "candidate_domains": ["possible medical domains"],
  "key_symptoms": ["normalized symptom list"],
  "missing_info": ["only information still needed after this answer"],
  "risk_flags": ["any red flags or urgent concerns"]
}}
"""


class AssessmentService:
    """Run initial triage via LLM and update the provided *AISession* in place.

    The caller is responsible for committing the SQLAlchemy session.
    """

    async def assess(
        self,
        session: AISession,
        structured_input: dict | None = None,
        context: AIContext | None = None,
    ) -> None:
        """Populate *session* assessment fields from an LLM triage prompt.

        Args:
            session: The ORM AISession instance to update.
            structured_input: Optional pre-computed structured data from InputProcessor.
        """
        symptoms = (structured_input or {}).get("symptoms", [])
        duration = (structured_input or {}).get("duration")
        severity = (structured_input or {}).get("severity")
        entities = (structured_input or {}).get("entities", [])

        prompt = _TRIAGE_PROMPT.format(
            symptoms=json.dumps(symptoms),
            duration=duration or "unknown",
            severity=severity or "unknown",
            entities=json.dumps(entities),
        )

        if context and context.clinical_profile:
            prompt += "\nApproved clinical context:\n" + json.dumps(asdict(context.clinical_profile), default=str)
        data = await self._parse_assessment(prompt)

        self._apply(session, data)

    async def reassess(
        self,
        session: AISession,
        structured_input: dict,
        context: AIContext | None = None,
    ) -> None:
        """Update outstanding information gaps after a follow-up answer."""
        profile = asdict(context.clinical_profile) if context and context.clinical_profile else {}
        prompt = _FOLLOW_UP_PROMPT.format(
            current_assessment=json.dumps({
                "candidate_domains": session.candidate_domains,
                "key_symptoms": session.key_symptoms,
                "missing_info": session.missing_info,
                "risk_flags": session.risk_flags,
            }),
            clinical_context=json.dumps(profile, default=str),
            latest_input=json.dumps(structured_input),
        )
        self._apply(session, await self._parse_assessment(prompt))

    async def _parse_assessment(self, prompt: str) -> dict:
        """Run an assessment prompt and return a safely parsed response."""
        response = await query_llm(prompt, max_tokens=512, temperature=0.3)
        cleaned = clean_json_response(response)

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            logger.warning("AssessmentService: failed to decode JSON from LLM response.")
            data = {}

        return data

    def _apply(self, session: AISession, data: dict) -> None:
        """Persist a normalized assessment result on the session."""
        session.candidate_domains = data.get("candidate_domains") or []
        session.key_symptoms = data.get("key_symptoms") or []
        session.missing_info = data.get("missing_info") or []
        session.risk_flags = data.get("risk_flags") or []
        session.assessment_done = True
        session.gaps_remaining = len(session.missing_info)
