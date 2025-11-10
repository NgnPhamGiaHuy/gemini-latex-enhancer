from __future__ import annotations

import csv
import json
from io import StringIO
from typing import Dict, List, Tuple

from fastapi import UploadFile, HTTPException

from app.application.contracts.job_data_parser import JobDataParser, JobParseResult
from app.domain.value_objects.job_context import JobContext

# Required fields in canonical form
REQUIRED_FIELDS = ["job_title", "job_description"]
OPTIONAL_FIELDS = ["company_name"]

# Flexible key mappings for normalization
KEY_MAPPINGS = {
    "job_title": [
        "job title",
        "job_title",
        "position title",
        "position_title",
        "title",
        "role",
        "position",
        "job",
        "job_name",
        "jobname",
        "job-title",
        "position-title",
        "role_title",
    ],
    "job_description": [
        "job description",
        "job_description",
        "description",
        "desc",
        "job_desc",
        "jobdesc",
        "job-desc",
        "position description",
        "position_description",
        "role description",
        "role_description",
        "responsibilities",
        "duties",
        "requirements",
    ],
    "company_name": [
        "company name",
        "company_name",
        "company",
        "employer",
        "company-name",
        "employer_name",
        "employer_name",
        "organization",
        "org",
        "org_name",
        "orgname",
        "firm",
        "firm_name",
    ],
}


class KeyNormalizer:
    """Optimized utility class for normalizing field names with O(1) lookup."""

    # Precomputed lookup table for O(1) access
    _NORMALIZED_LOOKUP: Dict[str, str] = {}
    _LOOKUP_BUILT = False

    @classmethod
    def _build_lookup_table(cls):
        """Build the normalized lookup table once for optimal performance."""
        if not cls._LOOKUP_BUILT:
            for canonical_field, variations in KEY_MAPPINGS.items():
                for variation in variations:
                    normalized_variation = (
                        variation.lower().replace(" ", "_").replace("-", "_")
                    )
                    cls._NORMALIZED_LOOKUP[normalized_variation] = canonical_field
            cls._LOOKUP_BUILT = True

    @staticmethod
    def normalize_key(key: str) -> str:
        """Normalize a key to its canonical form with O(1) lookup.

        Args:
            key: The input key to normalize.

        Returns:
            The canonical field name, or the original key if no mapping is found.
        """
        if not key:
            return key

        KeyNormalizer._build_lookup_table()

        clean_key = key.strip().lower().replace(" ", "_").replace("-", "_")
        return KeyNormalizer._NORMALIZED_LOOKUP.get(clean_key, clean_key)

    @staticmethod
    def normalize_dict(data: Dict[str, str]) -> Dict[str, str]:
        """Normalize all keys in a dictionary to canonical forms.

        Args:
            data: Dictionary with potentially non‑canonical keys.

        Returns:
            Dictionary with normalized keys.
        """
        normalized = {}
        for key, value in data.items():
            normalized_key = KeyNormalizer.normalize_key(key)
            normalized[normalized_key] = value
        return normalized


class CsvJsonJobParser(JobDataParser):
    """Parse and validate CSV and JSON files for batch job enhancement."""

    @staticmethod
    def _extract_job_fields(normalized_row: Dict[str, str]) -> Tuple[str, str, str]:
        """Extract job_title, job_description, and company_name from normalized row.

        Returns:
            Tuple of (job_title, job_description, company_name)
        """
        job_title = ""
        job_description = ""
        company_name = ""

        for field in KEY_MAPPINGS["job_title"]:
            if field in normalized_row and normalized_row[field]:
                job_title = str(normalized_row[field]).strip()
                break
        for field in KEY_MAPPINGS["job_description"]:
            if field in normalized_row and normalized_row[field]:
                job_description = str(normalized_row[field]).strip()
                break
        for field in KEY_MAPPINGS["company_name"]:
            if field in normalized_row and normalized_row[field]:
                company_name = str(normalized_row[field]).strip()
                break

        return job_title, job_description, company_name

    @staticmethod
    def _is_valid_job(job_title: str, job_description: str, company_name: str) -> bool:
        """Check if extracted fields form a valid job entry."""
        # Must have at least job_title and job_description
        return bool(job_title and job_description)

    async def parse(self, file: UploadFile) -> JobParseResult:
        file_extension = file.filename.lower().split(".")[-1]
        if file_extension == "csv":
            return await self._parse_csv(file)
        elif file_extension == "json":
            return await self._parse_json(file)
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload a CSV or JSON file.",
            )

    async def _parse_csv(self, csv_file: UploadFile) -> JobParseResult:
        try:
            raw_bytes = await csv_file.read()
            text = raw_bytes.decode("utf-8", errors="ignore")
            if not text.strip():
                raise HTTPException(status_code=400, detail="CSV file is empty")

            csv_reader = csv.DictReader(StringIO(text))
            if not csv_reader.fieldnames:
                raise HTTPException(
                    status_code=400, detail="CSV file has no header row"
                )

            normalized_headers = [
                KeyNormalizer.normalize_key(h) for h in csv_reader.fieldnames
            ]
            has_job_title = any(
                field in normalized_headers for field in KEY_MAPPINGS["job_title"]
            )
            has_job_description = any(
                field in normalized_headers for field in KEY_MAPPINGS["job_description"]
            )

            if not has_job_title or not has_job_description:
                raise HTTPException(
                    status_code=400,
                    detail="CSV must include Job Title and Job Description columns (or their variations).",
                )

            header_map = {
                original_header: KeyNormalizer.normalize_key(original_header)
                for original_header in csv_reader.fieldnames
            }

            jobs: List[JobContext] = []
            preview_rows: List[List[str]] = []
            for row in csv_reader:
                normalized_row = {
                    header_map.get(original_key, original_key): (value or "").strip()
                    for original_key, value in row.items()
                }

                job_title, job_description, company_name = self._extract_job_fields(
                    normalized_row
                )

                if not self._is_valid_job(job_title, job_description, company_name):
                    continue

                jobs.append(
                    JobContext(
                        job_title=job_title,
                        job_description=job_description,
                        company_name=company_name or None,
                    )
                )
                preview_rows.append([job_title, job_description, company_name or ""])

            if not jobs:
                raise HTTPException(
                    status_code=400, detail="No valid job entries found in CSV"
                )

            return JobParseResult(
                jobs=jobs, headers=normalized_headers, preview_rows=preview_rows
            )

        except HTTPException:
            raise
        except Exception as e:  # noqa: BLE001
            raise HTTPException(
                status_code=400, detail=f"Failed to parse CSV: {e}"
            ) from e

    async def _parse_json(self, json_file: UploadFile) -> JobParseResult:
        try:
            raw_bytes = await json_file.read()
            text = raw_bytes.decode("utf-8", errors="ignore")
            if not text.strip():
                raise HTTPException(status_code=400, detail="JSON file is empty")

            data = json.loads(text)
            if isinstance(data, dict):
                data = [data]
            elif not isinstance(data, list):
                raise HTTPException(
                    status_code=400,
                    detail="JSON must contain an array of job objects or a single job object",
                )

            if not data:
                raise HTTPException(status_code=400, detail="JSON file has no data")

            jobs: List[JobContext] = []
            preview_rows: List[List[str]] = []
            all_keys = set()

            for item in data:
                if not isinstance(item, dict):
                    continue

                normalized_item = KeyNormalizer.normalize_dict(item)
                all_keys.update(normalized_item.keys())

                job_title, job_description, company_name = self._extract_job_fields(
                    normalized_item
                )

                if not self._is_valid_job(job_title, job_description, company_name):
                    continue

                jobs.append(
                    JobContext(
                        job_title=job_title,
                        job_description=job_description,
                        company_name=company_name or None,
                    )
                )
                preview_rows.append([job_title, job_description, company_name or ""])

            if not jobs:
                raise HTTPException(
                    status_code=400, detail="No valid job entries found in JSON"
                )

            return JobParseResult(
                jobs=jobs, headers=sorted(list(all_keys)), preview_rows=preview_rows
            )

        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=400, detail=f"Invalid JSON format: {e}"
            ) from e
        except HTTPException:
            raise
        except Exception as e:  # noqa: BLE001
            raise HTTPException(
                status_code=400, detail=f"Failed to parse JSON: {e}"
            ) from e

    async def preview(
        self, file: UploadFile, limit: int = 3
    ) -> Tuple[List[str], List[List[str]]]:
        file_extension = file.filename.lower().split(".")[-1]
        if file_extension == "csv":
            return await self._preview_csv(file, limit)
        elif file_extension == "json":
            return await self._preview_json(file, limit)
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload a CSV or JSON file.",
            )

    async def _preview_csv(
        self, csv_file: UploadFile, limit: int = 3
    ) -> Tuple[List[str], List[List[str]]]:
        try:
            raw_bytes = await csv_file.read()
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
        except Exception as e:  # noqa: BLE001
            raise HTTPException(
                status_code=400, detail=f"Failed to preview CSV: {e}"
            ) from e

    async def _preview_json(
        self, json_file: UploadFile, limit: int = 3
    ) -> Tuple[List[str], List[List[str]]]:
        try:
            raw_bytes = await json_file.read()
            text = raw_bytes.decode("utf-8", errors="ignore")
            if not text.strip():
                raise HTTPException(status_code=400, detail="JSON file is empty")

            data = json.loads(text)
            if isinstance(data, dict):
                data = [data]
            elif not isinstance(data, list):
                raise HTTPException(
                    status_code=400,
                    detail="JSON must contain an array of job objects or a single job object",
                )

            if not data:
                raise HTTPException(status_code=400, detail="JSON file has no data")

            all_keys = set()
            for item in data:
                if isinstance(item, dict):
                    all_keys.update(item.keys())

            headers = sorted(list(all_keys))
            rows = []
            for item in data[:limit]:
                if isinstance(item, dict):
                    row = [str(item.get(key, "")) for key in headers]
                    rows.append(row)

            return headers, rows

        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=400, detail=f"Invalid JSON format: {e}"
            ) from e
        except HTTPException:
            raise
        except Exception as e:  # noqa: BLE001
            raise HTTPException(
                status_code=400, detail=f"Failed to preview JSON: {e}"
            ) from e
