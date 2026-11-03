# What's Nearby — Phase 2, Batch P2-5 Summary

Built Mon Nov 2, 2026. Roster range covered: **entries 104–128 exactly — 25 buildings, no skips, no extension needed** (every entry in 104–128 carries a street address). Skipped problem entries in this range: **none**. Mop-up list carried forward unchanged: **entries 52 (The Hart), 85 (District Flats at Southlands), 86 (The Granary at Southlands)**.

**Batch totals:** 25 files written to `~/workspace/local-notes/nearby/buildings/` (folder now holds 125 files). **145 measurements kept (69 walk, 76 drive)**, all measured 2026-11-02 starting at each building's own address; every walk inside the 4–6 km/h sanity band and the walk ≤1.5 km / drive ≤10 km caps. **HTTP 429s: none** across all five workers (Nominatim / OSRM / routed-foot all paced ~1 req/sec). All five sections + NOT CONFIRMED written in every file — **no section omitted anywhere**.

**Roster lines proved wrong on the ground: none.** No roster address was corrected anywhere; substitutions below are disclosed in-file.

**Correction incident (Worker 2, entries 109–113) — disclosed:** the worker's first Nominatim batch ran long and finished in the background; it drafted its first routing pass before the full output landed, and the belated complete output contradicted several origin points first used (Gilmore Avenue sits west of Brentwood Town Centre station, not east; the Bellwood towers geocode ~700 m south of the first-pass origin; Northview Estates has no named OSM building point at all). The worker re-ran geocodes and routes in a verified foreground pass and rewrote §5 in the four affected files (109, 110, 111, 113) before delivery; entry 112's origin and destinations were read in full in foreground passes and its measurements stand unchanged. The corrected figures below are what is on disk (coordinator spot-checked entries 109 and 113 in full: corrected origins, distances and the segment-origin disclosure are in the files).

## Per-building detail

### brentwood-park (Burnaby)

**104. Oma 1 (OMA) — 2345 Madison Avenue** — oma-1--brentwood-park-nearby-2026-11-02.md — 3,392 B — **462 words (+62 over cap, disclosed)**
- Origin: exact OSM apartments point for 2345 Madison Avenue — but OSM names that point "One Madison Avenue West," differing from the roster name; disclosed in §5/NOT CONFIRMED, roster kept as stated.
- Measurements (7): walk → Gilmore Station 0.79 km/10.5 min; walk → Save-On-Foods (4399 Lougheed Hwy) 0.75/10.0; walk → Whole Foods (4420 Lougheed Hwy) 0.81/10.8; walk → Brentwood Town Centre Station 1.11/14.7; drive → The Amazing Brentwood (4567 Lougheed Hwy) 1.80/4.6; drive → Kitchener Elementary 1.71/4.2; drive → Confederation Park 3.41/7.2. Discarded: walk → Amazing Brentwood 1.73 km (over walk cap).
- NOT CONFIRMED: SD41 catchments (no locator run); bus frequencies; no operator-named exchange at Gilmore Station; OSM-vs-roster building-name difference.

**105. Slate — 2135 Springer Avenue** — slate--brentwood-park-nearby-2026-11-02.md — 3,613 B — **460 words (+60)**
- Origin: disclosed substitution — no Nominatim house-number point for 2135 Springer Ave (named "Slate" query also empty); origin = Springer Avenue segment point in the V5B 2X7 area (the segment calibrated against this address in batch P2-4); times approximate.
- Measurements (6): walk → Holdom Station 0.57/7.6; walk → Holy Cross Elementary 0.84/11.1; walk → Brentwood Park Elementary 0.91/12.1; walk → Brentwood Park 1.12/15.4; drive → Burnaby North Secondary 2.79/5.2; drive → Confederation Park 3.46/5.7.
- NOT CONFIRMED: catchments; frequencies; segment-point geocode; §4 grocery anchors beyond ~1 km (none within ~1 km confirmed from an allowed source); Confederation Park outside ~1 km, carried as nearest City recreation anchor.

**106. Stratus (SOLO District) — 2008 Rosser Avenue** — stratus--brentwood-park-nearby-2026-11-02.md — 3,504 B — **433 words (+33)**
- Origin: exact named OSM "Stratus" building point — no substitution. Title drops the "(SOLO District)" qualifier per the brief's slug rule; header line retains it.
- Measurements (6): walk → Brentwood Town Centre Station 0.31/4.1; walk → Save-On-Foods 0.31/4.1; walk → The Amazing Brentwood 0.94/12.5; walk → Brentwood Park 1.21/16.4; drive → Brentwood Park Elementary 1.74/3.5; drive → Confederation Park 2.81/5.7. Discarded (in NOT CONFIRMED): walk → Whole Foods returned 0.01 km — both points snap to the same routing node beside the building; treated as a routing artifact.
- NOT CONFIRMED: catchments; frequencies; the Whole Foods snap artifact; Confederation Park outside ~1 km.

**107. Tailor — 2425 Alpha Avenue** — tailor--brentwood-park-nearby-2026-11-02.md — 3,430 B — **445 words (+45)**
- Origin: disclosed substitution — no house-number point for 2425 Alpha Ave (named "Tailor" query also empty); origin = the Alpha Avenue segment point in the V5C 5Z9 (Brentwood) area, just north of Milano's exact point at 2378 Alpha Ave (geocoded this pass for calibration); Burnaby Heights Alpha segments returned in the same pass were discarded; times approximate.
- Measurements (6): walk → Brentwood Town Centre Station 0.27/3.6; walk → Whole Foods 0.46/6.1; walk → The Amazing Brentwood 0.69/9.2; walk → Brentwood Park Elementary 1.27/17.0; drive → Alpha Secondary (930 Alpha Ave) 1.79/3.7; drive → Confederation Park 2.74/5.5.
- NOT CONFIRMED: catchments; frequencies; no operator-named exchange at Brentwood Town Centre Station; segment-point geocode.

**108. Triomphe — 1888 Gilmore Avenue** — triomphe--brentwood-park-nearby-2026-11-02.md — 2,965 B — 397 words (under cap)
- Origin: exact OSM apartments point — no substitution.
- Measurements (6): walk → Gilmore Station 0.36/4.7; walk → Kitchener Elementary 0.89/11.8; walk → Brentwood Town Centre Station 1.05/14.0; walk → The Amazing Brentwood 1.50 km (raw 1,498 m, within cap)/20.0; drive → Gilmore Community Elementary (50 S Gilmore Ave) 2.18/4.5; drive → Confederation Park 3.20/6.2.
- NOT CONFIRMED: catchments; frequencies; no operator-named exchange at Gilmore Station; §2 notes no municipal park within ~1 km confirmed from a City page this pass.

**109. Two Gilmore Place (Gilmore Place) — 2108 Gilmore Avenue** — two-gilmore-place--brentwood-park-nearby-2026-11-02.md — 3,062 B — 384 words (under cap) — **§5 corrected in the Worker-2 re-pass (see incident note above)**
- Origin (corrected): Nominatim address point for 2108 Gilmore Avenue, V5C 6P9 area — no substitution.
- Measurements (5, corrected): walk → Gilmore Station 0.17/2.3; walk → Brentwood Town Centre Station 0.94/12.5; walk → Kitchener Elementary 1.12/14.8; drive → Save-On-Foods 0.52/1.1; drive → Confederation Park 3.29/6.0. Discarded: walk → The Amazing Brentwood 1.56 km (over cap).
- NOT CONFIRMED: SD41 catchments; bus frequencies; Gilmore Station exchange name; Brentwood Park Elementary outside the ~1 km walking scope, not measured.

**110. Vantage Point I — 2020 Bellwood Avenue** — vantage-point-i--brentwood-park-nearby-2026-11-02.md — 3,096 B — 380 words — **§5 corrected in the re-pass**
- Origin: exact named Nominatim building point "Vantage Point I, 2020 Bellwood Avenue" (south end of Bellwood Ave).
- Measurements (5, corrected): walk → Holy Cross Elementary 0.81/10.8; walk → Brentwood Park Elementary 0.88/11.7; walk → Brentwood Park 1.10/15.1; drive → Brentwood Town Centre Station 1.60/2.7; drive → Burnaby North Secondary 2.99/5.9.
- NOT CONFIRMED: catchments; frequencies; Confederation Park / Eileen Dailly carried as phase-1 anchors, not measured.

**111. Vantage Point II — 2060 Bellwood Avenue** — vantage-point-ii--brentwood-park-nearby-2026-11-02.md — 3,099 B — 380 words — **§5 corrected in the re-pass**
- Origin: exact named Nominatim building point "Vantage Point II, 2060 Bellwood Avenue."
- Measurements (5, corrected): walk → Holy Cross Elementary 0.95/12.7; walk → Brentwood Park Elementary 1.02/13.7; walk → Brentwood Park 1.24/17.0; drive → Brentwood Town Centre Station 1.78/3.3; drive → Burnaby North Secondary 3.16/6.5.
- NOT CONFIRMED: catchments; frequencies; Confederation Park / Eileen Dailly carried as phase-1 anchors, not measured.

### bridgeport-ri (Richmond)

**112. North Gate Residences (Northgate, by Pakland Homes) — 3033 Shell Road + 10760–10780 Bridgeport Road** — north-gate-residences--bridgeport-ri-nearby-2026-11-02.md — 3,628 B — **490 words (+90)** — unaffected by the Worker-2 re-pass
- Origin: disclosed Shell Road V6X 2W8 segment point (no house-number point exists). Multi-address: header carries both addresses exactly; anchor/title use 3033 Shell Road; choice disclosed in NOT CONFIRMED.
- Measurements (6, all drive): Costco 1.87/3.5; Tait Elementary 1.49/3.4; King George Park 1.85/3.5; Cambie Community Centre 1.99/3.5; Cambie Secondary 2.24/4.2; Bridgeport Station 2.90/4.7. Discarded: walk → Talmey Elementary 1.87 km (over cap).
- NOT CONFIRMED: multi-address anchor choice; building-point geocode; SD38 catchments; frequencies.

**113. Northview Estates (Citimark & Western Construction) — 10311 River Drive** — northview-estates--bridgeport-ri-nearby-2026-11-02.md — 3,905 B — **494 words (+94, driven by the segment-origin disclosure)** — **§5 corrected in the re-pass**
- Origin (corrected): **no house-number or named building point exists for 10311 River Drive** (named query also returned none on re-run). Origin = the easternmost River Drive segment point returned for the exact roster-address query (V6X 1T3 area, the 10311 end of the River Drive strip), disclosed in §5/NOT CONFIRMED; times approximate; far-west segments from the same queries discarded, not used. Roster address not corrected.
- Measurements (6, corrected): walk → Tait Waterfront Park 0.59/8.0; walk → Robert J Tait Elementary 0.91/12.1; drive → Bridgeport Station 1.99/3.2; drive → Costco 2.02/3.7; drive → Talmey Elementary 2.87/5.4; drive → Cambie Secondary 3.15/5.6.
- NOT CONFIRMED: segment-origin geocode; SD38 catchments; frequencies; which Tait Waterfront Park section the single OSM park point belongs to.

**114. Parc Portofino (Dava Developments) — 10333 River Drive** — parc-portofino--bridgeport-ri-nearby-2026-11-02.md — 3,589 B — **442 words (+42)**
- Origin: disclosed substitution — River Drive segment point east of McLennan Ave (49.1971853, −123.1051954), nearest the 10333 block; no building point exists. (River Drive segment origins in this batch were calibrated against fixed anchors — No. 4 Road ≈ −123.115, Tait Elementary −123.1118, McLennan Ave ≈ −123.1078; River Drive numbers rise eastward.)
- Measurements (6): walk → Tait Waterfront Park 0.41/5.6; walk → Robert J Tait Elementary 0.72/9.6; drive → Bridgeport Station 1.80/2.9; drive → Costco (9151 Bridgeport Rd) 2.15/3.8; drive → R.C. Talmey Elementary 3.06/5.7; drive → Cambie Secondary 3.34/5.9.
- NOT CONFIRMED: building-point geocode (roster address not proven wrong); SD38 catchments; frequencies; supermarket anchor (§4 is Costco only); exact nearest individual bus stop.

**115. Parc Riviera — 10033 River Drive** — parc-riviera--bridgeport-ri-nearby-2026-11-02.md — 3,558 B — **441 words (+41)**
- Origin: disclosed substitution — River Drive segment point between No. 4 Road and McLennan Ave (49.1984731, −123.1108854).
- Measurements (6): walk → Tait Waterfront Park 0.25/3.5; walk → Tait Elementary 0.75/10.0; drive → Bridgeport Station 1.35/2.2; drive → Costco 1.70/3.1; drive → Talmey Elementary 2.83/5.6; drive → Cambie Secondary 3.79/6.6.
- NOT CONFIRMED: same five items as 114.

**116. Parc Riviera Mews (Dava Developments) — 10199 and 10233 River Drive** — parc-riviera-mews--bridgeport-ri-nearby-2026-11-02.md — 3,615 B — **446 words (+46)**
- Origin: same disclosed River Drive segment point as 115; anchor = first address 10199 River Drive; header carries both addresses exactly; anchor choice disclosed in NOT CONFIRMED.
- Measurements (4): walk → Tait Waterfront Park 0.25/3.5; walk → Tait Elementary 0.75/10.0; drive → Bridgeport Station 1.35/2.2; drive → Costco 1.70/3.1.
- NOT CONFIRMED: multi-address anchor choice; building-point geocode (none for either address; not proven wrong); catchments; frequencies; supermarket anchor; exact nearest stop.

**117. Parc Riviera – Monaco — 10177 River Drive** — parc-riviera-monaco--bridgeport-ri-nearby-2026-11-02.md — 3,418 B — **415 words (+15)**
- Origin: same disclosed River Drive segment point as 115/116 — 10177 lies on the same No. 4 Rd–McLennan segment.
- Measurements (4): walk → Tait Waterfront Park 0.25/3.5; walk → Tait Elementary 0.75/10.0; drive → Bridgeport Station 1.35/2.2; drive → Costco 1.70/3.1.
- NOT CONFIRMED: same items as 115.

### brighouse (Richmond)

**118. Ascott Wynde — 8751 Citation Drive (also 8880 Cook Road, disclosed-basis)** — ascott-wynde--brighouse-nearby-2026-11-02.md — 4,092 B — **504 words (+104 — largest overage of the batch, driven by 9 measurements + dual-address disclosure; kept rather than cut facts)**
- Origin: exact Nominatim named point "Ascott Wynde" (49.1655, −123.1256122) — no substitution. Title/anchor use 8751 Citation Drive; header carries both addresses; basis disclosed in NOT CONFIRMED.
- Measurements (9): walk → William Cook Elementary (8600 Cook Rd) 0.47/6.2; walk → Garden City Community Park 0.57/7.6; walk → Richmond-Brighouse Station 1.20/16.0; walk → PriceSmart Foods (8200 Ackroyd Rd) 1.37/18.2; drive → CF Richmond Centre 1.55/4.0; drive → T&T Supermarket (8311 Lansdowne Rd) 1.58/3.6; drive → Richmond Secondary 1.69/3.8; drive → Richmond Public Library (Brighouse) 1.74/3.9; drive → Minoru Centre for Active Living 1.85/3.8.
- NOT CONFIRMED: disclosed-basis dual address; SD38 catchments; frequencies; Samuel Brighouse Elementary listed from the Ministry list but not measured.

**119. Flo — 7360 Elmbridge Way (also 6888 Alderbridge Way)** — flo--brighouse-nearby-2026-11-02.md — 2,867 B — 368 words (under cap)
- Origin: exact OSM apartments point for 7360 Elmbridge Way — no substitution. Multi-address anchor (7360) disclosed; header carries both addresses.
- Measurements (7): walk → 7000 Westminster Highway 0.53/7.1; walk → Richmond Olympic Oval (6111 River Rd) 0.71/9.5; walk → Minoru Park 0.81/10.9; walk → Richmond-Brighouse Station 1.07/14.3; drive → Samuel Brighouse Elementary 1.13/2.5; drive → CF Richmond Centre (6551 No. 3 Rd) 1.18/2.5; drive → Walmart Supercentre (9251 Alderbridge Way) 2.26/4.3.
- NOT CONFIRMED: anchor choice; SD38 catchments; frequencies; 7000 Westminster Hwy is a measured point only, no facility fact stated.

**120. The Paramount — 6340 No. 3 Road (towers 6320, 6328 No. 3 Road)** — the-paramount--brighouse-nearby-2026-11-02.md — 3,097 B — **409 words (+9)**
- Origin: disclosed substitution — no OSM house-number point for 6340 No. 3 Road; origin is the OSM landuse point named "The Paramount." The 6320 and 6328 tower addresses geocode exactly as named tower points in the same development (noted in-file). Process note: plain "No. 3 Road" Nominatim queries mis-parse to a fishing pier in south Richmond (49.11°N) — those points were discarded, never used; "Number 3 Road" variants used throughout this worker's pass.
- Measurements (6): walk → Richmond-Brighouse Station 0.30/3.9; walk → CF Richmond Centre 0.41/5.4; walk → Richmond Public Library Brighouse (7700 Minoru Gate) 0.84/11.2; walk → Minoru Park 1.15/15.3; drive → Richmond Secondary (7171 Minoru Blvd) 1.42/3.5; drive → Real Canadian Superstore (4651 No. 3 Rd) 2.00/4.1.
- NOT CONFIRMED: anchor choice; no building-point geocode for 6340; catchments; frequencies.

**121. Quintet Tower A — 7988 Ackroyd Road** — quintet-tower-a--brighouse-nearby-2026-11-02.md — 3,021 B — **407 words (+7)**
- Origin: exact OSM point named "Quintet Tower A, 7988 Ackroyd Road" — no substitution. Nearest station for this building is Lansdowne Station, not Brighouse (measured).
- Measurements (7): walk → Lansdowne Station 0.36/4.8; walk → CF Richmond Centre 0.54/7.2; walk → Lansdowne Centre point (5300 No. 3 Rd) 0.65/8.6; walk → T&T Supermarket (8311 Lansdowne Rd) 0.74/9.9; drive → William Cook Elementary (8600 Cook Rd) 1.34/3.0; drive → Real Canadian Superstore 1.41/3.1; drive → Walmart Supercentre 2.25/4.3.
- NOT CONFIRMED: catchments; frequencies; no operator-named exchange for nearest stops; Lansdowne Centre's address not read on the centre's own site (§5 uses its OSM point as a measured destination only); T&T address rests on a retailer own-domain search result, disclosed in-file.

**122. Regency Park Towers (Park Towers) — 6611 / 6631 / 6651 Minoru Boulevard** — regency-park-towers--brighouse-nearby-2026-11-02.md — 3,085 B — 385 words (under cap)
- Origin: exact OSM point named "Park Towers – Tower C, 6611 Minoru Boulevard" (anchor = first roster address, disclosed); header carries all three addresses.
- Measurements (6): walk → Richmond Public Library Brighouse 0.38/5.0; walk → Minoru Park 0.54/7.2; walk → CF Richmond Centre 0.62/8.3; walk → Minoru Centre for Active Living (7191 Granville Ave) 0.80/10.6; drive → Richmond Secondary 0.95/2.6; drive → Richmond-Brighouse Station 1.46/3.1.
- NOT CONFIRMED: anchor choice; catchments; frequencies; no supermarket within walking radius confirmed on a retailer's own site (§4 centre-only).

**123. River Green — 5199 Brighouse Way** — river-green--brighouse-nearby-2026-11-02.md — 3,185 B — **440 words (+40 — driven by the segment-origin and discarded-walk disclosures)**
- Origin: disclosed segment-point substitution — no OSM house-number point for 5199 Brighouse Way; origin is the Brighouse Way street-segment point in V7C 4V4, on the correct street segment; times approximate. Roster address not proven wrong (condos home file states the same address).
- Measurements (6 kept + 1 discarded): walk → Richmond Olympic Oval (6111 River Rd) 0.43/5.7; walk → 7000 Westminster Highway 1.33/17.8; drive → Minoru Park 1.80/3.4; drive → CF Richmond Centre 2.33/4.7; drive → Richmond-Brighouse Station 2.74/5.5; drive → Spul'u'kwuks Elementary (5999 Blanshard Dr) 2.91/5.2. Discarded and disclosed in-file: walk → Samuel Brighouse Elementary 1.52 km, over the 1.5 km walk cap.
- NOT CONFIRMED: building-point geocode (none exists); catchments; frequencies; no grocery within walking radius confirmed (§4 centre is a drive anchor); 7000 Westminster Hwy is a measured point only.

**124. Seasons — 5028 Kwantlen Street (also 5068 Kwantlen Street)** — seasons--brighouse-nearby-2026-11-02.md — 3,261 B — **403 words (+3)**
- Origin: exact OSM building point "Seasons, 5028 Kwantlen Street" (49.1749, −123.1277). Header carries both addresses; anchor/title use 5028, disclosed in NOT CONFIRMED.
- Measurements (6): walk → Lansdowne Station 0.69/9.1; walk → Lansdowne Centre 0.70/9.3; drive → CF Richmond Centre 1.76/3.9; drive → Garden City Community Park 1.83/4.1; drive → Richmond-Brighouse Station 1.91/4.2; drive → Tomsett Elementary 2.10/4.4.
- NOT CONFIRMED: multi-address anchor choice; SD38 catchments; bus frequencies; walks discarded over cap — Tomsett Elementary 1.75 km, Garden City Community Park 1.63 km (drives given instead); MacNeill Secondary street address not confirmed on a district/Ministry page read this pass.

### british-properties (West Vancouver)

**125. Aerie II at Garden Court — 2575 Garden Court** — aerie-ii-at-garden-court--british-properties-nearby-2026-11-02.md — 3,021 B — 379 words (under cap)
- Origin: disclosed substitution — no house-number point exists; Garden Court street-segment point in V7S 0A2 nearest the 2575 block (49.3514, −123.1476); times approximate.
- Measurements (5): walk → Chartwell Elementary 0.94/12.5; walk → Sentinel Secondary 1.21/16.2; drive → Westcot Elementary 2.27/3.9; drive → Park Royal 3.44/6.1; drive → West Vancouver Community Centre 3.75/5.4.
- NOT CONFIRMED: segment-point geocode; SD45 catchments; route 254 frequency; no District park within the walking radius confirmed on a District page.

**126. Hawksley — 3963 Uplands Way (Uplands / Rodgers Creek)** — hawksley--british-properties-nearby-2026-11-02.md — 3,101 B — 400 words (at cap)
- Origin: exact OSM building point for 3963 Uplands Way (49.3544, −123.1842) — no substitution. Both program home files (condos + townhomes) read; one file produced. §1 uses route 253 (Caulfeild/Park Royal/Vancouver, via Woodgreen Drive) — route 254 does not serve the Uplands pocket.
- Measurements (5, all drive): Chartwell Elementary 6.03/9.0; West Vancouver Community Centre 6.20/8.7; West Bay Elementary 8.34/11.6; Park Royal 8.64/11.6; Cypress Falls Park 9.69/11.4.
- NOT CONFIRMED: SD45 catchments; route 253 frequency; walk → West Bay Elementary 5.42 km discarded over cap (drive given); no grocery/shopping anchor within ~1 km confirmed (Park Royal in §4 is beyond walking radius); Cypress Park Primary street address/grades not confirmed.

**127. Highgrove — 2559 Highgrove Mews / Highgrove Place** — highgrove--british-properties-nearby-2026-11-02.md — 3,260 B — **417 words (+17)**
- Origin: disclosed substitution — header carries the roster address exactly as stated; anchor is the Highgrove Mews street-segment point in V7S 0B3 nearest the 2559 block (49.3507, −123.1498); the Highgrove Place form returned no geocode point. Anchor choice disclosed in NOT CONFIRMED.
- Measurements (3, all drive — both walks in range exceeded the cap): Westcot Elementary 3.76/6.4; West Vancouver Community Centre 4.23/6.3; Park Royal 5.72/7.9.
- NOT CONFIRMED: anchor choice + dual-street roster address; segment-point geocode; SD45 catchments; route 254 frequency; walks discarded over cap — Chartwell Elementary 1.54 km, Sentinel Secondary 1.88 km; no District park within walking radius confirmed.

### brookswood (Langley)

**128. Cedar Creek Estates — 3031 200 St** — cedar-creek-estates--brookswood-nearby-2026-11-02.md — 3,340 B — **429 words (+29)**
- Origin: exact OSM address point for 3031 200 Street, Langley (49.0550, −122.6713) — no substitution. Identified by name/class only in the header per the brief (55-plus manufactured-home park); no age-restriction claims in the file.
- Measurements (6, all drive): Noel Booth Elementary 1.63/2.4; Brookswood Library 2.38/4.0; Buy-Low Foods 2.52/4.2; Alice Brown Elementary 3.24/5.4; George Preston Recreation Centre 3.88/5.9; Langley Centre 6.83/10.0 (destination is a disclosed Logan Avenue street-segment point in the exchange area — no exchange building point exists).
- NOT CONFIRMED: SD35 catchments; bus frequencies; walk → Noel Booth Elementary 1.70 km discarded over cap (drive given); roster name record carried — also documented as Cedar Creek Manufactured Home Park; not Cedar Lane Park, Cedar Crest Estates or Deer Creek Estates.

## Flags carried forward for the mop-up pass

1. **Entries 52, 85, 86** remain the mop-up set (ADDRESS NOT IN NOTES) — untouched by this batch.
2. **River Drive (entries 113–117):** no OSM house-number or named building point exists for any River Drive roster address tried; all five files rest on disclosed segment-point origins (113 corrected in the re-pass; 114–117 calibrated against fixed anchors). Roster addresses not proven wrong.
3. **Entry 104, Oma 1:** OSM names the exact address point "One Madison Avenue West" against the roster's "Oma 1 (OMA)" — carried as stated, flagged in-file.
4. **Entry 120, The Paramount:** plain "No. 3 Road" Nominatim queries mis-parse to a south-Richmond fishing pier — a query-handling caution for later Richmond batches ("Number 3 Road" variants work).
5. Word overages are concentrated in measurement-dense + disclosure-heavy files (largest: Ascott Wynde +104); no cited fact or URL was cut anywhere in the batch.
