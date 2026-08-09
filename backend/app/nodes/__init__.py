from backend.app.nodes.registry import node_registry

from backend.app.nodes.ai_node import AINode
from backend.app.nodes.http_node import HTTPNode
from backend.app.nodes.google_sheets_node import GoogleSheetsNode


def register_builtin_nodes():
    """
    Register all built-in workflow nodes.
    Safe to call multiple times.
    """

    nodes = [
        ("ai", AINode),
        ("http", HTTPNode),
        ("google_sheets", GoogleSheetsNode),
    ]

    for node_type, node_class in nodes:
        if not node_registry.exists(node_type):
            node_registry.register(
                node_type,
                node_class,
            )