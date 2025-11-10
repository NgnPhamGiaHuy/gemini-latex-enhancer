"""
Enhanced session logger utility for the application.

Provides comprehensive session logging capabilities, including:
- JSON‑formatted logs for structured data
- Prompt logging for AI interactions
- Configurable log levels and formats
- File and console output options with rotation
- Session‑based log management
- Sensitive‑data redaction
"""

import sys
import json
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

from app.utils.data_redaction import (
    sanitize_log_data,
    redact_prompt_content,
    redact_job_description,
    redact_latex_content,
)


class JSONFormatter(logging.Formatter):
    """Custom formatter that outputs logs in JSON format."""

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as JSON with proper `extra_data` handling."""
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields if present — handle both direct attribute and dict access
        extra_data = getattr(record, "extra_data", None)
        if extra_data is None:
            # Try to get from __dict__ if not directly accessible
            extra_data = record.__dict__.get("extra_data", None)

        if extra_data is not None:
            # Sanitize sensitive data before logging
            if isinstance(extra_data, dict):
                log_entry["data"] = sanitize_log_data(extra_data)
            else:
                log_entry["data"] = extra_data

        # Add any other extra fields (excluding internal logging fields)
        excluded_fields = {
            "name",
            "msg",
            "args",
            "created",
            "filename",
            "funcName",
            "levelname",
            "levelno",
            "lineno",
            "module",
            "msecs",
            "message",
            "pathname",
            "process",
            "processName",
            "relativeCreated",
            "thread",
            "threadName",
            "exc_info",
            "exc_text",
            "stack_info",
            "extra_data",
        }

        for key, value in record.__dict__.items():
            if key not in excluded_fields and not key.startswith("_"):
                log_entry[key] = value

        return json.dumps(log_entry, ensure_ascii=False, indent=2)


class SessionPromptLogger:
    """Specialized session logger for AI‑prompt interactions with data redaction."""

    def __init__(self, name: str = "session_prompt_logger"):
        self.logger = logging.getLogger(name)
        self._setup_logger()

    def _setup_logger(self):
        """Configure the session‑prompt logger with JSON formatting and log rotation."""
        if not self.logger.handlers:
            from app.config import settings

            log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

            # Console handler for development
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)

            # Use JSON formatter for structured logs
            json_formatter = JSONFormatter()
            console_handler.setFormatter(json_formatter)

            self.logger.addHandler(console_handler)
            self.logger.setLevel(log_level)

            # File handler with rotation for session logs
            session_log_dir = Path(settings.SESSION_LOG_DIR)
            session_log_dir.mkdir(exist_ok=True)

            # Use TimedRotatingFileHandler for daily rotation with 7‑day retention
            log_file = session_log_dir / "session_prompts.log"
            file_handler = TimedRotatingFileHandler(
                filename=str(log_file),
                when="midnight",
                interval=1,
                backupCount=settings.SESSION_LOG_RETENTION_DAYS,
                encoding="utf-8",
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(json_formatter)
            file_handler.suffix = "%Y%m%d"  # Format: session_prompts.log.20241215

            self.logger.addHandler(file_handler)

    def log_prompt_request(
        self,
        prompt_type: str,
        job_title: str,
        job_description: str,
        company_name: str,
        slice_projects: bool,
        prompt_content: str,
        prompt_length: int,
        model_id: str,
        session_id: Optional[str] = None,
    ):
        """Log a complete session‑prompt request with redacted sensitive data.

        Note: `prompt_content` and `job_description` are redacted to protect privacy.
        Only metadata and previews are logged.
        """
        # Redact sensitive content
        redacted_prompt = redact_prompt_content(prompt_content)
        redacted_job_desc = redact_job_description(job_description)

        extra_data = {
            "prompt_type": prompt_type,
            "job_title": job_title,  # Job title is usually safe to log
            "job_description": redacted_job_desc,  # Redacted
            "company_name": company_name,
            "slice_projects": slice_projects,
            "prompt_content": redacted_prompt,  # Redacted - only structure/preview
            "prompt_length": prompt_length,
            "model_id": model_id,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
        }

        self.logger.info(
            f"Session AI Prompt Request - {prompt_type} | Model: {model_id} | Session: {session_id or 'N/A'}",
            extra={"extra_data": extra_data},
        )

    def log_prompt_response(
        self,
        response_content: str,
        response_length: int,
        processing_time: float,
        model_id: str,
        session_id: Optional[str] = None,
        success: bool = True,
        error_message: Optional[str] = None,
    ):
        """Log a session‑prompt response with redacted content.

        Note: `response_content` is redacted to protect privacy.
        Only metadata, structure, and previews are logged.
        """
        # Redact response content (likely contains LaTeX/CV data)
        redacted_response = (
            redact_latex_content(response_content) if response_content else None
        )

        extra_data = {
            "response_content": redacted_response,  # Redacted - only structure/preview
            "response_length": response_length,
            "processing_time": round(processing_time, 3),  # Round to 3 decimal places
            "model_id": model_id,
            "session_id": session_id,
            "success": success,
            "error_message": (
                error_message[:200] if error_message else None
            ),  # Truncate errors
            "timestamp": datetime.now().isoformat(),
        }

        level = logging.INFO if success else logging.ERROR
        status = "Success" if success else "Error"
        message = f"Session AI Prompt Response - {status} | Model: {model_id} | Time: {processing_time:.2f}s | Session: {session_id or 'N/A'}"

        self.logger.log(level, message, extra={"extra_data": extra_data})


def get_logger(name: str, enable_file_logging: bool = True) -> logging.Logger:
    """Return a configured logger bound to the given module name.

    Args:
        name: Logger name (typically __name__)
        enable_file_logging: If True, also write to a log file with rotation

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        from app.config import settings

        # Get log level from settings
        log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)

        # Create formatter — use JSON if LOG_FORMAT is json, otherwise text
        if settings.LOG_FORMAT.lower() == "json":
            formatter = JSONFormatter()
        else:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.setLevel(log_level)

        # Add file handler if enabled
        if enable_file_logging:
            log_dir = Path(settings.SESSION_LOG_DIR)
            log_dir.mkdir(exist_ok=True)

            # Sanitize logger name for filename
            safe_name = name.replace(".", "_").replace("/", "_")
            log_file = log_dir / f"{safe_name}.log"

            # Use RotatingFileHandler with 10MB max size, 5 backups
            file_handler = RotatingFileHandler(
                filename=str(log_file),
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
                encoding="utf-8",
            )
            file_handler.setLevel(logging.DEBUG)  # File always logs DEBUG and above
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger


# Global session prompt logger instance
session_prompt_logger = SessionPromptLogger()
