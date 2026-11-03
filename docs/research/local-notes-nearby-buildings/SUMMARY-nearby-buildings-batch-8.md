# What's Nearby — Phase 2, Batch P2-8 Summary

Produced 2026-11-02 under PHASE2-BRIEF.md. Roster range covered: **entries 180–207 — 25 buildings produced.** Skipped: **entry 188, Natura (central-abbotsford; condos) — ADDRESS NOT IN NOTES** (exact civic address UNCONFIRMED in home file; off Gladwin Road, behind Regency Park); **entry 193, Upper Montrose (central-abbotsford; condos) — ADDRESS NOT IN NOTES** (street address UNCONFIRMED in home file, Historic Downtown only); **entry 195, The Abby Townhome Series at The Rail District (central-abbotsford-guide; townhomes) — ADDRESS NOT IN NOTES** (no single civic address in notes). All three held for the final mop-up batch; their addresses were not researched. Extension to entry 207 was needed to reach 25 addressed buildings. **Mop-up list to date: entries 52 (The Hart), 85 (District Flats at Southlands), 86 (The Granary at Southlands), 156 (Winona Park), 188 (Natura), 193 (Upper Montrose), 195 (The Abby Townhome Series).**

Areas: central-abbotsford 13, central-abbotsford-guide 1, central-bn 5, central-coquitlam 6. All five sections + NOT CONFIRMED written in every file **except 3058 Smith Avenue, whose §5 is the brief's single-bullet fallback** ("Travel times: not measured in this pass") because no reliable geocode origin exists for its address — disclosed in-file. No other section omitted anywhere.

**Measurements: 129 kept (68 walk, 61 drive)**, all measured 2026-11-02 starting at each building's own address; every kept walk inside the 4–6 km/h sanity band and the walk ≤1.5 km / drive ≤10 km caps. **11 routes were measured but not kept**, all stated or disclosed in-file: 9 over the walk cap (Regency Park 2, Summerset Place 1, Willband Creek Estates 1, Canterbury Gate 1, Oakhurst Park 1, Norfolk Terrace 1, Hideaway Park 2) — plus the Georgian Park walk to Horn Creek Park (0.66 km / 4.6 min = 8.6 km/h), discarded on the speed-sanity rule after a re-check, and one further route set replaced wholesale by the corrected re-measurements described below. **HTTP 429s: none** across all five workers (Nominatim, OSRM driving, routed-foot).

**Roster lines proved wrong on the ground: none** — the roster was never silently corrected. Every error this batch was in first-pass geocode points, not in roster addresses, and each is disclosed in the affected file.

**Process incidents — the backgrounded-geocode failure mode hit four of the five workers this batch; in every case the foreground re-run governed, all measurements were re-taken from the governed points, and the files were rewritten before delivery, with the discrepancy disclosed in each file's NOT CONFIRMED:**
1. Worker A (entries 180–184): its first geocode script backgrounded unexpectedly and returned points disagreeing with foreground re-runs for every building (worst: College Park ~1.8 km west; Cloud Croft Manor ~700 m south, off the street line). Foreground points govern throughout; disclosed per file.
2. Worker B (entries 185–190): the delayed background delivery disagreed with its first measurement set. Foreground re-runs govern: Mayfair Place's first origin was ~2.3 km wrong (the building is in the Bevan Ave / Mill Lake cluster — four anchors are in fact within a 1 km walk); Parkside Place's first point sat essentially on Clearbrook Library ~1.1 km away — its §§2–3 were re-scoped to the corrected Murray Avenue segment origin and the first report's "walk to Clearbrook Library 0.06 km" figure is withdrawn and appears nowhere in the delivered file. Oakhurst Park and Parkside Place have NO exact house point in Nominatim (foreground-confirmed, incl. layer=address and postal-code variants); disclosed segment-point origins were used.
3. Worker C (entries 191–197): the first geocode output delivered into its session disagreed with both the actual backgrounded session output and foreground re-runs; the first set was discarded entirely. Foreground findings: 3150 Gladwin Road has an exact building point (~250 m from the discarded point); 2456 Ware St / 33020 Maclure Rd / 32659 George Ferguson Way return only unstable street-segment points on civic-address queries (one Maclure point landed at -122.446, in Langley), so building-name queries returning residential points whose Nominatim address details carry the exact roster house numbers were used as origins, disclosed in-file. **3058 Smith Avenue has NO reliable origin** — repeated foreground variants returned only Smith Avenue segment points scattering >1 km — so its §5 is "Travel times: not measured in this pass" with the failure disclosed; the 4 Smith measurements in the worker's first report are withdrawn. Bourquin Exchange geocodes in Nominatim as a bus_station point and was used as such.
4. Worker E (entries 203–207): its first in-conversation geocode delivery proved to be a contaminated point set (it placed the Grand Central complex and Burlington Estates east of Pinetree Way); the real backgrounded output and the foreground re-run agreed with each other and govern — the complex sits west of Pinetree Way (Harbour Village / Hoy Creek side), confirmed by named building points and calibrated against Oasis at 2955 Atlantic Avenue. All 41 routes re-measured, all 5 files rewritten. Its Hideaway Park origin (OSM house node for 4200 Dewdney Trunk Road, Cassin side) is the toolchain's consistent answer across both runs and governs; it sits NW of the Ranch Park anchors the program home file describes, flagged in-file and here for the record — the roster line was not corrected.
5. Worker D (entries 198–202) is the exception: when its backgrounded delivery arrived, it agreed with the foreground points actually used for all four Burnaby buildings, and for Altamonte the River Springs segment point used appears identically in both runs (only unused Harbour Village candidates differed). No re-measurement or rewrite was required; the comparison is recorded here and in its files as reported.
This coordinator spot-checked the corrected Parkside Place file in full on disk; the corrected figures and disclosures are what the file carries. All 25 worker-reported byte sizes and word counts were re-verified against disk by the coordinator — every one matches the corrected reports exactly.

**Word-cap overages (disclosed; wording trimmed only, no cited fact or URL cut):** Parkside Place 608 (+208), Mayfair Place 589 (+189), Oakhurst Park 561 (+161), Montvue 540 (+140), The Mason at The Rail District 498 (+98), Willband Creek Estates 430 (+30), Summerset Place 426 (+26), Burlington Estates 413 (+13), Regency Park 402 (+2). The Abbotsford overages are driven by 6–9 measurements per file plus the required geocode-discrepancy and segment-origin disclosures. All other files 282–392 words.

---

## Per-building detail

### 180. Cloud Croft Manor — 33464 George Ferguson Way (central-abbotsford; 55-plus)
- File: cloud-croft-manor--central-abbotsford-nearby-2026-11-02.md — 3,568 B; 387 words — within cap
- Origin: George Ferguson Way segment point (49.0501, -122.2885) — Nominatim returned no house point in foreground runs. Backgrounded run had returned 49.0438, -122.2870 (~700 m south, off the street line); foreground governs, disclosed in-file
- Measurements (4): drive Bourquin Exchange 2.06 km / 4.0 min; drive Clearbrook Library 3.69 / 7.4; walk Abbotsford Senior Secondary 1.37 / 18.3 (4.5 km/h); walk Babich Park 1.20 / 16.0 (4.5 km/h)
- NOT CONFIRMED: segment-point origin + background discrepancy; school catchments (no locator run); nearest bus stop and frequencies; no grocery within ~1 km confirmed (anchors listed are the central centres west)

### 181. College Park — 33728 King Road (central-abbotsford; condos)
- File: college-park--central-abbotsford-nearby-2026-11-02.md — 2,624 B; 324 words — within cap
- Origin: exact house point (Nominatim "apartments", 49.0306, -122.2895). Backgrounded run returned a King Road segment point at -122.3113 (~1.8 km west) — foreground governs, disclosed in-file
- Measurements (3): walk University of the Fraser Valley 0.86 km / 11.4 min; walk Berry Park 1.26 / 16.9; drive Bourquin Exchange 3.49 / 6.5
- NOT CONFIRMED: background-geocode discrepancy; no SD34 school within ~1 km confirmed (Ministry list checked; Yale Secondary and King Traditional Elementary both geocode well beyond 1 km); catchments; nearest stop/frequencies; no grocery within ~1 km (nearest confirmed: Save-On-Foods, 2140 Sumas Way, via retailer's own-domain search result, disclosed in-file)

### 182. Georgian Park — 3300 Horn St (central-abbotsford; 55-plus)
- File: georgian-park--central-abbotsford-nearby-2026-11-02.md — 2,819 B; 346 words — within cap
- Origin: named point — Nominatim caravan_site "Georgian Park, 3300 Horn Street" (49.0619, -122.3058). Backgrounded run returned a Horn St segment point (49.0525, -122.2966); foreground governs, disclosed in-file. Header class only: manufactured-home park, per the roster
- Measurements (2): drive Real Canadian Superstore (2855 Gladwin Rd) 1.64 km / 3.5 min; drive Bourquin Exchange 1.71 / 2.9
- Discarded: walk Horn Creek Park 0.66 km / 4.6 min = 8.6 km/h, outside the 4–6 km/h sanity range — re-run once, same result, discarded and stated in-file
- NOT CONFIRMED: background-geocode discrepancy; no SD34 school within ~1 km confirmed; catchments; nearest stop/frequencies; Horn Creek Park street address not stated on the Tourism Abbotsford listing read

### 183. Horizon Place — 33233 Bourquin Cres (central-abbotsford; 55-plus)
- File: horizon-place--central-abbotsford-nearby-2026-11-02.md — 3,294 B; 350 words — within cap
- Origin: named point — Nominatim "apartments / Horizon Place, Bourquin Crescent East" (49.0471, -122.3037). Backgrounded run returned 49.0501, -122.3010; foreground governs, disclosed in-file
- Measurements (4): walk Bourquin Exchange 0.45 km / 6.1 min; walk Sevenoaks Shopping Centre 0.80 / 10.8; walk Mill Lake Park 0.86 / 11.2; drive Clearbrook Library 2.71 / 5.3
- NOT CONFIRMED: background-geocode discrepancy; school catchments (no locator run); bus frequencies

### 184. Mahogany at Mill Lake — 2180 Gladwin Road (central-abbotsford; condos)
- File: mahogany-at-mill-lake--central-abbotsford-nearby-2026-11-02.md — 3,079 B; 338 words — within cap
- Origin: exact house point (Nominatim "apartments", 49.0415, -122.3150). Backgrounded run returned a point ~185 m north (49.0432, -122.3144); foreground governs, disclosed in-file
- Measurements (4): walk Mill Lake Park 0.69 km / 8.8 min; walk Godson Elementary 0.97 / 12.9; walk Abbotsford Middle School 1.16 / 15.5; drive Sevenoaks Shopping Centre 2.22 / 4.5
- NOT CONFIRMED: background-geocode discrepancy; school catchments (no locator run); nearest stop/frequencies

### 185. The Mason at The Rail District — 2771 Montrose Avenue (central-abbotsford; condos)
- File: the-mason-at-the-rail-district--central-abbotsford-nearby-2026-11-02.md — 4,136 B; 498 words — OVER cap (disclosed)
- Origin: exact house point (49.0526909, -122.2918790) — foreground re-run, agreeing with the background delivery; the first draft set had used a point ~130 m off, disclosed in-file
- Measurements (6): walk Montrose Exchange 0.80 km / 10.7 min; drive Montrose Exchange 0.77 / 2.2; drive Bourquin Exchange 2.14 / 4.2; drive Berry Park 2.26 / 4.9; drive Mill Lake Park 2.54 / 5.5; drive Sevenoaks 2.82 / 5.9
- NOT CONFIRMED: catchments; bus frequencies; origin discrepancy disclosed

### 186. Mayfair Place — 33375 Mayfair Ave (central-abbotsford; 55-plus)
- File: mayfair-place--central-abbotsford-nearby-2026-11-02.md — 4,573 B; 589 words — OVER cap (disclosed)
- Origin: named building point "Mayfair Place" (49.0405641, -122.2995593) — foreground re-run. The first draft set used 49.0574, -122.2815, ~2.3 km away and wrong; the building is in the Bevan Ave / Mill Lake cluster. The earlier "no school within ~1 km" note is withdrawn — four anchors are within a 1 km walk
- Measurements (9): walk Abbotsford Middle 0.56 km / 7.4 min; walk Abbotsford Community Library 0.57 / 7.6; walk Abbotsford Senior Secondary 0.62 / 8.3; walk Godson Elementary 0.74 / 9.9; drive Bourquin Exchange 1.48 / 3.0; drive Berry Park 1.47 / 3.6; drive Mill Lake Park 1.88 / 4.3; drive No Frills 2.08 / 4.7; drive Sevenoaks 1.98 / 4.8
- NOT CONFIRMED: catchments; bus frequencies; which exchange (Bourquin vs Montrose) is nearer — not confirmed in the corrected set; origin discrepancy disclosed

### 187. Montvue — 33820 South Fraser Way (central-abbotsford; condos)
- File: montvue--central-abbotsford-nearby-2026-11-02.md — 4,267 B; 540 words — OVER cap (disclosed)
- Origin: exact building point (49.0459550, -122.2884210) — foreground re-run; first draft used a point ~520 m off, disclosed in-file. Montrose Exchange is in fact ~0.25 km away
- Measurements (8): walk Montrose Exchange 0.24 km / 3.2 min; drive Montrose Exchange 0.26 / 0.5; drive Abbotsford Senior Secondary 0.96 / 2.4; drive Berry Park 1.29 / 2.6; drive No Frills 1.62 / 3.3; walk Berry Park 1.45 / 19.4 (within the 1.5 km walk cap in the corrected set — the earlier over-cap exclusion was an artifact of the wrong origin); drive Mill Lake Park 2.43 / 4.8; drive Sevenoaks 2.71 / 5.2
- NOT CONFIRMED: catchments; bus frequencies; origin discrepancy disclosed

### 189. Oakhurst Park — 32959 George Ferguson Way (central-abbotsford; 55-plus + townhomes)
- File: oakhurst-park--central-abbotsford-nearby-2026-11-02.md — 4,567 B; 561 words — OVER cap (disclosed)
- Origin: George Ferguson Way SEGMENT point (49.0548328, -122.3210867) — NO exact house point exists in Nominatim (foreground-confirmed incl. layer=address and postal-code variants); disclosed in-file
- Measurements (7): walk West Oaks Mall 0.74 km / 10.0 min; walk Clearbrook Town Square 0.75 / 10.2; walk Clearbrook Library 0.78 / 10.6; walk Sevenoaks 1.35 / 18.1; drive Centennial Park Elementary 1.29 / 2.4; drive Bourquin Exchange 1.54 / 2.5; drive Sevenoaks 1.41 / 2.8
- Over-cap excluded (stated in-file): walk to Bourquin Exchange 1.63 km — over the 1.5 km walk cap
- NOT CONFIRMED: catchments; bus frequencies; segment-point origin + discrepancy disclosed

### 190. Parkside Place — 32640 Murray Ave (central-abbotsford; 55-plus)
- File: parkside-place--central-abbotsford-nearby-2026-11-02.md — 4,801 B; 608 words — OVER cap (disclosed; largest in batch — 8 measurements + two origin disclosures + the roster home-area note)
- Origin: Murray Avenue SEGMENT point (49.0461935, -122.3202446) — no house point returned. The first draft point (49.0536, -122.3286) sat essentially on Clearbrook Library ~1.1 km away and was wrong; §§2–3 were re-scoped to the corrected origin (Centennial Park Elementary / Mill Lake Park area; Exhibition Park and Dormick Park Elementary dropped) and the first report's "walk to Clearbrook Library 0.06 km" figure is withdrawn. Spot-checked in full by the coordinator — the delivered file carries the corrected set
- Measurements (8): walk Centennial Park Elementary 0.53 km / 7.0 min; walk West Oaks Mall 0.72 / 9.6; walk Clearbrook Town Square 1.05 / 14.0; walk Mill Lake Park 1.07 / 14.1; drive Centennial Park Elementary 0.53 / 1.4; drive Sevenoaks 0.96 / 2.3; drive Bourquin Exchange 1.54 / 2.8; drive Clearbrook Library 2.15 / 4.6
- NOT CONFIRMED: catchments; bus frequencies; roster home-area note (Central vs Abbotsford West feeds — roster placement used, not corrected); segment-point origin + wrong earlier point disclosed

### 191. Regency Park — 3150 Gladwin Road and 3170 Gladwin Road (central-abbotsford; 55-plus + condos) — MULTI-ADDRESS
- File: regency-park--central-abbotsford-nearby-2026-11-02.md — 3,427 B; 402 words — marginally OVER cap (+2, driven by the required discrepancy disclosure)
- Title/anchor use the FIRST address (3150 Gladwin Road); header carries both addresses exactly as roster states; anchor choice disclosed in NOT CONFIRMED
- Origin: exact house point, 3150 Gladwin Road (49.0588948, -122.3149635; Nominatim building point, house number confirmed) — differs ~250 m from the discarded first geocode set, disclosed in-file
- Measurements (3, all drive): Bourquin Exchange 1.52 km / 2.6 min; Sevenoaks 1.33 / 2.8; Ten Broeck Elementary 3.34 / 6.0
- Over-cap measured but excluded (stated in-file): walk Mill Lake Park 2.36 km / 31.6 min; walk Clearbrook Library 1.60 / 21.5
- NOT CONFIRMED: anchor choice; geocode discrepancy; catchments (no locator run); bus frequencies

### 192. Summerset Place — 2456 Ware Street (central-abbotsford; 55-plus + townhomes)
- File: summerset-place--central-abbotsford-nearby-2026-11-02.md — 3,685 B; 426 words — OVER cap (disclosed; discrepancy + geocode-method disclosures)
- Origin: named point — Nominatim "Summerset Place" residential point whose address details carry house number 2456 (49.0465765, -122.3037704). Civic-address query returns only Ware Street segment points; disclosed in-file
- Measurements (4): walk Mill Lake Park 0.85 km / 11.1 min; drive Bourquin Exchange 0.42 / 0.8; drive Sevenoaks 0.98 / 2.8; drive Dormick Park Elementary 3.61 / 6.7
- Over-cap excluded (in-file): walk Clearbrook Library 2.40 km / 32.1 min
- NOT CONFIRMED: geocode discrepancy + segment-point method note; catchments; frequencies; Ware Street nearest-stop route assignment

### 194. Willband Creek Estates — 33020 Maclure Road (central-abbotsford; 55-plus + townhomes)
- File: willband-creek-estates--central-abbotsford-nearby-2026-11-02.md — 3,677 B; 430 words — OVER cap (disclosed; disclosures)
- Origin: named point — Nominatim "Willband Creek Estates" residential point whose address details carry house number 33020 (49.0603076, -122.3106027). Civic-address query returns only Maclure Road segment points (one landed at -122.446, in Langley); disclosed in-file
- Measurements (4, all drive): Bourquin Exchange 1.77 km / 2.9 min; Sevenoaks 2.26 / 4.3; Abbotsford Middle School 2.65 / 4.6; Willband Creek Park 2.83 / 4.0
- Over-cap excluded (in-file): walk Willband Creek Park 4.21 km / 56.1 min
- NOT CONFIRMED: geocode discrepancy + method note; catchments + no school within ~1 km confirmed; frequencies; Willband Creek Park street address not on municipal page

### 196. Canterbury Gate — 32659 George Ferguson Way (central-abbotsford-guide; townhomes)
- File: canterbury-gate--central-abbotsford-guide-nearby-2026-11-02.md — 3,553 B; 392 words — within cap
- Origin: named point — Nominatim "Canterbury Gate" residential point whose address details carry house number 32659 (49.0553607, -122.3198447). Civic-address query returns only George Ferguson Way segment points; disclosed in-file
- Measurements (3): walk Clearbrook Library 0.89 km / 12.0 min; drive Sevenoaks 1.25 / 2.6; drive Bourquin Exchange 1.44 / 2.4
- Over-cap excluded (in-file): walk Mill Lake Park 2.28 km / 30.4 min. (The 0.09 km library walk in the worker's first report is withdrawn — an artefact of the discarded points)
- NOT CONFIRMED: geocode discrepancy + method note; catchments; frequencies

### 197. 3058 Smith Avenue — 3058 Smith Avenue (central-bn; townhomes)
- File: 3058-smith-avenue--central-bn-nearby-2026-11-02.md — 2,680 B; 342 words — within cap
- Origin: NONE — no reliable geocode obtainable: repeated foreground variants returned only Smith Avenue segment points scattering >1 km. Title/header use the roster name = address (the complex is unnamed in notes)
- Measurements: **none** — §5 is the brief's single bullet "Travel times: not measured in this pass," with the failure disclosed in-file. (The 4 Smith measurements in the worker's first report are withdrawn)
- NOT CONFIRMED: origin geocode failure (full disclosure in-file); catchments; frequencies; no grocery within ~1 km sourced (Metropolis at Metrotown is the sourced anchor); Bob Prittie branch street address; complex unnamed in notes

### 198. Norfolk Terrace — 4025 Norfolk Street (central-bn; townhomes)
- File: norfolk-terrace--central-bn-nearby-2026-11-02.md — 2,401 B; 318 words — within cap
- Origin: Norfolk Street segment point (eastern segment) — Nominatim returned no house point; disclosed in-file. (Detail extracted from the delivered file by the coordinator; the worker's follow-up comparison confirmed its backgrounded delivery agreed with the foreground points used — no discrepancy in any used origin)
- Measurements (3): walk Broadview Park 0.21 km / 2.8 min; drive Moscrop Secondary 2.24 / 4.2; drive Save-On-Foods, Madison Centre 2.04 / 3.6
- Over-cap excluded (stated in-file): walk to Cascade Heights Elementary 1.66 km / 22.1 min — over the 1.5 km walk cap
- NOT CONFIRMED: segment-point origin; school catchments (no locator run); bus frequencies; no recreation centre or library within ~1 km sourced

### 199. Parkside Greene — 3888 Norfolk Street (central-bn; townhomes)
- File: parkside-greene--central-bn-nearby-2026-11-02.md — 2,179 B; 282 words — within cap
- Origin: exact house point (Nominatim)
- Measurements (4): walk Broadview Park 0.26 km / 3.5 min; walk Cascade Heights Elementary 1.32 / 17.6; drive Moscrop Secondary 2.70 / 5.1; drive Save-On-Foods, Madison Centre 2.79 / 4.8
- NOT CONFIRMED: school catchments (no locator run); bus frequencies; no recreation centre or library within ~1 km sourced

### 200. Smith + Norfolk — 3868 Norfolk Street (central-bn; townhomes)
- File: smith-norfolk--central-bn-nearby-2026-11-02.md — 2,378 B; 316 words — within cap
- Origin: Norfolk Street segment point (just west of 3888 Norfolk Street) — no house point returned; disclosed in-file
- Measurements (4): walk Broadview Park 0.31 km / 4.1 min; walk Cascade Heights Elementary 1.25 / 16.7; drive Moscrop Secondary 2.65 / 4.9; drive Save-On-Foods, Madison Centre 2.73 / 4.7
- NOT CONFIRMED: segment-point origin; school catchments (no locator run); bus frequencies; no recreation centre or library within ~1 km sourced

### 201. Winchelsea — 3738 Norfolk Street and 3733 Norfolk Street (central-bn; condos) — MULTI-ADDRESS
- File: winchelsea--central-bn-nearby-2026-11-02.md — 2,414 B; 319 words — within cap
- Title/anchor use the FIRST address (3738 Norfolk Street); header carries both addresses exactly as roster states; anchor choice disclosed in NOT CONFIRMED
- Origin: exact house point (Nominatim) for 3738 Norfolk Street
- Measurements (4): walk Broadview Park 0.67 km / 8.9 min; walk Cascade Heights Elementary 1.23 / 16.5; drive Moscrop Secondary 2.79 / 5.2; drive Save-On-Foods, Madison Centre 2.55 / 4.7
- NOT CONFIRMED: anchor choice; school catchments (no locator run); bus frequencies; no recreation centre or library within ~1 km sourced

### 202. Altamonte — 2979 Glen Drive (central-coquitlam; condos)
- File: altamonte--central-coquitlam-nearby-2026-11-02.md — 2,678 B; 330 words — within cap
- Origin: Glen Drive segment point (River Springs segment, 49.2826766, -122.7916244) — Nominatim returned no house point. The point appears identically in the worker's backgrounded delivery and foreground re-run; only the unused Harbour Village segment candidates differed between runs
- Measurements (6): walk Coquitlam Public Library, City Centre Branch 0.26 km / 3.4 min; walk Glen Elementary 0.31 / 4.1; walk Glen Park 0.32 / 4.3; walk Lincoln Station 0.49 / 6.5; walk Coquitlam Centre 0.92 / 12.3; drive Save-On-Foods, Pinetree Village 0.90 / 1.7
- NOT CONFIRMED: segment-point origin; school catchments (no locator run); bus frequencies

### 203. Burlington Estates — 2963 Burlington Drive and 2973 Burlington Drive (central-coquitlam; 55-plus) — MULTI-ADDRESS
- File: burlington-estates--central-coquitlam-nearby-2026-11-02.md — 3,495 B; 413 words — OVER cap (+13; all cited facts and measurements kept per brief, overage disclosed)
- Title/anchor use the FIRST address (2963 Burlington Drive); header carries both addresses exactly as roster states; anchor choice disclosed in NOT CONFIRMED
- Origin: building point, exact 2963 Burlington Drive (49.2847041, -122.7970966) — governed foreground re-run. NAME TRAP held: The Burlington at 2968/2978 Burlington Drive across the street is a different building and is NOT 55-plus; no facts from it were used
- Measurements (9): walk Lafarge Lake–Douglas Station 0.55 km / 7.4 min; walk Lincoln 0.78 / 10.4; walk Glen Elementary 0.86 / 11.5; walk Library City Centre 0.62 / 8.3; walk City Centre Aquatic Complex 0.54 / 7.3; walk Town Centre Park 1.27 / 16.1; walk Pinetree Secondary 1.23 / 16.4; walk Coquitlam Centre 0.70 / 9.3; drive Coquitlam Central Station 1.70 / 3.7
- NOT CONFIRMED: geocode discrepancy (foreground governs); anchor choice; The Burlington distinction; catchments; frequencies not stated

### 204. Grand Central 2 — 2968 Glen Drive (central-coquitlam; condos)
- File: grand-central-2--central-coquitlam-nearby-2026-11-02.md — 3,221 B; 372 words — within cap
- Origin: named building point (OSM labels it "2970A Glen Drive", 49.2824330, -122.7975550) — governed foreground re-run; roster address kept as stated, the OSM label noted in-file
- Measurements (8): walk Lincoln 0.60 km / 8.0 min; walk Lafarge Lake–Douglas 0.67 / 8.9; walk Glen Elementary 0.73 / 9.8; walk Library 0.49 / 6.5; walk Save-On-Foods Sunwood 1.13 / 15.0; walk Coquitlam Centre 0.48 / 6.4; walk Pinetree Secondary 1.38 / 18.4; drive Coquitlam Central Station 1.59 / 3.3
- NOT CONFIRMED: geocode discrepancy (foreground governs; OSM building point labelled 2970A Glen Drive); catchments; frequencies. §3 includes Pinetree Secondary (within ~1 km of the governed origin)

### 205. Grand Central 3 — 2975 Atlantic Avenue (central-coquitlam; condos)
- File: grand-central-3--central-coquitlam-nearby-2026-11-02.md — 3,213 B; 369 words — within cap
- Origin: named building point, Atlantic Avenue (49.2820073, -122.7970620) — governed foreground re-run
- Measurements (8): walk Lincoln 0.48 km / 6.4 min; walk Lafarge Lake–Douglas 0.72 / 9.6; walk Glen Elementary 0.78 / 10.4; walk Library 0.43 / 5.8; walk Save-On-Foods Sunwood 1.01 / 13.4; walk Coquitlam Centre 0.43 / 5.8; walk Pinetree Secondary 1.43 / 19.1; drive Coquitlam Central Station 1.45 / 3.3
- NOT CONFIRMED: geocode discrepancy (foreground governs; named building point on Atlantic Avenue); catchments; frequencies

### 206. Grand Central One — 2978 Glen Drive (central-coquitlam; condos)
- File: grand-central-one--central-coquitlam-nearby-2026-11-02.md — 3,196 B; 369 words — within cap
- Origin: named building point ("Grand Central 1", Glen Drive, 49.2824135, -122.7965339) — governed foreground re-run. (The worker's first report's "segment point" note for this building is superseded — the governed origin is the named building point)
- Measurements (8): walk Lincoln 0.53 km / 7.0 min; walk Lafarge Lake–Douglas 0.59 / 7.9; walk Glen Elementary 0.66 / 8.8; walk Library 0.41 / 5.5; walk Save-On-Foods Sunwood 1.05 / 14.0; walk Coquitlam Centre 0.56 / 7.4; walk Pinetree Secondary 1.31 / 17.4; drive Coquitlam Central Station 1.51 / 3.3
- NOT CONFIRMED: geocode discrepancy (foreground governs; named "Grand Central 1" building point); catchments; frequencies

### 207. Hideaway Park — 4200 Dewdney Trunk Road (central-coquitlam; 55-plus)
- File: hideaway-park--central-coquitlam-nearby-2026-11-02.md — 2,786 B; 366 words — within cap
- Origin: house node, exact 4200 Dewdney Trunk Road (49.2758871, -122.8224307, Cassin side) — the toolchain's consistent answer across the backgrounded run and the foreground re-run, so it governs. Flagged for the record: the point sits NW of the Ranch Park anchors, while the program home file describes the park as being in Ranch Park; the roster line was NOT corrected. Header class only: manufactured-home park, per the roster
- Measurements (6, all drive): Coquitlam Central Station 2.98 km / 5.2 min; Coquitlam Centre 3.46 / 6.2; Ranch Park 4.27 / 6.8; Ranch Park Elementary 4.52 / 6.8; Poirier Sport and Leisure Complex 4.91 / 10.1; Save-On-Foods Austin Ave 6.73 / 10.4
- Over-cap measured but excluded (stated in-file): walk to Ranch Park 2.22 km / 28.6 min; walk to Ranch Park Elementary 1.84 / 25.2 min — both over the 1.5 km walk cap
- NOT CONFIRMED: geocode discrepancy (foreground governs); the over-cap walks above; no grocery within ~1 km confirmed (Austin Ave Save-On-Foods, #1-2662 Austin Avenue via retailer's own-domain search result, disclosed in-file, is nearest confirmed); catchments; frequencies
