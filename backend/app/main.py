"""RUNIX backend FastAPI application.

Main entry point for the RUNIX API server.
Per docs/06-API-SPECIFICATION.md: base path is /api/v1.
"""

import uuid
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.exceptions import RunixError

settings = get_settings()

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application startup and shutdown lifecycle."""
    logger.info("RUNIX API starting", environment=settings.environment)

    # Ensure database schema is created (SQLite or PostgreSQL)
    from sqlalchemy import select

    import app.models  # noqa: F401
    from app.db.base import Base
    from app.db.session import async_session_factory, engine
    from app.models.user import User
    from app.services.auth_service import AuthService

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Seed default developer accounts if not present
        async with async_session_factory() as session:
            from app.schemas.auth import UserRegisterRequest
            auth_svc = AuthService(session)

            for email, pw, name in [
                ("developer@runix.internal", "runix-dev-password-2025", "Developer"),
                ("demo@runix.internal", "Demopassword123!", "Demo Developer"),
            ]:
                stmt = select(User).where(User.email == email)
                res = await session.execute(stmt)
                if not res.scalar_one_or_none():
                    await auth_svc.register(
                        UserRegisterRequest(
                            email=email,
                            password=pw,
                            display_name=name,
                        )
                    )
                    logger.info("Seeded dev user", email=email)
    except Exception as e:
        logger.warning("Database startup init skipped", error=str(e))

    yield
    logger.info("RUNIX API shutting down")


app = FastAPI(
    title="RUNIX API",
    description="Cloud Development Platform API — Build. Run. Ship. Anywhere.",
    version=settings.app_version,
    docs_url="/docs" if not settings.is_production else None,
    openapi_url="/openapi.json" if not settings.is_production else None,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)


# Request ID middleware
@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    """Attach a request ID to every request per docs/06-API-SPECIFICATION.md section 49."""
    request_id = request.headers.get("X-Request-ID")
    if not request_id or len(request_id) > 128:
        request_id = f"req_{uuid.uuid4().hex[:16]}"

    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# Structured error handlers
@app.exception_handler(RunixError)
async def runix_error_handler(request: Request, exc: RunixError):
    """Handle all RUNIX domain errors with structured response format."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning(
        "Domain error",
        error_code=exc.code,
        status_code=exc.status_code,
        request_id=request_id,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "data": None,
            "error": {
                "code": exc.code,
                "message": exc.message,
            },
            "request_id": request_id,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    request_id = getattr(request.state, "request_id", "unknown")
    errors = []
    for error in exc.errors():
        errors.append(
            {
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
            }
        )
    return JSONResponse(
        status_code=422,
        content={
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed.",
                "details": errors,
            },
            "request_id": request_id,
        },
    )


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    """Catch-all for unhandled errors — never expose internal details."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(
        "Unhandled error",
        error=str(exc),
        error_type=type(exc).__name__,
        request_id=request_id,
    )
    return JSONResponse(
        status_code=500,
        content={
            "data": None,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal error occurred.",
            },
            "request_id": request_id,
        },
    )


# Register routers
from app.api.v1.auth import router as auth_router  # noqa: E402
from app.api.v1.commands import router as commands_router  # noqa: E402
from app.api.v1.files import router as files_router  # noqa: E402
from app.api.v1.health import router as health_router  # noqa: E402
from app.api.v1.projects import router as projects_router  # noqa: E402
from app.api.v1.templates import router as templates_router  # noqa: E402
from app.api.ws.terminal import router as terminal_ws_router  # noqa: E402

app.include_router(health_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1")
app.include_router(templates_router, prefix="/api/v1")
app.include_router(files_router, prefix="/api/v1")
app.include_router(commands_router, prefix="/api/v1")
app.include_router(terminal_ws_router)
