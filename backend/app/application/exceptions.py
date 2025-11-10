from __future__ import annotations


class ApplicationError(Exception):
    """Generic application-layer error."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
