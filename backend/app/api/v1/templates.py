"""RUNIX Template Registry API Endpoints.

Per docs/06-API-SPECIFICATION.md and docs/15-PROJECT-TEMPLATES.md.
"""

from fastapi import APIRouter, Depends, Request

from app.api.deps import get_template_service
from app.schemas.common import ApiResponse
from app.schemas.template import TemplateItem, TemplateListResponse
from app.services.template_service import TemplateService

router = APIRouter(prefix="/templates", tags=["templates"])


@router.get("")
async def list_templates(
    request: Request,
    template_service: TemplateService = Depends(get_template_service),
) -> ApiResponse[TemplateListResponse]:
    """List all supported project templates in RUNIX."""
    templates = template_service.list_templates()
    req_id = getattr(request.state, "request_id", "req_unknown")
    return ApiResponse(
        data=TemplateListResponse(items=templates),
        error=None,
        request_id=req_id,
    )


@router.get("/{template_id}")
async def get_template(
    template_id: str,
    request: Request,
    template_service: TemplateService = Depends(get_template_service),
) -> ApiResponse[TemplateItem]:
    """Get details for a specific template."""
    template = template_service.get_template(template_id)
    req_id = getattr(request.state, "request_id", "req_unknown")
    return ApiResponse(
        data=template,
        error=None,
        request_id=req_id,
    )
