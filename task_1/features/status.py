# task_1/features/status.py

import pandas as pd

VALID_STATUSES = {"active", "inactive", "paused"}

def normalize_status(value):
    """
    Normalize and validate status.

    Valid statuses:
        active
        inactive
        paused

    Returns:
        normalized status if valid
        None otherwise
    """

    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    if value in VALID_STATUSES:
        return value

    return None


def find_status(row, status_column="Status", visited_columns=None):
    """
    Find and normalize status.

    1. Check expected Status column first.
    2. If invalid/missing, search other unvisited columns.
    3. Return normalized status and source column.
    """

    if visited_columns is None:
        visited_columns = set()

    # ----------------------------------------
    # 1. Check expected Status column
    # ----------------------------------------

    if (
        status_column in row.index
        and status_column not in visited_columns
    ):

        status = normalize_status(row[status_column])

        if status is not None:
            return status, status_column

    # ----------------------------------------
    # 2. Search other unvisited columns
    # ----------------------------------------

    for column in row.index:

        if column == status_column:
            continue

        if column in visited_columns:
            continue

        status = normalize_status(row[column])

        if status is not None:
            return status, column

    return None, None