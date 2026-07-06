"""WebSocket ConnectionManager singleton."""

from __future__ import annotations

import asyncio
import json
import uuid
from typing import Any

from fastapi import WebSocket


class ConnectionManager:
    """Singleton managing active WebSocket connections with async safety."""

    _instance: ConnectionManager | None = None
    _lock: asyncio.Lock

    def __new__(cls) -> ConnectionManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connections: dict[uuid.UUID, WebSocket] = {}
            cls._instance._lock = asyncio.Lock()
        return cls._instance

    async def connect(self, websocket: WebSocket, user_id: uuid.UUID) -> None:
        """Accept connection and store mapping user_id -> websocket."""
        await websocket.accept()
        async with self._lock:
            existing = self._connections.get(user_id)
            if existing:
                try:
                    await existing.close()
                except Exception:
                    pass
            self._connections[user_id] = websocket

    async def disconnect(self, user_id: uuid.UUID) -> None:
        """Remove a user's connection from the active pool."""
        async with self._lock:
            self._connections.pop(user_id, None)

    async def send_personal_message(
        self, user_id: uuid.UUID, message: dict[str, Any]
    ) -> None:
        """Send JSON to a specific user's WebSocket if they are online."""
        async with self._lock:
            websocket = self._connections.get(user_id)
        if websocket:
            try:
                await websocket.send_text(json.dumps(message))
            except Exception:
                pass

    async def broadcast(self, message: dict[str, Any]) -> None:
        """Send JSON to every connected client."""
        async with self._lock:
            connections = list(self._connections.values())
        for websocket in connections:
            try:
                await websocket.send_text(json.dumps(message))
            except Exception:
                continue


manager = ConnectionManager()
