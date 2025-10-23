"""
File Service for handling file operations.

Responsibilities:
- Ensure upload/output directories exist
- Persist uploaded `.tex` files with unique IDs
- Read and write LaTeX content safely
- Provide relative paths for API responses
- Cleanup temporary files after use
"""

import os
import re
import shutil
import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class FileService:
    """Utility service for reading/writing LaTeX files and housekeeping."""

    @staticmethod
    def ensure_directories():
        """Create upload and output directories when missing."""
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        os.makedirs(settings.OUTPUT_DIR, exist_ok=True)

    @staticmethod
    def save_uploaded_file(file: UploadFile) -> str:
        """Persist an uploaded `.tex` file with enhanced security validation.

        Args:
            file: FastAPI `UploadFile` representing the client upload.

        Returns:
            Absolute path to the stored file.

        Raises:
            HTTPException: For invalid file types, size limits, or IO failures.
        """
        logger.info(f"=== FILE SAVE STARTED ===")
        logger.info(f"Filename: {file.filename}")
        logger.info(f"Content type: {file.content_type}")

        try:
            FileService.ensure_directories()
            logger.info("✅ Directories ensured")

            # Validate file type
            if not file.filename.endswith(".tex"):
                logger.error(f"❌ Invalid file type: {file.filename}")
                raise HTTPException(
                    status_code=400, detail="Only .tex files are allowed"
                )

            logger.info("✅ File type validation passed")

            # Generate unique filename
            file_id = str(uuid.uuid4())
            file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.tex")
            logger.info(f"Generated file path: {file_path}")

            # Read file content with enhanced validation
            logger.info("Reading file content...")
            content = file.file.read()
            logger.info(f"File content read, size: {len(content)} bytes")

            # Validate file size before processing
            if len(content) > settings.MAX_FILE_SIZE:
                logger.error(
                    f"❌ File too large: {len(content)} bytes (max: {settings.MAX_FILE_SIZE})"
                )
                raise HTTPException(status_code=400, detail="File too large")

            # Additional content validation
            if len(content) == 0:
                logger.error("❌ File is empty")
                raise HTTPException(status_code=400, detail="File is empty")

            # Validate content is valid UTF-8
            try:
                content.decode("utf-8")
                logger.info("✅ File content is valid UTF-8")
            except UnicodeDecodeError as e:
                logger.error(f"❌ File contains invalid characters: {str(e)}")
                raise HTTPException(
                    status_code=400, detail="File contains invalid characters"
                )

            # Basic content validation - check for suspicious patterns
            content_str = content.decode("utf-8")
            if len(content_str.strip()) < 10:
                logger.error("❌ File content too short")
                raise HTTPException(
                    status_code=400, detail="File content appears to be too short"
                )

            # Check for basic LaTeX structure
            if not any(
                marker in content_str
                for marker in [
                    "\\documentclass",
                    "\\begin{document}",
                    "\\end{document}",
                ]
            ):
                logger.warning("⚠️ File may not contain valid LaTeX structure")

            logger.info("Writing file to disk...")
            with open(file_path, "wb") as f:
                f.write(content)

            logger.info(f"✅ File saved successfully: {file_path}")
            logger.info("=== FILE SAVE COMPLETED ===")
            return file_path

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Failed to save file: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500, detail=f"Failed to save file: {str(e)}"
            )

    @staticmethod
    def read_latex_content(file_path: str) -> str:
        """Read LaTeX content from disk for further processing.

        Args:
            file_path: Absolute/relative path to the `.tex` file.

        Returns:
            The file contents as a UTF-8 string.

        Raises:
            HTTPException: If the file does not exist or cannot be read.
        """
        logger.info(f"=== READING LATEX CONTENT ===")
        logger.info(f"File path: {file_path}")

        try:
            if not os.path.exists(file_path):
                logger.error(f"❌ File does not exist: {file_path}")
                raise HTTPException(
                    status_code=404, detail=f"File not found: {file_path}"
                )

            logger.info("✅ File exists, reading content...")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            logger.info(
                f"✅ Content read successfully, length: {len(content)} characters"
            )
            logger.debug(f"Content preview: {content[:200]}...")

            return content
        except Exception as e:
            logger.error(f"❌ Failed to read file {file_path}: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500, detail=f"Failed to read file: {str(e)}"
            )

    @staticmethod
    def save_result(latex_content: str, base_name: str = "cv") -> str:
        """Write enhanced LaTeX content to the outputs directory.

        Args:
            latex_content: The LaTeX source to persist.
            base_name: Base filename (without extension/id); a UUID suffix is added.

        Returns:
            Absolute path to the created `.tex` file within outputs.

        Raises:
            HTTPException: If writing fails.
        """
        try:
            FileService.ensure_directories()

            # Generate unique filename
            file_id = str(uuid.uuid4())
            result_path = os.path.join(
                settings.OUTPUT_DIR, f"{base_name}_{file_id}.tex"
            )

            # Save enhanced content
            with open(result_path, "w", encoding="utf-8") as f:
                f.write(latex_content)

            logger.info(f"Enhanced CV saved: {result_path}")
            return result_path

        except Exception as e:
            logger.error(f"Failed to save result: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"Failed to save result: {str(e)}"
            )

    @staticmethod
    def save_result_with_original_name(
        latex_content: str, original_filename: str
    ) -> str:
        """Write enhanced LaTeX content using the original filename.

        Args:
            latex_content: The LaTeX source to persist.
            original_filename: Original filename to use (with .tex extension).

        Returns:
            Absolute path to the created `.tex` file within outputs.

        Raises:
            HTTPException: If writing fails.
        """
        try:
            FileService.ensure_directories()

            # Use original filename directly
            result_path = os.path.join(settings.OUTPUT_DIR, original_filename)

            # Save enhanced content
            with open(result_path, "w", encoding="utf-8") as f:
                f.write(latex_content)

            logger.info(f"Enhanced CV saved with original name: {result_path}")
            return result_path

        except Exception as e:
            logger.error(f"Failed to save result with original name: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save result with original name: {str(e)}",
            )

    @staticmethod
    def save_result_with_job_info(
        latex_content: str,
        original_filename: str,
        job_title: str,
        company_name: str = None,
    ) -> str:
        """Write enhanced LaTeX content using format: Filename-Job title-Company name(if have).

        Args:
            latex_content: The LaTeX source to persist.
            original_filename: Original filename (with .tex extension).
            job_title: Job title for the enhancement.
            company_name: Optional company name.

        Returns:
            Absolute path to the created `.tex` file within outputs.

        Raises:
            HTTPException: If writing fails.
        """
        try:
            FileService.ensure_directories()

            # Remove .tex extension if present and sanitize base name
            base_name = (
                original_filename.replace(".tex", "")
                if original_filename.endswith(".tex")
                else original_filename
            )
            # Remove parentheses and other non-critical special characters
            base_name = re.sub(r"[()\[\]{}~`!@#$%^&+=,;']+", "", base_name)
            # Replace forbidden filesystem characters with hyphens
            base_name = re.sub(r"[\\/:*?\"<>|]+", "-", base_name)
            base_name = re.sub(r"\s+", "-", base_name)
            base_name = base_name.strip("-")

            # Sanitize job title and company name for filesystem compatibility
            # Remove parentheses and other non-critical special characters
            job_title_clean = re.sub(r"[()\[\]{}~`!@#$%^&+=,;']+", "", job_title)
            # Replace forbidden filesystem characters with hyphens
            job_title_clean = re.sub(r"[\\/:*?\"<>|]+", "-", job_title_clean)
            job_title_clean = re.sub(r"\s+", "-", job_title_clean)
            job_title_clean = job_title_clean.strip("-")

            company_name_clean = None
            if company_name:
                # Remove parentheses and other non-critical special characters
                company_name_clean = re.sub(
                    r"[()\[\]{}~`!@#$%^&+=,;']+", "", company_name
                )
                # Replace forbidden filesystem characters with hyphens
                company_name_clean = re.sub(r"[\\/:*?\"<>|]+", "-", company_name_clean)
                company_name_clean = re.sub(r"\s+", "-", company_name_clean)
                company_name_clean = company_name_clean.strip("-")

            # Build filename in format: Filename-Job title-Company name(if have)
            if company_name_clean:
                final_name = f"{base_name}-{job_title_clean}-{company_name_clean}"
            else:
                final_name = f"{base_name}-{job_title_clean}"

            result_path = os.path.join(settings.OUTPUT_DIR, f"{final_name}.tex")

            # Save enhanced content
            with open(result_path, "w", encoding="utf-8") as f:
                f.write(latex_content)

            logger.info(f"Enhanced CV saved with job info: {result_path}")
            return result_path

        except Exception as e:
            logger.error(f"Failed to save result with job info: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"Failed to save result with job info: {str(e)}"
            )

    @staticmethod
    def get_relative_path(absolute_path: str) -> str:
        """Convert an absolute path under outputs to a client-facing relative path."""
        return os.path.relpath(absolute_path, settings.OUTPUT_DIR)

    @staticmethod
    def cleanup_file(file_path: str):
        """Remove a temporary file, if present, ignoring missing files."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup file {file_path}: {str(e)}")
