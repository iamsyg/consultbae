# task_1/features/project_completed.py

import re
import pandas as pd

def normalize_projects_completed(value):
    """
    Normalize and validate Projects Completed.
    """

    if pd.isna(value):
        return None

    # Convert to string and strip whitespace
    value = str(value).strip()

    if not value:
        return None

    # Must contain ONLY digits
    if not re.fullmatch(r"\d+", value):
        return None

    # Convert to integer
    projects = int(value)

    # Must be between 0 and 20
    if 0 <= projects <= 20:
        return projects

    return None

def find_projects_completed(
    row,
    project_column="Projects Completed",
    visited_columns=None
):
    """
    Find and normalize Projects Completed.

    1. Check expected Projects Completed column first.
    2. If invalid/missing, search other unvisited columns.
    3. Return normalized value and source column.
    """

    if visited_columns is None:
        visited_columns = set()

    # ----------------------------------------
    # 1. Check expected column
    # ----------------------------------------

    if (
        project_column in row.index
        and project_column not in visited_columns
    ):

        projects = normalize_projects_completed(
            row[project_column]
        )

        if projects is not None:
            return projects, project_column

    # ----------------------------------------
    # 2. Search other unvisited columns
    # ----------------------------------------

    for column in row.index:

        if column == project_column:
            continue

        if column in visited_columns:
            continue

        projects = normalize_projects_completed(
            row[column]
        )

        if projects is not None:
            return projects, column

    return None, None