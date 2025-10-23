"""
Shared Prompt Template for CV Enhancement

This module contains common prompt sections that are shared across all CV enhancement
prompt variants. This centralizes maintenance and ensures consistency across:
- CV_ENHANCEMENT_PROMPT (standard)
- CV_ENHANCEMENT_PROMPT_ADVANCED (advanced)
- CV_ENHANCEMENT_PROMPT_WITH_SLICING (with project slicing)

All common sections are defined as constants that can be imported and injected
into individual prompt variants.

Version: 2.0
Last Updated: 2025-10-24
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

# Content structure guidelines
CONTENT_STRUCTURE_GUIDELINES = """
CONTENT STRUCTURE:
- Each section: 3-5 items maximum (prioritize most relevant)
- Each item: more than 30-40 words (180-240 characters)
- Use action verbs and quantifiable achievements
- Focus on job-relevant content over general content
- Remove redundant or outdated information
"""

# Enhancement strategy
ENHANCEMENT_STRATEGY = """
ENHANCEMENT APPROACH:
- Replace generic descriptions with job-specific keywords
- Quantify achievements with metrics and percentages
- Use action verbs from job description
- Use industry terminology from job posting
- Consolidate similar experiences
- Use \\textbf{{}} to highlight key technologies, achievements, and skills
"""

# Factual integrity requirements
FACTUAL_INTEGRITY_REQUIREMENTS = """
FACTUAL INTEGRITY:
- NEVER fabricate or exaggerate experience duration
- Compute duration only from explicit date ranges
- If dates are missing, use neutral phrasing without quantifying time
- Maintain accuracy of all factual information
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

# Quality standards
QUALITY_STANDARDS = """
QUALITY REQUIREMENTS:
- Maintain professional tone and authenticity
- Ensure factual accuracy and truthfulness
- Use industry-standard terminology from job description
- Highlight transferable skills and achievements
- Preserve document readability and visual hierarchy
"""

# Keyword highlighting guidelines
KEYWORD_HIGHLIGHTING_GUIDELINES = """
KEYWORD HIGHLIGHTING:
Use \\textbf{{keyword}} to emphasize:
- Quantifiable achievements (metrics, percentages, team sizes)
- Industry terminology (Agile, Scrum, CI/CD, Microservices)
- Strong action verbs (Developed, Implemented, Optimized, Led)
- Key technologies and frameworks (JavaScript, React, Python, Docker, AWS)
- Company/project names when relevant

Guidelines:
- 3-5 bold terms per bullet point maximum
- Only highlight job-relevant terms
- Match job description terminology exactly
- Keep Skills section clean (no bold formatting)
"""

# Advanced quality assurance
ADVANCED_QUALITY_ASSURANCE = """
ADVANCED QUALITY CHECK:
- Every word must add value to job application
- Maintain professional authenticity
- Ensure factual accuracy
- Use consistent formatting
- Check for typos and grammar
- Preserve document readability and visual hierarchy
"""

# Enhanced factual integrity (for slicing prompt)
ENHANCED_FACTUAL_INTEGRITY = """
ENHANCED FACTUAL INTEGRITY:
- NEVER fabricate, exaggerate, or alter factual details
- Preserve employment duration, company names, job titles exactly
- Keep education dates, internships, work experience dates accurate
- Maintain personal information (GPA, awards, certifications) as stated
- When clarifying ambiguous phrasing, stay conservative and truthful
- If details are missing, omit rather than invent or estimate
"""

# Personal projects slicing (for slicing prompt)
PERSONAL_PROJECTS_SLICING = """
PROJECT SLICING STRATEGY:
When multiple personal projects exist, select only the most job-relevant ones:

1. **Relevance Scoring**: Rate each project 1-10 based on:
   - Technology stack alignment with job requirements
   - Project complexity matching job level
   - Industry relevance to target role
   - Demonstrated skills mentioned in job description

2. **Selection Rules**:
   - 4+ projects: Keep TOP 2 most relevant
   - 3 projects: Keep TOP 2-3 based on content length
   - 2 projects: Keep both if space allows, otherwise most relevant
   - 1 project: Keep if relevant, remove if not

3. **Content Optimization**:
   - Focus on projects showcasing job-relevant skills
   - Emphasize quantifiable results and achievements
   - Use job-specific terminology and keywords
   - Remove generic or outdated descriptions
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

# Combined common template for easy injection
COMMON_PROMPT_TEMPLATE = f"""
{CORE_OUTPUT_REQUIREMENTS}

{SPACING_PRESERVATION_RULES}

{EXECUTION_RULES}

{CONTENT_STRUCTURE_GUIDELINES}

{ENHANCEMENT_STRATEGY}

{KEYWORD_HIGHLIGHTING_GUIDELINES}

{QUALITY_STANDARDS}

{FACTUAL_INTEGRITY_REQUIREMENTS}

{LATEX_COMPILATION_SAFETY}

{FINAL_VALIDATION_CHECKLIST}
"""
