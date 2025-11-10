from __future__ import annotations

from typing import Tuple

from fastapi import UploadFile

from app.application.contracts.job_data_parser import JobDataParser, JobParseResult


class ParseJobFileUseCase:
    """Parse and validate job data from an uploaded file."""

    def __init__(self, parser: JobDataParser) -> None:
        self._parser = parser

    async def execute(self, file: UploadFile) -> JobParseResult:
        """Parse a job file and return structured results."""
        return await self._parser.parse(file)

    async def preview(
        self, file: UploadFile, limit: int = 3
    ) -> Tuple[List[str], List[List[str]]]:
        """Preview a job file without full parsing."""
        return await self._parser.preview(file, limit=limit)
