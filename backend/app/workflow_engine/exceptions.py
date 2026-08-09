class WorkflowEngineError(Exception):
    """
    Base exception for the workflow engine.
    """


class WorkflowValidationError(WorkflowEngineError):
    """
    Raised when a workflow is invalid.
    """


class WorkflowExecutionError(WorkflowEngineError):
    """
    Raised when workflow execution fails.
    """


class NodeExecutionError(WorkflowEngineError):
    """
    Raised when a node fails during execution.
    """

    def __init__(self, node_id: str, message: str):
        self.node_id = node_id
        super().__init__(f"Node '{node_id}' failed: {message}")


class NodeNotFoundError(WorkflowEngineError):
    """
    Raised when a node cannot be found.
    """

    def __init__(self, node_id: str):
        self.node_id = node_id
        super().__init__(f"Node '{node_id}' not found.")


class CircularWorkflowError(WorkflowEngineError):
    """
    Raised when a circular dependency is detected.
    """


class WorkflowTimeoutError(WorkflowEngineError):
    """
    Raised when workflow execution exceeds the configured timeout.
    """