from fastapi import APIRouter, HTTPException
from openai import OpenAI
from pydantic import BaseModel, Field

from backend.app.core.config import settings

router = APIRouter()


class AssistantRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=4000)


class AssistantResponse(BaseModel):
    response: str
    mode: str
    model: str


@router.get("/status")
def ai_status():
    return {
        "configured": bool(settings.OPENAI_API_KEY),
        "demo_mode": settings.DEMO_MODE,
        "model": settings.OPENAI_MODEL,
    }


@router.post("/assistant", response_model=AssistantResponse)
def assistant(request: AssistantRequest):
    if settings.DEMO_MODE or not settings.OPENAI_API_KEY:
        return AssistantResponse(
            response=(
                "Demo AI plan for: " + request.prompt + "\n\n"
                "Suggested workflow:\n"
                "1. Trigger — capture the incoming business event.\n"
                "2. Validate — check required fields and business rules.\n"
                "3. Action — update the connected system and send the required notification.\n"
                "4. Condition — branch for exceptions such as delays, missing data, or failed delivery.\n"
                "5. Log — record the result for audit and monitoring.\n\n"
                "Next step: open Workflow Builder and create the trigger, action, condition, and log nodes."
            ),
            mode="demo",
            model=settings.OPENAI_MODEL,
        )

    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        completion = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the workflow copilot for an enterprise automation platform. "
                        "Translate the user's business process into a practical automation plan. "
                        "Use clear numbered steps, identify trigger, actions, conditions, "
                        "integrations, exception handling, and a short implementation checklist. "
                        "Do not claim an integration exists unless the user states it."
                    ),
                },
                {"role": "user", "content": request.prompt},
            ],
        )
        text = completion.choices[0].message.content or "No AI response was returned."
        return AssistantResponse(response=text, mode="openai", model=settings.OPENAI_MODEL)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI provider error: {exc}") from exc
