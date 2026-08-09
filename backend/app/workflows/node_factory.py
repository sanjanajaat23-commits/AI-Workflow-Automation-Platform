from backend.app.nodes.ai_node import AINode
from backend.app.nodes.http_node import HTTPNode
from backend.app.nodes.google_sheets_node import GoogleSheetsNode


class NodeFactory:
    @staticmethod
    def get_node(node_type: str):
        node_type = node_type.lower()

        if node_type == "ai":
            return AINode

        if node_type == "http":
            return HTTPNode

        if node_type == "google_sheets":
            return GoogleSheetsNode

        # Start node doesn't execute any logic.
        if node_type == "start":
            return None

        raise ValueError(f"Unsupported node type: {node_type}")