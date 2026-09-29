"""RUNIX Project Pydantic Schemas.

Per docs/06-API-SPECIFICATION.md sections 11-15.
"""

import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ProjectCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    template: str = Field(min_length=1, max_length=50)
    visibility: Literal["private", "public"] = "private"


class ProjectUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)


class ProjectItem(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    description: str | None = None
    template: str
    visibility: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProjectCreatedResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    template: str
    status: str

    model_config = {"from_attributes": True}


class ProjectListResponse(BaseModel):
    items: list[ProjectItem]
    page: int = 1
    page_size: int = 20
    total: int = 0
