from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class WorkflowExecutionContext:
    """
    Shared runtime context passed between every node during workflow execution.
    """

    workflow_id: int
    execution_id: int

    started_at: datetime = field(default_factory=datetime.utcnow)

    current_node: str | None = None

    variables: dict[str, Any] = field(default_factory=dict)

    node_outputs: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    execution_stack: list[str] = field(default_factory=list)

    def set_variable(self, key: str, value: Any) -> None:
        self.variables[key] = value

    def get_variable(self, key: str, default: Any = None) -> Any:
        return self.variables.get(key, default)

    def set_node_output(self, node_id: str, output: Any) -> None:
        self.node_outputs[node_id] = output

    def get_node_output(self, node_id: str) -> Any:
        return self.node_outputs.get(node_id)

    def push_node(self, node_id: str) -> None:
        self.execution_stack.append(node_id)
        self.current_node = node_id

    def pop_node(self) -> str | None:
        if not self.execution_stack:
            self.current_node = None
            return None

        node = self.execution_stack.pop()

        self.current_node = (
            self.execution_stack[-1]
            if self.execution_stack
            else None
        )

        return node

    @property
    def current_variables(self) -> dict[str, Any]:
        return self.variables

    @property
    def outputs(self) -> dict[str, Any]:
        return self.node_outputs