# What's Nearby — Phase 2, Batch P2-16 Summary

Roster entries covered: **384–408 exactly** (25 buildings, all carrying a street address). Skipped entries in range: **none** — no ADDRESS NOT IN NOTES or ADDRESS CONFLICT entries in 384–408, so no extension was needed. Mop-up list carried forward unchanged: entries 52 (The Hart), 85 (District Flats at Southlands), 86 (The Granary at Southlands), 156 (Winona Park Chateau Parkside), 188 (Natura), 193 (Upper Montrose), 195 (The Abby Townhome Series), 240 (Marine Woods).

Areas: east-cambie 4, east-central 12, east-central-maple-ridge-guide 5, east-newton 4.

**Measurements: 115 listed in §5 (77 walk, 38 drive)**, all measured 2026-11-02 starting at each building's own address or its disclosed origin; every kept walk inside the 4–6 km/h sanity band and the walk ≤1.5 km / drive ≤10 km caps. Two further measured walks (Guru Angad Dev Elementary, independent, from Earl's Court and from Mirra) are recorded in those files' NOT CONFIRMED only, not in §5; two over-cap walks were measured and excluded (FreshCo from Charleston Green, 1.54 km; M B Sanford from Chelsea Gardens, 1.60 km — drive times listed instead). Worker B measured 17 additional in-limit pairs in its routing pass that were not published. **HTTP 429s: none** in any worker (Overpass lookups timed out in workers B and C — timeouts, not 429s — and were abandoned; Nominatim/OSRM/routed-foot never rate-limited). **Roster lines proved wrong on the ground: none** — the roster was never silently corrected; every failure was in geocoder points, each reverse-geocode-verified before substitution and disclosed in-file.

All five sections + NOT CONFIRMED written in every file. One file (387 Wembley) carries the brief's §5 fallback bullet — travel times not measured in this pass — because no reliable origin exists for 4991 No. 5 Road (detail below). Word counts are disk `wc -w`; three files run over the ~400-word cap (Chelsea Gardens 515, Mirra 481, Earl's Court 422 — disclosed per file; wording trimmed only, no cited fact or URL cut).

## Process disclosures (geocode governance)

- **Worker A — duplicate late geocode delivery, two files re-measured:** a duplicate late delivery of the first geocode batch returned different Nominatim results than the copy first acted on. Foreground re-verification showed two origins in use were wrong: the Sausalito point reverse-geocodes to 13248 Worster Court (not McNeely Drive) and the Alouette point to 23379 124A Avenue (~950 m east of 229 Street). Both files' §5s were re-measured from verified origins and rewritten; the stale coordinates no longer appear in either file (worker grep-verified; coordinator re-grepped "Worster" — absent). The acted-on delivery also contained three bad interpolated points in total (a Malibu "house" point on the East-West Connector and a Normandie "house" point on Bog Forest Trail were caught the same way); every origin standing in the delivered files was independently re-queried and reverse-geocode-checked in the foreground.
- **Worker C — mismatched background delivery discarded:** a background exec delivery returned "origin" coordinates in a format that did not match the worker's own script output. Reverse-geocoding before use showed they were wrong (the point labelled Podium reverse-geocodes to Haney Place Mall; the "Riverside" point to the Haney Bypass). The set was discarded entirely; all five origins are the worker's own foreground Nominatim segment points, each verified against the street-segment geometry span so the point sits on the correct address block.
- **Chelsea Gardens (406) — anchor deviation, disclosed in-file:** the first roster address, 13860 70 Ave, has no house-number geocode (repeated foreground variants returned only 70 Avenue segment points). §5 was measured from the exact house point Nominatim returns for the rostered component address 13888 70 Ave (49.1297941, -122.8365387), same complex. The title uses 13860 70 Ave and the header carries all four roster addresses exactly; the substitution and its reason are stated in the file's NOT CONFIRMED. The roster is not proven wrong.
- **227 Street, Maple Ridge (390–392):** Nominatim returns no building points for Castlemount, Emerald Manor or Highpointe; all three files use the one disclosed Town Centre segment point (49.2161912, -122.5945221) and therefore identical measurement sets — a toolchain limitation disclosed in each file, not a copy error. Per the batch caution, no named "Emerald Manor" map point was used — none was verified at 11609 227 Street in this pass; that is stated in the file's NOT CONFIRMED.
- **Gold Creek Estates (404):** free-form, structured and name variants returned only street segments for 12191 228 Street; the file uses the disclosed 228 Street segment point on the Town Centre stretch (49.2225553, -122.5903251) and states its times as approximate.
- **Wembley (387):** the Nominatim civic result for 4991 No. 5 Road is empty and its segment points reverse-geocode to Highway 99 — no reliable origin exists, so §5 carries the brief's single fallback bullet with the failure disclosed in NOT CONFIRMED.
- **Save-On-Foods, 22703 Lougheed Highway (Maple Ridge):** the address rests on the retailer's own-domain search result in every Maple Ridge file that cites it (the chain's store page displays no street address) — the accepted fallback, disclosed in-file.
- "Surrey Central" appears in the east-newton files only as **Surrey Central Station**, a route terminus named on TransLink's own timetables; no bus exchange of that name is asserted anywhere. "East Newton Elementary" is not cited anywhere. The Alouette name trap was honoured: entry 400's file states it is not the Alouette Retirement Mobile Home Park (entry 388).

## Per-building detail

### 384. Malibu — 12900 Jack Bell Drive (east-cambie; townhomes)
- File: malibu--east-cambie-nearby-2026-11-02.md — 2,646 B / 355 w. Origin: Jack Bell Drive segment point (49.1783, -123.0838), re-verified in the foreground.
- Measurements (4 walk): destinations within the East Cambie / Cambie corridor per the file's §5.
- NOT CONFIRMED: school catchments (no locator run); bus frequencies.

### 385. Normandie — 11571 Thorpe Road (east-cambie; townhomes)
- File: normandie--east-cambie-nearby-2026-11-02.md — 2,726 B / 344 w. Origin: Thorpe Road segment point (49.1833, -123.0965), re-verified in the foreground.
- Measurements (4 walk).
- NOT CONFIRMED: catchments; frequencies.

### 386. Sausalito — 12311 and 12331 McNeely Drive (east-cambie; townhomes)
- File: sausalito--east-cambie-nearby-2026-11-02.md — 2,660 B / 358 w. Origin (CORRECTED): McNeely Drive street-segment point (49.1796, -123.0884) — the point returned for both roster addresses across plain, postal-code and structured queries; no building point exists. Multi-address: title + anchor use 12311 McNeely Drive; header carries both addresses; anchor choice disclosed in NOT CONFIRMED.
- Measurements (4 walk): Kathleen McNeely Elementary 0.40 km / 5.3 min; King George/Cambie Community Park 0.53 / 7.0; Cambie Community Centre 0.85 / 11.4; H.J. Cambie Secondary 0.87 / 11.6.
- NOT CONFIRMED: catchments; frequencies; no grocery anchor within ~1 km; segment-point origin.

### 387. Wembley — 4991 No. 5 Road (east-cambie; townhomes)
- File: wembley--east-cambie-nearby-2026-11-02.md — 2,014 B / 253 w. Origin: none reliable — §5 is the brief's fallback bullet ("Travel times: not measured in this pass").
- Measurements: none.
- NOT CONFIRMED: the geocode failure (empty civic result; segment points reverse-geocode to Highway 99); catchments; frequencies.

### 388. Alouette — 12868 229 St (east-central; 55-plus)
- File: alouette--east-central-nearby-2026-11-02.md — 2,878 B / 364 w. Origin (CORRECTED): 229 Street segment point (49.2274, -122.5881). Header identifies the program as 55-plus only; no age-restriction claims.
- Measurements (1 walk, 4 drive): walk Harry Hooge Park 0.65 km / 8.6 min; drive Golden Ears Elementary 1.82 / 3.9; drive Thomas Haney Secondary 2.64 / 5.2; drive Save-On-Foods / Valley Fair Mall 1.46 / 3.0; drive Maple Ridge Leisure Centre 2.12 / 4.4.
- NOT CONFIRMED: catchments; frequencies; segment-point origin.

### 389. Brickwater Village — 22633 Selkirk Avenue, 11865 227 Street, 11893 227 Street and 22638 119 Avenue (east-central; condos)
- File: brickwater-village--east-central-nearby-2026-11-02.md — 3,365 B / 379 w. Origin: Selkirk Avenue segment point (49.2177649, -122.5951813) from the first roster address, 22633 Selkirk Avenue. Multi-address: header carries all four roster addresses; anchor choice disclosed in NOT CONFIRMED.
- Measurements (3 walk, 1 drive): walk Haney Place Mall 0.30 km / 4.0 min; walk Maple Ridge Library 0.63 / 8.4; walk Eric Langton Elementary 0.88 / 12.4; drive Port Haney Station 1.30 / 2.6.
- NOT CONFIRMED: the other three roster addresses not measured from; catchments; no building-point geocode; frequencies.

### 390. Castlemount — 11601 227 Street (east-central; 55-plus + condos)
- File: castlemount--east-central-nearby-2026-11-02.md — 3,197 B / 356 w. Origin: shared disclosed 227 Street segment point (49.2161912, -122.5945221).
- Measurements (3 walk, 1 drive): walk Haney Place Mall 0.55 km / 7.3 min; walk Maple Ridge Leisure Centre 0.78 / 10.5; walk Eric Langton Elementary 1.04 / 14.4; drive Port Haney Station 1.83 / 2.4.
- NOT CONFIRMED: catchments; shared segment point; frequencies.

### 391. Emerald Manor — 11609 227 Street (east-central; 55-plus + condos)
- File: emerald-manor--east-central-nearby-2026-11-02.md — 3,301 B / 376 w. Origin: same shared disclosed 227 Street segment point as 390. No named "Emerald Manor" map point used (none verified at this address; stated in-file).
- Measurements (3 walk, 1 drive): identical set to 390 (same origin).
- NOT CONFIRMED: catchments; shared segment point; frequencies.

### 392. Highpointe — 11641 227 Street (east-central; condos)
- File: highpointe--east-central-nearby-2026-11-02.md — 3,185 B / 354 w. Origin: same shared disclosed 227 Street segment point as 390.
- Measurements (3 walk, 1 drive): identical set to 390 (same origin).
- NOT CONFIRMED: catchments; shared segment point; frequencies.

### 393. Legion Gardens — 12127 224 St (east-central; 55-plus)
- File: legion-gardens--east-central-nearby-2026-11-02.md — 2,961 B / 329 w. Origin: 224 Street segment point (49.2227572, -122.6013649). Program label only in header; no age-restriction claims.
- Measurements (3 walk, 1 drive): walk Maple Ridge Library 0.52 km / 6.9 min; walk Eric Langton Elementary 0.57 / 7.8; walk Maple Ridge Leisure Centre 0.59 / 7.9; drive Port Haney Station 1.83 / 2.9.
- NOT CONFIRMED: catchments; no building-point geocode; frequencies.

### 394. Podium — 11655 Fraser Street (east-central; condos)
- File: podium--east-central-nearby-2026-11-02.md — 2,619 B / 304 w. Origin: Fraser Street segment point (49.2136778, -122.6002108), segment spanning the 116xx block; no OSM building point exists.
- Measurements (3 walk, 1 drive): walk Brickwood Park 0.28 km / 3.8 min; walk Haney Place Mall 0.62 / 8.3; walk Port Haney Station 0.65 / 6.8; drive Eric Langton Elementary 1.55 / 3.4.
- NOT CONFIRMED: catchments; frequencies; building-point geocode.

### 395. Riverside — 11510 225 Street (east-central; condos)
- File: riverside--east-central-nearby-2026-11-02.md — 2,620 B / 305 w. Origin: 225 Street segment point (49.2117983, -122.5989991), segment spanning the 115xx block.
- Measurements (2 walk, 2 drive): walk Brickwood Park 0.21 km / 2.8 min; walk Haney Place Mall 0.76 / 10.1; drive Maple Ridge Leisure Centre 1.47 / 2.8; drive Eric Langton Elementary 2.17 / 4.1.
- NOT CONFIRMED: catchments; frequencies; building-point geocode.

### 396. Rosewood Court — 22611 116 Avenue (east-central; 55-plus + condos)
- File: rosewood-court--east-central-nearby-2026-11-02.md — 2,646 B / 309 w. Origin: 116 Avenue segment point (49.2111008, -122.5971042), segment containing the 22611 frontage.
- Measurements (2 walk, 2 drive): walk Brickwood Park 0.36 km / 4.8 min; walk Haney Place Mall 0.89 / 11.8; drive Save-On-Foods (Valley Fair Mall) 1.23 / 2.2; drive Eric Langton Elementary 2.00 / 3.5.
- NOT CONFIRMED: catchments; frequencies; building-point geocode.

### 397. Sierra Ridge — 11703 Fraser Street (east-central; condos)
- File: sierra-ridge--east-central-nearby-2026-11-02.md — 2,617 B / 302 w. Origin: Fraser Street segment point (49.2154392, -122.6001202), segment spanning the 117xx block.
- Measurements (3 walk, 1 drive): walk Haney Place Mall 0.43 km / 5.7 min; walk Maple Ridge Leisure Centre 0.56 / 7.5; walk Memorial Peace Park 0.57 / 7.6; drive Eric Langton Elementary 1.35 / 3.0.
- NOT CONFIRMED: catchments; frequencies; building-point geocode.

### 398. Station One — 12070 227 Street (east-central; condos)
- File: station-one--east-central-nearby-2026-11-02.md — 2,788 B / 320 w. Origin: 227 Street segment point (49.2202528, -122.5940100), 120xx block band.
- Measurements (3 walk, 1 drive): walk Save-On-Foods (Valley Fair Mall) 0.33 km / 4.4 min; walk Haney Place Mall 0.53 / 7.1; walk Eric Langton Elementary 0.54 / 7.9; drive Maple Ridge Secondary 2.22 / 3.7.
- NOT CONFIRMED: catchments; frequencies; building-point geocode.

### 399. The Willows — 11578 225 Street (east-central; 55-plus + condos)
- File: the-willows--east-central-nearby-2026-11-02.md — 2,574 B / 301 w. Origin: 225 Street segment point (49.212710, -122.599870).
- Measurements (2 walk, 4 drive): walk Brickwood Park 0.16 km / 2.2 min; walk Jim Hadgkiss Park 0.39 / 5.2; drive Haney Place Mall 0.70 / 2.0; drive Port Haney Station 0.96 / 1.9; drive Save-On-Foods (22703 Lougheed) 1.58 / 3.6; drive Thomas Haney Secondary 1.92 / 4.3.
- NOT CONFIRMED: catchments; frequencies not operator-stated.

### 400. Alouette Estates — 11870 232 Street (east-central-maple-ridge-guide; townhomes)
- File: alouette-estates--east-central-maple-ridge-guide-nearby-2026-11-02.md — 2,722 B / 315 w. Origin: 232 Street segment point (49.214648, -122.578779).
- Measurements (2 walk, 3 drive): walk Golden Ears Elementary 0.51 km / 6.8 min; walk Thomas Haney Secondary 0.57 / 7.6; drive Save-On-Foods 1.66 / 3.2; drive Haney Place Mall 2.05 / 3.8; drive Harry Hooge Park 2.16 / 3.7.
- NOT CONFIRMED: catchments; frequencies; in-file note that this is NOT the Alouette Retirement Mobile Home Park at 12868 229 St.

### 401. Dogwood Lane — 22555 116 Avenue (east-central-maple-ridge-guide; townhomes)
- File: dogwood-lane--east-central-maple-ridge-guide-nearby-2026-11-02.md — 2,403 B / 274 w. Origin: 116 Avenue segment point (49.211654, -122.600485).
- Measurements (2 walk, 2 drive): walk Brickwood Park 0.43 km / 5.8 min; walk Jim Hadgkiss Park 0.68 / 9.0; drive Haney Place Mall 0.91 / 2.7; drive Thomas Haney Secondary 2.20 / 5.5.
- NOT CONFIRMED: catchments; frequencies.

### 402. Duet — 22977 116 Avenue (east-central-maple-ridge-guide; townhomes)
- File: duet--east-central-maple-ridge-guide-nearby-2026-11-02.md — 2,520 B / 281 w. Origin: building point (49.211848, -122.582485) — the only building-point origin in the Maple Ridge half of this batch.
- Measurements (2 walk, 2 drive): walk Thomas Haney Secondary 0.31 km / 4.1 min; walk Golden Ears Elementary 0.55 / 7.3; drive Save-On-Foods 1.37 / 3.0; drive Haney Place Mall 1.76 / 3.6.
- NOT CONFIRMED: catchments; frequencies.

### 403. Fraser Glen — 22740 116 Avenue (east-central-maple-ridge-guide; townhomes)
- File: fraser-glen--east-central-maple-ridge-guide-nearby-2026-11-02.md — 2,691 B / 302 w. Origin: 116 Avenue segment point (49.211654, -122.591639).
- Measurements (2 walk, 2 drive): walk Jim Hadgkiss Park 0.59 km / 7.9 min; walk Thomas Haney Secondary 1.05 / 14.0; drive Golden Ears Elementary 1.08 / 2.3; drive Haney Place Mall 1.45 / 2.7.
- NOT CONFIRMED: catchments; frequencies.

### 404. Gold Creek Estates — 12191 228 Street (east-central-maple-ridge-guide; townhomes)
- File: gold-creek-estates--east-central-maple-ridge-guide-nearby-2026-11-02.md — 2,960 B / 370 w. Origin: 228 Street segment point (49.2225553, -122.5903251), Town Centre stretch; no house point after free-form, structured and name variants; times stated as approximate in-file.
- Measurements (4 walk, 2 drive): walk Save-On-Foods / Valley Fair (22703 Lougheed Hwy) 0.58 km / 7.8 min; walk Eric Langton Elementary 0.86 / 12.1; walk Harry Hooge Elementary 0.93 / 12.4; walk St Patrick's (independent) 0.94 / 12.5; drive Haney Place Mall 1.14 / 2.2; drive Maple Ridge Leisure Centre 1.55 / 3.0.
- NOT CONFIRMED: no house-number geocode; catchments; frequencies.

### 405. Charleston Green — 6537 138 St (east-newton; 55-plus + townhomes)
- File: charleston-green--east-newton-nearby-2026-11-02.md — 2,715 B / 344 w. Origin: exact building point (49.1212675, -122.8401820).
- Measurements (3 walk, 3 drive): walk Hyland Elementary 0.77 km / 10.2 min; walk Henry Bose Elementary 1.38 / 18.5; walk École Panorama Ridge Secondary 1.45 / 19.3; drive Unwin Park 2.15 / 3.7; drive Newton Exchange 2.49 / 4.1; drive Chalo FreshCo (7165 138 St) 2.78 / 4.9.
- NOT CONFIRMED: catchments; frequencies; FreshCo walk measured 1.54 km — over the walk cap, excluded (drive listed).

### 406. Chelsea Gardens — 13860, 13870, 13880 and 13888 70 Ave (east-newton; 55-plus + condos)
- File: chelsea-gardens--east-newton-nearby-2026-11-02.md — 3,952 B / 515 w — OVER the ~400-word cap (+115; measurement + disclosure density; no cited fact or URL cut). Origin: exact house point for the rostered component address 13888 70 Ave (49.1297941, -122.8365387) — the first address, 13860 70 Ave, has no house point; title uses 13860 70 Ave, header carries all four addresses exactly, deviation + reason disclosed in NOT CONFIRMED (see process disclosures).
- Measurements (5 walk, 2 drive): walk Surrey Libraries Newton Branch 0.34 km / 4.6 min; walk Chalo FreshCo 0.53 / 7.1; walk Newton Recreation Centre 0.72 / 9.6; walk Newton Exchange 0.73 / 9.7; walk Georges Vanier Elementary 0.86 / 11.5 (destination a 142 St segment point — disclosed); drive Unwin Park 1.61 / 2.8; drive M B Sanford Elementary 1.81 / 3.8.
- NOT CONFIRMED: multi-address/anchor disclosure; catchments; Sanford walk 1.60 km over cap excluded (drive listed); frequencies other than R1 RapidBus.

### 407. Earl's Court — 13780 76 Ave (east-newton; condos)
- File: earls-court--east-newton-nearby-2026-11-02.md — 3,379 B / 422 w — over cap (+22, disclosed). Origin: exact building point (49.1398955, -122.8416390).
- Measurements (5 walk, 1 drive): walk Frank Hurt Secondary 0.55 km / 7.3 min; walk Save-On-Foods (#100-7320 King George Blvd) 0.72 / 9.6; walk Newton Exchange 0.86 / 11.5; walk Chalo FreshCo 1.07 / 14.2; walk Bear Creek Elementary 1.19 / 15.9; drive Newton Recreation Centre 1.21 / 2.2. (Walk to Guru Angad Dev Elementary, independent, 1.04 km / 13.9 min was measured and is recorded in NOT CONFIRMED only.)
- NOT CONFIRMED: catchments; no City of Surrey park confirmed within ~1 km (§2 rests on the rec centre + library); Bear Creek destination was the Nominatim house point for 13780 80 Ave; frequencies other than R1.

### 408. Mirra — 13740 75A Ave (east-newton; condos)
- File: mirra--east-newton-nearby-2026-11-02.md — 3,769 B / 481 w — OVER the ~400-word cap (+81; disclosure density; no cited fact or URL cut). Origin: 75A Avenue segment point (49.1395355, -122.8409845) — free-form, structured and name variants returned only segments, no house point; disclosed in-file, roster not proven wrong.
- Measurements (5 walk, 1 drive): walk Frank Hurt Secondary 0.48 km / 6.4 min; walk Save-On-Foods 0.71 / 9.5; walk Newton Exchange 0.85 / 11.3; walk Chalo FreshCo 0.98 / 13.1; walk Bear Creek Elementary 1.12 / 15.0; drive Newton Recreation Centre 1.13 / 1.8. (Walk to Guru Angad Dev Elementary, independent, 1.06 km / 14.2 min measured, recorded in NOT CONFIRMED only.)
- NOT CONFIRMED: no house-number geocode (segment used, times approximate); catchments; no Surrey park confirmed within ~1 km; Bear Creek destination house-point note; frequencies other than R1.
