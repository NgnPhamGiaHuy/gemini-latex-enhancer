"""
Slicing Rules for Advanced CV Enhancement

This module contains project slicing strategies and advanced features
for specialized CV enhancement operations.

Version: 2.0
Last Updated: 2025-10-27
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
