from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.auth.service import login_doctor, login_patient, refresh_access_token, logout
from app.auth.dependencies import get_current_user, oauth2_scheme
from app.auth.jwt import decode_token
from app.auth.demo import is_demo_token, generate_demo_tokens, _DEMO_DOCTOR_UUID, _DEMO_PATIENT_UUID
from app.schemas.envelope import Envelope
from app.schemas.token import TokenPair
from app.schemas.user import UserResponse

router = APIRouter()


class DoctorLoginRequest(BaseModel):
    model_config = ConfigDict(strict=True)
    email: EmailStr
    password: str


class PatientLoginRequest(BaseModel):
    model_config = ConfigDict(strict=True)
    national_id: str
    pin: str


class RefreshRequest(BaseModel):
    model_config = ConfigDict(strict=True)
    refresh_token: str


class RefreshResponse(BaseModel):
    model_config = ConfigDict(strict=True)
    access_token: str
    token_type: str = "bearer"
    expires_in: int


@router.post(
    "/doctor/login",
    response_model=Envelope[TokenPair],
    summary="Doctor login",
    description="Authenticate a doctor by email and password, with demo fallback.",
)
async def doctor_login(
    body: DoctorLoginRequest,
    db: AsyncSession = Depends(get_db),
) -> Envelope[TokenPair]:
    token_pair = await login_doctor(body.email, body.password, db)
    return Envelope.ok(token_pair)


@router.post(
    "/patient/login",
    response_model=Envelope[TokenPair],
    summary="Patient login",
    description="Authenticate a patient by national ID and PIN, with demo fallback.",
)
async def patient_login(
    body: PatientLoginRequest,
    db: AsyncSession = Depends(get_db),
) -> Envelope[TokenPair]:
    token_pair = await login_patient(body.national_id, body.pin, db)
    return Envelope.ok(token_pair)


@router.post(
    "/refresh",
    response_model=Envelope[RefreshResponse],
    summary="Refresh access token",
    description="Exchange a valid refresh token for a new access token.",
)
async def refresh(body: RefreshRequest) -> Envelope[RefreshResponse]:
    new_access = await refresh_access_token(body.refresh_token)
    from app.core.config import settings
    return Envelope.ok(
        RefreshResponse(
            access_token=new_access,
            token_type="bearer",
            expires_in=settings.jwt_expiration,
        )
    )


@router.post(
    "/logout",
    response_model=Envelope[dict],
    summary="Logout",
    description="Revoke the current token by blacklisting its JTI in Redis.",
)
async def logout_endpoint(
    token: str = Depends(oauth2_scheme),
) -> Envelope[dict]:
    payload = decode_token(token)
    jti = payload.get("jti")
    if jti:
        await logout(jti)
    return Envelope.ok({"message": "Logged out successfully."})


@router.get(
    "/me",
    response_model=Envelope[UserResponse],
    summary="Current user profile",
    description="Return the authenticated user's profile.",
)
async def me(
    current_user=Depends(get_current_user),
) -> Envelope[UserResponse]:
    user = current_user
    return Envelope.ok(
        UserResponse(
            id=str(user.id),
            role=user.role,
            first_name=user.first_name,
            last_name=user.last_name,
            email=getattr(user, "email", ""),
            avatar_url=getattr(user, "avatar_url", None),
        )
    )
