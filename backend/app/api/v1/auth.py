"""RUNIX Authentication API Endpoints.

Per docs/06-API-SPECIFICATION.md sections 6-10.
"""

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import Response

from app.api.deps import get_auth_service, get_current_user
from app.models.user import User
from app.schemas.auth import (
    AuthUserResponse,
    SessionRefreshResponse,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserSummary,
)
from app.schemas.common import ApiResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    req: UserRegisterRequest,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
) -> ApiResponse[AuthUserResponse]:
    """Create a new RUNIX developer account."""
    user = await auth_service.register(req)
    req_id = getattr(request.state, "request_id", "req_unknown")
    return ApiResponse(
        data=AuthUserResponse(user=user),
        error=None,
        request_id=req_id,
    )


@router.post("/login")
async def login(
    req: UserLoginRequest,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
) -> ApiResponse[TokenResponse]:
    """Authenticate with email and password."""
    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None

    access_token, _, user = await auth_service.login(
        req, user_agent=user_agent, ip_address=ip_address
    )
    req_id = getattr(request.state, "request_id", "req_unknown")

    return ApiResponse(
        data=TokenResponse(access_token=access_token, user=user),
        error=None,
        request_id=req_id,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> Response:
    """Invalidate authenticated sessions."""
    await auth_service.logout(current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/refresh")
async def refresh(
    request: Request,
    current_user: User = Depends(get_current_user),
) -> ApiResponse[SessionRefreshResponse]:
    """Refresh active session."""
    req_id = getattr(request.state, "request_id", "req_unknown")
    return ApiResponse(
        data=SessionRefreshResponse(authenticated=True),
        error=None,
        request_id=req_id,
    )


@router.get("/me")
async def get_me(
    request: Request,
    current_user: User = Depends(get_current_user),
) -> ApiResponse[UserSummary]:
    """Return currently authenticated user profile."""
    req_id = getattr(request.state, "request_id", "req_unknown")
    return ApiResponse(
        data=UserSummary.model_validate(current_user),
        error=None,
        request_id=req_id,
    )
