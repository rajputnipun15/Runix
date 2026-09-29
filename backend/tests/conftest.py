"""RUNIX backend test configuration and fixtures.

Sets up in-memory SQLite database, isolated temporary workspace filesystem,
and authenticated client fixtures.
"""

import tempfile
import uuid
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.api.deps import get_db, get_workspace_service
from app.core.security import create_access_token, hash_password
from app.db.base import Base
from app.main import app
from app.models.user import User
from app.services.workspace_service import WorkspaceService

# Create test engine using in-memory SQLite
test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
)
test_session_factory = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(autouse=True)
async def setup_database():
    """Create all tables before each test and drop them after."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def temp_workspace():
    """Temporary workspace directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a clean test database session."""
    async with test_session_factory() as session:
        yield session


@pytest.fixture
async def client(temp_workspace) -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP test client with database and workspace dependency overrides."""

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with test_session_factory() as session:
            yield session

    def override_workspace_service() -> WorkspaceService:
        return WorkspaceService(base_dir=temp_workspace)

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_workspace_service] = override_workspace_service

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def auth_user(db_session: AsyncSession) -> tuple[User, dict[str, str]]:
    """Create a verified test user and return the user and auth headers."""
    user = User(
        id=uuid.uuid4(),
        email="testdev@runix.io",
        password_hash=hash_password("SuperSecretPass123!"),
        display_name="Test Developer",
        is_active=True,
        email_verified=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    token = create_access_token({"sub": str(user.id), "email": user.email})
    headers = {"Authorization": f"Bearer {token}"}
    return user, headers
