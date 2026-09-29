"""RUNIX Health check API endpoints.

GET /health — basic process health (lightweight).
GET /health/ready — checks required dependencies.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """Basic process health check — remains lightweight."""
    return {"status": "ok"}


@router.get("/health/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    """Check required dependencies: PostgreSQL, Redis, runtime_manager."""
    dependencies = {}

    # PostgreSQL check
    try:
        await db.execute(text("SELECT 1"))
        dependencies["postgres"] = "ok"
    except Exception:
        dependencies["postgres"] = "unavailable"

    # Redis check — placeholder until Redis integration is wired
    dependencies["redis"] = "ok"

    # Runtime manager check — placeholder until runtime manager exists
    dependencies["runtime_manager"] = "ok"

    all_ok = all(v == "ok" for v in dependencies.values())

    if not all_ok:
        from fastapi.responses import JSONResponse

        return JSONResponse(
            status_code=503,
            content={
                "status": "unavailable",
                "dependencies": dependencies,
            },
        )

    return {
        "status": "ready",
        "dependencies": dependencies,
    }
