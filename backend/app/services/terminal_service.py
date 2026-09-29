"""RUNIX Terminal and Command Execution Service.

Executes shell commands within project workspace directories with timeout
and output streaming per docs/07-WEBSOCKET-SPECIFICATION.md and docs/06-API-SPECIFICATION.md.
"""

import asyncio
import os
import subprocess
import sys
import uuid
from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from typing import Any

import structlog

from app.schemas.command import CommandExecutionResponse
from app.services.workspace_service import WorkspaceService

logger = structlog.get_logger()


def get_shell_args(command: str) -> list[str]:
    """Return platform-appropriate shell invocation args."""
    if sys.platform == "win32":
        ps_cmd = (
            "$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'; "
            "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; "
            f"{command}"
        )
        return ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", ps_cmd]
    return ["/bin/bash", "-c", command]


class TerminalService:
    def __init__(self, workspace_service: WorkspaceService | None = None) -> None:
        self.workspace_service = workspace_service or WorkspaceService()

    async def execute_command(
        self,
        project_id: str | uuid.UUID,
        command: str,
        timeout_seconds: int = 30,
    ) -> CommandExecutionResponse:
        """Execute a shell command inside the project workspace directory."""
        workspace_dir = self.workspace_service.get_workspace_dir(str(project_id))
        exec_id = uuid.uuid4()
        started_at = datetime.now(UTC)
        shell_cmd = command.strip()

        logger.info(
            "Executing workspace command",
            project_id=str(project_id),
            command=shell_cmd,
            cwd=str(workspace_dir),
        )

        args = get_shell_args(shell_cmd)

        def _run() -> tuple[int, str, str]:
            res = subprocess.run(  # noqa: S603
                args,
                cwd=str(workspace_dir),
                capture_output=True,
                text=True,
                timeout=float(timeout_seconds),
                env=dict(os.environ),
            )
            return res.returncode, res.stdout, res.stderr

        try:
            exit_code, stdout_text, stderr_text = await asyncio.to_thread(_run)
            status = "completed" if exit_code == 0 else "failed"

        except subprocess.TimeoutExpired:
            exit_code = 124
            stdout_text = ""
            stderr_text = f"Command timed out after {timeout_seconds} seconds."
            status = "timed_out"

        except Exception as exc:
            exit_code = 1
            stdout_text = ""
            stderr_text = f"Execution error: {exc}"
            status = "error"

        finished_at = datetime.now(UTC)

        try:
            pid_uuid = uuid.UUID(str(project_id))
        except Exception:
            pid_uuid = uuid.uuid4()

        return CommandExecutionResponse(
            id=exec_id,
            project_id=pid_uuid,
            command=shell_cmd,
            status=status,
            exit_code=exit_code,
            stdout=stdout_text,
            stderr=stderr_text,
            started_at=started_at,
            finished_at=finished_at,
        )

    async def stream_command(
        self,
        project_id: str | uuid.UUID,
        command: str,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Stream command output line by line as an async generator."""
        workspace_dir = self.workspace_service.get_workspace_dir(str(project_id))
        shell_cmd = command.strip()
        args = get_shell_args(shell_cmd)

        try:
            proc = subprocess.Popen(  # noqa: S603
                args,
                cwd=str(workspace_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env=dict(os.environ),
            )

            if proc.stdout:
                while True:
                    line = await asyncio.to_thread(proc.stdout.readline)
                    if not line:
                        break
                    yield {
                        "type": "output",
                        "data": line,
                    }

            await asyncio.to_thread(proc.wait)
            yield {
                "type": "exit",
                "exit_code": proc.returncode or 0,
            }

        except Exception as exc:
            yield {
                "type": "error",
                "data": f"Failed to execute command: {exc}\n",
            }
