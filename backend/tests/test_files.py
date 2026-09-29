"""Tests for Workspace Filesystem API endpoints.

Validates docs/06-API-SPECIFICATION.md sections 16-19 and Rule 5 (path traversal protection).
"""

import pytest


@pytest.mark.asyncio
async def test_list_and_read_files(client, auth_user):
    """GET /projects/{id}/files returns tree and GET .../content returns file body."""
    _, headers = auth_user
    # Create project with React template
    create_res = await client.post(
        "/api/v1/projects",
        headers=headers,
        json={"name": "Files Test", "template": "react-vite-ts"},
    )
    project_id = create_res.json()["data"]["id"]

    # List files
    list_res = await client.get(f"/api/v1/projects/{project_id}/files", headers=headers)
    assert list_res.status_code == 200
    items = list_res.json()["data"]["items"]
    paths = [item["path"] for item in items]
    assert "package.json" in paths
    assert "src/App.tsx" in paths

    # Read file content
    content_res = await client.get(
        f"/api/v1/projects/{project_id}/files/content?path=src/App.tsx",
        headers=headers,
    )
    assert content_res.status_code == 200
    data = content_res.json()["data"]
    assert "⚡ RUNIX Cloud IDE" in data["content"]
    assert data["path"] == "src/App.tsx"


@pytest.mark.asyncio
async def test_write_and_update_file(client, auth_user):
    """PUT .../content updates a file atomically."""
    _, headers = auth_user
    create_res = await client.post(
        "/api/v1/projects",
        headers=headers,
        json={"name": "Write Test", "template": "blank-docker"},
    )
    project_id = create_res.json()["data"]["id"]

    new_content = "console.log('Hello from test!');"
    write_res = await client.put(
        f"/api/v1/projects/{project_id}/files/content",
        headers=headers,
        json={"path": "test.js", "content": new_content},
    )
    assert write_res.status_code == 200
    assert write_res.json()["data"]["saved"] is True

    # Read back to verify
    read_res = await client.get(
        f"/api/v1/projects/{project_id}/files/content?path=test.js",
        headers=headers,
    )
    assert read_res.status_code == 200
    assert read_res.json()["data"]["content"] == new_content


@pytest.mark.asyncio
async def test_path_traversal_prevention(client, auth_user):
    """Verify Rule 5: Path traversal attempts are rejected with 400 PATH_TRAVERSAL."""
    _, headers = auth_user
    create_res = await client.post(
        "/api/v1/projects",
        headers=headers,
        json={"name": "Security Test", "template": "blank-docker"},
    )
    project_id = create_res.json()["data"]["id"]

    # Traversal in read
    res1 = await client.get(
        f"/api/v1/projects/{project_id}/files/content?path=../../etc/passwd",
        headers=headers,
    )
    assert res1.status_code == 400
    assert res1.json()["error"]["code"] == "PATH_TRAVERSAL"

    # Traversal in write
    res2 = await client.put(
        f"/api/v1/projects/{project_id}/files/content",
        headers=headers,
        json={"path": "../../../hacked.txt", "content": "malicious"},
    )
    assert res2.status_code == 400
    assert res2.json()["error"]["code"] == "PATH_TRAVERSAL"
