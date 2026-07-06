"""FastAPI WebSocket endpoint at ``/ws``."""

from __future__ import annotations

import asyncio
import json
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.auth.jwt import decode_token
from app.websocket.connection_manager import manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    Authenticated WebSocket at ``/ws``.

    - Accepts JWT via query param ``?token=<JWT>``
    - Clients subscribe via ``{"action": "subscribe", "channels": ["patient:123"]}``
    - Heartbeat pong on ``{"action": "ping"}`` (or ``heartbeat``)
    """
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4001, reason="Missing authentication token.")
        return

    try:
        payload = decode_token(token)
    except Exception:
        await websocket.close(code=4001, reason="Invalid authentication token.")
        return

    user_id_str: str | None = payload.get("sub")
    if not user_id_str:
        await websocket.close(code=4001, reason="Invalid token payload.")
        return

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        await websocket.close(code=4001, reason="Malformed user identifier.")
        return

    await manager.connect(websocket, user_id)

    try:
        while True:
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(), timeout=30.0
                )
            except asyncio.TimeoutError:
                await websocket.send_text(
                    json.dumps(
                        {
                            "type": "heartbeat",
                            "payload": {},
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        }
                    )
                )
                continue

            try:
                message = json.loads(data)
            except json.JSONDecodeError:
                continue

            action = message.get("action")
            if action in ("heartbeat", "ping"):
                await websocket.send_text(
                    json.dumps(
                        {
                            "type": "pong",
                            "payload": {},
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        }
                    )
                )
            elif action == "subscribe":
                channels = message.get("channels", [])
                await manager.subscribe(user_id, channels)
                await websocket.send_text(
                    json.dumps(
                        {
                            "type": "subscribed",
                            "payload": {"channels": channels},
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        }
                    )
                )
            elif action == "unsubscribe":
                channels = message.get("channels", [])
                await manager.unsubscribe(user_id, channels)
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        await manager.disconnect(websocket)
