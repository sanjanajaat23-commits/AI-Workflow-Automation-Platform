from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from backend.app.workflow_engine.state import WorkflowExecutionState


@dataclass
class WorkflowExecutionResult:
    """
    Standard result returned after executing a workflow.
    """

    workflow_id: int
    execution_id: int

    status: WorkflowExecutionState

    started_at: datetime
    finished_at: datetime | None = None

    outputs: dict[str, Any] = field(default_factory=dict)

    errors: list[str] = field(default_factory=list)

    logs: list[str] = field(default_factory=list)

    execution_time: float = 0.0

    metadata: dict[str, Any] = field(default_factory=dict)

    def add_log(self, message: str) -> None:
        self.logs.append(message)

    def add_error(self, error: str) -> None:
        self.errors.append(error)

    def set_output(self, key: str, value: Any) -> None:
        self.outputs[key] = value

    @property
    def success(self) -> bool:
        return self.status == WorkflowExecutionState.SUCCESS