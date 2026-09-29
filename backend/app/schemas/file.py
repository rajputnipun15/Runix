"""RUNIX File and Workspace Schemas.

Per docs/06-API-SPECIFICATION.md sections 16-19 and docs/09-WORKSPACE-FILESYSTEM.md.
"""

from typing import Literal

from pydantic import BaseModel, Field


class FileTreeItem(BaseModel):
    path: str
    type: Literal["file", "directory"]
    size_bytes: int | None = None


class FileListResponse(BaseModel):
    items: list[FileTreeItem]


class FileContentResponse(BaseModel):
    path: str
    content: str
    encoding: str = "utf-8"
    size_bytes: int


class FileWriteRequest(BaseModel):
    path: str = Field(min_length=1)
    content: str


class FileWriteResponse(BaseModel):
    path: str
    saved: bool = True
    size_bytes: int


class FileCreateRequest(BaseModel):
    path: str = Field(min_length=1)
    type: Literal["file", "directory"]
    content: str | None = None
