"""RUNIX Workspace Commands API.

Implements command execution endpoints per docs/06-API-SPECIFICATION.md.
"""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.command import CommandExecutionRequest, CommandExecutionResponse
from app.schemas.common import ApiResponse
from app.services.terminal_service import TerminalService

router = APIRouter(tags=["commands"])


def get_terminal_service() -> TerminalService:
    return TerminalService()


@router.post("/projects/{project_id}/commands")
async def execute_command(
    project_id: uuid.UUID,
    req: CommandExecutionRequest,
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    terminal_service: Annotated[TerminalService, Depends(get_terminal_service)],
) -> ApiResponse[CommandExecutionResponse]:
    """Execute a shell command inside the project's workspace."""
    result = await terminal_service.execute_command(
        project_id=project_id,
        command=req.command,
        timeout_seconds=req.timeout_seconds,
    )

    req_id = getattr(request.state, "request_id", "req_unknown")
    return ApiResponse(
        data=result,
        error=None,
        request_id=req_id,
    )
