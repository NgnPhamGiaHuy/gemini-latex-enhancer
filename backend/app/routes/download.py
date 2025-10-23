"""
Download route for file downloads with enhanced security
"""

import re
from fastapi import APIRouter, HTTPException, Path
from fastapi.responses import FileResponse
from app.config import settings
from app.utils.logger import get_logger
import os

router = APIRouter()
logger = get_logger(__name__)


@router.get("/download/{filename}")
async def download_file(filename: str = Path(...)):
    """Download a produced `.tex` or `.pdf` from the outputs directory with security validation.

    Args:
        filename: Basename of the file to download (no path traversal allowed).

    Returns:
        FileResponse with the appropriate media type.
    """
    try:
        # Sanitize filename to prevent path traversal attacks
        sanitized_filename = re.sub(r"[^a-zA-Z0-9._-]", "", filename)

        # Additional security check - ensure no path traversal attempts
        if ".." in filename or "/" in filename or "\\" in filename:
            logger.warning(f"Path traversal attempt detected: {filename}")
            raise HTTPException(status_code=400, detail="Invalid filename")

        # Ensure filename is not empty after sanitization
        if not sanitized_filename:
            raise HTTPException(status_code=400, detail="Invalid filename")

        # Construct full path with sanitized filename
        file_path = os.path.join(settings.OUTPUT_DIR, sanitized_filename)

        # Check if file exists
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {sanitized_filename}")
            raise HTTPException(status_code=404, detail="File not found")

        # Determine media type
        if sanitized_filename.endswith(".pdf"):
            media_type = "application/pdf"
        elif sanitized_filename.endswith(".tex"):
            media_type = "text/plain"
        elif sanitized_filename.endswith(".zip"):
            media_type = "application/zip"
        else:
            media_type = "application/octet-stream"

        logger.info(f"File downloaded: {sanitized_filename}")

        return FileResponse(
            path=file_path, media_type=media_type, filename=sanitized_filename
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")
