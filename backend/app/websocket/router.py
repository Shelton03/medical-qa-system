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


async def _send_error(websocket: WebSocket, code: int, message: str) -> None:
    """Send a typed error message before closing."""
    await websocket.send_text(
        json.dumps(
            {
                "type": "error",
                "payload": {"code": code, "message": message},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )
    )


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    Authenticated WebSocket at ``/ws``.

    - Clients authenticate via ``{"action": "auth", "token": "<JWT>"}``
      within 5 seconds of connection establishment.
    - Clients subscribe via ``{"action": "subscribe", "channels": ["patient:123"]}``
    - Heartbeat pong on ``{"action": "ping"}`` (or ``heartbeat``)
    """
    await websocket.accept()

    user_id: uuid.UUID | None = None

    # Phase 1: Authentication handshake (5s timeout)
    try:
        auth_data = await asyncio.wait_for(websocket.receive_text(), timeout=5.0)
        try:
            message = json.loads(auth_data)
        except json.JSONDecodeError:
            await _send_error(websocket, 4001, "Malformed authentication message.")
            await websocket.close(code=4001, reason="Malformed authentication message.")
            return

        if message.get("action") != "auth":
            await _send_error(websocket, 4001, "Expected action=auth.")
            await websocket.close(code=4001, reason="Expected action=auth.")
            return

        token = message.get("token")
        if not token:
            await _send_error(websocket, 4001, "Missing authentication token.")
            await websocket.close(code=4001, reason="Missing authentication token.")
            return

        try:
            payload = decode_token(token)
        except Exception:
            await _send_error(websocket, 4001, "Invalid authentication token.")
            await websocket.close(code=4001, reason="Invalid authentication token.")
            return

        user_id_str: str | None = payload.get("sub")
        if not user_id_str:
            await _send_error(websocket, 4001, "Invalid token payload.")
            await websocket.close(code=4001, reason="Invalid token payload.")
            return

        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            await _send_error(websocket, 4001, "Malformed user identifier.")
            await websocket.close(code=4001, reason="Malformed user identifier.")
            return

        await manager.connect(websocket, user_id)
        await websocket.send_text(
            json.dumps(
                {
                    "type": "authenticated",
                    "payload": {"user_id": str(user_id)},
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            )
        )
    except asyncio.TimeoutError:
        await _send_error(websocket, 4001, "Authentication timed out.")
        await websocket.close(code=4001, reason="Authentication timed out.")
        return
    except WebSocketDisconnect:
        return

    # Phase 2: Normal operation
    try:
        while True:
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(), timeout=45.0
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
        if user_id is not None:
            await manager.disconnect(websocket)
