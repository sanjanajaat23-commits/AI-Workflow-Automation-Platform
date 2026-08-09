from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class NodeResult:
    """
    Standard result returned by every workflow node.
    """

    success: bool = True

    output: Any = None

    message: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)

    logs: list[str] = field(default_factory=list)

    def add_log(self, message: str) -> None:
        self.logs.append(message)

    @classmethod
    def success_result(
        cls,
        output: Any = None,
        message: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> "NodeResult":

        return cls(
            success=True,
            output=output,
            message=message,
            metadata=metadata or {},
        )

    @classmethod
    def failure_result(
        cls,
        message: str,
        metadata: dict[str, Any] | None = None,
    ) -> "NodeResult":

        return cls(
            success=False,
            output=None,
            message=message,
            metadata=metadata or {},
        )