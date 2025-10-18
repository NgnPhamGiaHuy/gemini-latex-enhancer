"""
Prompt Manager — centralized accessors for all AI prompts.

The manager exposes typed helpers to retrieve correctly formatted prompts for
Gemini. Using a single entry point keeps prompt text, variables, and versions
cohesive across the app.
"""

from .enhancement import (
    CV_ENHANCEMENT_PROMPT,
    CV_ENHANCEMENT_PROMPT_ADVANCED,
    CV_ENHANCEMENT_PROMPT_WITH_SLICING,
)


class PromptManager:
    """Manages all AI prompts for different tasks."""

    @staticmethod
    def get_enhancement_prompt(
        latex_content: str,
        job_title: str,
        job_description: str,
        company_name: str = "N/A",
        use_advanced: bool = False,
        slice_projects: bool = False,
    ) -> str:
        """Return the enhancement prompt with optional advanced/slicing variants.

        Args:
            latex_content: Raw LaTeX CV.
            job_title: Target job title.
            job_description: Full job description text.
            company_name: Optional employer name used for tailoring.
            use_advanced: Use the advanced prompt that enforces strict budgets.
            slice_projects: Use the variant that selects relevant projects only.
        """
        from .shared_template import (
            COMMON_PROMPT_TEMPLATE,
            ADVANCED_QUALITY_ASSURANCE,
            PERSONAL_PROJECTS_SLICING,
            FACTUAL_INTEGRITY_RULES,
        )

        if slice_projects:
            return CV_ENHANCEMENT_PROMPT_WITH_SLICING.format(
                latex_content=latex_content,
                job_title=job_title,
                job_description=job_description,
                company_name=company_name,
                common_template=COMMON_PROMPT_TEMPLATE,
                factual_integrity_rules=FACTUAL_INTEGRITY_RULES,
                personal_projects_slicing=PERSONAL_PROJECTS_SLICING,
                quality_assurance=ADVANCED_QUALITY_ASSURANCE,
            )
        elif use_advanced:
            return CV_ENHANCEMENT_PROMPT_ADVANCED.format(
                latex_content=latex_content,
                job_title=job_title,
                job_description=job_description,
                company_name=company_name,
                common_template=COMMON_PROMPT_TEMPLATE,
                quality_assurance=ADVANCED_QUALITY_ASSURANCE,
            )
        else:
            return CV_ENHANCEMENT_PROMPT.format(
                latex_content=latex_content,
                job_title=job_title,
                job_description=job_description,
                company_name=company_name,
                common_template=COMMON_PROMPT_TEMPLATE,
            )

    @staticmethod
    def list_available_prompts() -> list:
        """List all available prompt identifiers for diagnostics and UI."""
        return [
            "enhancement",
            "enhancement_advanced",
            "enhancement_with_slicing",
        ]
