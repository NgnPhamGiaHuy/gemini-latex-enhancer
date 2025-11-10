from __future__ import annotations

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Tuple

from app.application.contracts.output_packager import OutputPackager
from app.config import settings
from app.utils.filename_sanitizer import sanitize_filename_for_filesystem


class LocalOutputPackager(OutputPackager):
    def __init__(self) -> None:
        self._base_dir = Path(settings.SESSION_OUTPUT_DIR)

    def create_main_folder(self) -> Path:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder = self._base_dir / f"Enhanced_CVs_{timestamp}"
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def create_job_subfolder(
        self, parent: Path, company_name: str | None, job_title: str
    ) -> Path:
        company_part = self._sanitize(company_name) if company_name else ""
        title_part = self._sanitize(job_title)
        sub_name = f"{company_part} - {title_part}" if company_part else title_part
        sub_path = parent / sub_name
        sub_path.mkdir(parents=True, exist_ok=True)
        return sub_path

    def build_result_filenames(
        self, original_cv_name: str, company_name: str | None, job_title: str
    ) -> Tuple[str, str]:
        base = self._sanitize(original_cv_name)
        title = self._sanitize(job_title)
        company = self._sanitize(company_name) if company_name else None
        if company:
            base_name = f"{base}-{title}-{company}"
        else:
            base_name = f"{base}-{title}"
        return f"{base_name}.tex", f"{base_name}.pdf"

    def build_result_filenames_with_original_name(
        self, original_filename: str, company_name: str | None, job_title: str
    ) -> Tuple[str, str]:
        base = (
            original_filename[:-4]
            if original_filename.endswith(".tex")
            else original_filename
        )
        return self.build_result_filenames(base, company_name, job_title)

    def zip_folder(self, folder: Path) -> Path:
        archive_path = shutil.make_archive(str(folder), "zip", root_dir=folder)
        return Path(archive_path)

    def to_relative_path(self, path: Path) -> str:
        """Convert an absolute Path object to a client-facing relative path."""
        return os.path.relpath(path, start=self._base_dir)

    @staticmethod
    def _sanitize(name: str | None) -> str:
        if not name:
            return ""
        return sanitize_filename_for_filesystem(name)
