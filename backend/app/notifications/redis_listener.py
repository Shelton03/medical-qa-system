"""Redis Pub/Sub listener that bridges Redis events into WebSocket pushes."""

from __future__ import annotations

import asyncio
import json
import logging
import uuid

from app.notifications.websocket_manager import manager
from app.core.redis import get_redis

logger = logging.getLogger(__name__)


async def listen_for_notifications() -> None:
    """
    Background task subscribing to Redis channels and pushing messages
    to connected WebSocket clients.

    Subscribes to pattern ``notifications:*`` so both broadcast
    (``notifications:all``) and personal (``notifications:user:{id}``)
    channels are handled by a single listener.
    """
    while True:
        try:
            redis = await get_redis()
            pubsub = redis.pubsub()
            await pubsub.psubscribe("notifications:*")
            logger.info("Redis Pub/Sub listener started on pattern notifications:*")

            async for message in pubsub.listen():
                if message["type"] != "pmessage":
                    continue

                channel_raw = message.get("channel")
                data_raw = message.get("data")
                if not channel_raw or not data_raw:
                    continue

                channel = (
                    channel_raw.decode("utf-8")
                    if isinstance(channel_raw, bytes)
                    else str(channel_raw)
                )
                data = (
                    data_raw.decode("utf-8")
                    if isinstance(data_raw, bytes)
                    else str(data_raw)
                )

                if channel == "notifications:all":
                    try:
                        payload = json.loads(data)
                    except json.JSONDecodeError:
                        continue
                    await manager.broadcast(payload)
                elif channel.startswith("notifications:user:"):
                    user_id_str = channel.split(":", 2)[2]
                    try:
                        user_id = uuid.UUID(user_id_str)
                    except ValueError:
                        continue
                    try:
                        payload = json.loads(data)
                    except json.JSONDecodeError:
                        continue
                    await manager.send_personal_message(user_id, payload)

        except asyncio.CancelledError:
            logger.info("Redis Pub/Sub listener cancelled.")
            raise
        except Exception as exc:
            logger.error("Redis Pub/Sub listener error: %s", exc)
            await asyncio.sleep(5)
