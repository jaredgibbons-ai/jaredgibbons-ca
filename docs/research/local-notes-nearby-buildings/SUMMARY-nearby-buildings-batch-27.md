# What's Nearby — Phase 2, Batch P2-27 Summary

Production date: 2026-11-02 (all measurements taken 2026-11-02).

**Roster range covered: entries 670–694 — 25 buildings produced.** Every entry in the range carries a street address, so no extension was needed and nothing in the range was skipped.

**Skipped problem entries in range: none.** Mop-up list to date (unchanged): entries 52, 85, 86, 156, 188, 193, 195, 240, 415, 487, 535, 549–552, 627, 632, 643, 667.

**Areas:** mission-homes-for-sale 3, montecito 2, moody-park 5, morgan-creek 6, mount-pleasant-ve 3, murrayville 6.

**Measurements: 88 listed in §5 (50 walk, 38 drive)**, all measured 2026-11-02 starting at each building's own address or its disclosed origin; every kept walk inside the 4–6 km/h sanity band and the walk ≤1.5 km / drive ≤10 km caps. **HTTP 429s: none** across all seven workers (five production + two remediation). **Roster lines proved wrong on the ground: none** — the roster was never silently corrected. **Word-cap overages: none** (largest file 397 words).

**Five buildings could not be measured** — Preston on Fourteenth (670), Silver & Cedar (672), Kingston House (681), 9 On The Park (686), Eaglecrest (691): after repeated foreground variants no origin point verified to the building (Mission's 14th Ave / Cedar St returned only whole-street segments identical for neighbouring addresses; 2337 Brunswick St returned only segment points reverse-geocoding to other Brunswick addresses; Eaglecrest's only block segment point reverse-geocoded to the Murrayville Library, a different feature; Kingston House — see correction note below). Each file's §§1–4 are complete and §5 is the brief's single bullet "Travel times: not measured in this pass," with the failure disclosed in NOT CONFIRMED.

**Correction governance — the Morgan Creek set (the batch's main event, all disclosed in-file):** the Morgan Creek worker's first geocode run backgrounded despite a foreground request and its full output landed only after that worker's report; the coordinator held the set and commissioned two remediation passes before this batch was assembled.
- **Edgewater (680), Sundance (683), Tehama (684) re-measured** from their verified building-footprint points (building ways tagged with the roster addresses; Sundance a house node). The first-pass origins reverse-geocode to 3569 150A Street, the Rosemary Greenway cycleway, and 3336 155 Street respectively — all discarded. Tehama's walks lengthened from the correct (western) building point, as expected. Edgewater gained a walk pair: Rosemary Heights Elementary is 0.76 km from the footprint point (1.53 km, over cap, from the wrong origin). One further in-cap pair from the correction pass — Edgewater walk to Morgan Creek Park, 1.50 km / 20.0 min — was measured but NOT listed; the destination already appears in that §5 as a drive pair, and the omission is recorded here.
- **Kingston House (681):** no house point exists for 3323 151 Street, and the first-pass origin reverse-geocodes to an Indigo parking point on 32 Avenue. A dedicated segment attempt then failed on the merits: only three 151 Street ways exist in South Surrey in the geocoder and none spans the 3300 block; reverse probes along the building's frontage return "32 Avenue Diversion" / "Pioneer Greenway" — that stretch of road is not named 151 Street in OSM. §5 converted to the not-measured fallback and the first-pass measurements withdrawn, disclosed in-file.
- **Prescott Commons (682):** no house point for either rostered address; first-pass origin reverse-geocodes to 15077 34 Avenue. Re-measured from a verified street-segment origin: way 415574582 on 33 Avenue runs exactly from the 151 Street to the 152 Street intersection (the building's own 15100 block); the origin vertex used reverse-geocodes to 33 Avenue. Anchor stayed on the first rostered address; no anchor switch needed.
- Kingston/Prescott §§1–4 were untouched by both remediation passes; only §5 and the origin disclosures changed.

**Other geocode resolutions, all disclosed in-file:**
- Murrayville wrong-town discards: initial address-only geocodes for five of six buildings returned generic road segments in the City of Langley (wrong town) and were discarded; name/postal/viewbox foreground variants produced the points used. Four Murrayville origins are street-segment points on the building's own block (Cedar Crest Estates, Fraser, Murray's Landing, Murrayville House), each reverse-geocoding to the correct street and disclosed.
- Montecito sanity discards: walks to Montecito Elementary from The Ambassador (7.9 km/h) and to Montecito Park from both Montecito buildings (10.1 / 11.8 km/h) fell outside the 4–6 km/h band and were discarded rather than published (drive pairs used where applicable); disclosed in-file.
- Moody Park destination points: Royal City Centre and təməsew̓txʷ Aquatic and Community Centre centroids reverse to tenants at the same civic addresses — same buildings, accepted; the first Moody Park Arena geocode (an Eighth Avenue segment in Glenbrooke North) was discarded for the named arena building point.
- Mount Pleasant destination points: Mount Pleasant Elementary and Kingsgate Mall points reverse-geocode to other features at the same civic addresses (2300 Guelph St; 370 E Broadway) — named points at those addresses used, disclosed in both Vancouver files. Broadway Subway / Mount Pleasant Station status was NOT confirmed from a TransLink page read in this pass and is named as open/serving nowhere; carried in NOT CONFIRMED.
- Wedgewood (685): the Walmart destination's named point sits at the rostered address 2355 160 St though its reverse names a co-located business at the same address — used, disclosed.
- Morgan Creek Park destination point: the address node for its §2 civic address (3302 156A Street) is used program-wide in this set, as in the original files; a named park-way centroid ~80 m southeast exists and was not substituted (recorded here for a possible later harmonizing pass).

**Name-spelling discrepancy (flagged, roster kept):** The Doncaster (676) — OSM spells the building "The Duncaster" at the roster's exact address, 620 Eighth Avenue; the roster name stands and the discrepancy is disclosed in the file's NOT CONFIRMED.

**Multi-address entries** produced as one file each, first address as title/anchor, all addresses in the header exactly as rostered, anchor choice disclosed: Villa Montecito (674, anchor 7307 Montecito Drive), Prescott Commons (682, anchor 15137 33 Avenue), The District (687, anchor 250 East 6th Avenue), Autumn Ridge (689, anchor 22015 48 Avenue).

## Per-building detail

### 670. Preston on Fourteenth ("The Preston") — 32690 14th Avenue, Mission (mission-homes-for-sale; condos)
- File: preston-on-fourteenth--mission-homes-for-sale-nearby-2026-11-02.md — 2,148 B / 238 w
- Origin: NONE usable — only whole-street 14th Avenue segments (identical for 32590/32600/32700); named-building and postal variants empty. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); school catchments; bus frequencies.

### 671. Ridgewood Place — 7265 Haig Street, Mission (mission-homes-for-sale; condos)
- File: ridgewood-place--mission-homes-for-sale-nearby-2026-11-02.md — 2,553 B / 306 w
- Origin: verified house point (reverse: 7265 Haig Street).
- Measurements (5): walk Superstore 14.3 min/1.06 km; drive Mission City Station 2.6/1.60; drive Superstore 2.2/1.15; drive Mission Leisure Centre 3.9/2.14; drive Mission Library 3.4/1.81. Excluded over-cap walks (station/Leisure/Library/Centennial Park, 1.62–2.57 km), disclosed.
- NOT CONFIRMED: catchments; bus frequencies.

### 672. Silver & Cedar — 8423 Cedar Street, Mission (mission-homes-for-sale; condos)
- File: silver-cedar--mission-homes-for-sale-nearby-2026-11-02.md — 2,162 B / 243 w
- Origin: NONE usable — only whole-street Cedar Street segments (identical for 8400/8450/8500/8955). §5 = not-measured fallback.
- Measurements (0). §3 schools: Albert McMahon Elementary; Valley Christian School (independent, Ministry-listed), 8955 Cedar St.
- NOT CONFIRMED: travel times (origin failure); catchments; bus frequencies.

### 673. The Ambassador — 7321 Halifax Street, Burnaby (montecito; condos)
- File: the-ambassador--montecito-nearby-2026-11-02.md — 2,844 B / 331 w
- Origin: named-building point (reverse: The Ambassador, 7321 Halifax Street).
- Measurements (5): walk Halifax Park 11.7/0.91; drive Montecito Elementary 1.6/0.76; drive Sperling–Burnaby Lake Station 4.3/2.36; drive Kensington Square 4.8/2.84; drive Bill Copeland Sports Centre 5.8/3.54. Discarded sanity-failing walks (Montecito Elementary 7.9 km/h; Montecito Park 10.1 km/h), disclosed.
- NOT CONFIRMED: catchment for this address (the program's Duthie Ave district run was not carried over); bus frequencies; §4 Safeway address from a retailer own-domain search result, disclosed.

### 674. Villa Montecito — 7307, 7321 and 7335 Montecito Drive, and 7363 and 7387 Capistrano Drive, Burnaby (montecito; townhomes)
- File: villa-montecito--montecito-nearby-2026-11-02.md — 2,838 B / 353 w
- Multi-address: one file; anchor 7307 Montecito Drive (verified house point, reverse exact); header carries all five addresses; anchor choice disclosed.
- Measurements (4): walk Montecito Elementary 3.0/0.23; walk Halifax Park 14.5/1.22; drive Sperling Station 3.6/1.84; drive Kensington Square 5.6/3.23. Discarded: Montecito Park walk (11.8 km/h, outside sanity band) and its drive, disclosed.
- NOT CONFIRMED: anchor choice; catchment; bus frequencies.

### 675. The Diplomat — 707 Eighth Street, New Westminster (moody-park; condos)
- File: the-diplomat--moody-park-nearby-2026-11-02.md — 3,242 B / 386 w
- Origin: verified house point (reverse: 707 Eighth Street).
- Measurements (5): walk Moody Park 2.9/0.22; walk Moody Park Arena 6.5/0.49; walk NWPL Main Branch 5.4/0.41; walk Royal City Centre 9.9/0.74; drive New Westminster Station 3.6/1.81.
- NOT CONFIRMED: catchments; bus frequencies; Royal City Centre street address source (centre's own pages do not print it; §4 Save-On-Foods address from a retailer own-domain search result, disclosed).

### 676. The Doncaster — 620 Eighth Avenue, New Westminster (moody-park; condos)
- File: the-doncaster--moody-park-nearby-2026-11-02.md — 3,353 B / 396 w
- Origin: verified building point (reverse: 620 Eighth Avenue; OSM name reads "The Duncaster" — spelling discrepancy disclosed, roster name kept).
- Measurements (5): walk Moody Park Arena 2.4/0.18; walk New Westminster Secondary 4.6/0.34; walk Moody Park 7.3/0.54; walk NWPL Main Branch 10.3/0.77; drive New Westminster Station 4.4/2.14.
- NOT CONFIRMED: the name-spelling discrepancy; catchments; bus frequencies; Royal City Centre address source.

### 677. Fraser Gardens — 1169 Eighth Avenue, New Westminster (moody-park; condos)
- File: fraser-gardens--moody-park-nearby-2026-11-02.md — 3,227 B / 372 w
- Origin: verified house point (reverse: 1169 Eighth Avenue).
- Measurements (4): walk Moody Park 10.1/0.76; walk Lord Tweedsmuir Elementary 13.3/1.00; drive New Westminster Station 4.9/2.57; drive təməsew̓txʷ Aquatic and Community Centre 5.4/2.84.
- NOT CONFIRMED: catchments; bus frequencies; Royal City Centre address source.

### 678. Moody Gardens — 777 Eighth Street, New Westminster (moody-park; condos)
- File: moody-gardens--moody-park-nearby-2026-11-02.md — 3,207 B / 380 w
- Origin: verified house point (reverse: 777 Eighth Street).
- Measurements (5): walk Moody Park Arena 2.9/0.21; walk Moody Park 4.3/0.32; walk NWPL Main Branch 7.9/0.59; walk Royal City Centre 12.4/0.93; drive New Westminster Station 3.8/1.97.
- NOT CONFIRMED: catchments; bus frequencies; Royal City Centre address source.

### 679. Villa Franciscan — 708 Eighth Avenue, New Westminster (moody-park; condos)
- File: villa-franciscan--moody-park-nearby-2026-11-02.md — 3,280 B / 387 w
- Origin: verified house point (reverse: 708 Eighth Avenue).
- Measurements (5): walk Moody Park Arena 2.6/0.20; walk New Westminster Secondary 4.8/0.36; walk Moody Park 6.7/0.50; walk NWPL Main Branch 10.3/0.77; drive New Westminster Station 4.5/2.15.
- NOT CONFIRMED: catchments; bus frequencies; Royal City Centre address source.

### 680. Edgewater — 15195 36 Avenue, Surrey (morgan-creek; condos)
- File: edgewater--morgan-creek-nearby-2026-11-02.md — 3,073 B / 386 w
- Origin: CORRECTED in remediation — building way tagged 15195 36 Avenue (reverse exact). First-pass origin (reverse: 3569 150A Street) discarded.
- Measurements (6): walk Rosemary Heights Park 9.7/0.73; walk Rosemary Heights Elementary 10.1/0.76 (added in correction — in cap from the correct origin); drive Morgan Creek Park 3.1/1.80; drive Walmart 6.0/3.64; drive White Rock Centre 6.8/4.13; drive Grandview Heights Aquatic Centre 8.4/5.67. Measured-not-listed: walk Morgan Creek Park 20.0/1.50 (destination already a drive pair; recorded in the governance note above).
- NOT CONFIRMED: correction-pass origin disclosure; catchments; bus frequencies.

### 681. Kingston House (Harvard Gardens) — 3323 151 Street, Surrey (morgan-creek; condos)
- File: kingston-house--morgan-creek-nearby-2026-11-02.md — 2,550 B / 300 w
- Origin: NONE — no house point exists; first-pass origin failed reverse-geocoding (Indigo parking, 32 Avenue) and its measurements were withdrawn; block-segment attempt failed (no 151 Street way spans the 3300 block; frontage reverse-probes return 32 Avenue Diversion / Pioneer Greenway). §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: measurement-origin disclosure (as above); catchments; bus frequencies; unit count unconfirmed in the home program file.

### 682. Prescott Commons (Harvard Gardens) — 15137 33 Avenue and 15138 34 Avenue, Surrey (morgan-creek; condos)
- File: prescott-commons--morgan-creek-nearby-2026-11-02.md — 3,084 B / 391 w
- Multi-address: one file; anchor 15137 33 Avenue (unchanged); header carries both addresses; anchor disclosed.
- Origin: CORRECTED in remediation 2 — street-segment point on way 415574582 (33 Avenue, the building's own 15100 block, 151 St→152 St; reverse: 33 Avenue). First-pass origin (reverse: 15077 34 Avenue) discarded.
- Measurements (5): walk Rosemary Heights Park 10.8/0.81; walk Rosemary Heights Elementary 14.8/1.11; drive Morgan Creek Park 2.5/1.35; drive Walmart Supercentre 5.4/3.19; drive White Rock Centre 7.2/4.16.
- NOT CONFIRMED: anchor; segment-origin + correction disclosure; catchments; bus frequencies.

### 683. Sundance — 15233 34 Avenue, Surrey (morgan-creek; townhomes)
- File: sundance--morgan-creek-nearby-2026-11-02.md — 2,962 B / 366 w
- Origin: CORRECTED in remediation — house node tagged 15233 34 Avenue (reverse exact). First-pass origin (reverse: Rosemary Greenway cycleway) discarded.
- Measurements (5): walk Rosemary Heights Park 6.1/0.46; walk Rosemary Heights Elementary 10.5/0.79; walk Morgan Creek Park 13.2/0.99; drive Morgan Elementary 2.8/1.01; drive Walmart 5.5/3.26.
- NOT CONFIRMED: correction-pass origin disclosure; catchments; bus frequencies.

### 684. Tehama — 3355 Rosemary Heights Drive, Surrey (morgan-creek; condos)
- File: tehama--morgan-creek-nearby-2026-11-02.md — 3,043 B / 377 w
- Origin: CORRECTED in remediation — building way tagged 3355 Rosemary Heights Drive (reverse exact). First-pass origin (reverse: 3336 155 Street) discarded; walks lengthened from the correct point.
- Measurements (5): walk Rosemary Heights Elementary 8.0/0.60; walk Morgan Creek Park 9.5/0.71; walk Morgan Elementary 10.4/0.78; drive Walmart 5.6/3.04; drive White Rock Centre 7.2/4.09.
- NOT CONFIRMED: correction-pass origin disclosure; catchments; bus frequencies.

### 685. Wedgewood — 15715 34 Avenue, Morgan Creek, Surrey (morgan-creek; townhomes)
- File: wedgewood--morgan-creek-nearby-2026-11-02.md — 2,799 B / 372 w
- Origin: verified house point (reverse: 15715 34 Avenue).
- Measurements (5): walk Morgan Elementary 4.1/0.31; walk Morgan Creek Park 5.3/0.40; drive Rosemary Heights Elementary 2.9/1.24; drive Save-On-Foods (3033 152 St) 4.5/2.21; drive Walmart Supercentre (2355 160 St) 5.2/2.93.
- NOT CONFIRMED: catchments; bus frequencies; no recreation centre/library confirmed on a City of Surrey page read; Walmart destination-point note (same-address co-located business).

### 686. 9 On The Park — 2337 Brunswick Street, Vancouver (mount-pleasant-ve; townhomes)
- File: 9-on-the-park--mount-pleasant-ve-nearby-2026-11-02.md — 2,221 B / 266 w
- Origin: NONE verified — only Brunswick Street segment points, reverse-geocoding to 2222 / 2150 / 2490 Brunswick Street (other blocks/features); all discarded per governance rather than substituting a neighbouring point. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); catchments; bus frequencies; Broadway Subway / Mount Pleasant Station status not confirmed from a TransLink page read.

### 687. The District — 250 East 6th Avenue and 255 East 7th Avenue, Vancouver (mount-pleasant-ve; condos)
- File: the-district--mount-pleasant-ve-nearby-2026-11-02.md — 3,120 B / 397 w
- Multi-address: one file; anchor 250 East 6th Avenue (verified house point, reverse exact); header carries both addresses; anchor disclosed.
- Measurements (5): walk Mount Pleasant Community Centre 2.2/0.17; walk Guelph Park 4.6/0.35; walk Kingsgate Mall 7.5/0.56; walk Mount Pleasant Elementary 7.5/0.56; drive VCC–Clark Station 4.1/1.78.
- NOT CONFIRMED: anchor choice; catchments; bus frequencies; Broadway Subway station status; same-address destination-point notes (Mount Pleasant Elementary, Kingsgate Mall).

### 688. Main & Sixth (M6) — 2218 Main Street at East 6th Avenue, Vancouver (mount-pleasant-ve; condos)
- File: main-sixth--mount-pleasant-ve-nearby-2026-11-02.md — 3,074 B / 383 w
- Origin: verified building point (reverse at the exact point: 2218 Main Street; an early transposed-coordinate reverse returning 2202 Main Street was discarded).
- Measurements (5): walk Mount Pleasant Community Centre 1.3/0.10; walk Guelph Park 4.5/0.34; walk Kingsgate Mall 7.0/0.52; walk Mount Pleasant Elementary 7.4/0.55; drive VCC–Clark Station 4.4/1.86. §1 anchored on TransLink stop 50177 (Northbound Main St @ E 6th Ave; routes 3 and 8), read from the TransLink stop page this pass.
- NOT CONFIRMED: catchments; bus frequencies; Broadway Subway station status; same-address destination-point notes.

### 689. Autumn Ridge — 22015 / 22025 48 Avenue, Langley (murrayville; condos)
- File: autumn-ridge--murrayville-nearby-2026-11-02.md — 2,604 B / 313 w
- Multi-address: one file; anchor 22015 48 Avenue (named building point, reverse: Autumn Ridge, 22015 48 Avenue); header carries the rostered address form; anchor disclosed.
- Measurements (3): walk Murrayville Library 2.5/0.18; walk IGA (22259 48 Ave) 7.3/0.55; drive W.C. Blair Recreation Centre 1.7/0.53.
- NOT CONFIRMED: bus frequencies; catchments; origin verification note.

### 690. Cedar Crest Estates — 21848 50 Avenue, Langley (murrayville; townhomes)
- File: cedar-crest-estates--murrayville-nearby-2026-11-02.md — 2,563 B / 310 w
- Origin: 50 Avenue street-segment point spanning the building's block (reverse: 50 Avenue, Murrayville), disclosed; no named/house point in any variant.
- Measurements (3): walk Langley Fundamental Elementary 1.1/0.08; drive W.C. Blair Recreation Centre 2.3/1.05; drive Shoppers Drug Mart (22196 50 Ave) 2.4/1.40.
- NOT CONFIRMED: bus frequencies; catchments; origin segment disclosure. (No age-restriction claim of any kind — the program record's 55+/45+ status conflict is not stated as fact.)

### 691. Eaglecrest — 22150 48 Avenue, Langley (murrayville; condos)
- File: eaglecrest--murrayville-nearby-2026-11-02.md — 2,464 B / 287 w
- Origin: NONE accepted — no named/house point exists; the only 48 Avenue segment point spanning the block reverse-geocoded to FVRL: Murrayville Library, 100 22071 48 Avenue (a different feature) and was discarded per governance. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: bus frequencies; catchments; the origin failure above.

### 692. Fraser — 22128 48A Avenue, Langley (murrayville; townhomes)
- File: fraser--murrayville-nearby-2026-11-02.md — 2,684 B / 317 w
- Origin: 48A Avenue street-segment point (segment bbox exactly the 221 block; reverse: 48A Avenue, Murrayville), disclosed.
- Measurements (3): walk Murrayville Outdoor Activity Park 1.6/0.12; walk Murrayville Library 1.8/0.13; drive W.C. Blair Recreation Centre 0.8/0.19.
- NOT CONFIRMED: bus frequencies; catchments; origin segment disclosure.

### 693. Murray's Landing — 22225 50 Avenue, Langley (murrayville; townhomes)
- File: murrays-landing--murrayville-nearby-2026-11-02.md — 2,675 B / 332 w
- Origin: 50 Avenue street-segment point spanning the building's block (reverse: 50 Avenue, Murrayville), disclosed.
- Measurements (3): walk Shoppers Drug Mart 2.6/0.19; walk IGA 6.9/0.52; drive W.C. Blair Recreation Centre 1.6/0.66.
- NOT CONFIRMED: bus frequencies; catchments; origin segment disclosure; James Hill Elementary excluded from §3 (its geocoded point sits just over 1 km from the origin).

### 694. Murrayville House — 5020 221A Street, Langley (murrayville; condos)
- File: murrayville-house--murrayville-nearby-2026-11-02.md — 2,480 B / 293 w
- Origin: 221A Street street-segment point spanning the building's block (reverse: 221A Street, Murrayville), disclosed.
- Measurements (2): walk W.C. Blair Recreation Centre 10.8/0.81; drive Murrayville Library 1.8/1.07. (A drive to James Hill Elementary, 3.0 min/1.63 km, was measured but not listed — the school is over 1 km away and is not a §§1–4 anchor for this building.)
- NOT CONFIRMED: bus frequencies; catchments; origin segment disclosure.
