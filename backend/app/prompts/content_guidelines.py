"""
Content Guidelines for CV Enhancement Prompts

This module contains content structure guidelines, enhancement strategies,
and formatting rules for CV enhancement operations.

Version: 2.0
Last Updated: 2025-10-27
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

# Intelligent selective bolding guidelines
INTELLIGENT_BOLDING_GUIDELINES = """
INTELLIGENT SELECTIVE BOLDING RULES:

Section Labels:
- ONLY bold section labels or leading keywords with colons (e.g., \\textbf{Core Concepts:}, \\textbf{Languages \\& Frameworks:})
- Do NOT bold every skill after the label unless it's a key differentiator
- Avoid mechanical bolding in Skills sections

Bullet Points / Descriptions:
- Bold selectively to emphasize core achievements, technologies, or technical phrases
- Examples: \\textbf{asynchronous crawling engine}, \\textbf{Python}, \\textbf{RESTful APIs}
- Avoid bolding overly generic or repeated terms (e.g., "data", "project", "task")

Consistency Rules:
- Within the same section, use bolding consistently and sparingly
- Never double-wrap in bold (avoid nested braces like \\textbf{{Python}} — use \\textbf{Python})
- Learn from previous sections — if a section consistently overuses bolding, adjust automatically

Section-Specific Rules:
- Skills/Languages: ONLY bold section labels, not individual items
- Experience/Projects: Bold key tools, frameworks, and achievements contextually
- Professional Summary: Bold 2-3 key differentiators maximum
- Education: Bold institution names and degree titles only

Examples:
❌ Overbolded: \\textbf{Core Concepts:} \\textbf{OOP}, \\textbf{SQL}, \\textbf{Data Structures}, \\textbf{Algorithms}
✅ Correct: \\textbf{Core Concepts:} Object-Oriented Programming (OOP), SQL, Data Structures, Algorithms

✅ Balanced bullet: \\item Developed an \\textbf{asynchronous crawling engine} using \\textbf{Python} and aiohttp to optimize media extraction performance.

Quality Control:
- Maximum 2-3 bold terms per bullet point
- Maximum 1-2 bold terms per Skills section item
- Never bold common words like "data", "project", "system" unless they're technical differentiators
"""
