from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.latex_document import LatexDocument
from app.domain.value_objects.job_context import JobContext


class CvEnhancer(ABC):
    """Contract for AI or rule-based CV enhancement providers."""

    @abstractmethod
    def enhance(
        self,
        document: LatexDocument,
        job_context: JobContext,
        *,
        session_id: str | None = None,
    ) -> LatexDocument:
        """Return an enhanced LaTeX document."""
