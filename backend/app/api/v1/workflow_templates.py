from fastapi import APIRouter, HTTPException

from backend.app.templates import (
    get_template,
    get_templates,
)

router = APIRouter(prefix="/workflow-templates", tags=["Workflow Templates"])


@router.get("")
def list_templates():
    return get_templates()


@router.get("/{template_id}")
def template_details(template_id: str):
    template = get_template(template_id)

    if template is None:
        raise HTTPException(
            status_code=404,
            detail="Template not found.",
        )

    return template