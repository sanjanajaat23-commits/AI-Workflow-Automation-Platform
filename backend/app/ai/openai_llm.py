from __future__ import annotations

import os

from openai import OpenAI

from backend.app.ai.llm import BaseLLM
from backend.app.ai.prompt import PromptBuilder
from backend.app.core.config import settings


class OpenAILLM(BaseLLM):
    """
    OpenAI implementation of the BaseLLM interface.
    """

    def __init__(self):
        api_key = (settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY", "")).strip()
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured. Add it to backend/.env and restart the backend."
            )
        self.client = OpenAI(api_key=api_key)

    @property
    def provider_name(self) -> str:
        return "openai"

    def generate(
        self,
        prompt: str,
        **kwargs,
    ) -> str:

        builder = PromptBuilder()

        messages = (
            builder
            .system(
                kwargs.get(
                    "system_prompt",
                    "You are a helpful AI assistant.",
                )
            )
            .user(prompt)
            .build()
        )

        response = self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=kwargs.get(
                "temperature",
                0.7,
            ),
            max_tokens=kwargs.get(
                "max_tokens",
                1000,
            ),
        )

        return response.choices[0].message.content or ""