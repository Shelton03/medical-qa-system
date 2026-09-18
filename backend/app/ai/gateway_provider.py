"""Gateway AI Provider — routes all chat/completion calls through ccaimex."""

from __future__ import annotations

import json
import logging
from collections.abc import AsyncIterator
from typing import Any

import httpx

from app.ai.provider import AIContext, AIMessage, AIProvider
from app.core.config import settings
from app.shared.schemas import MedicalRecordResponse

logger = logging.getLogger(__name__)

_CLINICAL_SYSTEM_PROMPT = """\
You are a cautious clinical intake assistant. Your role is to gather information, ask focused follow-up questions, and provide educational information. You do not diagnose or prescribe. Always encourage the patient to seek care from a licensed physician for any urgent or serious concerns.
"""


class GatewayAIProvider(AIProvider):
    """OpenAI-compatible gateway provider for chat, streaming, and record analysis."""

    def __init__(self) -> None:
        self._http: httpx.AsyncClient | None = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._http is None:
            if not settings.llm_gateway_url:
                raise RuntimeError("LLM_GATEWAY_URL is not configured")
            headers = {"Content-Type": "application/json"}
            if settings.llm_gateway_api_key:
                headers["Authorization"] = f"Bearer {settings.llm_gateway_api_key}"
            self._http = httpx.AsyncClient(
                base_url=settings.llm_gateway_url.rstrip("/"),
                headers=headers,
                timeout=60.0,
            )
        return self._http

    def _build_messages(
        self,
        conversation_history: list[AIMessage],
        context: AIContext | None = None,
    ) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = [
            {"role": "system", "content": _CLINICAL_SYSTEM_PROMPT}
        ]
        if context and context.clinical_profile:
            profile = context.clinical_profile
            ctx_parts: list[str] = []
            if profile.demographics:
                ctx_parts.append(f"Demographics: {profile.demographics}")
            if profile.allergies:
                ctx_parts.append(f"Allergies: {json.dumps(profile.allergies, default=str)}")
            if profile.chronic_conditions:
                ctx_parts.append(f"Conditions: {json.dumps(profile.chronic_conditions, default=str)}")
            if profile.current_medications:
                ctx_parts.append(f"Medications: {json.dumps(profile.current_medications, default=str)}")
            if ctx_parts:
                messages.append(
                    {"role": "system", "content": "Patient context:\n" + "\n".join(ctx_parts)}
                )
        for msg in conversation_history:
            role = msg.role.lower()
            if role not in {"system", "user", "assistant"}:
                role = "user"
            messages.append({"role": role, "content": msg.content})
        return messages

    async def generate_response(
        self,
        conversation_history: list[AIMessage],
        context: AIContext,
    ) -> str:
        messages = self._build_messages(conversation_history, context)
        payload = {
            "model": settings.llm_model,
            "messages": messages,
            "max_tokens": 512,
            "temperature": 0.3,
        }
        try:
            resp = await self._get_client().post("/v1/chat/completions", json=payload)
            resp.raise_for_status()
            data = resp.json()
            choice = data.get("choices", [{}])[0]
            content = choice.get("message", {}).get("content", "")
            return content.strip()
        except Exception as exc:
            logger.error("Gateway chat completion failed: %s", exc)
            return ""

    async def generate_stream(
        self,
        conversation_history: list[AIMessage],
        context: AIContext,
    ) -> AsyncIterator[str]:
        messages = self._build_messages(conversation_history, context)
        payload = {
            "model": settings.llm_model,
            "messages": messages,
            "max_tokens": 512,
            "temperature": 0.3,
            "stream": True,
        }
        try:
            async with self._get_client().stream("POST", "/v1/chat/completions", json=payload) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    line = line.strip()
                    if not line or line.startswith(":"):
                        continue
                    if line.startswith("data: "):
                        line = line[len("data: "):]
                    if line == "[DONE]":
                        break
                    try:
                        chunk = json.loads(line)
                        delta = chunk.get("choices", [{}])[0].get("delta", {})
                        text = delta.get("content", "")
                        if text:
                            yield text
                    except json.JSONDecodeError:
                        continue
        except Exception as exc:
            logger.error("Gateway streaming completion failed: %s", exc)

    async def analyze_medical_record(
        self,
        record: MedicalRecordResponse,
        query: str,
    ) -> str:
        prompt = (
            "You are a clinical documentation assistant. Analyze the following medical record "
            f"and answer this query: {query}\n\n"
            f"Record: {record.model_dump_json()}"
        )
        messages = [
            {"role": "system", "content": _CLINICAL_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
        payload = {
            "model": settings.llm_model,
            "messages": messages,
            "max_tokens": 1024,
            "temperature": 0.2,
        }
        try:
            resp = await self._get_client().post("/v1/chat/completions", json=payload)
            resp.raise_for_status()
            data = resp.json()
            choice = data.get("choices", [{}])[0]
            content = choice.get("message", {}).get("content", "")
            return content.strip()
        except Exception as exc:
            logger.error("Gateway record analysis failed: %s", exc)
            return ""
