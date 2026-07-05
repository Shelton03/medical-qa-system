#!/usr/bin/env python3
"""Async Redis client singleton."""

from __future__ import annotations

from redis.asyncio import Redis

from app.shared.settings import settings

_redis_client: Redis | None = None


async def get_redis() -> Redis:
    """Return the shared async Redis client, creating it if necessary."""
    global _redis_client
    if _redis_client is None:
        _redis_client = Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )
    return _redis_client
