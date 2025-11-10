"""
Enhance route for CV enhancement.
"""

from typing import Optional

from fastapi import (
    APIRouter,
    HTTPException,
    Form,
    UploadFile,
    File,
    Depends,
    BackgroundTasks,
)

from app.application.exceptions import ApplicationError
from app.application.use_cases.batch_enhance import BatchEnhanceUseCase
from app.application.use_cases.enhance_cv import EnhanceCvUseCase
from app.application.use_cases.parse_job_file import ParseJobFileUseCase
from app.application.use_cases.save_and_compile import SaveAndCompileUseCase
from app.domain.exceptions import DomainValidationError
from app.interface.di import (
    enhance_cv_use_case,
    parse_job_use_case,
    save_and_compile_use_case,
    batch_enhance_use_case,
    get_progress_tracker,
)
from app.application.contracts.progress_tracker import ProgressTracker
from app.infrastructure.execution.background_job_executor import BackgroundJobExecutor
from app.utils.response_builder import ResponseBuilder
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/enhance")
async def enhance_cv(
    session_id: str = Form(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    company_name: str = Form(None),
    latex_content: str = Form(...),
    original_filename: str = Form(None),
    model_id: str = Form(None),
    slice_projects: bool = Form(False),
    use_case: EnhanceCvUseCase = Depends(enhance_cv_use_case),
    save_use_case: SaveAndCompileUseCase = Depends(save_and_compile_use_case),
):
    """Enhance a LaTeX CV for a specific job.

    Args:
        session_id: Client-generated UUID to correlate backend progress.
        job_title: Target job title.
        job_description: Full job description text.
        company_name: Optional company/employer name.
        latex_content: Raw LaTeX CV content to enhance.
        original_filename: Original filename of the uploaded CV.
        model_id: Optional model override; defaults to system config.
        slice_projects: If True, select the most relevant personal projects only.

    Returns:
        Success response with relative `tex_path` and optional `pdf_path`.

    Raises:
        HTTPException: On validation failure or enhancement/compilation errors.
    """
    try:
        job_data = {
            "job_title": job_title,
            "job_description": job_description,
            "company_name": company_name,
        }

        logger.info("Initializing enhancement pipeline via use case...")
        enhance_result = use_case.execute(
            latex_content=latex_content,
            job_data=job_data,
            session_id=session_id,
            slice_projects=slice_projects,
            model_id=model_id,
        )
        enhanced_latex = enhance_result.enhanced_document.content

        sc_result = save_use_case.execute(
            latex_content=enhanced_latex,
            original_filename=original_filename,
            job_title=job_title,
            company_name=company_name,
        )
        tex_relative = sc_result.tex_relative_path
        pdf_relative = sc_result.pdf_relative_path
        clean_tex_filename = sc_result.clean_tex_filename
        clean_pdf_filename = sc_result.clean_pdf_filename

        if not pdf_relative:
            logger.warning(
                "PDF compilation failed or PDF unavailable; returning LaTeX only"
            )

        logger.info(f"CV enhanced successfully. Session ID: {session_id}")
        logger.info(f"LaTeX file: {tex_relative}")
        logger.info(f"PDF file: {pdf_relative}")
        logger.info(
            f"Clean filenames - LaTeX: {clean_tex_filename}, PDF: {clean_pdf_filename}"
        )

        return ResponseBuilder.success_response(
            data={
                "session_id": session_id,
                "tex_path": tex_relative,
                "pdf_path": pdf_relative,
                "clean_tex_filename": clean_tex_filename,
                "clean_pdf_filename": clean_pdf_filename,
            },
            message="CV enhanced successfully",
        )

    except DomainValidationError as exc:
        logger.warning("Enhancement validation failed: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ApplicationError as exc:
        logger.error("Save/compile failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enhancement failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Enhancement failed: {str(e)}")


@router.post("/enhance/batch")
async def enhance_cv_batch(
    session_id: str = Form(...),
    latex_content: str = Form(...),
    original_filename: str = Form(None),
    model_id: Optional[str] = Form(None),
    job_file: UploadFile = File(...),
    slice_projects: bool = Form(False),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    job_parser_use_case: ParseJobFileUseCase = Depends(parse_job_use_case),
    batch_use_case: BatchEnhanceUseCase = Depends(batch_enhance_use_case),
    tracker: ProgressTracker = Depends(get_progress_tracker),
):
    """Batch-enhance a CV for multiple jobs defined in a CSV or JSON file.

    The file must include fields for Job Title and Job Description; Company Name
    is optional. Supports flexible field naming (e.g., "job title", "position_title", etc.).
    Produces per-job LaTeX/PDF files and a zip archive.

    This endpoint returns immediately with a session_id. The batch processing
    runs in the background, and progress can be tracked via GET /api/progress.

    Args:
        session_id: Progress/session identifier.
        latex_content: Source LaTeX CV.
        model_id: Optional model selection.
        job_file: CSV or JSON file upload listing job entries.
        slice_projects: Enable intelligent project selection.
        background_tasks: FastAPI BackgroundTasks for async execution.

    Returns:
        Success response with session_id. Results available when status is "completed".
    """
    try:
        # Parse job file synchronously (fast operation)
        jobs = (await job_parser_use_case.execute(job_file)).jobs

        if not jobs:
            raise DomainValidationError("No jobs found in file")

        # Initialize progress tracker
        tracker.init(session_id, total=len(jobs), message="Starting batch enhancement")

        # Create job executor for background processing
        executor = BackgroundJobExecutor(background_tasks)

        # Define the batch processing function
        def process_batch() -> None:
            """Process batch jobs in background."""
            try:
                result = batch_use_case.execute(
                    session_id=session_id,
                    latex_content=latex_content,
                    jobs=jobs,
                    original_filename=original_filename,
                    slice_projects=slice_projects,
                    model_id=model_id,
                )
                logger.info(
                    f"Batch enhancement completed for session {session_id}: "
                    f"{len(result.results)} jobs processed"
                )
            except Exception as exc:
                logger.error(
                    f"Batch enhancement failed in background for session {session_id}: {exc}",
                    exc_info=True,
                )
                tracker.fail(session_id, message=f"Batch processing failed: {str(exc)}")

        # Execute in background and return immediately
        executor.execute_in_background(process_batch)

        # Return immediately with session_id for progress tracking
        return ResponseBuilder.success_response(
            data={
                "session_id": session_id,
                "jobs_count": len(jobs),
                "status": "processing",
                "message": "Batch enhancement started. Use GET /api/progress to track progress.",
            },
            message="Batch enhancement started",
        )

    except DomainValidationError as exc:
        tracker.fail(session_id, message=str(exc))
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch enhancement setup failed: {str(e)}", exc_info=True)
        tracker.fail(session_id, message="Batch enhancement setup failed")
        raise HTTPException(
            status_code=500, detail=f"Batch enhancement setup failed: {str(e)}"
        )


@router.get("/progress")
async def get_progress(
    session_id: str, tracker: ProgressTracker = Depends(get_progress_tracker)
):
    """Return progress for a given session as counts and percentage.

    Args:
        session_id: Identifier used when starting the batch.

    Returns:
        Success response with `current`, `total`, `percent`, `status`, `message`.
    """
    state = tracker.get(session_id)
    if not state:
        raise HTTPException(status_code=404, detail="No progress found for session")
    # Convert to percent progress for frontend convenience
    total = max(state.get("total", 0), 1)
    percent = int((state.get("current", 0) / total) * 100)
    return ResponseBuilder.success_response(
        data={
            "current": state.get("current", 0),
            "total": state.get("total", 0),
            "percent": percent,
            "status": state.get("status"),
            "message": state.get("message"),
            "zip_path": state.get("zip_path"),
            "errors": state.get("errors", 0),
        },
        message="Progress fetched",
    )


@router.post("/file/preview")
async def preview_file(
    file: UploadFile = File(...),
    parser_use_case: ParseJobFileUseCase = Depends(parse_job_use_case),
):
    """Preview the file headers and first rows with quoted-field handling.

    Args:
        file: CSV or JSON file containing job entries.
        parser_use_case: The ParseJobFileUseCase dependency.

    Returns:
        Success response with `headers` and `rows` (up to a small limit).
    """
    try:
        headers, rows = await parser_use_case.preview(file)

        return ResponseBuilder.success_response(
            data={
                "headers": headers,
                "rows": rows,
            },
            message="File preview generated",
        )
    except HTTPException:
        raise
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"File preview failed: {str(e)}")
