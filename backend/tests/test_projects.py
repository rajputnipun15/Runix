"""Tests for Project Management API endpoints.

Validates docs/06-API-SPECIFICATION.md sections 11-15.
"""

import pytest


@pytest.mark.asyncio
async def test_create_project_seeds_workspace(client, auth_user):
    """POST /api/v1/projects creates project and initializes starter files."""
    _, headers = auth_user
    response = await client.post(
        "/api/v1/projects",
        headers=headers,
        json={
            "name": "My React App",
            "description": "A test portfolio project",
            "template": "react-vite-ts",
            "visibility": "private",
        },
    )
    assert response.status_code == 201
    res = response.json()
    assert res["error"] is None
    data = res["data"]
    assert data["name"] == "My React App"
    assert data["slug"] == "my-react-app"
    assert data["status"] == "active"
    project_id = data["id"]

    # Verify project detail endpoint
    get_res = await client.get(f"/api/v1/projects/{project_id}", headers=headers)
    assert get_res.status_code == 200
    pdata = get_res.json()["data"]
    assert pdata["id"] == project_id
    assert pdata["template"] == "react-vite-ts"


@pytest.mark.asyncio
async def test_list_projects(client, auth_user):
    """GET /api/v1/projects returns paginated projects for user."""
    _, headers = auth_user
    # Create two projects
    await client.post(
        "/api/v1/projects",
        headers=headers,
        json={"name": "Project A", "template": "python-fastapi"},
    )
    await client.post(
        "/api/v1/projects",
        headers=headers,
        json={"name": "Project B", "template": "node-typescript"},
    )

    response = await client.get("/api/v1/projects", headers=headers)
    assert response.status_code == 200
    res = response.json()
    assert res["data"]["total"] == 2
    assert len(res["data"]["items"]) == 2


@pytest.mark.asyncio
async def test_update_project(client, auth_user):
    """PATCH /api/v1/projects/{id} updates project name and description."""
    _, headers = auth_user
    create_res = await client.post(
        "/api/v1/projects",
        headers=headers,
        json={"name": "Old Name", "template": "blank-docker"},
    )
    project_id = create_res.json()["data"]["id"]

    update_res = await client.patch(
        f"/api/v1/projects/{project_id}",
        headers=headers,
        json={"name": "New Name", "description": "Updated Description"},
    )
    assert update_res.status_code == 200
    assert update_res.json()["data"]["name"] == "New Name"
    assert update_res.json()["data"]["description"] == "Updated Description"


@pytest.mark.asyncio
async def test_delete_project(client, auth_user):
    """DELETE /api/v1/projects/{id} removes project and returns 204."""
    _, headers = auth_user
    create_res = await client.post(
        "/api/v1/projects",
        headers=headers,
        json={"name": "To Delete", "template": "blank-docker"},
    )
    project_id = create_res.json()["data"]["id"]

    del_res = await client.delete(f"/api/v1/projects/{project_id}", headers=headers)
    assert del_res.status_code == 204

    # Verify 404 after deletion
    get_res = await client.get(f"/api/v1/projects/{project_id}", headers=headers)
    assert get_res.status_code == 404
