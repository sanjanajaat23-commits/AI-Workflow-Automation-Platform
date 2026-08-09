from typing import Any


class WorkflowContext:
    def __init__(self):
        self.data: dict[str, Any] = {}

    def set(self, key: str, value: Any):
        self.data[key] = value

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def to_dict(self):
        return self.data
