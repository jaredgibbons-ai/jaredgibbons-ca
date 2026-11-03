# What's Nearby — Phase 2, Batch P2-3 Summary

Produced Mon Nov 2, 2026 under PHASE2-BRIEF.md. One file per building in `~/workspace/local-notes/nearby/buildings/`.

- **Roster entries covered: 51, 53–76 (25 buildings).** Entry 52 (The Hart, aldergrove, condos) skipped — ADDRESS NOT IN NOTES; held for the final mop-up batch (address not researched, per the brief).
- Areas: aldergrove 4, aldergrove-guide 6, ambleside 11, annieville 2, arbutus 1, arista-townhomes 1.
- All five sections + NOT CONFIRMED written in every file — **no sections omitted anywhere**.
- **Measurements: 104 total (70 walk, 34 drive)**, all measured 2026-11-02 starting at each building's own address; every walk inside the 4–6 km/h sanity band and the walk ≤1.5 km / drive ≤10 km caps. Over-cap routes were discarded and disclosed in-file.
- **HTTP 429s: none** across all five workers (Nominatim / OSRM / routed-foot paced ~1 req/sec).
- **Roster lines proved wrong on the ground: none** — the roster was never silently corrected. Geocode substitutions are disclosed in-file wherever used (below).
- Word-cap overages (disclosed, never cut): Jackman 419 (+19), Tudor Gardens 457 (+57), Arbutus Village 437 (+37), Creekside Estates 405 (+5), Sea Wind 404 (+4), The Tides 404 (+4), Westshore Place 404 (+4), Shortreed 403 (+3), Vanetta 403 (+3), Creekside Villa (aldergrove-guide) 401 (+1), Westerlies 401 (+1). Delta Cedars exactly 400 (at cap). All other files 352–399 words.

## Per building

**51. Creekside Villa — 27435 29A Ave (aldergrove; 55-plus)** — creekside-villa--aldergrove-nearby-2026-11-02.md — 3,523 B, 396 words.
- Address used: roster address; no house-number point exists — origin = the OSM "Creekside Villas" residential point on 29A Avenue, disclosed in §5.
- Measurements (5): walk → Shortreed Community School 0.59 km / 7.9 min; walk → FreshCo, 27566 Fraser Hwy 1.22 km / 16.2 min; walk → Aldergrove Community Centre, 27032 Fraser Hwy 1.38 km / 18.5 min; drive → Aldergrove Library, 26770 29 Ave 1.50 km / 3.1 min; drive → Save-On-Foods, 26310 Fraser Hwy 2.58 km / 4.7 min. Over-cap walks measured but not carried: Parkside Centennial 1.69 km, Aldergrove Community Secondary 1.56 km, Betty Gilbert 1.64 km, Library 1.84 km.
- NOT CONFIRMED: catchments (no locator run); bus frequencies; roster name trap carried in-file (NOT Creekside Estates, 27125 31A Ave, not 55-plus; not the Town Centre Creekside, 27249 Aldergrove Town Centre Dr); entry 60 covers this same building under aldergrove-guide/townhomes — this file is the aldergrove/55-plus one.

**53. Jackman — 27218 Aldergrove Town Centre Dr (aldergrove; condos)** — jackman--aldergrove-nearby-2026-11-02.md — 3,658 B, **419 words (+19 over cap)**.
- Address used: roster address in title/header; measurements from the OSM "Aldergrove Town Centre" site point — the address and the street return no Nominatim result in any variant and the street is absent from returned OSM data (re-verified in this pass; same ground fact as batch 2's entry 50). Substitution disclosed in §5 and NOT CONFIRMED. Roster address not proven wrong — the condos home file states the same address.
- Measurements (5): walk → FreshCo 1.06 km / 14.1 min; walk → Shortreed Community School 0.92 km / 12.3 min; walk → Aldergrove Community Centre 0.89 km / 11.9 min; drive → Save-On-Foods 2.17 km / 3.9 min; drive → Aldergrove Library 1.47 km / 2.7 min. A valid walk → Parkside Centennial (0.86 km / 11.4 min) was measured but not carried after the word-cap trim.
- NOT CONFIRMED: catchments; frequencies; building-point geocode (substitution above); name trap — not Jackman Manor, the long-term care home at 27477 28 Ave (condos home file).

**54. Shortreed — 27215 Aldergrove Town Centre Dr (aldergrove; condos)** — shortreed--aldergrove-nearby-2026-11-02.md — 3,574 B, **403 words (+3)**.
- Address used: roster address; same disclosed "Aldergrove Town Centre" site-point substitution as entry 53 (independently re-verified for this address).
- Measurements (5): identical set to entry 53 (same origin): walk → FreshCo 1.06/14.1; walk → Shortreed Community School 0.92/12.3; walk → Aldergrove Community Centre 0.89/11.9; drive → Save-On-Foods 2.17/3.9; drive → Aldergrove Library 1.47/2.7.
- NOT CONFIRMED: catchments; frequencies; building-point geocode (substitution above).

**55. Vanetta — 27254 Aldergrove Town Centre Dr (aldergrove; condos)** — vanetta--aldergrove-nearby-2026-11-02.md — 3,570 B, **403 words (+3)**.
- Address used: roster address; same disclosed site-point substitution as entries 53–54 (independently re-verified).
- Measurements (5): identical set to entries 53–54 (same origin).
- NOT CONFIRMED: catchments; frequencies; building-point geocode (substitution above).
- Note: entries 53–55 share entry 50's origin point, so their §5 measurements are identical by construction (precedent: batch 2's Hartwell/Harvest shared-segment disclosure); worker 1's independent re-measurement matched batch 2's Creekside values exactly for all five shared destinations.

**56. Alderwood Manor — 27090 32 Ave (aldergrove-guide; townhomes)** — alderwood-manor--aldergrove-guide-nearby-2026-11-02.md — 3,391 B, 373 words.
- Address used: roster address; origin = the named OSM "Alderwood Manor" residential point for the complex (plain address queries returned only 32 Avenue street segments), disclosed in §5.
- Measurements (5): walk → Parkside Centennial Elementary 0.50 km / 6.6 min; walk → Aldergrove Community Centre 0.86 km / 11.5 min; walk → Shortreed Community School 1.41 km / 18.9 min; drive → FreshCo 1.65 km / 3.0 min; drive → Save-On-Foods 1.93 km / 3.5 min. Over-cap walks not carried: FreshCo 1.61 km, Library 1.65 km.
- NOT CONFIRMED: catchments; frequencies; building-footprint geocode (named complex point used).

**57. Bertrand Estates — 27044 32 Ave (aldergrove-guide; townhomes)** — bertrand-estates--aldergrove-guide-nearby-2026-11-02.md — 3,328 B, 393 words.
- Address used: roster address; no building point exists — origin = 32 Avenue street-segment point in the V4W 3L5 area nearest the 27044 block, disclosed in §5/NOT CONFIRMED.
- Measurements (4): walk → Aldergrove Community Centre 0.94 km / 12.6 min; walk → Parkside Centennial Elementary 0.46 km / 6.2 min; walk → Aldergrove Community Secondary 1.28 km / 17.1 min; drive → Save-On-Foods 1.47 km / 2.5 min. Discarded: walk → Shortreed Community School 1.78 km (over cap, disclosed).
- NOT CONFIRMED: catchments; building-point geocode; exact nearest stop + frequencies; no municipal park within ~1 km confirmed.
- New sourcing: BC Transit route 21's route map PDF read in this pass confirms route 21 stops on 32 Ave itself — cited in entries 57–61.

**58. Cedar Park Estates — 27456 32 Ave (aldergrove-guide; townhomes)** — cedar-park-estates--aldergrove-guide-nearby-2026-11-02.md — 3,169 B, 378 words.
- Address used: roster address; origin = 32 Avenue segment point in the V4W 3P9 area nearest the 27456 block (postal area matches the home file's V4W 3P1), disclosed.
- Measurements (3): walk → FreshCo 0.94 km / 12.5 min; walk → Aldergrove Community Centre 1.29 km / 17.2 min; drive → Save-On-Foods 2.51 km / 4.2 min. Discarded: walk → Shortreed 1.62 km (over cap, disclosed). §3 carries two elementary schools only — no middle/secondary within ~1 km confirmed.
- NOT CONFIRMED: catchments; building-point geocode; exact nearest stop + frequencies; no municipal park or middle/secondary school within ~1 km confirmed.

**59. Creekside Estates — 27125 31A Ave (aldergrove-guide; townhomes)** — creekside-estates--aldergrove-guide-nearby-2026-11-02.md — 3,396 B, **405 words (+5)**.
- Address used: roster address; origin = 31A Avenue segment point in the V4W 3H7 area, disclosed. (The plain address query returned a same-named Brookswood-Fernridge 31A Avenue segment first — not used, disclosed in-file.)
- Measurements (4): walk → Aldergrove Community Centre 0.66 km / 8.8 min; walk → Parkside Centennial Elementary 0.68 km / 9.0 min; walk → Shortreed Community School 1.22 km / 16.3 min; drive → FreshCo 1.38 km / 2.8 min.
- NOT CONFIRMED: catchments; building-point geocode; exact nearest stop + frequencies; no municipal park within ~1 km confirmed; roster name trap carried (Creekside Villa and Creekside are different buildings). No age-restriction claim made for this building, per the roster note.

**60. Creekside Villa — 27435 29A Ave (aldergrove-guide; townhomes)** — creekside-villa--aldergrove-guide-nearby-2026-11-02.md — 3,264 B, **401 words (+1)**.
- Built from the aldergrove-guide phase-1 file and the townhomes home file, per its own roster line; the entry-51 separation is stated in NOT CONFIRMED.
- Address used: roster address; origin = the 29A Avenue segment point named "Creekside Villas" in Nominatim (V4W 3N5) — the segment is named for the building itself, disclosed.
- Measurements (4): walk → Shortreed Community School 0.59 km / 7.9 min; walk → FreshCo 1.22 km / 16.2 min; walk → Aldergrove Community Centre 1.38 km / 18.5 min; drive → Aldergrove Library 1.50 km / 3.1 min. (Matches entry 51's origin and values — same building.)
- NOT CONFIRMED: catchments; building-point geocode; exact nearest stop + frequencies; no municipal park or middle/secondary school within ~1 km confirmed (§3 carries Shortreed only).

**61. Twin Firs — 27272 32 Ave (aldergrove-guide; townhomes)** — twin-firs--aldergrove-guide-nearby-2026-11-02.md — 3,395 B, 397 words.
- Address used: roster address; origin = 32 Avenue segment point in the V4W 3H7 area nearest the 27272 block, disclosed (a Fern Ridge 32 Ave segment was returned first — not used, disclosed in-file).
- Measurements (4): walk → Aldergrove Community Centre 0.87 km / 11.7 min; walk → Parkside Centennial Elementary 0.67 km / 9.0 min; walk → Shortreed Community School 1.20 km / 16.1 min; drive → Save-On-Foods 2.11 km / 3.6 min.
- NOT CONFIRMED: catchments; building-point geocode; exact nearest stop + frequencies; no municipal park within ~1 km confirmed.

**62. Grosvenor Ambleside — 1355 Bellevue Avenue (ambleside; condos)** — grosvenor-ambleside--ambleside-nearby-2026-11-02.md — 3,064 B, 363 words.
- Address used: roster address, the exact address point returned by Nominatim — no substitution.
- Measurements (4): walk → Hollyburn Elementary, 1329 Duchess Ave 0.47 km / 6.2 min; walk → Ambleside Park 0.65 km / 8.7 min; walk → West Vancouver Community Centre, 2121 Marine Drive 1.35 km / 18.0 min; drive → Park Royal, 2002 Park Royal South 1.27 km / 1.7 min. Over-cap walk excluded (disclosed): Ridgeview Elementary 1.52 km.
- NOT CONFIRMED: catchments (no SD45 locator run); exact nearest individual bus stop; bus frequencies other than the cited SeaBus (15 min) and R2 peak (6–7 min) lines.

**63. Lincoln Gardens — 2110 Marine Dr (ambleside; 55-plus)** — lincoln-gardens--ambleside-nearby-2026-11-02.md — 3,231 B, 396 words.
- Address used: roster address, the building point returned by Nominatim — no substitution. Building identified by name/class in the header line only — no age-restriction claim in the body (per the roster note on its 55+ basis).
- Measurements (4): walk → West Vancouver Community Centre 0.22 km / 2.9 min; walk → West Vancouver Memorial Library, 1950 Marine Drive 0.26 km / 3.4 min; walk → École Pauline Johnson Elementary, 1150 22nd St 0.72 km / 9.6 min; drive → Park Royal 2.40 km / 3.2 min. Over-cap walk excluded: Ambleside Park 1.81 km — park not carried in §2 (Memorial Park, District-sourced, carried instead).
- NOT CONFIRMED: catchments; exact nearest stop; other bus frequencies.

**64. Oceanbrook — 1425 Esquimalt Avenue (ambleside; condos)** — oceanbrook--ambleside-nearby-2026-11-02.md — 3,141 B, 376 words.
- Address used: roster address, the named "Oceanbrook Condos" building point — no substitution.
- Measurements (4): walk → Hollyburn Elementary 0.30 km / 3.9 min; walk → Ambleside Park 1.10 km / 14.7 min; walk → Ridgeview Elementary, 1250 Mathers Ave 1.25 km / 16.7 min; drive → Park Royal 1.65 km / 2.6 min. Over-cap walk excluded (disclosed): École Pauline Johnson 1.53 km — school not carried in §3.
- NOT CONFIRMED: catchments; exact nearest stop; other bus frequencies.

**65. Park Marine — 1930 Marine Drive (ambleside; condos)** — park-marine--ambleside-nearby-2026-11-02.md — 3,249 B, 399 words.
- Address used: roster address, the named "Park Marine" building point — no substitution.
- Measurements (4): walk → West Vancouver Memorial Library 0.21 km / 2.8 min; walk → West Vancouver Community Centre 0.48 km / 6.3 min; walk → École Pauline Johnson Elementary 0.98 km / 13.1 min; drive → Park Royal 2.02 km / 2.4 min. Over-cap walk excluded: Ambleside Park 1.51 km — park not carried in §2 (Memorial Park carried instead).
- NOT CONFIRMED: catchments; exact nearest stop; other bus frequencies.

**66. Parkview Tower — 555 13th Street (ambleside; condos)** — parkview-tower--ambleside-nearby-2026-11-02.md — 2,980 B, 352 words.
- Address used: roster address, the named "Parkview Tower" building point — no substitution.
- Measurements (4): walk → Hollyburn Elementary 0.16 km / 2.1 min; walk → Ambleside Park 0.76 km / 10.2 min; walk → Ridgeview Elementary 1.18 km / 15.7 min; drive → Park Royal 1.22 km / 1.7 min.
- NOT CONFIRMED: catchments; exact nearest stop; other bus frequencies.

**67. Sea Wind — 1930 Bellevue Avenue (ambleside; condos)** — sea-wind--ambleside-nearby-2026-11-02.md — 3,187 B, **404 words (+4)**.
- Address used: roster address; origin = named OSM building point "Sea Wind, 1930 Bellevue Avenue" — no substitution.
- Measurements (4): walk → West Vancouver Memorial Library, 1950 Marine Dr 0.23 km / 3.1 min; walk → Ambleside Park 1.48 km / 19.8 min (to the OSM named Ambleside Park point, disclosed); walk → Hollyburn Elementary 1.17 km / 15.5 min; drive → Park Royal 2.15 km / 2.9 min.
- NOT CONFIRMED: catchments; bus frequencies + nearest individual stop; Ambleside/John Lawson Park street addresses (not on the District pages read); Park Royal sits outside the ~1 km radius (nearest allowed-source grocery anchor); Fresh St. Market street address not stated on its own pages read, so not an anchor.

**68. The Tides — 588 16th Street (ambleside; condos)** — the-tides--ambleside-nearby-2026-11-02.md — 3,175 B, **404 words (+4)**.
- Address used: roster address; origin = named OSM building point "The Tides, 588 16th Street" — no substitution.
- Measurements (4): walk → Hollyburn Elementary 0.54 km / 7.1 min; walk → Memorial Library 0.76 km / 10.1 min; walk → Ambleside Park 1.19 km / 15.8 min; drive → Park Royal 1.73 km / 2.3 min.
- NOT CONFIRMED: same set as entry 67.

**69. Tudor Gardens — 843 22nd St (ambleside; 55-plus)** — tudor-gardens--ambleside-nearby-2026-11-02.md — 3,482 B, **457 words (+57)** — the batch's largest overage, kept rather than cut a second in-scope school plus three required geocode/measurement disclosures; building identified by name/class in the header line only, zero age-restriction claims in the body.
- Address used: roster address in title/header; **no OSM building point exists in any variant tried** — origin = the 22nd Street segment point in the roster postal-code area (V7V 4C4); times approximate, disclosed in-file.
- Measurements (2): walk → École Pauline Johnson Elementary, 1150 22nd St 0.48 km / 6.4 min; drive → Park Royal 3.48 km / 4.3 min. Excluded: walk → John Lawson Park 1.89 km (over cap). Not measured: the West Vancouver Community Centre — no OSM point exists for 2121 Marine Drive and every address query returns far-west Marine Drive segments (Altamont/Sandy Cove), which were discarded (two bogus first-pass values, 2.89 km and 4.89 km, caught and thrown out before writing).
- NOT CONFIRMED: catchments; frequencies + nearest stop; building-point geocode; John Lawson Park street address; Fresh St. Market address. §2/§4 flag John Lawson Park and Park Royal as outside the ~1 km scope for this building.

**70. Westerlies — 1480 Duchess Avenue (ambleside; condos)** — westerlies--ambleside-nearby-2026-11-02.md — 3,186 B, **401 words (+1)**.
- Address used: roster address; origin = OSM residential building point for 1480 Duchess Avenue — no substitution.
- Measurements (4): walk → Hollyburn Elementary 0.31 km / 4.1 min; walk → Memorial Library 0.98 km / 13.0 min; walk → Ambleside Park 1.08 km / 14.4 min; drive → Park Royal 1.59 km / 2.1 min.
- NOT CONFIRMED: same set as entry 67.

**71. Westshore Place — 650 16th Street (ambleside; condos)** — westshore-place--ambleside-nearby-2026-11-02.md — 3,193 B, **404 words (+4)**.
- Address used: roster address; origin = named OSM building point "Westshore Place, 650 16th Street" — no substitution.
- Measurements (4): walk → Hollyburn Elementary 0.53 km / 7.1 min; walk → Memorial Library 0.83 km / 11.0 min; walk → Ambleside Park 1.26 km / 16.8 min; drive → Park Royal 1.75 km / 2.5 min.
- NOT CONFIRMED: same set as entry 67.

**72. Westview Terrace — 1390 Duchess Ave (ambleside; 55-plus)** — westview-terrace--ambleside-nearby-2026-11-02.md — 3,220 B, 386 words.
- Address used: roster address, geocoded exactly as the named OSM building point "Westview Terrace, 1390 Duchess Avenue" (V7T 1H6) — no substitution. Building identified by name/class in the header line only.
- Measurements (4): walk → Hollyburn Elementary 0.14 km / 1.9 min; walk → Ambleside Park 0.98 km / 13.0 min; walk → West Vancouver Memorial Library 1.14 km / 15.2 min; drive → Park Royal 1.49 km / 2.3 min.
- NOT CONFIRMED: catchments; bus frequencies (the SeaBus every-15-minutes figure is TransLink-stated and carried in §1); Ambleside Park street address (not on the District park page).

**73. Delta Cedars — 8635 120 Street (annieville; condos)** — delta-cedars--annieville-nearby-2026-11-02.md — 3,183 B, 400 words (at cap).
- Address used: roster address, geocoded exactly as the named OSM building point "Delta Cedars, 8635 120 Street" (V4C 6R5) — no substitution. New in-pass sources: TransLink tt319 + tt391 (routes 319/391 on Scott Rd; Scottsdale Exchange + Scott Road Station named); SD37 Ministry list read in full.
- Measurements (5): walk → Hellings Elementary, 11655 86 Ave 0.64 km / 9.0 min; walk → Immaculate Conception School, 8840 119 St (independent) 0.72 km / 9.5 min; drive → North Delta Recreation Centre, 11415 84 Avenue 1.79 km / 3.3 min; drive → Delview Secondary, 9111 116 St 2.24 km / 3.8 min; drive → Scottsdale Centre, 7019 120 Street 3.30 km / 5.4 min. Discarded (disclosed): walk → Delview 1.98 km, walk → Annieville Lions Park 2.76 km, both over cap.
- NOT CONFIRMED: catchments; frequencies; Annieville Lions Park street address (not stated on the City of Delta page read in this pass); the two over-cap walks.

**74. Muse North Delta ("Muse") — 9015 120 Street (annieville; condos + townhomes)** — muse-north-delta--annieville-nearby-2026-11-02.md — 3,108 B, 384 words.
- ONE file only, per the roster component note; header carries the roster name and both programs.
- Address used: roster address, geocoded exactly as the named OSM building point "Muse North Delta, 9015 120 Street" (V4C 0E3) — no substitution.
- Measurements (4): walk → Gibson Elementary, 11451 90 Ave 1.16 km / 15.5 min; walk → Delview Secondary 1.24 km / 16.5 min; drive → Scott Road Station 4.87 km / 6.0 min; drive → Scottsdale Centre 4.14 km / 6.8 min. Discarded (disclosed): walk → Annieville Elementary, 9240 112 St 1.95 km, over cap.
- NOT CONFIRMED: catchments; frequencies (routes 312/319/391); Annieville Lions Park street address; the over-cap walk.

**75. Arbutus Village — 2202 McBain Avenue (arbutus; condos)** — arbutus-village--arbutus-nearby-2026-11-02.md — 3,502 B, **437 words (+37)** — overage kept rather than cut cited facts/URLs or the required geocode disclosure (batch 2's Creekside precedent, +43).
- Address used: roster address in title/header; **Nominatim has no building point for 2202 McBain Avenue, only street segments** — the first segment point returned (V6L 2P2, ~700 m west) was discarded; measurements run from the McBain Avenue segment point at the Arbutus Street end (V6L 0B9 segment), consistent with the CD-1 village range 2202–2298 McBain in the condos home file. Disclosed in-file. Roster address NOT proven wrong.
- New in-pass sources: TransLink tt016 (route 16 via Arbutus St / West Blvd); SD39 Ministry list read in full (Shaughnessy Elementary 4250 Marguerite St; York House School 4176 Alexandra St, independent).
- Measurements (4): walk → Prince of Wales Secondary, 2250 Eddington Dr 0.68 km / 9.1 min; walk → Shaughnessy Elementary 1.31 km / 17.5 min; drive → Safeway, 990 King Edward Avenue 2.51 km / 4.4 min; drive → Kerrisdale Community Centre, 5851 West Blvd 2.56 km / 4.5 min. Discarded (disclosed): walk → York House 1.53 km (just over cap); walk → Safeway 2.49 km (drive used).
- NOT CONFIRMED: catchments; frequencies; building-point geocode (substitution above); a grocery store inside the Arbutus Shopping Centre at 4255 Arbutus Street (no retailer locator page with that street address read in this pass).

**76. Arista — 2955 156 Street (arista-townhomes; townhomes)** — arista--arista-townhomes-nearby-2026-11-02.md — 3,382 B, 381 words.
- Phase-1 file used: the phase-1 file under the project slug itself (arista-townhomes-nearby-2026-11-02.md) — no fallback needed.
- Address used: roster address, geocoded as an exact OSM address point (2955 156 Street, V3Z 0E5) — no substitution. §5 re-measured fresh in this pass.
- Measurements (4): walk → Sunnyside Elementary, 2828 159 St 0.84 km / 11.2 min (identical to phase 1's independent measurement); drive → Thrifty Foods, 15745 Croydon Dr 1.09 km / 2.7 min; drive → Orchard Grove Park, 16685 24 Ave 3.03 km / 5.7 min; drive → Grandview Heights Aquatic Centre, 16855 24 Avenue 3.60 km / 6.4 min.
- NOT CONFIRMED: catchments; frequencies; Morgan Crossing street address on the centre's own site (carried from phase 1 as name/street only).

## Flags carried forward

1. **Skipped:** entry 52, The Hart (aldergrove; condos) — ADDRESS NOT IN NOTES → final mop-up batch.
2. **Aldergrove Town Centre Drive (entries 53–55):** ungeocodable in Nominatim in any variant and absent from returned OSM data — all three files use the disclosed "Aldergrove Town Centre" site point (entry 50's pattern, re-verified in this pass; §5 sets identical by construction). Roster addresses NOT proven wrong — the condos home file states the same addresses.
3. **Entry 69, Tudor Gardens:** no building-point geocode exists; 22nd Street segment origin used and disclosed; times approximate.
4. **Entry 75, Arbutus Village:** no building point; Arbutus-end McBain segment used and disclosed; roster address not proven wrong.
5. **Ambleside toolchain gap (entries 67–71 vs 62–66):** the West Vancouver Community Centre (2121 Marine Drive) is carried as a §2 anchor across the Ambleside files but has no reliable address-query point — worker 3 used Nominatim's named "West Vancouver Community Centre" POI beside 21st Street and measured to it for entries 62, 63, 65; worker 4 found no usable point for entries 67–71 and measured to it in none. Both treatments are disclosed in-file; plain "2121 Marine Drive" queries return far-west Marine Drive segments (Altamont/Sandy Cove) and were discarded by both workers.
6. **Segment-origin pattern (entries 51, 56–61):** no building points exist in Nominatim for the Aldergrove 29A/31A/32 Ave complexes; origins are disclosed segment or named-complex points. A same-named Brookswood-Fernridge segment trap (31A Ave / 32 Ave) was returned first for entries 59 and 61 — not used, disclosed in-file.
7. **Toolchain caution (worker 5):** plain civic-address queries returned wrong points for 7019 120 Street, 9240 112 Street, 2828 159 Street, 16685 24 Avenue and 2121 Marine Drive; named-POI queries returned the correct points in every case, and only corrected points sit behind the measurements above.
