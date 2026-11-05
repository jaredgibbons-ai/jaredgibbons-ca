Dataset pack: BC school districts 38, 39, 40, 41, 42, 43, 44, 45, 75, 78, 93
Retrieval date: 2026-11-05 (America/Vancouver). Working directory: run2_sd38-93/ (does not overwrite the SD33-37 pack).

Primary dataset:
- DataBC "BC Schools - K-12 with Francophone Indicators" (CKAN id 95da1091-7e8c-4aa6-9c1b-5ab159ea7b42)
- Resource: bc_k12_schools_2026_databc_07_update.csv, SCHOOL_YEAR 2025/2026, resource last_modified 2026-07-20
- Catalogue: https://catalogue.data.gov.bc.ca/dataset/95da1091-7e8c-4aa6-9c1b-5ab159ea7b42/resource/5832eff2-3380-435e-911b-5ada41c1d30b
- Local raw copy: k12.csv. Filter: DISTRICT_NUMBER in {038,039,040,041,042,043,044,045,075,078,093} → 476 public + 130 independent (=606). SD93 included province-wide as DataBC lists CSF schools.

Other official sources (retrieved 2026-11-05):
- BC School Contacts registry (bcschoolcontacts.gov.bc.ca API /school/{id}): grade flags, website field, registry-only schools → missing_from_dataset.csv
- DataBC student enrolment-by-grade 2025/26 (enrol.csv): grade fallback / cross-check
- District and school official sites only (no ratings, Fraser Institute, real estate, or review sites):
  SD38 sd38.bc.ca (+ *.sd38.bc.ca school sites); SD39 vsb.bc.ca; SD40 newwestschools.ca and school domains (e.g. herbertspencerschool.ca); SD41 burnabyschools.ca; SD42 sd42.ca; SD43 sd43.bc.ca (+ french-programs / early-french-immersion / late-french-immersion); SD44 sd44.ca; SD45 westvancouverschools.ca; SD75 mpsd.ca; SD78 sd78.bc.ca; SD93 csf.bc.ca (+ *.csf.bc.ca)

Files:
- README.txt (this file)
- all_public_schools.csv, independent_schools.csv
- all_catchments.csv (includes catchment_type: map only | street list | PDF map)
- catchments_text.csv (verbatim street/boundary text where a district/school publishes it)
- missing_from_dataset.csv (registry schools absent from DataBC K-12 extract)
- Per-district: sd{N}_schools.csv, sd{N}_independent_schools.csv, sd{N}_catchments.csv

Source per field:
- school_name, district_number, district_name, street_address, city, postal_code, latitude, longitude: DataBC K-12 (blank if blank in source)
- grades: registry grade flags; enrolment fallback when registry blank (noted); mismatches noted
- level: derived from grades (max≤7 elementary; min≥6 & max≤9 middle; min≥8 secondary); multi-level spans left blank with note (common for SD93 K–12)
- programs: district French Immersion / Programs of Choice pages + StrongStart co-location + CSF Programme francophone; DataBC FI flags used when district page does not list the school (noted as conflict)
- school_url: registry website field first; else district school directory / official school subdomain (noted). Blank if not found. Never invented.
- notes: every conflict, including District lists FI but DataBC FI indicator NO (and vice versa)
- catchments: district official locator/map URL; catchment_type as published (Baragar/map only, PDF map, or street list). SD93 = CSF zones de fréquentation (province-wide francophone board)
- catchments_text.csv: currently Hugh McRoberts Secondary (SD38) street-boundary description copied verbatim from mcroberts.sd38.bc.ca/information/catchment. Other districts in this pack publish maps/PDF/Baragar locators rather than pasteable street lists on the pages reviewed.

Rules followed: blank if source does not say; never fill from memory; no rankings/ratings/Fraser Institute/real estate/review sites.
