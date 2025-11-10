from __future__ import annotations

import re
import time
from typing import Optional

import google.generativeai as genai
from fastapi import HTTPException
from pylatexenc.latexencode import unicode_to_latex

from app.application.contracts.cv_enhancer import CvEnhancer
from app.domain.entities.latex_document import LatexDocument
from app.domain.services.latex_validator import LatexValidator
from app.domain.value_objects.job_context import JobContext
from app.config import settings
from app.prompts import PromptManager
from app.utils.logger import get_logger, session_prompt_logger

logger = get_logger(__name__)


class GeminiClient:
    """Thin wrapper over generative model for easier testing."""

    def __init__(self, model_id: str, api_key: str) -> None:
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(model_id)
        self.model_id = model_id

    def generate(self, prompt: str):
        return self._model.generate_content(prompt)


class GeminiCvEnhancer(CvEnhancer):
    """Adapter that calls Google Gemini and normalises its output.

    Simplified version that trusts prompts and uses existing sanitization tools.
    """

    def __init__(
        self, client: GeminiClient, prompt_manager: PromptManager | None = None
    ) -> None:
        self._client = client
        self._prompt_manager = prompt_manager or PromptManager
        self.model_id = client.model_id

    def enhance(
        self,
        document: LatexDocument,
        job_context: JobContext,
        *,
        session_id: str | None = None,
        slice_projects: bool = False,
    ) -> LatexDocument:
        start = time.time()

        prompt = self._prompt_manager.get_enhancement_prompt(
            latex_content=document.content,
            job_title=job_context.job_title,
            job_description=job_context.job_description,
            company_name=job_context.company_name or "N/A",
            slice_projects=slice_projects,
        )

        if settings.ENABLE_PROMPT_LOGGING:
            session_prompt_logger.log_prompt_request(
                prompt_type="enhancement",
                job_title=job_context.job_title,
                job_description=job_context.job_description,
                company_name=job_context.company_name or "N/A",
                slice_projects=slice_projects,
                prompt_content=prompt,
                prompt_length=len(prompt),
                model_id=self._client.model_id,
                session_id=session_id,
            )

        try:
            logger.info("Generating AI response using model %s", self._client.model_id)
            response = self._client.generate(prompt)

            # Minimal cleaning: strip markdown code blocks if present
            cleaned = self._strip_markdown_code_blocks(response.text)

            # Ensure document structure (simple validation + minimal fix)
            cleaned = self._ensure_document_structure(cleaned, document.content)

            # Validate LaTeX structure
            LatexValidator.validate(cleaned)

        except Exception as exc:
            duration = time.time() - start
            if settings.ENABLE_PROMPT_LOGGING:
                session_prompt_logger.log_prompt_response(
                    response_content="",
                    response_length=0,
                    processing_time=duration,
                    model_id=self._client.model_id,
                    session_id=session_id,
                    success=False,
                    error_message=str(exc),
                )
            raise HTTPException(
                status_code=500, detail=f"AI enhancement failed: {exc}"
            ) from exc

        duration = time.time() - start
        if settings.ENABLE_PROMPT_LOGGING:
            session_prompt_logger.log_prompt_response(
                response_content=cleaned,
                response_length=len(cleaned),
                processing_time=duration,
                model_id=self._client.model_id,
                session_id=session_id,
                success=True,
            )

        return LatexDocument(cleaned)

    @staticmethod
    def _strip_markdown_code_blocks(text: str) -> str:
        """Strip markdown code fences if present (prompts should prevent this)."""
        text = text.strip()
        # Remove ```latex or ``` at start/end
        if text.startswith("```"):
            # Find first newline after ```
            start_idx = text.find("\n", text.find("```"))
            if start_idx == -1:
                text = text[3:].strip()
            else:
                text = text[start_idx + 1 :].strip()

        if text.endswith("```"):
            text = text[:-3].strip()

        return text

    def _ensure_document_structure(self, enhanced: str, original: str) -> str:
        """Ensure document has proper structure. Minimal fix if needed.

        Prompts explicitly require \\documentclass and \\end{document}, so this
        should rarely be needed. If structure is missing, we wrap with original
        preamble or minimal fallback.
        """
        # Check for required structure
        has_docclass = bool(re.search(r"\\documentclass\s*\{[^}]+\}", enhanced))
        has_begin = bool(re.search(r"\\begin\{document\}", enhanced))
        has_end = bool(re.search(r"\\end\{document\}", enhanced))

        # If all present, return as-is (trust the prompt)
        if has_docclass and has_begin and has_end:
            logger.debug("Document structure is valid")
            return enhanced

        # If missing structure, log warning and apply minimal fix
        logger.warning(
            "AI response missing document structure (docclass: %s, begin: %s, end: %s). "
            "Applying minimal fix.",
            has_docclass,
            has_begin,
            has_end,
        )

        # Extract preamble from original (preferred) or use minimal fallback
        original_preamble, _ = self._split_preamble_and_body(original)
        if original_preamble and original_preamble.strip():
            preamble = original_preamble.strip()
        else:
            preamble = "\\documentclass{article}\n\\usepackage[utf8]{inputenc}\n\\usepackage[T1]{fontenc}\n"

        # Extract body: everything after preamble commands or use enhanced as-is
        if has_begin and has_end:
            # Has document environment, extract body
            match = re.search(
                r"\\begin\{document\}(.*?)\\end\{document\}",
                enhanced,
                flags=re.DOTALL | re.IGNORECASE,
            )
            if match:
                body = match.group(1).strip()
            else:
                body = enhanced.strip()
        else:
            # No document environment, use enhanced content as body
            # Remove any stray preamble commands that might be in the content
            body = self._remove_preamble_commands(enhanced)

        if not preamble.endswith("\n"):
            preamble += "\n"

        return f"{preamble}\\begin{{document}}\n{body}\n\\end{{document}}\n"

    @staticmethod
    def _split_preamble_and_body(latex: str) -> tuple[str, str]:
        """Split LaTeX into preamble and body."""
        match = re.search(
            r"\\begin\{document\}(.*?)\\end\{document\}",
            latex,
            flags=re.DOTALL | re.IGNORECASE,
        )
        if not match:
            # If has documentclass, treat as preamble; otherwise as body
            if "\\documentclass" in latex:
                return latex, ""
            return "", latex

        start = match.start()
        preamble = latex[:start].strip()
        body = match.group(1).strip()
        return preamble, body

    @staticmethod
    def _remove_preamble_commands(content: str) -> str:
        """Remove preamble commands from content (simple line-based filter)."""
        preamble_patterns = [
            r"^\\documentclass[^\n]*$",
            r"^\\usepackage[^\n]*$",
            r"^\\RequirePackage[^\n]*$",
            r"^\\newcommand[^\n]*$",
            r"^\\newenvironment[^\n]*$",
        ]

        lines = []
        for line in content.split("\n"):
            line_stripped = line.strip()
            # Skip empty lines, comments, and preamble commands
            if not line_stripped or line_stripped.startswith("%"):
                continue
            if any(
                re.match(pattern, line_stripped, re.IGNORECASE)
                for pattern in preamble_patterns
            ):
                continue
            lines.append(line)

        return "\n".join(lines).strip()
