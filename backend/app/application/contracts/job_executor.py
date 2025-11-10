"""
Job executor contract for background job execution.

Follows SOLID principles:
- Interface Segregation: Single-purpose interface for job execution
- Dependency Inversion: Use cases depend on abstraction, not concrete implementation
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Any


class JobExecutor(ABC):
    """Execute jobs in the background, allowing progress updates to be visible."""

    @abstractmethod
    def execute_in_background(
        self,
        job_fn: Callable[[], Any],
        *,
        on_complete: Callable[[Any], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
    ) -> None:
        """Execute a job function in the background.

        Args:
            job_fn: The function to execute (no arguments).
            on_complete: Optional callback when job completes successfully.
            on_error: Optional callback when job fails.

        Note:
            This method should return immediately, allowing the caller to
            return a response while the job runs in the background.
        """
        ...
