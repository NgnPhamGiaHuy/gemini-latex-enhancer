"""
Validation Service for input sanity checks.

Provides lightweight validation helpers for LaTeX content, job data, and
uploaded files. These checks are intentionally simple and fast to fail early
before more expensive AI or LaTeX operations.
"""

import re
from typing import Dict, Any
from fastapi import HTTPException


class ValidationService:
    """Service providing fast validation routines for inputs."""

    @staticmethod
    def validate_latex_content(latex_content: str) -> bool:
        """Validate essential LaTeX document markers and non-emptiness.

        Args:
            latex_content: Raw LaTeX text.

        Returns:
            True when valid; raises HTTPException otherwise.
        """
        if not latex_content or len(latex_content.strip()) == 0:
            raise HTTPException(status_code=400, detail="LaTeX content cannot be empty")

        # Check for basic LaTeX structure
        if not re.search(r"\\documentclass", latex_content):
            raise HTTPException(
                status_code=400,
                detail="Invalid LaTeX document: missing \\documentclass",
            )

        if not re.search(r"\\begin\{document\}", latex_content):
            raise HTTPException(
                status_code=400,
                detail="Invalid LaTeX document: missing \\begin{document}",
            )

        if not re.search(r"\\end\{document\}", latex_content):
            raise HTTPException(
                status_code=400,
                detail="Invalid LaTeX document: missing \\end{document}",
            )

        return True

    @staticmethod
    def validate_job_data(job_data: Dict[str, Any]) -> bool:
        """Validate job payload for required fields and reasonable lengths.

        Args:
            job_data: Dict containing at least `job_title` and `job_description`.

        Returns:
            True when valid; raises HTTPException otherwise.
        """
        required_fields = ["job_title", "job_description"]

        for field in required_fields:
            if not job_data.get(field) or len(job_data.get(field, "").strip()) == 0:
                raise HTTPException(
                    status_code=400, detail=f"Field '{field}' is required"
                )

        # Validate job title length
        if len(job_data["job_title"]) > 200:
            raise HTTPException(
                status_code=400, detail="Job title too long (max 200 characters)"
            )

        # Validate job description length
        if len(job_data["job_description"]) > 15000:
            raise HTTPException(
                status_code=400,
                detail="Job description too long (max 15000 characters)",
            )

        # Validate company name if provided
        if job_data.get("company_name") and len(job_data["company_name"]) > 100:
            raise HTTPException(
                status_code=400, detail="Company name too long (max 100 characters)"
            )

        return True

    @staticmethod
    def validate_file_upload(file) -> bool:
        """Validate that an uploaded file is present and is a `.tex` file."""
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")

        if not file.filename.endswith(".tex"):
            raise HTTPException(status_code=400, detail="Only .tex files are allowed")

        return True

    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize arbitrary input for safe logging/storage.

        Removes potentially dangerous characters and truncates to a maximum length.
        Enhanced to handle more edge cases and provide better security.

        Args:
            text: Untrusted input string.

        Returns:
            A trimmed and cleaned string.
        """
        if not text:
            return ""

        # Remove potentially dangerous characters and patterns
        # Remove HTML/XML tags
        text = re.sub(r"<[^>]+>", "", text)

        # Remove script patterns
        text = re.sub(
            r"<script[^>]*>.*?</script>", "", text, flags=re.IGNORECASE | re.DOTALL
        )

        # Remove potentially dangerous characters
        text = re.sub(r'[<>"\']', "", text)

        # Remove control characters except newlines and tabs
        text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)

        # Remove excessive whitespace
        text = re.sub(r"\s+", " ", text)

        # Limit length
        if len(text) > 10000:
            text = text[:10000]
            # Try to cut at word boundary
            last_space = text.rfind(" ")
            if last_space > 8000:  # Only if we don't lose too much content
                text = text[:last_space]

        return text.strip()
