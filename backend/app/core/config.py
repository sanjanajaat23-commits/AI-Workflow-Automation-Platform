import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_DIR = BACKEND_DIR.parent

# Load the local backend environment explicitly. This makes local Windows
# development reliable regardless of the current working directory.
load_dotenv(BACKEND_DIR / ".env", override=False)
load_dotenv(PROJECT_DIR / ".env", override=False)


class Settings(BaseSettings):
    APP_NAME: str = "AI Workflow Automation Platform"
    APP_VERSION: str = "2.3.0"
    DEBUG: bool = True

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    DATABASE_URL: str = "sqlite:///./backend/ai_workflow.db"
    SECRET_KEY: str = "dev-secret-key-change-this-locally"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REDIS_URL: str = "redis://localhost:6379/0"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4.1-mini"
    # Demo mode keeps the project runnable without OpenAI credits.
    # Set DEMO_MODE=false locally to use the real OpenAI API.
    DEMO_MODE: bool = True
    CORS_ORIGINS: str = (
        "http://localhost:5173,http://localhost:5174,http://localhost:5175"
    )

    model_config = SettingsConfigDict(
        env_file=(BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
