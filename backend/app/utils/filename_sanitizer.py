"""
Unicode‑safe filename‑sanitization utilities.

Provides robust filename sanitization that preserves Unicode characters while
removing only unsafe symbols that are invalid across major operating systems.
"""

import re
import unicodedata
from typing import Optional


def sanitize_filename(text: str) -> str:
    """
    Sanitize a filename to be safe across operating systems while preserving Unicode characters.

    This function:
    - Preserves all alphabetic characters from any language (Vietnamese, French, Japanese, etc.)
    - Removes only unsafe symbols and reserved characters
    - Normalizes Unicode characters to prevent encoding issues
    - Replaces spaces with hyphens for consistency

    Args:
        text: The text to sanitize for use as a filename

    Returns:
        A sanitized filename safe for use across operating systems

    Examples:
        >>> sanitize_filename("Nguyen Pham Gia Huy")
        "Nguyen-Pham-Gia-Huy"

        >>> sanitize_filename("Chợ Tốt")
        "Chợ-Tốt"

        >>> sanitize_filename("François Dupont")
        "François-Dupont"

        >>> sanitize_filename("山田太郎")
        "山田太郎"

        >>> sanitize_filename("Test/File*Name?")
        "Test-File-Name"
    """
    if not text or not text.strip():
        return "untitled"

    # Normalize Unicode characters to prevent encoding issues (NFC is recommended)
    text = unicodedata.normalize("NFC", text)

    # Remove only truly unsafe characters for filenames across OS:
    # Windows: < > : " | ? * \ /
    # Unix/Linux: / (forward slash)
    # Additional problematic chars: control characters (0-31), DEL (127)
    unsafe_chars = r'[<>:"|?*\\/\x00-\x1f\x7f]'
    text = re.sub(unsafe_chars, "-", text)

    # Replace multiple spaces and hyphens with a single hyphen
    text = re.sub(r"[\s\-]+", "-", text)

    # Remove leading/trailing hyphens and dots (can cause issues on some systems)
    text = text.strip("-.")

    # Ensure the filename is not empty after sanitization
    if not text:
        return "untitled"

    # Limit length to prevent filesystem issues (255 chars is safe for most filesystems)
    if len(text) > 200:  # Leave some room for extensions
        text = text[:200].rstrip("-")

    return text


def sanitize_filename_for_download(text: str) -> str:
    """
    Sanitize a filename specifically for download headers.

    This is more permissive than regular filename sanitization because browsers
    can handle more Unicode characters in download filenames.

    Args:
        text: The text to sanitize for download filename

    Returns:
        A sanitized filename safe for download headers
    """
    if not text or not text.strip():
        return "download"

    # Normalize Unicode characters
    text = unicodedata.normalize("NFC", text)

    # Remove only the most problematic characters for HTTP headers;
    # retain most Unicode characters for international filenames
    text = re.sub(r"[\r\n\t\x00-\x1f\x7f]", "", text)

    # Replace spaces with hyphens for consistency
    text = re.sub(r"\s+", "-", text)

    # Remove leading/trailing hyphens
    text = text.strip("-")

    # Ensure not empty
    if not text:
        return "download"

    return text


def sanitize_filename_for_filesystem(text: str) -> str:
    """
    Sanitize a filename for filesystem storage (more restrictive).

    Used for actual file storage where stricter filesystem compatibility is required.

    Args:
        text: The text to sanitize for filesystem storage

    Returns:
        A sanitized filename safe for filesystem storage
    """
    if not text or not text.strip():
        return "file"

    # Normalize Unicode characters
    text = unicodedata.normalize("NFC", text)

    # Remove filesystem‑unsafe characters (stricter than download sanitization)
    unsafe_chars = r'[<>:"|?*\\/\x00-\x1f\x7f]'
    text = re.sub(unsafe_chars, "-", text)

    # Replace spaces and repeated hyphens with a single hyphen
    text = re.sub(r"[\s\-]+", "-", text)

    # Remove leading/trailing hyphens and dots
    text = text.strip("-.")

    # Ensure not empty
    if not text:
        return "file"

    # Limit length for filesystem safety
    if len(text) > 200:
        text = text[:200].rstrip("-")

    return text
