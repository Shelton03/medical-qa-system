"""WebSocket endpoint for real-time local transcription."""

from __future__ import annotations

import asyncio
import json
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.auth.jwt import decode_token
from app.providers.implementations.local_transcription_provider import (
    LocalTranscriptionProvider,
)

router = APIRouter()

_provider = LocalTranscriptionProvider()

# Buffer heuristics for ~1 second of webm/opus from MediaRecorder(start(100))
_MAX_CHUNKS_BEFORE_FLUSH = 10
_MIN_BYTES_BEFORE_FLUSH = 16384  # 16 KB

_SENTENCE_END = frozenset({".", "?", "!"})


class _SessionState:
    def __init__(self, language: str = "en") -> None:
        self.buffer = bytearray()
        self.language = language
        self.final_text = ""
        self.chunk_count = 0
        self.lock = asyncio.Lock()


def _looks_final(text: str) -> bool:
    stripped = text.rstrip()
    return bool(stripped) and stripped[-1] in _SENTENCE_END


async def _transcribe_buffer(state: _SessionState) -> str:
    if not state.buffer:
        return ""
    audio = bytes(state.buffer)
    state.buffer.clear()
    state.chunk_count = 0
    return await asyncio.to_thread(_provider.transcribe, audio, state.language)


@router.websocket("/ws/transcription")
async def transcription_websocket(websocket: WebSocket) -> None:
    """
    Real-time transcription WebSocket at ``/ws/transcription``.

    Query param:
      ?token=<JWT>

    Binary audio chunks (webm/opus) are accepted.  Interim / final
    transcripts are streamed back as JSON.
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
        uuid.UUID(user_id_str)
    except ValueError:
        await websocket.close(code=4001, reason="Malformed user identifier.")
        return

    await websocket.accept()

    # Ensure the model is loaded so the first flush isn't slow.
    await _provider.initialize()

    state = _SessionState()

    try:
        while True:
            data = await websocket.receive()

            # Text messages are control commands (stop / ping).
            if "text" in data:
                try:
                    message = json.loads(data["text"])
                except json.JSONDecodeError:
                    continue

                action = message.get("action")
                if action == "stop":
                    async with state.lock:
                        text = await _transcribe_buffer(state)
                        if text:
                            state.final_text += (
                                " " + text if state.final_text else text
                            )
                    await websocket.send_json(
                        {
                            "text": state.final_text.strip(),
                            "is_final": True,
                        }
                    )
                    await websocket.close(code=1000, reason="Stopped by client.")
                    return
                elif action == "ping":
                    await websocket.send_json(
                        {
                            "type": "pong",
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        }
                    )
                continue

            chunk = data.get("bytes")
            if not chunk:
                continue

            async with state.lock:
                state.buffer.extend(chunk)
                state.chunk_count += 1

                should_flush = (
                    state.chunk_count >= _MAX_CHUNKS_BEFORE_FLUSH
                    or len(state.buffer) >= _MIN_BYTES_BEFORE_FLUSH
                )

                if should_flush:
                    text = await _transcribe_buffer(state)
                else:
                    continue

            if text:
                if _looks_final(text):
                    state.final_text += (
                        " " + text if state.final_text else text
                    )
                    await websocket.send_json(
                        {"text": text.strip(), "is_final": True}
                    )
                else:
                    await websocket.send_json(
                        {"text": text.strip(), "is_final": False}
                    )

    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        # Drain any leftover audio and send a final envelope.
        async with state.lock:
            if state.buffer:
                try:
                    text = await _transcribe_buffer(state)
                    if text:
                        state.final_text += (
                            " " + text if state.final_text else text
                        )
                except Exception:
                    pass

        if state.final_text:
            try:
                await websocket.send_json(
                    {"text": state.final_text.strip(), "is_final": True}
                )
            except Exception:
                pass

        try:
            await websocket.close()
        except Exception:
            pass
