# What's Nearby — Phase 2, Batch P2-6 Summary

Produced 2026-11-02 under PHASE2-BRIEF.md. Roster range covered: **entries 129–153 exactly — 25/25 buildings produced, no skips, no extension.** Every entry in 129–153 carries a street address. Mop-up list carried forward unchanged: **entries 52 (The Hart), 85 (District Flats at Southlands), 86 (The Granary at Southlands)**.

Areas: brookswood 2, burke-mountain 10, burnaby-hospital 1, burnaby-lake 1, cambie 11. All five sections + NOT CONFIRMED written in every file — **no sections omitted anywhere**.

**Measurements: 151 kept (66 walk, 85 drive)**, all measured 2026-11-02 starting at each building's own address; every kept walk inside the 4–6 km/h sanity band and the walk ≤1.5 km / drive ≤10 km caps; over-cap routes measured, discarded and disclosed in-file (noted per building below). **HTTP 429s: none** across all five workers (Nominatim, OSRM driving, routed-foot).

**Roster lines proved wrong on the ground: none** — the roster was never silently corrected.

**Two process incidents, both self-caught, corrected before delivery, and disclosed in the affected files:**
1. Worker for entries 129–133 began from a partial/backgrounded geocode summary whose coordinates did not match the full Nominatim output (the P2-5 failure mode). All measurements were re-run from the full verified geocode set; the correct Burke Mountain Mitchell Street sits at ≈ −122.739, not the −122.7657 segment in the partial summary. A service restart wiped its /tmp mid-pass; the routing run was recreated and completed in full.
2. Worker for entries 139–143 routed its first pass from a backgrounded geocode delivery that reported OSM "house points" for four origins that could not be reproduced. Foreground re-runs (multiple, consistent) corrected four files: Secret Ridge's reproducible house point sits ~850 m from the first-used point; OSM carries NO house-number point for 3980 Canada Way, 5122 Canada Way or 4949 Cambie Street (segment/named-building points used, disclosed); 35 Park West's first-pass origin sat ~1.2 km south and its "Langara–49th nearest station" claim was wrong — corrected in-file to Oakridge–41st Avenue Station. Entry 140 (Victoria at Burke Mountain) was verified unchanged across three independent runs. This coordinator spot-checked the corrected files' word counts and §5 structure on disk; the corrected figures are what the files carry.

**Word-cap overages (disclosed; wording trimmed only, no cited fact or URL cut):** 35 Park West 493 (+93), Forester 471 (+71), Culmena 466 (+66), Ballantree 463 (+63), Heartwood 456 (+56), Pineridge 455 (+55), Kentwell 465 (+65), Victoria at Burke Mountain 442 (+42), Savile Row 431 (+31), Fernridge Park 420 (+20), Roxton Avenue rowhomes 420 (+20), Belpark 424 (+24), Cambie Gardens Phase 1 424 (+24), 3980 Canada Way 418 (+18), Secret Ridge 406 (+6), Rocklin on the Creek 403 (+3). The Burke Mountain overages are driven by 5–8 measurements per file plus required geocode-basis disclosures; the Brookswood pair carry disclosure-heavy rural files (no walkable anchors — all measurements are drives).

---

## Per-building detail

### 129. Fernridge Park — 20071 24 Ave (brookswood; 55-plus, manufactured-home park)
- File: fernridge-park--brookswood-nearby-2026-11-02.md — 3,284 B; 420 words — OVER cap (disclosed)
- Origin: OSM Fernridge Park point (no house-number point in Nominatim, disclosed in-file)
- Measurements (6, all drive): Glenwood Elementary 1.99 km / 4.3 min; Brookswood Library 3.94 / 7.1; Buy-Low Foods 4.07 / 7.4; Campbell Valley Regional Park 4.43 / 7.6; Brookswood Secondary 5.10 / 8.5; Langley Centre 8.39 / 13.2 (Logan Ave segment destination, disclosed)
- NOT CONFIRMED: SD35 catchments; bus frequencies; walks over cap discarded (Glenwood 2.23 km, Campbell Valley 3.91 km); no pharmacy/second grocery confirmed

### 130. Pineridge — 2270 196 St (brookswood; 55-plus, manufactured-home park)
- File: pineridge--brookswood-nearby-2026-11-02.md — 3,496 B; 455 words — OVER cap (disclosed)
- Origin: 196 Street Brookswood-Fernridge segment point (no house-number/park point in Nominatim, disclosed)
- Measurements (6, all drive): Glenwood Elementary 2.96 km / 4.8 min; Brookswood Library 3.83 / 6.2; Buy-Low Foods 3.96 / 6.5; Campbell Valley Regional Park 5.12 / 7.7; George Preston Recreation Centre 5.32 / 8.1; Langley Centre 8.28 / 12.3 (Logan Ave segment destination, disclosed)
- NOT CONFIRMED: SD35 catchments; bus frequencies; walks over cap discarded (Glenwood 3.21 km, Campbell Valley 4.60 km); roster alias (Pine Ridge Park / Pineridge Estates, one park counted once) carried in-file; no pharmacy/second grocery confirmed

### 131. Ballantree (Polygon Homes) — 1350 Mitchell Street (burke-mountain; townhomes)
- File: ballantree--burke-mountain-nearby-2026-11-02.md — 3,691 B; 463 words — OVER cap (disclosed)
- Origin: Burke Mountain Mitchell Street segment point (49.2936, −122.7388; no house-number point; a same-named street segment elsewhere in Coquitlam was returned and discarded, disclosed)
- Measurements (6): walk Coast Salish Elementary 0.83 km / 11.1 min; walk Smiling Creek Elementary/Park 1.27 / 16.9; drive Queenston Park 1.53 / 2.5; drive Burke Mountain Pioneer Park 2.20 / 3.6; drive Coquitlam Centre 6.00 / 9.0; drive Coquitlam Central Station 6.47 / 9.4
- NOT CONFIRMED: SD43 catchments; bus frequencies; walk to Queenston Park 1.52 km over cap, discarded; no Burke Mountain supermarket confirmed open

### 132. Culmena (Tangerine Developments) — 1292 Rosenburg Way (burke-mountain; townhomes)
- File: culmena--burke-mountain-nearby-2026-11-02.md — 3,682 B; 466 words — OVER cap (disclosed)
- Origin: Rosenburg Way segment point (49.2901, −122.7382; no house-number point; a David Avenue segment returned for the civic query was discarded as the wrong segment, disclosed)
- Measurements (6): walk Coast Salish Elementary 1.29 km / 17.2 min; drive Queenston Park 2.00 / 3.5; drive Smiling Creek Elementary/Park 2.03 / 3.9; drive Burke Mountain Pioneer Park 2.68 / 4.7; drive Coquitlam Centre 6.32 / 9.7; drive Coquitlam Central Station 6.80 / 10.1
- NOT CONFIRMED: SD43 catchments; bus frequencies; walks over cap discarded (Smiling Creek Park 1.65 km, Queenston Park 1.90 km); no Burke Mountain supermarket confirmed open

### 133. Forester at Burke Mountain (Townline) — 1290 Mitchell Street (burke-mountain; townhomes)
- File: forester-at-burke-mountain--burke-mountain-nearby-2026-11-02.md — 3,737 B; 471 words — OVER cap (disclosed)
- Origin: Burke Mountain Mitchell Street segment point (49.2909, −122.7393; no house-number point; same-named street discard disclosed)
- Measurements (6): walk Coast Salish Elementary 1.15 km / 15.3 min; drive Queenston Park 1.85 / 2.9; drive Smiling Creek Elementary/Park 1.87 / 3.4; drive Burke Mountain Pioneer Park 2.52 / 4.1; drive Coquitlam Centre 6.03 / 9.3; drive Coquitlam Central Station 6.50 / 9.7
- NOT CONFIRMED: SD43 catchments; bus frequencies; walks over cap discarded (Smiling Creek Park 1.51 km, Queenston Park 1.76 km); no Burke Mountain supermarket confirmed open

### 134. Heartwood (StreetSide Developments, Qualico) — 3535 Highland Drive (burke-mountain; townhomes)
- File: heartwood--burke-mountain-nearby-2026-11-02.md — 3,814 B; 456 words — OVER cap (disclosed)
- Origin: Nominatim road point on Highland Drive (no house-number point)
- Measurements (8): walk Burke Mountain Pioneer Park 0.48 km / 6.4 min; walk Queenston Park 0.59 / 7.9; walk Smiling Creek Elementary 0.78 / 10.4; walk Galloway Park 0.87 / 11.6; drive Minnekhada Middle 3.65 / 5.4; drive Save-On-Foods Sunwood 5.26 / 7.4; drive Coquitlam Centre 5.28 / 8.0; drive Coquitlam Central Station 5.76 / 8.4
- NOT CONFIRMED: SD43 catchments; bus frequencies (not on timetables read); roster note — units also listed under Harper Road, measurements anchored at 3535 Highland Drive; Burke Mountain Village grocery anticipated, not confirmed open; library time not measured
- Source note: Save-On-Foods Sunwood address rests on the retailer's own-domain media release (its store page renders no address in text) — labelled in-file

### 135. Kentwell (Polygon Kentwell Homes Ltd.) — 3500 Burke Village Promenade (burke-mountain; townhomes)
- File: kentwell--burke-mountain-nearby-2026-11-02.md — 3,827 B; 465 words — OVER cap (disclosed)
- Geocode substitution disclosed in-file: the first Nominatim result landed on an eastern segment of Burke Village Promenade (~800 m off) and was discarded; the point used is the Burke Mountain segment result, corroborated by the exact 3458 Burke Village Promenade point (Secret Ridge) ~60 m away
- Measurements (8): walk Riley Park 0.42 km / 5.7 min; walk Sheffield Park 1.02 / 13.6; walk Galloway Park 1.09 / 14.5; walk Coast Salish Elementary 1.19 / 15.8; walk Smiling Creek Elementary 1.33 / 17.7; drive Minnekhada Middle 3.43 / 5.7; drive Save-On-Foods Sunwood 5.52 / 7.9; drive Coquitlam Central Station 6.01 / 8.9
- NOT CONFIRMED: catchments; frequencies; village grocery; library time

### 136. Reef — 1219 Burke Mountain Street (burke-mountain; townhomes)
- File: reef--burke-mountain-nearby-2026-11-02.md — 3,116 B; 387 words — within cap
- Origin: Nominatim road point on Burke Mountain Street
- Measurements (7): walk Victoria Park 0.38 km / 5.1 min; walk Leigh Elementary 0.54 / 7.2; drive Smiling Creek Elementary 2.50 / 4.8; drive Minnekhada Middle 2.83 / 5.0; drive Terry Fox Secondary 3.83 / 6.2; drive Save-On-Foods Sunwood 5.72 / 8.4; drive Coquitlam Central Station 6.30 / 9.6
- NOT CONFIRMED: catchments; frequencies; Galloway Park walk measured 1.53 km — over cap, excluded from §5; village grocery; library time

### 137. Rocklin on the Creek (Woodbridge Homes) — 1220 Rocklin Street (burke-mountain; townhomes)
- File: rocklin-on-the-creek--burke-mountain-nearby-2026-11-02.md — 3,334 B; 403 words — marginally OVER cap (disclosed)
- Origin: Nominatim road point on Rocklin Street
- Measurements (5): walk Riley Park 1.33 km / 17.7 min; drive Minnekhada Middle 4.29 / 7.1; drive Save-On-Foods Sunwood 6.38 / 9.3; drive Coquitlam Centre 6.41 / 9.9; drive Coquitlam Central Station 6.88 / 10.3
- NOT CONFIRMED: catchments; frequencies; roster note — units also listed under 1225 Mitchell Street, anchored at 1220 Rocklin Street; walks to Coast Salish Elementary (1.51 km) and Sheffield Park (1.57 km) over cap, excluded; village grocery; library time
- Note: worker routed 43 pairs in its group; 4 drives measured but not published to hold word count (group-level note)

### 138. Roxton Avenue rowhomes — 3406 / 3416 Roxton Avenue (burke-mountain; townhomes) — MULTI-ADDRESS
- File: roxton-avenue-rowhomes--burke-mountain-nearby-2026-11-02.md — 3,334 B; 420 words — OVER cap (disclosed)
- Title/anchor use the FIRST address (3406 Roxton Avenue); header carries both addresses exactly as roster states; anchor choice disclosed in NOT CONFIRMED
- Origin: Nominatim road point on Roxton Avenue
- Measurements (7): walk Leigh Elementary 0.39 km / 5.2 min; walk Victoria Park 0.58 / 7.7; walk Galloway Park 1.12 / 14.9; drive Minnekhada Middle 2.71 / 4.7; drive Terry Fox Secondary 3.71 / 5.9; drive Save-On-Foods Sunwood 5.18 / 7.8; drive Coquitlam Central Station 5.67 / 8.8
- NOT CONFIRMED: multi-address anchor disclosure; catchments; frequencies; Smiling Creek Elementary walk measured 1.68 km — over cap, excluded; village grocery; library time
- Geocode hygiene (group): wrong-segment address points for Sheffield Park, Galloway Park and Victoria Park were discarded in favour of Nominatim named-place points matching the City/Tourism addresses

### 139. Secret Ridge — 3458 Burke Village Promenade (burke-mountain; townhomes) — CORRECTED FILE
- File: secret-ridge--burke-mountain-nearby-2026-11-02.md — 2,994 B; 406 words — OVER cap (disclosed)
- Origin: verified OSM house point for 3458 Burke Village Promenade (beside Kentwell at 3500, corroborating). The first-pass origin sat ~850 m away — all §5 measurements re-run; correction disclosed in-file
- Measurements (4): walk Coast Salish Elementary 1.23 km / 16.5 min; drive Burke Mountain Pioneer Park 2.21 / 3.5; drive Coquitlam Centre 5.70 / 7.9; drive Coquitlam Central Station 5.98 / 8.8
- NOT CONFIRMED: SD43 catchments; bus frequencies; second roster address 3451 Burke Village (anchor 3458 only); village grocery not confirmed open
- Discarded (over walk cap, disclosed in-file): Smiling Creek Elementary walk 1.59 km; Smiling Creek Park walk 1.62 km

### 140. Victoria at Burke Mountain (Mosaic) — 1221 Rocklin Street (burke-mountain; townhomes)
- File: victoria-at-burke-mountain--burke-mountain-nearby-2026-11-02.md — 3,080 B; 442 words — OVER cap (disclosed)
- Origin: Rocklin Street segment point for 1221 Rocklin Street, returned identically by three independent runs — verified, no correction needed; disclosed in-file. Roster note address 3552 Victoria Drive not used as anchor
- Measurements (5, all drive): Coast Salish Elementary 1.71 km / 3.2 min; Victoria Park 2.01 / 3.1; Leigh Elementary 1.97 / 3.3; Coquitlam Centre 6.60 / 9.3; Coquitlam Central Station 6.88 / 10.3
- NOT CONFIRMED: catchments; frequencies; discarded walks 1.51 / 1.58 / 1.62 km disclosed in-file

### 141. 3980 Canada Way — 3980 Canada Way (burnaby-hospital; townhomes; UNNAMED IN NOTES) — CORRECTED FILE
- File: 3980-canada-way--burnaby-hospital-nearby-2026-11-02.md — 3,142 B; 418 words — OVER cap (disclosed)
- Origin: Nominatim's Canada Way segment point for the Deer Lake stretch, V5G 1M2 — OSM carries NO house-number point for this address (the first delivery's "house point" does not exist in OSM); basis stated in §5 and NOT CONFIRMED
- Measurements (6): walk Burnaby Central Secondary 0.47 km / 6.3 min; walk Deer Lake Park 0.57 / 7.5; walk Douglas Road Elementary 1.05 / 14.0; drive Sperling–Burnaby Lake Station 2.87 / 5.1; drive Metropolis at Metrotown 4.97 / 8.6; drive Patterson Station 5.35 / 8.4
- NOT CONFIRMED: SD41 catchments; bus frequencies; no bus-exchange name; UNNAMED IN NOTES (address as name); origin-point basis. Save-On-Foods 4469 Kingsway cited as the retailer's own-domain search result, disclosed in-file

### 142. Savile Row — 5122–5152 Canada Way (burnaby-lake; townhomes) — CORRECTED FILE
- File: savile-row--burnaby-lake-nearby-2026-11-02.md — 3,332 B; 431 words — OVER cap (disclosed)
- Origin: 5122 Canada Way low end of the roster range, on Nominatim's Canada Way segment point for the Deer Lake stretch, V5G 2J3 — no OSM house point exists; basis stated in §5 and NOT CONFIRMED
- Measurements (5): walk Deer Lake Park 0.30 km / 4.0 min; walk Burnaby Central Secondary 0.84 / 11.2; drive Sperling–Burnaby Lake Station 2.66 / 5.2; drive Bonsor Recreation Complex 4.64 / 7.6; drive Metropolis at Metrotown 5.14 / 8.7
- NOT CONFIRMED: SD41 catchments; bus frequencies; range-anchor + segment-point basis; no bus-exchange name. Discarded (disclosed in-file): Bill Copeland Sports Centre walk 1.58 km

### 143. 35 Park West — 4949 Cambie Street (Phase 1) and 5077 Cambie Street (cambie; condos) — MULTI-ADDRESS, CORRECTED FILE
- File: 35-park-west--cambie-nearby-2026-11-02.md — 3,561 B; 493 words — OVER cap (disclosed; largest in batch — 8 measurements + dual-address + corrected-origin disclosures)
- Origin: OSM building point named "35 Park West", 5033 Cambie Street (~W 35th Ave frontage; consistent with the condos home file's West 29th–35th Ave QE Park rise placement and the 5077 Cambie Street house point ~50 m away). 4949 Cambie Street has NO OSM house point. Title still uses 4949 Cambie Street; header carries both roster addresses; basis disclosed in §5 and NOT CONFIRMED. The first-pass origin sat at W 49th Avenue (~1.2 km south) — corrected; the original §1 claim that Langara–49th was the nearest station was wrong and has been corrected in-file: Oakridge–41st Avenue Station is nearest
- Measurements (8): walk Oakridge–41st Avenue Station 0.82 km / 11.0 min; walk Queen Elizabeth Park 0.84 / 11.1; walk Oakridge Park 0.96 / 12.8; walk Hillcrest Centre 1.33 / 17.8; drive Langara–49th Avenue Station 1.82 / 3.8; drive Dr Annie B Jamieson Elementary 2.19 / 4.4; drive Sir William Osler Elementary 2.44 / 5.1; drive Sir Winston Churchill Secondary 3.17 / 5.9
- NOT CONFIRMED: SD39 catchments; bus frequencies; anchor basis (above); Oakridge Park street address not read on the centre's own site; no bus-exchange name. Walk to Dr Annie B Jamieson Elementary 1.77 km discarded (over cap, disclosed)

### 144. Aperture — 759 West 41st Avenue (cambie; townhomes)
- File: aperture--cambie-nearby-2026-11-02.md — 2,962 B; 383 words — within cap
- Origin: Nominatim house-number point for the roster address, no substitution
- Measurements (7): walk Oakridge–41st Avenue Station 0.59 km / 8.0 min; walk Tisdall Park 1.11 / 14.8; walk Osler Elementary 1.20 / 15.9; walk Van Horne Elementary 1.42 / 19.0; drive Oakridge Park 0.84 / 1.8; drive Hillcrest Centre 2.75 / 5.2; drive Queen Elizabeth Park 3.27 / 7.6
- NOT CONFIRMED: catchments (no locator run); bus frequencies not read; Route R4 not confirmed; walks to QE Park (1.71 km) and Hillcrest (2.21 km) over the walk cap — drive times given instead

### 145. Belpark by Intracorp — 375 West 59th Avenue (also 389 West 59th Avenue and 7428 Alberta Street) (cambie; condos) — MULTI-ADDRESS
- File: belpark-by-intracorp--cambie-nearby-2026-11-02.md — 3,294 B; 424 words — OVER cap (disclosed)
- Geocode substitution disclosed in-file: title/header use the first roster address (375 West 59th Avenue; header carries all three addresses), but Nominatim has NO house-number point for 375 West 59th Avenue — it returned only street-segment points on other parts of West 59th Avenue (Kerrisdale/Oak St area), discarded as wrong-segment. Measurements therefore start at **7428 Alberta Street**, another roster address for the same building (valid Nominatim house-number point)
- Measurements (7): walk Winona Park 0.23 km / 3.1 min; walk J.W. Sexsmith Elementary 0.38 / 5.0; walk Marine Drive Station 1.24 / 16.6; walk Marpole-Oakridge Community Centre 1.31 / 17.8; drive T&T Supermarket (Marine Gateway) 1.14 / 2.3; drive Churchill Secondary 1.24 / 2.7; drive Langara Golf Course 2.46 / 6.5
- NOT CONFIRMED: measurement anchor disclosure (above); catchments; frequencies; walk to Langara Golf Course 1.92 km over cap — drive given

### 146. Cambie Gardens, Phase 1 (East Tower) — 7433 Cambie Street and 7418 Paulson Street (cambie; condos) — MULTI-ADDRESS
- File: cambie-gardens-phase-1--cambie-nearby-2026-11-02.md — 3,338 B; 424 words — OVER cap (disclosed)
- Anchor: first roster address 7433 Cambie Street (Nominatim East Tower point); 7418 Paulson Street not used as anchor — disclosed in-file
- Measurements (8): walk Winona Park 0.58 km / 7.8 min; walk Sexsmith Elementary 0.76 / 10.2; walk Churchill Secondary 0.92 / 12.3; walk Marpole-Oakridge CC 1.02 / 14.0; walk Marine Drive Station 1.13 / 15.0; drive T&T Supermarket 0.97 / 1.8; drive Safeway Marpole (8475 Granville St) 2.82 / 5.1; drive Langara Golf Course 2.43 / 6.3
- NOT CONFIRMED: anchor disclosure; catchments; frequencies; walk to Langara Golf Course 1.73 km over cap — drive given
- Source note: Safeway Marpole's own store page gives **8475 Granville Street** (not 8555, which is the residential building above it); the geocoded point used sits on the same block (~5 m difference)

### 147. The Camellia — 6733 Cambie Street (townhouse address 6723 Cambie Street) (cambie; condos) — MULTI-ADDRESS
- File: the-camellia--cambie-nearby-2026-11-02.md — 2,924 B; 386 words — within cap
- Anchor: 6733 Cambie Street; townhouse address 6723 Cambie Street not used — disclosed in-file
- Measurements (5): walk Langara–49th Avenue Station 0.31 km / 4.1 min; walk Tisdall Park 0.47 / 6.3; walk Churchill Secondary 1.02 / 13.7; walk Langara Golf Course 1.48 / 19.8; drive Oakridge Park 1.39 / 3.0
- NOT CONFIRMED: anchor disclosure; catchments; frequencies; walks to Osler Elementary (1.86 km) and Marine Drive Station (1.78 km) over cap, no walk times stated; Langara–49th Avenue Station named from TransLink's route 49 timetable (no TransLink station page read this pass) — stated in-file

### 148. The Charlotte by Nobleland Developments — 5118 Cambie Street (cambie; condos)
- File: the-charlotte--cambie-nearby-2026-11-02.md — 2,776 B; 356 words — within cap
- Origin: Nominatim house-number point for the roster address, no substitution
- Measurements (6): walk Oakridge–41st Avenue Station 0.75 km / 10.0 min; walk Queen Elizabeth Park 0.86 / 11.4; walk Hillcrest Centre 1.41 / 18.8; walk Van Horne Elementary 1.48 / 19.8; drive Oakridge Park 0.96 / 1.9; drive Churchill Secondary 3.16 / 5.8
- NOT CONFIRMED: catchments; frequencies; Route R4 not confirmed; walk to Churchill 2.73 km over cap — drive given
- Geocode hygiene (group): first-pass Nominatim segment points for J.W. Sexsmith Elementary (7455 Ontario St query) and David Lloyd George Elementary were discarded and replaced with school-name geocodes; Sexsmith is cited at its current address, 7410 Columbia Street, matching the school-name geocode point used for its measurements

### 149. Chelsea by Cressey — 4675 Cambie Street and 4685 Cambie Street (cambie; condos) — MULTI-ADDRESS
- File: chelsea--cambie-nearby-2026-11-02.md — 3,008 B; 385 words — within cap
- Anchor: first roster address 4675 Cambie Street (origin resolved directly); header carries both addresses; anchor choice disclosed in NOT CONFIRMED
- Measurements (6): walk Queen Elizabeth Park 0.72 km / 10.2 min; walk King Edward Station 0.74 / 9.9; walk Hillcrest Centre (4575 Clancy Loranger Way) 1.03 / 13.8; walk Edith Cavell Elementary (500 20th Ave W) 1.21 / 16.1; drive Oakridge Park (650 West 41st Ave) 1.52 / 2.7; drive VanDusen Botanical Garden (5251 Oak St) 1.37 / 2.9
- NOT CONFIRMED: multi-address anchor disclosure; school catchments (no locator run); bus frequencies; Eric Hamber Secondary geocode discarded — Nominatim returned a West 33rd Avenue segment point at −123.1545, west of the school site, discarded as wrong-segment; Hamber is listed in §3 from the Ministry list but no travel time to it is stated
- Sources: TransLink station pages (Oakridge–41st, King Edward, Langara–49th) opened and verified in this pass; Safeway Oakridge via the retailer's own-domain store page found as a search result, disclosed in-file as such

### 150. Claridge House by Polygon — 485 West 42nd Avenue (cambie; condos)
- File: claridge-house--cambie-nearby-2026-11-02.md — 2,880 B; 362 words — within cap
- Origin: resolved directly to the roster address; no substitutions
- Measurements (6): walk Oakridge–41st Avenue Station 0.20 km / 2.6 min; walk Oakridge Park 0.21 / 2.9; walk Sir Wm Van Horne Elementary 0.83 / 11.1; walk Dr Annie B Jamieson Elementary 1.02 / 13.6; drive Sir Winston Churchill Secondary 2.65 / 5.0; drive Queen Elizabeth Park 2.81 / 6.6
- NOT CONFIRMED: school catchments; bus frequencies; Route R4 41st Ave (timetable not read on a TransLink page)

### 151. Forty Nine West — 6383 Cambie Street (cambie; condos)
- File: forty-nine-west--cambie-nearby-2026-11-02.md — 2,698 B; 335 words — within cap
- Origin: resolved directly; no substitutions. §2 uses Tisdall Park, 6210 Tisdall St (Park Board Park Finder)
- Measurements (4): walk Langara–49th Avenue Station 0.17 km / 2.2 min; walk Dr Annie B Jamieson Elementary 0.68 / 9.0; drive Oakridge Park 1.41 / 2.7; drive Sir Winston Churchill Secondary 1.70 / 3.1
- NOT CONFIRMED: school catchments; bus frequencies; walk to Sir William Osler Elementary measured 1.59 km — over the walk cap, so no walk time stated

### 152. Lina at QE Park — 5212 Cambie Street (cambie; condos)
- File: lina-at-qe-park--cambie-nearby-2026-11-02.md — 2,763 B; 343 words — within cap
- Origin: resolved directly; no substitutions
- Measurements (5): walk Oakridge–41st Avenue Station 0.74 km / 9.9 min; walk Queen Elizabeth Park 0.89 / 11.9; walk Sir Wm Van Horne Elementary 1.40 / 18.6; drive Hillcrest Centre 1.64 / 3.5; drive Sir Winston Churchill Secondary 3.24 / 6.2
- NOT CONFIRMED: school catchments; bus frequencies; Route R4 41st Ave

### 153. Livingstone House (Livingstone by Intracorp) — 5115 Cambie Street (cambie; condos)
- File: livingstone-house--cambie-nearby-2026-11-02.md — 2,736 B; 329 words — within cap
- Origin: resolved directly; no substitutions
- Measurements (4): walk Oakridge–41st Avenue Station 0.71 km / 9.6 min; walk Queen Elizabeth Park 0.93 / 12.4; walk Hillcrest Centre 1.47 / 19.7; drive Sir Winston Churchill Secondary 3.12 / 5.6
- NOT CONFIRMED: school catchments; bus frequencies; Route R4 41st Ave

---

## Batch totals

- Files: 25 (buildings folder now holds 150: batches 1–6)
- Measurements kept: **151 (66 walk, 85 drive)** — tallied from the per-file lists above (the 139–143 worker's own group tally said 29; its per-file corrected lists enumerate 28, and 28 is what is carried here)
- 429s: **none**
- Skipped entries: **none in range** (mop-up list unchanged: 52, 85, 86)
- Roster lines proved wrong on the ground: **none**
- Sections omitted: **none** (all 25 files carry §§1–5 + NOT CONFIRMED)
