"""RUNIX API common schemas and response envelopes.

Per docs/06-API-SPECIFICATION.md: All responses use standard envelope:
{
  "data": ...,
  "error": ...,
  "request_id": "req_..."
}
"""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: list[dict[str, Any]] | None = None


class ApiResponse(BaseModel, Generic[T]):
    data: T | None = None
    error: ErrorDetail | None = None
    request_id: str
