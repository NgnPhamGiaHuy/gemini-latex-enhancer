"""
Progress Service.

Lightweight in-memory progress tracking per session for batch enhancements.
Thread-safe operations are implemented via a `threading.Lock`.
"""

from typing import Dict, Optional
from threading import Lock


class ProgressService:
    _progress: Dict[str, Dict] = {}
    _lock: Lock = Lock()

    @classmethod
    def init(cls, session_id: str, total: int, message: str = "") -> None:
        """Initialize progress state for a session.

        Args:
            session_id: Unique identifier for the batch job.
            total: Total number of units of work (e.g., jobs).
            message: Optional human-readable status message.
        """
        with cls._lock:
            cls._progress[session_id] = {
                "total": max(total, 0),
                "current": 0,
                "status": "running",
                "message": message,
                "zip_path": None,
                "errors": 0,
            }

    @classmethod
    def update(
        cls,
        session_id: str,
        current: Optional[int] = None,
        message: Optional[str] = None,
    ) -> None:
        """Update current count and/or message for a session.

        Args:
            session_id: Target session.
            current: Absolute current count to set.
            message: Optional status text.
        """
        with cls._lock:
            state = cls._progress.get(session_id)
            if not state:
                return
            if current is not None:
                state["current"] = max(0, min(current, state.get("total", 0)))
            if message is not None:
                state["message"] = message

    @classmethod
    def increment(
        cls, session_id: str, inc: int = 1, message: Optional[str] = None
    ) -> None:
        """Increment the current counter and optionally set a message.

        Args:
            session_id: Target session.
            inc: Amount to increase current by (defaults to 1).
            message: Optional status text to store.
        """
        with cls._lock:
            state = cls._progress.get(session_id)
            if not state:
                return
            state["current"] = min(state.get("current", 0) + inc, state.get("total", 0))
            if message is not None:
                state["message"] = message

    @classmethod
    def mark_error(cls, session_id: str) -> None:
        """Increment the error count for a session, if present."""
        with cls._lock:
            state = cls._progress.get(session_id)
            if state:
                state["errors"] = state.get("errors", 0) + 1

    @classmethod
    def complete(
        cls, session_id: str, zip_path: Optional[str] = None, message: str = "Completed"
    ) -> None:
        """Mark a session as completed, optionally attaching a result zip path.

        Args:
            session_id: Target session.
            zip_path: Relative path to a results archive.
            message: Final status message.
        """
        with cls._lock:
            state = cls._progress.get(session_id)
            if not state:
                return
            state["current"] = state.get("total", 0)
            state["status"] = "completed"
            state["message"] = message
            state["zip_path"] = zip_path

    @classmethod
    def fail(cls, session_id: str, message: str) -> None:
        """Mark a session as failed with a message, resetting counters."""
        with cls._lock:
            cls._progress[session_id] = {
                "total": 0,
                "current": 0,
                "status": "failed",
                "message": message,
                "zip_path": None,
                "errors": 0,
            }

    @classmethod
    def get(cls, session_id: str) -> Optional[Dict]:
        """Return a shallow copy of the session state for read-only access."""
        with cls._lock:
            state = cls._progress.get(session_id)
            return dict(state) if state else None
