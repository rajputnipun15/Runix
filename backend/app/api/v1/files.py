"""RUNIX Workspace Filesystem API Endpoints.

Per docs/06-API-SPECIFICATION.md sections 16-19.
Always validates project authorization and prevents path traversal.
"""

import uuid

from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import Response

from app.api.deps import get_current_user, get_project_service, get_workspace_service
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.file import (
    FileContentResponse,
    FileCreateRequest,
    FileListResponse,
    FileWriteRequest,
    FileWriteResponse,
)
from app.services.project_service import ProjectService
from app.services.workspace_service import WorkspaceService

router = APIRouter(prefix="/projects/{project_id}/files", tags=["files"])


@router.get("")
async def list_files(
    project_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
) -> ApiResponse[FileListResponse]:
    """List all workspace files and directories for a project."""
    # Authorize project access
    await project_service.get_project(project_id, current_user.id)

    files = workspace_service.list_files(str(project_id))
    req_id = getattr(request.state, "request_id", "req_unknown")
    return ApiResponse(data=FileListResponse(items=files), error=None, request_id=req_id)


@router.get("/content")
async def get_file_content(
    project_id: uuid.UUID,
    request: Request,
    path: str = Query(..., min_length=1),
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
) -> ApiResponse[FileContentResponse]:
    """Read contents of a file inside the project workspace."""
    await project_service.get_project(project_id, current_user.id)

    content = workspace_service.read_file(str(project_id), path)
    req_id = getattr(request.state, "request_id", "req_unknown")
    return ApiResponse(data=content, error=None, request_id=req_id)


@router.put("/content")
async def update_file_content(
    project_id: uuid.UUID,
    req: FileWriteRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
) -> ApiResponse[FileWriteResponse]:
    """Atomically write content to a file inside the project workspace."""
    await project_service.get_project(project_id, current_user.id)

    result = workspace_service.write_file(str(project_id), req.path, req.content)
    req_id = getattr(request.state, "request_id", "req_unknown")
    return ApiResponse(data=result, error=None, request_id=req_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_file_or_dir(
    project_id: uuid.UUID,
    req: FileCreateRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
) -> ApiResponse[FileWriteResponse]:
    """Create a new file or directory inside the project workspace."""
    await project_service.get_project(project_id, current_user.id)

    if req.type == "directory":
        workspace_service.create_directory(str(project_id), req.path)
        result = FileWriteResponse(path=req.path, saved=True, size_bytes=0)
    else:
        result = workspace_service.write_file(str(project_id), req.path, req.content or "")

    req_id = getattr(request.state, "request_id", "req_unknown")
    return ApiResponse(data=result, error=None, request_id=req_id)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file_or_dir(
    project_id: uuid.UUID,
    path: str = Query(..., min_length=1),
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
) -> Response:
    """Delete a file or directory from the workspace."""
    await project_service.get_project(project_id, current_user.id)
    workspace_service.delete_item(str(project_id), path)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
