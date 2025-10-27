"""
Enhanced Session Logger utility for the application.

Provides comprehensive session logging capabilities including:
- JSON formatted logs for structured data
- Prompt logging for AI interactions
- Configurable log levels and formats
- File and console output options
- Session-based log management
"""

import json
import logging
import sys
import os
from datetime import datetime
from typing import Any, Dict, Optional, Union
from pathlib import Path


class JSONFormatter(logging.Formatter):
    """Custom formatter that outputs logs in JSON format."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add extra fields if present
        if hasattr(record, 'extra_data'):
            log_entry["data"] = record.extra_data
            
        return json.dumps(log_entry, ensure_ascii=False, indent=2)


class SessionPromptLogger:
    """Specialized session logger for AI prompt interactions."""
    
    def __init__(self, name: str = "session_prompt_logger"):
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup the session prompt logger with JSON formatting."""
        if not self.logger.handlers:
            from app.config import settings
            
            # Console handler for development
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
            
            # Use JSON formatter for structured logs
            json_formatter = JSONFormatter()
            console_handler.setFormatter(json_formatter)
            
            self.logger.addHandler(console_handler)
            self.logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
            
            # File handler for session logs
            session_log_dir = Path(settings.SESSION_LOG_DIR)
            session_log_dir.mkdir(exist_ok=True)
            
            file_handler = logging.FileHandler(
                session_log_dir / f"session_prompts_{datetime.now().strftime('%Y%m%d')}.log"
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(json_formatter)
            
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
        session_id: Optional[str] = None
    ):
        """Log a complete session prompt request in JSON format."""
        extra_data = {
            "prompt_type": prompt_type,
            "job_title": job_title,
            "job_description": job_description,
            "company_name": company_name,
            "slice_projects": slice_projects,
            "prompt_content": prompt_content,
            "prompt_length": prompt_length,
            "model_id": model_id,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }
        
        self.logger.info(
            f"Session AI Prompt Request - {prompt_type}",
            extra={"extra_data": extra_data}
        )
    
    def log_prompt_response(
        self,
        response_content: str,
        response_length: int,
        processing_time: float,
        model_id: str,
        session_id: Optional[str] = None,
        success: bool = True,
        error_message: Optional[str] = None
    ):
        """Log a session prompt response in JSON format."""
        extra_data = {
            "response_content": response_content,
            "response_length": response_length,
            "processing_time": processing_time,
            "model_id": model_id,
            "session_id": session_id,
            "success": success,
            "error_message": error_message,
            "timestamp": datetime.now().isoformat()
        }
        
        level = logging.INFO if success else logging.ERROR
        message = f"Session AI Prompt Response - {'Success' if success else 'Error'}"
        
        self.logger.log(
            level,
            message,
            extra={"extra_data": extra_data}
        )


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger bound to the given module name."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        # Create handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger


def get_json_logger(name: str) -> logging.Logger:
    """Return a logger configured for JSON output."""
    logger = logging.getLogger(f"{name}_json")
    
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # JSON formatter
        json_formatter = JSONFormatter()
        console_handler.setFormatter(json_formatter)
        
        logger.addHandler(console_handler)
        logger.setLevel(logging.INFO)
        
        # File handler
        from app.config import settings
        session_log_dir = Path(settings.SESSION_LOG_DIR)
        session_log_dir.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(
            session_log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(json_formatter)
        
        logger.addHandler(file_handler)
    
    return logger


def log_structured_data(
    logger: logging.Logger,
    message: str,
    data: Dict[str, Any],
    level: int = logging.INFO
):
    """Log structured data with the given logger."""
    logger.log(level, message, extra={"extra_data": data})


# Global session prompt logger instance
session_prompt_logger = SessionPromptLogger()
