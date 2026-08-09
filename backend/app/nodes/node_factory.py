from __future__ import annotations

from backend.app.nodes.base_node import BaseNode
from backend.app.nodes.registry import node_registry


class NodeFactory:
    """
    Creates workflow node instances using the global registry.
    """

    def create(self, workflow_node) -> BaseNode:
        """
        Create a node instance from a workflow node model.
        """

        node_type = workflow_node.node_type.lower()

        node_class = node_registry.get(node_type)

        return node_class(workflow_node)