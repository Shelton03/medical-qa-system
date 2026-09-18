#!/usr/bin/env python3
"""Provider Factory — resolves concrete AIProvider instances by name."""

from __future__ import annotations

from app.ai.local_llm_provider import LocalAIProvider
from app.ai.mock_provider import MockAIProvider
from app.ai.provider import AIProvider
from app.core.config import settings

# Singleton cache for provider instances
_provider_instances: dict[str, AIProvider] = {}


class OpenAIProvider(AIProvider):
    """Placeholder for future OpenAI integration."""

    async def generate_response(self, conversation_history, context) -> str:
        raise NotImplementedError("OpenAIProvider is not yet implemented.")

    async def generate_stream(self, conversation_history, context):
        raise NotImplementedError("OpenAIProvider is not yet implemented.")
        yield ""  # noqa: PIE790

    async def analyze_medical_record(self, record, query) -> str:
        raise NotImplementedError("OpenAIProvider is not yet implemented.")


class AnthropicProvider(AIProvider):
    """Placeholder for future Anthropic integration."""

    async def generate_response(self, conversation_history, context) -> str:
        raise NotImplementedError("AnthropicProvider is not yet implemented.")

    async def generate_stream(self, conversation_history, context):
        raise NotImplementedError("AnthropicProvider is not yet implemented.")
        yield ""  # noqa: PIE790

    async def analyze_medical_record(self, record, query) -> str:
        raise NotImplementedError("AnthropicProvider is not yet implemented.")


def get_ai_provider(provider_name: str | None = None) -> AIProvider:
    """
    Resolve and return a singleton AIProvider instance by name.

    Defaults to the provider configured in ``settings.ai_provider``.
    Supported names: ``mock``, ``local``, ``openai``, ``anthropic``.
    """
    name = (provider_name or settings.ai_provider or "local").lower()

    if name in _provider_instances:
        return _provider_instances[name]

    if name == "mock":
        provider: AIProvider = MockAIProvider()
    elif name == "local":
        provider = LocalAIProvider()
    elif name == "openai":
        provider = OpenAIProvider()
    elif name == "anthropic":
        provider = AnthropicProvider()
    else:
        raise ValueError(f"Unsupported AI provider: {name}")

    _provider_instances[name] = provider
    return provider
