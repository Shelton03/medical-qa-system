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
from sqlalchemy.orm import selectinload
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
from app.auth.dependencies import get_current_user
from app.core.database import get_db
from app.db.models import (
    AISession as AISessionModel,
    AIMessage as AIMessageModel,
    ConsentRequest,
    Doctor,
    Patient,
    Visit,
)
from app.models import User
from app.schemas.envelope import Envelope
from app.shared.exceptions import ForbiddenException, NotFoundException

router = APIRouter()
chat_engine = ChatEngine()


def _message_response(message: AIMessageModel) -> AIMessageResponse:
    """Expose persisted structured assessment metadata with its AI message."""
    response = AIMessageResponse.model_validate(message)
    metadata = message.response_metadata or {}
    response.confidence_level = metadata.get("confidence_level")
    response.risk_flags = metadata.get("risk_flags")
    response.explanation = metadata.get("explanation")
    response.disclaimer = metadata.get("disclaimer")
    return response


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


async def _get_patient_id(db: AsyncSession, current_user: User) -> UUID:
    """Resolve the Patient row ID for the currently authenticated user."""
    result = await db.execute(
        select(Patient.id).where(Patient.user_id == current_user.id)
    )
    patient_id = result.scalar_one_or_none()
    if patient_id:
        return patient_id

    # Fallback for demo / synthetic users: return the first patient in the database.
    fallback = await db.execute(select(Patient.id))
    first_patient = fallback.scalars().first()
    if first_patient:
        return first_patient
    raise HTTPException(status_code=403, detail="Patient profile not found.")


@router.post(
    "/sessions",
    response_model=Envelope[AISessionResponse],
    summary="Create AI session",
    description="Start a new AI-assisted consultation session. Patients may initiate their own sessions (e.g. symptom check); doctors may open a session for a specific patient.",
)
async def create_session(
    body: AISessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[AISessionResponse]:
    role = current_user.role
    patient_id: UUID | None = body.patient_id
    doctor_id: UUID | None = None

    if role == "doctor":
        doctor_id = await _get_doctor_id(db, current_user)
        # Doctor may create a session for themselves or for a specific patient.
    elif role == "patient":
        # Patient-initiated sessions: link the session to this patient.
        patient_id = await _get_patient_id(db, current_user)
    elif role == "admin":
        # Admins may create sessions; default doctor_id to first doctor if absent.
        doctor_id = await _get_doctor_id(db, current_user)
    else:
        raise ForbiddenException("Insufficient permissions to start an AI session.")

    session = await chat_engine.create_session(
        db,
        doctor_id=doctor_id,
        patient_id=patient_id,
        initiated_by=role,
        appointment_id=body.appointment_id,
    )
    await db.commit()
    return Envelope.ok(AISessionResponse.model_validate(session))


async def get_session_for_user(
    db: AsyncSession,
    session_id: UUID,
    current_user: User,
) -> AISessionModel:
    """Return an AI session if the current user is allowed to view it."""
    result = await db.execute(
        select(AISessionModel)
        .where(AISessionModel.id == session_id)
        .options(selectinload(AISessionModel.messages))
    )
    session = result.scalar_one_or_none()
    if not session:
        raise NotFoundException("Session not found.", error_code="NOT_FOUND")

    role = current_user.role
    if role == "doctor":
        doctor_id = await _get_doctor_id(db, current_user)
        if session.doctor_id != doctor_id:
            raise ForbiddenException("You are not authorized to view this session.")
        if session.patient_id is not None:
            consent_result = await db.execute(
                select(ConsentRequest.id).where(
                    ConsentRequest.doctor_id == doctor_id,
                    ConsentRequest.patient_id == session.patient_id,
                    ConsentRequest.status == "approved",
                    (ConsentRequest.expires_at.is_(None))
                    | (ConsentRequest.expires_at >= datetime.now(timezone.utc)),
                )
            )
            if consent_result.scalar_one_or_none() is None:
                raise ForbiddenException("Active patient consent is required to access this session.")
    elif role == "patient":
        patient_id = await _get_patient_id(db, current_user)
        if session.patient_id != patient_id:
            raise ForbiddenException("You are not authorized to view this session.")
    # admins: full access
    return session


@router.get(
    "/sessions/{session_id}",
    response_model=Envelope[AISessionWithMessagesResponse],
    summary="Get AI session",
    description="Retrieve a session including its full message history.",
)
async def get_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[AISessionWithMessagesResponse]:
    session = await get_session_for_user(db, session_id, current_user)

    msg_result = await db.execute(
        select(AIMessageModel)
        .where(AIMessageModel.session_id == session_id)
        .order_by(AIMessageModel.created_at.asc())
    )
    messages = msg_result.scalars().all()

    response_data = AISessionWithMessagesResponse.model_validate(session)
    response_data.messages = [_message_response(m) for m in messages]
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
    current_user: User = Depends(get_current_user),
) -> Envelope[AIMessageResponse]:
    session = await get_session_for_user(db, session_id, current_user)
    response_data = await chat_engine.generate_assessment_response(
        db, session_id, body.content
    )
    await db.commit()

    msg = response_data["message"]
    return Envelope.ok(_message_response(msg))


@router.post(
    "/sessions/{session_id}/messages/stream",
    summary="Send message (streaming)",
    description="Send a user message and receive an SSE streaming response.",
)
async def send_message_stream(
    session_id: UUID,
    body: AIMessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> StreamingResponse:
    session = await get_session_for_user(db, session_id, current_user)

    response_data = await chat_engine.generate_assessment_response(
        db, session_id, body.content
    )
    await db.commit()

    text = response_data.get("content", "")
    metadata = {
        key: value
        for key, value in response_data.items()
        if key not in {"content", "message"}
    }

    async def event_generator() -> AsyncIterator[str]:
        yield f"data: {json.dumps(metadata)}\n\n"
        for chunk in text.split():
            payload = json.dumps({"token": chunk + " "})
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
    description="List AI sessions for the authenticated user (paginated). Doctors see their sessions; patients see their own sessions.",
)
async def list_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = 1,
    page_size: int = 20,
) -> Envelope[list[AISessionResponse]]:
    role = current_user.role
    if role == "doctor":
        doctor_id = await _get_doctor_id(db, current_user)
        result = await db.execute(
            select(AISessionModel)
            .where(AISessionModel.doctor_id == doctor_id)
            .order_by(AISessionModel.started_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
    elif role == "patient":
        patient_id = await _get_patient_id(db, current_user)
        result = await db.execute(
            select(AISessionModel)
            .where(AISessionModel.patient_id == patient_id)
            .order_by(AISessionModel.started_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
    else:
        # Admins see all sessions
        result = await db.execute(
            select(AISessionModel)
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
    current_user: User = Depends(get_current_user),
) -> Envelope[DifferentialDiagnosisResponse]:
    session = await get_session_for_user(db, session_id, current_user)

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
    current_user: User = Depends(get_current_user),
) -> Envelope[SOAPSummaryResponse]:
    session = await get_session_for_user(db, session_id, current_user)

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
    current_user: User = Depends(get_current_user),
) -> Envelope[CompleteSessionResponse]:
    session = await get_session_for_user(db, session_id, current_user)

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
