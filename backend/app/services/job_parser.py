"""
CSV Job Parser Service.

Parses CSV uploads that define multiple job entries for batch enhancement.
Performs basic header normalization and row validation, returning canonical
dicts consumable by the enhancement pipeline.
"""

import csv
from io import StringIO
from typing import List, Dict, Tuple
from fastapi import UploadFile, HTTPException

REQUIRED_HEADERS = ["job title", "job description"]
OPTIONAL_HEADERS = ["company name"]


class JobCSVParser:
    """Parse and validate CSV files for batch job enhancement."""

    @staticmethod
    async def parse(csv_file: UploadFile) -> List[Dict[str, str]]:
        """Parse a CSV file into a list of canonical job dictionaries.

        Each row is mapped to keys: `job_title`, `job_description`, and optional
        `company_name`. Invalid/empty rows are skipped.

        Args:
            csv_file: The uploaded CSV file from the client.

        Returns:
            A non-empty list of job dictionaries.

        Raises:
            HTTPException: If the file is missing/empty, has no headers, or
                contains no valid rows.
        """
        if not csv_file or not csv_file.filename:
            raise HTTPException(status_code=400, detail="No CSV file provided")

        try:
            # Read file content as text (UTF-8)
            raw_bytes = await csv_file.read()
            try:
                text = raw_bytes.decode("utf-8")
            except UnicodeDecodeError:
                text = raw_bytes.decode("utf-8", errors="ignore")

            if not text.strip():
                raise HTTPException(status_code=400, detail="CSV file is empty")

            csv_reader = csv.DictReader(StringIO(text))
            if not csv_reader.fieldnames:
                raise HTTPException(
                    status_code=400, detail="CSV file has no header row"
                )

            normalized_headers = [h.strip().lower() for h in csv_reader.fieldnames]

            # Validate required headers
            for required in REQUIRED_HEADERS:
                if required not in normalized_headers:
                    raise HTTPException(
                        status_code=400,
                        detail="CSV must include Job Title and Job Description columns.",
                    )

            # Map to canonical names
            header_map = {h.strip().lower(): h for h in csv_reader.fieldnames}

            jobs: List[Dict[str, str]] = []
            for row in csv_reader:
                job_title = (row.get(header_map.get("job title", "")) or "").strip()
                job_description = (
                    row.get(header_map.get("job description", "")) or ""
                ).strip()
                company_name = (
                    row.get(header_map.get("company name", "")) or ""
                ).strip()

                if not job_title and not job_description and not company_name:
                    continue

                if not job_title or not job_description:
                    # Skip invalid rows
                    continue

                jobs.append(
                    {
                        "job_title": job_title,
                        "job_description": job_description,
                        "company_name": company_name or None,
                    }
                )

            if not jobs:
                raise HTTPException(
                    status_code=400, detail="No valid job entries found in CSV"
                )

            return jobs

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to parse CSV: {str(e)}"
            )

    @staticmethod
    async def preview(
        csv_file: UploadFile, limit: int = 3
    ) -> Tuple[List[str], List[List[str]]]:
        """Return headers and first few rows, respecting quoted-field newlines.

        Args:
            csv_file: The uploaded CSV file.
            limit: Max number of data rows to include in the preview.

        Returns:
            A tuple of (headers, rows).
        """
        if not csv_file or not csv_file.filename:
            raise HTTPException(status_code=400, detail="No CSV file provided")

        try:
            raw_bytes = await csv_file.read()
            try:
                text = raw_bytes.decode("utf-8")
            except UnicodeDecodeError:
                text = raw_bytes.decode("utf-8", errors="ignore")

            if not text.strip():
                raise HTTPException(status_code=400, detail="CSV file is empty")

            reader = csv.reader(StringIO(text))
            rows = list(reader)
            if not rows:
                raise HTTPException(status_code=400, detail="CSV file has no data")

            headers = [h.strip() for h in rows[0]]
            data_rows = rows[1 : 1 + max(0, limit)]
            return headers, data_rows

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to preview CSV: {str(e)}"
            )
