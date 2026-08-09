from __future__ import annotations

from typing import Dict, List


class ConversationMemory:
    """
    Simple in-memory conversation history.

    Future versions can replace this with:
    - Redis
    - PostgreSQL
    - Vector Database
    - LangGraph Memory
    """

    def __init__(self):
        self._messages: List[Dict[str, str]] = []

    def add_user_message(
        self,
        message: str,
    ) -> None:

        self._messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

    def add_assistant_message(
        self,
        message: str,
    ) -> None:

        self._messages.append(
            {
                "role": "assistant",
                "content": message,
            }
        )

    def clear(self) -> None:
        self._messages.clear()

    def get_messages(self) -> List[Dict[str, str]]:
        return list(self._messages)