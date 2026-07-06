"""Tests for the Authentication API."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_demo_login_patient(client: AsyncClient) -> None:
    response = await client.post("/api/v1/auth/demo-login", json={"role": "patient"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert data["data"]["role"] == "patient"
    assert data["data"]["demo_mode"] is True


@pytest.mark.asyncio
async def test_demo_login_doctor(client: AsyncClient) -> None:
    response = await client.post("/api/v1/auth/demo-login", json={"role": "doctor"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["role"] == "doctor"


@pytest.mark.asyncio
async def test_demo_login_admin(client: AsyncClient) -> None:
    response = await client.post("/api/v1/auth/demo-login", json={"role": "admin"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["role"] == "admin"


@pytest.mark.asyncio
async def test_demo_login_invalid_role(client: AsyncClient) -> None:
    response = await client.post("/api/v1/auth/demo-login", json={"role": "nurse"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_jwt_me(client: AsyncClient, demo_doctor_token: str) -> None:
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {demo_doctor_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["role"] == "doctor"


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient) -> None:
    from app.auth.demo import generate_demo_tokens
    _, refresh_token, _ = generate_demo_tokens("doctor")
    response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]


@pytest.mark.asyncio
async def test_logout(client: AsyncClient, demo_doctor_token: str) -> None:
    response = await client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {demo_doctor_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
