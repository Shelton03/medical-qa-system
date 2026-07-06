from fastapi import HTTPException, status, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db_session
from app.core.security import verify_jwt_token
from app.models import User
from app.services.orchestrator import Orchestrator
from app.db.repositories import SessionRepository, MessageRepository
from app.db.mongodb import get_database
from sqlalchemy import select
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient

def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = authorization.split(" ")[1]
    user_id, email = verify_jwt_token(token)
    
    if user_id is None or email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"user_id": user_id, "email": email}

async def get_db_session_dep() -> AsyncSession:
    session: AsyncSession = next(get_db_session())
    try:
        yield session
    finally:
        await session.close()

async def get_orchestrator() -> Orchestrator:
    db = get_database()
    session_repo = SessionRepository(db)
    message_repo = MessageRepository(db)
    return Orchestrator(session_repo, message_repo)
