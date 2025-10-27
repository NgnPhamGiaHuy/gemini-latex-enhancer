"""
Enhance route for CV enhancement
"""

from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from app.services.ai_service import AIService
from app.services.file_service import FileService
from app.services.latex_service import LatexService
from app.services.validation import ValidationService
from app.utils.response_builder import ResponseBuilder
from app.utils.logger import get_logger
from typing import Optional
import os
from app.services.job_parser import JobFileParser
from app.services.output_manager import OutputManager
from app.services.progress_service import ProgressService
import uuid

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
        # Validate inputs
        job_data = {
            "job_title": job_title,
            "job_description": job_description,
            "company_name": company_name,
        }
        ValidationService.validate_job_data(job_data)
        ValidationService.validate_latex_content(latex_content)

        # Initialize AI service with selected model
        logger.info("Initializing AI service for enhancement...")
        if model_id:
            logger.info(f"Using selected model: {model_id}")
        else:
            logger.info("Using default model")
        ai_service = AIService(model_id=model_id)

        # Enhance CV
        enhanced_latex = ai_service.enhance_cv(latex_content, job_data, slice_projects)

        # Validate enhanced LaTeX content
        if not LatexService.validate_latex_content(enhanced_latex):
            logger.error("Enhanced LaTeX content validation failed")
            raise HTTPException(
                status_code=500, detail="Enhanced LaTeX content is invalid"
            )

        # Save enhanced LaTeX
        if original_filename:
            tex_path, clean_tex_filename = FileService.save_result_with_job_info(
                enhanced_latex, original_filename, job_title, company_name
            )
        else:
            tex_path = FileService.save_result(enhanced_latex, "cv")
            clean_tex_filename = os.path.basename(tex_path)

        # Compile to PDF
        pdf_path = LatexService.compile_to_pdf(tex_path)

        if not pdf_path:
            logger.warning(
                "PDF compilation failed, but LaTeX file was created successfully"
            )
            # Continue without PDF - user can still download LaTeX file

        # Clean up LaTeX auxiliary files
        LatexService.cleanup_latex_files(tex_path)

        # Get relative paths for response
        tex_relative = FileService.get_relative_path(tex_path)
        pdf_relative = FileService.get_relative_path(pdf_path) if pdf_path else None

        # Generate clean PDF filename for download (convert .tex to .pdf)
        clean_pdf_filename = None
        if pdf_path and clean_tex_filename:
            # Convert the clean LaTeX filename to PDF filename
            clean_pdf_filename = clean_tex_filename.replace(".tex", ".pdf")

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
):
    """Batch-enhance a CV for multiple jobs defined in a CSV or JSON file.

    The file must include fields for Job Title and Job Description; Company Name
    is optional. Supports flexible field naming (e.g., "job title", "position_title", etc.).
    Produces per-job LaTeX/PDF files and a zip archive.

    Args:
        session_id: Progress/session identifier.
        latex_content: Source LaTeX CV.
        model_id: Optional model selection.
        job_file: CSV or JSON file upload listing job entries.
        slice_projects: Enable intelligent project selection.

    Returns:
        Success response containing results array and `zip_path`.
    """
    try:
        jobs = await JobFileParser.parse(job_file)

        # Initialize progress
        ProgressService.init(
            session_id, total=len(jobs), message="Starting batch enhancement"
        )
        # Nudge UI off 10%
        ProgressService.update(
            session_id, current=0, message=f"Queued {len(jobs)} jobs"
        )

        main_folder = OutputManager.create_main_output_folder()
        ai_service = AIService(model_id=model_id)

        # Derive original CV base name for output naming
        original_cv_name = (
            original_filename.replace(".tex", "") if original_filename else "OriginalCV"
        )
        results = []

        for idx, job in enumerate(jobs, start=1):
            logger.info(f"[Batch] Processing job {idx}/{len(jobs)}: {job['job_title']}")
            try:
                enhanced_latex = ai_service.enhance_cv(
                    latex_content, job, slice_projects
                )

                # Validate LaTeX
                is_valid = LatexService.validate_latex_content(enhanced_latex)
                if not is_valid:
                    logger.error("[Batch] Enhanced LaTeX invalid; skipping PDF compile")

                # Create subfolder and filenames
                subfolder = OutputManager.create_job_subfolder(
                    main_folder, job.get("company_name"), job["job_title"]
                )
                if original_filename:
                    tex_name, pdf_name = (
                        OutputManager.build_result_filenames_with_original_name(
                            original_filename, job.get("company_name"), job["job_title"]
                        )
                    )
                else:
                    tex_name, pdf_name = OutputManager.build_result_filenames(
                        original_cv_name, job.get("company_name"), job["job_title"]
                    )

                tex_path = os.path.join(subfolder, tex_name)
                with open(tex_path, "w", encoding="utf-8") as f:
                    f.write(enhanced_latex)

                pdf_path = None
                if is_valid:
                    pdf_path = LatexService.compile_to_pdf(tex_path)
                    LatexService.cleanup_latex_files(tex_path)

                results.append(
                    {
                        "job_title": job["job_title"],
                        "company_name": job.get("company_name"),
                        "tex_path": FileService.get_relative_path(tex_path),
                        "pdf_path": (
                            FileService.get_relative_path(pdf_path)
                            if pdf_path
                            else None
                        ),
                    }
                )
                ProgressService.increment(
                    session_id, 1, message=f"Completed {idx} of {len(jobs)}"
                )
            except Exception as job_err:
                logger.error(f"[Batch] Failed job {idx}: {str(job_err)}")
                ProgressService.mark_error(session_id)
                continue

        zip_path = OutputManager.zip_folder(main_folder)
        zip_rel = FileService.get_relative_path(zip_path)

        ProgressService.complete(
            session_id, zip_path=zip_rel, message="Batch enhancement completed"
        )

        return ResponseBuilder.success_response(
            data={
                "session_id": session_id,
                "jobs_count": len(results),
                "results": results,
                "zip_path": zip_rel,
            },
            message="Batch enhancement completed",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch enhancement failed: {str(e)}", exc_info=True)
        ProgressService.fail(session_id, message="Batch enhancement failed")
        raise HTTPException(
            status_code=500, detail=f"Batch enhancement failed: {str(e)}"
        )


@router.get("/progress")
async def get_progress(session_id: str):
    """Return progress for a given session as counts and percentage.

    Args:
        session_id: Identifier used when starting the batch.

    Returns:
        Success response with `current`, `total`, `percent`, `status`, `message`.
    """
    state = ProgressService.get(session_id)
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
async def preview_file(file: UploadFile = File(...)):
    """Preview the file headers and first rows with quoted-field handling.

    Args:
        file: CSV or JSON file containing job entries.

    Returns:
        Success response with `headers` and `rows` (up to a small limit).
    """
    try:
        headers, rows = await JobFileParser.preview(file)

        return ResponseBuilder.success_response(
            data={
                "headers": headers,
                "rows": rows,
            },
            message="File preview generated",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File preview failed: {str(e)}")
