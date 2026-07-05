from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from app.core.redis import get_redis


async def notify_patient_new_consent(patient_id: uuid.UUID, consent_data: dict) -> None:
    """Push a real-time notification to the patient via Redis Pub/Sub and list."""
    redis = get_redis()
    channel = f"patient:{patient_id}:notifications"
    message = {
        "type": "CONSENT_REQUESTED",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": consent_data,
    }
    payload = json.dumps(message)
    await redis.lpush(channel, payload)
    await redis.publish(channel, payload)


async def notify_doctor_consent_updated(doctor_id: uuid.UUID, consent_data: dict) -> None:
    """Push a real-time notification to the doctor via Redis Pub/Sub and list."""
    redis = get_redis()
    channel = f"doctor:{doctor_id}:notifications"
    consent_status = consent_data.get("status", "updated")
    event_type = {
        "approved": "CONSENT_APPROVED",
        "declined": "CONSENT_DECLINED",
        "revoked": "CONSENT_REVOKED",
    }.get(consent_status, "CONSENT_UPDATED")
    message = {
        "type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": consent_data,
    }
    payload = json.dumps(message)
    await redis.lpush(channel, payload)
    await redis.publish(channel, payload)
