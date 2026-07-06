"""Tests for WebSocket infrastructure."""

from __future__ import annotations

import asyncio
import json
import uuid
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import WebSocketDisconnect

from app.auth.jwt import create_access_token
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
        self.closed = False
        self.close_code: int | None = None
        self.close_reason: str | None = None
        self._text_queue: asyncio.Queue[str] = asyncio.Queue()
        self.client_state = 1  # CONNECTING = 1 (WebSocketState.CONNECTING)

    async def accept(self, subprotocol: str | None = None) -> None:
        self.client_state = 2  # CONNECTED = 2

    async def send_text(self, data: str) -> None:
        self.sent.append(data)

    async def close(self, code: int = 1000, reason: str | None = None) -> None:
        self.closed = True
        self.close_code = code
        self.close_reason = reason
        self.client_state = 3  # DISCONNECTED = 3

    async def receive_text(self) -> str:
        return await self._text_queue.get()

    def queue(self, msg: str) -> None:
        self._text_queue.put_nowait(msg)


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


# ------------------------------------------------------------------
# Auth-via-message flow tests (added for B+C+D+E fix)
# ------------------------------------------------------------------

@pytest.mark.anyio
async def test_ws_requires_auth_message(mock_ws):
    """Connecting without sending auth message should time out and close."""
    from app.websocket.router import websocket_endpoint
    # No auth message queued -> receive_text blocks; asyncio.TimeoutError in 5s
    await websocket_endpoint(mock_ws)

    assert mock_ws.closed is True
    assert mock_ws.close_code == 4001
    errors = [s for s in mock_ws.sent if json.loads(s).get("type") == "error"]
    assert len(errors) == 1
    assert json.loads(errors[0])["payload"]["code"] == 4001


@pytest.mark.anyio
async def test_ws_accepts_auth_message():
    """Connection with valid auth message sends authenticated event."""
    from app.websocket.router import websocket_endpoint

    ws = FakeWebSocket()
    user_id = uuid.uuid4()
    token = create_access_token(user_id, "doctor")

    call_count = 0

    async def _recv() -> str:
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return json.dumps({"action": "auth", "token": token})
        raise WebSocketDisconnect()

    ws.receive_text = _recv

    with patch("app.websocket.router.manager") as mock_manager:
        mock_manager.connect = AsyncMock()
        mock_manager.disconnect = AsyncMock()

        await websocket_endpoint(ws)

        mock_manager.connect.assert_awaited_once()
        authed = [s for s in ws.sent if json.loads(s).get("type") == "authenticated"]
        assert len(authed) == 1


@pytest.mark.anyio
async def test_ws_rejects_bad_auth_message():
    """Connection with malformed auth should receive error and close."""
    from app.websocket.router import websocket_endpoint

    ws = FakeWebSocket()
    ws.queue("not-json")

    await websocket_endpoint(ws)

    assert ws.closed is True
    assert ws.close_code == 4001


@pytest.mark.anyio
async def test_ws_rejects_invalid_token():
    """Connection with an invalid token should receive error and close."""
    from app.websocket.router import websocket_endpoint

    ws = FakeWebSocket()
    ws.queue(json.dumps({"action": "auth", "token": "bad-token"}))

    await websocket_endpoint(ws)

    assert ws.closed is True
    assert ws.close_code == 4001
    errors = [s for s in ws.sent if json.loads(s).get("type") == "error"]
    assert len(errors) == 1


@pytest.mark.anyio
async def test_ws_heartbeat_ping_pong():
    """Server should reply with pong on heartbeat/ping action."""
    from app.websocket.router import websocket_endpoint

    ws = FakeWebSocket()
    user_id = uuid.uuid4()
    token = create_access_token(user_id, "doctor")

    call_count = 0
    messages = [
        json.dumps({"action": "auth", "token": token}),
        json.dumps({"action": "ping"}),
        json.dumps({"action": "heartbeat"}),
    ]

    async def _recv() -> str:
        nonlocal call_count
        msg = messages[call_count]
        call_count += 1
        return msg

    ws.receive_text = _recv

    with patch("app.websocket.router.manager") as mock_manager:
        mock_manager.connect = AsyncMock()
        mock_manager.disconnect = AsyncMock()
        mock_manager.subscribe = AsyncMock()

        try:
            await websocket_endpoint(ws)
        except IndexError:
            pass

        pongs = [s for s in ws.sent if json.loads(s).get("type") == "pong"]
        assert len(pongs) == 2
