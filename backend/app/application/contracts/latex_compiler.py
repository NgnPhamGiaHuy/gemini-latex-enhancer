from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from app.domain.value_objects.file_descriptor import FileDescriptor


@dataclass(frozen=True)
class CompilationResult:
    pdf_path: Path
    log_path: Optional[Path] = None


class LatexCompiler(ABC):
    """Contract for compiling LaTeX documents."""

    @abstractmethod
    def compile(self, descriptor: FileDescriptor) -> Optional[CompilationResult]:
        """Compile the descriptor and return metadata or None on failure."""

    @abstractmethod
    def cleanup(self, descriptor: FileDescriptor) -> None:
        """Remove tool-specific artefacts."""
