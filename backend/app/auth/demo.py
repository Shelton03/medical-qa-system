from __future__ import annotations

import uuid

from app.auth.jwt import create_access_token, create_refresh_token
from app.core.config import settings

DEMO_CREDENTIALS = {
    "doctor": [
        {
            "email": "dr.sarah.mirage@mirage.health",
            "password": "Healthathon2024!",
        }
    ],
    "patient": [
        {
            "national_id": "ZIM-89-4567234",
            "pin": "2024",
        }
    ],
    "admin": [
        {
            "email": "admin@mirage.health",
            "password": "Admin2024!",
        }
    ],
}

_DEMO_DOCTOR_UUID = uuid.uuid5(uuid.NAMESPACE_OID, "demo-doctor-dr.sarah.mirage@mirage.health")
_DEMO_PATIENT_UUID = uuid.uuid5(uuid.NAMESPACE_OID, "demo-patient-ZIM-89-4567234")
_DEMO_ADMIN_UUID = uuid.uuid5(uuid.NAMESPACE_OID, "demo-admin@mirage.health")


def authenticate_demo_doctor(email: str, password: str) -> bool:
    """Check whether provided credentials match demo doctor credentials."""
    if not settings.demo_mode_enabled:
        return False
    for cred in DEMO_CREDENTIALS["doctor"]:
        if cred["email"] == email and cred["password"] == password:
            return True
    return False


def authenticate_demo_patient(national_id: str, pin: str) -> bool:
    """Check whether provided credentials match demo patient credentials."""
    if not settings.demo_mode_enabled:
        return False
    for cred in DEMO_CREDENTIALS["patient"]:
        if cred["national_id"] == national_id and cred["pin"] == pin:
            return True
    return False


def authenticate_demo_admin(email: str, password: str) -> bool:
    """Check whether provided credentials match demo admin credentials."""
    if not settings.demo_mode_enabled:
        return False
    for cred in DEMO_CREDENTIALS["admin"]:
        if cred["email"] == email and cred["password"] == password:
            return True
    return False


def generate_demo_tokens(role: str) -> tuple[str, str, uuid.UUID]:
    """Return (access_token, refresh_token, synthetic_uuid) for a demo role."""
    if role == "doctor":
        synthetic_uuid = _DEMO_DOCTOR_UUID
    elif role == "patient":
        synthetic_uuid = _DEMO_PATIENT_UUID
    elif role == "admin":
        synthetic_uuid = _DEMO_ADMIN_UUID
    else:
        raise ValueError("Unsupported demo role")

    access = create_access_token(synthetic_uuid, role=role)
    refresh = create_refresh_token(synthetic_uuid, role=role)
    return access, refresh, synthetic_uuid


def is_demo_token(token_payload: dict) -> bool:
    """Return True if the payload subject matches a synthetic demo UUID."""
    payload_sub = token_payload.get("sub")
    return payload_sub in (
        str(_DEMO_DOCTOR_UUID),
        str(_DEMO_PATIENT_UUID),
        str(_DEMO_ADMIN_UUID),
    )
