from sqlalchemy.orm import Session

from backend.app.crud.execution import (
    create_execution,
    update_execution_status,
)
from backend.app.crud.execution_log import create_log
from backend.app.models.workflow import Workflow
from backend.app.nodes import register_builtin_nodes
from backend.app.nodes.node_factory import NodeFactory


class WorkflowExecutor:
    def __init__(self, db: Session):
        self.db = db
        register_builtin_nodes()
        self.factory = NodeFactory()

    def validate(self, workflow: Workflow) -> None:
        for node in sorted(workflow.nodes, key=lambda item: item.position_x):
            if node.node_type.lower() == "start":
                continue

            runner = self.factory.create(node)
            runner.validate()

    def execute(self, workflow: Workflow, input_data: dict | None = None):
        input_data = input_data or {}
        self.validate(workflow)

        execution = create_execution(
            db=self.db,
            workflow_id=workflow.id,
            input_data=input_data,
        )

        update_execution_status(
            db=self.db,
            execution=execution,
            status="running",
        )

        context = {"webhook": input_data}

        try:
            nodes = sorted(
                workflow.nodes,
                key=lambda node: node.position_x,
            )

            for node in nodes:
                if node.node_type.lower() == "start":
                    context[node.node_key] = {}
                    continue

                runner = self.factory.create(node)
                node_result = runner.execute(context)
                context[node.node_key] = node_result.output

                create_log(
                    db=self.db,
                    execution_id=execution.id,
                    message=f"{node.name} executed.",
                    level="info",
                )

            return update_execution_status(
                db=self.db,
                execution=execution,
                status="completed",
                output_data=context,
            )

        except Exception as exc:
            create_log(
                db=self.db,
                execution_id=execution.id,
                message=str(exc),
                level="error",
            )
            update_execution_status(
                db=self.db,
                execution=execution,
                status="failed",
                error_message=str(exc),
            )
            raise
