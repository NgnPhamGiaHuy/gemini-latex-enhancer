"""
Slicing Rules for Advanced CV Enhancement

This module contains project slicing strategies and advanced features
for specialized CV enhancement operations.

Version: 2.0
Last Updated: 2025-10-27
"""

# Personal projects slicing (for slicing prompt)
PERSONAL_PROJECTS_SLICING = """
### 🚫 MANDATORY PROJECT SLICING REQUIREMENT
You MUST strictly limit the number of personal projects based on the total count in the original CV. This is NON-NEGOTIABLE and takes absolute precedence over other guidelines.

### PROJECT COUNT RULES

**Rule 1: 3+ Original Projects → Flexible 2-3 Based on Content Length**
- Input: 3 or more projects in source CV
- Action: Keep 2-3 projects based on bullet item lengths AND job relevance
- Decision Process:
  
  **Step 1: Score All Projects**
  - Score each project 1-10 for job relevance
  - Identify top 3 most relevant projects
  
  **Step 2: Assess Content Density**
  - For each of top 3 projects, count number of bullet items per project
  - Calculate total words across all 3 projects
  - Assess if all 3 will fit on one page
  
  **Step 3: Make Flexible Decision**
  - ✅ Keep 3 projects IF:
     - Each has 3 or fewer bullet items AND
     - Total content fits on one page AND
     - All 3 score 7+ for job relevance
  - ✅ Keep 2 projects IF:
     - Projects have 4+ bullet items each OR
     - Content won't fit on one page OR
     - Only 2 projects score 7+ for job relevance
  - Default: When in doubt, keep 2 projects (safer for one-page fit)
  
  **Step 4: Execute Selection**
  - Select top 2 OR top 3 based on decision above
  - DELETE all other projects completely from output
- Compliance Check: Output must contain 2 or 3 project entries maximum

**Flexibility Guidelines:**
- Short bullet lists (< 3 bullets per project) = Can fit 3 projects
- Medium bullet lists (3-4 bullets per project) = Usually 2 projects
- Long bullet lists (5+ bullets per project) = Always 2 projects
- Job relevance scores matter, but page fit is final arbiter

**Rule 2: 2 Original Projects → Keep 1-2**
- Input: 2 projects in source CV
- Action: Keep 1-2 projects based on space
- Process:
  1. If one page can accommodate both: Keep both
  2. If space is tight: Keep only the most relevant one

**Rule 3: 1 Original Project → Keep 0-1**
- Input: 1 project in source CV
- Action: Keep only if highly relevant to job
- Process:
  1. Score project for relevance
  2. If score ≥ 7: Keep it
  3. If score < 7: Remove it entirely

### RELEVANCE SCORING METHODOLOGY
For each project, calculate a numerical score (1-10) using these criteria:

**Scoring Rubric:**
- **Technology Stack Alignment (0-4 points):** How well do the technologies used in the project match job requirements?
- **Project Complexity (0-2 points):** Does the project complexity match the level expected by the job?
- **Industry Relevance (0-2 points):** How relevant is the project domain to the target role/industry?
- **Skill Demonstration (0-2 points):** Does the project showcase skills explicitly mentioned in the job description?

**Example Scoring:**
- Project using 80% matching tech stack + medium complexity + relevant industry + demonstrates 3/5 key skills = Score: 4+1+1+2 = 8/10

### SELECTION EXECUTION PROCESS

**Step 1: Discovery Phase**
- Count total personal projects in source CV
- Identify each project's name and key technologies
- Document the project count category (1, 2, 3, or 4+)

**Step 2: Scoring Phase**
- For each project, calculate relevance score using the rubric above
- Note which projects mention job-relevant technologies and skills
- Rank ALL projects from highest to lowest score

**Step 3: Flexible Selection Phase**
- Apply the rule for your project count category
- **For 3+ projects (new flexible rule):**
  - Check bullet count per project in top 3
  - Estimate total word count for top 3 projects
  - If each has ≤3 bullets AND all 3 fit on one page AND all score 7+: Keep 3
  - Otherwise: Keep top 2 projects
- **For 2 projects:** Keep both if space allows, otherwise keep most relevant
- **For 1 project:** Keep only if score ≥7
- Mark unselected projects for complete removal

**Step 4: Removal Phase**
- DELETE unselected projects entirely from the enhanced CV
- Do NOT include them in output at all
- Ensure only selected projects appear in the Personal Projects section

### CRITICAL REMINDER
The "3-5 items maximum" guideline for other sections does NOT apply to personal projects in slicing mode. These strict project count limits take absolute precedence and are not negotiable.
"""
