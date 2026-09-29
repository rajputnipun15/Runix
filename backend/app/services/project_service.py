"""RUNIX Project Management Service.

Per docs/06-API-SPECIFICATION.md sections 11-15 and docs/03-SYSTEM-ARCHITECTURE.md.
"""

import contextlib
import re
import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    ProjectAccessDeniedError,
    ProjectNotFoundError,
)
from app.models.project import Project
from app.models.workspace import Workspace
from app.schemas.project import (
    ProjectCreateRequest,
    ProjectItem,
    ProjectListResponse,
    ProjectUpdateRequest,
)
from app.services.template_service import TemplateService
from app.services.workspace_service import WorkspaceService


def slugify(text: str) -> str:
    """Generate a clean URL-friendly slug from a project name."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text or "project"


class ProjectService:
    def __init__(
        self,
        db: AsyncSession,
        workspace_service: WorkspaceService | None = None,
        template_service: TemplateService | None = None,
    ) -> None:
        self.db = db
        self.workspace_service = workspace_service or WorkspaceService()
        self.template_service = template_service or TemplateService()

    async def create_project(self, owner_id: uuid.UUID, req: ProjectCreateRequest) -> Project:
        """Create a new project, its workspace, and initialize template files."""
        # Validate template
        template_info = self.template_service.get_template(req.template)

        base_slug = slugify(req.name)
        slug = base_slug

        # Check slug uniqueness for owner
        stmt = select(Project).where(Project.owner_id == owner_id).where(Project.slug == slug)
        res = await self.db.execute(stmt)
        if res.scalar_one_or_none() is not None:
            # Append unique suffix
            slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"

        project_id = uuid.uuid4()
        new_project = Project(
            id=project_id,
            owner_id=owner_id,
            name=req.name.strip(),
            slug=slug,
            description=req.description.strip() if req.description else None,
            template=template_info.id,
            visibility=req.visibility,
            status="active",
        )
        self.db.add(new_project)

        # Create Workspace record
        workspace = Workspace(
            id=uuid.uuid4(),
            project_id=project_id,
            storage_path=str(project_id),
            status="ready",
        )
        self.db.add(workspace)

        await self.db.commit()
        await self.db.refresh(new_project)

        # Seed starter files into workspace filesystem
        with contextlib.suppress(Exception):
            self.template_service.seed_template_files(
                str(project_id), template_info.id, self.workspace_service
            )

        return new_project

    async def list_projects(
        self,
        user_id: uuid.UUID,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        status: str | None = None,
    ) -> ProjectListResponse:
        """List all projects owned by or accessible to user with pagination."""
        offset = (page - 1) * page_size

        query = select(Project).where(Project.owner_id == user_id)

        if status:
            query = query.where(Project.status == status)
        else:
            query = query.where(Project.status != "deleted")

        if search:
            query = query.where(Project.name.ilike(f"%{search}%"))

        # Count total
        count_stmt = select(func.count()).select_from(query.subquery())
        count_res = await self.db.execute(count_stmt)
        total = count_res.scalar_one() or 0

        # Fetch items
        query = query.order_by(Project.updated_at.desc()).offset(offset).limit(page_size)
        items_res = await self.db.execute(query)
        projects = items_res.scalars().all()

        items = [ProjectItem.model_validate(p) for p in projects]
        return ProjectListResponse(
            items=items,
            page=page,
            page_size=page_size,
            total=total,
        )

    async def get_project(self, project_id: uuid.UUID, user_id: uuid.UUID) -> Project:
        """Get project by ID, verifying user authorization."""
        stmt = select(Project).where(Project.id == project_id)
        res = await self.db.execute(stmt)
        project = res.scalar_one_or_none()

        if project is None or project.status == "deleted":
            raise ProjectNotFoundError()

        if project.owner_id != user_id and project.visibility != "public":
            raise ProjectAccessDeniedError()

        return project

    async def update_project(
        self, project_id: uuid.UUID, user_id: uuid.UUID, req: ProjectUpdateRequest
    ) -> Project:
        """Update project name or description."""
        project = await self.get_project(project_id, user_id)

        if project.owner_id != user_id:
            raise ProjectAccessDeniedError()

        if req.name is not None:
            project.name = req.name.strip()
        if req.description is not None:
            project.description = req.description.strip()

        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def delete_project(self, project_id: uuid.UUID, user_id: uuid.UUID) -> None:
        """Delete a project and its workspace storage."""
        project = await self.get_project(project_id, user_id)

        if project.owner_id != user_id:
            raise ProjectAccessDeniedError()

        # Delete workspace storage
        self.workspace_service.delete_workspace(str(project_id))

        # Soft or hard delete in DB
        await self.db.delete(project)
        await self.db.commit()
