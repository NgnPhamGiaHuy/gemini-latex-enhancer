"""
Download route for file downloads
"""

from fastapi import APIRouter, HTTPException, Path
from fastapi.responses import FileResponse
from app.config import settings
from app.utils.logger import get_logger
import os

router = APIRouter()
logger = get_logger(__name__)


@router.get("/download/{filename}")
async def download_file(filename: str = Path(...)):
    """Download a produced `.tex` or `.pdf` from the outputs directory.

    Args:
        filename: Basename of the file to download (no path traversal allowed).

    Returns:
        FileResponse with the appropriate media type.
    """
    try:
        # Construct full path
        file_path = os.path.join(settings.OUTPUT_DIR, filename)

        # Check if file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Determine media type
        if filename.endswith(".pdf"):
            media_type = "application/pdf"
        elif filename.endswith(".tex"):
            media_type = "text/plain"
        else:
            media_type = "application/octet-stream"

        logger.info(f"File downloaded: {filename}")

        return FileResponse(path=file_path, media_type=media_type, filename=filename)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")
