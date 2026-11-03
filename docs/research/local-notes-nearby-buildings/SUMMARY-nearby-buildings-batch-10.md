# What's Nearby — Phase 2, Batch P2-10 Summary

Produced Nov 2, 2026. Roster range covered: **entries 233–258 — 25 buildings produced. Skipped: entry 240, Marine Woods (champlain-heights; townhomes) — ADDRESS NOT IN NOTES** (streets given as Millstone Street / Fieldstone Avenue / Cobblestone Avenue; no civic address in notes; address not researched, per the brief). Extension to entry 258 was needed to reach 25. Mop-up list to date: entries 52 (The Hart), 85 (District Flats at Southlands), 86 (The Granary at Southlands), 156 (Winona Park), 188 (Natura), 193 (Upper Montrose), 195 (The Abby Townhome Series), 240 (Marine Woods).

Areas: central-park-bs 1, central-pt-coquitlam 4, champlain-heights 2, chilliwack-downtown 5, chilliwack-mountain 5, chilliwack-proper-east 6, chilliwack-proper-south 2.

**Totals: 124 measurements listed (71 walk, 53 drive), all measured 2026-11-02 starting at each building's own address (or its disclosed origin — see below); every kept walk inside the 4–6 km/h sanity band and the walk ≤1.5 km / drive ≤10 km caps. HTTP 429s: none across all five workers. Roster lines proved wrong on the ground: NONE — the roster was never silently corrected.**

**The Yale Road geocode gap (the batch's structural fact):** Nominatim has NO house-number coverage for Yale Road, Chilliwack — repeated foreground variants (free-form, structured, postal-code, building-name) returned only road-segment points scattering over kilometres. Two disclosed treatments resulted, both brief-consistent and neither silent: Worker 4's three Yale Road files (251, 252, 253) use the §5 fallback bullet "Travel times: not measured in this pass" with the failure disclosed; Worker 5's three Yale Road files (254, 255, 256) use disclosed approximate origins (a Yale Road segment point for Mountainview Estates; the named Chilliwack Middle School point ~120 m east for Newmark; the named Chilliwack Secondary point for Thornberry Lane), each disclosed in §5 and NOT CONFIRMED with times stated as approximate. The same gap hit Young Road (Cottage Grove used the named Chilliwack City Hall point ~80 m north, disclosed) and Kelly Avenue / Mary Hill Road in Port Coquitlam (segment points, below). A future mop-up measurement pass for Yale Road would need a different geocoder or sourced civic points.

**Segment-point origins with identical measurement sets (toolchain limitation, not copy errors):** the three Kelly Avenue buildings (234, 235, 237) share one disclosed Kelly Avenue segment origin and therefore identical §5 sets; a later foreground variant returned a Kelly segment point ~100 m east — the first foreground run's point was kept and governs, disclosed in-file. The POCO (236) uses a disclosed Mary Hill Road segment point on the same basis.

**Geocode process:** the backgrounded-delivery failure mode appeared in four of five workers. Outcomes: Worker 2's backgrounded run agreed with its foreground re-run (no disclosure needed); Worker 5's backgrounded output agreed on every exact point used (no disclosure needed); Worker 3's backgrounded run disagreed for The Willows (backgrounded house point vs foreground segment point ~5 m apart — foreground governed, discrepancy disclosed in-file); Workers 1 and 4 worked from foreground runs with disclosed segment fallbacks. All routing was re-verified in isolated scratch dirs (/tmp/p2b10-w1/ … w5/).

**Word-cap overages: 4 of 25 files** — The Willows 444 (+44, driven by its two required geocode disclosures), Cottage Grove 420 (+20), Mountainview Estates 415 (+15), Chilliwack Gardens 401 (+1). Wording was trimmed in each; no cited fact or URL was cut. Westpointe is exactly 400; all other files 313–399 words.

**Coordinator verification:** all 25 files ls-verified on disk after delivery — every byte size below matches the workers' reports exactly; the buildings folder now holds 250 files. Spot-checked in full: the 46693 Yale Road file (§5 fallback bullet exactly as the brief prescribes, §§1–4 complete) and The Willows (segment-point origin + foreground/background discrepancy both disclosed in NOT CONFIRMED).

---

## 233. Wimbledon Club — 6188 Patterson Avenue (central-park-bs; condos)
- File: wimbledon-club--central-park-bs-nearby-2026-11-02.md — 2,778 B, 333 words. All 5 sections + NOT CONFIRMED written.
- Address/origin: roster address; Nominatim named house point "Wimbledon Club, 6188 Patterson Avenue".
- Measurements (5): walk Patterson Station 0.25 km/3.3 min; walk Chaffey-Burke Elementary 1.19/15.8; walk Central Park 1.26/16.7; walk Maywood Community Elementary 1.41/18.7; drive Metropolis at Metrotown 1.42/2.9. Walk to Moscrop Secondary measured 2.12 km — excluded over the walk cap.
- NOT CONFIRMED: catchments; bus frequencies; Central Park destination is the Swangard Stadium point Nominatim returned for 3883 Imperial St (disclosed in-file); no supermarket confirmed on a retailer's own site within walking radius (§4 centre-only).

## 234. Lumiere — 2436 Kelly Avenue (central-pt-coquitlam; condos)
- File: lumiere--central-pt-coquitlam-nearby-2026-11-02.md — 3,206 B, 386 words. All sections written.
- Address/origin: **disclosed Kelly Avenue street-segment point** (no house point exists for any Kelly Ave address on repeated foreground variants).
- Measurements (7): walk PoCo Community Centre 0.19/2.6; walk Port Coquitlam Station 0.46/6.1; walk Gates Park 0.88/11.7; walk Central Elementary 1.00/13.4; walk Riverside Secondary 1.21/16.2; walk Shaughnessy Station 1.26/16.9; drive Shaughnessy Station 1.79/3.2.
- NOT CONFIRMED: segment-point origin; catchments; frequencies; supermarket unconfirmed (§4 centre-only).

## 235. Montrose Square — 2180 Kelly Avenue (central-pt-coquitlam; condos)
- File: montrose-square--central-pt-coquitlam-nearby-2026-11-02.md — 3,222 B, 388 words. All sections written.
- Address/origin: same disclosed Kelly Avenue segment origin as 234 — identical measurement set (7, as 234), a toolchain limitation disclosed in-file, not a copy error.
- NOT CONFIRMED: as 234.

## 236. The POCO — 2427 Mary Hill Road (central-pt-coquitlam; condos)
- File: the-poco--central-pt-coquitlam-nearby-2026-11-02.md — 3,189 B, 389 words. All sections written.
- Address/origin: **disclosed Mary Hill Road street-segment point** (first foreground run's point kept; later variants returned different segments).
- Measurements (6): walk PoCo Community Centre 0.50/6.6; walk Central Elementary 0.62/8.2; walk Port Coquitlam Station 0.85/11.3; walk Gates Park 1.04/13.9; walk Riverside Secondary 1.07/14.3; drive Shaughnessy Station 1.74/3.1.
- NOT CONFIRMED: segment-point origin; catchments; frequencies; supermarket unconfirmed (§4 centre-only). Note: the condos home file records The POCO as a presale project (estimated completion 2028); the roster address was used exactly as given — not treated as a roster error.

## 237. Symphony at Gates Park — 2488 Kelly Avenue (central-pt-coquitlam; condos)
- File: symphony-at-gates-park--central-pt-coquitlam-nearby-2026-11-02.md — 3,236 B, 392 words. All sections written.
- Address/origin: same disclosed Kelly Avenue segment origin as 234/235 — identical measurement set (7, as 234). The file reports only the measured segment-origin figures with the origin disclosed, per the brief (the building's true Gates Park walk is likely shorter than the segment-origin figure).
- NOT CONFIRMED: as 234.

## 238. Bordeaux at Champlain Gardens — 3265 Clermont Mews (champlain-heights; townhomes)
- File: bordeaux-at-champlain-gardens--champlain-heights-nearby-2026-11-02.md — 2,774 B, 338 words. All sections written.
- Address/origin: roster address; foreground Nominatim house point (a backgrounded first run agreed with the foreground re-run — no discrepancy to disclose).
- Measurements (6): walk Captain James Cook Elementary 0.18/2.4; walk Your Independent Grocer 0.45/6.0; walk Champlain Heights Community Centre 0.67/9.0; walk Champlain Heights Annex 0.91/12.1; walk Champlain Heights Community Elementary 1.25/16.7; drive Killarney Secondary 1.31/3.9.
- NOT CONFIRMED: catchments; frequencies; the Your Independent Grocer destination is the retailer's own locator-result point for 7190 Kerr St (the civic geocode returned a Kerr St segment point, not used — disclosed in-file).

## 239. Highgate — 3150 East 58th Avenue (champlain-heights; townhomes)
- File: highgate--champlain-heights-nearby-2026-11-02.md — 2,787 B, 347 words. All sections written.
- Address/origin: roster address; foreground Nominatim house point.
- Measurements (5): walk Your Independent Grocer 0.44/5.8; walk Captain James Cook Elementary 0.60/8.0; walk Champlain Heights Community Centre 0.83/11.1; walk Everett Crowley Park 0.86/11.5; walk Champlain Heights Annex 1.07/14.2.
- NOT CONFIRMED: catchments; frequencies; grocer locator-point substitution (as 238); walk to Champlain Heights Community Elementary measured exactly 1.50 km — at the walk cap, excluded from §5 and noted in-file.

## 241. 9000 Birch Street — 9000 Birch Street (chilliwack-downtown; condos)
- File: 9000-birch-street--chilliwack-downtown-nearby-2026-11-02.md — 3,266 B, 389 words. All sections written. Building UNNAMED IN NOTES — title/header use the address exactly, per the roster.
- Address/origin: roster address; foreground Nominatim house point, returned as "The Birch Street Properties, 9000 Birch Street".
- Measurements (6): walk Chilliwack Library 0.35/4.7; walk Save-On-Foods 0.58/7.8; walk Central Community Park 1.08/14.4; walk Bernard Elementary 1.17/15.5; drive Chilliwack Middle 1.90/3.2; drive Chilliwack Central Elementary Community 2.29/3.8.
- NOT CONFIRMED: catchments; frequencies; Save-On-Foods destination = named store point (the 46020 Yale Rd civic geocode returned an out-of-downtown segment point, not used); Central Community Park destination = Victoria Ave segment point for 45943 Victoria Ave; Central Elementary destination = Young Rd segment point for 9435 Young Rd — all disclosed in-file.

## 242. 9060 Birch Street — 9060 Birch Street (chilliwack-downtown; condos)
- File: 9060-birch-street--chilliwack-downtown-nearby-2026-11-02.md — 3,251 B, 390 words. All sections written. UNNAMED IN NOTES — same treatment as 241.
- Address/origin: foreground Nominatim point for the roster address (returned display name "Birch Street, Five Corners" without the house number; coordinates sit immediately north of the 9000 Birch point, consistent with the address order).
- Measurements (5): walk Chilliwack Library 0.24/3.2; walk Save-On-Foods 0.49/6.5; walk Central Community Park 0.97/12.9; walk Bernard Elementary 1.28/17.1; drive Chilliwack Middle 1.68/2.7.
- NOT CONFIRMED: catchments; frequencies; Save-On-Foods named-point substitution and Central Park segment point (as 241, disclosed in-file).

## 243. Cedar Court — 45882 Cheam Ave (chilliwack-downtown; townhomes)
- File: cedar-court--chilliwack-downtown-nearby-2026-11-02.md — 3,310 B, 399 words. All sections written.
- Address/origin: roster address; foreground Nominatim house point.
- Measurements (6): walk Chilliwack Library 0.37/4.9; walk Save-On-Foods 0.37/4.9; walk Chilliwack Cultural Centre 0.83/11.1; walk Central Community Park 0.92/12.2; walk Bernard Elementary 1.19/15.8; drive Chilliwack Middle 1.60/2.4.
- NOT CONFIRMED: catchments; frequencies; Save-On-Foods named-point substitution and Central Park segment point (disclosed in-file).

## 244. Chilliwack Gardens — 45749 Spadina Avenue (chilliwack-downtown; condos)
- File: chilliwack-gardens--chilliwack-downtown-nearby-2026-11-02.md — 3,462 B, 401 words — **OVER CAP (+1)**.
- Address/origin: roster address; Nominatim house point.
- Measurements (9): walk Downtown Exchange 0.24/3.3; walk Save-On-Foods 0.33/4.5; walk Chilliwack Cultural Centre 0.52/6.9; walk Chilliwack Landing Leisure Centre 0.73/9.7; walk Central Community Park 0.77/10.4; walk Chilliwack Library 0.78/10.4; walk Bernard Elementary 1.35/18.0; walk Chilliwack Middle School 1.38/18.5; drive Chilliwack Secondary 1.52/2.8.
- NOT CONFIRMED: catchments; frequencies; Save-On-Foods routing point = retailer own search-result coordinates (a foreground re-run for 46020 Yale Rd returned a far-east Yale Road segment — disclosed); walk to Chilliwack Secondary dropped (1.54 km, over cap).

## 245. The Willows — 45893 Chesterfield Avenue (chilliwack-downtown; condos)
- File: the-willows--chilliwack-downtown-nearby-2026-11-02.md — 3,745 B, 444 words — **OVER CAP (+44, the batch's largest file; driven by its two required geocode disclosures; wording trimmed, no cited fact/URL dropped)**.
- Address/origin: **disclosed street-segment point** — Nominatim returned a Chesterfield Avenue segment point, not a house point; a backgrounded run had returned a house point ~5 m away — the foreground segment point governed, discrepancy disclosed in §5 and NOT CONFIRMED.
- Measurements (9): walk Salish Park 0.31/4.1; walk Chilliwack Library 0.39/5.2; walk Save-On-Foods 0.66/8.8; walk Downtown Exchange 0.67/8.9; walk Central Community Park 0.95/12.6; walk Bernard Elementary 1.33/17.8; walk Chilliwack Landing Leisure Centre 1.35/18.1; drive Chilliwack Middle School 1.61/2.6; drive Chilliwack Secondary 1.70/3.1.
- NOT CONFIRMED: catchments; frequencies; segment-point origin + foreground/background discrepancy; Save-On-Foods retailer-point substitution (as 244); walks to Middle (1.53 km) and Secondary (1.69 km) dropped over cap.

## 246. Eagles Perch — 43610 Chilliwack Mountain Road (chilliwack-mountain; townhomes)
- File: eagles-perch--chilliwack-mountain-nearby-2026-11-02.md — 3,143 B, 392 words. All sections written.
- Address/origin: roster address; house point.
- Measurements (5, all drives — rural ground, no in-cap walks): drive La Verendrye 3.86/9.4; drive Hillkeep Regional Park 4.12/10.0; drive Chilliwack Landing Leisure Centre 4.79/11.9; drive Chilliwack Library 5.23/12.1; drive Cottonwood Centre 8.45/15.7.
- NOT CONFIRMED: catchments; frequencies; all 5 walks over cap (shortest Hillkeep 4.12 km) and excluded; Hillkeep destination = Hillkeep Place street point and La Verendrye destination = Lickman Road segment point (no named-point geocode returned), disclosed in-file.

## 247. Maple Hills — 8590 Sunrise Drive (chilliwack-mountain; townhomes)
- File: maple-hills--chilliwack-mountain-nearby-2026-11-02.md — 3,109 B, 388 words. All sections written.
- Address/origin: **disclosed segment point** on Sunrise Drive (Nominatim returned no house number).
- Measurements (5, all drives): drive La Verendrye 3.45/8.4; drive Chilliwack Landing Leisure Centre 4.77/11.8; drive Chilliwack Library 5.21/12.0; drive Hillkeep Regional Park 6.55/16.0; drive Cottonwood Centre 8.04/14.7.
- NOT CONFIRMED: catchments; frequencies; all walks over cap (shortest Hillkeep 2.34 km) and excluded; Hillkeep/La Verendrye destination substitutions as 246.

## 248. Osprey Ridge — 43998 Chilliwack Mountain Road (chilliwack-mountain; townhomes)
- File: osprey-ridge--chilliwack-mountain-nearby-2026-11-02.md — 3,132 B, 391 words. All sections written.
- Address/origin: roster address; house point.
- Measurements (5, all drives): drive La Verendrye 3.26/7.9; drive Hillkeep Regional Park 3.79/9.2; drive Chilliwack Landing Leisure Centre 4.19/10.3; drive Chilliwack Library 4.63/10.5; drive Cottonwood Centre 7.85/14.2.
- NOT CONFIRMED: catchments; frequencies; all walks over cap (shortest La Verendrye 3.26 km) and excluded; destination substitutions as 246.

## 249. Reflections @ Cedar Sky — 43680 Chilliwack Mountain Road (chilliwack-mountain; townhomes)
- File: reflections-cedar-sky--chilliwack-mountain-nearby-2026-11-02.md — 3,024 B, 399 words. All sections written (trimmed from 406, wording only).
- Address/origin: roster address; Nominatim house point.
- Measurements (6, all drives): drive La Verendrye 3.76/9.2; drive Hillkeep Regional Park 4.03/9.8; drive Chilliwack Landing Leisure Centre 4.69/11.6; drive Downtown Exchange 5.25/11.7; drive Chilliwack Library 5.13/11.8; drive Cottonwood Centre 8.02/13.9.
- NOT CONFIRMED: catchments; frequencies; walk to Hillkeep 4.03 km over the walk cap — excluded (its 4.5 km/h speed was sane; the cap was the only reason); La Verendrye destination is a Lickman Road segment point, disclosed in-file; no grocery within ~1 km confirmed.

## 250. Westpointe — 43777 Chilliwack Mountain Road (chilliwack-mountain; townhomes)
- File: westpointe--chilliwack-mountain-nearby-2026-11-02.md — 3,031 B, 400 words (exactly at cap). All sections written.
- Address/origin: roster address; Nominatim house point.
- Measurements (6, all drives): drive La Verendrye 3.69/9.1; drive Hillkeep Regional Park 3.95/9.7; drive Chilliwack Landing Leisure Centre 4.62/11.5; drive Downtown Exchange 5.17/11.6; drive Chilliwack Library 5.06/11.7; drive Cottonwood Centre 7.95/13.8.
- NOT CONFIRMED: as 249 (walk to Hillkeep 3.95 km over cap, excluded; La Verendrye segment-point destination disclosed).

## 251. 46693 Yale Road — 46693 Yale Road (chilliwack-proper-east; condos)
- File: 46693-yale-road--chilliwack-proper-east-nearby-2026-11-02.md — 2,685 B, 315 words. §§1–4 + NOT CONFIRMED complete; **§5 = the brief's fallback bullet "Travel times: not measured in this pass."** Building UNNAMED IN NOTES — title/header use the address exactly.
- Address/origin: **none usable** — Nominatim returned no house point across repeated foreground variants (free-text ×2 incl. postal code V2P 7Z4, structured query, building-name search); only Yale Road segment points kilometres apart. Failure disclosed in NOT CONFIRMED.
- Measurements: 0.
- NOT CONFIRMED: origin geocode failure; catchments; frequencies; park street addresses not on the City parks list page read.

## 252. Evergreen Estates — 46777 Yale Road (chilliwack-proper-east; condos)
- File: evergreen-estates--chilliwack-proper-east-nearby-2026-11-02.md — 2,689 B, 313 words. §§1–4 + NOT CONFIRMED complete; **§5 fallback bullet, as 251** (structured + "Evergreen Estates" name search also returned nothing).
- Measurements: 0.
- NOT CONFIRMED: as 251.

## 253. Heritage Lane — 46735 Yale Road (chilliwack-proper-east; townhomes)
- File: heritage-lane--chilliwack-proper-east-nearby-2026-11-02.md — 2,684 B, 313 words. §§1–4 + NOT CONFIRMED complete; **§5 fallback bullet, as 251** (variants incl. postal code V2P 2S3 and a "Heritage Lane" name search, which returned nothing).
- Measurements: 0.
- NOT CONFIRMED: as 251.

## 254. Mountainview Estates — 46966 Yale Road (chilliwack-proper-east; 55-plus + condos)
- File: mountainview-estates--chilliwack-proper-east-nearby-2026-11-02.md — 3,312 B, 415 words — **OVER CAP (+15)**.
- Address/origin: **disclosed segment point** — the Yale Road segment point in the V2P 3J3 area returned for the roster address; times approximate, disclosed in §5 + NOT CONFIRMED.
- Measurements (4): walk Little Mountain Elementary 0.48/6.4; drive Chilliwack Middle School 1.16/1.5; drive Chilliwack Secondary 1.25/2.0; drive Chilliwack Library 2.51/3.5.
- NOT CONFIRMED: name spelling variant ("Mountain View Estates" in the condos program; the roster name governs; NOT Mountview Apartments, 46374 Margaret Ave — the roster's name trap, carried in-file); no building-point geocode (roster address not proven wrong); catchments; frequencies; park street addresses not read on a City page. §1 includes Route 71 Agassiz-Harrison, read from BC Transit in this pass.

## 255. Newmark — 46289 Yale Road (chilliwack-proper-east; condos)
- File: newmark--chilliwack-proper-east-nearby-2026-11-02.md — 3,244 B, 393 words. All sections written.
- Address/origin: **disclosed named-point substitution** — Nominatim's Chilliwack Middle School point, 46354 Yale Road (~120 m east of the roster address); disclosed in §5 + NOT CONFIRMED.
- Measurements (4): walk Chilliwack Secondary 0.27/3.6; walk Central Community Park 0.92/12.3; drive Save-On-Foods (46020 Yale Rd W) 0.60/1.0; drive Chilliwack Library 1.52/2.6. A walk to the Library routed at exactly 1.50 km and was excluded in favour of the drive.
- NOT CONFIRMED: no building-point geocode (roster address not proven wrong); catchments; frequencies; park street addresses.

## 256. Thornberry Lane — 46608 Yale Road (chilliwack-proper-east; townhomes)
- File: thornberry-lane--chilliwack-proper-east-nearby-2026-11-02.md — 3,137 B, 395 words. All sections written.
- Address/origin: **disclosed named-point substitution** — Nominatim's Chilliwack Secondary point, 46363 Yale Road (nearest named point west of the roster address); disclosed in §5 + NOT CONFIRMED.
- Measurements (3): drive Save-On-Foods 0.70/1.6; drive Chilliwack Library 1.62/3.2; drive Townsend Park 3.09/5.7.
- NOT CONFIRMED: no building-point geocode (roster address not proven wrong); walk to Gwynne Vaughan Park routed 1.94 km — outside the walk limit, excluded and disclosed in-file; catchments; frequencies; park street addresses.

## 257. Cottage Grove — 8500 Young Road (chilliwack-proper-south; 55-plus)
- File: cottage-grove--chilliwack-proper-south-nearby-2026-11-02.md — 3,278 B, 420 words — **OVER CAP (+20)**.
- Address/origin: **disclosed named-point substitution** — Nominatim's Chilliwack City Hall point, 8550 Young Road (~80 m north of the roster address; Young Road house-number geocodes returned only far-scattered segment points); disclosed in §5 + NOT CONFIRMED.
- Measurements (4): walk Robertson Elementary 0.36/4.9; drive Bernard Elementary 1.88/4.0; drive Save-On-Foods, 45585 Luckakuck Way 3.34/6.2 (destination = Cottonwood Centre named point at that address); drive Sardis Park 4.76/7.3.
- NOT CONFIRMED: the roster's boundary flag recorded as instructed (south end of Young Road / Sardis side, carried on the Proper South board feed label; the roster home slug governs the file); no building-point geocode (roster address not proven wrong); walk to Bernard Elementary routed 1.87 km — outside the walk limit, excluded and disclosed; catchments; frequencies; park street addresses.

## 258. The Elliot — 45562 Airport Road (chilliwack-proper-south; condos)
- File: the-elliot--chilliwack-proper-south-nearby-2026-11-02.md — 2,607 B, 314 words. All sections written.
- Address/origin: roster address; exact Nominatim house-number point (a backgrounded first run agreed on every exact point used — no discrepancy to disclose).
- Measurements (4): walk Bernard Elementary 1.42/18.9; walk Robertson Elementary 1.47/19.6; drive Chilliwack Library 1.75/2.6; drive Townsend Park 2.88/4.8. (The Robertson destination point is the Southlands Crescent segment point returned for its Ministry-list address.)
- NOT CONFIRMED: catchments; frequencies; park street addresses.
