# task_1/normalize-data/normalize_data2.py
import pandas as pd

from features.email import find_email
from features.name import find_name
from features.city import find_city
from features.rate import find_rate
from features.status import find_status
from features.skills import find_skills

def normalize_data2(data):

    normalized_rows = []
    
    for _, row in data.iterrows():

        # Each person gets their own visited columns
        visited_columns = set()

        # ----------------------------------------
        # EMAIL
        # ----------------------------------------

        email, email_source_column = find_email(
            row,
            email_column="email_id",
            visited_columns=visited_columns
        )

        if email_source_column is not None:
            visited_columns.add(email_source_column)

        # ----------------------------------------
        # RATE
        # ----------------------------------------

        rate, rate_source_column = find_rate(
            row,
            rate_column="rate",
            visited_columns=visited_columns
        )

        if rate_source_column is not None:
            visited_columns.add(rate_source_column)

        # ----------------------------------------
        # CITY
        # ----------------------------------------

        city, city_source_column = find_city(
            row,
            city_column="location",
            visited_columns=visited_columns
        )

        if city_source_column is not None:
            visited_columns.add(city_source_column)

        # ----------------------------------------
        # STATUS
        # ----------------------------------------

        status, status_source_column = find_status(
            row,
            status_column="Status",
            visited_columns=visited_columns
        )

        if status_source_column is not None:
            visited_columns.add(status_source_column)

        # ------------------------------------------
        # SKILLS
        # -------------------------------------------

        skills, skills_source_columns = find_skills(
            row,
            skill_column="skill_tags",
            visited_columns=visited_columns
        )

        # Skills may come from multiple columns
        visited_columns.update(skills_source_columns)

        # ----------------------------------------
        # NAME
        # ----------------------------------------

        name, name_source_column = find_name(
            row,
            name_column="worker_name",
            visited_columns=visited_columns
        )

        if name_source_column is not None:
            visited_columns.add(name_source_column)

        # ----------------------------------------
        # CREATE NORMALIZED ROW
        # ----------------------------------------

        normalized_rows.append({
            "name": name,
            "email": email,
            "rate": rate,
            "city": city,
            "status": status,
            "skills": skills
        })

    return pd.DataFrame(normalized_rows)

# gig_workers = normalize_data2(data2)
# gig_workers.head(21)