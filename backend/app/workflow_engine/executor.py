from __future__ import annotations

import logging

from backend.app.nodes.node_result import NodeResult
from backend.app.workflow_engine.context import WorkflowExecutionContext
from backend.app.workflow_engine.exceptions import NodeExecutionError
from backend.app.workflow_engine.result import WorkflowExecutionResult
from backend.app.workflow_engine.state import WorkflowExecutionState

logger = logging.getLogger(__name__)


class WorkflowExecutor:
    """
    Executes workflow nodes sequentially.

    Future versions will support:
    - Parallel execution
    - Conditional branches
    - Retry policies
    - Queue execution
    - Human approval nodes
    """

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def execute(
        self,
        workflow,
        context: WorkflowExecutionContext,
        result: WorkflowExecutionResult,
    ) -> WorkflowExecutionResult:

        result.status = WorkflowExecutionState.RUNNING

        logger.info(
            "Starting workflow execution: %s",
            workflow.id,
        )

        try:

            for workflow_node in workflow.nodes:

                context.push_node(str(workflow_node.id))

                logger.info(
                    "Executing node %s (%s)",
                    workflow_node.id,
                    workflow_node.node_type,
                )

                node = self.node_factory.create(workflow_node)

                node_result: NodeResult = node.execute(context)

                if not node_result.success:
                    raise NodeExecutionError(
                        str(workflow_node.id),
                        node_result.message,
                    )

                context.set_node_output(
                    str(workflow_node.id),
                    node_result.output,
                )

                result.set_output(
                    str(workflow_node.id),
                    node_result.output,
                )

                result.logs.extend(node_result.logs)

                result.add_log(
                    f"Node '{workflow_node.name}' executed successfully."
                )

                context.pop_node()

            result.status = WorkflowExecutionState.SUCCESS

            logger.info(
                "Workflow %s completed successfully.",
                workflow.id,
            )

        except Exception as exc:

            logger.exception(
                "Workflow execution failed."
            )

            result.status = WorkflowExecutionState.FAILED

            result.add_error(str(exc))

            raise

        return result