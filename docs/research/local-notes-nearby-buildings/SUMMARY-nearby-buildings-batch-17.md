# What's Nearby — Phase 2, Batch P2-17 Summary

Roster entries covered: **409–434** (25 buildings produced). Skipped in range: **entry 415, Connaught (Grosvenor Edgemont), edgemont — ADDRESS CONFLICT (3230 Connaught Crescent / 3220 Connaught Crescent)**, held for the mop-up batch; the batch extended to entry 434 to reach 25 addressed buildings. Mop-up list is now 9 entries: 52 (The Hart), 85 (District Flats at Southlands), 86 (The Granary at Southlands), 156 (Winona Park Chateau Parkside), 188 (Natura), 193 (Upper Montrose), 195 (The Abby Townhome Series), 240 (Marine Woods), 415 (Connaught). No address was researched for the skipped entry.

Areas: east-newton 2, east-newton-guide 4, edgemont 3, edmonds-be 16.

**Measurements: 108 listed in §5 (78 walk, 30 drive)**, counted from disk, all measured 2026-11-02 starting at each building's own address or its disclosed origin; every kept walk inside the 4–6 km/h sanity band and the walk ≤1.5 km / drive ≤10 km caps. **HTTP 429s: none** in any worker or in the coordinator pass. **Roster lines proved wrong on the ground: none** — the roster was never silently corrected; every failure was in geocoder points, each reverse-geocode-verified before substitution and disclosed in-file.

All five sections + NOT CONFIRMED written in every file. Four files (416, 417, 418, 419) carry the brief's §5 fallback bullet — travel times not measured in this pass — because no reproducible reliable origin exists for their addresses (detail below). Word counts are disk `wc -w`; five files run over the ~400-word cap (Silva 402, Chelsea Gardens townhouse section 410, Kingsgate Gardens 421, Element 2 432, Kensington 436 — disclosed per file; wording trimmed only, no cited fact or URL cut; the Element 2 and Kensington overages are driven by the coordinator-correction disclosures below).

## Process disclosures (geocode governance)

- **Worker 2 — irreproducible Nominatim candidates discarded; four §5 fallbacks:** for Crescentview at Edgemont (416), Edgemont Ridge Estates (417), Edgemont Villa (418) and 7333 16th Avenue (419), a first pass returned candidate house points, but three separate reproducible foreground re-runs (limit=1, then limit=10 with every candidate reverse-geocoded, then named-building/abbreviated variants) could not reproduce any origin that reverse-verifies to the roster address — candidates reverse-geocoded to other addresses (3233 Connaught Crescent; 710 Edgemont Boulevard; 7250/7593/7728/7856/8048/8355 16th Avenue) or to no house number. Per the brief the unverifiable origins were discarded and §5 carries the single fallback bullet with the failure disclosed in each file's NOT CONFIRMED. The Summit (414), from the same worker, reverse-verified reproducibly in two independent runs and stands measured. A later mop-up pass with a different geocoder or sourced civic points could recover these four §5s.
- **Worker 4 — delayed duplicate geocode delivery; coordinator re-verification; two §5s re-measured:** a delayed duplicate delivery of Worker 4's first geocode run contradicted the delivery first acted on for Element 2 (425) and Kensington (426), returning segment-only results where the first delivery had shown house-number nodes. The coordinator re-ran both addresses in the foreground (free-form limit=10, structured, and street-geometry reads): **no house-number geocode exists for 7161 17th Avenue or 7184 Stride Avenue** — only street segments. The points the files first used reverse-geocode to buildings on different streets (Element 2's to Cedar Creek 2, 7169 14th Avenue; Kensington's to Byrne Creek Secondary, 7777 18th Street, ~0.5 km south of the roster address — its first-pass "walk to Byrne Creek, 0.30 km" was measured from a point ~35 m from the school itself). Both origins were discarded; the coordinator re-measured both §5s 2026-11-02 from on-street segment points at the correct block (Element 2: 17th Avenue segment point reverse-geocoding to 7138 17th Avenue; Kensington: Stride Avenue segment point reverse-geocoding to 7158 Stride Avenue — same street and block face in each case), keeping each file's original destination set and caps. The corrected figures are what stand on disk; the discard and substitution are disclosed in each file's NOT CONFIRMED. Kings Crossing 1 and 2's named-building points were independently confirmed by the delayed run and stand unchanged; Kingsgate Gardens' segment-point substitution was likewise consistent across both deliveries.
- **Worker 5 — Riverstone origin failed reverse-geocode on the full run; §5 redone by the worker:** Riverstone's (432) first origin point reverse-geocoded to an unrelated 18th Street address when the complete background geocode output arrived; the worker discarded it and re-measured from a Stride Avenue point reverse-geocoding to 7131 Stride Avenue (across-street frontage from roster address 7128), disclosed in-file. Its other four origins were re-checked against the full output and stand (Leeside Creek and Toscana reverse-geocode exactly; Maplewood Terrace and Sylvan Court are disclosed segment substitutions).
- **Silva (409) — segment-point origin:** repeated foreground variants returned only 75A Avenue segment points; the file uses the segment point in the matching postal block, times stated as approximate, disclosed in-file.
- **Edgemont Villa (418) — count-home ambiguity recorded, not resolved:** the roster note (verified in both the edgemont and capilano-nv 55-plus files; edgemont used here) is carried in the file's NOT CONFIRMED. The header identifies the building by name/class only; no age-restriction claims anywhere.
- **7333 16th Avenue (419) — unnamed status stated:** UNNAMED IN NOTES, marketing name UNCONFIRMED, counted by address ("Southgate townhomes" label); the address serves as the building name in title/header, disclosed in-file.
- "Surrey Central" appears in the east-newton files only as **Surrey Central Station**, a route terminus named on TransLink's own timetables; no bus exchange of that name is asserted anywhere. "East Newton Elementary" is not cited anywhere. Edmonds Station is named in the edmonds-be files only from TransLink timetable pages read in this pass.

## Per-building detail

### 409. Silva — 13760 75A Ave (east-newton; condos)
- File: silva--east-newton-nearby-2026-11-02.md — 3,248 B / 402 w (**over cap +2, disclosed**). Origin: 75A Ave segment point in the matching V3W 0H9 postal block (49.1395355, -122.8409845); reverse-geocode returns "75A Avenue" only, so times are approximate. Multi-address: title + anchor use 13760 75A Ave; header carries all three roster addresses; anchor choice disclosed in NOT CONFIRMED.
- Measurements (3 walk, 2 drive): walk Frank Hurt Secondary 0.48 km / 6.4 min; walk Save-On-Foods, 7320 King George Blvd 0.71 / 9.5; walk Newton Exchange 0.85 / 11.3; drive Chalo FreshCo, 7165 138 St 1.06 / 2.0; drive Chimney Hill Elementary 3.22 / 5.3.
- NOT CONFIRMED: multi-address anchor; no house geocode (segment point, approximate); school catchments (no locator run); bus frequencies other than RapidBus not stated.

### 410. Wedgewood Estates — 13880 74 Ave (east-newton; townhomes)
- File: wedgewood-estates--east-newton-nearby-2026-11-02.md — 3,010 B / 358 w. Origin: exact Nominatim house point 13880 74 Ave (49.1370425, -122.8371725), reverse-geocoded exactly.
- Measurements (4 walk, 1 drive): walk Chalo FreshCo 0.71 km / 9.5 min; walk Georges Vanier Elementary 0.75 / 10.0; walk Frank Hurt Secondary 0.84 / 11.2; walk M B Sanford Elementary 1.24 / 17.0; drive Newton Exchange 0.91 / 1.9.
- NOT CONFIRMED: catchments; Georges Vanier destination was a 142 St segment point (walk approximate); frequencies other than RapidBus not stated.

### 411. Chelsea Gardens (townhouse section) — 13888 70 Ave (east-newton-guide; townhomes)
- File: chelsea-gardens--east-newton-guide-nearby-2026-11-02.md — 3,263 B / 410 w (**over cap +10, disclosed**). Origin: exact Nominatim house point 13888 70 Ave (49.1297941, -122.8365387), reverse-geocoded exactly — the same point batch P2-16 measured the complex's condos/55-plus file (entry 406) from. Header carries the full roster wording ("within the Chelsea Gardens community at 13860–13888 70 Ave").
- Measurements (5 walk, 1 drive): walk Surrey Libraries Newton Branch 0.34 km / 4.6 min; walk Chalo FreshCo 0.53 / 7.1; walk Newton Recreation Centre 0.72 / 9.6; walk Newton Exchange 0.73 / 9.7; walk Georges Vanier Elementary 1.46 / 19.4; drive M B Sanford Elementary 1.81 / 3.8.
- NOT CONFIRMED: townhouse-section-only scope; catchments; Vanier segment point (walk approximate); walk to M B Sanford measured 1.60 km, over walk cap — excluded, drive listed; frequencies.

### 412. Chimney Ridge — 7250 144 St (east-newton-guide; townhomes)
- File: chimney-ridge--east-newton-guide-nearby-2026-11-02.md — 3,181 B / 383 w. Origin: exact Nominatim house point 7250 144 St (49.1350783, -122.8230681), reverse-geocoded exactly.
- Measurements (4 walk, 1 drive): walk M B Sanford Elementary 0.18 km / 2.6 min; walk Georges Vanier Elementary 0.76 / 10.1; walk Chimney Heights Park 1.01 / 13.4; walk Chimney Hill Elementary 1.16 / 15.5; drive Newton Exchange 1.64 / 3.0.
- NOT CONFIRMED: catchments; Chimney Heights Park destination was a 74 Ave segment point and Vanier a 142 St segment point (walks approximate); walks to Newton Exchange (1.54 km) and Newton Recreation Centre (1.55 km) over walk cap — excluded, Exchange drive listed; frequencies.

### 413. Newton Park I — 13915–13955 72 Ave (east-newton-guide; townhomes)
- File: newton-park-i--east-newton-guide-nearby-2026-11-02.md — 3,270 B / 400 w (at cap). Origin: exact Nominatim house point for the range anchor 13915 72 Ave (49.1338725, -122.8368925), reverse-geocoded exactly; the range is carried in the header and disclosed in NOT CONFIRMED.
- Measurements (5 walk, 1 drive): walk Chalo FreshCo 0.38 km / 5.1 min; walk Newton Exchange 0.42 / 5.6; walk Newton Recreation Centre 0.43 / 5.7; walk Surrey Libraries Newton Branch 0.60 / 8.0; walk M B Sanford Elementary 1.15 / 15.5; drive Georges Vanier Elementary 1.35 / 3.0.
- NOT CONFIRMED: address-range anchor choice; catchments; Vanier segment point (drive approximate); frequencies.

### 414. The Summit — 14468 73A Ave (east-newton-guide; townhomes)
- File: the-summit--east-newton-guide-nearby-2026-11-02.md — 2,901 B / 370 w. Origin: Nominatim house point (49.1364303, -122.8216452), reverse-geocoded to "14468, 73A Avenue" and verified in two independent runs.
- Measurements (2 walk, 5 drive): walk Chimney Heights Park, 14677 74 Ave 0.62 km / 8.3 min; walk Chimney Hill Elementary, 14755 74 Ave 0.95 / 12.6; drive Chimney Heights Park 0.62 / 1.6; drive Chimney Hill Elementary 0.87 / 2.4; drive Newton Recreation Centre, 13730 72 Ave 2.13 / 3.8; drive Newton Exchange 2.11 / 3.8; drive Shoppers Drug Mart, 7322 King George Blvd 2.33 / 4.4.
- NOT CONFIRMED: SD36 catchment; bus frequencies; walks over the 1.5 km cap measured and dropped (Newton Recreation Centre, Newton Exchange, Shoppers Drug Mart — drives listed).

### 416. Crescentview at Edgemont — 3121 Connaught Crescent (edgemont; condos)
- File: crescentview-at-edgemont--edgemont-nearby-2026-11-02.md — 2,569 B / 280 w. Origin: **none reliable** — candidates reverse-geocoded to Pharmasave, 3233 Connaught Crescent, or to Connaught Crescent with no house number across three reproducible foreground passes. §5 = the brief's fallback bullet.
- Measurements: none.
- NOT CONFIRMED: the travel-time failure; SD44 catchments; bus frequencies.

### 417. Edgemont Ridge Estates — 2425 Edgemont Boulevard (edgemont; townhomes)
- File: edgemont-ridge-estates--edgemont-nearby-2026-11-02.md — 2,475 B / 268 w. Origin: **none reliable** — the only candidate reverse-geocodes to 710 Edgemont Boulevard; named-building query returned no results. §5 = fallback bullet.
- Measurements: none.
- NOT CONFIRMED: the travel-time failure; SD44 catchments; bus frequencies.

### 418. Edgemont Villa — 3151 Connaught Crescent (edgemont; 55-plus + condos)
- File: edgemont-villa--edgemont-nearby-2026-11-02.md — 2,767 B / 312 w. Origin: **none reliable** — same Connaught Crescent candidate failures as 416. §5 = fallback bullet. Header identifies the building by name/class only; no age-restriction claims.
- Measurements: none.
- NOT CONFIRMED: the count-home ambiguity (55-plus program presents the complex as verified in both the edgemont and capilano-nv files; edgemont is the home used here — recorded, not resolved); the travel-time failure; SD44 catchments; bus frequencies.

### 419. 7333 16th Avenue — 7333 16th Avenue (edmonds-be; townhomes)
- File: 7333-16th-avenue--edmonds-be-nearby-2026-11-02.md — 2,612 B / 311 w. Origin: **none reliable** — 10+ candidates all reverse-geocoded to other 16th Avenue addresses or no house number. §5 = fallback bullet.
- Measurements: none.
- NOT CONFIRMED: the unnamed status (UNNAMED IN NOTES; marketing name UNCONFIRMED; counted by address; "Southgate townhomes" label; address used as the building name in title/header); the travel-time failure; PriceSmart Foods Kings Crossing address not confirmed on the retailer's own site (§4 lists Shoppers Drug Mart Highgate Village, 7155 Kingsway #250, from a retailer own-domain search result, disclosed in-file — matching the phase-1 Edmonds treatment); SD41 catchments; bus frequencies.

### 420. Azure 2 at Southgate City — 7769 Park Crescent (edmonds-be; condos)
- File: azure-2-at-southgate-city--edmonds-be-nearby-2026-11-02.md — 2,978 B / 362 w. Origin: Nominatim named-building point "Azure 2", reverse-geocoded exactly to 7769 Park Crescent.
- Measurements (4 walk, 1 drive): walk Byrne Creek Community Secondary 0.58 km / 7.8 min; walk Stride Avenue Community Elementary 0.84 / 11.2; walk Edmonds Station 1.17 / 15.6; walk Taylor Park Elementary 1.38 / 18.3; drive Edmonds Community Centre 1.94 / 4.7.
- NOT CONFIRMED: school catchments (no locator run); bus frequencies; PriceSmart Foods Kings Crossing address not on the retailer's own site; Save-On-Foods Highgate grocery address not on the retailer's own site (only its pharmacy result displayed one).

### 421. Azure at Southgate City — 7683 Park Crescent (edmonds-be; condos)
- File: azure-at-southgate-city--edmonds-be-nearby-2026-11-02.md — 3,143 B / 387 w. Origin: Nominatim named-building point "Azure", reverse-geocoded exactly to 7683 Park Crescent.
- Measurements (4 walk, 1 drive): walk Byrne Creek Community Secondary 0.47 km / 6.3 min; walk Stride Avenue Community Elementary 0.76 / 10.1; walk Edmonds Station 1.09 / 14.5; walk Taylor Park Elementary 1.29 / 17.2; drive Edmonds Community Centre 1.95 / 4.7.
- NOT CONFIRMED: the same four items as 420, plus: other addresses for this building appear in the program home file (a presentation address and a second listing address) — the roster address was used throughout, flagged in-file, not silently corrected.

### 422. Cedar Creek — 7133 14th Avenue (edmonds-be; condos)
- File: cedar-creek--edmonds-be-nearby-2026-11-02.md — 3,187 B / 396 w. Origin: Nominatim named-building point "Cedar Creek 1", reverse-geocoded exactly to 7133 14th Avenue. Multi-address: header carries all four roster addresses exactly (7133 14th Avenue; 7579 / 7588 16th Street; 7599 15th Street); title + anchor use 7133 14th Avenue, disclosed in NOT CONFIRMED.
- Measurements (4 walk, 1 drive): walk Stride Avenue Community Elementary 0.52 km / 7.0 min; walk Byrne Creek Community Secondary 0.70 / 9.3; walk Edmonds Station 0.86 / 11.4; walk Taylor Park Elementary 1.06 / 14.1; drive Edmonds Community Centre 1.36 / 3.1.
- NOT CONFIRMED: multi-address anchor choice (the 16th/15th Street buildings not measured from); catchments; frequencies; both grocery-address items as at 420.

### 423. Eden at Edmonds — 7168 Stride Avenue (edmonds-be; townhomes)
- File: eden-at-edmonds--edmonds-be-nearby-2026-11-02.md — 3,184 B / 390 w. Origin: **segment substitution, disclosed in-file** — no building point for 7168 Stride Avenue (named and postal-code variants tried); a Stride Avenue segment point reverse-geocoding to 7159 Stride Avenue (same street, 9 civic numbers away) was used.
- Measurements (4 walk, 1 drive): walk Stride Avenue Community Elementary 0.48 km / 6.3 min; walk Edmonds Station 0.78 / 10.4; walk Byrne Creek Community Secondary 0.87 / 11.6; walk Taylor Park Elementary 1.01 / 13.5; drive Edmonds Community Centre 1.20 / 2.9.
- NOT CONFIRMED: measurement-origin substitution; catchments; frequencies; both grocery-address items as at 420.

### 424. Element 1 — 7131 17th Avenue (edmonds-be; townhomes)
- File: element-1--edmonds-be-nearby-2026-11-02.md — 3,165 B / 386 w. Origin: **neighbouring-address substitution, disclosed in-file** — no building point for 7131 17th Avenue (named, postal and structured variants tried; one 17th Avenue segment point reverse-geocoding to 7252 17th Avenue was discarded); the verified 7128 17th Avenue point (3 civic numbers away, same street) was used.
- Measurements (4 walk, 1 drive): walk Edmonds Station 0.55 km / 7.3 min; walk Stride Avenue Community Elementary 0.55 / 7.3; walk Byrne Creek Community Secondary 0.94 / 12.6; walk Taylor Park Elementary 1.08 / 14.3; drive Edmonds Community Centre 1.12 / 2.6.
- NOT CONFIRMED: measurement-origin substitution; catchments; frequencies; both grocery-address items as at 420.

### 425. Element 2 — 7161 17th Avenue (edmonds-be; townhomes)
- File: element-2--edmonds-be-nearby-2026-11-02.md — 3,521 B / 432 w (**over cap +32, disclosed** — driven by the correction disclosure). Origin: **coordinator-corrected** — no house-number geocode exists for 7161 17th Avenue; the first-pass origin reverse-geocodes to Cedar Creek 2, 7169 14th Avenue (different street) and was discarded on coordinator re-verification. §5 re-measured 2026-11-02 from a 17th Avenue segment point at the 7161 block (49.2143, -122.9534), reverse-geocoding to 7138 17th Avenue — same street and block face; times approximate, disclosed in-file.
- Measurements (4 walk, 2 drive): walk Edmonds Station 0.61 km / 8.2 min; walk Stride Avenue Community Elementary 0.61 / 8.2; walk Byrne Creek Community Secondary 0.86 / 11.5; walk Taylor Park 1.32 / 17.6; drive PriceSmart Foods, Kings Crossing 0.79 / 1.9; drive Edmonds Community Centre 1.05 / 2.5.
- NOT CONFIRMED: the "(Square Nine Developments)" qualifier, dropped from title/header per the brief and not itself confirmed in this pass; the origin correction as above; school catchments; bus frequencies.

### 426. Kensington — 7184 Stride Avenue (edmonds-be; townhomes)
- File: kensington--edmonds-be-nearby-2026-11-02.md — 3,569 B / 436 w (**over cap +36, disclosed** — driven by the correction disclosure). Origin: **coordinator-corrected** — no house-number geocode exists for 7184 Stride Avenue; the first-pass origin reverse-geocodes to Byrne Creek Secondary, 7777 18th Street (~0.5 km south) and was discarded on coordinator re-verification. §5 re-measured 2026-11-02 from a Stride Avenue segment point at the 7184 block (49.2136, -122.9514), reverse-geocoding to 7158 Stride Avenue — same street and block face; times approximate, disclosed in-file.
- Measurements (4 walk, 2 drive): walk Stride Avenue Community Elementary 0.52 km / 7.0 min; walk Byrne Creek Community Secondary 0.77 / 10.3; walk Taylor Park Elementary 1.06 / 14.1; walk Taylor Park 1.24 / 16.5; drive Edmonds Station 0.90 / 2.5; drive Edmonds Community Centre 1.16 / 2.7.
- NOT CONFIRMED: the origin correction as above; school catchments; bus frequencies; both confirmed grocery anchors are beyond the roughly 1 km radius and no closer grocery address was confirmed from a retailer page in this pass.

### 427. Kings Crossing 1 — 7388 Kingsway (edmonds-be; condos)
- File: kings-crossing-1--edmonds-be-nearby-2026-11-02.md — 3,045 B / 352 w. Origin: Nominatim named-building point "Kings Crossing One", 7388 Kingsway (49.2185996, -122.9495587); reverse-geocode confirms name and address; independently confirmed by the delayed duplicate geocode run.
- Measurements (4 walk, 1 drive): walk PriceSmart Foods, Kings Crossing 0.23 km / 3.1 min; walk Tommy Douglas Library 0.23 / 3.1; walk Edmonds Park 0.47 / 6.2; walk Edmonds Community Centre 0.47 / 6.3; drive Edmonds Station 1.20 / 2.3.
- NOT CONFIRMED: school catchments; bus frequencies; a first Nominatim result at 7155 Kingsway was discarded and the named-building point used instead (disclosed in-file).

### 428. Kings Crossing 2 — 7358 Edmonds Street (edmonds-be; condos)
- File: kings-crossing-2--edmonds-be-nearby-2026-11-02.md — 2,997 B / 347 w. Origin: Nominatim named-building point "Kings Crossing Two", 7358 Edmonds Street (49.2189135, -122.9500466); reverse-geocode confirms name and address; independently confirmed by the delayed duplicate geocode run.
- Measurements (3 walk, 1 drive): walk PriceSmart Foods, Kings Crossing 0.03 km / 0.4 min; walk Tommy Douglas Library 0.22 / 2.9; walk Edmonds Community Centre 0.38 / 5.1; drive Edmonds Station 1.15 / 2.2.
- NOT CONFIRMED: the "(King Crossing Tower 2)" alias, dropped from title/header per the brief and not itself confirmed in this pass; school catchments; bus frequencies.

### 429. Kingsgate Gardens — 7428 14th Avenue (edmonds-be; townhomes)
- File: kingsgate-gardens--edmonds-be-nearby-2026-11-02.md — 3,531 B / 421 w (**over cap +21, disclosed**). Origin: 14th Avenue street-segment point in the 7400 block (reverse-geocodes to 7299 14th Avenue); Nominatim has no exact point for 7428 14th Avenue and no point for the building name — disclosed in-file; the roster address stands as written.
- Measurements (3 walk, 3 drive): walk St. Thomas More Collegiate 0.79 km / 10.6 min; walk Edmonds Community Elementary 1.24 / 16.6; walk Twelfth Avenue Elementary 1.24 / 16.6; drive Edmonds Station 1.38 / 2.4; drive Edmonds Community Centre 1.34 / 2.8; drive Byrne Creek Community Secondary 1.38 / 3.2.
- NOT CONFIRMED: the segment-point origin as above; school catchments; bus frequencies; both confirmed grocery anchors are beyond the roughly 1 km radius and no closer grocery address was confirmed from a retailer page in this pass.

### 430. Leeside Creek — 7128 17th Avenue (edmonds-be; townhomes)
- File: leeside-creek--edmonds-be-nearby-2026-11-02.md — 3,063 B / 359 w. Origin: Nominatim building point for 7128 17th Avenue, reverse-geocoded exactly to the roster address (re-checked against the worker's full geocode run output).
- Measurements (3 walk, 1 drive): walk Edmonds Station 0.55 km / 7.3 min; walk Stride Avenue Community Elementary 0.55 / 7.3; walk Edmonds Community Centre 1.21 / 16.1; drive Byrne Creek Community Secondary 1.62 / 4.1.
- NOT CONFIRMED: school catchments; bus frequencies; grocery items per the worker's report.

### 431. Maplewood Terrace — 7370 Stride Avenue (edmonds-be; townhomes)
- File: maplewood-terrace--edmonds-be-nearby-2026-11-02.md — 3,311 B / 392 w. Origin: **segment substitution, disclosed in-file** — no Nominatim building point for 7370 Stride Avenue; a Stride Avenue segment point was used.
- Measurements (4 walk, 1 drive): walk Edmonds Community Centre 0.82 km / 11.0 min; walk Edmonds Community Elementary 0.98 / 13.1; walk Twelfth Avenue Elementary 1.16 / 15.4; walk Edmonds Station 1.41 / 18.8; drive Byrne Creek Community Secondary 1.94 / 3.8.
- NOT CONFIRMED: the segment-point origin; school catchments; bus frequencies.

### 432. Riverstone — 7128 Stride Avenue (edmonds-be; townhomes)
- File: riverstone--edmonds-be-nearby-2026-11-02.md — 3,240 B / 384 w. Origin: **substitution, disclosed in-file, after a discarded first origin** — the worker's first point reverse-geocoded to an unrelated 18th Street address when the complete geocode output arrived and was discarded; §5 was re-measured from a Stride Avenue point reverse-geocoding to 7131 Stride Avenue, the across-street frontage from roster address 7128. No Nominatim building point for 7128 Stride Avenue exists.
- Measurements (4 walk, 1 drive): walk Stride Avenue Community Elementary 0.37 km / 5.0 min; walk Edmonds Station 0.70 / 9.4; walk Byrne Creek Community Secondary 0.76 / 10.2; walk Taylor Park Elementary 0.91 / 12.1; drive Edmonds Station 0.76 / 2.2.
- NOT CONFIRMED: the "(Adera)" qualifier, dropped from title/header per the brief and noted in-file; the origin substitution as above; school catchments; bus frequencies; PriceSmart Foods source item per the worker's report.

### 433. Sylvan Court — 7188 Edmonds Street (edmonds-be; townhomes)
- File: sylvan-court--edmonds-be-nearby-2026-11-02.md — 3,313 B / 392 w. Origin: **segment substitution, disclosed in-file** — no Nominatim building point for 7188 Edmonds Street; an Edmonds Street segment point was used.
- Measurements (3 walk, 1 drive): walk Edmonds Station 0.77 km / 10.3 min; walk Edmonds Community Centre 0.81 / 10.7; walk Stride Avenue Community Elementary 0.98 / 13.1; drive Edmonds Community Centre 0.71 / 1.5.
- NOT CONFIRMED: the segment-point origin; school catchments; bus frequencies.

### 434. Toscana — 7738 Edmonds Street (edmonds-be; condos)
- File: toscana--edmonds-be-nearby-2026-11-02.md — 3,255 B / 381 w. Origin: Nominatim building point for 7738 Edmonds Street, reverse-geocoded exactly to the roster address (re-checked against the worker's full geocode run output).
- Measurements (3 walk, 1 drive): walk Edmonds Community Elementary 0.62 km / 8.3 min; walk Edmonds Community Centre 0.82 / 11.0; walk Twelfth Avenue Elementary 1.34 / 17.8; drive Edmonds Station 2.22 / 4.2.
- NOT CONFIRMED: school catchments; bus frequencies; grocery items per the worker's report.
