"""
Quality standards for CV enhancement prompts.

Defines quality requirements, factual‑integrity rules, and validation standards
for CV enhancement operations.

Version: 2.0
Last updated: 2025‑10‑27
"""

# Quality standards
QUALITY_STANDARDS = """
### QUALITY REQUIREMENTS

**Tone and Authenticity:**
- Maintain professional, confident tone throughout
- Preserve candidate's authentic voice and style
- Avoid generic, templated language
- Use industry-standard terminology naturally

**Factual Accuracy:**
- Every statement must be verifiable from source CV
- No exaggerations, fabrications, or creative additions
- All dates, names, and titles preserved exactly
- Quantifications only from derivable data

**Strategic Highlighting:**
- Emphasize skills transferable to target role
- Showcase achievements with clear impact
- Connect experience to job requirements
- Maintain professional credibility

**Visual Hierarchy:**
- Consistent formatting across sections
- Proper use of spacing and structure
- Clear section boundaries
- Readable, scannable layout
"""

# Advanced quality assurance
ADVANCED_QUALITY_ASSURANCE = """
### ADVANCED QUALITY ASSURANCE CHECKLIST

**Content Quality Checks:**
✅ Every word adds measurable value to job application
✅ Professional tone maintained without sounding robotic
✅ Factual accuracy verified against source data
✅ No filler phrases or redundant information
✅ Clear, impactful language used throughout

**Formatting Consistency Checks:**
✅ Consistent use of bold formatting per section rules
✅ Uniform bullet point structure across sections
✅ Proper spacing and section separation
✅ LaTeX formatting syntax correct and error-free

**Job Description Traceability:**
✅ A Job Alignment Plan exists linking JD requirements to CV evidence
✅ MUST-have requirements prioritized when verifiable evidence exists
✅ NICE-to-have requirements integrated only when space allows and evidence exists
✅ Missing MUST-have evidence noted internally as risks (never fabricated)

**Coverage Targets (Guidance, Not Hard Constraints):**
- Aim for ≥70% coverage of MUST-have items when evidence exists in the source CV
- Incorporate NICE-to-have items opportunistically without displacing higher-value evidence
- If coverage gaps remain, preserve integrity by stating only verifiable adjacent or transferable skills

**Job Alignment Checks:**
✅ Content directly addresses job requirements
✅ Keywords from job description naturally incorporated
✅ Transferable skills explicitly highlighted
✅ Achievements quantified where possible

**Readability Validation:**
✅ No typos or grammatical errors
✅ Professional vocabulary used appropriately
✅ Sentence structure clear and concise
✅ Visual hierarchy supports easy scanning

**Technical Compliance:**
✅ Document will fit on one page when rendered
✅ No LaTeX compilation errors
✅ Character escaping correct
✅ All environments properly closed
"""

# Factual‑integrity requirements
FACTUAL_INTEGRITY_REQUIREMENTS = """
### FACTUAL INTEGRITY - MANDATORY RULES

**Experience Duration:**
- NEVER fabricate or exaggerate duration of employment
- Calculate duration ONLY from explicit start/end dates in source CV
- If dates are missing or ambiguous, use neutral phrasing
- Examples:
  - ✅ "3-month internship" when dates given: Aug 2024 - Nov 2024
  - ✅ "Short-term position" when dates unknown
  - ❌ "6-month role" when actual duration was 3 months
  - ❌ "Led team for 2 years" when actual was 6 months

**Quantification Rules:**
- Only include metrics that can be derived from source material
- Never invent numbers, percentages, or scale indicators
- If data exists but is vague, use conservative estimates
- Example: "Multiple teams" not "10+ teams" unless explicitly stated

**Accuracy Preservation:**
- Maintain exact company names, job titles, and institutions
- Preserve all certifications and credentials exactly as stated
- Keep education degree types and names unchanged
- No modernization of titles or organizations
"""

# Enhanced factual integrity (for slicing prompt variants)
ENHANCED_FACTUAL_INTEGRITY = """
### ENHANCED FACTUAL INTEGRITY - ABSOLUTE REQUIREMENTS

**CRITICAL RULE:** Every single detail in the enhanced CV must be verifiable from the source CV. When in doubt, omit rather than invent.

**Employment Data Preservation:**
- Preserve job titles exactly as stated in source CV
- Keep company names unchanged
- Maintain employment dates precisely (no rounding or estimation)
- Preserve all factual details about roles and responsibilities

**Education and Credentials:**
- Keep degree names and institutions exactly as stated
- Preserve GPA, honors, and academic distinctions verbatim
- Maintain certification names and issuing organizations
- Keep education dates accurate to the source

**Personal Information:**
- Preserve all personal information (GPA, awards, certifications) as stated
- No embellishments or improvements to credentials
- Keep accurate representation of qualifications

**Ambiguity Handling:**
- When clarifying ambiguous phrasing, stay conservative
- Choose the most conservative interpretation
- If information is missing, omit rather than invent or estimate
- Prioritize truthfulness over completeness

**Verification Protocol:**
- Every achievement must be traceable to source CV
- Every skill must appear in the original document
- Every date must match the source exactly
- Every number must be derivable from provided data

**Examples of Proper Handling:**
- ✅ "Fast-paced environment" when source says "startup culture"
- ✅ "Team collaboration" when source mentions "worked with team"
- ❌ "Managed 5-person team" when source doesn't mention team size
- ❌ "Increased revenue by 30%" when source only says "improved sales"
"""
