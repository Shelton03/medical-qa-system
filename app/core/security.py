import os
import secrets
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_salt() -> str:
    return secrets.token_hex(32)

def generate_password_hash(password: str, salt: str) -> str:
    combined = password + salt
    return pwd_context.hash(combined)

def verify_password(password: str, hash: str, salt: str) -> bool:
    combined = password + salt
    return pwd_context.verify(combined, hash)

def create_jwt_token(user_id: int, email: str, expiry_hours: int = None) -> str:
    if expiry_hours is None:
        expiry_hours = settings.JWT_EXPIRY_HOURS
    
    expire = datetime.utcnow() + timedelta(hours=expiry_hours)
    to_encode = {
        "exp": expire,
        "iat": datetime.utcnow(),
        "user_id": user_id,
        "email": email
    }
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm="HS256"
    )
    return encoded_jwt

def verify_jwt_token(token: str) -> tuple:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"]
        )
        user_id = payload.get("user_id")
        email = payload.get("email")
        if user_id is None or email is None:
            return None, None
        return user_id, email
    except JWTError:
        return None, None
