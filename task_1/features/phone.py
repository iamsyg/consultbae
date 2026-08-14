# task_1/features/phone.py

import re
import pandas as pd

def normalize_phone(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    # Allow only a trailing .0 caused by pandas/Excel
    if re.fullmatch(r"\d+\.0", value):
        value = value[:-2]

    # If decimal occurs anywhere else, reject it
    elif "." in value:
        return None

    # Remove non-digit characters
    digits = re.sub(r"\D", "", value)

    # Handle +91 / 91
    if digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]

    # Must be exactly 10 digits
    if len(digits) != 10:
        return None

    # Indian mobile number
    if digits[0] not in "6789":
        return None

    return f"+91-{digits}"


def find_phone(row, phone_column="Phone", visited_columns=None):

    if visited_columns is None:
        visited_columns = set()

    # Check expected Phone column first
    if (
        phone_column in row.index
        and phone_column not in visited_columns
    ):

        phone = normalize_phone(row[phone_column])

        if phone is not None:
            return phone, phone_column

    # Search other columns
    for column in row.index:

        if column == phone_column:
            continue

        if column in visited_columns:
            continue

        phone = normalize_phone(row[column])

        if phone is not None:
            return phone, column

    return None, None