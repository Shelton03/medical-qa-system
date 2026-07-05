from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import create_jwt_token
from app.models import User, Session as SessionModel
from app.db.postgres import get_db_session
from app.api.deps import get_current_user

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
async def get_user_sessions(current_user: dict = Depends(get_current_user)):
    session: AsyncSession = next(get_db_session())
    try:
        result = await session.execute(
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await session.close()

@router.get("/sessions/{session_id}", response_model=SessionMessagesResponse)
async def get_session_messages(
    session_id: int,
    current_user: dict = Depends(get_current_user)
):
    db_session: AsyncSession = next(get_db_session())
    try:
        result = await db_session.execute(
            select(SessionModel).where(
                SessionModel.id == session_id,
                SessionModel.user_id == current_user["user_id"]
            )
        )
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        from motor.motor_asyncio import AsyncIOMotorClient
        from app.core.config import settings
        
        client = AsyncIOMotorClient(settings.MONGODB_URI)
        db = client[settings.MONGODB_DB_NAME]
        messages_collection = db["messages"]
        
        cursor = messages_collection.find({"session_id": session_id}).sort("created_at", 1)
        messages = await cursor.to_list(length=None)
        
        message_list = [
            Message(
                id=m.get("_id"),
                session_id=m["session_id"],
                role=m["role"],
                content=m["content"],
                created_at=m.get("created_at")
            )
            for m in messages
        ]
        
        await client.close()
        
        return SessionMessagesResponse(
            session=SessionResponse(
                id=session.id,
                user_id=session.user_id,
                token=session.token,
                expires_at=session.expires_at,
                created_at=session.created_at,
                session_name=None
            ),
            messages=message_list
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await db_session.close()

@router.post("/sessions", response_model=SessionCreateResponse)
async def create_session(
    request: SessionCreateRequest,
    current_user: dict = Depends(get_current_user)
):
    db_session: AsyncSession = next(get_db_session())
    try:
        token = create_jwt_token(current_user["user_id"], current_user["email"])
        expires_at = datetime.utcnow() + timedelta(hours=24)
        
        new_session = SessionModel(
            user_id=current_user["user_id"],
            token=token,
            expires_at=expires_at,
            created_at=datetime.utcnow()
        )
        
        db_session.add(new_session)
        await db_session.commit()
        await db_session.refresh(new_session)
        
        return SessionCreateResponse(
            session_id=new_session.id,
            session_name=request.session_name,
            token=token
        )
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await db_session.close()

@router.delete("/sessions/{session_id}", response_model=dict)
async def delete_session(
    session_id: int,
    current_user: dict = Depends(get_current_user)
):
    db_session: AsyncSession = next(get_db_session())
    try:
        result = await db_session.execute(
            select(SessionModel).where(
                SessionModel.id == session_id,
                SessionModel.user_id == current_user["user_id"]
            )
        )
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        await db_session.delete(session)
        await db_session.commit()
        
        from motor.motor_asyncio import AsyncIOMotorClient
        from app.core.config import settings
        
        client = AsyncIOMotorClient(settings.MONGODB_URI)
        db = client[settings.MONGODB_DB_NAME]
        messages_collection = db["messages"]
        await messages_collection.delete_many({"session_id": session_id})
        await client.close()
        
        return {"success": True, "message": "Session deleted"}
    except HTTPException:
        raise
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await db_session.close()
