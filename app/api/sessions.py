from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import create_jwt_token
from app.models import User, Session as SessionModel
from app.api.deps import get_current_user, get_db_session_dep

router = APIRouter()

class SessionCreateRequest(BaseModel):
    session_name: Optional[str] = None

class SessionCreateResponse(BaseModel):
    session_id: int
    session_name: Optional[str]
    token: str

class SessionResponse(BaseModel):
    id: int
    user_id: int
    token: str
    expires_at: datetime
    created_at: datetime
    session_name: Optional[str] = None

class Message(BaseModel):
    id: Optional[int] = None
    session_id: int
    role: str
    content: str
    created_at: Optional[datetime] = None

class SessionMessagesResponse(BaseModel):
    session: SessionResponse
    messages: List[Message]

@router.get("/sessions", response_model=List[SessionResponse])
async def get_user_sessions(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session_dep),
):
    result = await db.execute(
        select(SessionModel).where(SessionModel.user_id == current_user["user_id"])
    )
    sessions = result.scalars().all()
    
    return [
        SessionResponse(
            id=s.id,
            user_id=s.user_id,
            token=s.token,
            expires_at=s.expires_at,
            created_at=s.created_at,
            session_name=None
        )
        for s in sessions
    ]

@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session_dep),
):
    result = await db.execute(
        select(SessionModel).where(
            SessionModel.id == session_id,
            SessionModel.user_id == current_user["user_id"]
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return SessionResponse(
        id=session.id,
        user_id=session.user_id,
        token=session.token,
        expires_at=session.expires_at,
        created_at=session.created_at,
        session_name=None
    )

@router.post("/sessions", response_model=SessionCreateResponse)
async def create_session(
    request: SessionCreateRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session_dep),
):
    token = create_jwt_token(current_user["user_id"], current_user["email"])
    expires_at = datetime.utcnow() + timedelta(hours=24)
    
    new_session = SessionModel(
        user_id=current_user["user_id"],
        token=token,
        expires_at=expires_at,
        created_at=datetime.utcnow()
    )
    
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    
    return SessionCreateResponse(
        session_id=new_session.id,
        session_name=request.session_name,
        token=token
    )

@router.delete("/sessions/{session_id}", response_model=dict)
async def delete_session(
    session_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session_dep),
):
    result = await db.execute(
        select(SessionModel).where(
            SessionModel.id == session_id,
            SessionModel.user_id == current_user["user_id"]
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    await db.delete(session)
    await db.commit()
    
    return {"success": True, "message": "Session deleted"}
