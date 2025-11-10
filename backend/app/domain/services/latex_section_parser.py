from __future__ import annotations

import re
from typing import List, Dict


class LatexSectionParser:
    """Utility for extracting high-level sections from LaTeX content."""

    SECTION_PATTERNS = [
        r"\\section\*?\{([^}]+)\}",
        r"\\subsection\*?\{([^}]+)\}",
        r"\\cvsection\{([^}]+)\}",
        r"\\cvsubsection\{([^}]+)\}",
    ]

    @classmethod
    def parse(cls, latex_content: str) -> List[Dict[str, str]]:
        sections: List[Dict[str, str]] = []
        for pattern in cls.SECTION_PATTERNS:
            for match in re.findall(pattern, latex_content, re.IGNORECASE):
                title = match.strip()
                sections.append({"title": title, "content": f"Content for {title}"})

        if not sections:
            sections = [
                {"title": "Education", "content": "Education section"},
                {"title": "Experience", "content": "Experience section"},
                {"title": "Skills", "content": "Skills section"},
            ]
        return sections
