from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict

from app.application.contracts import CvEnhancer
from app.domain.entities.latex_document import LatexDocument
from app.domain.services.job_validator import JobValidator
from app.domain.value_objects.job_context import JobContext


@dataclass(frozen=True)
class EnhanceCvResult:
    enhanced_document: LatexDocument
    job_context: JobContext


class EnhanceCvUseCase:
    """Coordinate the AI enhancement pipeline."""

    def __init__(
        self,
        *,
        enhancer: CvEnhancer,
        enhancer_factory: Callable[[str], CvEnhancer] | None = None,
    ) -> None:
        self._default_enhancer = enhancer
        self._enhancer_factory = enhancer_factory

    def execute(
        self,
        *,
        latex_content: str,
        job_data: Dict[str, Any],
        session_id: str | None = None,
        slice_projects: bool = False,
        model_id: str | None = None,
    ) -> EnhanceCvResult:
        JobValidator.validate(job_data)
        original_document = LatexDocument(latex_content).assert_valid()
        job_context = JobContext(
            job_title=job_data.get("job_title", ""),
            job_description=job_data.get("job_description", ""),
            company_name=job_data.get("company_name"),
        ).trimmed()

        enhancer = self._resolve_enhancer(model_id)

        enhanced_document = enhancer.enhance(
            original_document,
            job_context,
            session_id=session_id,
            slice_projects=slice_projects,
        )

        return EnhanceCvResult(
            enhanced_document=enhanced_document,
            job_context=job_context,
        )

    def _resolve_enhancer(self, model_id: str | None) -> CvEnhancer:
        if (
            model_id
            and self._enhancer_factory
            and model_id != getattr(self._default_enhancer, "model_id", None)
        ):
            return self._enhancer_factory(model_id)
        return self._default_enhancer
