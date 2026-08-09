from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.schemas.workflow import (
    WorkflowCreate,
    WorkflowUpdate,
)
from backend.app.services.workflow_service import (
    create_new_workflow,
    delete_owned_workflow,
    get_owned_workflow,
    list_user_workflows,
    update_owned_workflow,
    WorkflowNotFoundError,
    WorkflowPermissionError,
)

router = APIRouter()

# Temporary user until JWT is connected
TEMP_USER_ID = 1


@router.post("/")
def create_workflow(
    workflow: WorkflowCreate,
    db: Session = Depends(get_db),
):
    return create_new_workflow(
        db=db,
        workflow=workflow,
        user_id=TEMP_USER_ID,
    )


@router.get("/")
def list_workflows(
    db: Session = Depends(get_db),
):
    return list_user_workflows(
        db=db,
        user_id=TEMP_USER_ID,
    )


@router.get("/{workflow_id}")
def get_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_owned_workflow(
            db=db,
            workflow_id=workflow_id,
            user_id=TEMP_USER_ID,
        )

    except WorkflowNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except WorkflowPermissionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e),
        )


@router.put("/{workflow_id}")
def update_workflow(
    workflow_id: int,
    workflow: WorkflowUpdate,
    db: Session = Depends(get_db),
):
    try:
        return update_owned_workflow(
            db=db,
            workflow_id=workflow_id,
            user_id=TEMP_USER_ID,
            workflow_update=workflow,
        )

    except WorkflowNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except WorkflowPermissionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e),
        )


@router.delete("/{workflow_id}")
def delete_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
):
    try:
        delete_owned_workflow(
            db=db,
            workflow_id=workflow_id,
            user_id=TEMP_USER_ID,
        )

        return {
            "message": "Workflow deleted successfully."
        }

    except WorkflowNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except WorkflowPermissionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e),
        )