from __future__ import annotations

import requests

from backend.app.nodes.base_node import BaseNode
from backend.app.nodes.node_result import NodeResult


class HTTPNode(BaseNode):
    """Execute an outbound HTTP request."""

    @property
    def node_type(self) -> str:
        return "http"

    def validate(self) -> bool:
        config = self.node_data.config or {}
        url = str(config.get("url", "")).strip()

        if not url:
            raise ValueError("HTTP node requires a URL.")

        method = str(config.get("method", "GET")).upper()
        if method not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
            raise ValueError(f"Unsupported HTTP method: {method}")

        return True

    def execute(self, context):
        self.validate()

        config = self.node_data.config or {}
        method = str(config.get("method", "GET")).upper()
        url = str(config["url"]).strip()
        headers = config.get("headers") or {}
        body = config.get("body") or {}
        timeout = max(1, int(config.get("timeout", 30)))

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=body if method != "GET" else None,
                timeout=timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(f"HTTP request failed: {exc}") from exc

        try:
            output = response.json()
        except ValueError:
            output = response.text

        return NodeResult.success_result(
            output=output,
            message="HTTP request successful.",
            metadata={"status_code": response.status_code},
        )
