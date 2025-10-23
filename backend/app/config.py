"""
Configuration settings for the CV Enhancement API.

Loads environment variables via `python-dotenv` and exposes a typed `Settings`
object for application-wide configuration (AI, LaTeX, storage, CORS).
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
# Look for .env in the project root (two levels up from this file)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


class Settings:
    """Application settings container with sane defaults."""

    # API Configuration
    API_TITLE: str = "CV Enhancement API"
    API_VERSION: str = "1.0.0"

    # AI Service Configuration
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    AI_MODEL: str = os.getenv("AI_MODEL", "gemini-2.5-flash")
    USE_ADVANCED_PROMPT: bool = (
        os.getenv("USE_ADVANCED_PROMPT", "true").lower() == "true"
    )

    # File Storage Configuration
    UPLOAD_DIR: str = "uploads"
    OUTPUT_DIR: str = "outputs"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB

    # LaTeX Configuration
    LATEX_TIMEOUT: int = 30  # seconds

    # CORS Configuration
    ALLOWED_ORIGINS: list = (
        os.getenv("ALLOWED_ORIGINS", "").split(",")
        if os.getenv("ALLOWED_ORIGINS")
        else ["http://localhost:3000", "http://127.0.0.1:3000"]
    )


settings = Settings()
