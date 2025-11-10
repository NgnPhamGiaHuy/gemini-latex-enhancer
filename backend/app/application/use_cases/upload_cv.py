from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import List, Dict

from app.application.contracts.file_storage import FileStorage
from app.domain.exceptions import DomainValidationError
from app.domain.services.latex_section_parser import LatexSectionParser
from app.domain.services.latex_validator import LatexValidator


@dataclass(frozen=True)
class UploadCvResult:
    session_id: str
    sections: List[Dict[str, str]]
    latex_content: str
    original_filename: str


class UploadCvUseCase:
    """Handle CV upload: persist temporarily, validate, and parse sections."""

    def __init__(self, storage: FileStorage, *, max_file_size: int) -> None:
        self._storage = storage
        self._max_file_size = max_file_size

    def execute(self, *, filename: str, content: bytes) -> UploadCvResult:
        if not filename or not filename.endswith(".tex"):
            raise DomainValidationError("Only .tex files are allowed")

        if not content:
            raise DomainValidationError("File is empty")

        if len(content) > self._max_file_size:
            raise DomainValidationError("File too large")

        try:
            content_str = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise DomainValidationError("File contains invalid characters") from exc

        LatexValidator.validate(content_str)

        self._storage.ensure_ready()
        descriptor = self._storage.store_bytes(
            content,
            suffix=".tex",
            original_name=filename,
        )
        try:
            sections = LatexSectionParser.parse(content_str)
        finally:
            self._storage.remove(descriptor)

        session_id = str(uuid.uuid4())
        return UploadCvResult(
            session_id=session_id,
            sections=sections,
            latex_content=content_str,
            original_filename=filename,
        )
