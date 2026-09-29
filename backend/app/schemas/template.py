"""RUNIX Template Pydantic Schemas.

Per docs/15-PROJECT-TEMPLATES.md and docs/06-API-SPECIFICATION.md.
"""

from pydantic import BaseModel


class TemplateItem(BaseModel):
    id: str
    name: str
    description: str
    language: str
    framework: str
    runtime: str
    version: str
    default_port: int | None = None
    tags: list[str] = []


class TemplateListResponse(BaseModel):
    items: list[TemplateItem]
