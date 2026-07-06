"""Tests for the Records API."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_record_not_found(client: AsyncClient, demo_doctor_token: str) -> None:
    import uuid
    response = await client.get(
        f"/api/v1/records/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {demo_doctor_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_patch_record_not_found(client: AsyncClient, demo_doctor_token: str) -> None:
    import uuid
    response = await client.patch(
        f"/api/v1/records/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {demo_doctor_token}"},
        json={"record_status": "active"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_record_versions_not_found(client: AsyncClient, demo_doctor_token: str) -> None:
    import uuid
    response = await client.get(
        f"/api/v1/records/{uuid.uuid4()}/versions",
        headers={"Authorization": f"Bearer {demo_doctor_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_patch_record_forbidden_for_patient(client: AsyncClient, demo_patient_token: str) -> None:
    import uuid
    response = await client.patch(
        f"/api/v1/records/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {demo_patient_token}"},
        json={"record_status": "active"},
    )
    assert response.status_code == 403
