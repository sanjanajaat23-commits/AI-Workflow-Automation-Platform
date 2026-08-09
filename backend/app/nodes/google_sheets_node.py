from __future__ import annotations

from backend.app.nodes.base_node import BaseNode
from backend.app.nodes.node_result import NodeResult


class GoogleSheetsNode(BaseNode):
    """Validate Google Sheets configuration.

    The connector itself is intentionally not enabled yet; this node keeps
    execution explicit instead of pretending a write succeeded.
    """

    @property
    def node_type(self) -> str:
        return "google_sheets"

    def validate(self) -> bool:
        config = self.node_data.config or {}
        if not config.get("spreadsheet_id"):
            raise ValueError("Google Sheets node requires a spreadsheet ID.")
        if not config.get("sheet_name"):
            raise ValueError("Google Sheets node requires a sheet name.")
        return True

    def execute(self, context):
        self.validate()
        raise RuntimeError(
            "Google Sheets execution is not connected yet. Configure a Google Sheets connector first."
        )
