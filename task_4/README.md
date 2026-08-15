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
