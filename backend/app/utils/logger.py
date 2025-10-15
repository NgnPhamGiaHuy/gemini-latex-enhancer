"""
Logger utility for the application.

Provides a simple stdout logger with a consistent format and INFO level by
default. Handlers are added once per logger name to avoid duplicate logs in
development reload scenarios.
"""

import logging
import sys
from typing import Optional


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
