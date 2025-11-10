from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Optional

from fastapi import HTTPException

from app.application.contracts.output_storage import OutputStorage
from app.config import settings
from app.domain.value_objects.file_descriptor import FileDescriptor
from app.utils.filename_sanitizer import sanitize_filename_for_filesystem
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SessionOutputStorage(OutputStorage):
    """Persist enhanced documents under `SESSION_OUTPUT_DIR`."""

    def __init__(self, output_dir: Path | None = None) -> None:
        self._output_dir = Path(output_dir or settings.SESSION_OUTPUT_DIR)

    def ensure_ready(self) -> None:
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def save_generated(
        self, latex_content: str, base_name: str = "cv"
    ) -> FileDescriptor:
        self.ensure_ready()
        file_id = uuid.uuid4().hex
        filename = f"{base_name}_{file_id}.tex"
        path = self._output_dir / filename
        return self._write_text(path, latex_content, original_name=filename)

    def save_with_original(
        self, latex_content: str, original_filename: str
    ) -> FileDescriptor:
        self.ensure_ready()
        filename = sanitize_filename_for_filesystem(original_filename or "cv.tex")
        if not filename.endswith(".tex"):
            filename = f"{filename}.tex"
        path = self._output_dir / filename
        return self._write_text(path, latex_content, original_name=original_filename)

    def save_with_job_info(
        self,
        latex_content: str,
        original_filename: str,
        job_title: str,
        company_name: Optional[str] = None,
    ) -> tuple[FileDescriptor, str]:
        self.ensure_ready()
        base = (
            original_filename.replace(".tex", "")
            if original_filename.endswith(".tex")
            else original_filename
        )
        base = sanitize_filename_for_filesystem(base)
        job_part = sanitize_filename_for_filesystem(job_title)
        company_part = (
            sanitize_filename_for_filesystem(company_name) if company_name else None
        )

        if company_part:
            clean_name = f"{base}-{job_part}-{company_part}"
        else:
            clean_name = f"{base}-{job_part}"

        unique_id = uuid.uuid4().hex[:8]
        filename = f"{clean_name}-{unique_id}.tex"
        path = self._output_dir / filename
        descriptor = self._write_text(
            path, latex_content, original_name=f"{clean_name}.tex"
        )
        return descriptor, f"{clean_name}.tex"

    def to_relative(self, descriptor: FileDescriptor) -> str:
        return os.path.relpath(descriptor.path, start=self._output_dir)

    def to_relative_path(self, path: Path) -> str:
        return os.path.relpath(path, start=self._output_dir)

    def sanitize_filename(self, filename: str) -> str:
        return sanitize_filename_for_filesystem(filename)

    def _write_text(
        self, path: Path, content: str, *, original_name: Optional[str]
    ) -> FileDescriptor:
        try:
            with path.open("w", encoding="utf-8") as handle:
                handle.write(content)
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to save LaTeX result at %s: %s", path, exc)
            raise HTTPException(
                status_code=500, detail=f"Failed to save result: {exc}"
            ) from exc
        logger.info("Enhanced CV saved: %s", path)
        return FileDescriptor(path=path, original_name=original_name)
