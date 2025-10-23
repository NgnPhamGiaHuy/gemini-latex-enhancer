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
    """Sanitize a folder/file name to avoid illegal characters and ensure LaTeX compatibility."""
    if not name:
        return ""
    # Remove parentheses and other non-critical special characters
    cleaned = re.sub(r"[()\[\]{}~`!@#$%^&+=,;']+", "", name)
    # Replace forbidden filesystem characters with hyphens
    cleaned = re.sub(r"[\\/:*?\"<>|]+", "-", cleaned)
    # Replace spaces with hyphens for LaTeX compatibility
    cleaned = re.sub(r"\s+", "-", cleaned)
    # Remove any leading/trailing hyphens
    cleaned = cleaned.strip("-")
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
    def build_result_filenames_with_original_name(
        original_filename: str, company_name: str, job_title: str
    ) -> Tuple[str, str]:
        """Return `.tex` and `.pdf` filenames using format: Filename-Job title-Company name(if have)."""
        # Remove .tex extension if present and sanitize base name
        base_name = (
            original_filename.replace(".tex", "")
            if original_filename.endswith(".tex")
            else original_filename
        )
        base_name = _sanitize_name(base_name)

        # Sanitize job title and company name for filesystem compatibility
        job_title_clean = _sanitize_name(job_title)
        company_name_clean = _sanitize_name(company_name) if company_name else None

        # Build filename in format: Filename-Job title-Company name(if have)
        if company_name_clean:
            final_name = f"{base_name}-{job_title_clean}-{company_name_clean}"
        else:
            final_name = f"{base_name}-{job_title_clean}"

        return f"{final_name}.tex", f"{final_name}.pdf"

    @staticmethod
    def zip_folder(main_folder: str) -> str:
        """Create a zip archive alongside the given folder and return its path."""
        zip_base = main_folder
        zip_path = shutil.make_archive(zip_base, "zip", root_dir=main_folder)
        return zip_path
