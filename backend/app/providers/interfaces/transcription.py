"""TranscriptionProvider interface."""

from __future__ import annotations

import abc
from typing import Any, AsyncIterator

from app.providers.interfaces.base import BaseProvider


class TranscriptionProvider(BaseProvider, abc.ABC):
    """
    Interface for speech-to-text / transcription providers.

    Responsibilities:
    - Start a transcription session.
    - Accept audio chunks.
    - Return finalized transcript with speaker annotations.
    """

    @abc.abstractmethod
    async def start_session(self) -> str:
        """Start a transcription session and return its id."""

    @abc.abstractmethod
    async def send_audio(self, session_id: str, audio_chunk: bytes) -> None:
        """Stream an audio chunk to the provider."""

    @abc.abstractmethod
    async def stop_session(self, session_id: str) -> dict[str, Any]:
        """Stop the session and return the final transcript."""

    @abc.abstractmethod
    async def stream_transcript(self, session_id: str) -> AsyncIterator[dict[str, Any]]:
        """Yield partial transcript segments as they arrive."""
        yield {}  # noqa: PIE790
