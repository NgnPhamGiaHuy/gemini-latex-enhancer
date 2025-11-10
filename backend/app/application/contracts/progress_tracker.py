from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Optional


class ProgressTracker(ABC):
    """Track status of asynchronous/batch operations."""

    @abstractmethod
    def init(self, session_id: str, total: int, message: str | None = None) -> None: ...

    @abstractmethod
    def update(
        self, session_id: str, *, current: int | None = None, message: str | None = None
    ) -> None: ...

    @abstractmethod
    def increment(
        self, session_id: str, inc: int = 1, message: str | None = None
    ) -> None: ...

    @abstractmethod
    def mark_error(self, session_id: str) -> None: ...

    @abstractmethod
    def complete(
        self, session_id: str, zip_path: str | None = None, message: str = "Completed"
    ) -> None: ...

    @abstractmethod
    def fail(self, session_id: str, message: str) -> None: ...

    @abstractmethod
    def get(self, session_id: str) -> Optional[Dict]: ...
