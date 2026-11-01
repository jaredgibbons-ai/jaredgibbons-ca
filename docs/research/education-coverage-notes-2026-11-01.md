# Education + Childcare Inventory — Coverage & Method Notes

Generated 2026-11-01 for Jared Gibbons' area research program (jaredgibbons.ca).
Outputs: `education-inventory.csv` (4,464 institution rows), `education-by-area.md` (per-area rollup).

## What this inventory is — and is not

- **Location-based.** An institution is attached to an area only because its building sits there, as evidenced below. It is **not** a catchment inventory: which schools *serve* an area is already documented in the research files' Section 4 catchment work, and nothing here duplicates or contradicts that.
- Every row comes from an official provincial dataset (below). No institution, address, or count was estimated or invented.

## Sources used (all official / primary)

| Category | Source | URL | Read |
|---|---|---|---|
| Public + independent K-12 schools | BC Ministry of Education and Child Care / BC Geographic Warehouse, "BC Schools – K-12 with Francophone Indicators" (2025/2026 school year file, updated Jul 2026) — the same data behind the Ministry's school directory at studentsuccess.gov.bc.ca | https://catalogue.data.gov.bc.ca/dataset/bc-schools-k-12-with-francophone-indicators | 2026-11-01 |
| Licensed childcare | BC Ministry of Education and Child Care, "Child Care Programs and Facilities, registry and map" (the Child Care Map data) | https://catalogue.data.gov.bc.ca/dataset/child-care-map-data | 2026-11-01 |
| Colleges / universities | Government of BC, "Locations of B.C. Post-Secondary Institutions" (public + private degree-granting + theological) | https://catalogue.data.gov.bc.ca/dataset/locations-of-b-c-post-secondary-institutions | 2026-11-01 |
| Area placement evidence | The program's own research files (`batch-1/`, `batch-2/`, `batch-3/`, `batch-4/`, `batch-5/`, `missing/` — 176 files read) | local | 2026-11-01 |

Because one provincial file per category covers every district, no district directory had to be scraped individually — and no district was blocked by an interactive-only directory. The Ministry K-12 file *is* the district-reported data (each row carries its district number/name), so per-district yields below are exact extracts, not samples.

## Per-district yields (K-12, program geography only)

Program geography = the municipalities covered by the master area list (595 rows: 541 named page slugs, the site homepage row, and 53 missing areas). Schools were filtered to districts SD33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 48, 75, 78, 93 **and** to a physical-address city inside program geography: **930 K-12 rows**.

| District | Rows in program geography |
|---|---|
| SD36 Surrey | 168 |
| SD39 Vancouver | 167 |
| SD43 Coquitlam (incl. Port Coquitlam, Port Moody, Anmore) | 87 |
| SD41 Burnaby | 69 |
| SD38 Richmond | 67 |
| SD35 Langley (City + Township, incl. Aldergrove/Fort Langley) | 60 |
| SD34 Abbotsford | 55 |
| SD44 North Vancouver | 47 |
| SD33 Chilliwack (incl. Cultus Lake, Rosedale) | 40 |
| SD37 Delta | 40 |
| SD42 Maple Ridge–Pitt Meadows | 38 |
| SD40 New Westminster | 25 |
| SD75 Mission (incl. Dewdney, Deroche) | 22 |
| SD45 West Vancouver | 19 |
| SD93 Conseil scolaire francophone (francophone schools inside program cities) | 14 |
| SD78 Fraser-Cascade (Hope, Agassiz, Harrison Hot Springs, Mount Currie) | 12 |
| SD48 Sea to Sky | 0 in program geography — see note |

Notes by district:

- **SD48 Sea to Sky:** the program's only Sea-to-Sky area is Furry Creek, and the provincial file lists **no school physically in Furry Creek** (nearest schools are in Squamish, which no program area covers, so Squamish/Whistler/Pemberton schools are excluded and counted nowhere in this inventory). The one Mount Currie school in the file, Q'aLaTKu7em School, is carried under SD78 in the provincial data and is included (city = Mount Currie).
- **SD93 (francophone):** filtered by city like every other district; its 14 in-geography schools are additional to the local districts' counts for the same cities.
- **Independent schools** are inside the same Ministry file (flagged "Independent School"): 190 of the 930 K-12 rows. This is the Ministry's funded independent-school list — the same population FISA BC represents; no separate FISA scrape was needed. Category for these rows is `private`; levels are as the Ministry classifies the school.
- **Facility types** in the file include standard schools plus alternate programs, continuing education, and online-learning schools with physical addresses (29 alternate, 20 provincial online, 15 continuing ed, 8 district online in scope). They are included — they are real directory entries with real addresses — but a reader should know "elementary/secondary" counts include them.
- **Level mapping:** the Ministry's `SCHOOL_EDUCATION_LEVEL` was mapped as Elementary→`elementary`, Middle School→`middle`, Secondary/Senior Secondary/Junior Secondary→`secondary`, Elementary-Secondary and Elementary Jr. Secondary→`elementary+secondary`. Independent schools are categorised `private` regardless of level (the output format has no level column).

## Spot-check against a second official source (SD45)

SD45's own reporting (West Vancouver Schools, Framework for Enhancing Student Learning Report 2024/2025, westvancouverschools.ca) states the district has **18 school sites: 4 secondary (incl. 1 alternate), 11 elementary, 1 Montessori K–5, 2 primary K–3** — district-wide, including Bowen Island and Lions Bay, which are outside program geography. The provincial file yields **19 rows with city = West Vancouver for SD45** (16 public + Collingwood, Mulgrave, St. Anthony's are independent). The public-school names match the district's own location list (westvancouverschools.ca "Location Addresses") one-for-one for the West Vancouver sites: Caulfeild, Chartwell, Cypress Park Primary, Eagle Harbour Montessori, École Cedardale, École Pauline Johnson, Gleneagles, Hollyburn, Irwin Park, Ridgeview, West Bay, Westcot, Rockridge, Sentinel, West Vancouver Secondary, West Vancouver Inglewood Secondary. Two naming variants to know: the district currently styles one school "Gleneagles Ch'axáý Elementary" (provincial file: "Gleneagles Elementary") and "École Pauline Johnson" (file: "Ecole Pauline Johnson Elementary"). Counts reconcile once Bowen Island Community School and Lions Bay Community School (in the district's 18, outside program geography) and the district's alternate-program counting are allowed for; no school appears in one source and not the other for West Vancouver addresses. **Disagreement logged, not silently resolved:** the inventory keeps the provincial file's names.

## How area assignment was decided (and its limits)

1. Each research file was machine-read for mentions of each institution's name. A mention counted as *located-in evidence* only when the sentence/bullet itself (or its schools-section heading) placed the institution in the area — e.g. central-abbotsford-guide's "Public schools physically in the central area … Godson Elementary (33130 Bevan Ave)…". Mentions in catchment/feeder/sample-address contexts were explicitly **not** treated as location evidence (files routinely print catchment schools' addresses — an early pass that trusted address-printing over-assigned, and was discarded).
2. A **namesake rule**: where a school is named for its neighbourhood (Bradner Elementary, Cape Horn Elementary, Mt Lehman Elementary…) and that area's file mentions it, it was assigned to that area.
3. Where two area keys cover the same geography (e.g. `central-abbotsford-guide` and `central-abbotsford`), claims were merged and the school assigned once, to the non-"-guide" key where one exists.
4. Post-secondary campuses (72 rows) were assigned only where placement is unambiguous (e.g. UBC Point Grey cluster → `university-vw`; SFU Burnaby + Fraser International College → `simon-fraser-univer`; SFU Surrey + KPU Civic Plaza → `surrey-city-centre`; downtown campuses → `downtown-vw` / `downtown-nw`; Capilano University main campus → `capilano-nv`). All other campuses are `unassigned-<city>`.
5. **Everything else is `unassigned-<city>` — deliberately not forced.** Of 930 K-12 rows: **172 assigned** to a named area; **23 left unassigned because two or more area files claim the school in located-in language** (conflicts listed below — the files disagree, and no official source in hand settles the boundary); **120 mentioned in a same-city file but never in located-in language**; the remaining **615 are in municipalities whose finer area files are not yet written or do not name them** (batches 5+ still to come, plus topic/non-geographic pages). As later batches land, re-running the placement pass will move more schools out of `unassigned-`.

**The 23 conflicted schools** (two+ area files claim them as located in the area; left unassigned rather than guessed): Cultus Lake Swílhcha Community School; Mountain Elementary (Abbotsford); Delta Secondary; R M Grauer Elementary; Blundell Elementary; Alfred B Dixon Elementary; John Oliver Secondary; L'Ecole Bilingue Elementary; Sir Richard McBride Elementary; Sir Richard McBride Annex; Trafalgar Elementary; Southlands Elementary; Carnarvon Community Elementary; Alexander Academy (Vancouver); Burnaby Central Secondary; Burnaby North Secondary; Burnaby Mountain Secondary; Cameron Elementary; Lyndhurst Elementary; Ecole Seaforth Elementary; Twelfth Avenue Elementary; Stoney Creek Community Elementary; Thomas Haney Secondary.

**Known source-data anomalies (logged, kept as published):**
- Coquitlam College's main campus (2920 Virtual Way) is listed in the post-secondary file with city "Vancouver"; the address is in Burnaby. The row keeps the published city/address verbatim.
- The childcare file spells Burnaby "Bunaby" for some facilities; those rows were normalised to Burnaby (flagged here, the only normalisation applied).
- Fairleigh Dickinson University's Vancouver campus is listed at 842 Cambie Street in the post-secondary file; the area program's own earlier research (missing/oakridge-vw.md) records FDU's campus at Oakridge Park opening Oct 15, 2026. Both are official-source statements from different dates; the inventory keeps the provincial file's row and flags the conflict here rather than rewriting it.
- 3 K-12 rows in scope districts had a blank physical-address city and were excluded.

## Daycare / childcare enumeration — result

**Enumerated in full.** The Child Care Map dataset is published as a bulk CSV by the Ministry, so no health-authority list scraping was needed: **3,462 licensed facilities** (Licensed Group + Licensed Family) have a physical address inside program geography, after removing the file's own 310 duplicate-flagged rows province-wide. This is the complete licensed population as published — it includes licensed preschools and school-age care programs operating as licensed facilities, and it excludes licence-not-required and registered licence-not-required care, which the province does not enumerate by address. City counts: Surrey 655; Vancouver 504; Burnaby 322; Coquitlam 241; Richmond 226; North Vancouver 207; Langley 199 (+ Aldergrove 21, Fort Langley 1); Abbotsford 185; Chilliwack 182 (+ Cultus Lake 1, Rosedale 4); Maple Ridge 161; Delta 129; Port Coquitlam 106; New Westminster 105; Mission 56 (+ Deroche 1); Port Moody 46; West Vancouver 37; Pitt Meadows 28; White Rock 26; Agassiz 7; Hope 7; Anmore 3; Harrison Hot Springs 2.

**Area-level placement of daycares is the inventory's weakest layer, stated plainly:** childcare facilities are almost never named in the research files, so only **3 of 3,462** could be placed in a named area from file evidence; the rest sit at `unassigned-<city>`. Placing them properly needs neighbourhood boundary polygons, which no official source in this pass provides. Fraser Health / Vancouver Coastal Health licensed-facility lists were not separately scraped because the provincial Child Care Map is the licensing registry those lists derive from; a health-authority cross-check remains a possible future verification step, not a missing enumeration.

## Colleges / universities — scope note

72 campus locations in program cities from the provincial locations file: 28 `university`, 44 `college`. The file covers public post-secondary institutions plus private **degree-granting** and theological institutions. It does **not** enumerate the several hundred PTIB-registered private career colleges and language schools in the region; those were **not** captured (no official bulk address list was used for them) — this category is therefore "degree-granting post-secondary," complete for that population, not for every training school.

## Totals

| Category | Rows | Assigned to a named area | Unassigned (city-level) |
|---|---|---|---|
| Elementary | 574 | — | — |
| Middle | 27 | — | — |
| Secondary | 110 | — | — |
| Elementary+secondary | 29 | — | — |
| Private / independent (K-12) | 190 | — | — |
| **K-12 subtotal** | **930** | **172** | **758** |
| College campuses | 44 | — | — |
| University campuses | 28 | — | — |
| **Post-secondary subtotal** | **72** | **18** | **54** |
| Licensed daycare / childcare | 3,462 | 3 | 3,459 |
| **TOTAL** | **4,464** | **193** | **4,271** |

Rollup: 90 of the 594 area keys have at least one institution located in them; 504 area keys have zero (listed as zero in `education-by-area.md`, not omitted — many are topic/price/tool pages that are not geographic areas at all, plus geographic areas whose files are not yet written). The 595th master-list row is the site homepage, also listed with zero.
