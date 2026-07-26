"""Async wrapper around the local llama-cpp Gemma model."""

from __future__ import annotations

import asyncio
import logging
from typing import Optional

from app.providers.implementations.local_ai_provider import _get_llama

logger = logging.getLogger(__name__)

_LLM_SEMAPHORE = asyncio.Semaphore(1)


async def query_llm(
    prompt: str,
    max_tokens: int = 512,
    temperature: float = 0.3,
) -> str:
    """Run a prompt through the local Gemma model and return generated text.

    Calls are serialized via an asyncio semaphore because llama-cpp is not
    thread-safe. Markdown code fences are stripped from the output.
    """
    async with _LLM_SEMAPHORE:
        try:
            llm = _get_llama()
            result = await asyncio.to_thread(
                llm,
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["\n\n", "```"],
            )
            raw_text = result["choices"][0]["text"].strip()
            return clean_json_response(raw_text)
        except Exception as exc:
            logger.error("LLM query failed: %s", exc)
            return ""


def clean_json_response(text: str) -> str:
    """Remove ``json and `` markdown fences from *text*."""
    return text.replace("```json", "").replace("```", "").strip()
