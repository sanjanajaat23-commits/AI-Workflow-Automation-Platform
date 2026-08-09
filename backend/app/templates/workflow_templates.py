from typing import Dict, List

TEMPLATES: Dict[str, dict] = {
    "ai_chatbot": {
        "id": "ai_chatbot",
        "name": "AI Chatbot",
        "description": "Simple AI chatbot workflow",
        "nodes": [
            {
                "type": "Start",
                "label": "Start",
                "config": {},
            },
            {
                "type": "AI",
                "label": "AI",
                "config": {
                    "prompt": "Hello! How can I help you today?"
                },
            },
        ],
        "edges": [
            {
                "source": "Start",
                "target": "AI",
            }
        ],
    },

    "lead_generation": {
        "id": "lead_generation",
        "name": "Lead Generation",
        "description": "Collect leads and save to Google Sheets",
        "nodes": [
            {
                "type": "Start",
                "label": "Start",
                "config": {},
            },
            {
                "type": "HTTP",
                "label": "HTTP",
                "config": {
                    "url": "",
                    "method": "GET",
                },
            },
            {
                "type": "Google Sheets",
                "label": "Google Sheets",
                "config": {},
            },
        ],
        "edges": [
            {
                "source": "Start",
                "target": "HTTP",
            },
            {
                "source": "HTTP",
                "target": "Google Sheets",
            },
        ],
    },

    "email_automation": {
        "id": "email_automation",
        "name": "Email Automation",
        "description": "AI generated email sender",
        "nodes": [
            {
                "type": "Start",
                "label": "Start",
                "config": {},
            },
            {
                "type": "AI",
                "label": "AI",
                "config": {
                    "prompt": "Generate a professional email."
                },
            },
            {
                "type": "Email",
                "label": "Email",
                "config": {},
            },
        ],
        "edges": [
            {
                "source": "Start",
                "target": "AI",
            },
            {
                "source": "AI",
                "target": "Email",
            },
        ],
    },
}


def get_templates() -> List[dict]:
    return list(TEMPLATES.values())


def get_template(template_id: str):
    return TEMPLATES.get(template_id)