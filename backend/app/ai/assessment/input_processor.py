#!/usr/bin/env python3
"""Input Processor — extracts structured clinical data from free-text user input."""

from __future__ import annotations

import json
import logging

from app.ai.local_llm import clean_json_response, query_llm

logger = logging.getLogger(__name__)

_INPUT_EXTRACTION_PROMPT = """\
You are a medical intake assistant. Extract structured information from the patient's message below.

Patient message:
"{raw_text}"

Return ONLY valid JSON matching this schema:
{{
  "symptoms": ["list of reported symptoms"],
  "duration": "how long the symptoms have been present, or null",
  "severity": "mild|moderate|severe|unknown",
  "entities": ["other relevant medical entities (medications, conditions, etc.)"]
}}
"""


class InputProcessor:
    """Transform unstructured patient text into structured intake fields."""

    async def process(self, raw_text: str) -> dict:
        """Send *raw_text* to the LLM and return a parsed dict.

        On JSON failure or LLM error, returns a safe fallback with empty fields.
        """
        prompt = _INPUT_EXTRACTION_PROMPT.format(raw_text=raw_text)
        response = await query_llm(prompt, max_tokens=512, temperature=0.2)
        cleaned = clean_json_response(response)

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            logger.warning("InputProcessor: failed to decode JSON from LLM response.")
            return {
                "symptoms": [],
                "duration": None,
                "severity": None,
                "entities": [],
            }

        return {
            "symptoms": data.get("symptoms") or [],
            "duration": data.get("duration"),
            "severity": data.get("severity"),
            "entities": data.get("entities") or [],
        }
