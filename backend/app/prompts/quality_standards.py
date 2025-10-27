"""
Quality Standards for CV Enhancement Prompts

This module contains quality requirements, factual integrity rules,
and validation standards for CV enhancement operations.

Version: 2.0
Last Updated: 2025-10-27
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

# Factual integrity requirements
FACTUAL_INTEGRITY_REQUIREMENTS = """
FACTUAL INTEGRITY:
- NEVER fabricate or exaggerate experience duration
- Compute duration only from explicit date ranges
- If dates are missing, use neutral phrasing without quantifying time
- Maintain accuracy of all factual information
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
