"""Tests for RUNIX Workspace Terminal and Command Execution API."""

import pytest
from httpx import AsyncClient

from app.models.user import User
from app.services.terminal_service import TerminalService
from app.services.workspace_service import WorkspaceService


@pytest.mark.asyncio
async def test_terminal_service_execute():
    """TerminalService should execute shell commands inside workspace directory."""
    ws = WorkspaceService()
    ts = TerminalService(ws)

    res = await ts.execute_command("test-proj", "echo RUNIX_TEST_OK")
    assert res.status == "completed"
    assert res.exit_code == 0
    assert "RUNIX_TEST_OK" in res.stdout


@pytest.mark.asyncio
async def test_commands_api_unauthorized(client: AsyncClient):
    """POST /projects/{id}/commands without auth should return 401."""
    resp = await client.post(
        "/api/v1/projects/00000000-0000-0000-0000-000000000001/commands",
        json={"command": "echo test"},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_commands_api_authorized(
    client: AsyncClient,
    auth_user: tuple[User, dict[str, str]],
):
    """POST /projects/{id}/commands with auth should execute command and return results."""
    user, headers = auth_user

    # 1. Create a project
    create_resp = await client.post(
        "/api/v1/projects",
        json={
            "name": "Terminal Test App",
            "template": "react-vite-ts",
            "visibility": "private",
        },
        headers=headers,
    )
    assert create_resp.status_code == 201
    proj_id = create_resp.json()["data"]["id"]

    # 2. Execute a command in this project's workspace
    cmd_resp = await client.post(
        f"/api/v1/projects/{proj_id}/commands",
        json={"command": "echo HELLO_FROM_RUNIX_TERMINAL"},
        headers=headers,
    )
    assert cmd_resp.status_code == 200
    data = cmd_resp.json()["data"]
    assert data["status"] == "completed"
    assert data["exit_code"] == 0
    assert "HELLO_FROM_RUNIX_TERMINAL" in data["stdout"]
