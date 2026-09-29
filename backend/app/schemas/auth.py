"""RUNIX Authentication Pydantic Schemas.

Per docs/06-API-SPECIFICATION.md section 6-10.
"""

import uuid

from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    display_name: str = Field(min_length=1, max_length=100)


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserSummary(BaseModel):
    id: uuid.UUID
    email: str
    display_name: str
    avatar_url: str | None = None
    email_verified: bool = False

    model_config = {"from_attributes": True}


class AuthUserResponse(BaseModel):
    user: UserSummary


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"  # noqa: S105
    user: UserSummary


class SessionRefreshResponse(BaseModel):
    authenticated: bool = True
