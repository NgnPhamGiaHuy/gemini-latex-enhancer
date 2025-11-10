from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from app.application.contracts import OutputPackager, ProgressTracker
from app.application.exceptions import ApplicationError
from app.application.use_cases.enhance_cv import EnhanceCvUseCase
from app.application.use_cases.save_and_compile import SaveAndCompileUseCase
from app.domain.exceptions import DomainValidationError
from app.domain.value_objects.job_context import JobContext
from app.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class BatchEnhanceResult:
    results: List[Dict[str, Optional[str]]]
    zip_path: str


class BatchEnhanceUseCase:
    """Coordinate batch enhancements with progress reporting."""

    def __init__(
        self,
        *,
        enhance_use_case: EnhanceCvUseCase,
        save_use_case: SaveAndCompileUseCase,
        packager: OutputPackager,
        progress_tracker: ProgressTracker,
    ) -> None:
        self._enhance_use_case = enhance_use_case
        self._save_use_case = save_use_case
        self._packager = packager
        self._progress_tracker = progress_tracker

    def execute(
        self,
        *,
        session_id: str,
        latex_content: str,
        jobs: List[JobContext],
        original_filename: Optional[str],
        slice_projects: bool,
        model_id: Optional[str],
    ) -> BatchEnhanceResult:
        """Execute batch enhancement.

        Note: Progress tracker should be initialized before calling this method.
        This method assumes the tracker is already initialized and will update
        progress as jobs are processed.

        Args:
            session_id: Session identifier for progress tracking.
            latex_content: Source LaTeX CV content.
            jobs: List of job contexts to process.
            original_filename: Original filename of the CV.
            slice_projects: Whether to slice projects.
            model_id: Optional model ID override.

        Returns:
            BatchEnhanceResult with processed results and zip path.

        Raises:
            DomainValidationError: If no jobs provided.
        """
        if not jobs:
            raise DomainValidationError("No jobs provided")

        main_folder = Path(self._packager.create_main_folder())
        # Note: Progress tracker initialization is handled by the route handler
        # to allow immediate return while processing happens in background.

        results: List[Dict[str, Optional[str]]] = []

        for idx, job in enumerate(jobs, start=1):
            try:
                enhance_result = self._enhance_use_case.execute(
                    latex_content=latex_content,
                    job_data={
                        "job_title": job.job_title,
                        "job_description": job.job_description,
                        "company_name": job.company_name,
                    },
                    session_id=session_id,
                    slice_projects=slice_projects,
                    model_id=model_id,
                )

                save_result = self._save_use_case.execute(
                    latex_content=enhance_result.enhanced_document.content,
                    original_filename=original_filename,
                    job_title=job.job_title,
                    company_name=job.company_name,
                    output_root=main_folder,
                    use_subfolder=True,
                )

                results.append(
                    {
                        "job_title": job.job_title,
                        "company_name": job.company_name,
                        "tex_path": save_result.tex_relative_path,
                        "pdf_path": save_result.pdf_relative_path,
                    }
                )
                self._progress_tracker.increment(
                    session_id,
                    message=f"Completed {idx} of {len(jobs)}",
                )
            except DomainValidationError as exc:
                logger.warning("Validation failed for job %s: %s", idx, exc)
                self._progress_tracker.mark_error(session_id)
                self._progress_tracker.increment(session_id)
                continue
            except ApplicationError as exc:
                logger.error("Saving outputs failed for job %s: %s", idx, exc)
                self._progress_tracker.mark_error(session_id)
                self._progress_tracker.increment(session_id)
                continue
            except Exception as exc:  # noqa: BLE001
                logger.error("Batch job %s failed: %s", idx, exc, exc_info=True)
                self._progress_tracker.mark_error(session_id)
                self._progress_tracker.increment(session_id)
                continue

        zip_path = self._packager.zip_folder(main_folder)
        zip_relative = self._packager.to_relative_path(zip_path)
        self._progress_tracker.complete(
            session_id, zip_path=zip_relative, message="Batch enhancement completed"
        )

        return BatchEnhanceResult(results=results, zip_path=zip_relative)
