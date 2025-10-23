"""
Job Parser Service for CSV and JSON files.

Parses CSV and JSON uploads that define multiple job entries for batch enhancement.
Performs flexible key normalization and validation, returning canonical
dicts consumable by the enhancement pipeline.
"""

import csv
import json
from io import StringIO
from typing import List, Dict, Tuple, Union
from fastapi import UploadFile, HTTPException

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

    # Pre-computed lookup table for O(1) access
    _NORMALIZED_LOOKUP: Dict[str, str] = {}
    _LOOKUP_BUILT = False

    @classmethod
    def _build_lookup_table(cls):
        """Build normalized lookup table once for optimal performance."""
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
            key: The input key to normalize

        Returns:
            The canonical field name, or the original key if no mapping found
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
            data: Dictionary with potentially non-canonical keys

        Returns:
            Dictionary with normalized keys
        """
        normalized = {}
        for key, value in data.items():
            normalized_key = KeyNormalizer.normalize_key(key)
            normalized[normalized_key] = value
        return normalized


class JobFileParser:
    """Parse and validate CSV and JSON files for batch job enhancement."""

    @staticmethod
    async def parse(file: UploadFile) -> List[Dict[str, str]]:
        """Parse a CSV or JSON file into a list of canonical job dictionaries.

        Each entry is mapped to keys: `job_title`, `job_description`, and optional
        `company_name`. Invalid/empty entries are skipped.

        Args:
            file: The uploaded CSV or JSON file from the client.

        Returns:
            A non-empty list of job dictionaries.

        Raises:
            HTTPException: If the file is missing/empty, has no valid entries, or
                contains no valid jobs.
        """
        if not file or not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")

        # Determine file type
        file_extension = file.filename.lower().split(".")[-1]

        if file_extension == "csv":
            return await JobFileParser._parse_csv(file)
        elif file_extension == "json":
            return await JobFileParser._parse_json(file)
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload a CSV or JSON file.",
            )

    @staticmethod
    async def _parse_csv(csv_file: UploadFile) -> List[Dict[str, str]]:
        """Parse a CSV file into canonical job dictionaries."""
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

            # Normalize headers using the key normalizer
            normalized_headers = [
                KeyNormalizer.normalize_key(h) for h in csv_reader.fieldnames
            ]

            # Check if we have the required fields after normalization
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

            # Create mapping from original headers to normalized keys
            header_map = {}
            for original_header in csv_reader.fieldnames:
                normalized_key = KeyNormalizer.normalize_key(original_header)
                header_map[original_header] = normalized_key

            jobs: List[Dict[str, str]] = []
            for row in csv_reader:
                # Normalize the row data
                normalized_row = {}
                for original_key, value in row.items():
                    normalized_key = header_map.get(original_key, original_key)
                    normalized_row[normalized_key] = (value or "").strip()

                # Extract required fields
                job_title = ""
                job_description = ""
                company_name = ""

                # Find job title using any of its variations
                for field in KEY_MAPPINGS["job_title"]:
                    if field in normalized_row and normalized_row[field]:
                        job_title = normalized_row[field]
                        break

                # Find job description using any of its variations
                for field in KEY_MAPPINGS["job_description"]:
                    if field in normalized_row and normalized_row[field]:
                        job_description = normalized_row[field]
                        break

                # Find company name using any of its variations
                for field in KEY_MAPPINGS["company_name"]:
                    if field in normalized_row and normalized_row[field]:
                        company_name = normalized_row[field]
                        break

                # Skip empty rows
                if not job_title and not job_description and not company_name:
                    continue

                # Skip rows missing required fields
                if not job_title or not job_description:
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
    async def _parse_json(json_file: UploadFile) -> List[Dict[str, str]]:
        """Parse a JSON file into canonical job dictionaries."""
        try:
            # Read file content as text (UTF-8)
            raw_bytes = await json_file.read()
            try:
                text = raw_bytes.decode("utf-8")
            except UnicodeDecodeError:
                text = raw_bytes.decode("utf-8", errors="ignore")

            if not text.strip():
                raise HTTPException(status_code=400, detail="JSON file is empty")

            try:
                data = json.loads(text)
            except json.JSONDecodeError as e:
                raise HTTPException(
                    status_code=400, detail=f"Invalid JSON format: {str(e)}"
                )

            # Handle both array of objects and single object
            if isinstance(data, dict):
                data = [data]
            elif not isinstance(data, list):
                raise HTTPException(
                    status_code=400,
                    detail="JSON must contain an array of job objects or a single job object",
                )

            jobs: List[Dict[str, str]] = []
            for item in data:
                if not isinstance(item, dict):
                    continue  # Skip non-object entries

                # Normalize the keys in this item
                normalized_item = KeyNormalizer.normalize_dict(item)

                # Extract required fields using flexible matching
                job_title = ""
                job_description = ""
                company_name = ""

                # Find job title using any of its variations
                for field in KEY_MAPPINGS["job_title"]:
                    if field in normalized_item and normalized_item[field]:
                        job_title = str(normalized_item[field]).strip()
                        break

                # Find job description using any of its variations
                for field in KEY_MAPPINGS["job_description"]:
                    if field in normalized_item and normalized_item[field]:
                        job_description = str(normalized_item[field]).strip()
                        break

                # Find company name using any of its variations
                for field in KEY_MAPPINGS["company_name"]:
                    if field in normalized_item and normalized_item[field]:
                        company_name = str(normalized_item[field]).strip()
                        break

                # Skip empty entries
                if not job_title and not job_description and not company_name:
                    continue

                # Skip entries missing required fields
                if not job_title or not job_description:
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
                    status_code=400, detail="No valid job entries found in JSON"
                )

            return jobs

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to parse JSON: {str(e)}"
            )

    @staticmethod
    async def preview(
        file: UploadFile, limit: int = 3
    ) -> Tuple[List[str], List[List[str]]]:
        """Return headers and first few entries for CSV/JSON files.

        Args:
            file: The uploaded CSV or JSON file.
            limit: Max number of data entries to include in the preview.

        Returns:
            A tuple of (headers, rows).
        """
        if not file or not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")

        # Determine file type
        file_extension = file.filename.lower().split(".")[-1]

        if file_extension == "csv":
            return await JobFileParser._preview_csv(file, limit)
        elif file_extension == "json":
            return await JobFileParser._preview_json(file, limit)
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload a CSV or JSON file.",
            )

    @staticmethod
    async def _preview_csv(
        csv_file: UploadFile, limit: int = 3
    ) -> Tuple[List[str], List[List[str]]]:
        """Preview CSV file headers and first few rows."""
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

    @staticmethod
    async def _preview_json(
        json_file: UploadFile, limit: int = 3
    ) -> Tuple[List[str], List[List[str]]]:
        """Preview JSON file structure and first few entries."""
        try:
            raw_bytes = await json_file.read()
            try:
                text = raw_bytes.decode("utf-8")
            except UnicodeDecodeError:
                text = raw_bytes.decode("utf-8", errors="ignore")

            if not text.strip():
                raise HTTPException(status_code=400, detail="JSON file is empty")

            try:
                data = json.loads(text)
            except json.JSONDecodeError as e:
                raise HTTPException(
                    status_code=400, detail=f"Invalid JSON format: {str(e)}"
                )

            # Handle both array of objects and single object
            if isinstance(data, dict):
                data = [data]
            elif not isinstance(data, list):
                raise HTTPException(
                    status_code=400,
                    detail="JSON must contain an array of job objects or a single job object",
                )

            if not data:
                raise HTTPException(status_code=400, detail="JSON file has no data")

            # Get all unique keys from all objects
            all_keys = set()
            for item in data:
                if isinstance(item, dict):
                    all_keys.update(item.keys())

            headers = sorted(list(all_keys))

            # Convert first few objects to rows
            rows = []
            for item in data[:limit]:
                if isinstance(item, dict):
                    row = [str(item.get(key, "")) for key in headers]
                    rows.append(row)

            return headers, rows

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to preview JSON: {str(e)}"
            )


# Backward compatibility alias
JobCSVParser = JobFileParser
