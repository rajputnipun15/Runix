"""Pydantic schemas for command execution."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class CommandExecutionRequest(BaseModel):
    """Request to execute a command inside a workspace."""

    command: str = Field(
        ...,
        min_length=1,
        max_length=2048,
        description="Command to execute",
    )
    timeout_seconds: int = Field(
        default=30,
        ge=1,
        le=300,
        description="Execution timeout in seconds",
    )


class CommandExecutionResponse(BaseModel):
    """Response containing command execution results."""

    id: uuid.UUID
    project_id: uuid.UUID
    command: str
    status: str
    exit_code: int
    stdout: str
    stderr: str
    started_at: datetime
    finished_at: datetime
