"""RUNIX Terminal WebSocket Endpoint.

Implements /ws/projects/{project_id}/terminal per docs/07-WEBSOCKET-SPECIFICATION.md.
"""

import contextlib
import json
import uuid
from datetime import UTC, datetime

import structlog
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.terminal_service import TerminalService
from app.services.workspace_service import WorkspaceService

logger = structlog.get_logger()
router = APIRouter(tags=["terminal-ws"])


@router.websocket("/ws/projects/{project_id}/terminal")
async def websocket_terminal(
    websocket: WebSocket,
    project_id: str,
) -> None:
    """Interactive WebSocket terminal connection."""
    await websocket.accept()

    session_id = str(uuid.uuid4())
    logger.info("Terminal WebSocket connected", project_id=project_id, session_id=session_id)

    terminal_service = TerminalService(WorkspaceService())

    # Send initial connection handshake per spec Section 17
    await websocket.send_text(
        json.dumps(
            {
                "type": "connected",
                "terminal_session_id": session_id,
                "runtime_id": str(project_id),
                "shell": "powershell" if os_is_windows() else "/bin/bash",
            }
        )
    )

    # Initial terminal prompt banner
    welcome_banner = (
        "\r\n\x1b[1;34m⚡ RUNIX Cloud IDE Workspace Terminal\x1b[0m\r\n"
        f"\x1b[2mSession ID: {session_id[:8]} | Workspace: /workspace\x1b[0m\r\n"
        "\x1b[2mType commands (e.g., ls, cat package.json, npm run dev, help)\x1b[0m\r\n\r\n"
    )
    await websocket.send_text(json.dumps({"type": "output", "data": welcome_banner}))

    try:
        while True:
            raw_msg = await websocket.receive_text()
            try:
                msg = json.loads(raw_msg)
            except Exception:
                msg = {"type": "input", "data": raw_msg}

            msg_type = msg.get("type", "input")

            if msg_type == "ping":
                await websocket.send_text(
                    json.dumps(
                        {
                            "type": "pong",
                            "timestamp": datetime.now(UTC).isoformat(),
                        }
                    )
                )

            elif msg_type == "input":
                cmd = msg.get("data", "").strip()
                if not cmd:
                    continue

                if cmd == "clear" or cmd == "cls":
                    await websocket.send_text(
                        json.dumps({"type": "clear", "data": "\x1b[2J\x1b[H"})
                    )
                    continue

                # Stream command execution output in real time
                async for chunk in terminal_service.stream_command(project_id, cmd):
                    await websocket.send_text(json.dumps(chunk))

            elif msg_type == "close":
                break

    except WebSocketDisconnect:
        logger.info("Terminal WebSocket disconnected", session_id=session_id)
    except Exception as exc:
        logger.error("Terminal WebSocket error", error=str(exc), session_id=session_id)
    finally:
        with contextlib.suppress(Exception):
            await websocket.close()


def os_is_windows() -> bool:
    import platform
    return platform.system().lower() == "windows"
