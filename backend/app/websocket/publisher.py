"""WebSocket event publisher using Redis Pub/Sub."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from app.core.redis import get_redis
from app.websocket.events import WSEventType


async def emit_ws_event(channel: str, event_type: WSEventType, payload: dict) -> None:
    """Publish a WebSocket event to the Redis channel ``mirage:ws:{channel}``."""
    redis = await get_redis()
    message = {
        "type": event_type.value,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }
    await redis.publish(f"mirage:ws:{channel}", json.dumps(message))
