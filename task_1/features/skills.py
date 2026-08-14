# task_1/features/skills.py
import re
import pandas as pd

KNOWN_SKILLS = {
    'pandas', 
    'rest apis', 
    'mysql', 
    'fastapi', 
    'javascript', 
    'zapier', 
    'react', 
    'docker', 
    'web scraping', 
    'sql', 
    'langchain', 
    'python', 
    'mongodb', 
    'selenium', 
    'n8n'
}

def normalize_skills(skills):
    """
    Normalize skills:
    - Convert to string/list
    - Convert to lowercase
    - Strip whitespace
    - Remove duplicates
    - Return a list of unique skills
    """

    if pd.isna(skills):
        return []

    # Handle list / array values
    if isinstance(skills, (list, tuple, set)):
        values = skills
    else:
        # Convert to string
        skills = str(skills).strip()

        if not skills:
            return []

        # Split on common delimiters
        values = re.split(r"[,|;/]", skills)

    # Normalize and remove duplicates
    unique_skills = set()

    for skill in values:

        skill = str(skill).strip().lower()

        if skill:
            unique_skills.add(skill)

    # Return sorted list for consistent output
    return sorted(unique_skills)



def find_skills(
    row,
    skill_column="Skills",
    visited_columns=None
):

    if visited_columns is None:
        visited_columns = set()

    all_skills = []
    source_columns = set()

    # ----------------------------------------
    # Check expected Skills column first
    # ----------------------------------------

    if (
        skill_column in row.index
        and skill_column not in visited_columns
    ):

        skills = normalize_skills(row[skill_column])

        valid_skills = [
            skill for skill in skills
            if skill in KNOWN_SKILLS
        ]

        if valid_skills:
            all_skills.extend(valid_skills)
            source_columns.add(skill_column)

            return all_skills, source_columns

    # ----------------------------------------
    # Search other columns
    # ----------------------------------------

    for column in row.index:

        if column == skill_column:
            continue

        if column in visited_columns:
            continue

        skills = normalize_skills(row[column])

        valid_skills = [
            skill for skill in skills
            if skill in KNOWN_SKILLS
        ]

        if valid_skills:
            all_skills.extend(valid_skills)
            source_columns.add(column)

    # Remove duplicates
    all_skills = sorted(set(all_skills))

    return all_skills, source_columns