from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, List

from fastapi import UploadFile

from app.domain.value_objects.job_context import JobContext


@dataclass(frozen=True)
class JobParseResult:
    """Result of parsing a job data file."""

    jobs: List[JobContext]
    headers: List[str]
    preview_rows: List[List[str]]


class JobDataParser(ABC):
    """Contract for parsing uploaded job definitions."""

    @abstractmethod
    async def parse(self, file: UploadFile) -> JobParseResult: ...

    @abstractmethod
    async def preview(
        self, file: UploadFile, limit: int = 3
    ) -> Tuple[List[str], List[List[str]]]: ...
