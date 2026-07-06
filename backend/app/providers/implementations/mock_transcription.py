"""MockTranscriptionProvider — returns mock transcript text."""

from __future__ import annotations

import uuid
from typing import Any, AsyncIterator

from app.providers.interfaces.transcription import TranscriptionProvider


class MockTranscriptionProvider(TranscriptionProvider):
    """Synthetic transcription provider for local development and testing."""

    async def initialize(self) -> None:
        """No-op initialization."""

    async def validate(self, **params: Any) -> bool:
        return True

    async def execute(self, **params: Any) -> dict[str, Any]:
        return params

    async def start_session(self) -> str:
        return str(uuid.uuid4())

    async def send_audio(self, session_id: str, audio_chunk: bytes) -> None:
        pass

    async def stop_session(self, session_id: str) -> dict[str, Any]:
        return {
            "session_id": session_id,
            "status": "completed",
            "segments": [
                {
                    "speaker": "Doctor",
                    "text": "Good morning. What brings you in today?",
                    "timestamp": "2026-07-06T09:00:00Z",
                },
                {
                    "speaker": "Patient",
                    "text": "I've had a cough and fever for three days.",
                    "timestamp": "2026-07-06T09:00:15Z",
                },
                {
                    "speaker": "Doctor",
                    "text": "Any difficulty breathing or chest pain?",
                    "timestamp": "2026-07-06T09:00:30Z",
                },
            ],
        }

    async def stream_transcript(self, session_id: str) -> AsyncIterator[dict[str, Any]]:
        segments = [
            {
                "speaker": "Doctor",
                "text": "Good morning. What brings you in today?",
                "timestamp": "2026-07-06T09:00:00Z",
            },
            {
                "speaker": "Patient",
                "text": "I've had a cough and fever for three days.",
                "timestamp": "2026-07-06T09:00:15Z",
            },
        ]
        for seg in segments:
            yield seg
