from __future__ import annotations

from typing import Type

from backend.app.nodes.base_node import BaseNode


class NodeRegistry:
    """
    Registry that keeps track of all available node types.
    """

    def __init__(self):
        self._nodes: dict[str, Type[BaseNode]] = {}

    def register(
        self,
        node_type: str,
        node_class: Type[BaseNode],
    ) -> None:
        """
        Register a node class.
        """

        if node_type in self._nodes:
            raise ValueError(
                f"Node '{node_type}' is already registered."
            )

        self._nodes[node_type] = node_class

    def unregister(self, node_type: str) -> None:
        """
        Remove a node from the registry.
        """

        self._nodes.pop(node_type, None)

    def get(self, node_type: str) -> Type[BaseNode]:
        """
        Get the registered node class.
        """

        if node_type not in self._nodes:
            raise ValueError(
                f"Unknown node type '{node_type}'."
            )

        return self._nodes[node_type]

    def exists(self, node_type: str) -> bool:
        """
        Check if a node type is registered.
        """

        return node_type in self._nodes

    def available_nodes(self) -> list[str]:
        """
        Return all registered node types.
        """

        return sorted(self._nodes.keys())


# Global registry instance
node_registry = NodeRegistry()