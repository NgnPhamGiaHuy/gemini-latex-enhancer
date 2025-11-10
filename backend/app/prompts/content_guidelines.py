"""
Content guidelines for CV enhancement prompts.

Provides content‑structure guidelines, enhancement strategies, and formatting
rules for CV enhancement operations.

Version: 2.0
Last updated: 2025‑10‑27
"""

# Content‑structure guidelines
CONTENT_STRUCTURE_GUIDELINES = """
### CONTENT STRUCTURE REQUIREMENTS

**Per-Section Limits:**
- Maximum 3-5 items per section (prioritize most job-relevant)
- Each item should be 30-40 words (180-240 characters) for optimal readability
- **SPECIAL EXCEPTION for Personal Projects (when slicing enabled):**
  *Project count follows strict slicing rules (typically 2 projects for 4+ original projects)*
  *This overrides the standard 3-5 limit for this section only*

**Content Quality Standards:**
1. **Action Verb Requirement:** Start each bullet with a strong action verb
   - Examples: "Engineered", "Developed", "Implemented", "Architected"
   - Avoid weak verbs: "Responsible for", "Assisted with", "Helped"
   
2. **Quantification Focus:** Include numbers, percentages, timeframes when available
   - Good: "Reduced processing time by 75%"
   - Better: "Engineered async engine reducing processing time by 75%"
   - Best: "Engineered async engine using Python/aiohttp, reducing extraction times by 75%"

3. **Job Relevance Priority:** Each bullet must directly relate to job requirements
   - Rate every bullet 1-10 for job relevance
   - Remove or compress bullets scoring below 5
   - Emphasize skills and achievements mentioned in job description

4. **Information Pruning:** Remove redundant, outdated, or irrelevant information
   - Delete duplicate achievements across sections
   - Remove projects >5 years old unless highly relevant
   - Eliminate filler phrases ("various", "multiple", "some")

**JD Traceability:**
- Maintain a Job Alignment Plan that captures MUST-have and NICE-to-have requirements from the job description
- Ensure each retained bullet maps to at least one JD requirement in the plan
- When no clear mapping exists and space is limited, compress or remove the bullet unless it uniquely differentiates the candidate
- Document any uncovered MUST-have requirements internally as risks (never fabricate coverage)
"""

# Enhancement strategy
ENHANCEMENT_STRATEGY = """
### ENHANCEMENT EXECUTION STRATEGY

**Strategy 0: Job Description Analysis (Mandatory Pre-Work)**
- Parse the job description to extract:
  - MUST-have requirements (core responsibilities, essential skills, mandatory credentials)
  - NICE-to-have requirements (preferred skills, bonus qualifications)
  - Skill taxonomy buckets: Languages, Frameworks, Tools, Databases, Cloud, Methodologies, Domains
  - Role scope indicators: seniority, ownership level, domain focus, impact expectations
- Build a Job Alignment Plan containing:
  - A prioritized keyword list (MUST-first) preserving exact JD phrasing
  - A synonym normalization map aligning CV terminology with JD terminology
  - A traceability matrix linking each JD requirement to concrete CV evidence or marking "no evidence"
- Never claim coverage for JD items without CV evidence. When evidence is partial, use conservative phrasing that stays truthful.
- Prioritize MUST-have coverage in Professional Summary and Experience; include NICE-to-have items only when space allows and relevance is high.

**Strategy 1: Keyword Alignment**
- Extract top 10-15 keywords and phrases from job description
- Identify which CV elements naturally contain or relate to these keywords
- Prioritize content that aligns with job terminology
- Rewrite descriptions to incorporate job-relevant terms naturally
- Use the synonym normalization map from the Job Alignment Plan to mirror JD terminology without altering facts

**Strategy 2: Quantification and Metrics**
- Add numerical data where derivable from original content:
  - Time periods: "3-month internship" → "Gained 3 months of hands-on experience"
  - Percentages: "Significantly improved" → "Improved performance by 40%"
  - Scale indicators: "Large user base" → "Served 10,000+ monthly active users"
- Use qualitative terms when metrics aren't available:
  - "Streamlined workflow processes"
  - "Enhanced user engagement"

**Strategy 3: Action Verb Optimization**
- Use verbs from job description when appropriate
- Common strong verbs:
  - Leadership: "Led", "Managed", "Oversaw", "Coordinated"
  - Technical: "Engineered", "Architected", "Developed", "Implemented", "Designed"
  - Achievement: "Optimized", "Improved", "Reduced", "Increased"
  - Innovation: "Pioneered", "Spearheaded", "Introduced", "Created"

**Strategy 4: Industry Terminology**
- Mirror exact terms from job posting naturally
- Example: If job mentions "data pipelines" but CV says "ETL processes", use "data pipelines"
- Example: If job mentions "microservices" but CV says "services", use "microservices"
- Maintain authenticity - don't force terms that don't fit context

**Strategy 5: Experience Consolidation**
- Combine similar roles or projects into cohesive descriptions
- Remove duplicate achievements or skills
- Merge overlapping time periods when appropriate
- Group related technologies and methodologies

**Strategy 6: Strategic Bolding**
- Use \\textbf{{keyword}} sparingly for maximum impact
- Bold 2-3 key terms per bullet point only
- Focus on: Technologies, Key achievements, Quantifiable results
- Never bold: Generic terms, filler words, or redundant phrases
"""

# Intelligent selective‑bolding guidelines
INTELLIGENT_BOLDING_GUIDELINES = """
INTELLIGENT SELECTIVE BOLDING RULES:

⚠️ CRITICAL: SKILLS SECTION - ABSOLUTE RESTRICTION ⚠️
The Skills section has the STRICTEST bolding rules. You MUST follow these exactly:
- ✅ ONLY bold the section label (the text before the colon and including the colon)
- ❌ NEVER bold ANY individual items, technologies, or terms after the colon
- ❌ NEVER bold programming languages, frameworks, tools, databases, or any other skill items

**Skills Section Examples:**
❌ INCORRECT: \\textbf{{Core Concepts:}} Object-Oriented Programming (OOP), \\textbf{{SQL}}, Data Structures, \\textbf{{Algorithms}}
❌ INCORRECT: \\textbf{{Languages & Frameworks:}} \\textbf{{Python}} (Flask, FastAPI), JavaScript (ES6+), \\textbf{{Node.js}}
❌ INCORRECT: \\textbf{{Databases:}} \\textbf{{MySQL}}, \\textbf{{MongoDB}}, PostgreSQL
✅ CORRECT: \\textbf{{Core Concepts:}} Object-Oriented Programming (OOP), SQL, Data Structures, Algorithms
✅ CORRECT: \\textbf{{Languages & Frameworks:}} Python (Flask, FastAPI), JavaScript (ES6+), Node.js, Express.js
✅ CORRECT: \\textbf{{Databases:}} MySQL, MongoDB, PostgreSQL

⚠️ CRITICAL: LANGUAGES SECTION - ABSOLUTE RESTRICTION ⚠️
The Languages section has STRICT bolding rules:
- ✅ ONLY bold the language name label (e.g., \\textbf{{English:}})
- ❌ NEVER bold proficiency levels, certifications, or additional text

**Languages Section Examples:**
❌ INCORRECT: \\textbf{{English:}} Full Professional Proficiency (\\textbf{{IELTS 6.5}})
❌ INCORRECT: \\textbf{{English:}} \\textbf{{Full Professional}} Proficiency (IELTS 6.5)
✅ CORRECT: \\textbf{{English:}} Full Professional Proficiency (IELTS 6.5)
✅ CORRECT: \\textbf{{German:}} Elementary Proficiency

**Bullet Points in Experience/Projects - Moderate Bolding:**
- Maximum 2-3 bold terms per bullet point
- Bold core technologies, frameworks, or major achievements
- Avoid bolding generic terms like "data", "project", "system", "application"
- Examples:
  ✅ Good: \\item Engineered an \\textbf{{asynchronous crawling engine}} using \\textbf{{Python}} and aiohttp
  ❌ Too much: \\item Developed a \\textbf{{high-performance}} \\textbf{{data extraction}} \\textbf{{system}} using \\textbf{{Python}} \\textbf{{FastAPI}}

**Professional Summary - Minimal Bolding:**
- Bold 2-3 key differentiators maximum
- Focus on unique skills or technologies
- Keep bolding minimal and meaningful

**Education Section:**
- Bold only institution names and degree titles
- No other bolding needed

**General Rules:**
- Never double-wrap in bold (avoid nested braces like \\textbf{{{Python}}})
- Within the same section, use bolding consistently
- If unsure, err on the side of less bolding rather than more

**CRITICAL REMINDER:**
The Skills and Languages sections have the ABSOLUTE STRICTEST rules - only section labels should be bolded, NEVER individual items!
"""
