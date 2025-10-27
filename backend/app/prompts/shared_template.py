"""
Shared Prompt Template for CV Enhancement

This module imports and combines all prompt sections from organized modules
to create the main templates used by CV enhancement prompts.

All common sections are imported from specialized modules and combined
into templates for easy injection into individual prompt variants.

Version: 2.0
Last Updated: 2025-10-27
"""

# Import core requirements
from .core_requirements import (
    CORE_OUTPUT_REQUIREMENTS,
    SPACING_PRESERVATION_RULES,
    LATEX_COMPILATION_SAFETY,
    EXECUTION_RULES,
    FINAL_VALIDATION_CHECKLIST,
)

# Import content guidelines
from .content_guidelines import (
    CONTENT_STRUCTURE_GUIDELINES,
    ENHANCEMENT_STRATEGY,
    INTELLIGENT_BOLDING_GUIDELINES,
)

# Import quality standards
from .quality_standards import (
    QUALITY_STANDARDS,
    ADVANCED_QUALITY_ASSURANCE,
    FACTUAL_INTEGRITY_REQUIREMENTS,
    ENHANCED_FACTUAL_INTEGRITY,
)

# Import specialist frameworks
from .specialist_frameworks import (
    TAG_FRAMEWORK,
    TRACE_FRAMEWORK,
    CARE_FRAMEWORK,
    PAR_FRAMEWORK,
    CRISPE_FRAMEWORK,
    AIDA_FRAMEWORK,
    STAR_FRAMEWORK,
    APE_FRAMEWORK,
    BAB_FRAMEWORK,
    RTF_FRAMEWORK,
    ANTI_HALLUCINATION_GUARDRAILS,
    FINAL_OUTPUT_REQUIREMENTS,
    DOCUMENT_STRUCTURE_ANALYSIS,
)

# Import slicing rules
from .slicing_rules import (
    PERSONAL_PROJECTS_SLICING,
)

# Combined template that includes both specialist framework and common requirements
# This single template is used across all three enhancement prompts
COMBINED_PROMPT_TEMPLATE = f"""
{TAG_FRAMEWORK}

{TRACE_FRAMEWORK}

{CARE_FRAMEWORK}

{PAR_FRAMEWORK}

{CRISPE_FRAMEWORK}

{AIDA_FRAMEWORK}

{STAR_FRAMEWORK}

{APE_FRAMEWORK}

{BAB_FRAMEWORK}

{RTF_FRAMEWORK}

{DOCUMENT_STRUCTURE_ANALYSIS}

{ANTI_HALLUCINATION_GUARDRAILS}

{FINAL_OUTPUT_REQUIREMENTS}

{CORE_OUTPUT_REQUIREMENTS}

{SPACING_PRESERVATION_RULES}

{EXECUTION_RULES}

{CONTENT_STRUCTURE_GUIDELINES}

{ENHANCEMENT_STRATEGY}

{INTELLIGENT_BOLDING_GUIDELINES}

{QUALITY_STANDARDS}

{FACTUAL_INTEGRITY_REQUIREMENTS}

{LATEX_COMPILATION_SAFETY}

{FINAL_VALIDATION_CHECKLIST}
"""
