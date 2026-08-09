from sqlalchemy.orm import Session

from backend.app.crud.execution import (
    create_execution,
    get_execution,
    get_workflow_executions,
    update_execution_status,
)
from backend.app.crud.workflow import get_workflow


class ExecutionNotFoundError(Exception):
    pass


class WorkflowNotFoundError(Exception):
    pass


def start_execution(
    db: Session,
    workflow_id: int,
    input_data: dict | None = None,
):
    workflow = get_workflow(db, workflow_id)

    if workflow is None:
        raise WorkflowNotFoundError("Workflow not found.")

    return create_execution(db, workflow_id, input_data)


def get_execution_by_id(
    db: Session,
    execution_id: int,
):
    execution = get_execution(db, execution_id)

    if execution is None:
        raise ExecutionNotFoundError("Execution not found.")

    return execution


def list_executions(
    db: Session,
    workflow_id: int,
):
    return get_workflow_executions(db, workflow_id)


def mark_execution_completed(
    db: Session,
    execution,
    output_data: dict | None = None,
):
    return update_execution_status(
        db,
        execution,
        status="completed",
        output_data=output_data,
    )


def mark_execution_failed(
    db: Session,
    execution,
    error_message: str,
):
    return update_execution_status(
        db,
        execution,
        status="failed",
        error_message=error_message,
    )
