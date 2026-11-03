# What's Nearby — Phase 2, Batch P2-15 Summary

Roster entries covered: **359–383 exactly** (25 buildings, all carrying a street address). Skipped entries in range: **none**. Mop-up list carried forward unchanged: entries 52 (The Hart), 85 (District Flats at Southlands), 86 (The Granary at Southlands), 156 (Winona Park Chateau Parkside), 188 (Natura), 193 (Upper Montrose), 195 (The Abby Townhome Series), 240 (Marine Woods).

Areas: downtown-ve 5, downtown-vw 4, dunbar 3, dundarave 6, eagle-ridge-cq 2, east-burnaby 1, east-cambie 4.

**Measurements: 109 total (80 walk, 29 drive)**, all measured 2026-11-02 starting at each building's own address or its disclosed origin; every kept walk inside the 4–6 km/h sanity band and the walk ≤1.5 km / drive ≤10 km caps. **HTTP 429s: none** in any worker, including the remediation pass. **Roster lines proved wrong on the ground: none** — the roster was never silently corrected.

All five sections + NOT CONFIRMED written in every file. One file (375 Rosemont) carries the brief's §5 fallback bullet — travel times not measured in this pass — because no reliable origin exists for 2271 Bellevue Avenue after repeated foreground geocode variants (detail below).

## Process disclosures (geocode governance)

- **Workers A and B — late-landing backgrounded geocode output:** In both workers, a backgrounded origin-geocode job's full output landed after a first routing pass and contradicted the origins used (Worker A: One Burrard Place and Vancouver House materially; Worker B: Hotel Georgia ~200 m, Spectrum 1 and 3590 W 39th materially). Both workers re-ran geocodes in the foreground (Worker B's twice-replicated) and re-routed every affected pair; the corrected figures are what stand in the files and below. Worker B retained its original origins for 1188 Howe and Tate Downtown: the replicated Nominatim points sit ~300 m north of the Davie/Drake grid, inconsistent with the replicated Yaletown–Roundhouse Station point on Davie St — a reasoned judgment, flagged by the worker and recorded here; those files state their measurements as from the roster street address.
- **Worker D + remediation pass — Dundarave §5 redo:** Worker D's first Dundarave §5s rested on waterfront-shelf coordinates, and its Regatta Pointe file carried a "2282 Bellevue Avenue" map-label discrepancy note. A later full geocode run returned exact named-building points matching the roster for Regatta Pointe and Seastrand, and no reliable point for Rosemont. On the coordinator's direction a remediation pass: (a) deleted the false "2282 Bellevue" note (grep-verified absent; the named point "Regatta Point, 2280, Bellevue Avenue, Dundarave" matches the roster exactly, so there is no discrepancy), (b) re-ran §5 in the foreground from the named-building points for Regatta Pointe and Seastrand, (c) ran fresh foreground variants for Rosemont — named query returned 0 results, plain/postal/structured queries returned only unstable Bellevue Avenue segment points with differing postal codes, and the known-wrong Ambleside segment point was discarded — so Rosemont's §5 keeps the not-measured bullet with the fresh failure disclosed in-file.
- **Lansdowne Drive, Coquitlam (377/378):** plain civic geocodes returned three distinct wrong segments across runs (incl. one ~1.4 km east at Harbour Chines and one in Westwood Plateau). Both files use disclosed segment points on Lansdowne Drive by the schools (router snap 0 m), re-verified — the right call, disclosed in-file.
- **IGA, Dundarave (destination):** civic-address geocodes for 2491 Marine Dr failed or fell to wrong segments; the OSM node named "IGA" at 1140 25th St (~55 m from the address point) was used as the measurement destination and disclosed in every file that measures to it; §4 keeps the retailer's own locator address, 2491 Marine Dr.
- **West Vancouver Community Centre (2121 Marine Dr):** Worker C could not get a reliable building point and cited it in §2 unmeasured (371–373); the remediation pass obtained named points and measured to it for 374 and 376.
- **Cambie Community Centre, Richmond (destination):** Nominatim's named-building point for 12800 Cambie Rd sits west of the address-number position; used as the named-building point and disclosed in the three files that measure to it (380, 382, 383).
- Word counts below are disk `wc -w`; five files run over the ~400-word cap (disclosed per file; wording trimmed only, no cited fact or URL cut).

## Per-building detail

### 359. One Burrard Place — 1289 Hornby Street (downtown-ve; condos)
- File: one-burrard-place--downtown-ve-nearby-2026-11-02.md — 2,778 B / 350 w. Origin: Nominatim building point (49.2778503, −123.1295899), from the corrected foreground re-run.
- Measurements (4 walk): Emery Barnes Park 0.54 km / 7.3 min; IGA (909 Burrard St) 0.67 / 9.0; Elsie Roy Elementary 0.89 / 11.9; Burrard Station 1.28 / 17.0.
- NOT CONFIRMED: school catchments (no locator run); bus frequencies; exchange/loop names.

### 360. One Wall Centre — 1088 Burrard Street (downtown-ve; condos)
- File: one-wall-centre--downtown-ve-nearby-2026-11-02.md — 2,847 B / 352 w. Origin: named point "One Wall Centre" (49.2805153, −123.1255358).
- Measurements (3 walk, 1 drive): IGA (909 Burrard St) 0.26 / 3.4 w; Nelson Park 0.46 / 6.1 w; Burrard Station 0.86 / 11.5 w; King George Secondary 1.83 / 4.8 d.
- NOT CONFIRMED: catchments; frequencies; exchange names.

### 361. TELUS Garden Residences — 777 Richards Street (downtown-ve; condos)
- File: telus-garden-residences--downtown-ve-nearby-2026-11-02.md — 2,851 B / 353 w. Origin: named point "Telus Garden Residences" (49.2805204, −123.1177996).
- Measurements (4 walk): Central Library 0.22 / 3.0; Vancouver City Centre Station 0.31 / 4.1; CF Pacific Centre 0.36 / 4.9; Nesters Market (990 Seymour St) 0.43 / 5.7.
- NOT CONFIRMED: catchments; frequencies; exchange names.

### 362. Vancouver House — 1480 Howe Street (downtown-ve; condos)
- File: vancouver-house--downtown-ve-nearby-2026-11-02.md — 2,638 B / 338 w. Origin: named point "Vancouver House" (49.2747550, −123.1309861), from the corrected foreground re-run.
- Measurements (4 walk): George Wainborn Park 0.33 / 4.3; Roundhouse Community Centre 0.88 / 11.7; Yaletown–Roundhouse Station 0.96 / 12.7; Urban Fare (177 Davie St) 0.96 / 12.9.
- NOT CONFIRMED: catchments; frequencies; David Lam Park listed in §2 but not measured.

### 363. Woodward's W-43 (W Building) — 128 West Cordova Street (downtown-ve; condos)
- File: woodwards-w-43--downtown-ve-nearby-2026-11-02.md — 2,852 B / 356 w. Origin: named point "Woodwards West Tower" (49.2829488, −123.1080778).
- Measurements (3 walk, 1 drive): Nesters Market (333 Abbott St) 0.17 / 2.3 w; Waterfront Station 0.54 / 7.2 w; Crosstown Elementary 0.64 / 8.6 w; Central Library 0.96 / 2.1 d.
- NOT CONFIRMED: catchments; frequencies; exchange names.

### 364. 1188 Howe — 1188 Howe Street (downtown-vw; condos)
- File: 1188-howe--downtown-vw-nearby-2026-11-02.md — 2,518 B / 315 w. Origin: roster address; worker retained its grid-consistent origin over replicated Nominatim points judged unreliable (see process disclosures).
- Measurements (5 walk): Choices Markets (1202 Richards St) 0.29 km / 3.8 min; Yaletown–Roundhouse Station 0.55 / 7.3; Emery Barnes Park 0.63 / 8.5; Urban Fare (177 Davie St) 0.66 / 8.8; Elsie Roy Elementary 0.69 / 9.2.
- NOT CONFIRMED: catchments; bus frequencies.

### 365. The Private Residences at Hotel Georgia — 667 Howe Street (downtown-vw; condos)
- File: the-private-residences-at-hotel-georgia--downtown-vw-nearby-2026-11-02.md — 2,730 B / 339 w. Origin: corrected replicated address point (49.2837772, −123.1185672), confirmed by the named-building point; first-pass §5 re-routed.
- Measurements (5 walk): CF Pacific Centre 0.20 / 2.7; Vancouver City Centre Station 0.27 / 3.6; Urban Fare Alberni 0.63 / 8.3; Central Library 0.71 / 9.5; Nelson Park 1.12 / 15.0.
- NOT CONFIRMED: catchments; frequencies.

### 366. Spectrum 1 — 111 West Georgia Street (downtown-vw; condos)
- File: spectrum-1--downtown-vw-nearby-2026-11-02.md — 2,942 B / 368 w. Origin: disclosed West Georgia street-segment point (49.2796559, −123.1137340) — no building point exists; disclosed in-file.
- Measurements (5 walk): Central Library 0.26 / 3.6; Stadium–Chinatown Station 0.51 / 6.8; Vancouver City Centre Station 0.53 / 7.1; CF Pacific Centre 0.65 / 8.7; Crosstown Elementary 0.66 / 8.8.
- NOT CONFIRMED: catchments; frequencies.

### 367. Tate Downtown (Tate on Howe) — 1283 Howe Street (downtown-vw; condos)
- File: tate-downtown--downtown-vw-nearby-2026-11-02.md — 2,571 B / 322 w. Origin: roster address; grid-consistent origin retained (see 364 note).
- Measurements (5 walk): Yaletown–Roundhouse Station 0.47 / 6.2; Roundhouse Community Centre 0.48 / 6.4; Elsie Roy Elementary 0.48 / 6.5; Urban Fare (177 Davie St) 0.56 / 7.4; Emery Barnes Park 0.69 / 9.2.
- NOT CONFIRMED: catchments; bus frequencies.

### 368. 3590 West 39th Avenue — 3590 West 39th Avenue (dunbar; condos)
- File: 3590-west-39th-avenue--dunbar-nearby-2026-11-02.md — 2,881 B / 374 w. Origin: corrected replicated address point (49.2360698, −123.1850232). Building is unnamed in the notes; the name is the address, as rostered.
- Measurements (4 walk, 2 drive): Memorial West Park 1.00 / 13.4 w; Dunbar Community Centre 1.01 / 13.5 w; VPL Dunbar Branch 1.15 / 15.3 w; Stong's Market 1.38 / 18.4 w; Lord Kitchener Elementary 1.97 / 3.5 d; Lord Byng Secondary 2.98 / 5.1 d.
- NOT CONFIRMED: catchments; frequencies.

### 369. Fifty-Five 55 Dunbar — 5555 Dunbar Street (dunbar; condos)
- File: fifty-five-55-dunbar--dunbar-nearby-2026-11-02.md — 2,734 B / 338 w. Origin: roster address geocode (49.23583, −123.18576).
- Measurements (3 walk, 2 drive): Dunbar Community Centre 1.02 / 13.6 w; Memorial West Park 1.01 / 13.5 w; Southlands Elementary 1.09 / 14.6 w; Stong's Market 1.38 / 2.8 d; VPL Dunbar Branch 1.27 / 2.7 d.
- NOT CONFIRMED: catchments; bus frequencies.

### 370. West Pointe — 5629 Dunbar Street (dunbar; condos)
- File: west-pointe--dunbar-nearby-2026-11-02.md — 2,599 B / 318 w. Origin: roster address geocode (49.23536, −123.18573).
- Measurements (3 walk, 1 drive): Dunbar Community Centre 1.08 / 14.3 w; Memorial West Park 1.07 / 14.2 w; Southlands Elementary 1.15 / 15.3 w; Stong's Market 1.57 / 3.2 d.
- NOT CONFIRMED: catchments; frequencies.

### 371. The Bellevue by Cressey — 2289 Bellevue Avenue (dundarave; condos + townhomes)
- File: the-bellevue-by-cressey--dundarave-nearby-2026-11-02.md — 3,270 B / 417 w — **OVER CAP +17** (mandated 2299-variant NOT CONFIRMED item on top of a full measurement set). Origin: Nominatim node named "Bellevue, 2289 Bellevue Avenue" (49.33237, −123.17444); roster address is the anchor per the roster note.
- Measurements (3 walk, 2 drive): Dundarave Park 0.83 / 11.1 w; IGA 0.69 / 9.1 w; Irwin Park Elementary 0.66 / 8.7 w; West Vancouver Memorial Library 0.88 / 1.6 d; Park Royal 2.97 / 4.7 d.
- NOT CONFIRMED: **2299 Bellevue Avenue variant — UNCONFIRMED** (appears in the research file and a 55-plus sibling record; roster note: not treated as a conflict); catchments; frequencies; IGA destination-point note; WV Community Centre cited in §2, not measured in this file.

### 372. Bellevue Gardens — 2119 Bellevue Avenue (dundarave; condos)
- File: bellevue-gardens--dundarave-nearby-2026-11-02.md — 3,093 B / 388 w. Origin: Nominatim node named "Bellevue Gardens" (49.32940, −123.16890).
- Measurements (3 walk, 2 drive): WV Memorial Library 0.23 / 3.1 w; Dundarave Park 1.28 / 17.0 w; IGA 1.22 / 16.3 w; Irwin Park Elementary 1.29 / 2.0 d; Park Royal 2.54 / 4.6 d.
- NOT CONFIRMED: catchments; frequencies; IGA point note; WV CC not measured.

### 373. Les Terraces — 2250 Bellevue Avenue (dundarave; condos)
- File: les-terraces--dundarave-nearby-2026-11-02.md — 3,086 B / 389 w. Origin: roster address geocode (49.33097, −123.17365).
- Measurements (3 walk, 2 drive): Dundarave Park 0.84 / 11.2 w; IGA 0.88 / 11.7 w; Irwin Park Elementary 0.85 / 11.3 w; WV Memorial Library 0.70 / 2.0 d; Park Royal 3.00 / 5.3 d.
- NOT CONFIRMED: catchments; frequencies; IGA point note; WV CC not measured.

### 374. Regatta Pointe — 2280 Bellevue Avenue (dundarave; condos)
- File: regatta-pointe--dundarave-nearby-2026-11-02.md — 3,470 B / 438 w — **OVER CAP +38** (post-remediation §5 carries 6 measurements; house style kept rather than dropping measurements). Origin: Nominatim named-building point "Regatta Point, 2280, Bellevue Avenue, Dundarave" (49.3313697, −123.1742502), re-verified in the foreground twice in the remediation pass; origin snaps ~14 m.
- Measurements (5 walk, 1 drive): Dundarave Park 0.78 / 10.4 w; WV Community Centre 0.63 / 8.4 w; WV Memorial Library 0.81 / 10.8 w; Irwin Park Elementary 0.79 / 10.5 w; IGA 0.81 / 10.8 w; Park Royal 3.30 / 5.3 d.
- NOT CONFIRMED: catchments; frequencies (SeaBus frequency in §1 excepted — operator-stated); IGA destination-point note. The earlier "2282 Bellevue Avenue" map-label note was **withdrawn and deleted** in remediation — it came from a superseded geocode run; the verified named point matches the roster address exactly.

### 375. Rosemont — 2271 Bellevue Avenue (dundarave; condos)
- File: rosemont--dundarave-nearby-2026-11-02.md — 3,142 B / 368 w. **§5: travel times not measured in this pass** (single fallback bullet); §§1–4 complete.
- Origin: none reliable. Fresh foreground variants in remediation: named-building query 0 results; "Rosemont Apartments" 0 results; plain, postal-code (V7V 1C7 / V7V 1C6) and structured queries returned only generic Bellevue Avenue segment points with differing postal codes and unstable ranking; the known-wrong Ambleside segment point (49.3270227, −123.1526568) appeared and was discarded. Failure disclosed in-file. A candidate for a later harmonizing pass if a sourced civic point is obtained.
- NOT CONFIRMED: the unmeasured-times disclosure; catchments; frequencies.

### 376. Seastrand — 150 24th Street (dundarave; condos)
- File: seastrand--dundarave-nearby-2026-11-02.md — 3,434 B / 435 w — **OVER CAP +35** (post-remediation, same reason as 374). Origin: Nominatim named-building point "Seastrand, 150, 24th Street, Dundarave" (49.3325579, −123.1787320), re-verified in the foreground twice; snaps ~36–43 m.
- Measurements (5 walk, 1 drive): Dundarave Park 0.27 / 3.6 w; WV Community Centre 1.05 / 14.0 w; WV Memorial Library 1.23 / 16.5 w; Irwin Park Elementary 0.48 / 6.4 w; IGA 0.49 / 6.5 w; Park Royal 3.59 / 5.3 d.
- NOT CONFIRMED: catchments; frequencies; IGA destination-point note.

### 377. 1135 Lansdowne Drive — 1135 Lansdowne Drive (eagle-ridge-cq; townhomes)
- File: 1135-lansdowne-drive--eagle-ridge-cq-nearby-2026-11-02.md — 3,338 B / 421 w — **OVER CAP +21** (mandated origin disclosure on a full measurement set). Origin: disclosed Nominatim segment point on Lansdowne Drive by the schools (postal-code variant; router snap 0 m) — plain civic queries returned wrong segments (see process disclosures), disclosed in-file.
- Measurements (4 walk, 2 drive): Scott Creek Middle School 0.28 / 3.1 w; Gleneagle Secondary 0.57 / 7.5 w; Eagle Ridge Elementary 0.57 / 5.7 w; Eagle Ridge Park 0.73 / 9.0 w; Coquitlam Centre 1.41 / 3.5 d; Coquitlam Central Station 1.86 / 3.9 d.
- NOT CONFIRMED: catchments; bus frequencies; origin-geocode disclosure.

### 378. Eagle Ridge Court — 1170 Lansdowne Drive (eagle-ridge-cq; condos + townhomes)
- File: eagle-ridge-court--eagle-ridge-cq-nearby-2026-11-02.md — 3,360 B / 427 w — **OVER CAP +27** (same reason as 377). Origin: disclosed segment point on Lansdowne Drive by the schools (snap 0 m), re-verified; disclosed in-file.
- Measurements (3 walk, 3 drive): Scott Creek Middle School 0.41 / 5.5 w; Gleneagle Secondary 0.39 / 5.2 w; Eagle Ridge Elementary 0.72 / 8.4 w; Coquitlam Centre 1.27 / 3.3 d; Coquitlam Central Station 1.73 / 3.7 d; Town Centre Park Community Centre 1.72 / 3.1 d.
- NOT CONFIRMED: catchments; bus frequencies; origin-geocode disclosure.

### 379. Saxon — 7908 15th Avenue (east-burnaby; condos)
- File: saxon--east-burnaby-nearby-2026-11-02.md — 2,166 B / 269 w. Origin: roster address geocode (49.2220595, −122.9040951).
- Measurements (1 walk, 2 drive): Twelfth Avenue Elementary 1.17 / 15.5 w; Edmonds Station 5.59 / 9.8 d; Robert Burnaby Park (8155 Wedgewood St) 2.95 / 6.2 d.
- NOT CONFIRMED: SD41 catchments; bus frequencies; no supermarket within ~1 km confirmed — §4 carries the Shoppers Drug Mart anchor (7155 Kingsway #250, Highgate Village) as a retailer own-domain search result, disclosed in-file, in the same pattern as the phase-1 East Burnaby file.
- Destination note: Twelfth Avenue Elementary — two Nominatim returns disagreed; the point consistent with Burnaby address numbering was used.

### 380. Cambie Court — 12311 Cambie Road (east-cambie; townhomes)
- File: cambie-court--east-cambie-nearby-2026-11-02.md — 2,295 B / 291 w. Origin: roster address geocode (49.184624, −123.0710586).
- Measurements (1 walk, 2 drive): Cambie Community Centre 0.86 / 11.6 w; Kathleen McNeely Elementary 2.31 / 4.8 d; King George/Cambie Community Park 2.08 / 4.0 d.
- NOT CONFIRMED: SD38 catchments; bus frequencies; supermarket other than Fruiticana (4121 No. 5 Rd, retailer own-domain search result, disclosed) within ~1 km.

### 381. Cambie Gardens — 11331 Cambie Road (east-cambie; townhomes)
- File: cambie-gardens--east-cambie-nearby-2026-11-02.md — 2,481 B / 308 w. Origin: roster address geocode (49.1849364, −123.0906857).
- Measurements (2 walk, 1 drive): King George/Cambie Community Park 0.58 / 7.8 w; Mitchell Elementary 0.29 / 3.9 w; Cambie Community Centre 0.72 / 1.7 d.
- NOT CONFIRMED: SD38 catchments; bus frequencies; nearest bus exchange name. Transit rests on TransLink timetables read in this pass (routes 410 Cambie Rd, 405 No. 5 Rd).

### 382. Capistrano (Polygon) — 12871 and 12891 Jack Bell Drive (east-cambie; townhomes)
- File: capistrano--east-cambie-nearby-2026-11-02.md — 2,302 B / 295 w. Multi-address entry (not marked ADDRESS CONFLICT): ONE file; title/anchor = first address 12871 Jack Bell Drive (49.1783567, −123.0682673); header carries both addresses exactly as rostered; anchor choice disclosed in NOT CONFIRMED.
- Measurements (3 drive): Cambie Community Centre 1.75 / 3.2; Kathleen McNeely Elementary 3.21 / 6.3; H.J. Cambie Secondary 1.73 / 3.3.
- NOT CONFIRMED: multi-address anchor disclosure; SD38 catchments; bus frequencies.

### 383. Francisco Village (Polygon) — 12411 Jack Bell Drive and 12500 McNeely Drive (east-cambie; townhomes)
- File: francisco-village--east-cambie-nearby-2026-11-02.md — 2,392 B / 302 w. Multi-address entry: ONE file; title/anchor = first address 12411 Jack Bell Drive (49.1793969, −123.0758831); header carries both addresses exactly as rostered; anchor choice disclosed in NOT CONFIRMED.
- Measurements (2 walk, 1 drive): Kathleen McNeely Elementary 1.19 / 15.9 w; H.J. Cambie Secondary 0.85 / 11.4 w; Cambie Community Centre 1.11 / 3.2 d.
- NOT CONFIRMED: multi-address anchor disclosure; SD38 catchments; bus frequencies.

## Batch totals

- Files produced: 25 (buildings folder now holds 375 files: batches 1–15).
- Measurements: **109 (80 walk / 29 drive)**; one building (375 Rosemont) unmeasured with the failure disclosed.
- Word-cap overages: 5 files — The Bellevue by Cressey 417 (+17), 1135 Lansdowne Drive 421 (+21), Eagle Ridge Court 427 (+27), Seastrand 435 (+35), Regatta Pointe 438 (+38). All disclosure/measurement-driven; no cited fact or URL cut anywhere.
- 429s: none. Roster lines proved wrong on the ground: none. Skipped problem entries in range: none.
