# task_1/features/email.py

import re
import pandas as pd

EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)

def normalize_email(value):
    """Normalize a single email value."""
    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    if not value:
        return None

    return value


def is_valid_email(value):
    """Check whether a value is a valid email."""
    if not value:
        return False

    return bool(EMAIL_PATTERN.match(value))


def find_email(row, email_column="Email", visited_columns=None):
    """
    Find and normalize an email for one row.

    1. Check the expected email column first.
    2. If invalid/missing, search other unvisited columns.
    3. Return the email and the column where it was found.
    """

    # --------------------------------
    # 1. Check expected email column
    # --------------------------------
    if (
        email_column in row.index
        and email_column not in visited_columns
    ):
        email = normalize_email(row[email_column])

        if is_valid_email(email):
            return email, email_column

    # --------------------------------
    # 2. Search other unvisited columns
    # --------------------------------
    for column in row.index:

        if column == email_column:
            continue

        if column in visited_columns:
            continue

        value = normalize_email(row[column])

        if is_valid_email(value):
            return value, column

    return None, None


# def process_emails(df, email_column="Email"):
#     """Find, normalize and validate emails for the entire DataFrame."""

#     df = df.copy()

#     df["email"] = df.apply(
#         lambda row: find_email(row, email_column),
#         axis=1
#     )

#     # df["email_valid"] = df["email"].notna()

#     return df