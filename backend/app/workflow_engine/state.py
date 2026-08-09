from enum import Enum


class WorkflowExecutionState(str, Enum):
    """
    Represents the lifecycle state of a workflow execution.
    """

    PENDING = "PENDING"
    VALIDATING = "VALIDATING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    WAITING = "WAITING"
    RETRYING = "RETRYING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    TIMEOUT = "TIMEOUT"