"""LocalTranscriptionProvider — real-time STT via faster-whisper (tiny)."""

from __future__ import annotations

import asyncio
import logging
import os
import tempfile
import uuid
from typing import Any, AsyncIterator

from app.providers.interfaces.transcription import TranscriptionProvider

logger = logging.getLogger(__name__)


class LocalTranscriptionProvider(TranscriptionProvider):
    """Transcription provider backed by a local faster-whisper tiny model."""

    def __init__(self) -> None:
        self._model = None
        self._sessions: dict[str, bytearray] = {}

    # ------------------------------------------------------------------
    # Lazy model loading
    # ------------------------------------------------------------------
    def _load_model(self):
        if self._model is None:
            import faster_whisper

            logger.info("Loading faster-whisper tiny model …")
            self._model = faster_whisper.WhisperModel(
                "tiny",
                device="cpu",
                compute_type="int8",
                download_root="/app/models",
            )
        return self._model

    # ------------------------------------------------------------------
    # Synchronous transcription helper
    # ------------------------------------------------------------------
    def transcribe(self, audio_path_or_bytes: str | bytes, language: str = "en") -> str:
        """Transcribe an audio file path or raw bytes."""
        model = self._load_model()
        path: str
        tmp_path: str | None = None

        if isinstance(audio_path_or_bytes, bytes):
            fd, tmp_path = tempfile.mkstemp(suffix=".webm")
            try:
                with os.fdopen(fd, "wb") as f:
                    f.write(audio_path_or_bytes)
                path = tmp_path
            except Exception:
                if tmp_path:
                    try:
                        os.unlink(tmp_path)
                    except OSError:
                        pass
                raise
        else:
            path = audio_path_or_bytes

        try:
            segments, _info = model.transcribe(
                path,
                language=language,
                beam_size=5,
            )
            return " ".join(seg.text.strip() for seg in segments if seg.text.strip())
        finally:
            if tmp_path:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass

    # ------------------------------------------------------------------
    # Async interface implementation
    # ------------------------------------------------------------------
    async def initialize(self) -> None:
        """Pre-load model in a background thread."""
        await asyncio.to_thread(self._load_model)

    async def validate(self, **params: Any) -> bool:
        return True

    async def execute(self, **params: Any) -> dict[str, Any]:
        audio = params.get("audio")
        language = params.get("language", "en")
        if audio is None:
            return {"success": False, "error": "Missing audio parameter."}
        text = await asyncio.to_thread(self.transcribe, audio, language)
        return {"success": True, "text": text}

    async def start_session(self) -> str:
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = bytearray()
        return session_id

    async def send_audio(self, session_id: str, audio_chunk: bytes) -> None:
        buf = self._sessions.get(session_id)
        if buf is None:
            raise ValueError("Session not found.")
        buf.extend(audio_chunk)

    async def stop_session(self, session_id: str) -> dict[str, Any]:
        buf = self._sessions.pop(session_id, bytearray())
        text = await asyncio.to_thread(self.transcribe, bytes(buf))
        return {
            "session_id": session_id,
            "status": "completed",
            "text": text,
            "segments": [
                {
                    "speaker": "Unknown",
                    "text": text,
                    "timestamp": "",
                }
            ],
        }

    async def stream_transcript(self, session_id: str) -> AsyncIterator[dict[str, Any]]:
        buf = self._sessions.get(session_id)
        if not buf or len(buf) == 0:
            return
        text = await asyncio.to_thread(self.transcribe, bytes(buf))
        if text:
            yield {
                "speaker": "Unknown",
                "text": text,
                "timestamp": "",
            }
