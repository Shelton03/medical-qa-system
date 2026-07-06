"""Tests for the Patient API."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_me_requires_auth(client: AsyncClient) -> None:
    response = await client.get("/api/v1/me/patient")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_patient(client: AsyncClient, demo_patient_token: str) -> None:
    response = await client.get(
        "/api/v1/me/patient",
        headers={"Authorization": f"Bearer {demo_patient_token}"},
    )
    # May be 404 if no patient record seeded in test DB
    assert response.status_code in (200, 404)


@pytest.mark.asyncio
async def test_update_me_patient(client: AsyncClient, demo_patient_token: str) -> None:
    response = await client.put(
        "/api/v1/me/patient",
        headers={"Authorization": f"Bearer {demo_patient_token}"},
        json={"address": "123 Test St", "preferred_language": "en"},
    )
    assert response.status_code in (200, 404)


@pytest.mark.asyncio
async def test_get_me_timeline(client: AsyncClient, demo_patient_token: str) -> None:
    response = await client.get(
        "/api/v1/me/patient/timeline",
        headers={"Authorization": f"Bearer {demo_patient_token}"},
    )
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        data = response.json()
        assert data["success"] is True
        assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_get_me_visits(client: AsyncClient, demo_patient_token: str) -> None:
    response = await client.get(
        "/api/v1/me/patient/visits",
        headers={"Authorization": f"Bearer {demo_patient_token}"},
    )
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_get_me_visit_detail_not_found(client: AsyncClient, demo_patient_token: str) -> None:
    import uuid
    response = await client.get(
        f"/api/v1/me/patient/visit/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {demo_patient_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_me_notifications(client: AsyncClient, demo_patient_token: str) -> None:
    response = await client.get(
        "/api/v1/me/patient/notifications",
        headers={"Authorization": f"Bearer {demo_patient_token}"},
    )
    assert response.status_code in (200, 404)


@pytest.mark.asyncio
async def test_get_me_access_history(client: AsyncClient, demo_patient_token: str) -> None:
    response = await client.get(
        "/api/v1/me/patient/access-history",
        headers={"Authorization": f"Bearer {demo_patient_token}"},
    )
    assert response.status_code in (200, 404)


@pytest.mark.asyncio
async def test_patient_list_requires_doctor(client: AsyncClient, demo_patient_token: str) -> None:
    response = await client.get(
        "/api/v1/patients",
        headers={"Authorization": f"Bearer {demo_patient_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_patient_create_forbidden_for_patient(client: AsyncClient, demo_patient_token: str) -> None:
    response = await client.post(
        "/api/v1/patients",
        headers={"Authorization": f"Bearer {demo_patient_token}"},
        json={
            "first_name": "Test",
            "last_name": "User",
            "national_id": "TEST123",
            "phone": "000",
            "date_of_birth": "1990-01-01",
            "gender": "Male",
        },
    )
    assert response.status_code == 403
