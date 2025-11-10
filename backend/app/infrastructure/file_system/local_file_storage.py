from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import BinaryIO

from app.application.contracts.file_storage import FileStorage
from app.domain.value_objects.file_descriptor import FileDescriptor
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LocalFileStorage(FileStorage):
    """Filesystem-backed storage for LaTeX artefacts."""

    def __init__(self, upload_dir: Path, output_dir: Path) -> None:
        self._upload_dir = Path(upload_dir)
        self._output_dir = Path(output_dir)

    def ensure_ready(self) -> None:
        self._upload_dir.mkdir(parents=True, exist_ok=True)
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def store_bytes(
        self, content: bytes, suffix: str, original_name: str | None = None
    ) -> FileDescriptor:
        self.ensure_ready()
        file_id = uuid.uuid4().hex
        filename = f"{file_id}{suffix}"
        path = self._upload_dir / filename
        try:
            with path.open("wb") as handle:
                handle.write(content)
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to persist file %s: %s", path, exc)
            raise RuntimeError(f"Failed to persist file: {exc}") from exc

        return FileDescriptor(path=path, original_name=original_name)

    def store_stream(
        self, stream: BinaryIO, suffix: str, original_name: str | None = None
    ) -> FileDescriptor:
        data = stream.read()
        return self.store_bytes(data, suffix=suffix, original_name=original_name)

    def read_text(self, descriptor: FileDescriptor, encoding: str = "utf-8") -> str:
        path = descriptor.resolve()
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        try:
            return path.read_text(encoding=encoding)
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"Failed to read file: {exc}") from exc

    def remove(self, descriptor: FileDescriptor) -> None:
        path = descriptor.path
        try:
            if path.exists():
                path.unlink()
        except Exception as exc:
            logger.warning("Failed to delete %s: %s", path, exc)

    def to_relative(self, descriptor: FileDescriptor, base: Path) -> str:
        return os.path.relpath(descriptor.path, start=base)
