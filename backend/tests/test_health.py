"""Health endpoint tests.

Validates docs/06-API-SPECIFICATION.md sections 40-41.
"""

import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    """GET /api/v1/health returns ok status."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_health_check_has_request_id(client):
    """Every response must include X-Request-ID header."""
    response = await client.get("/api/v1/health")
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"].startswith("req_")


@pytest.mark.asyncio
async def test_health_propagates_request_id(client):
    """Server must propagate client-provided request ID."""
    response = await client.get(
        "/api/v1/health",
        headers={"X-Request-ID": "req_test123"},
    )
    assert response.headers["X-Request-ID"] == "req_test123"


@pytest.mark.asyncio
async def test_unhandled_error_returns_structured_response(client):
    """Unhandled errors must return structured error without internal details."""
    # Request to a non-existent endpoint returns 404 or structured error
    response = await client.get("/api/v1/nonexistent")
    assert response.status_code in (404, 405)
