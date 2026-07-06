from __future__ import annotations

import asyncio

from redis.asyncio import Redis

from app.core.config import settings

_redis_instances: dict[int, Redis] = {}


async def get_redis() -> Redis:
    """Return the shared async Redis client (one instance per event loop)."""
    loop = asyncio.get_running_loop()
    loop_id = id(loop)
    if loop_id not in _redis_instances:
        _redis_instances[loop_id] = Redis.from_url(
            settings.redis_url,
            decode_responses=True,
        )
    return _redis_instances[loop_id]
