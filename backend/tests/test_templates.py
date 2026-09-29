"""Tests for Template API endpoints.

Validates docs/15-PROJECT-TEMPLATES.md and docs/06-API-SPECIFICATION.md.
"""

import pytest


@pytest.mark.asyncio
async def test_list_templates(client):
    """GET /api/v1/templates returns catalog of 5 approved templates."""
    response = await client.get("/api/v1/templates")
    assert response.status_code == 200
    res = response.json()
    assert res["error"] is None
    assert "request_id" in res

    items = res["data"]["items"]
    assert len(items) == 5
    ids = [t["id"] for t in items]
    assert "react-vite-ts" in ids
    assert "node-typescript" in ids
    assert "python-fastapi" in ids
    assert "mern" in ids
    assert "blank-docker" in ids


@pytest.mark.asyncio
async def test_get_template_valid(client):
    """GET /api/v1/templates/{template_id} returns detailed template config."""
    response = await client.get("/api/v1/templates/react-vite-ts")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["id"] == "react-vite-ts"
    assert data["language"] == "TypeScript"
    assert data["default_port"] == 5173


@pytest.mark.asyncio
async def test_get_template_invalid(client):
    """GET /api/v1/templates/{template_id} with invalid ID returns 422."""
    response = await client.get("/api/v1/templates/unknown-template")
    assert response.status_code == 422
    err = response.json()["error"]
    assert err["code"] == "INVALID_TEMPLATE"
