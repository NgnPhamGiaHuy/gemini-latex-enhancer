from __future__ import annotations

import re


class InputSanitizer:
    """Utility for sanitising untrusted text for logs/storage."""

    @staticmethod
    def sanitize(text: str, max_length: int = 10000) -> str:
        if not text:
            return ""

        cleaned = re.sub(r"<[^>]+>", "", text)
        cleaned = re.sub(
            r"<script[^>]*>.*?</script>", "", cleaned, flags=re.IGNORECASE | re.DOTALL
        )
        cleaned = re.sub(r'[<>"\']', "", cleaned)
        cleaned = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        if len(cleaned) > max_length:
            cleaned = cleaned[:max_length]
            breakpoint = cleaned.rfind(" ")
            if breakpoint > max_length * 0.8:
                cleaned = cleaned[:breakpoint]

        return cleaned
