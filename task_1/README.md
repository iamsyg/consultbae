# ConsultBae data import

`main.py` reads each CSV, runs the existing feature normalizers, and writes the result to Supabase.

## Run

1. Copy `.env.example` to `.env` and add your Supabase URL and write-enabled key.
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python main.py`

The CSV files are expected in the parent folder, as supplied with the assignment.

## Matching rule

Rows are grouped before any database write. Two rows are the same person when their normalized email matches or their normalized phone matches. These links are transitive: a Naukri row can join a Gig Workers row by email and a CBNexus row by phone, producing one `people.person_id` used in every child table. Re-running the script first checks existing `people.emails` and `people.phones`, so it updates rather than creates a second person.

The scalar `emails` and `phones` schema fields store the first normalized value found. If a source has a duplicate record with a different email but the same phone, the shared phone still correctly creates one person; preserve alternate contacts in a separate table if that information must be retained.

## Source analysis / data issues found

- 105 rows become 62 people using exact normalized email/phone matching: 14 three-source groups, 12 two-row groups, 35 one-source groups, and one four-row group caused by a duplicate Gig Workers record.
- Names have casing differences and one missing normalized Naukri name. Names are lowercased by the supplied normalizer; another source's non-empty name fills the person record when available.
- Phones occur as `+91`, `91`, plain 10-digit values, and an invalid leading-zero form. The phone normalizer standardizes valid Indian mobile numbers to `+91-XXXXXXXXXX` and rejects invalid values.
- Cities have casing, whitespace, and aliases such as Bangalore/Bengaluru and Gurgaon/Gurugram. The normalizer maps these to canonical values and leaves unrecognized values empty.
- Dates use mixed formats, including DD-MM-YYYY and ISO dates; invalid dates become empty.
- CTC, hourly/monthly rates, verification values, status casing, skills delimiters, and projects-completed values are normalized by the existing feature modules before insert.
- Duplicate source rows are collapsed into the one allowed child row per person. For the source-specific fields, the last row in that CSV wins.
