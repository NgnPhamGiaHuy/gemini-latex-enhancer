"""
Shared Prompt Template for CV Enhancement

This module contains common prompt sections that are shared across all CV enhancement
prompt variants. This centralizes maintenance and ensures consistency across:
- CV_ENHANCEMENT_PROMPT (standard)
- CV_ENHANCEMENT_PROMPT_ADVANCED (advanced)
- CV_ENHANCEMENT_PROMPT_WITH_SLICING (with project slicing)

All common sections are defined as constants that can be imported and injected
into individual prompt variants.
"""

# Common critical rules that apply to all prompts
COMMON_CRITICAL_RULES = """
CRITICAL RULES:
- Output ONLY pure LaTeX code - NO markdown formatting
- Do NOT wrap output in ```latex``` code blocks
- Do NOT include explanations, comments, or metadata
- Output must start with \\documentclass and end with \\end{{document}}
- Preserve all formatting and structure
- Enhance content to match job requirements while maintaining authenticity
- Keep the same LaTeX document structure and packages
- **CRITICAL: DO NOT remove any \\vspace{{}} commands from the original CV**
- **CRITICAL: Preserve original font formatting - do NOT add unnecessary font commands like \\texttt{{}} to normal text**
"""

# Common spacing and formatting rules
COMMON_SPACING_RULES = """
**Spacing & Formatting Rules - CRITICAL:**
- PRESERVE ALL \\vspace{{}} commands exactly as they appear in the original CV
- DO NOT remove \\vspace{{{{spacing}}}} or any other spacing commands
- Maintain proper spacing between items within sections
- Keep consistent formatting and structure
- Only remove excessive spacing, not necessary spacing for readability
- Ensure sections are visually separated and easy to read
- Spacing commands like \\vspace{{{{spacing}}}} are ESSENTIAL for proper document layout
"""

# Common list formatting requirements
COMMON_LIST_FORMATTING = """
**List Formatting Requirements (CRITICAL):**
- Each list section (Experience, Projects, Skills, etc.) must contain exactly 4-5 items
- Each list item must be 25-30 words (approximately 150-200 characters without spaces)
- Prioritize the most relevant and impactful items for the target job
- If more than 5 items exist, select the top 5 most job-relevant ones
- If fewer than 4 items exist, expand with additional relevant achievements or skills
- Each item should be concise, specific, and quantifiable when possible
- Use action verbs and include metrics/numbers where applicable
"""

# Common enhancement strategy
COMMON_ENHANCEMENT_STRATEGY = """
**Enhancement Strategy:**
- Replace generic descriptions with job-specific keywords
- Quantify achievements (e.g., "increased efficiency by 25%")
- Use action verbs from job description
- Remove outdated or irrelevant information
- Consolidate similar experiences
- Use industry terminology from job posting
"""

# Common experience duration integrity rules
COMMON_EXPERIENCE_INTEGRITY = """
**Experience Duration Integrity - CRITICAL:**
- NEVER fabricate or exaggerate total experience duration
- If the PROFESSIONAL SUMMARY mentions an experience duration (e.g., "X months"), it MUST be derived directly from explicit date ranges in the EXPERIENCE section
- Compute duration only when start and end dates are clearly present; otherwise, OMIT duration in the summary
- If dates are missing or ambiguous, use neutral phrasing like "with hands-on internship experience" or "with practical experience" without quantifying months/years
- Do not alter or inflate durations stated elsewhere in the CV
"""

# Common LaTeX compilation safety rules
COMMON_LATEX_SAFETY = """
**LaTeX Compilation Safety Rules (CRITICAL):**
Before outputting the final LaTeX code, you MUST sanitize all text content to prevent compilation errors:

1. **Character Escaping (MANDATORY):**
   - & → \\& (CRITICAL: Never leave unescaped & in text content)
   - % → \\%
   - $ → \\$
   - _ → \\_
   - # → \\#
   - ~ → \\textasciitilde{{}}
   - ^ → \\textasciicircum{{}}
   - {{ and }} → Only escape when used outside LaTeX environments
   - Backslash (\\) → Double it if not part of a LaTeX command (\\\\ for literal slash)

2. **Special Content Handling:**
   - URLs, file paths, shell commands → Wrap in \\texttt{{}}
   - Code snippets, framework names → Use \\texttt{{}} or \\verb|content|
   - Technical terms with special chars → Escape appropriately
   - **IMPORTANT**: Do NOT wrap programming language names (JavaScript, Python, React, etc.) in \\texttt{{}} unless they contain special characters that need escaping

3. **Validation Checklist (MANDATORY):**
   - NO unescaped & symbols in text fields
   - NO raw alignment/tab (&) symbols outside tables
   - All brackets and braces properly balanced
   - All special characters properly escaped
   - URLs and paths wrapped in \\texttt{{}}

4. **Fallback Strategy:**
   - If escaping creates excessive backslashes, use natural alternatives (e.g., "and" instead of "&")
   - Only when semantically safe and maintaining readability

5. **Final Verification:**
   - Mentally verify the output will compile in standard LaTeX environments (Overleaf, TeXLive, LuaTeX)
   - Ensure no "Misplaced alignment tab character" or symbol-related errors
"""

# Common quality guidelines
COMMON_QUALITY_GUIDELINES = """
**Quality Guidelines:**
- Maintain professional tone and authenticity
- Ensure all information is accurate and truthful
- Use industry-standard terminology from the job description
- Highlight transferable skills and achievements
- Remove filler words and unnecessary details
- Preserve document readability and visual hierarchy
"""

# Advanced quality assurance (for advanced prompts)
ADVANCED_QUALITY_ASSURANCE = """
**Quality Assurance:**
- Every word must add value to job application
- Maintain professional authenticity
- Ensure factual accuracy
- Use consistent formatting
- Check for typos and grammar
- Preserve document readability and visual hierarchy
"""

# Factual integrity rules (for slicing prompt)
FACTUAL_INTEGRITY_RULES = """
- **NEVER fabricate, exaggerate, or alter factual details**, including:
  - Employment duration, company names, or job titles
  - Dates of education, internship, or work experience
  - Personal information such as GPA, awards, or certifications not present in the source
- When clarifying ambiguous phrasing, stay conservative and truthful (e.g., keep "3 months" if stated, not "6 months")
- If a requested detail (e.g., GPA or start date) is missing from the CV, simply omit it rather than inventing or estimating values
"""

# Personal projects slicing rules (for slicing prompt)
PERSONAL_PROJECTS_SLICING = """
**PERSONAL PROJECTS SLICING - CRITICAL:**
When multiple personal projects exist, you MUST intelligently select only the most job-relevant ones:

1. **Project Relevance Analysis**: Score each project 1-10 based on:
   - Technology stack alignment with job requirements
   - Project complexity matching job level
   - Industry relevance to target role
   - Demonstrated skills mentioned in job description

2. **Project Selection Rules**:
   - If 4+ projects exist: Keep only TOP 2 most relevant projects
   - If 3 projects exist: Keep TOP 2-3 based on content length
   - If 2 projects exist: Keep both if space allows, otherwise keep most relevant
   - If 1 project exists: Keep it if relevant, remove if not

3. **Content Length Consideration**:
   - For projects with extensive descriptions: Prioritize shorter, more impactful projects
   - For projects with brief descriptions: Can include more projects
   - Total projects section should not exceed 15% of CV word budget

4. **Project Enhancement Priority**:
   - Focus on projects that showcase skills mentioned in job description
   - Emphasize quantifiable results and achievements
   - Use job-specific terminology and keywords
   - Remove generic or outdated project descriptions
"""

# Combined common template for easy injection
COMMON_PROMPT_TEMPLATE = f"""
{COMMON_CRITICAL_RULES}

{COMMON_SPACING_RULES}

{COMMON_LIST_FORMATTING}

{COMMON_ENHANCEMENT_STRATEGY}

{COMMON_QUALITY_GUIDELINES}

{COMMON_EXPERIENCE_INTEGRITY}

{COMMON_LATEX_SAFETY}
"""
