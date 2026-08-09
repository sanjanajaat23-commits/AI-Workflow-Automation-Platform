from sqlalchemy.orm import Session

from backend.app.models.workflow import Workflow
from backend.app.models.workflow_node import WorkflowNode
from backend.app.models.workflow_connection import WorkflowConnection

from backend.app.crud.execution import update_execution_status
from backend.app.services.execution_log_service import add_log
from backend.app.workflows.executor import WorkflowExecutor


def run_workflow(
    db: Session,
    workflow_id: int,
    execution_id: int,
):

    workflow = (
        db.query(Workflow)
        .filter(Workflow.id == workflow_id)
        .first()
    )

    if workflow is None:

        update_execution_status(
            db=db,
            execution_id=execution_id,
            status="failed",
            error_message="Workflow not found.",
        )

        return

    nodes = (
        db.query(WorkflowNode)
        .filter(
            WorkflowNode.workflow_id == workflow_id
        )
        .all()
    )

    connections = (
        db.query(WorkflowConnection)
        .filter(
            WorkflowConnection.workflow_id == workflow_id
        )
        .all()
    )

    executor = WorkflowExecutor()

    try:

        add_log(
            db=db,
            execution_id=execution_id,
            message="Workflow execution started.",
        )

        result = executor.execute(
            nodes,
            connections,
        )

        add_log(
            db=db,
            execution_id=execution_id,
            message="Workflow execution completed.",
        )

        update_execution_status(
            db=db,
            execution_id=execution_id,
            status="completed",
            output_data=result,
        )

    except Exception as e:

        add_log(
            db=db,
            execution_id=execution_id,
            message=str(e),
            level="error",
        )

        update_execution_status(
            db=db,
            execution_id=execution_id,
            status="failed",
            error_message=str(e),
        )
