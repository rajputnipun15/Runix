"""RUNIX database session and engine configuration.

Uses SQLAlchemy 2.x async engine with asyncpg driver.
PostgreSQL is the control-plane source of truth per docs/03-SYSTEM-ARCHITECTURE.md.
"""

from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

settings = get_settings()

is_sqlite = str(settings.database_url).startswith("sqlite")
engine_kwargs: dict[str, Any] = {"echo": settings.database_echo}

if not is_sqlite:
    engine_kwargs.update(
        {
            "pool_pre_ping": True,
            "pool_size": 20,
            "max_overflow": 10,
        }
    )

engine = create_async_engine(
    str(settings.database_url),
    **engine_kwargs,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async database session for dependency injection."""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
