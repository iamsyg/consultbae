# task_1/features/experience.py
import pandas as pd

def normalize_experience(value):

    if pd.isna(value):
        return None

    # It should be a number (int or float)
    if not isinstance(value, (int, float)):
        return None

    if value < 0 or value > 6:
        return None

    return value


def find_experience(
    row,
    experience_column="Experience (Years)",
    visited_columns=None
):

    if visited_columns is None:
        visited_columns = set()

    # Expected column first
    if (
        experience_column in row.index
        and experience_column not in visited_columns
    ):

        experience = normalize_experience(
            row[experience_column]
        )

        if experience is not None:
            return experience, experience_column

    # Search other columns
    for column in row.index:

        if column == experience_column:
            continue

        if column in visited_columns:
            continue

        experience = normalize_experience(row[column])

        if experience is not None:
            return experience, column

    return None, None