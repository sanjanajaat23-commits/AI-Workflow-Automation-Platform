from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.workflow import Workflow
from backend.app.models.execution import Execution
from backend.app.schemas.execution import ExecutionResponse
from backend.app.services.workflow_executor import WorkflowExecutor

router = APIRouter()


@router.get("", response_model=list[ExecutionResponse])
def get_executions(db: Session = Depends(get_db)):
    return db.query(Execution).order_by(Execution.id.desc()).all()


@router.get("/{execution_id}", response_model=ExecutionResponse)
def get_execution(execution_id: int, db: Session = Depends(get_db)):
    execution = db.query(Execution).filter(Execution.id == execution_id).first()
    if execution is None:
        raise HTTPException(status_code=404, detail="Execution not found.")
    return execution


@router.post("/{workflow_id}/execute", response_model=ExecutionResponse)
def execute_workflow(workflow_id: int, db: Session = Depends(get_db)):
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found.")

    if not workflow.nodes:
        raise HTTPException(status_code=400, detail="Workflow contains no nodes.")

    executor = WorkflowExecutor(db)

    try:
        return executor.execute(workflow)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {exc}") from exc
