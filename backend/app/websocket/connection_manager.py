"""WebSocket ConnectionManager with per-user channel subscriptions."""

from __future__ import annotations

import asyncio
import json
import uuid
from typing import Any

from fastapi import WebSocket

from starlette.websockets import WebSocketState


class ConnectionManager:
    """Singleton managing active WebSocket connections with channel subscriptions."""

    _instance: ConnectionManager | None = None

    def __new__(cls) -> ConnectionManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connections: dict[uuid.UUID, WebSocket] = {}
            cls._instance._user_channels: dict[uuid.UUID, set[str]] = {}
            cls._instance._lock = asyncio.Lock()
        return cls._instance

    async def connect(
        self,
        websocket: WebSocket,
        user_id: uuid.UUID,
        channels: list[str] | None = None,
    ) -> None:
        """Accept connection (if still pending) and optionally pre-subscribe."""
        if websocket.client_state == WebSocketState.CONNECTING:
            await websocket.accept()
        async with self._lock:
            existing = self._connections.get(user_id)
            if existing:
                try:
                    await existing.close()
                except Exception:
                    pass
            self._connections[user_id] = websocket
            self._user_channels[user_id] = set(channels or [])

    async def disconnect(self, websocket: WebSocket) -> None:
        """Remove a WebSocket from the active pool by object identity."""
        async with self._lock:
            for uid, ws in list(self._connections.items()):
                if ws is websocket:
                    self._connections.pop(uid, None)
                    self._user_channels.pop(uid, None)
                    break

    async def subscribe(self, user_id: uuid.UUID, channels: list[str]) -> None:
        """Add channels to a user's subscription set."""
        async with self._lock:
            self._user_channels.setdefault(user_id, set()).update(channels)

    async def unsubscribe(self, user_id: uuid.UUID, channels: list[str]) -> None:
        """Remove channels from a user's subscription set."""
        async with self._lock:
            user_chs = self._user_channels.get(user_id, set())
            for ch in channels:
                user_chs.discard(ch)
            self._user_channels[user_id] = user_chs

    async def send_to_user(self, user_id: uuid.UUID, message: dict[str, Any]) -> None:
        """Send a JSON message to a specific user if they are online."""
        async with self._lock:
            websocket = self._connections.get(user_id)
        if websocket:
            try:
                await websocket.send_text(json.dumps(message))
            except Exception:
                pass

    async def send_to_channel(self, channel: str, message: dict[str, Any]) -> None:
        """Send a JSON message to every user subscribed to *channel*."""
        async with self._lock:
            targets = [
                uid
                for uid, channels in self._user_channels.items()
                if channel in channels
            ]
            connections = [self._connections.get(uid) for uid in targets]
        for websocket in connections:
            if websocket:
                try:
                    await websocket.send_text(json.dumps(message))
                except Exception:
                    continue

    async def broadcast(self, message: dict[str, Any]) -> None:
        """Send a JSON message to every connected client."""
        async with self._lock:
            connections = list(self._connections.values())
        for websocket in connections:
            try:
                await websocket.send_text(json.dumps(message))
            except Exception:
                continue


manager = ConnectionManager()
