# task_1/normalize-data/normalize_data1.py

import pandas as pd

from features.email import find_email
from features.name import find_name
from features.city import find_city
from features.phone import find_phone
from features.experience import find_experience
from features.ctc import find_ctc
from features.date import find_date
from features.skills import find_skills

def normalize_data1(data):

    normalized_rows = []

    for _, row in data.iterrows():

        # Each person gets their own visited columns
        visited_columns = set()

        # ----------------------------------------
        # EMAIL
        # ----------------------------------------

        email, email_source_column = find_email(
            row,
            email_column="Email",
            visited_columns=visited_columns
        )

        if email_source_column is not None:
            visited_columns.add(email_source_column)

        # ----------------------------------------
        # PHONE
        # ----------------------------------------

        phone, phone_source_column = find_phone(
            row,
            phone_column="Phone",
            visited_columns=visited_columns
        )

        if phone_source_column is not None:
            visited_columns.add(phone_source_column)

        # ----------------------------------------
        # CITY
        # ----------------------------------------

        city, city_source_column = find_city(
            row,
            city_column="City",
            visited_columns=visited_columns
        )

        if city_source_column is not None:
            visited_columns.add(city_source_column)

        # ----------------------------------------
        # EXPERIENCE
        # ----------------------------------------

        experience, experience_source_column = find_experience(
            row,
            experience_column="Experience (Years)",
            visited_columns=visited_columns
        )

        if experience_source_column is not None:
            visited_columns.add(experience_source_column)

        # ----------------------------------------
        # CTC
        # ----------------------------------------

        ctc, ctc_source_column = find_ctc(
            row,
            ctc_column="Current CTC",
            visited_columns=visited_columns
        )

        if ctc_source_column is not None:
            visited_columns.add(ctc_source_column)

        # ----------------------------------------
        # APPLIED DATE
        # ----------------------------------------

        applied_date, date_source_column = find_date(
            row,
            date_column="Applied Date",
            visited_columns=visited_columns
        )

        if date_source_column is not None:
            visited_columns.add(date_source_column)

        # ----------------------------------------
        # SKILLS
        # ----------------------------------------

        skills, skills_source_columns = find_skills(
            row,
            skill_column="Skills",
            visited_columns=visited_columns
        )

        # Skills may come from multiple columns
        visited_columns.update(skills_source_columns)

        # ----------------------------------------
        # NAME
        # ----------------------------------------

        name, name_source_column = find_name(
            row,
            name_column="Full Name",
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
            "phone": phone,
            "city": city,
            "experience": experience,
            "ctc": ctc,
            "applied_date": applied_date,
            "skills": skills
        })

    return pd.DataFrame(normalized_rows)

# naukari_normalized = normalize_data1(data1)
# naukari_normalized.head(5)