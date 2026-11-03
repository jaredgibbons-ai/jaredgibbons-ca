# What's Nearby — Phase 2, Batch P2-4 Summary

Produced Mon Nov 2, 2026 under PHASE2-BRIEF.md. One file per building in `~/workspace/local-notes/nearby/buildings/`.

- **Roster entries covered: 77–84, 87–103 (25 buildings).** Entries 85 (District Flats at Southlands, boundary-beach, condos) and 86 (The Granary at Southlands, boundary-beach, condos + townhomes) skipped — ADDRESS NOT IN NOTES; held for the final mop-up batch (addresses not researched, per the brief). Mop-up list to date: entries 52, 85, 86.
- Areas: beach-grove 1, bear-creek-green-timbers 4, blu-living-townhomes-for-sale 1, blueridge-nv 2, boundary-beach 1, boyd-park 1, brentwood-park 15.
- All five sections + NOT CONFIRMED written in every file — **no sections omitted anywhere**.
- **Measurements: 134 total (75 walk, 59 drive)**, all measured 2026-11-02 starting at each building's own address; every walk inside the 4–6 km/h sanity band and the walk ≤1.5 km / drive ≤10 km caps. Over-cap routes were discarded and disclosed in-file.
- **HTTP 429s: none** across all five workers (Nominatim / OSRM / routed-foot paced ~1 req/sec).
- **Roster lines proved wrong on the ground: none** — the roster was never silently corrected. Geocode substitutions are disclosed in-file wherever used (below).
- Word-cap overages (disclosed, never cut): The Amazing Brentwood Tower 1 483 (+83), 2078–2082 Springer Avenue 454 (+54), Affinity and Affinity II 453 (+53), The Amazing Brentwood Tower 2 451 (+51), Altus 442 (+42), The Pillars 438 (+38), Concord Brentwood Hillside West 425 (+25), Oasis at Concord Brentwood 423 (+23), Escala 422 (+22), Trails at Bear Creek Park 416 (+16), Concord Brentwood Hillside East 415 (+15), Apple Greene 412 (+12), The Amazing Brentwood Tower 3 411 (+11), Baden Park 409 (+9), Kings Landing II 401 (+1). All other files 340–397 words. The Brentwood Park overages are driven by 5–7 measurements per file plus the required geocode/anchor disclosures.

## Per building

**77. The Pillars — 1702 56 Street (anchor); 1700 56 Street (townhouse component) (beach-grove; condos + townhomes)** — the-pillars--beach-grove-nearby-2026-11-02.md — 3,256 B, **438 words (+38 over cap)**.
- Address used: exact OSM building point for the anchor 1702 56 Street; header carries both roster addresses; anchor choice disclosed in NOT CONFIRMED.
- Measurements (7): walk → Grauer Park, 1720 56 St 0.45 km / 6.0 min; walk → Beach Grove Elementary 0.99 / 13.3; walk → Beach Grove Park 1.27 / 17.6; drive → Save-On-Foods, 1143 56 St 1.40 / 2.7; drive → Tsawwassen Library 1.67 / 3.0; drive → South Park Elementary 2.33 / 4.0; drive → South Delta Secondary 2.60 / 4.4.
- NOT CONFIRMED: catchments (no SD37 locator run); frequencies; South Delta Recreation Centre address not read on a City facility page; Boundary Bay Regional Park street address.

**78. Carlingwood — 8888 151 Street (bear-creek-green-timbers; townhomes)** — carlingwood--bear-creek-green-timbers-nearby-2026-11-02.md — 3,017 B, 393 words.
- Address used: exact OSM address point for 8888 151 Street — no substitution.
- Measurements (4): walk → Save-On-Foods, 9014 152 St 0.68 / 9.0; drive → Green Timbers Elementary 1.64 / 2.4; drive → Fleetwood Community Centre 2.88 / 4.7; drive → Bear Creek Park 3.13 / 5.0. Discarded over the walk cap and disclosed in-file: walk → Price Creek Park 1.64 km, walk → Coyote Creek Elementary 2.39 km.
- NOT CONFIRMED: catchments; frequencies; no operator-named exchange for the nearest stops; no school within ~1 km confirmed from the Ministry list.

**79. Kings Landing — 13628 81A Avenue (bear-creek-green-timbers; condos)** — kings-landing--bear-creek-green-timbers-nearby-2026-11-02.md — 2,813 B, 375 words.
- Address used: exact OSM address point for 13628 81A Avenue — no substitution.
- Measurements (6): walk → Bear Creek Park 0.60 / 8.8 (park's southern OSM point in Newton, disclosed); walk → Bear Creek Elementary 1.21 / 16.1; drive → Surrey Arts Centre 1.63 / 2.7; drive → Chalo FreshCo, 7165 138 St 2.52 / 4.3; drive → Frank Hurt Secondary 3.15 / 5.4; drive → King George Station 3.58 / 4.9.
- NOT CONFIRMED: catchments; frequencies; exact nearest individual stop; separation from Kings Landing II (entry 80) stated in-file.

**80. Kings Landing II — 13623 81A Avenue (anchor); 8168 136A Street + 13636 81A Avenue (townhomes) (bear-creek-green-timbers; condos + townhomes)** — kings-landing-ii--bear-creek-green-timbers-nearby-2026-11-02.md — 2,996 B, **401 words (+1)**.
- Address used: exact OSM address point for the anchor 13623 81A Avenue; header carries all three roster addresses; anchor disclosed in NOT CONFIRMED. Neither townhome address returned an exact OSM point (street segments only; the 13636 81A Avenue query returned wrong-city segment points first — discarded, not used).
- Measurements (6): walk → Bear Creek Park 0.59 / 8.8 (southern park point, disclosed); walk → Bear Creek Elementary 1.23 / 16.3; drive → Surrey Arts Centre 1.63 / 2.7; drive → Chalo FreshCo 2.52 / 4.3; drive → Frank Hurt Secondary 3.15 / 5.4; drive → King George Station 3.58 / 4.9.
- NOT CONFIRMED: multi-address anchor choice; catchments; frequencies; separate building from entry 79.

**81. Trails at Bear Creek Park (townhouse component) — 13660 84 Avenue (bear-creek-green-timbers; townhomes)** — trails-at-bear-creek-park--bear-creek-green-timbers-nearby-2026-11-02.md — 3,113 B, **416 words (+16)**.
- Address used: exact OSM address point for 13660 84 Avenue — no substitution.
- Measurements (6): walk → Bear Creek Park 1.16 / 16.3 (southern park point, disclosed); walk → Surrey Arts Centre 1.33 / 17.7; drive → Green Timbers Elementary 2.79 / 4.2; drive → Chalo FreshCo 3.07 / 5.7; drive → Bear Creek Elementary 3.96 / 6.2; drive → Enver Creek Secondary 4.23 / 7.6.
- NOT CONFIRMED: directory variant 13670 84 Avenue UNCONFIRMED whether same strata (carried verbatim, not used); 13680 84 Ave apartments not counted, per roster; catchments; frequencies; no operator-named exchange.

**82. Blu Living — 15988 32 Avenue (blu-living-townhomes-for-sale; townhomes)** — blu-living--blu-living-townhomes-for-sale-nearby-2026-11-02.md — 2,988 B, 340 words.
- Address used: exact Nominatim address point for 15988 32 Avenue — no substitution.
- Measurements (4): walk → Morgan Elementary 0.95 / 12.6; drive → Thrifty Foods 1.88 / 4.0; drive → Real Canadian Superstore 2.21 / 4.3; drive → Grandview Heights Aquatic Centre 3.42 / 5.1.
- NOT CONFIRMED: SD36 catchments (no locator run); bus frequencies; Morgan Crossing street address on the centre's own site.

**83. Baden Park — 948 Lytton Street (anchor); 954, 956, 968 Lytton Street (blueridge-nv; condos)** — baden-park--blueridge-nv-nearby-2026-11-02.md — 3,197 B, **409 words (+9)**.
- Address used: no house-number point exists — origin = Lytton Street segment point in V7H 2M5 nearest the 948 block, disclosed in §5/NOT CONFIRMED; times approximate. Header carries all four roster addresses.
- Measurements (5): walk → Ron Andrews Community Recreation Centre, 931 Lytton St 0.24 / 2.5; walk → Seymour Heights Elementary 0.63 / 8.5; drive → Blueridge Elementary 1.88 / 3.6; drive → Phibbs Exchange 3.35 / 4.7; drive → Save-On-Foods Park & Tilford 3.74 / 5.5.
- NOT CONFIRMED: anchor choice (first address); catchments; route 214 frequency; exact nearest stop; Blueridge / McCartney Creek Park street addresses.

**84. Berkley Terraces — 999 Berkley Road (blueridge-nv; condos)** — berkley-terraces--blueridge-nv-nearby-2026-11-02.md — 3,114 B, 390 words.
- Address used: no house-number point — Berkley Road segment point in V7H 1Y2 nearest the 999 block, disclosed; times approximate.
- Measurements (4): walk → Seymour Heights Elementary 0.53 / 7.1; walk → Blueridge Elementary 0.71 / 9.5; drive → Ron Andrews CRC 0.98 / 2.1; drive → Phibbs Exchange 3.71 / 5.1.
- NOT CONFIRMED: catchments; route 214 frequency; exact nearest stop; park street addresses; building-point geocode.

**87. Monterra — 6505 3 Avenue (boundary-beach; townhomes)** — monterra--boundary-beach-nearby-2026-11-02.md — 2,864 B, 371 words.
- Address used: exact Nominatim address point for 6505 3 Avenue — no substitution.
- Measurements (6): walk → Centennial Beach / Boundary Bay Regional Park (570 Boundary Bay Rd point) 1.21 / 16.0; drive → Diefenbaker Park 2.59 / 4.3; drive → South Park Elementary 2.90 / 4.8; drive → South Delta Secondary 3.41 / 5.6; drive → Save-On-Foods, 1143 56 St 3.53 / 5.6; drive → Beach Grove Elementary 3.85 / 7.4.
- NOT CONFIRMED: SD37 catchments; frequencies; Boundary Bay Regional Park street address (not on the Metro Vancouver page).

**88. Apple Greene — 8720 No. 1 Road (anchor); 8740, 8760, 8840, 8860, 8880 No. 1 Road (boyd-park; condos)** — apple-greene--boyd-park-nearby-2026-11-02.md — 3,048 B, **412 words (+12)**.
- Address used: Nominatim returns NO house-number point for any of the six roster addresses (all tried individually in this pass) — origin = No. 1 Road segment point in V7C 1J7 (the complex's postal area), disclosed in §5/NOT CONFIRMED; times approximate. Roster addresses NOT proven wrong. Header carries all six addresses.
- Measurements (4): walk → West Richmond Community Centre 0.40 / 5.4; walk → Safeway (Seafair) 0.43 / 5.7; walk → Hugh Boyd Secondary 0.55 / 7.4; drive → R.M. Grauer Elementary 1.53 / 2.6.
- NOT CONFIRMED: anchor choice; building-point geocode (none exists for any of the six); SD38 catchments; frequencies.

**89. 2078–2082 Springer Avenue — 2078–2082 Springer Avenue (brentwood-park; townhomes)** — 2078-2082-springer-avenue--brentwood-park-nearby-2026-11-02.md — 3,586 B, **454 words (+54)**. UNNAMED IN NOTES — the address is the name, kept as-is in title/header.
- Address used: substitution, disclosed in §5/NOT CONFIRMED — no Nominatim house-number point exists for 2078–2082 Springer Ave in any variant tried; origin = Springer Avenue segment point in the V5B 2X7 area nearest the 2078 block (calibrated against Slate, 2135 Springer Ave). Anchor = first address in the range.
- Measurements (6): walk → Holdom Station 0.40 / 5.4; walk → Holy Cross Elementary 1.10 / 14.7; walk → Brentwood Park Elementary 1.17 / 15.6; walk → Brentwood Park 1.39 / 18.9; drive → Burnaby North Secondary 2.93 / 5.3; drive → Confederation Park 4.06 / 6.7.
- NOT CONFIRMED: catchments (no SD41 locator run); bus frequencies; segment origin; no grocery anchor within ~1 km confirmed from an allowed source (§4 anchors sit beyond ~1 km).

**90. Affinity and Affinity II — 2200 Douglas Road (anchor); 2232 Douglas Road (brentwood-park; condos)** — affinity-and-affinity-ii--brentwood-park-nearby-2026-11-02.md — 3,609 B, **453 words (+53)**.
- Address used: exact — Nominatim building point "Affinity I, 2200 Douglas Road" (V5C 5A9). Header carries both roster addresses; anchor choice disclosed in NOT CONFIRMED.
- Measurements (5): walk → Holdom Station 0.59 / 7.9; walk → Holy Cross Elementary 0.99 / 13.2; walk → Brentwood Park Elementary 1.06 / 14.1; drive → The Amazing Brentwood 1.06 / 2.8; drive → Burnaby North Secondary 3.32 / 6.3.
- NOT CONFIRMED: anchor choice; catchments; frequencies.

**91. Altus — 4485 Skyline Drive (brentwood-park; condos)** — altus--brentwood-park-nearby-2026-11-02.md — 3,575 B, **442 words (+42)**.
- Address used: substitution, disclosed — no building point for 4485 Skyline Drive (named "Altus" query also empty); origin = Skyline Drive segment point, essentially coincident with the SOLO District landuse point returned in the same pass.
- Measurements (7): walk → Whole Foods Market, 4420 Lougheed Hwy 0.20 / 2.6; walk → Brentwood Town Centre Station 0.34 / 4.5; walk → The Amazing Brentwood 0.97 / 12.9; walk → Brentwood Park 1.24 / 16.8; drive → Save-On-Foods, 4399 Lougheed Hwy 0.73 / 1.8; drive → Brentwood Park Elementary 1.76 / 3.5; drive → Confederation Park 2.83 / 5.7.
- NOT CONFIRMED: catchments; frequencies; segment origin.

**92. The Amazing Brentwood, Tower 1 — 4510 Halifax Way (brentwood-park; condos)** — the-amazing-brentwood-tower-1--brentwood-park-nearby-2026-11-02.md — 3,746 B, **483 words (+83, largest overage; kept rather than cut the duplicate-geocode and Tower ONE/Tower 1 disclosures)**.
- Address used: Nominatim address point for 4510 Halifax Way in the V5C 3Z6 area beside the station. Disclosed in NOT CONFIRMED: Nominatim returned a second point for the same address (V5C 3Z0, ~600 m west) — not used.
- Measurements (7): walk → Brentwood Town Centre Station 0.18 / 2.3; walk → Whole Foods 0.39 / 5.2; walk → The Amazing Brentwood 0.57 / 7.6; walk → Brentwood Park 0.89 / 12.5; drive → Brentwood Park Elementary 1.21 / 2.6; drive → Confederation Park 2.64 / 5.3; drive → Burnaby North Secondary 3.94 / 6.9.
- NOT CONFIRMED: catchments; frequencies; duplicate geocode (above); strata Tower 1 ≠ rental "Tower ONE," 1820 Willingdon Ave (condos home file trap, carried in-file).

**93. The Amazing Brentwood, Tower 2 — 1955 Alpha Way (brentwood-park; condos)** — the-amazing-brentwood-tower-2--brentwood-park-nearby-2026-11-02.md — 3,615 B, **451 words (+51)**.
- Address used: substitution, disclosed — no house-number point for 1955 Alpha Way (named-tower query also empty); origin = Alpha Way segment point (V5C 3Z6) beside the station, ~40 m from Tower 1's origin point.
- Measurements (7): walk → Brentwood Town Centre Station 0.19 / 2.6; walk → Whole Foods 0.41 / 5.5; walk → The Amazing Brentwood 0.54 / 7.2; walk → Brentwood Park 0.86 / 12.1; drive → Save-On-Foods 0.72 / 1.5; drive → Brentwood Park Elementary 1.22 / 2.7; drive → Confederation Park 2.65 / 5.3.
- NOT CONFIRMED: catchments; frequencies; segment origin.

**94. The Amazing Brentwood, Tower 3 — 4650 Brentwood Boulevard (brentwood-park; condos)** — the-amazing-brentwood-tower-3--brentwood-park-nearby-2026-11-02.md — 3,282 B, **411 words (+11)**.
- Address used: no Nominatim building point for 4650 Brentwood Boulevard — Brentwood Boulevard street-segment point in the V5C 3Z0 area, disclosed in §5/NOT CONFIRMED.
- Measurements (5): walk → Brentwood Town Centre Station 0.39 / 5.2; walk → Save-On-Foods 0.56 / 7.5; walk → The Amazing Brentwood 0.65 / 8.7; walk → Brentwood Park 0.96 / 13.1; drive → Brentwood Park Elementary 1.24 / 3.3.
- NOT CONFIRMED: catchments; bus frequencies; segment geocode; no supermarket inside the centre confirmed from its own site.

**95. Anola Place — 2041 Bellwood Avenue (brentwood-park; condos)** — anola-place--brentwood-park-nearby-2026-11-02.md — 3,097 B, 388 words.
- Address used: exact named Nominatim building point "Anola Place, 2041 Bellwood Avenue" — no substitution.
- Measurements (5): walk → Holy Cross Elementary (independent) 0.84 / 11.2; walk → Brentwood Park Elementary 0.91 / 12.2; walk → Brentwood Park 1.13 / 15.5; drive → Brentwood Town Centre Station 1.65 / 2.9; drive → Burnaby North Secondary 3.03 / 6.1.
- NOT CONFIRMED: catchments; frequencies.

**96. Aviara — 4189 Halifax Street (brentwood-park; condos)** — aviara--brentwood-park-nearby-2026-11-02.md — 3,015 B, 377 words.
- Address used: exact named Nominatim building point "Aviara, 4189 Halifax Street" — no substitution.
- Measurements (5): walk → Save-On-Foods 0.45 / 6.0; walk → Whole Foods 0.72 / 9.7; walk → Brentwood Town Centre Station 0.96 / 12.8; drive → Brentwood Park Elementary 2.14 / 4.2; drive → Confederation Park 2.92 / 5.9.
- NOT CONFIRMED: catchments; frequencies; Brentwood Park (park) not measured from this address.

**97. Brentwood Block — 2180 Alpha Avenue (brentwood-park; condos)** — brentwood-block--brentwood-park-nearby-2026-11-02.md — 3,023 B, 390 words. Treated as a normal roster building; no status claims beyond the roster line.
- Address used: no building point — Alpha Avenue street-segment point in the V5C 0K2 (south Alpha) area returned for the address, disclosed; a first-returned Burnaby Heights Alpha segment was discarded/not used, disclosed in-file.
- Measurements (5): walk → Brentwood Town Centre Station 0.47 / 6.3; walk → Whole Foods 0.66 / 8.8; walk → The Amazing Brentwood 0.89 / 11.9; drive → Brentwood Park Elementary 1.46 / 3.0; drive → Alpha Secondary 2.00 / 4.1.
- NOT CONFIRMED: catchments; frequencies; segment geocode.

**98. Cirrus — 2085 Skyline Court (brentwood-park; condos)** — cirrus--brentwood-park-nearby-2026-11-02.md — 3,112 B, 387 words. Title name "Cirrus" per the brief's parenthetical-drop rule.
- Address used: no building point — Skyline Court street-segment point returned for 2085 Skyline Court, beside the named SOLO District point, disclosed in §5/NOT CONFIRMED.
- Measurements (5): walk → Whole Foods 0.21 / 2.8; walk → Brentwood Town Centre Station 0.38 / 5.1; walk → The Amazing Brentwood 1.01 / 13.5; drive → Save-On-Foods 0.85 / 2.0; drive → Brentwood Park Elementary 1.78 / 3.7.
- NOT CONFIRMED: catchments; frequencies; segment geocode.

**99. Concord Brentwood, Hillside East — 4890 Lougheed Highway (brentwood-park; condos)** — concord-brentwood-hillside-east--brentwood-park-nearby-2026-11-02.md — 3,269 B, **415 words (+15)**.
- Address used: no Nominatim building point for 4890 Lougheed Hwy (plain/structured queries returned only far-east trunk segments at Holdom/Coquitlam — discarded); origin = Lougheed Highway segment point in the V5C 0C6 area nearest the 4890 block, disclosed in §5/NOT CONFIRMED; times approximate.
- Measurements (5): walk → Brentwood Town Centre Station 0.73 / 9.7; walk → The Amazing Brentwood 0.77 / 10.3; walk → Brentwood Park Elementary 0.83 / 11.1; drive → Burnaby North Secondary 3.32 / 5.7; drive → Confederation Park 4.10 / 6.6.
- NOT CONFIRMED: catchments (no SD41 locator run); bus frequencies; building-point geocode; exchange name at Brentwood station.

**100. Concord Brentwood, Hillside West — 4730 Lougheed Highway (Tower 2) (brentwood-park; condos)** — concord-brentwood-hillside-west--brentwood-park-nearby-2026-11-02.md — 3,322 B, **425 words (+25)**.
- Address used: no point for 4730 Lougheed Hwy (all plain results were far-east segments — discarded); origin = the adjacent 4720 Lougheed Hwy point in the same Hillside West complex (condos home file gives Tower 1 at 4720), disclosed in §5/NOT CONFIRMED; header retains the roster's "(Tower 2)" qualifier.
- Measurements (5): walk → Brentwood Town Centre Station 0.48 / 6.4; walk → The Amazing Brentwood 0.52 / 6.9; walk → Save-On-Foods, 4399 Lougheed Hwy 1.02 / 13.6; walk → Brentwood Park Elementary 1.10 / 14.7; drive → Confederation Park 4.33 / 7.0.
- NOT CONFIRMED: catchments; frequencies; building-point geocode; exchange name at Brentwood station.

**101. Escala — 1768–1788 Gilmore Avenue (brentwood-park; condos)** — escala--brentwood-park-nearby-2026-11-02.md — 3,106 B, **422 words (+22)**.
- Address used: roster address RANGE kept as stated; origin = 1768 Gilmore Ave, the low end, geocoded exactly as an OSM apartments point (the 1788 end is the named "Escala" point), disclosed in §5/NOT CONFIRMED; no single civic number invented.
- Measurements (5): walk → Gilmore Station 0.64 / 8.4; walk → Kitchener Elementary 0.84 / 11.2; walk → Brentwood Town Centre Station 0.96 / 12.8; walk → The Amazing Brentwood 1.40 / 18.7; drive → Gilmore Community Elementary 2.01 / 3.8. Discarded (disclosed): walk → Gilmore Community Elementary 1.98 km, over cap.
- NOT CONFIRMED: catchments; frequencies; Gilmore exchange name; no municipal park within ~1 km confirmed (§2 carries Confederation Park flagged outside walking scope).

**102. Milano — 2378 Alpha Avenue (brentwood-park; condos)** — milano--brentwood-park-nearby-2026-11-02.md — 3,109 B, 397 words.
- Address used: roster address geocoded exactly as the named OSM "Milano" building point — no substitution.
- Measurements (5): walk → Brentwood Town Centre Station 0.51 / 6.8; walk → The Amazing Brentwood 0.91 / 12.2; walk → Brentwood Park Elementary 1.49 / 19.9; drive → Alpha Secondary, 930 Alpha Ave 2.04 / 4.3; drive → Confederation Park 2.99 / 6.1.
- NOT CONFIRMED: catchments; frequencies; exchange name; Holy Cross Elementary noted in-area but unmeasured.

**103. Oasis at Concord Brentwood — 4863 Dawson Street (brentwood-park; condos)** — oasis-at-concord-brentwood--brentwood-park-nearby-2026-11-02.md — 3,304 B, **423 words (+23)**. Treated as a normal roster building; no status claims beyond the roster line.
- Address used: no address point for 4863 Dawson St; origin = the OSM named "Concord Brentwood-Oasis" site point, disclosed in §5/NOT CONFIRMED.
- Measurements (5): walk → Brentwood Town Centre Station 0.95 / 12.7; walk → The Amazing Brentwood 1.00 / 13.3; walk → Save-On-Foods 1.49 / 19.9; drive → Brentwood Park Elementary 1.55 / 4.3; drive → Burnaby North Secondary 4.59 / 8.7. Discarded (disclosed): walk → Brentwood Park Elementary 1.58 km, over cap.
- NOT CONFIRMED: catchments; frequencies; building-point geocode; exchange name at Brentwood station.

## Batch flags for the mop-up pass

1. **Entries 85 + 86 (District Flats at Southlands; The Granary at Southlands)** — ADDRESS NOT IN NOTES, skipped this batch; mop-up list is now 52, 85, 86.
2. **Apple Greene (entry 88)** — none of the six roster addresses returns a Nominatim house-number point; measurements rest on a disclosed No. 1 Road segment point in the complex's postal area. Roster addresses not proven wrong (the condos home file states the same set).
3. **Tower 1 (entry 92)** — Nominatim returns two points for 4510 Halifax Way (V5C 3Z6 used; V5C 3Z0 ~600 m west discarded, disclosed). If a later pass re-geocodes this address, expect the duplicate.
4. **Hillside West (entry 100)** — origin is the adjacent 4720 Lougheed Hwy point (same complex, Tower 1 per the condos home file), disclosed; the roster's 4730 address itself has no OSM point.
5. **Brentwood Park pattern** — most Brentwood addresses have no OSM building point; segment-point origins (disclosed) are the norm for this area, and plain Lougheed Highway queries return far-east trunk segments that must be discarded.
