"""
Shared prompt template for CV enhancement.

This module imports and consolidates prompt sections from specialized modules
to compose the primary templates used by the CV enhancement prompts.

Common sections are assembled into templates for reuse across individual prompt variants.

Version: 2.0
Last updated: 2025‑10‑27
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

# Lightweight framework to ensure consistent job‑description analysis across prompts
JOB_DESCRIPTION_ANALYSIS = """
## 🧭 JOB DESCRIPTION ANALYSIS FRAMEWORK
- Extract MUST-have and NICE-to-have requirements from the job description
- Build a skill taxonomy (Languages, Frameworks, Tools, Databases, Cloud, Methodologies, Domains)
- Capture role scope indicators (seniority, responsibilities, impact expectations)
- Create a prioritized keyword list preserving exact JD phrasing (MUST items first)
- Maintain a synonym normalization map aligning CV terminology with JD terminology
- Build a traceability matrix linking JD requirements to verifiable CV evidence (mark "no evidence" when missing)
- Prioritize MUST-have coverage while never fabricating information; use conservative wording when evidence is partial
"""

# Combined template including specialist frameworks and common requirements.
# This template is reused across all enhancement prompt variants.
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

{JOB_DESCRIPTION_ANALYSIS}

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
