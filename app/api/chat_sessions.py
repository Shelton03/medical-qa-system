from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.api.deps import get_current_user, get_orchestrator
from app.db.repositories import SessionRepository, MessageRepository
from app.db.mongodb import get_database
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
async def list_chat_sessions(current_user: dict = Depends(get_current_user)):
    db = get_database()
    repo = SessionRepository(db)
    msg_repo = MessageRepository(db)
    
    sessions = await repo.get_user_sessions(current_user["user_id"])
    
    return [await convert_session_to_response(s, msg_repo) for s in sessions]

@router.post("", response_model=CreateChatSessionResponse)
async def create_chat_session(current_user: dict = Depends(get_current_user)):
    db = get_database()
    repo = SessionRepository(db)
    
    session = ChatSession(user_id=current_user["user_id"])
    await repo.create_session(session)
    
    return CreateChatSessionResponse(
        session_id=session.session_id,
        created_at=session.created_at
    )

@router.get("/{session_id}", response_model=ChatSessionMessagesResponse)
async def get_chat_session_messages(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    msg_repo = MessageRepository(db)
    
    session_repo = SessionRepository(db)
    session = await session_repo.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.user_id != current_user["user_id"]:
        raise HTTPException(status_code=404, detail="Session not found")
    
    messages = await msg_repo.get_session_history(session_id)
    return ChatSessionMessagesResponse(session_id=session_id, messages=messages)

@router.delete("/{session_id}")
async def delete_chat_session(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    session_repo = SessionRepository(db)
    msg_repo = MessageRepository(db)
    
    session = await session_repo.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.user_id != current_user["user_id"]:
        raise HTTPException(status_code=404, detail="Session not found")
    
    await msg_repo.collection.delete_many({"session_id": session_id})
    await session_repo.delete_session(session_id)
    
    return {"success": True, "message": "Session deleted"}
