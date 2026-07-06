"""Tests for the Audit API."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_audit_logs(client: AsyncClient, demo_admin_token: str) -> None:
    response = await client.get(
        "/api/v1/audit/",
        headers={"Authorization": f"Bearer {demo_admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"]["items"], list)


@pytest.mark.asyncio
async def test_list_audit_logs_forbidden_for_doctor(client: AsyncClient, demo_doctor_token: str) -> None:
    response = await client.get(
        "/api/v1/audit/",
        headers={"Authorization": f"Bearer {demo_doctor_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_list_audit_logs_forbidden_for_patient(client: AsyncClient, demo_patient_token: str) -> None:
    response = await client.get(
        "/api/v1/audit/",
        headers={"Authorization": f"Bearer {demo_patient_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_audit_log_not_found(client: AsyncClient, demo_admin_token: str) -> None:
    import uuid
    response = await client.get(
        f"/api/v1/audit/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {demo_admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_audit_logs_with_filters(client: AsyncClient, demo_admin_token: str) -> None:
    response = await client.get(
        "/api/v1/audit/?action=CONSENT_APPROVED&page=1&pageSize=10",
        headers={"Authorization": f"Bearer {demo_admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
