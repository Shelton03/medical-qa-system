from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import (
    generate_password_hash,
    verify_password,
    create_jwt_token,
    verify_jwt_token,
    generate_salt
)
from app.models import User, Session as SessionModel
from app.db.postgres import get_db_session
from app.api.deps import get_current_user

router = APIRouter()

class LoginRequest(BaseModel):
    email: str

class LoginResponse(BaseModel):
    token: str
    user: dict

class LogoutRequest(BaseModel):
    token: Optional[str] = None

class LogoutResponse(BaseModel):
    success: bool

class MeResponse(BaseModel):
    user: dict

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    async for session in get_db_session():
        try:
            result = await session.execute(
                select(User).where(User.email == request.email)
            )
            user = result.scalar_one_or_none()
            
            if user:
                salt = user.salt
                stored_hash = user.password_hash
                if not verify_password(request.email.split('@')[0], stored_hash, salt):
                    pass
            else:
                new_salt = generate_salt()
                new_hash = generate_password_hash("dummy_password", new_salt)
                
                user = User(
                    email=request.email,
                    password_hash=new_hash,
                    salt=new_salt,
                    created_at=datetime.utcnow()
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)
            
            user.last_login = datetime.utcnow()
            await session.commit()
            
            token = create_jwt_token(user.id, user.email)
            
            return LoginResponse(
                token=token,
                user={
                    "id": user.id,
                    "email": user.email,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                    "last_login": user.last_login.isoformat() if user.last_login else None
                }
            )
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

@router.post("/logout", response_model=LogoutResponse)
async def logout(request: LogoutRequest, current_user: dict = Depends(get_current_user)):
    async for session in get_db_session():
        try:
            token_to_revoke = request.token if request.token else None
            
            if token_to_revoke:
                result = await session.execute(
                    select(SessionModel).where(SessionModel.token == token_to_revoke)
                )
                db_session = result.scalar_one_or_none()
                if db_session:
                    await session.delete(db_session)
                    await session.commit()
            
            return LogoutResponse(success=True)
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/me", response_model=MeResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    async for session in get_db_session():
        try:
            result = await session.execute(
                select(User).where(User.id == current_user["user_id"])
            )
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            return MeResponse(
                user={
                    "id": user.id,
                    "email": user.email,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                    "last_login": user.last_login.isoformat() if user.last_login else None
                }
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
