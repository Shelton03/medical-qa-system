"""Tests for the Doctor API."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_doctor_dashboard(client: AsyncClient, demo_doctor_token: str) -> None:
    response = await client.get(
        "/api/v1/doctor/dashboard",
        headers={"Authorization": f"Bearer {demo_doctor_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "pending_consents" in data["data"]


@pytest.mark.asyncio
async def test_doctor_search(client: AsyncClient, demo_doctor_token: str) -> None:
    response = await client.post(
        "/api/v1/doctor/search",
        headers={"Authorization": f"Bearer {demo_doctor_token}"},
        json={"query": "Alice"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_doctor_patient_overview_not_found(client: AsyncClient, demo_doctor_token: str) -> None:
    import uuid
    response = await client.get(
        f"/api/v1/doctor/patient/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {demo_doctor_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_doctor_patient_timeline_not_found(client: AsyncClient, demo_doctor_token: str) -> None:
    import uuid
    response = await client.get(
        f"/api/v1/doctor/patient/{uuid.uuid4()}/timeline",
        headers={"Authorization": f"Bearer {demo_doctor_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_doctor_create_consultation_not_found(client: AsyncClient, demo_doctor_token: str) -> None:
    import uuid
    response = await client.post(
        f"/api/v1/doctor/patient/{uuid.uuid4()}/consultation",
        headers={"Authorization": f"Bearer {demo_doctor_token}"},
        json={"reason": "Routine checkup"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_doctor_dashboard_forbidden_for_patient(client: AsyncClient, demo_patient_token: str) -> None:
    response = await client.get(
        "/api/v1/doctor/dashboard",
        headers={"Authorization": f"Bearer {demo_patient_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_consultation_list_doctor(client: AsyncClient, demo_doctor_token: str) -> None:
    response = await client.get(
        "/api/v1/doctor",
        headers={"Authorization": f"Bearer {demo_doctor_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
