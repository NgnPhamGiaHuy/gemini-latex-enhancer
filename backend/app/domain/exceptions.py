from __future__ import annotations


class DomainValidationError(ValueError):
    """Raised when domain-level validation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
