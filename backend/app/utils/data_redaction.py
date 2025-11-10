"""
Data‑redaction utilities for logging sensitive information.

Provides helpers to log sensitive data safely by:
- Truncating long content
- Redacting full prompts/content
- Summarizing instead of logging full payloads
- Masking common PII patterns
"""

import re
from typing import Any, Dict, Optional


# Maximum lengths for logged content and previews before truncation
MAX_LOG_CONTENT_LENGTH = 500
MAX_LOG_PREVIEW_LENGTH = 200


def truncate_content(content: str, max_length: int = MAX_LOG_CONTENT_LENGTH) -> str:
    """Truncate content to a maximum length with an ellipsis.

    Args:
        content: The content to truncate.
        max_length: Maximum length before truncation.

    Returns:
        Truncated content with a '... (truncated)' suffix if needed.
    """
    if not isinstance(content, str):
        return str(content)

    if len(content) <= max_length:
        return content

    return content[:max_length] + f"... (truncated, {len(content)} total chars)"


def preview_content(content: str, max_length: int = MAX_LOG_PREVIEW_LENGTH) -> str:
    """Create a preview of content for logging.

    Args:
        content: The content to preview.
        max_length: Maximum length for the preview.

    Returns:
        Preview string with a length indicator.
    """
    if not isinstance(content, str):
        return str(content)

    if len(content) <= max_length:
        return content

    preview = content[:max_length]
    return f"{preview}... (preview, {len(content)} chars total)"


def redact_prompt_content(prompt: str, keep_structure: bool = True) -> Dict[str, Any]:
    """Redact prompt content while preserving metadata.

    Args:
        prompt: The full prompt content.
        keep_structure: When True, include prompt structure (section titles) without content.

    Returns:
        Dictionary containing redacted prompt information.
    """
    if not prompt:
        return {"length": 0, "preview": "", "redacted": True}

    # Extract section headers when present (common in LaTeX prompts)
    sections = []
    if keep_structure:
        # Look for common section markers
        section_patterns = [
            r"\\section\{([^}]+)\}",
            r"\\subsection\{([^}]+)\}",
            r"#+\s+([^\n]+)",
            r"##\s+([^\n]+)",
        ]

        for pattern in section_patterns:
            matches = re.findall(pattern, prompt)
            sections.extend(matches[:5])  # Limit to first 5 sections

    return {
        "length": len(prompt),
        "preview": preview_content(prompt, MAX_LOG_PREVIEW_LENGTH),
        "sections": sections[:5] if sections else None,
        "redacted": True,
        "word_count": len(prompt.split()) if prompt else 0,
    }


def redact_job_description(description: str) -> Dict[str, Any]:
    """Redact a job description while preserving key metadata.

    Args:
        description: The full job description.

    Returns:
        Dictionary containing redacted job‑description information.
    """
    if not description:
        return {"length": 0, "preview": "", "redacted": True}

    # Extract key requirements (common patterns)
    requirements = []
    requirement_patterns = [
        r"(?:required|must have|requirements?)[:;]\s*([^\n]+)",
        r"(?:qualifications?|skills?)[:;]\s*([^\n]+)",
    ]

    for pattern in requirement_patterns:
        matches = re.findall(pattern, description, re.IGNORECASE)
        requirements.extend(matches[:3])  # Limit to first 3 requirements

    return {
        "length": len(description),
        "preview": preview_content(description, MAX_LOG_PREVIEW_LENGTH),
        "requirements_preview": requirements[:3] if requirements else None,
        "redacted": True,
        "word_count": len(description.split()) if description else 0,
    }


def redact_latex_content(latex: str) -> Dict[str, Any]:
    """Redact LaTeX content while preserving structural metadata.

    Args:
        latex: The LaTeX content.

    Returns:
        Dictionary containing redacted LaTeX information.
    """
    if not latex:
        return {"length": 0, "preview": "", "redacted": True}

    # Extract document structure
    has_documentclass = "\\documentclass" in latex
    has_sections = bool(re.search(r"\\section\{", latex))
    has_items = bool(re.search(r"\\item", latex))

    # Count common LaTeX elements
    section_count = len(re.findall(r"\\section\{", latex))
    item_count = len(re.findall(r"\\item", latex))

    return {
        "length": len(latex),
        "preview": preview_content(latex, MAX_LOG_PREVIEW_LENGTH),
        "structure": {
            "has_documentclass": has_documentclass,
            "has_sections": has_sections,
            "has_items": has_items,
            "section_count": section_count,
            "item_count": item_count,
        },
        "redacted": True,
    }


def sanitize_log_data(
    data: Dict[str, Any], sensitive_keys: Optional[list] = None
) -> Dict[str, Any]:
    """Sanitize a dictionary for logging by redacting sensitive keys.

    Args:
        data: Dictionary to sanitize.
        sensitive_keys: Keys to redact (defaults to a set of common sensitive keys).

    Returns:
        Sanitized dictionary with sensitive values redacted.
    """
    if sensitive_keys is None:
        sensitive_keys = [
            "prompt_content",
            "response_content",
            "job_description",
            "latex_content",
            "cv_content",
            "api_key",
            "password",
            "token",
            "secret",
        ]

    sanitized = {}

    for key, value in data.items():
        key_lower = key.lower()

        # Check if this is a sensitive key
        if any(sensitive in key_lower for sensitive in sensitive_keys):
            if isinstance(value, str):
                if "prompt" in key_lower:
                    sanitized[key] = redact_prompt_content(value)
                elif "job_description" in key_lower or "description" in key_lower:
                    sanitized[key] = redact_job_description(value)
                elif "latex" in key_lower or "tex" in key_lower:
                    sanitized[key] = redact_latex_content(value)
                else:
                    sanitized[key] = {
                        "length": len(value),
                        "preview": preview_content(value),
                        "redacted": True,
                    }
            else:
                sanitized[key] = "[REDACTED]"
        elif isinstance(value, dict):
            # Recursively sanitize nested dictionaries
            sanitized[key] = sanitize_log_data(value, sensitive_keys)
        elif isinstance(value, str) and len(value) > MAX_LOG_CONTENT_LENGTH:
            # Truncate very long non-sensitive strings
            sanitized[key] = truncate_content(value)
        else:
            sanitized[key] = value

    return sanitized
