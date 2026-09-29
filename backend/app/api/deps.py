"""RUNIX FastAPI route dependencies.

Handles database session injection, services, and JWT authentication.
"""

import uuid

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthenticationRequiredError
from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User
from app.services.auth_service import AuthService
from app.services.project_service import ProjectService
from app.services.template_service import TemplateService
from app.services.workspace_service import WorkspaceService

security_bearer = HTTPBearer(auto_error=False)


def get_template_service() -> TemplateService:
    return TemplateService()


def get_workspace_service() -> WorkspaceService:
    return WorkspaceService()


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)


def get_project_service(
    db: AsyncSession = Depends(get_db),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
    template_service: TemplateService = Depends(get_template_service),
) -> ProjectService:
    return ProjectService(db, workspace_service, template_service)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_bearer),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Extract and validate JWT Bearer token, returning the authenticated User."""
    if not credentials or not credentials.credentials:
        raise AuthenticationRequiredError()

    token = credentials.credentials
    payload = decode_token(token)

    if not payload:
        raise AuthenticationRequiredError()

    if payload.get("type") != "access":
        raise AuthenticationRequiredError()

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise AuthenticationRequiredError()

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise AuthenticationRequiredError() from None

    auth_service = AuthService(db)
    user_summary = await auth_service.get_user_by_id(user_id)

    # Return minimal user object with id and email
    user = User(
        id=user_summary.id,
        email=user_summary.email,
        display_name=user_summary.display_name,
        avatar_url=user_summary.avatar_url,
        is_active=True,
        email_verified=user_summary.email_verified,
    )
    return user
