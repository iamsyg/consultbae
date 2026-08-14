# task_1/features/date.py

import pandas as pd


def normalize_date(date):
    if pd.isna(date):
        return None

    date = pd.to_datetime(
        date,
        errors="coerce",
        dayfirst=True
    )

    if pd.isna(date):
        return None

    return date.date()


def find_date(
    row,
    date_column="Applied Date",
    visited_columns=None
):

    if visited_columns is None:
        visited_columns = set()

    # Expected column first
    if (
        date_column in row.index
        and date_column not in visited_columns
    ):

        date = normalize_date(row[date_column])

        if date is not None:
            return date, date_column

    # Search other columns
    for column in row.index:

        if column == date_column:
            continue

        if column in visited_columns:
            continue

        date = normalize_date(row[column])

        if date is not None:
            return date, column

    return None, None