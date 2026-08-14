# task_1/features/rate.py
import re
import pandas as pd

def normalize_rate(value):
    """
    Normalize rate to INR per month and return in k/month format.

    Examples:
        440/hr       -> "91.52k/month"
        1406/hr      -> "292.45k/month"
        32k/month    -> "32k/month"
        32000/month  -> "32k/month"
    """

    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    if not value:
        return None

    # Extract number + optional unit
    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(k|thousand|l|lakh|lac)?",
        value
    )

    if not match:
        return None

    number = float(match.group(1))
    unit = match.group(2)

    # Convert unit to INR
    if unit in ("k", "thousand"):
        number *= 1_000

    elif unit in ("l", "lakh", "lac"):
        number *= 100_000

    # Convert to monthly rate
    if re.search(r"\b(hour|hr|hourly)\b", value):

        # 8 hours/day × 26 working days/month
        monthly_rate = number * 8 * 26

    elif re.search(r"\b(month|monthly|mo)\b", value):

        monthly_rate = number

    else:
        return None

    if monthly_rate <= 0:
        return None

    # Convert to k
    monthly_k = monthly_rate / 1000

    # Remove unnecessary decimal zeros
    return f"{monthly_k:g}k/month"


def find_rate(row, rate_column="Rate", visited_columns=None):
    """
    Find and normalize rate.

    1. Check expected Rate column first.
    2. If invalid/missing, search other unvisited columns.
    3. Return normalized rate and source column.
    """

    if visited_columns is None:
        visited_columns = set()

    # ----------------------------------------
    # 1. Check expected Rate column
    # ----------------------------------------

    if (
        rate_column in row.index
        and rate_column not in visited_columns
    ):

        rate = normalize_rate(row[rate_column])

        if rate is not None:
            return rate, rate_column

    # ----------------------------------------
    # 2. Search other columns
    # ----------------------------------------

    for column in row.index:

        if column == rate_column:
            continue

        if column in visited_columns:
            continue

        rate = normalize_rate(row[column])

        if rate is not None:
            return rate, column

    return None, None