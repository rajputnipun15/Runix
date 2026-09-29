"""RUNIX Authentication and Session Service.

Per docs/06-API-SPECIFICATION.md and docs/12-SECURITY-ARCHITECTURE.md.
"""

import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.exceptions import (
    AccountDisabledError,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    UserNotFoundError,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_token,
    verify_password,
)
from app.models.session import Session
from app.models.user import User
from app.schemas.auth import UserLoginRequest, UserRegisterRequest, UserSummary

settings = get_settings()


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def register(self, req: UserRegisterRequest) -> UserSummary:
        """Register a new user account with unique email and Argon2id hashed password."""
        email = req.email.strip().lower()

        # Check existing user
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        if result.scalar_one_or_none() is not None:
            raise EmailAlreadyExistsError()

        hashed_pw = hash_password(req.password)
        new_user = User(
            id=uuid.uuid4(),
            email=email,
            password_hash=hashed_pw,
            display_name=req.display_name.strip(),
            is_active=True,
            email_verified=False,
        )

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return UserSummary.model_validate(new_user)

    async def login(
        self, req: UserLoginRequest, user_agent: str | None = None, ip_address: str | None = None
    ) -> tuple[str, str, UserSummary]:
        """Authenticate user credentials and issue access + refresh tokens."""
        email = req.email.strip().lower()

        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            raise InvalidCredentialsError()

        if not verify_password(req.password, user.password_hash):
            raise InvalidCredentialsError()

        if not user.is_active:
            raise AccountDisabledError()

        # Generate tokens
        token_payload = {"sub": str(user.id), "email": user.email}
        access_token = create_access_token(token_payload)
        raw_refresh_token = create_refresh_token(token_payload)

        # Store session in DB with hashed refresh token
        expires_at = datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days)
        new_session = Session(
            id=uuid.uuid4(),
            user_id=user.id,
            refresh_token_hash=hash_token(raw_refresh_token),
            user_agent=user_agent,
            ip_address=ip_address,
            expires_at=expires_at,
        )
        self.db.add(new_session)
        await self.db.commit()

        return access_token, raw_refresh_token, UserSummary.model_validate(user)

    async def logout(self, user_id: uuid.UUID) -> None:
        """Revoke all active sessions for the user."""
        stmt = select(Session).where(Session.user_id == user_id).where(Session.revoked_at.is_(None))
        result = await self.db.execute(stmt)
        sessions = result.scalars().all()

        now = datetime.now(UTC)
        for s in sessions:
            s.revoked_at = now

        await self.db.commit()

    async def get_user_by_id(self, user_id: uuid.UUID) -> UserSummary:
        """Get user details by user ID."""
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            raise UserNotFoundError()

        return UserSummary.model_validate(user)
