"""
AI Service for CV enhancement using Google Gemini.

This module centralizes all interactions with the Gemini API so that:
- Authentication and model selection are consistently handled in one place
- Prompt construction is delegated to `app.prompts.PromptManager`
- Responses are validated and normalized for downstream services (e.g., LaTeX)

The service exposes one primary capability:
1) enhance_cv: return a full, compilable LaTeX document tailored to a job
"""

import google.generativeai as genai
from typing import Dict, Any
from fastapi import HTTPException
from app.config import settings
from app.utils.logger import get_logger
from app.prompts import PromptManager

logger = get_logger(__name__)


class AIService:
    """Service for AI-powered CV operations using Google Gemini.

    The instance encapsulates a configured `genai.GenerativeModel` and keeps
    the selected model id for observability.
    """

    def __init__(self, model_id: str = None):
        """Initialize the AI service.

        Args:
            model_id: Optional override for the model identifier. If omitted,
                the default from settings is used. If the provided model is not
                available, a safe default is selected.

        Raises:
            ValueError: If `GEMINI_API_KEY` is not configured.
            Exception: If the Gemini model fails to initialize.
        """
        logger.info("=== AI SERVICE INITIALIZATION ===")

        if not settings.GEMINI_API_KEY:
            logger.error("❌ GEMINI_API_KEY environment variable is not set")
            raise ValueError("GEMINI_API_KEY environment variable is required")

        logger.info(f"✅ GEMINI_API_KEY found: {settings.GEMINI_API_KEY[:10]}...")

        # Use provided model or default
        selected_model = model_id or settings.AI_MODEL
        logger.info(f"✅ Selected AI Model: {selected_model}")

        # Validate model exists using model service
        from app.services.model_service import model_service

        available_model = model_service.get_model_by_id(selected_model)

        if not available_model:
            logger.warning(
                f"⚠️ Model {selected_model} not found in available models, using default"
            )
            selected_model = model_service.get_default_model()
            available_model = model_service.get_model_by_id(selected_model)

        if available_model:
            logger.info(
                f"✅ Model validated: {available_model['name']} (v{available_model.get('version', 'Unknown')})"
            )
        else:
            logger.error(f"❌ No valid model found, falling back to hardcoded default")
            selected_model = "gemini-2.5-flash"

        try:
            # Configure Gemini
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(selected_model)
            self.model_id = selected_model
            logger.info(f"✅ Gemini model '{selected_model}' initialized successfully")
        except Exception as e:
            logger.error(
                f"❌ Failed to initialize Gemini model '{selected_model}': {str(e)}"
            )
            raise

    def enhance_cv(
        self, latex_content: str, job_data: Dict[str, Any], slice_projects: bool = False
    ) -> str:
        """Enhance a LaTeX CV for a specific job context.

        Uses advanced prompts to tailor the CV to the given job while enforcing
        page-length and formatting constraints. The AI output is cleaned to
        ensure it is pure LaTeX (no markdown fences).

        Args:
            latex_content: Original LaTeX CV content.
            job_data: Dictionary containing at least `job_title` and
                `job_description`. May include `company_name`.
            slice_projects: When True, instructs the prompt to intelligently
                select a subset of personal projects based on relevance.

        Returns:
            A full LaTeX document string intended to compile without changes.

        Raises:
            HTTPException: If model invocation or cleaning fails.
        """
        try:
            prompt = PromptManager.get_enhancement_prompt(
                latex_content=latex_content,
                job_title=job_data.get("job_title"),
                job_description=job_data.get("job_description"),
                company_name=job_data.get("company_name", "N/A"),
                use_advanced=settings.USE_ADVANCED_PROMPT,
                slice_projects=slice_projects,
            )

            response = self.model.generate_content(prompt)
            enhanced_latex = response.text

            # Clean the response to remove markdown formatting
            enhanced_latex = self._clean_latex_response(enhanced_latex)

            # Restore missing vspace commands from original
            enhanced_latex = self._restore_vspace_commands(
                enhanced_latex, latex_content
            )

            logger.info("CV enhancement completed successfully")
            return enhanced_latex

        except Exception as e:
            logger.error(f"CV enhancement failed: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"AI enhancement failed: {str(e)}"
            )

    def _clean_latex_response(self, response_text: str) -> str:
        """Normalize AI output to pure LaTeX.

        Strips common markdown code fences (e.g., ```latex ... ```) and trims
        leading/trailing artifacts so the result can be fed directly to LaTeX
        compilation.

        Args:
            response_text: Raw text returned by the model.

        Returns:
            Cleaned LaTeX string without markdown formatting.
        """
        logger.info("=== CLEANING LATEX RESPONSE ===")
        logger.debug(f"Raw response length: {len(response_text)} characters")
        logger.debug(f"Raw response preview: {response_text[:200]}...")

        # Remove markdown code blocks
        if "```latex" in response_text:
            logger.info("Found markdown code block, extracting LaTeX content")
            start_marker = "```latex"
            end_marker = "```"

            start_idx = response_text.find(start_marker)
            if start_idx != -1:
                start_idx += len(start_marker)
                end_idx = response_text.find(end_marker, start_idx)
                if end_idx != -1:
                    cleaned = response_text[start_idx:end_idx].strip()
                    logger.info(
                        f"Extracted LaTeX content, length: {len(cleaned)} characters"
                    )
                    return cleaned

        # Remove other common markdown patterns
        cleaned = response_text.strip()

        # Remove any leading/trailing markdown artifacts
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

        logger.info(f"Final cleaned LaTeX length: {len(cleaned)} characters")
        logger.debug(f"Cleaned LaTeX preview: {cleaned[:200]}...")

        return cleaned

    def _restore_vspace_commands(self, enhanced_latex: str, original_latex: str) -> str:
        """Restore missing \\vspace commands from the original LaTeX.

        This method ensures that essential spacing commands are preserved even if
        the AI model removes them during enhancement.

        Args:
            enhanced_latex: The AI-enhanced LaTeX content
            original_latex: The original LaTeX content

        Returns:
            Enhanced LaTeX with restored \\vspace commands
        """
        import re

        logger.info("=== RESTORING VSPACE COMMANDS ===")

        # Find all \\vspace commands in the original
        vspace_pattern = r"\\vspace\{[^}]+\}"
        original_vspaces = re.findall(vspace_pattern, original_latex)

        if not original_vspaces:
            logger.info("No \\vspace commands found in original LaTeX")
            return enhanced_latex

        logger.info(f"Found {len(original_vspaces)} \\vspace commands in original")

        # Check if any \\vspace commands are missing in enhanced version
        enhanced_vspaces = re.findall(vspace_pattern, enhanced_latex)
        missing_vspaces = [
            vspace for vspace in original_vspaces if vspace not in enhanced_vspaces
        ]

        if not missing_vspaces:
            logger.info("All \\vspace commands preserved in enhanced version")
            return enhanced_latex

        logger.warning(
            f"Found {len(missing_vspaces)} missing \\vspace commands, attempting to restore"
        )

        # Try to restore missing \\vspace commands by finding similar contexts
        restored_latex = enhanced_latex

        for missing_vspace in missing_vspaces:
            # Find the context around this vspace in the original
            vspace_index = original_latex.find(missing_vspace)
            if vspace_index == -1:
                continue

            # Get some context before and after the vspace
            context_start = max(0, vspace_index - 100)
            context_end = min(
                len(original_latex), vspace_index + len(missing_vspace) + 100
            )
            context = original_latex[context_start:context_end]

            # Look for similar context in enhanced version
            # This is a simple approach - we could make it more sophisticated
            if "\\end{itemize}" in context and missing_vspace in context:
                # This vspace likely comes after an itemize block
                # Try to find similar itemize blocks in enhanced version
                itemize_pattern = r"\\end\{itemize\}"
                enhanced_matches = list(re.finditer(itemize_pattern, restored_latex))

                for match in enhanced_matches:
                    # Check if there's already a vspace after this itemize
                    after_itemize = restored_latex[match.end() : match.end() + 20]
                    if not re.search(vspace_pattern, after_itemize):
                        # Insert the missing vspace
                        insert_pos = match.end()
                        restored_latex = (
                            restored_latex[:insert_pos]
                            + missing_vspace
                            + restored_latex[insert_pos:]
                        )
                        logger.info(f"Restored {missing_vspace} after itemize block")
                        break

        logger.info("=== VSPACE RESTORATION COMPLETED ===")
        return restored_latex
