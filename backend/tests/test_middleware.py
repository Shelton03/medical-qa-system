"""Tests for middleware components."""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.middleware.correlation_id import CorrelationIdMiddleware, get_correlation_id
from app.middleware.rate_limit import RateLimitMiddleware


# ---------------------------------------------------------------------------
# Correlation ID
# ---------------------------------------------------------------------------
def test_correlation_id_header_propagation():
    app = FastAPI()
    app.add_middleware(CorrelationIdMiddleware)

    @app.get("/test")
    def endpoint():
        return {"correlation_id": get_correlation_id()}

    client = TestClient(app)
    custom_id = "abc-123"
    response = client.get("/test", headers={"X-Request-ID": custom_id})
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == custom_id
    assert response.json()["correlation_id"] == custom_id


def test_correlation_id_auto_generation():
    app = FastAPI()
    app.add_middleware(CorrelationIdMiddleware)

    @app.get("/test")
    def endpoint():
        return {"correlation_id": get_correlation_id()}

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200
    cid = response.headers["X-Request-ID"]
    assert cid
    assert len(cid) == 36  # UUID default length


# ---------------------------------------------------------------------------
# Rate Limit
# ---------------------------------------------------------------------------
def test_rate_limit_allows_under_limit():
    app = FastAPI()
    app.add_middleware(RateLimitMiddleware)

    @app.get("/test")
    def endpoint():
        return {"ok": True}

    client = TestClient(app)
    for _ in range(5):
        response = client.get("/test")
        assert response.status_code == 200


def test_rate_limit_skips_health():
    app = FastAPI()
    app.add_middleware(RateLimitMiddleware)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    client = TestClient(app)
    for _ in range(200):
        response = client.get("/health")
        assert response.status_code == 200


def test_rate_limit_returns_429():
    app = FastAPI()
    app.add_middleware(RateLimitMiddleware)

    @app.get("/heavy")
    def heavy():
        return {"ok": True}

    client = TestClient(app)
    # Each IP is tracked separately; TestClient uses 127.0.0.1
    responses = [client.get("/heavy") for _ in range(110)]
    # After 100 requests, should be rate limited
    assert any(r.status_code == 429 for r in responses)
    # Verify envelope
    limited = [r for r in responses if r.status_code == 429][0]
    body = limited.json()
    assert body["success"] is False
    assert body["errors"][0]["code"] == "RATE_LIMITED"
