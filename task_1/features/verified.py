# task_1/features/verified.py

import pandas as pd

VALID_VERIFIED = {
    "y": "yes",
    "yes": "yes",
    "n": "no",
    "no": "no"
}


def normalize_verified(value):
    """
    Returns:
        "yes"
        "no"
        None if invalid
    """

    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    return VALID_VERIFIED.get(value)



def find_verified(row, verified_column="verified", visited_columns=None):
    """
    Find and normalize verified status.

    1. Check expected verified column first.
    2. If invalid/missing, search other unvisited columns.
    3. Return normalized value and source column.
    """

    if visited_columns is None:
        visited_columns = set()

    # ----------------------------------------
    # 1. Check expected verified column
    # ----------------------------------------

    if (
        verified_column in row.index
        and verified_column not in visited_columns
    ):

        verified = normalize_verified(row[verified_column])

        if verified is not None:
            return verified, verified_column

    # ----------------------------------------
    # 2. Search other unvisited columns
    # ----------------------------------------

    for column in row.index:

        if column == verified_column:
            continue

        if column in visited_columns:
            continue

        verified = normalize_verified(row[column])

        if verified is not None:
            return verified, column

    return None, None