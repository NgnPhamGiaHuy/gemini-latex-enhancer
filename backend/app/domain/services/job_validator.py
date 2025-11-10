from __future__ import annotations

from typing import Dict, Any

from app.domain.exceptions import DomainValidationError


class JobValidator:
    """Domain validation for job payloads."""

    MAX_TITLE = 200
    MAX_DESCRIPTION = 15000
    MAX_COMPANY = 100

    REQUIRED_FIELDS = ("job_title", "job_description")

    @classmethod
    def validate(cls, job_data: Dict[str, Any]) -> None:
        for field in cls.REQUIRED_FIELDS:
            value = job_data.get(field)
            if not value or not str(value).strip():
                raise DomainValidationError(f"Field '{field}' is required")

        if len(job_data["job_title"]) > cls.MAX_TITLE:
            raise DomainValidationError(
                f"Job title too long (max {cls.MAX_TITLE} characters)"
            )

        if len(job_data["job_description"]) > cls.MAX_DESCRIPTION:
            raise DomainValidationError(
                f"Job description too long (max {cls.MAX_DESCRIPTION} characters)"
            )

        company_name = job_data.get("company_name")
        if company_name and len(company_name) > cls.MAX_COMPANY:
            raise DomainValidationError(
                f"Company name too long (max {cls.MAX_COMPANY} characters)"
            )
