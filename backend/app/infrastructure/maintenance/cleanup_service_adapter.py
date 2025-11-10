from __future__ import annotations

import shutil
import os
from pathlib import Path
from datetime import datetime, timedelta

from app.application.contracts.cleanup_service import CleanupService
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LocalCleanupService(CleanupService):
    """Infrastructure adapter for file and directory cleanup operations."""

    def cleanup_session_outputs_directory(self) -> None:
        """Remove all files and subfolders under the session outputs directory."""
        try:
            session_outputs_dir = Path(settings.SESSION_OUTPUT_DIR)

            if not session_outputs_dir.exists():
                logger.info(
                    f"Session outputs directory does not exist: {session_outputs_dir}"
                )
                return

            # Get all files in the session outputs directory
            files = list(session_outputs_dir.glob("*"))
            file_count = len([f for f in files if f.is_file()])

            if file_count == 0:
                logger.info("Session outputs directory is already clean")
                return

            logger.info(
                f"Cleaning up {file_count} files from session outputs directory..."
            )

            # Remove all files (but keep the directory)
            for file_path in files:
                try:
                    if file_path.is_file():
                        file_path.unlink()
                        logger.debug(f"Removed file: {file_path.name}")
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                        logger.debug(f"Removed directory: {file_path.name}")
                except Exception as e:  # noqa: BLE001
                    logger.warning(f"Failed to remove {file_path}: {str(e)}")

            logger.info(
                f"✅ Successfully cleaned up session outputs directory ({file_count} files removed)"
            )

        except Exception as e:  # noqa: BLE001
            logger.error(f"❌ Failed to cleanup session outputs directory: {str(e)}")

    def cleanup_old_session_outputs(self, days_to_keep: int = 7) -> None:
        """Remove session output files older than specified days.

        Args:
            days_to_keep: Number of days to keep session output files (default: 7)
        """
        try:
            session_outputs_dir = Path(settings.SESSION_OUTPUT_DIR)

            if not session_outputs_dir.exists():
                logger.info(
                    f"Session outputs directory does not exist: {session_outputs_dir}"
                )
                return

            # Calculate cutoff date
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)

            # Get all session output files
            session_output_files = list(session_outputs_dir.glob("*"))
            removed_count = 0

            for session_output_file in session_output_files:
                try:
                    # Get file modification time
                    file_mtime = datetime.fromtimestamp(
                        session_output_file.stat().st_mtime
                    )

                    if file_mtime < cutoff_date:
                        if session_output_file.is_file():
                            session_output_file.unlink()
                        elif session_output_file.is_dir():
                            shutil.rmtree(session_output_file)
                        removed_count += 1
                        logger.debug(
                            f"Removed old session output: {session_output_file.name} (modified: {file_mtime.strftime('%Y-%m-%d %H:%M:%S')})"
                        )

                except Exception as e:  # noqa: BLE001
                    logger.warning(f"Failed to process {session_output_file}: {str(e)}")

            if removed_count > 0:
                logger.info(
                    f"✅ Cleaned up {removed_count} old session output files (older than {days_to_keep} days)"
                )
            else:
                logger.info("No old session output files found to clean up")

        except Exception as e:  # noqa: BLE001
            logger.error(f"❌ Failed to cleanup old session outputs: {str(e)}")

    def cleanup_uploads_directory(self) -> None:
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
                except Exception as e:  # noqa: BLE001
                    logger.warning(f"Failed to remove {file_path}: {str(e)}")

            logger.info(
                f"✅ Successfully cleaned up uploads directory ({file_count} files removed)"
            )

        except Exception as e:  # noqa: BLE001
            logger.error(f"❌ Failed to cleanup uploads directory: {str(e)}")

    def cleanup_session_logs_directory(self) -> None:
        """Remove all session log files from the session logs directory."""
        try:
            session_logs_dir = Path(settings.SESSION_LOG_DIR)

            if not session_logs_dir.exists():
                logger.info(
                    f"Session logs directory does not exist: {session_logs_dir}"
                )
                return

            # Get all session log files in the session logs directory
            session_log_files = list(session_logs_dir.glob("*.log"))
            file_count = len(session_log_files)

            if file_count == 0:
                logger.info("Session logs directory is already clean")
                return

            logger.info(
                f"Cleaning up {file_count} session log files from session logs directory..."
            )

            # Remove all session log files
            for session_log_file in session_log_files:
                try:
                    session_log_file.unlink()
                    logger.debug(f"Removed session log file: {session_log_file.name}")
                except Exception as e:  # noqa: BLE001
                    logger.warning(f"Failed to remove {session_log_file}: {str(e)}")

            logger.info(
                f"✅ Successfully cleaned up session logs directory ({file_count} files removed)"
            )

        except Exception as e:  # noqa: BLE001
            logger.error(f"❌ Failed to cleanup session logs directory: {str(e)}")

    def cleanup_old_session_logs(self, days_to_keep: int = 7) -> None:
        """Remove session log files older than specified days.

        Args:
            days_to_keep: Number of days to keep session log files (default: 7)
        """
        try:
            session_logs_dir = Path(settings.SESSION_LOG_DIR)

            if not session_logs_dir.exists():
                logger.info(
                    f"Session logs directory does not exist: {session_logs_dir}"
                )
                return

            # Calculate cutoff date
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)

            # Get all session log files
            session_log_files = list(session_logs_dir.glob("*.log"))
            removed_count = 0

            for session_log_file in session_log_files:
                try:
                    # Get file modification time
                    file_mtime = datetime.fromtimestamp(
                        session_log_file.stat().st_mtime
                    )

                    if file_mtime < cutoff_date:
                        session_log_file.unlink()
                        removed_count += 1
                        logger.debug(
                            f"Removed old session log file: {session_log_file.name} (modified: {file_mtime.strftime('%Y-%m-%d %H:%M:%S')})"
                        )

                except Exception as e:  # noqa: BLE001
                    logger.warning(f"Failed to process {session_log_file}: {str(e)}")

            if removed_count > 0:
                logger.info(
                    f"✅ Cleaned up {removed_count} old session log files (older than {days_to_keep} days)"
                )
            else:
                logger.info("No old session log files found to clean up")

        except Exception as e:  # noqa: BLE001
            logger.error(f"❌ Failed to cleanup old session logs: {str(e)}")

    def cleanup_all_directories(self) -> None:
        """Clean uploads, session outputs, and session logs directories."""
        logger.info("=== STARTING DIRECTORY CLEANUP ===")
        self.cleanup_uploads_directory()
        self.cleanup_session_outputs_directory()
        self.cleanup_session_logs_directory()
        logger.info("=== DIRECTORY CLEANUP COMPLETED ===")

    def ensure_directories_exist(self) -> None:
        """Ensure uploads, session outputs, and session logs directories exist, creating them if needed."""
        try:
            logger.info("=== ENSURING DIRECTORY STRUCTURE ===")

            # Create uploads directory
            uploads_dir = Path(settings.UPLOAD_DIR)
            uploads_dir.mkdir(exist_ok=True)
            logger.info(f"✅ Uploads directory ready: {uploads_dir}")

            # Create session outputs directory
            session_outputs_dir = Path(settings.SESSION_OUTPUT_DIR)
            session_outputs_dir.mkdir(exist_ok=True)
            logger.info(f"✅ Session outputs directory ready: {session_outputs_dir}")

            # Create session logs directory
            session_logs_dir = Path(settings.SESSION_LOG_DIR)
            session_logs_dir.mkdir(exist_ok=True)
            logger.info(f"✅ Session logs directory ready: {session_logs_dir}")

            logger.info("=== DIRECTORY STRUCTURE READY ===")

        except Exception as e:  # noqa: BLE001
            logger.error(f"❌ Failed to ensure directory structure: {str(e)}")
            raise
