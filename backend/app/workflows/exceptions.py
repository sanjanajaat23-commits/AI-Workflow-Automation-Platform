class WorkflowExecutionError(Exception):
    """Base exception for workflow execution."""
    pass


class NodeExecutionError(WorkflowExecutionError):
    """Raised when a workflow node fails."""
    pass


class NodeNotFoundError(WorkflowExecutionError):
    """Raised when a node cannot be found."""
    pass


class InvalidWorkflowError(WorkflowExecutionError):
    """Raised when the workflow structure is invalid."""
    pass
