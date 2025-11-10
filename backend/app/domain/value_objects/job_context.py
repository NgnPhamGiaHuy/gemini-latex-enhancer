from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class JobContext:
    """Value object representing the target role for CV enhancement."""

    job_title: str
    job_description: str
    company_name: Optional[str] = None

    def trimmed(
        self, max_title: int = 200, max_description: int = 15000
    ) -> "JobContext":
        return JobContext(
            job_title=self.job_title[:max_title],
            job_description=self.job_description[:max_description],
            company_name=self.company_name,
        )
