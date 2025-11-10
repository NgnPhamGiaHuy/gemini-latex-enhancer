"""
Response builder utility for consistent API responses.

Standardizes success and error payloads returned by the API to simplify the
frontend and logs basic response metadata for observability.
"""

from typing import Any, Dict, Optional
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ResponseBuilder:
    """Utility for building consistent API responses."""

    @staticmethod
    def success_response(data: Any, message: str = "Success") -> JSONResponse:
        """Build a 200 success response with a conventional payload shape.

        Args:
            data: Arbitrary payload object to return under `data`.
            message: Short human-friendly message.

        Returns:
            FastAPI `JSONResponse` with status 200.
        """
        logger.info(f"=== BUILDING SUCCESS RESPONSE ===")
        logger.info(f"Message: {message}")
        logger.info(f"Data type: {type(data)}")
        logger.info(
            f"Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}"
        )

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    logger.info(f"  {key}: {len(value)} characters")
                elif isinstance(value, list):
                    logger.info(f"  {key}: {len(value)} items")
                else:
                    logger.info(f"  {key}: {type(value)}")

        response_content = {"success": True, "message": message, "data": data}

        logger.info(f"✅ Response built successfully")
        logger.debug(f"Response content: {response_content}")

        return JSONResponse(status_code=200, content=response_content)

    @staticmethod
    def error_response(
        message: str, status_code: int = 400, details: Optional[Dict] = None
    ) -> JSONResponse:
        """Build a non-200 error response with a standard error envelope.

        Args:
            message: Short error message suitable for end users.
            status_code: HTTP status code to use.
            details: Optional structured details for debugging/UX.

        Returns:
            FastAPI `JSONResponse` with the given status code.
        """
        content = {
            "success": False,
            "message": message,
            "error": {"code": status_code, "message": message},
        }

        if details:
            content["error"]["details"] = details

        return JSONResponse(status_code=status_code, content=content)

    @staticmethod
    def validation_error_response(errors: Dict[str, str]) -> JSONResponse:
        """Build a 422 validation error response with detailed field errors."""
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": "Validation error",
                "error": {
                    "code": 422,
                    "message": "Validation error",
                    "details": errors,
                },
            },
        )
