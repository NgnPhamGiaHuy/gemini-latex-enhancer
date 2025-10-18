"""
Upload route for handling CV file uploads
"""

import re
from fastapi import APIRouter, UploadFile, HTTPException, Depends
from app.services.ai_service import AIService
from app.services.file_service import FileService
from app.services.validation import ValidationService
from app.utils.response_builder import ResponseBuilder
from app.utils.logger import get_logger
import uuid

router = APIRouter()
logger = get_logger(__name__)


@router.post("/upload")
async def upload_cv(file: UploadFile, model_id: str = None):
    """Upload a `.tex` CV, validate it, and return parsed sections.

    Args:
        file: Uploaded LaTeX file (.tex only).
        model_id: Optional AI model override.

    Returns:
        Success response with parsed `sections` and a new `session_id` for subsequent enhancement.

    Raises:
        HTTPException: On validation or processing errors.
    """
    logger.info(f"=== UPLOAD REQUEST STARTED ===")
    logger.info(f"File received: {file.filename}")
    logger.info(f"Content type: {file.content_type}")
    logger.info(f"File size: {file.size if hasattr(file, 'size') else 'unknown'}")

    try:
        # Validate file
        logger.info("Validating file...")
        ValidationService.validate_file_upload(file)
        logger.info("✅ File validation passed")

        # Save uploaded file
        logger.info("Saving uploaded file...")
        file_path = FileService.save_uploaded_file(file)
        logger.info(f"✅ File saved to: {file_path}")

        # Read LaTeX content
        logger.info("Reading LaTeX content...")
        latex_content = FileService.read_latex_content(file_path)
        logger.info(f"✅ LaTeX content read, length: {len(latex_content)} characters")
        logger.debug(f"LaTeX content preview: {latex_content[:200]}...")

        # Validate LaTeX content
        logger.info("Validating LaTeX content...")
        ValidationService.validate_latex_content(latex_content)
        logger.info("✅ LaTeX content validation passed")

        # Initialize AI service with selected model
        logger.info("Initializing AI service...")
        if model_id:
            logger.info(f"Using selected model: {model_id}")
        else:
            logger.info("Using default model")
        ai_service = AIService(model_id=model_id)
        logger.info("✅ AI service initialized")

        # Generate session ID
        session_id = str(uuid.uuid4())
        logger.info(f"✅ Session ID generated: {session_id}")

        # Parse sections from LaTeX (simplified - in real implementation, you'd parse LaTeX structure)
        logger.info("Parsing LaTeX sections...")
        sections = _parse_latex_sections(latex_content)
        logger.info(f"✅ Sections parsed: {len(sections)} sections found")
        logger.debug(f"Sections: {[s['title'] for s in sections]}")

        # Clean up uploaded file
        logger.info("Cleaning up uploaded file...")
        FileService.cleanup_file(file_path)
        logger.info("✅ File cleanup completed")

        response_data = {
            "session_id": session_id,
            "sections": sections,
        }

        logger.info(f"=== UPLOAD REQUEST COMPLETED SUCCESSFULLY ===")
        logger.info(f"Response data keys: {list(response_data.keys())}")

        return ResponseBuilder.success_response(
            data=response_data, message="CV uploaded and processed successfully"
        )

    except HTTPException as e:
        logger.error(f"❌ HTTP Exception in upload: {e.status_code} - {e.detail}")
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error in upload: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


def _parse_latex_sections(latex_content: str) -> list:
    """Extract a simple list of section titles from LaTeX content.

    This is a lightweight heuristic and not a full LaTeX parser; it targets
    common sectioning macros to give the UI a quick structural overview.

    Args:
        latex_content: Raw LaTeX text.

    Returns:
        A list of dict objects: {"title": str, "content": str}.
    """
    logger.info("Starting LaTeX section parsing...")
    sections = []

    # Look for common section commands
    section_patterns = [
        r"\\section\*?\{([^}]+)\}",
        r"\\subsection\*?\{([^}]+)\}",
        r"\\cvsection\{([^}]+)\}",
        r"\\cvsubsection\{([^}]+)\}",
    ]

    logger.info(f"Searching for sections in LaTeX content...")
    for i, pattern in enumerate(section_patterns):
        matches = re.findall(pattern, latex_content, re.IGNORECASE)
        logger.info(f"Pattern {i+1} ({pattern}): {len(matches)} matches")
        for match in matches:
            section_title = match.strip()
            logger.debug(f"Found section: {section_title}")
            sections.append(
                {
                    "title": section_title,
                    "content": f"Content for {section_title}",  # Simplified
                }
            )

    # If no sections found, create default ones
    if not sections:
        logger.warning("No sections found in LaTeX, creating default sections")
        sections = [
            {"title": "Education", "content": "Education section"},
            {"title": "Experience", "content": "Experience section"},
            {"title": "Skills", "content": "Skills section"},
        ]

    logger.info(f"Final sections count: {len(sections)}")
    return sections
