"""
Output Manager.

Creates structured output directories for batch runs and produces a zip
archive for convenient download.
"""

import os
import re
import shutil
from typing import Tuple
from datetime import datetime

from app.config import settings


def _sanitize_name(name: str) -> str:
    """Sanitize a folder/file name to avoid illegal characters and whitespace."""
    if not name:
        return ""
    # Replace forbidden characters and collapse whitespace
    cleaned = re.sub(r"[\\/:*?\"<>|]+", "-", name)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


class OutputManager:
    """Manage output folders and packaging for batch results."""

    @staticmethod
    def create_main_output_folder() -> str:
        """Create a timestamped main folder under the outputs directory."""
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = f"Enhanced_CVs_{ts}"
        base_dir = os.path.join(settings.OUTPUT_DIR)
        os.makedirs(base_dir, exist_ok=True)
        full_path = os.path.join(base_dir, folder_name)
        os.makedirs(full_path, exist_ok=True)
        return full_path

    @staticmethod
    def create_job_subfolder(
        main_folder: str, company_name: str, job_title: str
    ) -> str:
        """Create a per-job subfolder under the main batch output folder."""
        company_part = _sanitize_name(company_name) if company_name else ""
        title_part = _sanitize_name(job_title)
        if company_part:
            sub_name = f"{company_part} - {title_part}"
        else:
            sub_name = title_part
        sub_path = os.path.join(main_folder, sub_name)
        os.makedirs(sub_path, exist_ok=True)
        return sub_path

    @staticmethod
    def build_result_filenames(
        original_cv_name: str, company_name: str, job_title: str
    ) -> Tuple[str, str]:
        """Return sanitized `.tex` and `.pdf` filenames for a job output."""
        company_part = _sanitize_name(company_name) if company_name else None
        title_part = _sanitize_name(job_title)
        base = _sanitize_name(original_cv_name)
        if company_part:
            base_name = f"{base} - {company_part} - {title_part}"
        else:
            base_name = f"{base} - {title_part}"
        return f"{base_name}.tex", f"{base_name}.pdf"

    @staticmethod
    def zip_folder(main_folder: str) -> str:
        """Create a zip archive alongside the given folder and return its path."""
        zip_base = main_folder
        zip_path = shutil.make_archive(zip_base, "zip", root_dir=main_folder)
        return zip_path
