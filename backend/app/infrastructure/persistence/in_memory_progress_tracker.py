from __future__ import annotations

from typing import Dict, Optional
from threading import Lock

from app.application.contracts.progress_tracker import ProgressTracker


class InMemoryProgressTracker(ProgressTracker):
    """Thread-safe in-memory progress tracker."""

    def __init__(self) -> None:
        self._progress: Dict[str, Dict] = {}
        self._lock = Lock()

    def init(self, session_id: str, total: int, message: str | None = None) -> None:
        with self._lock:
            self._progress[session_id] = {
                "total": max(total, 0),
                "current": 0,
                "status": "running",
                "message": message or "",
                "zip_path": None,
                "errors": 0,
            }

    def update(
        self, session_id: str, *, current: int | None = None, message: str | None = None
    ) -> None:
        with self._lock:
            state = self._progress.get(session_id)
            if not state:
                return
            if current is not None:
                state["current"] = max(0, min(current, state.get("total", 0)))
            if message is not None:
                state["message"] = message

    def increment(
        self, session_id: str, inc: int = 1, message: str | None = None
    ) -> None:
        with self._lock:
            state = self._progress.get(session_id)
            if not state:
                return
            state["current"] = min(state.get("current", 0) + inc, state.get("total", 0))
            if message is not None:
                state["message"] = message

    def mark_error(self, session_id: str) -> None:
        with self._lock:
            state = self._progress.get(session_id)
            if state:
                state["errors"] = state.get("errors", 0) + 1

    def complete(
        self, session_id: str, zip_path: str | None = None, message: str = "Completed"
    ) -> None:
        with self._lock:
            state = self._progress.get(session_id)
            if not state:
                return
            state["current"] = state.get("total", 0)
            state["status"] = "completed"
            state["message"] = message
            state["zip_path"] = zip_path

    def fail(self, session_id: str, message: str) -> None:
        with self._lock:
            self._progress[session_id] = {
                "total": 0,
                "current": 0,
                "status": "failed",
                "message": message,
                "zip_path": None,
                "errors": 0,
            }

    def get(self, session_id: str) -> Optional[Dict]:
        with self._lock:
            state = self._progress.get(session_id)
            return dict(state) if state else None
