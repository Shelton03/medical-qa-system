"""Tests for WebSocket infrastructure."""

from __future__ import annotations

import asyncio
import json
import uuid
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import WebSocket

from app.websocket.connection_manager import ConnectionManager
from app.websocket.events import WSEventType


@pytest.fixture
def manager():
    """Provide a fresh ConnectionManager instance for each test."""
    instance = object.__new__(ConnectionManager)
    instance._connections = {}
    instance._user_channels = {}
    instance._lock = asyncio.Lock()
    return instance


class FakeWebSocket:
    def __init__(self):
        self.sent: list[str] = []

    async def accept(self, subprotocol: str | None = None) -> None:
        pass

    async def send_text(self, data: str) -> None:
        self.sent.append(data)

    async def close(self, code: int = 1000, reason: str | None = None) -> None:
        pass


@pytest.fixture
def mock_ws():
    return FakeWebSocket()


@pytest.mark.anyio
async def test_connect_stores_socket(manager, mock_ws):
    user_id = uuid.uuid4()
    await manager.connect(mock_ws, user_id)


@pytest.mark.anyio
async def test_send_to_user_delivers_message(manager, mock_ws):
    user_id = uuid.uuid4()
    await manager.connect(mock_ws, user_id)
    message = {"type": "TEST", "payload": {}}
    await manager.send_to_user(user_id, message)
    assert len(mock_ws.sent) == 1
    sent = json.loads(mock_ws.sent[0])
    assert sent["type"] == "TEST"
    assert sent["type"] == "TEST"


@pytest.mark.anyio
async def test_disconnect_removes_socket(manager, mock_ws):
    user_id = uuid.uuid4()
    await manager.connect(mock_ws, user_id)
    await manager.disconnect(mock_ws)
    # After disconnect, send should not reach the socket
    await manager.send_to_user(user_id, {"type": "TEST"})
    assert len(mock_ws.sent) == 0


@pytest.mark.anyio
async def test_subscribe_and_send_to_channel(manager, mock_ws):
    user_id = uuid.uuid4()
    await manager.connect(mock_ws, user_id, channels=["patient:123"])
    message = {"type": "EVENT", "payload": {}}
    await manager.send_to_channel("patient:123", message)
    assert len(mock_ws.sent) == 1
    sent = json.loads(mock_ws.sent[0])
    assert sent["type"] == "EVENT"


@pytest.mark.anyio
async def test_broadcast_delivers_to_all(manager):
    ws1 = FakeWebSocket()
    ws2 = FakeWebSocket()

    await manager.connect(ws1, uuid.uuid4())
    await manager.connect(ws2, uuid.uuid4())

    await manager.broadcast({"type": "BROADCAST", "payload": {}})
    assert len(ws1.sent) == 1
    assert len(ws2.sent) == 1


@pytest.mark.anyio
async def test_emit_ws_event_publishes_to_redis():
    with patch("app.websocket.publisher.get_redis") as mock_get_redis:
        mock_redis = AsyncMock()
        mock_get_redis.return_value = mock_redis

        from app.websocket.publisher import emit_ws_event

        await emit_ws_event("patient:123", WSEventType.CONSENT_REQUESTED, {"id": "abc"})

        mock_get_redis.assert_awaited_once()
        mock_redis.publish.assert_awaited_once()
        channel = mock_redis.publish.await_args[0][0]
        payload = json.loads(mock_redis.publish.await_args[0][1])
        assert channel == "mirage:ws:patient:123"
        assert payload["type"] == "CONSENT_REQUESTED"
