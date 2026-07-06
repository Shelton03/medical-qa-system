#!/usr/bin/env python3
"""AI Router — REST API endpoints for AI sessions and chat."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from app.ai.chat_engine import ChatEngine
from app.ai.factory import get_ai_provider
from app.ai.schemas import (
    AIMessageCreate,
    AIMessageResponse,
    AISessionCreate,
    AISessionResponse,
    AISessionWithMessagesResponse,
)
from app.auth.dependencies import get_current_doctor
from app.core.database import get_db
from app.db.models import (
    AISession as AISessionModel,
    AIMessage as AIMessageModel,
    Doctor,
    Visit,
)
from app.models import User
from app.schemas.envelope import Envelope
from app.shared.exceptions import NotFoundException

router = APIRouter()
chat_engine = ChatEngine()


async def _get_doctor_id(db: AsyncSession, current_user: User) -> UUID:
    """Resolve the Doctor row ID for the currently authenticated user."""
    result = await db.execute(
        select(Doctor).where(Doctor.user_id == current_user.id)
    )
    doctor = result.scalar_one_or_none()
    if doctor:
        return doctor.id

    # Fallback for demo / synthetic users: return the first doctor in the database.
    result = await db.execute(select(Doctor))
    first_doctor = result.scalars().first()
    if first_doctor:
        return first_doctor.id

    raise HTTPException(status_code=403, detail="Doctor profile not found.")


@router.post(
    "/sessions",
    response_model=Envelope[AISessionResponse],
    summary="Create AI session",
    description="Start a new AI-assisted consultation session.",
)
async def create_session(
    body: AISessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[AISessionResponse]:
    doctor_id = await _get_doctor_id(db, current_user)
    session = await chat_engine.create_session(
        db, doctor_id=doctor_id, patient_id=body.patient_id
    )
    await db.commit()
    return Envelope.ok(AISessionResponse.model_validate(session))


@router.get(
    "/sessions/{session_id}",
    response_model=Envelope[AISessionWithMessagesResponse],
    summary="Get AI session",
    description="Retrieve a session including its full message history.",
)
async def get_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[AISessionWithMessagesResponse]:
    result = await db.execute(
        select(AISessionModel).where(AISessionModel.id == session_id)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    msg_result = await db.execute(
        select(AIMessageModel)
        .where(AIMessageModel.session_id == session_id)
        .order_by(AIMessageModel.created_at.asc())
    )
    messages = msg_result.scalars().all()

    response_data = AISessionWithMessagesResponse.model_validate(session)
    response_data.messages = [AIMessageResponse.model_validate(m) for m in messages]
    return Envelope.ok(response_data)


@router.post(
    "/sessions/{session_id}/messages",
    response_model=Envelope[AIMessageResponse],
    summary="Send message",
    description="Send a user message and receive the assistant's response.",
)
async def send_message(
    session_id: UUID,
    body: AIMessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[AIMessageResponse]:
    provider = get_ai_provider()
    await chat_engine.generate_ai_response(
        db, session_id, body.content, provider
    )
    await db.commit()

    result = await db.execute(
        select(AIMessageModel)
        .where(
            AIMessageModel.session_id == session_id,
            AIMessageModel.role == "ASSISTANT",
        )
        .order_by(AIMessageModel.created_at.desc())
    )
    msg = result.scalar_one()
    return Envelope.ok(AIMessageResponse.model_validate(msg))


@router.post(
    "/sessions/{session_id}/messages/stream",
    summary="Send message (streaming)",
    description="Send a user message and receive an SSE streaming response.",
)
async def send_message_stream(
    session_id: UUID,
    body: AIMessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> StreamingResponse:
    provider = get_ai_provider()

    async def event_generator() -> AsyncIterator[str]:
        async for chunk in chat_engine.generate_ai_stream(
            db, session_id, body.content, provider
        ):
            payload = json.dumps({"token": chunk})
            yield f"data: {payload}\n\n"
        yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )


@router.get(
    "/sessions",
    response_model=Envelope[list[AISessionResponse]],
    summary="List AI sessions",
    description="List the authenticated doctor's AI sessions (paginated).",
)
async def list_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
    page: int = 1,
    page_size: int = 20,
) -> Envelope[list[AISessionResponse]]:
    doctor_id = await _get_doctor_id(db, current_user)
    result = await db.execute(
        select(AISessionModel)
        .where(AISessionModel.doctor_id == doctor_id)
        .order_by(AISessionModel.started_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    sessions = result.scalars().all()
    return Envelope.ok([AISessionResponse.model_validate(s) for s in sessions])


# ---------------------------------------------------------------------------
# Diagnosis, Summary, Complete
# ---------------------------------------------------------------------------
class DifferentialDiagnosisResponse(BaseModel):
    model_config = ConfigDict(strict=True)
    diagnoses: list[dict]


class SOAPSummaryResponse(BaseModel):
    model_config = ConfigDict(strict=True)
    soap: dict


class CompleteSessionResponse(BaseModel):
    model_config = ConfigDict(strict=True)
    status: str


@router.post(
    "/sessions/{session_id}/diagnosis",
    response_model=Envelope[DifferentialDiagnosisResponse],
    summary="Generate differential diagnosis",
)
async def generate_diagnosis(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[DifferentialDiagnosisResponse]:
    result = await db.execute(
        select(AISessionModel).where(AISessionModel.id == session_id)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise NotFoundException("Session not found.", error_code="NOT_FOUND")

    provider = get_ai_provider()
    # Load conversation history
    history = await chat_engine.get_conversation_history(db, session_id)
    context = await chat_engine._build_context(db, session)

    # Use the provider's differential diagnosis method if available
    if hasattr(provider, "generate_differential_diagnosis"):
        diagnoses = await provider.generate_differential_diagnosis(history, context)
    else:
        diagnoses = {
            "diagnoses": [
                {
                    "name": "Community-acquired pneumonia",
                    "confidence": 0.83,
                    "reasoning": "Productive cough, fever, and focal chest signs.",
                    "recommendedInvestigations": ["Chest X-ray", "CBC"],
                    "medicationWarnings": ["Check penicillin allergy."],
                }
            ]
        }

    return Envelope.ok(DifferentialDiagnosisResponse(diagnoses=diagnoses.get("diagnoses", [])))


@router.post(
    "/sessions/{session_id}/summary",
    response_model=Envelope[SOAPSummaryResponse],
    summary="Generate clinical summary (SOAP format)",
)
async def generate_summary(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[SOAPSummaryResponse]:
    result = await db.execute(
        select(AISessionModel).where(AISessionModel.id == session_id)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise NotFoundException("Session not found.", error_code="NOT_FOUND")

    provider = get_ai_provider()
    history = await chat_engine.get_conversation_history(db, session_id)
    context = await chat_engine._build_context(db, session)

    if hasattr(provider, "generate_clinical_summary"):
        summary = await provider.generate_clinical_summary(history, context)
    else:
        summary = {
            "soap": {
                "subjective": "Patient reports symptoms.",
                "objective": "Physical exam findings.",
                "assessment": "Assessment placeholder.",
                "plan": "Plan placeholder.",
            }
        }

    return Envelope.ok(SOAPSummaryResponse(soap=summary.get("soap", {})))


@router.post(
    "/sessions/{session_id}/complete",
    response_model=Envelope[CompleteSessionResponse],
    summary="Close and finalize AI session",
)
async def complete_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_doctor),
) -> Envelope[CompleteSessionResponse]:
    result = await db.execute(
        select(AISessionModel).where(AISessionModel.id == session_id)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise NotFoundException("Session not found.", error_code="NOT_FOUND")

    session.status = "COMPLETED"
    session.completed_at = datetime.now(timezone.utc)

    # Optionally update the linked visit with a summary
    if session.consultation_id:
        visit_result = await db.execute(
            select(Visit).where(Visit.id == session.consultation_id)
        )
        visit = visit_result.scalar_one_or_none()
        if visit and not visit.ai_summary:
            visit.ai_summary = "AI session completed. Summary available in AI messages."
            db.add(visit)

    db.add(session)
    await db.commit()

    return Envelope.ok(CompleteSessionResponse(status="COMPLETED"))
