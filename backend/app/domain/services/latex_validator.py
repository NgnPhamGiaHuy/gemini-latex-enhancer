from __future__ import annotations

import re

from app.domain.exceptions import DomainValidationError


class LatexValidator:
    """Domain-level LaTeX validation utilities."""

    REQUIRED_MARKERS = (
        r"\\documentclass",
        r"\\begin\{document\}",
        r"\\end\{document\}",
    )

    @classmethod
    def validate(cls, content: str) -> None:
        if not content or not content.strip():
            raise DomainValidationError("LaTeX content cannot be empty")

        for marker in cls.REQUIRED_MARKERS:
            if not re.search(marker, content):
                human_marker = marker.replace("\\\\", "\\")
                raise DomainValidationError(
                    f"Invalid LaTeX document: missing {human_marker}"
                )
