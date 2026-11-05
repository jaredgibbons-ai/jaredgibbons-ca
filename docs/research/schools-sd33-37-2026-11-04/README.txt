Dataset: "BC Schools - K-12 with Francophone Indicators" (CKAN id 95da1091-7e8c-4aa6-9c1b-5ab159ea7b42; this is the dataset formerly titled "BC Schools - School Locations"; search for the old title returns this one), DataBC, Open Government Licence - BC.
Resource: "Schools K-12" bc_k12_schools_2026_databc_07_update.csv, SCHOOL_YEAR 2025/2026, resource last_modified 2026-07-20T21:32:36 UTC; package metadata_modified 2026-11-04T13:46 UTC.
URL: https://catalogue.data.gov.bc.ca/dataset/95da1091-7e8c-4aa6-9c1b-5ab159ea7b42/resource/5832eff2-3380-435e-911b-5ada41c1d30b
Retrieved: 2026-11-04 (America/Vancouver). Raw copy: k12.csv. Build script: build.py.

Other official sources (retrieved 2026-11-04):
- BC School Contacts registry (bcschoolcontacts.gov.bc.ca, Ministry of Education and Child Care; DataBC contacts metadata modified 2026-04-27): grade flags, website field (independent schools), registry-only schools.
- DataBC "BC Schools - Student Enrolment" 2025/26 School Level by grade (resource modified 2026-03-19): grade fallback and cross-check.
- District sites: sd33.bc.ca, abbyschools.ca, sd35.bc.ca, surreyschools.ca, deltasd.bc.ca (school lists, URLs, program pages, catchment locators).

Source per field:
- school_name, district, street_address, city, postal_code, latitude, longitude: DataBC K-12 file (unchanged; blank where blank in source).
- grades: registry grade flags; enrolment fallback (noted); mismatches noted.
- level: derived from grades (<=7 elementary; 6-9 middle; >=8 secondary); spans left blank with "Ambiguous level" note; conflicts with DataBC SCHOOL_EDUCATION_LEVEL noted.
- programs: district program pages (URL in source_url), SD35 find-a-school tags, StrongStart (DataBC EAR_LEARN), DataBC French immersion flags.
- school_url: district site directory (public); registry website field, else school's own site via web search (independent, noted). All checked by HTTP on 2026-11-04; non-200 results are in notes.
- catchments: every district publishes only an interactive Baragar locator -> "map only" + URL; no text published.
- missing_from_dataset.csv: schools in the registry not in the DataBC K-12 file.
No ratings, rankings, real-estate or review sources used. No walk times, no descriptions.
