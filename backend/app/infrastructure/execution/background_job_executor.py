"""
Background job executor using FastAPI BackgroundTasks.

Follows SOLID principles:
- Single Responsibility: Only handles background execution
- Open/Closed: Can be extended with other executors (Celery, etc.) without modifying use cases
- Liskov Substitution: Implements JobExecutor interface correctly
- Dependency Inversion: Use cases depend on JobExecutor abstraction
"""

from __future__ import annotations

from typing import Callable, Any

from fastapi import BackgroundTasks

from app.application.contracts.job_executor import JobExecutor


class BackgroundJobExecutor(JobExecutor):
    """Execute jobs using FastAPI BackgroundTasks."""

    def __init__(self, background_tasks: BackgroundTasks) -> None:
        """Initialize with FastAPI BackgroundTasks instance.

        Args:
            background_tasks: FastAPI BackgroundTasks from request context.
        """
        self._background_tasks = background_tasks

    def execute_in_background(
        self,
        job_fn: Callable[[], Any],
        *,
        on_complete: Callable[[Any], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
    ) -> None:
        """Execute job function in background using FastAPI BackgroundTasks.

        Args:
            job_fn: The function to execute (no arguments).
            on_complete: Optional callback when job completes successfully.
            on_error: Optional callback when job fails.
        """

        def _wrapped_job() -> None:
            """Wrapper that handles callbacks."""
            try:
                result = job_fn()
                if on_complete:
                    on_complete(result)
            except Exception as exc:
                if on_error:
                    on_error(exc)
                else:
                    raise

        self._background_tasks.add_task(_wrapped_job)
