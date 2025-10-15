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
        """Persist an uploaded `.tex` file to the uploads directory.

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

            # Save file
            logger.info("Reading file content...")
            content = file.file.read()
            logger.info(f"File content read, size: {len(content)} bytes")

            if len(content) > settings.MAX_FILE_SIZE:
                logger.error(
                    f"❌ File too large: {len(content)} bytes (max: {settings.MAX_FILE_SIZE})"
                )
                raise HTTPException(status_code=400, detail="File too large")

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
