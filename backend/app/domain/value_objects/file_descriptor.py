from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class FileDescriptor:
    """Value object describing a logical file in the workspace.

    Attributes:
        path: Absolute path to the file on disk.
        original_name: Optional original filename provided by the user.
        media_type: Optional media/content type hint.
    """

    path: Path
    original_name: Optional[str] = None
    media_type: Optional[str] = None

    def resolve(self) -> Path:
        return self.path.resolve()

    def exists(self) -> bool:
        return self.path.exists()
