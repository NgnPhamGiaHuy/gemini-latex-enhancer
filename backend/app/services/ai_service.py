"""
AI Service for CV summarization and enhancement using Google Gemini.

This module centralizes all interactions with the Gemini API so that:
- Authentication and model selection are consistently handled in one place
- Prompt construction is delegated to `app.prompts.PromptManager`
- Responses are validated and normalized for downstream services (e.g., LaTeX)

The service exposes two primary capabilities:
1) summarize_cv: produce a recruiter-friendly text summary from LaTeX content
2) enhance_cv: return a full, compilable LaTeX document tailored to a job
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

    def summarize_cv(self, latex_content: str) -> str:
        """Summarize a LaTeX CV into plain text.

        Sends the raw LaTeX content to Gemini using a strict summarization
        prompt and returns a concise, recruiter-oriented text summary.

        Args:
            latex_content: The original LaTeX document string.

        Returns:
            A plain-text summary string with consistent section headers.

        Raises:
            HTTPException: If the AI response is empty or any downstream error
                occurs.
        """
        logger.info("=== CV SUMMARIZATION STARTED ===")
        logger.info(f"LaTeX content length: {len(latex_content)} characters")
        logger.debug(f"LaTeX content preview: {latex_content[:300]}...")

        try:
            prompt = PromptManager.get_summarization_prompt(latex_content)

            logger.info(f"Prompt length: {len(prompt)} characters")
            logger.debug(f"Prompt preview: {prompt[:200]}...")

            logger.info("Sending request to Gemini API...")
            response = self.model.generate_content(prompt)

            if not response or not response.text:
                logger.error("❌ Empty response from Gemini API")
                raise HTTPException(
                    status_code=500, detail="Empty response from AI service"
                )

            summary = response.text.strip()
            logger.info(f"✅ Summary received, length: {len(summary)} characters")
            logger.debug(f"Summary content: {summary}")

            logger.info("=== CV SUMMARIZATION COMPLETED SUCCESSFULLY ===")
            return summary

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ CV summarization failed: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500, detail=f"AI summarization failed: {str(e)}"
            )

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
