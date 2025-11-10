from __future__ import annotations

from abc import ABC, abstractmethod


class CleanupService(ABC):
    """Abstract contract for file and directory cleanup operations."""

    @abstractmethod
    def cleanup_uploads_directory(self) -> None:
        """Remove all files and subfolders under the uploads directory."""
        ...

    @abstractmethod
    def cleanup_session_outputs_directory(self) -> None:
        """Remove all files and subfolders under the session outputs directory."""
        ...

    @abstractmethod
    def cleanup_session_logs_directory(self) -> None:
        """Remove all session log files from the session logs directory."""
        ...

    @abstractmethod
    def cleanup_old_session_outputs(self, days_to_keep: int = 7) -> None:
        """Remove session output files older than specified days."""
        ...

    @abstractmethod
    def cleanup_old_session_logs(self, days_to_keep: int = 7) -> None:
        """Remove session log files older than specified days."""
        ...

    @abstractmethod
    def cleanup_all_directories(self) -> None:
        """Clean uploads, session outputs, and session logs directories."""
        ...

    @abstractmethod
    def ensure_directories_exist(self) -> None:
        """Ensure uploads, session outputs, and session logs directories exist."""
        ...
