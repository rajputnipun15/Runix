"""RUNIX Project Management API Endpoints.

Per docs/06-API-SPECIFICATION.md sections 11-15.
"""

import uuid

from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import Response

from app.api.deps import get_current_user, get_project_service
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.project import (
    ProjectCreatedResponse,
    ProjectCreateRequest,
    ProjectItem,
    ProjectListResponse,
    ProjectUpdateRequest,
)
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("")
async def list_projects(
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
) -> ApiResponse[ProjectListResponse]:
    """List projects accessible to the current user."""
    result = await project_service.list_projects(
        user_id=current_user.id,
        page=page,
        page_size=page_size,
        search=search,
        status=status_filter,
    )
    req_id = getattr(request.state, "request_id", "req_unknown")
    return ApiResponse(data=result, error=None, request_id=req_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_project(
    req: ProjectCreateRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
) -> ApiResponse[ProjectCreatedResponse]:
    """Create a new project and initialize its workspace."""
    project = await project_service.create_project(current_user.id, req)
    req_id = getattr(request.state, "request_id", "req_unknown")

    return ApiResponse(
        data=ProjectCreatedResponse.model_validate(project),
        error=None,
        request_id=req_id,
    )


@router.get("/{project_id}")
async def get_project(
    project_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
) -> ApiResponse[ProjectItem]:
    """Get project details by ID with access verification."""
    project = await project_service.get_project(project_id, current_user.id)
    req_id = getattr(request.state, "request_id", "req_unknown")
    return ApiResponse(
        data=ProjectItem.model_validate(project),
        error=None,
        request_id=req_id,
    )


@router.patch("/{project_id}")
async def update_project(
    project_id: uuid.UUID,
    req: ProjectUpdateRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
) -> ApiResponse[ProjectItem]:
    """Update project name or description."""
    project = await project_service.update_project(project_id, current_user.id, req)
    req_id = getattr(request.state, "request_id", "req_unknown")
    return ApiResponse(
        data=ProjectItem.model_validate(project),
        error=None,
        request_id=req_id,
    )


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
) -> Response:
    """Delete a project and its workspace storage."""
    await project_service.delete_project(project_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
