# ConsultBae AI Automation — Task Setup Guide

## 1. Prerequisites

Install:

- Python 3.10+
- Git
- Supabase account
- VS Code or another code editor

---

## 2. Open the Project

```powershell
cd C:\Personal-space\projects\task_1
```

Expected structure:

```text
task_1/
├── main.py
├── .env
├── requirements.txt
├── features/
│   ├── name.py
│   ├── email.py
│   ├── phone.py
│   ├── city.py
│   ├── experience.py
│   ├── ctc.py
│   ├── date.py
│   ├── skills.py
│   ├── rate.py
│   ├── status.py
│   ├── verified.py
│   └── projects_completed.py
├── normalize-data/
│   ├── normalize_data1.py
│   ├── normalize_data2.py
│   └── normalize_data3.py
├── source1_naukri_applicants.csv
├── source2_gig_workers.csv
└── source3_cbnexus_contacts.csv
```

---

## 3. Create a Virtual Environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

---

## 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

If `requirements.txt` does not exist:

```powershell
pip install pandas supabase python-dotenv
```

Then:

```powershell
pip freeze > requirements.txt
```

---

## 5. Configure Supabase

Create a Supabase project and obtain:

- `SUPABASE_URL`
- `SUPABASE_KEY`

Create a `.env` file inside `task_1`:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_key
```

Never commit `.env`.

Add this to `.gitignore`:

```gitignore
.venv/
.env
__pycache__/
*.pyc
```

---

## 6. Create the Database

Open **Supabase → SQL Editor → New Query** and run the database schema.

The database is structured as:

```text
people
   │
   ├── naukri
   ├── gig_workers
   └── cbnexus
```

`people` stores consolidated identity information.

`naukri` stores:

```text
experience
ctc
applied_date
```

`gig_workers` stores:

```text
rate
status
```

`cbnexus` stores:

```text
verified
projects_completed
```

Each source table references `people(person_id)`.

---

## 7. Add the Source CSV Files

Make sure these files are available to the project:

```text
source1_naukri_applicants.csv
source2_gig_workers.csv
source3_cbnexus_contacts.csv
```

The current `main.py` uses:

```python
SOURCE_DIR = PROJECT_DIR.parent
```

Therefore, verify that the CSV location matches this path.

---

## 8. Data Normalization

Each source is passed through its corresponding normalizer:

```python
normalize_data1(data1)
normalize_data2(data2)
normalize_data3(data3)
```

The normalization layer handles:

- Name normalization
- Email validation and normalization
- Phone normalization
- City normalization
- Experience normalization
- CTC normalization
- Date normalization
- Skills normalization
- Rate normalization
- Status normalization
- Verified normalization
- Projects completed normalization

Invalid or missing values are represented as `None`, and misplaced values can be searched in other unvisited columns.

---

## 9. Identity Matching

The primary matching identifiers are:

```text
email
phone
```

A match occurs when either normalized email or phone is shared.

Example:

```text
A: phone=111, email=a@gmail.com
B: phone=111, email=b@gmail.com
```

These records are merged because the phone number is common.

Likewise:

```text
A: phone=111, email=a@gmail.com
B: phone=222, email=a@gmail.com
```

These records are merged because the email is common.

If both phone and email are different, the records remain separate.

---

## 10. Source-Specific Data

After a person receives a `person_id`, source-specific fields are stored in the corresponding table:

```text
people
  person_id
       │
       ├── naukri
       │     ├── experience
       │     ├── ctc
       │     └── applied_date
       │
       ├── gig_workers
       │     ├── rate
       │     └── status
       │
       └── cbnexus
             ├── verified
             └── projects_completed
```

---

## 11. Run the Import

From the project directory:

```powershell
python -m main
```

A successful run should print something similar to:

```text
Imported <number> unique people.
```

---

## 12. Verify Supabase

Open:

**Supabase → Table Editor**

Check:

```text
people
naukri
gig_workers
cbnexus
```

Verify that the child tables reference the correct `person_id` from `people`.

---

## 13. Validation Checklist

### Identity Matching

- [ ] Same phone + different email → one person
- [ ] Same email + different phone → one person
- [ ] Same phone + same email → one person
- [ ] Different phone + different email → separate people
- [ ] Transitive phone/email relationships → one person

### Data Preservation

- [ ] Preserve unique emails
- [ ] Preserve unique phone numbers
- [ ] Preserve unique cities
- [ ] Preserve unique names
- [ ] Combine and deduplicate skills

### Data Types

| Field | Expected Format |
|---|---|
| `experience` | Numeric |
| `ctc` | Numeric |
| `applied_date` | PostgreSQL `DATE` |
| `rate` | Monthly rate |
| `status` | `active`, `inactive`, `paused` |
| `verified` | `yes`, `no` |
| `projects_completed` | Integer, 0–20 |

---

## 14. Git Setup

```powershell
git init
git branch -M main
git add .
git commit -m "Complete ConsultBae AI automation task"
```

Connect the repository:

```powershell
git remote add origin <your-repository-url>
git push -u origin main
```

Before pushing:

```powershell
git status
```

Make sure `.env` is not committed.

---

## 15. Overall Pipeline

```text
             ┌─────────────────────┐
             │    3 Source CSVs    │
             │                     │
             │ Naukri              │
             │ Gig Workers         │
             │ CB Nexus            │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │ Data Normalization  │
             │                     │
             │ Email / Phone       │
             │ Name / City         │
             │ Skills              │
             │ CTC / Rate          │
             │ Dates / Status      │
             │ Verified / Projects │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │ Identity Matching   │
             │                     │
             │ Email OR Phone      │
             │ Transitive Matching │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │ Consolidated Person │
             │                     │
             │ person_id           │
             │ names               │
             │ emails              │
             │ phones              │
             │ cities              │
             │ skills_superset     │
             └──────────┬──────────┘
                        │
              ┌─────────┼─────────┐
              ▼         ▼         ▼
          ┌────────┐ ┌────────┐ ┌─────────┐
          │ Naukri │ │  Gig   │ │ CBNexus │
          │        │ │Workers │ │         │
          └────────┘ └────────┘ └─────────┘
                        │
                        ▼
                ┌──────────────┐
                │   Supabase   │
                │  PostgreSQL  │
                └──────────────┘
```

## 16. Quick Start

For an already configured project:

```powershell
cd C:\Personal-space\projects\task_1
.venv\Scripts\activate
pip install -r requirements.txt
python -m main
```

Then verify the consolidated records in Supabase.




# **Task 4** 

# **Data Issues Report** 

_Data quality problems identified and remediation applied across the three source files_ 

## **1. Scope** 

This report documents the data-quality problems addressed while normalizing and merging the three supplied source systems: Naukri applicants, Gig Workers, and CBNexus contacts. The assignment states that the CSVs intentionally contain overlapping people and inconsistent, messy data, and requires a specific account of the problems found and how they were handled. 

## **2. Source files reviewed** 

|Source|File|Rows|
|---|---|---|
|Naukri Applicants|source1_naukri_applicants.csv|42|
|GigWorkers|source2_gig_workers.csv|32|
|CBNexus Contacts|source3_cbnexus_contacts.csv|31|



## **3. Data quality issues and remediation** 

|Field / Area|Problem|Action taken|
|---|---|---|
|Names|Leading/trailing whitespace and<br>inconsistent casing.|Strip whitespace, collapse repeated<br>spaces,and normalize to lowercase.|
|Names|Values containing numbers are not<br>validperson names.|Reject them and search other<br>unvisited columns for a valid name.|
|Names|Values containing '@' are not valid<br>names and mayactuallybe emails.|Reject them and continue searching<br>other columns.|
|Names|Values containing characters such<br>as '/', '*', or other disallowed<br>symbols are invalid.|Validate against the allowed name<br>pattern and search other columns<br>when invalid.|
|Emails|Leading/trailing whitespace and<br>inconsistent casing.|Strip whitespace and convert to<br>lowercase.|
|Emails|Malformed values in the expected<br>email column.|Validate with an email pattern;<br>invalid values become None.|
|Emails|Email may be stored in an<br>unexpected column.|Check the expected Email column<br>frst, then search other unvisited<br>columns.|
|Phones|Phone values may be parsed as<br>integers/foats instead of strings.|Convert to string before<br>normalization.|
|Phones|Formatting, whitespace, and<br>decimal artifacts can appear in<br>phone values.|Normalize formatting and validate<br>the fnal 10-digit Indian number<br>before storingit.|
|Phones|A phone may be present in another<br>column instead of the expected<br>phone column.|Search other unvisited columns<br>when the expected value is<br>invalid/missing.|
|Cities|Inconsistent casingand whitespace.|Stripand normalize casing.|
|Cities|Equivalent city variants occur,<br>including Bengaluru/Bangalore,<br>Gurgaon/Gurugram, and Delhi/New<br>Delhi/Delhi NCR.|Map known variants to a canonical<br>city representation.|



|Cities|Numeric/unrelated values can<br>appear where a cityis expected.|Reject invalid city values and search<br>other unvisited columns.|
|---|---|---|
|Current CTC|Some of the values are like 472935|Represented in 4.7|
|Current CTC|The valid CTC may be located in<br>another column.<br>|Search other unvisited columns<br>using condition CTC > 100 (To<br>diferentiate from experience) when<br>the expected feld is invalid.|
|Dates|Dates appear in diferent formats.|Parse with pandas and convert<br>successful values to Python date<br>objects suitable for PostgreSQL<br>DATE.|
|Dates|Ambiguous month/day versus<br>day/month parsing can produce<br>warnings.|Invalid/unparseable values are<br>converted to None and parsing is<br>explicitly handled in the<br>normalization layer.|
|Experience|Experience may be non-numeric.|Reject it and search other unvisited<br>columns using condition exp >= 0 &&<br>exp <= 6 (0 and 6 are the min and<br>max valuepossible).|
|Skills|Inconsistent capitalization and<br>whitespace.|Lowercase and strip every skill.|
|Skills|Multiple delimiters can be used<br>within one skills feld.|Split on common delimiters such as<br>comma, pipe,semicolon,and slash.|
|Skills|Duplicate skills can occur.|Deduplicate and return a consistent<br>sorted list.|
|Skills|Skills may be misplaced in another<br>column.|Validate against the known skill set<br>and search other unvisited columns.|
|Rate|Rates can be hourly or monthly and<br>can use k/lakh notation.|Parse the number/unit and<br>normalize to monthly.|
|Rate|A valid rate may occur outside the<br>expected Rate column.|Search other unvisited columns.|
|Status|Casingand whitespace vary.|Stripand lowercase.|
|Status<br>|Unexpected status values may<br>occur.|Accept only active, inactive, or<br>paused; otherwise search other<br>columns.|
|Verifed<br>|Y/y and Yes/yes represent the same<br>value; N/n and No/no represent the<br>other value.<br>|Normalize whitespace/case and<br>map Y/Yes → yes and N/No → no.|
|Verifed|Verifed value may be misplaced.|Search other unvisited columns<br>when the expected feld is<br>invalid/missing.|
|Projects Completed|Pandas may represent an integer<br>count as a string/foat such as '14.0'.|Convert integer-valued numeric<br>representations to Python int.|
|Projects Completed|<br>Counts outside the confgured range<br>are invalid.|Accept only integers from 0 through<br>20.|
|Column ambiguity|Source schemas difer, so a feld<br>may be found under an unexpected<br>column.|Check the expected column frst and<br>then inspect other unvisited<br>columns.|
|Cross-source identity|There is no common ID across the<br>three source systems.|Use normalized email and phone as<br>primaryidentitysignals.|



## **4. Cross-source matching** 

- Records sharing a normalized phone number are treated as the same person even when their emails differ. 

- Records sharing a normalized email address are treated as the same person even when their phones differ. 

- If neither normalized email nor phone is shared, records are not merged solely because names or cities look similar. 

- Skills from the source records are combined into a skills superset. 

## **5. Type and database consistency** 

- Normalized application dates are converted to Python date values for PostgreSQL DATE. 

- Projects Completed is normalized to an integer and constrained to the 0–20 range before insertion into PostgreSQL INTEGER. 

- Gig-worker status is restricted to active, inactive, or paused. 

- CBNexus verification is restricted to yes or no. 

## **6. Note on observed issues versus validation safeguards** 

Some entries above describe concrete inconsistencies encountered during normalization (for example, city variants, mixed verification representations, rate units, and numeric/string representations). Other entries are validation safeguards implemented because the source schemas allow a value to be missing, misplaced, or malformed. These safeguards prevent bad values from entering the consolidated database. 

## **7. Summary** 

The pipeline addresses formatting inconsistencies, invalid values, misplaced fields, type mismatches, unit conversion, duplicate skills, categorical normalization, date normalization, and cross-source identity conflicts. The objective is to create consistent database-ready values while preserving useful differences between source records. 




## Stuck Log

### 1. Entire row shifted in `source2_gig_workers.csv`

**What I got stuck on**

While working with `source2_gig_workers.csv`, I found an edge case where one row was **entirely shifted**. The values were not present under their expected column names. For example, a value that should have been in the `skill_tags` column could appear under another column because the complete row structure was shifted.

My initial normalization approach assumed that each value would be present in its expected column.

**What I asked AI**

I asked AI:

> "There is a row where the columns are shifted. How can I identify the correct values?"

The initial suggestions focused mainly on validating the values found in the expected columns.

**What I rejected and why**

I rejected the validation-only approach because it only answers:

> "Is this value valid?"

It does not answer:

> "Where is the correct value if it is not in the expected column?"

For example, simply validating the `skill_tags` column would return an invalid/missing result, even though the actual skills might exist in another column.

**How I got unstuck**

I changed the approach from **only validating the expected column** to **searching across the other columns when the expected column does not contain a valid value**.

I used the possible characteristics of each field to identify it:

- Email → email pattern
- Phone → valid 10-digit phone number
- City → known/normalized city values
- Skills → keywords from the known skills set extracted from the datasets
- Experience → numeric value within the expected range
- CTC → numeric value/range consistent with CTC
- Date → valid date format
- Rate → recognizable rate/unit such as `/hr` or `/month`
- Status → `active`, `inactive`, `paused`
- Verified → `yes`, `no`, `y`, `n`
- Projects Completed → integer from `0` to `20`
- Name → valid name-like string

I also introduced a `visited_columns` concept so that once a column had already been identified as containing one field, it would not unnecessarily be reused while searching for another field.

This made the normalization process more resilient to misplaced or shifted data instead of assuming the CSV structure was always correct.

---

### 2. Connecting n8n to the PostgreSQL/Supabase database

**What I got stuck on**

I had not previously used **n8n with a database**, so I was unsure how to connect the workflow to the PostgreSQL/Supabase database and what should happen after the PostgreSQL node.

**What I asked AI**

I asked AI how to set up the database connection and how to continue the workflow after the PostgreSQL node.

The guidance took me through:

1. Connecting n8n to PostgreSQL.
2. Configuring the PostgreSQL credentials.
3. Selecting the appropriate database operation.
4. Passing data from one node to the PostgreSQL node.
5. Understanding the output returned by the PostgreSQL node.
6. Connecting the PostgreSQL result to the next step in the workflow.

**What I learned**

The important part was understanding that the PostgreSQL node is not necessarily the end of the workflow. Its output can be passed to subsequent n8n nodes and used to continue the automation.

I used this to build the workflow visually in n8n rather than implementing the entire automation purely in code.

**What I rejected and why**

I did not replace the n8n workflow with a pure-code implementation because the assignment specifically required demonstrating the use of a no-code/low-code automation tool.

Instead, I used AI to understand the n8n/PostgreSQL integration and then configured and tested the workflow myself.