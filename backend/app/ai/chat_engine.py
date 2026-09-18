#!/usr/bin/env python3
"""Chat Engine — orchestrates AI sessions, message persistence, and provider interaction."""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import date, datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.context_builder import enrich_context_with_patient_data
from app.ai.provider import AIContext, AIMessage, AIProvider
from app.core.config import settings
from app.db.models import AISession as AISessionModel, AIMessage as AIMessageModel, Appointment, ConsentRequest
from app.websocket.events import WSEventType
from app.websocket.publisher import emit_ws_event


class ChatEngine:
    """
    Manages AI sessions and coordinates between the database and AI providers.

    Responsibilities:
    - Create and persist AI sessions.
    - Append messages to conversation history.
    - Build clinical context (including consent-gated available_data).
    - Generate responses via the abstract AIProvider interface.
    """

    async def create_session(
        self,
        db: AsyncSession,
        doctor_id: UUID | None = None,
        patient_id: UUID | None = None,
        initiated_by: str | None = None,
        appointment_id: UUID | None = None,
    ) -> AISessionModel:
        """Create a new AI session row and return it."""
        metadata: dict = {}
        if initiated_by:
            metadata["initiated_by"] = initiated_by

        # Auto-link to patient's upcoming CONFIRMED appointment if not provided
        if appointment_id is None and patient_id is not None:
            result = await db.execute(
                select(Appointment.id, Appointment.doctor_id)
                .where(
                    Appointment.patient_id == patient_id,
                    Appointment.status == "CONFIRMED",
                    Appointment.appointment_date >= date.today(),
                )
                .order_by(Appointment.appointment_date.asc())
                .limit(1)
            )
            upcoming = result.one_or_none()
            if upcoming:
                appointment_id, appointment_doctor_id = upcoming
                if doctor_id is None:
                    doctor_id = appointment_doctor_id

        if appointment_id:
            metadata["appointment_id"] = str(appointment_id)

        session = AISessionModel(
            doctor_id=doctor_id,
            patient_id=patient_id,
            status="ACTIVE",
            appointment_id=appointment_id,
            provider_name=settings.ai_provider or "local",
            provider_metadata=metadata if metadata else None,
        )
        db.add(session)
        await db.flush()
        await db.refresh(session)
        return session

    async def add_message(
        self,
        db: AsyncSession,
        session_id: UUID,
        role: str,
        content: str,
        metadata: dict | None = None,
        message_type: str | None = None,
        response_metadata: dict | None = None,
    ) -> AIMessageModel:
        """Save a message to the ai_messages table."""
        message = AIMessageModel(
            session_id=session_id,
            role=role.upper(),
            content=content,
            message_type=message_type,
            response_metadata=response_metadata,
        )
        db.add(message)
        await db.flush()
        await db.refresh(message)
        return message

    async def get_conversation_history(
        self,
        db: AsyncSession,
        session_id: UUID,
    ) -> list[AIMessage]:
        """Load all messages for a session, ordered by creation time."""
        result = await db.execute(
            select(AIMessageModel)
            .where(AIMessageModel.session_id == session_id)
            .order_by(AIMessageModel.created_at.asc())
        )
        rows = result.scalars().all()
        return [
            AIMessage(
                role=row.role.lower(),
                content=row.content,
                timestamp=row.created_at,
                metadata=None,
            )
            for row in rows
        ]

    async def _check_consent(
        self,
        db: AsyncSession,
        doctor_id: UUID,
        patient_id: UUID | None,
    ) -> list[str]:
        """
        Return the list of data scopes the doctor has consent to access.

        If no patient is associated, or no active/valid consent exists,
        returns an empty list.
        """
        if patient_id is None:
            return []

        result = await db.execute(
            select(ConsentRequest)
            .where(
                ConsentRequest.doctor_id == doctor_id,
                ConsentRequest.patient_id == patient_id,
                ConsentRequest.status == "approved",
            )
            .order_by(ConsentRequest.approved_at.desc())
        )
        consent = result.scalar_one_or_none()
        if consent is None:
            return []

        if consent.expires_at and consent.expires_at < datetime.now(timezone.utc):
            return []

        return consent.scope or []

    async def _build_context(
        self,
        db: AsyncSession,
        session: AISessionModel,
    ) -> AIContext:
        available_data = await self._check_consent(
            db, session.doctor_id, session.patient_id
        )
        context = AIContext(
            patient_id=session.patient_id,
            doctor_id=session.doctor_id,
            session_id=session.id,
            available_data=available_data,
        )
        return await enrich_context_with_patient_data(db, context)

    async def generate_ai_response(
        self,
        db: AsyncSession,
        session_id: UUID,
        user_message: str,
        provider: AIProvider,
    ) -> str:
        """
        Full non-streaming flow:
        add user message → build context → generate response → save assistant message.
        """
        await self.add_message(db, session_id, "user", user_message)

        result = await db.execute(
            select(AISessionModel).where(AISessionModel.id == session_id)
        )
        session = result.scalar_one()

        context = await self._build_context(db, session)
        history = await self.get_conversation_history(db, session_id)
        assistant_text = await provider.generate_response(history, context)

        await self.add_message(db, session_id, "assistant", assistant_text)

        # Emit real-time AI response event to the appropriate channel
        # Patient-initiated sessions → emit to patient channel
        # Doctor-initiated sessions → emit to doctor channel
        channel = f"patient:{session.patient_id}" if session.doctor_id is None else f"doctor:{session.doctor_id}"
        await emit_ws_event(
            channel,
            WSEventType.AI_RESPONSE_READY,
            {
                "session_id": str(session_id),
                "patient_id": str(session.patient_id) if session.patient_id else None,
                "response_preview": assistant_text[:200],
            },
        )
        return assistant_text

    async def generate_ai_stream(
        self,
        db: AsyncSession,
        session_id: UUID,
        user_message: str,
        provider: AIProvider,
    ) -> AsyncIterator[str]:
        """
        Full streaming flow:
        add user message → build context → yield chunks → save assistant message.
        """
        await self.add_message(db, session_id, "user", user_message)

        result = await db.execute(
            select(AISessionModel).where(AISessionModel.id == session_id)
        )
        session = result.scalar_one()

        context = await self._build_context(db, session)
        history = await self.get_conversation_history(db, session_id)

        full_chunks: list[str] = []
        async for chunk in provider.generate_stream(history, context):
            full_chunks.append(chunk)
            yield chunk

        assistant_text = "".join(full_chunks)
        await self.add_message(db, session_id, "assistant", assistant_text)

        # Emit real-time AI response event to the appropriate channel
        channel = f"patient:{session.patient_id}" if session.doctor_id is None else f"doctor:{session.doctor_id}"
        await emit_ws_event(
            channel,
            WSEventType.AI_RESPONSE_READY,
            {
                "session_id": str(session_id),
                "patient_id": str(session.patient_id) if session.patient_id else None,
                "response_preview": assistant_text[:200],
            },
        )

    async def generate_assessment_response(
        self,
        db: AsyncSession,
        session_id: UUID,
        user_message: str,
    ) -> dict:
        """Run the full 5-service assessment pipeline and return structured response."""

        # 1. Save user message
        await self.add_message(db, session_id, "user", user_message)

        # Load session ORM model (not just IDs)
        result = await db.execute(select(AISessionModel).where(AISessionModel.id == session_id))
        session = result.scalar_one()

        # 2. Build context (with patient data enrichment)
        context = await self._build_context(db, session)

        # 3. Process input
        from app.ai.assessment import InputProcessor, AssessmentService, DecisionEngine, QuestionGenerator, AnswerGenerator

        input_processor = InputProcessor()
        assessment_service = AssessmentService()
        decision_engine = DecisionEngine()
        question_gen = QuestionGenerator()
        answer_gen = AnswerGenerator()

        processed = await input_processor.process(user_message)

        # 4. Build or update the assessment from the latest patient response.
        if not session.assessment_done:
            await assessment_service.assess(session, processed, context)
        else:
            await assessment_service.reassess(session, processed, context)
        await db.flush()

        # 5. Build history
        history = await self.get_conversation_history(db, session_id)
        history_dicts = [{"role": m.role.lower(), "content": m.content} for m in history]

        # 6. Decision engine
        decision = await decision_engine.decide(session, turn_count=len(history))
        await db.flush()

        response_data = {}
        assistant_content = ""
        msg_type = ""

        if decision == "ASK":
            # Generate follow-up question
            question = await question_gen.generate(session, history_dicts, context)
            assistant_content = question
            msg_type = "question"
            response_data = {
                "type": "question",
                "content": question,
            }
        else:
            # Generate final answer
            answer = await answer_gen.generate(session, history_dicts, context)
            assistant_content = answer["content"]
            msg_type = "answer"
            response_data = {
                "type": "answer",
                **answer,
            }

        # 7. Save assistant message
        response_metadata = {
            key: value
            for key, value in response_data.items()
            if key not in {"content", "type"}
        } or None
        assistant_message = await self.add_message(
            db,
            session_id,
            "assistant",
            assistant_content,
            message_type=msg_type,
            response_metadata=response_metadata,
        )
        await db.flush()

        # 8. Update session
        await db.refresh(session)

        # Emit real-time AI response event to the appropriate channel
        channel = f"patient:{session.patient_id}" if session.doctor_id is None else f"doctor:{session.doctor_id}"
        await emit_ws_event(
            channel,
            WSEventType.AI_RESPONSE_READY,
            {
                "session_id": str(session_id),
                "patient_id": str(session.patient_id) if session.patient_id else None,
                "response_preview": assistant_content[:200],
            },
        )

        response_data["message"] = assistant_message
        return response_data
