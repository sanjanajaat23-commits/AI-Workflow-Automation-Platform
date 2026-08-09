import re
from typing import Any


class VariableParser:
    """
    Replaces variables like:

    {{start.user}}
    {{http.body}}
    {{ai.response}}
    """

    VARIABLE_PATTERN = r"\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}"

    @classmethod
    def parse(cls, value: Any, context: dict):

        if not isinstance(value, str):
            return value

        matches = re.findall(
            cls.VARIABLE_PATTERN,
            value,
        )

        for match in matches:

            current = context

            for part in match.split("."):

                if isinstance(current, dict):
                    current = current.get(part)
                else:
                    current = None
                    break

            if current is None:
                current = ""

            value = value.replace(
                "{{" + match + "}}",
                str(current),
            )

        return value