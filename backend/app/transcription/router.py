#!/usr/bin/env python3
"""Mirage Transcription API router (mock implementation)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, UploadFile, File
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, get_current_doctor
from app.core.database import get_db
from app.db.models import User
from app.schemas.envelope import Envelope
from app.shared.exceptions import NotFoundException

router = APIRouter()


# ---------------------------------------------------------------------------
# In-memory mock storage
# ---------------------------------------------------------------------------
_transcription_sessions: dict[uuid.UUID, dict] = {}


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class TranscriptionStartResponse(BaseModel):
    model_config = ConfigDict(strict=True)
    session_id: uuid.UUID
    status: str


class TranscriptionSegment(BaseModel):
    model_config = ConfigDict(strict=True)
    speaker: str
    text: str
    timestamp: str


class TranscriptionStatusResponse(BaseModel):
    model_config = ConfigDict(strict=True)
    session_id: uuid.UUID
    status: str
    text: str
    segments: list[TranscriptionSegment]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _get_session(session_id: uuid.UUID) -> dict:
    session = _transcription_sessions.get(session_id)
    if not session:
        raise NotFoundException("Transcription session not found.", error_code="NOT_FOUND")
    return session


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@router.post(
    "/start",
    response_model=Envelope[TranscriptionStartResponse],
    summary="Start a new transcription session",
)
async def start_transcription(
    current_user: User = Depends(get_current_doctor),
) -> Envelope[TranscriptionStartResponse]:
    session_id = uuid.uuid4()
    _transcription_sessions[session_id] = {
        "id": session_id,
        "status": "ACTIVE",
        "text": "",
        "segments": [],
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    return Envelope.ok(
        TranscriptionStartResponse(session_id=session_id, status="ACTIVE")
    )


@router.post(
    "/{session_id}/audio",
    response_model=Envelope[dict],
    summary="Upload audio chunk",
)
async def upload_audio(
    session_id: uuid.UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[dict]:
    session = _get_session(session_id)
    if session["status"] != "ACTIVE":
        return Envelope.ok({"message": "Session is not active.", "received": False})

    # Mock: pretend we transcribed something from the chunk
    mock_text = f"[Chunk received: {file.filename or 'unnamed'}]"
    session["text"] += " " + mock_text if session["text"] else mock_text
    session["segments"].append(
        {
            "speaker": "Doctor",
            "text": mock_text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )
    session["updated_at"] = datetime.now(timezone.utc)
    return Envelope.ok({"message": "Audio chunk received.", "received": True})


@router.get(
    "/{session_id}",
    response_model=Envelope[TranscriptionStatusResponse],
    summary="Get transcription status and text",
)
async def get_transcription(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_doctor),
) -> Envelope[TranscriptionStatusResponse]:
    session = _get_session(session_id)
    return Envelope.ok(
        TranscriptionStatusResponse(
            session_id=session["id"],
            status=session["status"],
            text=session["text"],
            segments=[
                TranscriptionSegment(
                    speaker=s["speaker"],
                    text=s["text"],
                    timestamp=s["timestamp"],
                )
                for s in session["segments"]
            ],
        )
    )


@router.post(
    "/{session_id}/stop",
    response_model=Envelope[TranscriptionStatusResponse],
    summary="Stop and finalize transcription",
)
async def stop_transcription(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_doctor),
) -> Envelope[TranscriptionStatusResponse]:
    session = _get_session(session_id)
    session["status"] = "COMPLETED"
    session["updated_at"] = datetime.now(timezone.utc)
    # Add a finalization segment
    session["segments"].append(
        {
            "speaker": "System",
            "text": "Transcription finalized.",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )
    return Envelope.ok(
        TranscriptionStatusResponse(
            session_id=session["id"],
            status=session["status"],
            text=session["text"],
            segments=[
                TranscriptionSegment(
                    speaker=s["speaker"],
                    text=s["text"],
                    timestamp=s["timestamp"],
                )
                for s in session["segments"]
            ],
        )
    )
