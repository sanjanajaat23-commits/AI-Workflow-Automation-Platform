from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.workflow import Workflow
from backend.app.services.workflow_executor import WorkflowExecutor

router = APIRouter()


@router.post("/{workflow_id}")
async def trigger_webhook(
    workflow_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    workflow = (
        db.query(Workflow)
        .filter(Workflow.id == workflow_id)
        .first()
    )

    if workflow is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found.",
        )

    payload = await request.json()

    executor = WorkflowExecutor(db)

    execution = executor.execute(
        workflow=workflow,
        input_data=payload,
    )

    return {
        "message": "Webhook executed successfully.",
        "execution_id": execution.id,
        "workflow_id": workflow.id,
        "payload": payload,
    }