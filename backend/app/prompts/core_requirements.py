"""
Core Requirements for CV Enhancement Prompts

This module contains the fundamental output requirements and LaTeX safety rules
that are essential for all CV enhancement operations.

Version: 2.0
Last Updated: 2025-10-27
"""

# Core output requirements - highest priority
CORE_OUTPUT_REQUIREMENTS = """
CRITICAL OUTPUT REQUIREMENTS:
- Output ONLY pure LaTeX code - NO markdown formatting or code blocks
- Document must start with \\documentclass and end with \\end{{document}}
- Do NOT include explanations, comments, or metadata
- Preserve original LaTeX structure and packages
- Maintain authenticity while enhancing for job relevance
"""

# Spacing preservation rules
SPACING_PRESERVATION_RULES = """
IMPORTANT SPACING RULES:
- PRESERVE ALL \\vspace{{}} commands from the original CV
- Maintain proper section separation and readability
- Keep consistent formatting structure
- Only remove excessive spacing, not essential spacing
"""

# LaTeX compilation safety rules
LATEX_COMPILATION_SAFETY = """
LATEX SAFETY REQUIREMENTS:
1. **Character Escaping**: Always escape & → \\&, % → \\%, $ → \\$, _ → \\_, # → \\#
2. **Safe Characters**: Use -- for em-dash, avoid \\textasciimdash, \\textasciitilde, \\textasciicircum
3. **Content Wrapping**: URLs/paths in \\texttt{{}}, code in \\verb|content|
4. **Bold Usage**: Use \\textbf{{keyword}} for key terms, ensure balanced braces
5. **Validation**: No unescaped &, no undefined control sequences, balanced braces
6. **Fallback**: Use plain text alternatives when escaping becomes complex
7. **CRITICAL**: Never output regex artifacts like \\1, \\2, \\3 in LaTeX content
"""

# Execution rules (priority and editing discipline)
EXECUTION_RULES = """
EXECUTION RULES:
Priority if rules conflict: Output Format > Safety > Factual Integrity > Page Fit > Style
- Preamble Preservation: Do not add/remove packages or redefine macros unless fixing a compile error
- Section Mapping: Detect sections (Summary, Education, Experience, Projects, Skills, Certifications). Do not invent missing sections
- Delta Discipline: Modify content only; do not change layout environments, custom commands, or lengths
- Job-Term Mirroring: Mirror exact phrasing of top job keywords naturally; avoid stuffing
- ATS Readability: Prefer simple sentences and standard headings; avoid tables for core content unless already present
- Tense & Person: Past tense for completed roles, present for current; no first-person
- Quantification: Add metrics only if derivable from text; otherwise use qualitative impact terms
- Dates & Formats: Normalize to existing CV format; never infer missing dates
- Proper Nouns: Preserve correct casing for technologies and products (e.g., JavaScript, React)
- Numbers & Units: Keep unit styles consistent; prefer numerals for measures
- Bold Throttling: Max 3–5 bolded terms per bullet; never bold in Skills list
- No New Dependencies: Do not introduce commands that require missing packages
- URL/Code Handling: Wrap URLs/paths in \\texttt{{}}; avoid breaking lines mid-URL
- Environment Integrity: Ensure all \\begin{...} have matching \\end{...}; avoid introducing nested itemize unless already present
- Forbidden Areas: Do not modify contact block (name/email/phone) except for escaping fixes
- Ambiguity Handling: If information is missing or ambiguous, omit rather than infer; prefer neutral phrasing
- Unicode Normalization: Normalize dashes (— → --), quotes to ASCII where appropriate
- Idempotence: Ensure re-running will not double-bold, double-escape, or over-compress content
"""

# Final validation checklist (preflight and pagination)
FINAL_VALIDATION_CHECKLIST = """
FINAL VALIDATION CHECKLIST:
Output Schema:
- Starts with \\documentclass and ends with \\end{document}
- No prose outside LaTeX
Compile Preflight:
- No unescaped &, %, $, _, # in text
- No undefined control sequences
- Braces balanced; all environments properly closed
- No markdown artifacts (** __ ```)
Pagination & Fit:
- Mentally paginate; if risk of overflow, compress least relevant clauses first
- Keep section separation readable without altering layout commands
Consistency:
- Dates, units, casing, tense consistent with existing CV conventions
"""
