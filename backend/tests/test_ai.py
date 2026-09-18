"""Tests for the AI API."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_ai_session(client: AsyncClient, demo_doctor_token: str) -> None:
    response = await client.post(
        "/api/v1/ai/sessions",
        headers={"Authorization": f"Bearer {demo_doctor_token}"},
        json={"patient_id": None},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "id" in data["data"]


@pytest.mark.asyncio
async def test_create_ai_session_as_patient(client: AsyncClient, demo_patient_token: str) -> None:
    """Patients can now create their own AI sessions."""
    response = await client.post(
        "/api/v1/ai/sessions",
        headers={"Authorization": f"Bearer {demo_patient_token}"},
        json={},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "id" in data["data"]
    assert data["data"]["patient_id"] is not None
    assert data["data"]["doctor_id"] is None


@pytest.mark.asyncio
async def test_list_ai_sessions(client: AsyncClient, demo_doctor_token: str) -> None:
    response = await client.get(
        "/api/v1/ai/sessions",
        headers={"Authorization": f"Bearer {demo_doctor_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_list_ai_sessions_as_patient(client: AsyncClient, demo_patient_token: str) -> None:
    """Patients can list their own AI sessions."""
    response = await client.get(
        "/api/v1/ai/sessions",
        headers={"Authorization": f"Bearer {demo_patient_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_ai_diagnosis_not_found(client: AsyncClient, demo_doctor_token: str) -> None:
    import uuid
    response = await client.post(
        f"/api/v1/ai/session/{uuid.uuid4()}/diagnosis",
        headers={"Authorization": f"Bearer {demo_doctor_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_ai_summary_not_found(client: AsyncClient, demo_doctor_token: str) -> None:
    import uuid
    response = await client.post(
        f"/api/v1/ai/session/{uuid.uuid4()}/summary",
        headers={"Authorization": f"Bearer {demo_doctor_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_ai_complete_not_found(client: AsyncClient, demo_doctor_token: str) -> None:
    import uuid
    response = await client.post(
        f"/api/v1/ai/session/{uuid.uuid4()}/complete",
        headers={"Authorization": f"Bearer {demo_doctor_token}"},
    )
    assert response.status_code == 404
