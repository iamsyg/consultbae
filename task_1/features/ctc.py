# task_1/features/ctc.py

import pandas as pd


def normalize_ctc(ctc):
    if pd.isna(ctc):
        return None

    if ctc > 100:
        return int(ctc / 10000) / 10

    return ctc


def find_ctc(
    row,
    ctc_column="Current CTC",
    visited_columns=None
):

    if visited_columns is None:
        visited_columns = set()

    # Expected column first
    if (
        ctc_column in row.index
        and ctc_column not in visited_columns
    ):

        ctc = normalize_ctc(row[ctc_column])

        if ctc is not None:
            return ctc, ctc_column

    # Search other columns
    for column in row.index:

        if column == ctc_column:
            continue

        if column in visited_columns:
            continue

        ctc = normalize_ctc(row[column])

        if ctc is not None:
            return ctc, column

    return None, None