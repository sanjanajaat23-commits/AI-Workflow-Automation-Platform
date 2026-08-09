from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseLLM(ABC):
    """
    Abstract base class for all Large Language Models.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Name of the provider.
        Example:
            openai
            gemini
            claude
            ollama
        """
        raise NotImplementedError

    @abstractmethod
    def generate(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """
        Generate a response from the LLM.
        """
        raise NotImplementedError