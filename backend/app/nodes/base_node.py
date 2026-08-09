from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from backend.app.workflow_engine.context import WorkflowExecutionContext


class BaseNode(ABC):
    """
    Base class for every workflow node.

    Every node in the platform must inherit from this class.
    """

    def __init__(self, node_data: Any):
        self.node_data = node_data

    @property
    @abstractmethod
    def node_type(self) -> str:
        """
        Returns the node type.
        Example:
            http
            ai
            email
        """
        raise NotImplementedError

    @abstractmethod
    def execute(
        self,
        context: WorkflowExecutionContext,
    ) -> Any:
        """
        Execute the node.

        Returns the output that will be passed to the next node.
        """
        raise NotImplementedError

    def validate(self) -> bool:
        """
        Validate node configuration.
        Override in subclasses if needed.
        """
        return True