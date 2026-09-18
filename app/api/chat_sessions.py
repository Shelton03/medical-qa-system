from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user, get_db_session_dep
from app.db.repositories import SessionRepository, MessageRepository, AttachmentRepository
from app.db.storage import StorageClient
from app.core.config import settings
from app.models.domain import Session as ChatSession, Message as ChatMessage

router = APIRouter()

class ChatSessionListResponse(BaseModel):
    id: str
    session_id: str
    first_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class ChatSessionMessagesResponse(BaseModel):
    session_id: str
    messages: List[ChatMessage]

class CreateChatSessionResponse(BaseModel):
    session_id: str
    created_at: datetime

async def convert_session_to_response(session: ChatSession, msg_repo: MessageRepository) -> ChatSessionListResponse:
    first_msg = await msg_repo.get_first_user_message(session.session_id)
    return ChatSessionListResponse(
        id=session.session_id,
        session_id=session.session_id,
        first_message=first_msg or session.first_message,
        created_at=session.created_at,
        updated_at=session.updated_at
    )

@router.get("", response_model=List[ChatSessionListResponse])
async def list_chat_sessions(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session_dep),
):
    repo = SessionRepository(db)
    msg_repo = MessageRepository(db)

    sessions = await repo.get_user_sessions(current_user["user_id"])

    return [await convert_session_to_response(s, msg_repo) for s in sessions]

@router.post("", response_model=CreateChatSessionResponse)
async def create_chat_session(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session_dep),
):
    repo = SessionRepository(db)

    session = ChatSession(user_id=current_user["user_id"])
    await repo.create_session(session)
    await db.commit()

    return CreateChatSessionResponse(
        session_id=session.session_id,
        created_at=session.created_at
    )

@router.get("/{session_id}", response_model=ChatSessionMessagesResponse)
async def get_chat_session_messages(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session_dep),
):
    repo = SessionRepository(db)
    msg_repo = MessageRepository(db)

    session = await repo.get_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.user_id != current_user["user_id"]:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = await msg_repo.get_session_history(session_id)
    return ChatSessionMessagesResponse(session_id=session_id, messages=messages)

@router.delete("/{session_id}")
async def delete_chat_session(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session_dep),
):
    repo = SessionRepository(db)
    msg_repo = MessageRepository(db)
    attachment_repo = AttachmentRepository(db)
    storage = StorageClient(settings)

    session = await repo.get_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.user_id != current_user["user_id"]:
        raise HTTPException(status_code=404, detail="Session not found")

    # Delete MinIO objects + metadata linked to this chat session.
    await attachment_repo.delete_by_session_id(session_id, storage=storage)
    await msg_repo.delete_session_messages(session_id)
    await repo.delete_session(session_id)
    await db.commit()

    return {"success": True, "message": "Session deleted"}
