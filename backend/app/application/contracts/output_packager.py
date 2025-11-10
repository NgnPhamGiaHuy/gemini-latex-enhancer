from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple


class OutputPackager(ABC):
    """Contract for preparing output directory structures and archives."""

    @abstractmethod
    def create_main_folder(self) -> Path: ...

    @abstractmethod
    def create_job_subfolder(
        self, parent: Path, company_name: str | None, job_title: str
    ) -> Path: ...

    @abstractmethod
    def build_result_filenames(
        self, original_cv_name: str, company_name: str | None, job_title: str
    ) -> Tuple[str, str]: ...

    @abstractmethod
    def build_result_filenames_with_original_name(
        self, original_filename: str, company_name: str | None, job_title: str
    ) -> Tuple[str, str]: ...

    @abstractmethod
    def zip_folder(self, folder: Path) -> Path: ...

    @abstractmethod
    def to_relative_path(self, path: Path) -> str:
        """Convert an absolute Path object to a client-facing relative path."""
        ...
