from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from app.domain.value_objects.file_descriptor import FileDescriptor


class OutputStorage(ABC):
    """Contract for persisting enhanced LaTeX artefacts."""

    @abstractmethod
    def ensure_ready(self) -> None: ...

    @abstractmethod
    def save_generated(
        self, latex_content: str, base_name: str = "cv"
    ) -> FileDescriptor: ...

    @abstractmethod
    def save_with_original(
        self, latex_content: str, original_filename: str
    ) -> FileDescriptor: ...

    @abstractmethod
    def save_with_job_info(
        self,
        latex_content: str,
        original_filename: str,
        job_title: str,
        company_name: Optional[str] = None,
    ) -> tuple[FileDescriptor, str]: ...

    @abstractmethod
    def to_relative(self, descriptor: FileDescriptor) -> str: ...

    @abstractmethod
    def to_relative_path(self, path: Path) -> str: ...

    @abstractmethod
    def sanitize_filename(self, filename: str) -> str: ...
