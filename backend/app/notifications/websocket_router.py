"""WebSocket endpoint for real-time notification delivery."""

from __future__ import annotations

import asyncio
import json
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.auth.jwt import decode_token
from app.core.database import AsyncSessionLocal
from app.notifications.service import mark_read as mark_notification_read
from app.notifications.websocket_manager import manager

router = APIRouter()


@router.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    Authenticated WebSocket for real-time notifications.

    Query param: ?token=<JWT>
    Supported client actions: mark_read, heartbeat.
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
            if action == "heartbeat":
                await websocket.send_text(
                    json.dumps(
                        {
                            "type": "heartbeat_ack",
                            "payload": {},
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        }
                    )
                )
            elif action == "mark_read":
                notification_id_str = message.get("notification_id")
                if notification_id_str:
                    try:
                        notification_id = uuid.UUID(notification_id_str)
                        async with AsyncSessionLocal() as db:
                            await mark_notification_read(
                                db, notification_id, user_id
                            )
                            await db.commit()
                    except Exception:
                        pass
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        await manager.disconnect(user_id)
