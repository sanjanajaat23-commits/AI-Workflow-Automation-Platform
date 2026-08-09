from __future__ import annotations

from backend.app.ai.openai_llm import OpenAILLM
from backend.app.core.config import settings
from backend.app.nodes.base_node import BaseNode
from backend.app.nodes.node_result import NodeResult


class AINode(BaseNode):
    """AI node with a local demo mode and optional OpenAI execution."""

    @property
    def node_type(self) -> str:
        return "ai"

    def validate(self) -> bool:
        config = self.node_data.config

        if not str(config.get("prompt", "")).strip():
            raise ValueError("AI node requires a 'prompt' field.")

        return True

    def execute(self, context):
        self.validate()

        prompt = str(self.node_data.config["prompt"]).strip()

        # Demo mode is enabled by default so the public GitHub project can be
        # executed without an OpenAI account, API key, or API credits.
        if settings.DEMO_MODE:
            response = (
                "Demo AI response: workflow executed successfully. "
                f"Prompt received: {prompt}"
            )

            return NodeResult.success_result(
                output={"response": response},
                message="AI node executed successfully in demo mode.",
                metadata={"provider": "demo", "demo_mode": True},
            )

        llm = OpenAILLM()
        response = llm.generate(prompt)

        return NodeResult.success_result(
            output={"response": response},
            message="AI node executed successfully.",
            metadata={"provider": "openai", "demo_mode": False},
        )
