# task_1/features/city.py

import re
import pandas as pd

CITY_MAPPING = {
    "bengaluru": "bengaluru",
    "bangalore": "bengaluru",

    "gurgaon": "gurugram",
    "gurugram": "gurugram",

    "pune": "pune",

    "noida": "noida",

    "delhi": "delhi",
    "new delhi": "delhi",
    "delhi ncr": "delhi",
}


def normalize_city(value):
    """
    Normalize a city value and map it to a canonical city.
    Returns None if the value is invalid.
    """

    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    if not value:
        return None

    # Reject numeric values
    if re.search(r"\d", value):
        return None

    # Map to canonical city
    return CITY_MAPPING.get(value)


def find_city(row, city_column="City", visited_columns=None):

    if visited_columns is None:
        visited_columns = set()

    # Check expected City column
    if (
        city_column in row.index
        and city_column not in visited_columns
    ):

        city = normalize_city(row[city_column])

        if city is not None:
            return city, city_column

    # Search other columns
    for column in row.index:

        if column == city_column:
            continue

        if column in visited_columns:
            continue

        city = normalize_city(row[column])

        if city is not None:
            return city, column

    return None, None