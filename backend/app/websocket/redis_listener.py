"""Redis Pub/Sub listener bridging ``mirage:ws:*`` into WebSocket pushes."""

from __future__ import annotations

import asyncio
import json
import logging

from app.core.redis import get_redis
from app.websocket.connection_manager import manager

logger = logging.getLogger(__name__)


def _decode(value: bytes | str) -> str:
    return value.decode("utf-8") if isinstance(value, bytes) else str(value)


async def listen_for_websocket_events() -> None:
    """
    Background task subscribing to ``mirage:ws:*`` and forwarding messages
    to connected WebSocket clients via the ConnectionManager.
    """
    while True:
        try:
            redis = await get_redis()
            pubsub = redis.pubsub()
            await pubsub.psubscribe("mirage:ws:*")
            logger.info("WebSocket Redis listener started on pattern mirage:ws:*")

            async for message in pubsub.listen():
                if message["type"] != "pmessage":
                    continue

                channel_raw = message.get("channel")
                data_raw = message.get("data")
                if not channel_raw or not data_raw:
                    continue

                channel = _decode(channel_raw)
                data = _decode(data_raw)

                # Strip mirage:ws: prefix to derive the logical channel name
                ws_channel = channel.replace("mirage:ws:", "", 1)
                try:
                    payload = json.loads(data)
                except json.JSONDecodeError:
                    continue

                if ws_channel == "all":
                    await manager.broadcast(payload)
                else:
                    await manager.send_to_channel(ws_channel, payload)

        except asyncio.CancelledError:
            logger.info("WebSocket Redis listener cancelled.")
            raise
        except Exception as exc:
            logger.error("WebSocket Redis listener error: %s", exc)
            await asyncio.sleep(5)
