from __future__ import annotations

from typing import Dict, List


class PromptBuilder:
    """
    Utility class for constructing prompts.
    """

    def __init__(self):
        self._system_prompt = ""
        self._messages: List[Dict[str, str]] = []

    def system(self, prompt: str):
        self._system_prompt = prompt
        return self

    def user(self, prompt: str):
        self._messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )
        return self

    def assistant(self, prompt: str):
        self._messages.append(
            {
                "role": "assistant",
                "content": prompt,
            }
        )
        return self

    def build(self) -> List[Dict[str, str]]:
        messages = []

        if self._system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": self._system_prompt,
                }
            )

        messages.extend(self._messages)

        return messages