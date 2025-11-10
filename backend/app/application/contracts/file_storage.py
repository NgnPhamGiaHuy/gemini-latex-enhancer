from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO

from app.domain.value_objects.file_descriptor import FileDescriptor


class FileStorage(ABC):
    """Abstract storage service for LaTeX source files and outputs."""

    @abstractmethod
    def ensure_ready(self) -> None:
        """Validate or create required directories/resources."""

    @abstractmethod
    def store_bytes(
        self, content: bytes, suffix: str, original_name: str | None = None
    ) -> FileDescriptor:
        """Persist bytes and return a descriptor."""

    @abstractmethod
    def store_stream(
        self, stream: BinaryIO, suffix: str, original_name: str | None = None
    ) -> FileDescriptor:
        """Persist streamed content."""

    @abstractmethod
    def read_text(self, descriptor: FileDescriptor, encoding: str = "utf-8") -> str:
        """Read stored text content."""

    @abstractmethod
    def remove(self, descriptor: FileDescriptor) -> None:
        """Delete the associated resource."""

    @abstractmethod
    def to_relative(self, descriptor: FileDescriptor, base: Path) -> str:
        """Return a relative path for client consumption."""
