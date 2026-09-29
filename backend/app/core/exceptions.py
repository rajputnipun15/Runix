"""RUNIX domain exceptions and structured error handling.

Per docs/18-ERROR-HANDLING.md: All errors are structured, traceable, and safe.
Internal details are never exposed to users.
"""

from typing import Any


class RunixError(Exception):
    """Base exception for all RUNIX domain errors."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


# Authentication errors
class InvalidCredentialsError(RunixError):
    def __init__(self) -> None:
        super().__init__(
            code="INVALID_CREDENTIALS",
            message="Invalid email or password.",
            status_code=401,
        )


class AuthenticationRequiredError(RunixError):
    def __init__(self) -> None:
        super().__init__(
            code="AUTHENTICATION_REQUIRED",
            message="Authentication is required.",
            status_code=401,
        )


class TokenExpiredError(RunixError):
    def __init__(self) -> None:
        super().__init__(
            code="TOKEN_EXPIRED",
            message="Authentication token has expired.",
            status_code=401,
        )


class AccountDisabledError(RunixError):
    def __init__(self) -> None:
        super().__init__(
            code="ACCOUNT_DISABLED",
            message="This account has been disabled.",
            status_code=403,
        )


# Authorization errors
class ProjectAccessDeniedError(RunixError):
    def __init__(self) -> None:
        super().__init__(
            code="PROJECT_ACCESS_DENIED",
            message="You do not have access to this project.",
            status_code=403,
        )


# Resource errors
class ProjectNotFoundError(RunixError):
    def __init__(self) -> None:
        super().__init__(
            code="PROJECT_NOT_FOUND",
            message="Project was not found.",
            status_code=404,
        )


class UserNotFoundError(RunixError):
    def __init__(self) -> None:
        super().__init__(
            code="USER_NOT_FOUND",
            message="User was not found.",
            status_code=404,
        )


class FileNotFoundError(RunixError):  # noqa: A001
    def __init__(self, path: str = "") -> None:
        super().__init__(
            code="FILE_NOT_FOUND",
            message=f"File not found: {path}" if path else "File not found.",
            status_code=404,
        )


# Conflict errors
class EmailAlreadyExistsError(RunixError):
    def __init__(self) -> None:
        super().__init__(
            code="EMAIL_ALREADY_EXISTS",
            message="An account with this email already exists.",
            status_code=409,
        )


class ProjectSlugExistsError(RunixError):
    def __init__(self) -> None:
        super().__init__(
            code="PROJECT_SLUG_EXISTS",
            message="A project with this name already exists.",
            status_code=409,
        )


# Validation errors
class ValidationError(RunixError):
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(
            code="VALIDATION_ERROR",
            message=message,
            status_code=422,
            details=details,
        )


class InvalidTemplateError(RunixError):
    def __init__(self, template: str) -> None:
        super().__init__(
            code="INVALID_TEMPLATE",
            message=f"Template '{template}' is not a valid template.",
            status_code=422,
        )


# Security errors
class PathTraversalError(RunixError):
    def __init__(self) -> None:
        super().__init__(
            code="PATH_TRAVERSAL",
            message="Invalid file path.",
            status_code=400,
        )


class FileTooLargeError(RunixError):
    def __init__(self) -> None:
        super().__init__(
            code="FILE_TOO_LARGE",
            message="File exceeds maximum allowed size.",
            status_code=413,
        )


class WorkspaceQuotaExceededError(RunixError):
    def __init__(self) -> None:
        super().__init__(
            code="WORKSPACE_QUOTA_EXCEEDED",
            message="Workspace storage quota exceeded.",
            status_code=413,
        )


# Runtime errors
class RuntimeNotFoundError(RunixError):
    def __init__(self) -> None:
        super().__init__(
            code="RUNTIME_NOT_FOUND",
            message="Runtime not found.",
            status_code=404,
        )


class RuntimeInvalidStateError(RunixError):
    def __init__(self, current: str, requested: str) -> None:
        super().__init__(
            code="RUNTIME_INVALID_STATE",
            message=f"Cannot transition runtime from '{current}' to '{requested}'.",
            status_code=409,
        )
