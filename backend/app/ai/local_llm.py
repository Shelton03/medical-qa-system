"""Async wrapper around the configured AI provider (gateway/ccaimex by default)."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from app.ai.factory import get_ai_provider
from app.ai.provider import AIContext, AIMessage

logger = logging.getLogger(__name__)


async def query_llm(
    prompt: str,
    max_tokens: int = 512,
    temperature: float = 0.3,
) -> str:
    """Run a prompt through the configured AI gateway and return generated text."""
    provider = get_ai_provider()
    message = AIMessage(
        role="user",
        content=prompt,
        timestamp=datetime.now(timezone.utc),
    )
    try:
        return await provider.generate_response([message], AIContext())
    except Exception as exc:
        logger.error("LLM query failed: %s", exc)
        return ""


def clean_json_response(text: str) -> str:
    """Remove ``json and `` markdown fences from *text*."""
    return text.replace("```json", "").replace("```", "").strip()
