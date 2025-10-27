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

    # Session Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "text")  # "text" or "json"
    ENABLE_PROMPT_LOGGING: bool = (
        os.getenv("ENABLE_PROMPT_LOGGING", "true").lower() == "true"
    )
    SESSION_LOG_DIR: str = os.getenv("SESSION_LOG_DIR", "logs")
    
    # Session Log Cleanup Configuration
    CLEANUP_SESSION_LOGS_ON_STARTUP: bool = (
        os.getenv("CLEANUP_SESSION_LOGS_ON_STARTUP", "true").lower() == "true"
    )
    CLEANUP_SESSION_LOGS_ON_SHUTDOWN: bool = (
        os.getenv("CLEANUP_SESSION_LOGS_ON_SHUTDOWN", "true").lower() == "true"
    )
    SESSION_LOG_RETENTION_DAYS: int = int(os.getenv("SESSION_LOG_RETENTION_DAYS", "7"))

    # Session Output Configuration
    SESSION_OUTPUT_DIR: str = os.getenv("SESSION_OUTPUT_DIR", "outputs")
    
    # Session Output Cleanup Configuration
    CLEANUP_SESSION_OUTPUTS_ON_STARTUP: bool = (
        os.getenv("CLEANUP_SESSION_OUTPUTS_ON_STARTUP", "true").lower() == "true"
    )
    CLEANUP_SESSION_OUTPUTS_ON_SHUTDOWN: bool = (
        os.getenv("CLEANUP_SESSION_OUTPUTS_ON_SHUTDOWN", "true").lower() == "true"
    )
    SESSION_OUTPUT_RETENTION_DAYS: int = int(os.getenv("SESSION_OUTPUT_RETENTION_DAYS", "7"))

    # File Storage Configuration
    UPLOAD_DIR: str = "uploads"
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
