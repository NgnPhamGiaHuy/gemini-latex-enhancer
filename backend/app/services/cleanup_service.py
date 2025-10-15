"""
File cleanup service for managing temporary files.

Provides helpers to empty uploads/outputs directories and to ensure the
directory structure exists at startup.
"""

import shutil
from pathlib import Path
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class FileCleanupService:
    """Service for cleaning up temporary files and directories."""

    @staticmethod
    def cleanup_outputs_directory():
        """Remove all files and subfolders under the outputs directory."""
        try:
            outputs_dir = Path(settings.OUTPUT_DIR)

            if not outputs_dir.exists():
                logger.info(f"Outputs directory does not exist: {outputs_dir}")
                return

            # Get all files in the outputs directory
            files = list(outputs_dir.glob("*"))
            file_count = len([f for f in files if f.is_file()])

            if file_count == 0:
                logger.info("Outputs directory is already clean")
                return

            logger.info(f"Cleaning up {file_count} files from outputs directory...")

            # Remove all files (but keep the directory)
            for file_path in files:
                try:
                    if file_path.is_file():
                        file_path.unlink()
                        logger.debug(f"Removed file: {file_path.name}")
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                        logger.debug(f"Removed directory: {file_path.name}")
                except Exception as e:
                    logger.warning(f"Failed to remove {file_path}: {str(e)}")

            logger.info(
                f"✅ Successfully cleaned up outputs directory ({file_count} files removed)"
            )

        except Exception as e:
            logger.error(f"❌ Failed to cleanup outputs directory: {str(e)}")

    @staticmethod
    def cleanup_uploads_directory():
        """Remove all files and subfolders under the uploads directory."""
        try:
            uploads_dir = Path(settings.UPLOAD_DIR)

            if not uploads_dir.exists():
                logger.info(f"Uploads directory does not exist: {uploads_dir}")
                return

            # Get all files in the uploads directory
            files = list(uploads_dir.glob("*"))
            file_count = len([f for f in files if f.is_file()])

            if file_count == 0:
                logger.info("Uploads directory is already clean")
                return

            logger.info(f"Cleaning up {file_count} files from uploads directory...")

            # Remove all files (but keep the directory)
            for file_path in files:
                try:
                    if file_path.is_file():
                        file_path.unlink()
                        logger.debug(f"Removed file: {file_path.name}")
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                        logger.debug(f"Removed directory: {file_path.name}")
                except Exception as e:
                    logger.warning(f"Failed to remove {file_path}: {str(e)}")

            logger.info(
                f"✅ Successfully cleaned up uploads directory ({file_count} files removed)"
            )

        except Exception as e:
            logger.error(f"❌ Failed to cleanup uploads directory: {str(e)}")

    @staticmethod
    def cleanup_all_directories():
        """Clean both uploads and outputs directories."""
        logger.info("=== STARTING DIRECTORY CLEANUP ===")
        FileCleanupService.cleanup_uploads_directory()
        FileCleanupService.cleanup_outputs_directory()
        logger.info("=== DIRECTORY CLEANUP COMPLETED ===")

    @staticmethod
    def ensure_directories_exist():
        """Ensure uploads and outputs directories exist, creating them if needed."""
        try:
            logger.info("=== ENSURING DIRECTORY STRUCTURE ===")

            # Create uploads directory
            uploads_dir = Path(settings.UPLOAD_DIR)
            uploads_dir.mkdir(exist_ok=True)
            logger.info(f"✅ Uploads directory ready: {uploads_dir}")

            # Create outputs directory
            outputs_dir = Path(settings.OUTPUT_DIR)
            outputs_dir.mkdir(exist_ok=True)
            logger.info(f"✅ Outputs directory ready: {outputs_dir}")

            logger.info("=== DIRECTORY STRUCTURE READY ===")

        except Exception as e:
            logger.error(f"❌ Failed to ensure directory structure: {str(e)}")
            raise
