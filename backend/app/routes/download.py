"""
Download route for file downloads with enhanced security
"""

import re
import urllib.parse
from fastapi import APIRouter, HTTPException, Path, Query, Request
from fastapi.responses import FileResponse, Response
from app.config import settings
from app.utils.logger import get_logger
from app.utils.filename_sanitizer import sanitize_filename_for_download
import os

router = APIRouter()
logger = get_logger(__name__)


@router.get("/download/{filename}")
async def download_file(filename: str = Path(...), request: Request = None):
    """Download a produced `.tex` or `.pdf` from the session outputs directory with security validation.

    Args:
        filename: Basename of the file to download (no path traversal allowed).
        request: FastAPI request object to access query parameters safely.

    Returns:
        FileResponse with the appropriate media type and Content-Disposition header.
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
        file_path = os.path.join(settings.SESSION_OUTPUT_DIR, sanitized_filename)

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

        # Handle download_name query parameter safely
        final_download_name = sanitized_filename
        if request and "download_name" in request.query_params:
            try:
                # URL decode the download_name parameter safely
                download_name_encoded = request.query_params["download_name"]
                download_name = urllib.parse.unquote(download_name_encoded)

                # Sanitize the decoded download name
                final_download_name = sanitize_filename_for_download(download_name)
                if not final_download_name:
                    final_download_name = sanitized_filename

                logger.info(
                    f"Download name decoded: {download_name} -> {final_download_name}"
                )
            except Exception as decode_error:
                logger.warning(f"Failed to decode download_name: {decode_error}")
                final_download_name = sanitized_filename

        logger.info(f"File downloaded: {sanitized_filename} as {final_download_name}")

        # Create Content-Disposition header with proper encoding
        # Use RFC 5987 encoding for non-ASCII characters
        try:
            # Try to encode as ASCII first
            final_download_name.encode("ascii")
            content_disposition = f'attachment; filename="{final_download_name}"'
        except UnicodeEncodeError:
            # If ASCII encoding fails, use RFC 5987 encoding
            encoded_name = urllib.parse.quote(final_download_name, safe="")
            content_disposition = f"attachment; filename*=UTF-8''{encoded_name}"

        return FileResponse(
            path=file_path,
            media_type=media_type,
            filename=final_download_name,
            headers={"Content-Disposition": content_disposition},
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")
