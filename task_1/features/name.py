# task_1/features/name.py

import re
import pandas as pd

def normalize_name(name):
    """
    Normalize and validate a person's name.

    Returns:
        normalized lowercase name if valid
        None if invalid
    """

    if pd.isna(name):
        return None

    # Convert to string and normalize whitespace
    name = str(name).strip().lower()
    name = re.sub(r"\s+", " ", name)

    if not name:
        return None

    # Name should not contain numbers
    if re.search(r"\d", name):
        return None

    # Name should not contain @
    if "@" in name:
        return None

    # Allow letters, spaces, apostrophes and hyphens
    if not re.fullmatch(r"[a-zA-Z]+(?:[\s'-][a-zA-Z]+)*", name):
        return None

    return name


def find_name(row, visited_columns=None, name_column="Full Name"):

    if visited_columns is None:
        visited_columns = set()

    if name_column in row.index and name_column not in visited_columns:

        name = normalize_name(row[name_column])

        if name is not None:
            return name, name_column

    # --------------------------------
    # 2. Search other unvisited columns
    # --------------------------------
    for column in row.index:

        if column == name_column:
            continue

        if column in visited_columns:
            continue

        name = normalize_name(row[column])

        if name is not None:
            return name, column

    return None, None