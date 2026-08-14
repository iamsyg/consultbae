"""Import the three normalized CSV sources into the Supabase people schema.

Run with: python main.py
Set SUPABASE_URL and SUPABASE_KEY in .env first.
"""

import os
from collections import defaultdict
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from normalize_data.normalize_data1 import normalize_data1
from normalize_data.normalize_data2 import normalize_data2
from normalize_data.normalize_data3 import normalize_data3


PROJECT_DIR = Path(__file__).resolve().parent
SOURCE_DIR = PROJECT_DIR.parent


def value_or_none(value):
    """Convert pandas' missing values to normal Python None values."""
    if isinstance(value, list):
        return value
    return None if pd.isna(value) else value


def normalized_records():
    """Read all sources using the feature normalizers already in this project."""
    files_and_normalizers = [
        ("naukri", "source1_naukri_applicants.csv", normalize_data1),
        ("gig_workers", "source2_gig_workers.csv", normalize_data2),
        ("cbnexus", "source3_cbnexus_contacts.csv", normalize_data3),
    ]
    records = []
    for source, filename, normalizer in files_and_normalizers:
        dataframe = normalizer(pd.read_csv(SOURCE_DIR / filename))
        for row in dataframe.to_dict("records"):
            records.append((source, {key: value_or_none(value) for key, value in row.items()}))
    return records


def group_people(records):
    """Return connected groups of records sharing a normalized email or phone.

    Email links Naukri <-> Gig Workers and phone links Naukri <-> CBNexus.
    A connected component therefore gives every source row for one person the
    same person_id, including three-way matches.
    """
    parent = list(range(len(records)))

    def find(index):
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left, right):
        left, right = find(left), find(right)
        if left != right:
            parent[right] = left

    seen_identity = {}
    for index, (_, row) in enumerate(records):
        for field in ("email", "phone"):
            identity = row.get(field)
            if not identity:
                continue
            key = (field, identity)
            if key in seen_identity:
                union(index, seen_identity[key])
            else:
                seen_identity[key] = index

    groups = defaultdict(list)
    for index, record in enumerate(records):
        groups[find(index)].append(record)
    return list(groups.values())


def first_value(rows, field):
    """Use the first available normalized value; source order is deterministic."""
    for row in rows:
        value = row.get(field)
        if value is not None and value != []:
            return value
    return None


def rows_for_source(group, source):
    return [row for row_source, row in group if row_source == source]


def merge_skills(group):
    return sorted({skill for _, row in group for skill in row.get("skills", [])})


def build_person_payload(group):
    rows = [row for _, row in group]
    return {
        "names": first_value(rows, "name"),
        "emails": first_value(rows, "email"),
        "phones": first_value(rows, "phone"),
        "cities": first_value(rows, "city"),
        "skills_superset": merge_skills(group),
    }


def find_existing_person_id(supabase, person):
    """Find an already imported person by either scalar contact field."""
    person_ids = set()
    for column in ("emails", "phones"):
        value = person.get(column)
        if value:
            response = supabase.table("people").select("person_id").eq(column, value).execute()
            person_ids.update(row["person_id"] for row in response.data)

    if len(person_ids) > 1:
        raise ValueError(
            f"More than one database person matches {person['emails']!r} / {person['phones']!r}. "
            "Merge those records manually before rerunning the import."
        )
    return next(iter(person_ids), None)


def upsert_source_rows(supabase, person_id, group):
    """Write source-specific normalized fields using the same person_id."""
    naukri_rows = rows_for_source(group, "naukri")
    if naukri_rows:
        row = naukri_rows[-1]  # A duplicate source row replaces the older one.
        supabase.table("naukri").upsert({
            "person_id": person_id,
            "experience": row["experience"],
            "ctc": row["ctc"],
            "applied_date": str(row["applied_date"]) if row["applied_date"] else None,
        }, on_conflict="person_id").execute()

    gig_rows = rows_for_source(group, "gig_workers")
    if gig_rows:
        row = gig_rows[-1]
        supabase.table("gig_workers").upsert({
            "person_id": person_id,
            "rate": row["rate"],
            "status": row["status"],
        }, on_conflict="person_id").execute()

    cbnexus_rows = rows_for_source(group, "cbnexus")
    if cbnexus_rows:
        row = cbnexus_rows[-1]
        supabase.table("cbnexus").upsert({
            "person_id": person_id,
            "verified": row["verified"],
            "projects_completed": row["projects_completed"],
        }, on_conflict="person_id").execute()


def import_people(supabase):
    """Match, insert/update people, and fill all three child tables."""
    groups = group_people(normalized_records())
    for group in groups:
        person = build_person_payload(group)
        person_id = find_existing_person_id(supabase, person)
        if person_id:
            supabase.table("people").update(person).eq("person_id", person_id).execute()
        else:
            response = supabase.table("people").insert(person).execute()
            person_id = response.data[0]["person_id"]
        upsert_source_rows(supabase, person_id, group)
    return len(groups)


if __name__ == "__main__":
    from supabase import create_client

    load_dotenv(PROJECT_DIR / ".env")
    url, key = os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("Set SUPABASE_URL and SUPABASE_KEY in .env before importing.")
    client = create_client(url, key)
    print(f"Imported {import_people(client)} unique people.")
