from datetime import datetime

from backend.app.workflow_engine.context import WorkflowExecutionContext
from backend.app.workflow_engine.executor import WorkflowExecutor
from backend.app.workflow_engine.result import WorkflowExecutionResult
from backend.app.workflow_engine.state import WorkflowExecutionState
from backend.app.workflow_engine.validator import WorkflowValidator


class WorkflowEngine:
    """
    Main workflow execution engine.

    Responsibilities:
    - Validate workflow
    - Create execution context
    - Execute workflow
    - Return execution result
    """

    def __init__(self, node_factory):
        self.executor = WorkflowExecutor(node_factory)

    def execute(self, workflow, execution_id: int):

        WorkflowValidator.validate(workflow)

        context = WorkflowExecutionContext(
            workflow_id=workflow.id,
            execution_id=execution_id,
        )

        result = WorkflowExecutionResult(
            workflow_id=workflow.id,
            execution_id=execution_id,
            status=WorkflowExecutionState.PENDING,
            started_at=datetime.utcnow(),
        )

        result = self.executor.execute(
            workflow=workflow,
            context=context,
            result=result,
        )

        result.finished_at = datetime.utcnow()

        result.execution_time = (
            result.finished_at - result.started_at
        ).total_seconds()

        return result