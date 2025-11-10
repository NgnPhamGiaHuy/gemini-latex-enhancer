"""
Core requirements for CV enhancement prompts.

Defines fundamental output requirements and LaTeX safety rules that are essential
for all CV enhancement operations.

Version: 2.0
Last updated: 2025‑10‑27
"""

# Core output requirements — highest priority
CORE_OUTPUT_REQUIREMENTS = """
### CRITICAL OUTPUT REQUIREMENTS - HIGHEST PRIORITY

**Output Format Mandates:**
1. **Pure LaTeX Only:**
   - Output ONLY compilable LaTeX code
   - NO markdown formatting, code fences, or prose explanations
   - NO comments or metadata
   - NO surrounding text or instructions
   
2. **Document Structure:**
   - MUST start with: \\documentclass
   - MUST end with: \\end{{document}}
   - Complete, self-contained LaTeX document only

3. **Structure Preservation:**
   - Keep all original LaTeX packages unchanged
   - Preserve document class and layout settings
   - Maintain original preamble structure
   - Do not add or remove LaTeX packages

4. **Authenticity Maintenance:**
   - Enhance content for job relevance while preserving facts
   - Maintain original formatting where appropriate
   - Keep candidate's voice and style
   - Never change structural elements unnecessarily
"""

# Spacing preservation rules
SPACING_PRESERVATION_RULES = """
### SPACING PRESERVATION RULES

**Essential Spacing to Preserve:**
- KEEP ALL \\vspace{{}} commands from the original CV
- Maintain proper section separation for readability
- Preserve visual hierarchy and document flow
- Keep consistent formatting structure throughout

**Spacing Optimization Guidelines:**
- Only remove EXCESSIVE spacing that causes overflow
- Never remove spacing that improves readability
- Maintain breathing room between sections
- Preserve original paragraph and list spacing

**Decision Protocol:**
- If in doubt, keep the spacing
- Prioritize readability over strict space reduction
- One-page constraint should not compromise document quality
"""

# LaTeX compilation safety rules
LATEX_COMPILATION_SAFETY = """
### LATEX COMPILATION SAFETY REQUIREMENTS

**Requirement 1: Character Escaping**
- Escape: & → \\&
- Escape: % → \\%
- Escape: $ → \\$
- Escape: _ → \\_
- Escape: # → \\#
- Escaped characters MUST compile without errors

**Absolute Rule on Ampersands (&):**
- Never emit raw '&' outside a tabular/matrix environment
- If you need the literal character in text, ALWAYS use \\&

**Requirement 2: Safe Character Usage**
- Use -- for em-dash (not \\textasciimdash)
- Use ~ for non-breaking space when needed
- Avoid problematic characters: \\textasciitilde, \\textasciitilde, \\textasciicircum
- Use Unicode alternatives when escaping is complex

**Requirement 3: Content Wrapping**
- URLs: \\texttt{{URL}}
- File paths: \\texttt{{/path/to/file}}
- Code snippets: \\verb|code|
- Inline code: \\texttt{{inline}}

**Requirement 4: Bold Formatting Integrity**
- Use \\textbf{{keyword}} with balanced braces
- Never nest bold tags: \\textbf{{{keyword}}} ❌
- Ensure all \\textbf{{}} commands are properly closed

**Requirement 5: Syntax Validation**
- No unescaped special characters (&, %, $, _, #)
- No undefined LaTeX control sequences
- All braces { } must be balanced
- All environments properly opened and closed

**Requirement 6: Fallback Strategy**
- If character escaping becomes too complex, use plain text
- Choose simplicity over elaborate escaping schemes
- Prefer readability when possible

**Requirement 7: Regex Artifact Prevention - CRITICAL**
- NEVER output regex artifacts like \\1, \\2, \\3 in LaTeX content
- These indicate improper string processing
- Always output literal LaTeX code, never regex patterns
- If you see numbered references, replace with actual content
"""

# Execution rules (priority and editorial discipline)
EXECUTION_RULES = """
### EXECUTION RULES - PRIORITY HIERARCHY

**CRITICAL Priority Order (if rules conflict):**
1. Output Format > 2. Safety > 3. Factual Integrity > 4. Page Fit > 5. Style

### RULE CATEGORIES

**Category A: Structure Preservation (Do Not Modify)**
- **Preamble Preservation:** Do not add/remove packages or redefine macros unless fixing a compile error
- **Section Mapping:** Detect existing sections (Summary, Education, Experience, Projects, Skills, Certifications)
- **Rule:** Do NOT invent missing sections that don't exist in source
- **Environment Integrity:** Ensure all \\begin{{env}} have matching \\end{{env}}
- **Forbidden Areas:** Do not modify contact block (name/email/phone) except for LaTeX escaping fixes

**Category B: Content Modification (Edit With Caution)**
- **Delta Discipline:** Modify content only; do not change layout environments, custom commands, or lengths
- **Section Mapping:** Understand which sections exist before enhancing
- **No New Dependencies:** Do not introduce commands that require missing packages
- **Avoid Nested Structures:** Avoid introducing nested itemize unless already present in source

**Category C: Job Alignment (Strategic Enhancement)**
- **Job-Term Mirroring:** Mirror exact phrasing of top job keywords naturally; avoid keyword stuffing
- **Alignment Plan Discipline:** Build and reference a Job Alignment Plan (MUST vs NICE requirements, keyword list, traceability matrix) before rewriting
- **Evidence-First Claims:** Never claim coverage for JD requirements without verifiable CV evidence; prefer conservative, transferable phrasing when evidence is partial
- **ATS Readability:** Prefer simple sentences and standard headings
- **Synonym Normalization:** Map CV terminology to JD terminology using the alignment plan to maintain authenticity while matching phrasing
- **Tables Avoidance:** Avoid tables for core content unless already present in source
- **Tense Consistency:** Past tense for completed roles, present for current roles; no first-person

**Category D: Quantification and Formatting**
- **Quantification Rules:** Add metrics only if derivable from text; otherwise use qualitative impact terms
- **Dates & Formats:** Normalize to existing CV format; never infer missing dates
- **Proper Nouns:** Preserve correct casing for technologies (e.g., JavaScript, React, Node.js)
- **Numbers & Units:** Keep unit styles consistent; prefer numerals for measures

**Category E: Character and Syntax Handling**
- **Unicode Normalization:** Normalize dashes (— → --), quotes to ASCII where appropriate
- **Ambiguity Handling:** If information missing or ambiguous, omit rather than infer; prefer neutral phrasing
- **Idempotence:** Ensure re-running will not double-bold, double-escape, or over-compress content
- **URL/Code Handling:** Wrap URLs/paths in \\texttt{{}}; avoid breaking lines mid-URL

**Category F: Bolding Discipline**
- **Bold Throttling:** Maximum 3-5 bolded terms per bullet point
- **Skills Restriction:** NEVER bold individual items in Skills sections
- **Selective Emphasis:** Bold only key technologies, achievements, or quantifiable results
- **Consistency:** Within the same section, use bolding consistently and sparingly
"""

# Final validation checklist (preflight and pagination)
FINAL_VALIDATION_CHECKLIST = """
### FINAL VALIDATION CHECKLIST - PREFLIGHT

**Group 1: Output Schema Validation**
✅ Document starts with \\documentclass
✅ Document ends with \\end{{document}}
✅ No prose, explanations, or comments outside LaTeX
✅ Complete, self-contained LaTeX document
✅ No markdown artifacts (** __ ``` code fences)

**Group 2: Compile Preflight Checks**
✅ No unescaped special characters (&, %, $, _, #) in text
✅ No undefined control sequences (\\newcommand calls)
✅ All braces properly balanced { } and [ ]
✅ All environments properly closed (\\begin → \\end)
✅ Character escaping correct (\\&, \\%, \\$, \\_, \\#)

**Group 3: Pagination and Fit Assessment**
✅ Mentally estimate pagination before output
✅ If overflow risk, compress least relevant content first
✅ Section separation maintained and readable
✅ No excessive spacing that would cause overflow
✅ Layout commands preserved and functional

**Group 4: Consistency Verification**
✅ Date formats consistent with source CV
✅ Unit styles match (e.g., "3 months" vs "90 days")
✅ Proper noun casing preserved (JavaScript, Python, React)
✅ Tense consistent (past for completed, present for current)
✅ Person consistent (no first-person "I", "my", "me")

**Group 5: Content Integrity Check**
✅ All facts verifiable from source CV
✅ No fabricated information or inventions
✅ Quantifications derivable from source data
✅ No exaggeration or misrepresentation
✅ Professional tone maintained throughout

**Group 6: Formatting Compliance**
✅ Section-level bolding follows strict rules
✅ Skills section: ONLY labels bolded
✅ Languages section: ONLY language names bolded
✅ Experience/Projects: Max 2-3 bold terms per bullet
✅ No over-bolding or decoration bold

**Group 7: LaTeX Safety**
✅ No regex artifacts (\\1, \\2, \\3)
✅ URLs properly wrapped in \\texttt{{}}
✅ File paths properly escaped
✅ Code snippets use \\verb|content|
✅ Mathematical symbols properly formatted
"""
