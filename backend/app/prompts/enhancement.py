"""
CV Enhancement Prompt
Enhances LaTeX CV content to align with job requirements

This module contains three prompt versions:
1. CV_ENHANCEMENT_PROMPT: Standard prompt with basic word limits per section
2. CV_ENHANCEMENT_PROMPT_ADVANCED: Advanced prompt with dynamic section analysis
   and strict one-page constraint enforcement
3. CV_ENHANCEMENT_PROMPT_WITH_SLICING: Advanced prompt with intelligent project selection
   and personal projects slicing capabilities

All prompts use shared common sections from shared_template.py for consistency and maintainability.

The advanced prompt is used by default (configurable via USE_ADVANCED_PROMPT setting)
to ensure CVs don't expand beyond one page while maintaining quality and relevance.

Version: 2.0
Last Updated: 2025-10-24
"""

CV_ENHANCEMENT_PROMPT = """
You are an AI specialized in LaTeX CV enhancement.
Enhance this LaTeX CV to align with the following job context:
- Job Title: {job_title}
- Job Description: {job_description}
- Company Name: {company_name}

{common_template}

ONE-PAGE CONSTRAINT:
The CV MUST fit on ONE PAGE. Use these word limits:
- Header/Contact: Minimal (name, email, phone, location)
- Professional Summary: MAX 50 words
- Education: MAX 80 words per degree
- Work Experience: MAX 120 words per position
- Skills: MAX 60 words (concise bullet points)
- Projects: MAX 100 words per project
- Certifications: MAX 40 words per certification
- Additional sections: MAX 60 words each

OPTIMIZATION STRATEGY:
1. Prioritize job-relevant content over general content
2. Use action verbs and quantifiable achievements
3. Remove redundant or outdated information
4. Use bullet points for better space utilization
5. Focus on most recent and relevant experiences
6. Use concise, powerful language - every word must add value

LaTeX CV to enhance:
{latex_content}
"""

# Enhanced prompt with dynamic section analysis
CV_ENHANCEMENT_PROMPT_ADVANCED = """
You are an AI specialized in LaTeX CV enhancement with strict page length control.
Enhance this LaTeX CV to align with the following job context:
- Job Title: {job_title}
- Job Description: {job_description}
- Company Name: {company_name}

{common_template}

ONE-PAGE CONSTRAINT - ABSOLUTE PRIORITY:
The enhanced CV MUST fit on exactly ONE PAGE. This is non-negotiable.

DYNAMIC SECTION ANALYSIS:
First, analyze the CV structure and allocate word budget:
1. Header/Contact (5%): Name, email, phone, location only
2. Professional Summary (8%): MAX 40-60 words, job-focused
3. Core Sections (distribute remaining 87% based on relevance):
   - Work Experience: 40-50% (most important)
   - Education: 15-20%
   - Skills: 15-20%
   - Projects/Portfolio: 10-15%
   - Other sections: 5-10% each

CONTENT PRIORITIZATION:
1. Job Relevance Score: Rate each piece of content 1-10 based on job description match
2. Recency Weight: Recent experience gets higher priority
3. Impact Quantification: Include numbers, percentages, achievements
4. Space Efficiency: Use bullet points, abbreviations, concise phrasing

{quality_assurance}

FINAL CHECK:
Before outputting, mentally verify the CV would fit on one page when printed while maintaining proper spacing and readability.

LaTeX CV to enhance:
{latex_content}
"""

# Enhanced prompt with personal projects slicing
CV_ENHANCEMENT_PROMPT_WITH_SLICING = """
You are an AI specialized in LaTeX CV enhancement with strict page length control and intelligent project selection.
Enhance this LaTeX CV to align with the following job context:
- Job Title: {job_title}
- Job Description: {job_description}
- Company Name: {company_name}

{common_template}

{factual_integrity_rules}

ONE-PAGE CONSTRAINT - ABSOLUTE PRIORITY:
The enhanced CV MUST fit on exactly ONE PAGE. This is non-negotiable.

{personal_projects_slicing}

DYNAMIC SECTION ANALYSIS:
First, analyze the CV structure and allocate word budget:
1. Header/Contact (5%): Name, email, phone, location only
2. Professional Summary (8%): MAX 40-60 words, job-focused
3. Core Sections (distribute remaining 87% based on relevance):
   - Work Experience: 40-50% (most important)
   - Education: 15-20%
   - Skills: 15-20%
   - Projects/Portfolio: 10-15% (SLICED based on relevance)
   - Other sections: 5-10% each

CONTENT PRIORITIZATION:
1. Job Relevance Score: Rate each piece of content 1-10 based on job description match
2. Recency Weight: Recent experience gets higher priority
3. Impact Quantification: Include numbers, percentages, achievements
4. Space Efficiency: Use bullet points, abbreviations, concise phrasing

{quality_assurance}

FINAL CHECK:
Before outputting, mentally verify the CV would fit on one page when printed while maintaining proper spacing and readability.

LaTeX CV to enhance:
{latex_content}
"""
