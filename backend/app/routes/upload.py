"""
Upload route for handling CV file uploads.
"""

from fastapi import APIRouter, UploadFile, HTTPException, Depends

from app.application.use_cases.upload_cv import UploadCvUseCase
from app.domain.exceptions import DomainValidationError
from app.interface.di import upload_cv_use_case
from app.utils.response_builder import ResponseBuilder
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/upload")
async def upload_cv(
    file: UploadFile,
    model_id: str = None,
    use_case: UploadCvUseCase = Depends(upload_cv_use_case),
):
    """Upload a `.tex` CV, validate it, and return parsed sections."""
    logger.info("=== UPLOAD REQUEST STARTED ===")
    logger.info("File received: %s", file.filename)
    logger.info("Content type: %s", file.content_type)

    try:
        content = await file.read()
        logger.info("Read %s bytes from upload", len(content))

        result = use_case.execute(filename=file.filename or "", content=content)
        logger.info(
            "✅ Upload processed successfully for session %s", result.session_id
        )

        response_data = {
            "session_id": result.session_id,
            "sections": result.sections,
            "original_filename": result.original_filename,
        }

        return ResponseBuilder.success_response(
            data=response_data, message="CV uploaded and processed successfully"
        )

    except DomainValidationError as exc:
        logger.warning("Upload validation failed: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except HTTPException:
        raise
    except RuntimeError as exc:
        logger.error("❌ Runtime error in upload: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        logger.error("❌ Unexpected error in upload: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Upload failed: {exc}")
