"""Tests for Authentication API endpoints.

Validates docs/06-API-SPECIFICATION.md sections 6-10 and docs/12-SECURITY-ARCHITECTURE.md.
"""

import pytest


@pytest.mark.asyncio
async def test_register_success(client):
    """POST /api/v1/auth/register creates user account with hashed password."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "newdev@runix.io",
            "password": "SecurePassword123!",
            "display_name": "New Developer",
        },
    )
    assert response.status_code == 201
    res = response.json()
    assert res["error"] is None
    assert res["data"]["user"]["email"] == "newdev@runix.io"
    assert res["data"]["user"]["display_name"] == "New Developer"
    assert "password" not in res["data"]["user"]


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    """Registering with an already existing email returns 409 conflict."""
    payload = {
        "email": "duplicate@runix.io",
        "password": "Password123!",
        "display_name": "Dev One",
    }
    r1 = await client.post("/api/v1/auth/register", json=payload)
    assert r1.status_code == 201

    r2 = await client.post("/api/v1/auth/register", json=payload)
    assert r2.status_code == 409
    assert r2.json()["error"]["code"] == "EMAIL_ALREADY_EXISTS"


@pytest.mark.asyncio
async def test_login_success(client, auth_user):
    """POST /api/v1/auth/login with valid credentials returns JWT token."""
    user, _ = auth_user
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": user.email,
            "password": "SuperSecretPass123!",
        },
    )
    assert response.status_code == 200
    res = response.json()
    assert res["error"] is None
    data = res["data"]
    assert "access_token" in data
    assert data["user"]["email"] == user.email


@pytest.mark.asyncio
async def test_login_invalid_password(client, auth_user):
    """POST /api/v1/auth/login with wrong password returns 401 INVALID_CREDENTIALS."""
    user, _ = auth_user
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": user.email,
            "password": "WrongPassword999!",
        },
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"


@pytest.mark.asyncio
async def test_login_nonexistent_email(client):
    """POST /api/v1/auth/login with unknown email returns 401 without revealing user existence."""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "nonexistent@runix.io",
            "password": "Password123!",
        },
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"


@pytest.mark.asyncio
async def test_get_me_authenticated(client, auth_user):
    """GET /api/v1/auth/me returns current user profile when bearer token provided."""
    user, headers = auth_user
    response = await client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    res = response.json()
    assert res["data"]["email"] == user.email
    assert res["data"]["display_name"] == user.display_name


@pytest.mark.asyncio
async def test_get_me_unauthenticated(client):
    """GET /api/v1/auth/me without token returns 401 AUTHENTICATION_REQUIRED."""
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "AUTHENTICATION_REQUIRED"


@pytest.mark.asyncio
async def test_logout(client, auth_user):
    """POST /api/v1/auth/logout revokes sessions and returns 204."""
    _, headers = auth_user
    response = await client.post("/api/v1/auth/logout", headers=headers)
    assert response.status_code == 204
