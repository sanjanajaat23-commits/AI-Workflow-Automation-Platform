from __future__ import annotations


class AIService:
    """
    Central AI service.

    This class will become the single entry point for
    all AI operations in the platform.
    """

    def __init__(self):
        self._provider = None

    def set_provider(self, provider):
        """
        Register the active AI provider.
        """
        self._provider = provider

    def generate(
        self,
        prompt: str,
        **kwargs,
    ) -> str:

        if self._provider is None:
            raise RuntimeError(
                "No AI provider has been configured."
            )

        return self._provider.generate(
            prompt,
            **kwargs,
        )


ai_service = AIService()