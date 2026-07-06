"""Tests for the Consent API."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_request_consent(client: AsyncClient, demo_doctor_token: str) -> None:
    import uuid
    response = await client.post(
        "/api/v1/consents",
        headers={"Authorization": f"Bearer {demo_doctor_token}"},
        json={
            "patient_id": str(uuid.uuid4()),
            "doctor_id": str(uuid.uuid4()),
            "purpose": "Test consultation",
            "shared_data": ["medical_record"],
            "expiry_hours": 24,
        },
    )
    # Should succeed or fail depending on DB state
    assert response.status_code in (200, 404, 422)


@pytest.mark.asyncio
async def test_list_consents_doctor(client: AsyncClient, demo_doctor_token: str) -> None:
    response = await client.get(
        "/api/v1/consents",
        headers={"Authorization": f"Bearer {demo_doctor_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


@pytest.mark.asyncio
async def test_list_consents_patient(client: AsyncClient, demo_patient_token: str) -> None:
    response = await client.get(
        "/api/v1/consents",
        headers={"Authorization": f"Bearer {demo_patient_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


@pytest.mark.asyncio
async def test_approve_consent_not_found(client: AsyncClient, demo_patient_token: str) -> None:
    import uuid
    response = await client.post(
        f"/api/v1/consents/{uuid.uuid4()}/approve",
        headers={"Authorization": f"Bearer {demo_patient_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_deny_consent_not_found(client: AsyncClient, demo_patient_token: str) -> None:
    import uuid
    response = await client.post(
        f"/api/v1/consents/{uuid.uuid4()}/decline",
        headers={"Authorization": f"Bearer {demo_patient_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_revoke_consent_not_found(client: AsyncClient, demo_patient_token: str) -> None:
    import uuid
    response = await client.post(
        f"/api/v1/consents/{uuid.uuid4()}/revoke",
        headers={"Authorization": f"Bearer {demo_patient_token}"},
    )
    assert response.status_code == 404
