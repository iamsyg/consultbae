# task_1/normalize-data/normalize_data3.py

import pandas as pd

from features.name import find_name
from features.city import find_city
from features.phone import find_phone
from features.verified import find_verified
from features.projects_completed import find_projects_completed

def normalize_data3(data):

    normalized_rows = []

    for _, row in data.iterrows():

        visited_columns = set()

        # PHONE
        phone, phone_source_column = find_phone(
            row,
            phone_column="Phone Number",
            visited_columns=visited_columns
        )

        if phone_source_column is not None:
            visited_columns.add(phone_source_column)

        # CITY
        city, city_source_column = find_city(
            row,
            city_column="City",
            visited_columns=visited_columns
        )

        if city_source_column is not None:
            visited_columns.add(city_source_column)

        # VERIFIED
        verified, verified_source_column = find_verified(
            row,
            verified_column="Verified",
            visited_columns=visited_columns
        )

        if verified_source_column is not None:
            visited_columns.add(verified_source_column)

        # PROJECTS COMPLETED
        projects_completed, projects_source_column = find_projects_completed(
            row,
            project_column="Projects Completed",
            visited_columns=visited_columns
        )

        if projects_source_column is not None:
            visited_columns.add(projects_source_column)

        # NAME
        name, name_source_column = find_name(
            row,
            name_column="worker_name",
            visited_columns=visited_columns
        )

        if name_source_column is not None:
            visited_columns.add(name_source_column)

        normalized_rows.append({
            "name": name,
            "phone": phone,
            "city": city,
            "verified": verified,
            "projects_completed": projects_completed
        })

    normalized = pd.DataFrame(normalized_rows)

    # IMPORTANT:
    # Keep Projects Completed as integer while allowing missing values
    normalized["projects_completed"] = (
        pd.to_numeric(
            normalized["projects_completed"],
            errors="coerce"
        ).astype("Int64")
    )

    return normalized