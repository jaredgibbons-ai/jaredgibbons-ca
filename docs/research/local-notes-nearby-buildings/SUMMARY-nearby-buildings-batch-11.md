# What's Nearby — Phase 2, Batch P2-11 Summary

Produced Nov 2, 2026. Roster range covered: **entries 259–283 — 25 buildings produced. Skipped: NONE** — every entry in 259–283 carries a street address, so nothing was deferred to the mop-up batch from this range and no extension past entry 283 was needed. Mop-up list to date: entries 52 (The Hart), 85 (District Flats at Southlands), 86 (The Granary at Southlands), 156 (Winona Park), 188 (Natura), 193 (Upper Montrose), 195 (The Abby Townhome Series), 240 (Marine Woods).

Areas: chilliwack-proper-south 2, chilliwack-proper-west 7, cloverdale-bc 13, coal-harbour 3.

**Totals: 146 measurements listed (88 walk, 58 drive)**, tallied from the per-file lists below, all measured 2026-11-02 starting at each building's own address (or its disclosed origin — see below); every kept walk inside the 4–6 km/h sanity band and the walk ≤1.5 km / drive ≤10 km caps. **HTTP 429s: none across all five workers. Roster lines proved wrong on the ground: NONE — the roster was never silently corrected.**

**The Yale Road geocode gap recurred exactly as settled in batch 10:** The Vibe (260) has no building-point geocode — repeated foreground variants returned only Yale Road segment points scattering over kilometres. The disclosed treatment used: a named-point substitution (the Bernard Elementary point, 45465 Bernard Ave), disclosed in §5 + NOT CONFIRMED with times stated as approximate. Wolfe Road (261, 262, 267) and Spadina Avenue (263, 266) have the same segment-only coverage pattern in this part of Chilliwack; Clayton's 68/68A Avenue (269, 273, 274) and 194 Street (280) likewise returned no house points — every affected file uses a disclosed segment point or named-point substitution, stated in-file.

**Shared-origin measurement sets (toolchain limitation, not copy errors):** 45185 Wolfe Road (261) and Centre Field (262) share the disclosed Townsend Park origin point and therefore identical §5 sets; Calera (269) and Compass apartment phase (273) share the identical disclosed 68 Avenue segment point ("18854 68 Ave") and therefore identical §5 sets. Both pairings are disclosed in each file.

**Geocode process:** the backgrounded-delivery failure mode appeared in two of five workers. Worker 2 did not draft from its backgrounded run; its foreground re-runs governed, and the one kind-difference (Parkside Gardens: backgrounded Wolfe Road segment points vs the foreground named building point actually used) is disclosed in that file. Worker 1 received a garbled partial rendering of a backgrounded output mid-task; when the complete output landed it re-verified in a fresh foreground run and amended three files before delivery — Elmwood Terrace's false discrepancy bullet was removed, The Vibe's §5 wording was corrected to the exact segment-scatter finding, and Ivy Green's first-pass measurements (routed from an unverifiable named point) were withdrawn and re-measured from a disclosed segment point. Worker 1's corrected figures are what stand in the files and in this summary; the coordinator spot-checked the amended Ivy Green NOT CONFIRMED on disk. Workers 3–5 ran foreground-only.

**Two same-named buildings, separate files:** Compass (apartment phase, 273) and Compass (townhouse units, 274) are distinct roster buildings at different addresses; per the Central Park Place precedent both filenames carry address disambiguators, both titles use the plain name + roster address, and each file's NOT CONFIRMED notes the other's separate file.

**Word-cap overages: 9 of 25 files** — Compass (apartment phase) 482 (+82), The Vibe 458 (+58), Ivy Green 455 (+55), Spadina Regency 452 (+52), Centre Field 437 (+37), 45185 Wolfe Road 434 (+34), Waterstone 425 (+25), Charlton 403 (+3), Calera 402 (+2). All are driven by mandated disclosures (multi-address headers, segment/named-point origin disclosures, count-home disagreement items) on top of full measurement sets; wording was trimmed in each and no cited fact or URL was cut. All other files 336–398 words.

**Coordinator verification:** all 25 files ls-verified on disk after delivery — every byte size and word count below matches the workers' final/corrected reports exactly; the buildings folder now holds 275 files. Spot-checked in full or in part: The Vibe (four-address header, Yale Road substitution disclosed), Compass 18755 (two-address header, anchor disclosed), Ivy Green (corrected segment-origin NOT CONFIRMED; withdrawn first-pass figures absent).

---

## 259. Elmwood Terrace — 8725 Elm Drive (chilliwack-proper-south; condos)
- File: elmwood-terrace--chilliwack-proper-south-nearby-2026-11-02.md — 2,772 B, 336 words. All 5 sections + NOT CONFIRMED written.
- Address/origin: roster address; Nominatim house point for 8725 Elm Drive (civic and name queries return the same point).
- Measurements (6): walk Kw'íyeqel Secondary 0.37 km/4.9 min; walk Robertson Elementary 0.54/7.2; drive Chilliwack Library 1.48/3.0; drive Central Community Park 1.77/3.3; drive Chilliwack Middle School 2.38/4.0; drive Chilliwack Secondary 2.47/4.5.
- NOT CONFIRMED: catchments; frequencies; park street addresses on a City page.

## 260. The Vibe — 45555, 45559, 45561 and 45567 Yale Road (chilliwack-proper-south; condos)
- File: the-vibe--chilliwack-proper-south-nearby-2026-11-02.md — 3,629 B, 458 words (OVER CAP +58 — multi-address header + Yale Road disclosure).
- Address/origin: **disclosed named-point substitution** — the Bernard Elementary point, 45465 Bernard Ave. Yale Road has no house-number coverage (batch-10 settlement re-confirmed: only segment points scattering over kilometres); times approximate, disclosed in §5 + NOT CONFIRMED. Multi-address: title/anchor = first roster address 45555 Yale Road; header carries all four addresses exactly; anchor choice disclosed.
- Measurements (7): walk Chilliwack Cultural Centre 0.97/12.9; walk Chilliwack Landing Leisure Centre 1.06/14.3; walk Townsend Park 1.21/16.1; drive Downtown Exchange 1.45/3.4; drive Chilliwack Library 1.34/3.5; drive Central Community Park 2.19/4.8; drive Chilliwack Secondary 2.74/5.7.
- NOT CONFIRMED: anchor choice; no building-point geocode (roster address not proven wrong); catchments; frequencies; park street addresses.

## 261. 45185 Wolfe Road — 45185 Wolfe Road (chilliwack-proper-west; townhomes)
- File: 45185-wolfe-road--chilliwack-proper-west-nearby-2026-11-02.md — 3,509 B, 434 words (OVER CAP +34). Building UNNAMED IN NOTES — title/header use the address exactly.
- Address/origin: **disclosed named-point substitution** — the Townsend Park point, 45130 Wolfe Road; Wolfe Road civic queries returned only segment points. Times approximate.
- Measurements (6): walk Chilliwack Cultural Centre 1.17/15.8; walk Chilliwack Landing Leisure Centre 1.27/17.1; drive Chilliwack Library 1.68/3.4; drive Bernard Elementary 1.45/3.7; drive A D Rundle Middle School 2.64/4.7; drive Chilliwack Secondary 3.08/5.5.
- NOT CONFIRMED: no building-point geocode (roster address not proven wrong); shared origin with Centre Field (identical §5 set, disclosed); A D Rundle destination = named school point returned this pass; catchments; frequencies.

## 262. Centre Field — 45025 Wolfe Road (chilliwack-proper-west; townhomes)
- File: centre-field--chilliwack-proper-west-nearby-2026-11-02.md — 3,533 B, 437 words (OVER CAP +37).
- Address/origin: same disclosed Townsend Park substitution as 261 — identical measurement set (6, as 261), a toolchain limitation disclosed in-file, not a copy error.
- NOT CONFIRMED: as 261.

## 263. Ivy Green — 45775 Spadina Avenue (chilliwack-proper-west; 55-plus + condos)
- File: ivy-green--chilliwack-proper-west-nearby-2026-11-02.md — 3,829 B, 455 words (OVER CAP +55 — segment-origin disclosure + disagreement item).
- Address/origin: **disclosed Spadina Avenue street-segment point** (V2P 6S8 postal area, returned for the roster address); repeated foreground civic + name queries returned only segment points; times approximate. (First-pass measurements routed from an unverifiable named point were withdrawn and re-measured before delivery — see the geocode-process note above.)
- Measurements (7): walk Downtown Exchange 0.44/5.9; walk Chilliwack Landing Leisure Centre 0.53/7.1; walk Salish Park 0.95/12.7; walk Chilliwack Library 0.97/13.0; drive Chilliwack Middle 1.63/2.6; drive Chilliwack Secondary 1.72/3.1; drive Bernard Elementary 1.70/3.5.
- NOT CONFIRMED: **COUNT-HOME DISAGREEMENT recorded, not resolved** (55-plus counts it in chilliwack-proper-west; condos counts it in chilliwack-downtown; board listing data classifies the address as Chilliwack Downtown — the file follows the roster home); segment-point origin; catchments; frequencies.

## 264. Parkside Gardens — 45215 Wolfe Road (chilliwack-proper-west; townhomes)
- File: parkside-gardens--chilliwack-proper-west-nearby-2026-11-02.md — 3,006 B, 369 words. All sections written.
- Address/origin: roster address; foreground Nominatim named building point "Parkside Gardens".
- Measurements (6): walk Townsend Park 0.32/4.2; walk Chilliwack Cultural Centre 0.86/11.6; walk Chilliwack Landing Leisure Centre 0.96/12.9; walk Bernard Elementary 1.03/13.8; drive Chilliwack Library 1.41/2.7; drive Save-On-Foods (46020 Yale Rd W, named store point) 1.56/2.8.
- NOT CONFIRMED: catchments; frequencies/nearest stop; Save-On-Foods civic geocode returned no point (named store point used, disclosed); backgrounded-vs-foreground geocode discrepancy disclosed in-file (foreground governed).

## 265. The Robson — 9450 Robson Street (chilliwack-proper-west; condos)
- File: the-robson--chilliwack-proper-west-nearby-2026-11-02.md — 3,236 B, 398 words. All sections written.
- Address/origin: **disclosed Robson Street street-segment point** — no house point across repeated foreground variants; times approximate.
- Measurements (6): walk Central Community Park 0.55/7.3; walk Chilliwack Landing Leisure Centre 0.90/12.1; walk Downtown Exchange 0.92/12.3; walk Save-On-Foods (named store point) 0.98/13.0; walk Salish Park 1.26/16.8; drive Bernard Elementary 2.18/4.5.
- NOT CONFIRMED: segment-point origin (roster address not proven wrong); catchments; frequencies/nearest stop; Central Community Park and Salish Park street addresses not read on a City page.

## 266. Spadina Regency — 45765 Spadina Avenue (chilliwack-proper-west; 55-plus + condos)
- File: spadina-regency--chilliwack-proper-west-nearby-2026-11-02.md — 3,618 B, 452 words (OVER CAP +52 — 8 measurements + the two mandated NOT CONFIRMED items below; wording trimmed twice, no cited fact or URL cut).
- Address/origin: **disclosed Spadina Avenue street-segment point** (V2P 4H4 segment — same postal segment as the neighbouring 45749 Spadina house point); no house point returned; times approximate. 55-plus identified in the header line only; no age-restriction claims in the body.
- Measurements (8): walk Chilliwack Cultural Centre 0.33/4.4; walk Downtown Exchange 0.44/5.9; walk Chilliwack Landing Leisure Centre 0.54/7.2; walk Save-On-Foods (named store point) 0.55/7.4; walk Central Community Park 0.94/12.5; walk Chilliwack Library 0.97/13.0; drive Bernard Elementary 1.74/3.7; drive Chilliwack Secondary 1.76/3.4.
- NOT CONFIRMED: **COUNT-HOME DISAGREEMENT recorded, not resolved** (55-plus counts it in chilliwack-proper-west; condos counts it in chilliwack-downtown); **Form B/bylaw confirmation still owed per the 55-plus summary**; segment-point origin; catchments; frequencies; Central Community Park street address not read on a City page.

## 267. Townsend Terrace — 45085 Wolfe Road (chilliwack-proper-west; townhomes)
- File: townsend-terrace--chilliwack-proper-west-nearby-2026-11-02.md — 3,124 B, 389 words. All sections written.
- Address/origin: **disclosed named-point substitution** — Nominatim's Townsend Park point, 45130 Wolfe Road (the townhomes home file describes the complex as across from Townsend Park; Wolfe Road civic queries returned only segment points). No walk to Townsend Park is listed (the origin point is the park point itself; a 0.00 km route was measured and excluded).
- Measurements (5): walk Chilliwack Cultural Centre 1.17/15.8; walk Bernard Elementary 1.21/16.1; walk Chilliwack Landing Leisure Centre 1.27/17.1; drive Chilliwack Library 1.68/3.4; drive Save-On-Foods (named store point) 1.83/3.5.
- NOT CONFIRMED: no building-point geocode (roster address not proven wrong); catchments; frequencies/nearest stop.

## 268. Bacara — 7155 189 Street (cloverdale-bc; townhomes)
- File: bacara--cloverdale-bc-nearby-2026-11-02.md — 2,888 B, 348 words. All sections written.
- Address/origin: roster address; exact foreground Nominatim house point (backgrounded first run and foreground re-run agreed — no discrepancy to disclose).
- Measurements (4): walk Clayton Heights Secondary (7003 188 St) 0.71/9.4; walk École Salish Secondary 1.45/19.4; drive Save-On-Foods (17745 64 Ave) 4.19/6.6; drive Cloverdale Recreation Centre 4.82/7.6.
- NOT CONFIRMED: catchments; no bus exchange inside Cloverdale confirmed on a TransLink page; nearest stop and frequencies not stated; no grocery within ~1 km confirmed on a retailer's own site (§4 carries the phase-1 Cloverdale anchor, reached by the measured drive).

## 269. Calera — 18818 68 Avenue (cloverdale-bc; condos)
- File: calera--cloverdale-bc-nearby-2026-11-02.md — 3,128 B, 402 words (OVER CAP +2).
- Address/origin: **disclosed 68 Avenue segment point** (labelled "18854 68 Ave", ~250 m east of the building) — every variant returned this same segment point; no house point exists.
- Measurements (7): walk Clayton Heights Secondary 0.63/8.4; walk Hazelgrove Elementary 0.73/9.8; walk Clayton Community Centre 1.14/15.2; walk Hillcrest Elementary 1.18/15.8; walk Clayton Park 1.23/17.6; drive École Salish Secondary 2.19/4.4; drive Save-On-Foods (17745 64 Ave) 3.38/5.0.
- NOT CONFIRMED: segment-point origin (roster address not proven wrong); catchments; frequencies; no grocery within ~1 km confirmed on a retailer's own site (§4 drive-measured); walk to Adams Road Elementary measured 1.60 km — over the walk cap, excluded.

## 270. Carriage House — 17695 58 Ave (cloverdale-bc; 55-plus)
- File: carriage-house--cloverdale-bc-nearby-2026-11-02.md — 3,147 B, 377 words. All sections written. 55-plus identified in the header line only; no age claims in the body.
- Address/origin: roster address; exact Nominatim house point.
- Measurements (8): walk Cloverdale Library 0.45/6.0; walk Cloverdale Catholic School (independent, Ministry-listed) 0.60/8.0; walk Cloverdale Traditional 0.62/8.4; walk Cloverdale Recreation Centre 0.99/13.2; walk Cloverdale Youth Park 1.21/16.1; drive Lord Tweedsmuir Secondary 1.48/3.0; drive Save-On-Foods 1.93/3.6; drive Cloverdale Athletic Park 3.00/5.0.
- NOT CONFIRMED: bus exchange inside Cloverdale; catchments; frequencies; no grocery within ~1 km on a retailer's own site (§4 drive-measured).

## 271. Charlton — 17429 59 Avenue (cloverdale-bc; townhomes)
- File: charlton--cloverdale-bc-nearby-2026-11-02.md — 3,267 B, 403 words (OVER CAP +3).
- Address/origin: **disclosed 59 Avenue segment point in Cloverdale** (~200 m east) — no house point across variants; one variant returned a Sullivan/Newton segment point kilometres west, not used (disclosed in-file).
- Measurements (7): walk Cloverdale Catholic School 0.10/1.3; walk Cloverdale Recreation Centre 0.81/10.8; walk Cloverdale Youth Park 1.02/13.7; walk George Greenaway Elementary 1.04/13.9; drive Lord Tweedsmuir Secondary 1.96/4.2; drive Save-On-Foods 2.05/4.1; drive Cloverdale Athletic Park 2.46/4.9.
- NOT CONFIRMED: segment-point origin (roster address not proven wrong); bus exchange; catchments; frequencies; grocery as above.

## 272. Clayton Rise — 19505 68A Avenue (cloverdale-bc; townhomes)
- File: clayton-rise--cloverdale-bc-nearby-2026-11-02.md — 2,807 B, 369 words. All sections written (§2 is centre-only and §4 has no in-radius grocery — both disclosed in NOT CONFIRMED).
- Address/origin: **disclosed named-point substitution** — Nominatim's Katzie Elementary point, 6887 194A St (~200 m west); the only 68A Avenue segment points returned sat ~1.2 km west or in Sullivan (batch-10 named-point precedent).
- Measurements (4): walk Hazelgrove Elementary 0.82/10.9; walk Clayton Heights Secondary 1.49/19.9; drive Clayton Community Centre 2.25/3.7; drive Save-On-Foods 4.77/7.4.
- NOT CONFIRMED: named-point origin substitution; Katzie Elementary adjoins the origin point so no time to it was measured; catchments; frequencies; no park or grocery within ~1 km confirmed on a City/retailer page.

## 273. Compass (apartment phase) — 18755 68 Avenue (and 6815 188 Street), Clayton (cloverdale-bc; condos)
- File: compass-18755-68-avenue--cloverdale-bc-nearby-2026-11-02.md — 3,620 B, 482 words (OVER CAP +82 — structural: two-address header, anchor-choice disclosure, townhouse-phase note, shared-segment-origin disclosure, 7 measurements; wording trimmed, no cited fact or URL cut).
- Address/origin: **disclosed 68 Avenue segment point** (labelled "18854 68 Ave", ~450 m east of the anchor) — the identical point Nominatim returns for Calera, so Compass and Calera share one measurement set (toolchain limitation, disclosed in both files). The 6815 188 Street geocode returned a far-north 188 Street segment (Guildford/Anniedale), not used — disclosed. Multi-address: title/anchor = 18755 68 Avenue; header carries the full roster name and both addresses exactly.
- Measurements (7): identical set to Calera (walk Clayton Heights Secondary 0.63/8.4; walk Hazelgrove 0.73/9.8; walk Clayton Community Centre 1.14/15.2; walk Hillcrest 1.18/15.8; walk Clayton Park 1.23/17.6; drive Salish 2.19/4.4; drive Save-On-Foods 3.38/5.0).
- NOT CONFIRMED: anchor choice (second address not an anchor); townhouse phase (18777 68A Avenue) has its own separate file; shared segment-point origin (roster address not proven wrong); catchments; frequencies; grocery as above; Adams Road walk 1.60 km over cap, excluded.

## 274. Compass (townhouse units) — 18777 68A Avenue (cloverdale-bc; townhomes)
- File: compass-18777-68a-avenue--cloverdale-bc-nearby-2026-11-02.md — 2,983 B, 387 words. All sections written.
- Address/origin: **disclosed 68A Avenue street-segment point** in Clayton Heights — no house point across free-form, postal-code and structured variants; times approximate.
- Measurements (6): walk Clayton Heights Secondary 0.44/5.9; walk Save-On-Foods (18710 Fraser Hwy) 0.66/8.7; walk Clayton Park 1.06/14.8; walk Hillcrest Elementary 1.17/15.6; drive Clayton Community Centre 1.05/1.8; drive Adams Road Elementary 2.34/4.2.
- NOT CONFIRMED: apartment phase (18755 68 Avenue) has its own separate file; segment-point origin; catchments; frequencies; no Cloverdale bus exchange confirmed.

## 275. The Estates at Manor Ridge — 6140 192 St (cloverdale-bc; 55-plus)
- File: the-estates-at-manor-ridge--cloverdale-bc-nearby-2026-11-02.md — 2,947 B, 371 words. All sections written. 55-plus identified in the header line only; no age claims in the body.
- Address/origin: roster address; Nominatim house point.
- Measurements (4): walk Latimer Road Elementary 0.33/4.5; drive Save-On-Foods (18710 Fraser Hwy) 1.78/4.4; drive Save-On-Foods (17745 64 Ave) 3.64/6.4; drive Cloverdale Recreation Centre 4.17/7.2.
- NOT CONFIRMED: catchments; frequencies; walk to Don Christian Elementary routed 1.62 km — over the walk cap, excluded; no park within walking radius confirmed on a City page (§2 is recreation-centre only); no Cloverdale bus exchange confirmed. §1 uses Route 342, whose timetable routing runs on 192 St past this address.

## 276. Laredo — 16772 61 Avenue (cloverdale-bc; townhomes)
- File: laredo--cloverdale-bc-nearby-2026-11-02.md — 2,648 B, 339 words. All sections written.
- Address/origin: roster address; Nominatim house point.
- Measurements (5): walk A J McLellan Elementary 0.65/8.7; walk Cloverdale Athletic Park 0.85/11.3; walk Bose Forest Park 1.04/14.3; walk George Greenaway Elementary 1.39/18.6; drive Save-On-Foods (17745 64 Ave) 2.89/5.1.
- NOT CONFIRMED: catchments; frequencies; Bose Forest / Cloverdale Athletic destination points are the parks' named Nominatim points (civic geocodes returned segments in other areas — disclosed in-file); no Cloverdale bus exchange confirmed.

## 277. Manhattan Skye — 19551 66 Avenue (cloverdale-bc; townhomes)
- File: manhattan-skye--cloverdale-bc-nearby-2026-11-02.md — 2,854 B, 361 words. All sections written.
- Address/origin: **disclosed Nominatim named point "Manhattan Skye, Clayton Heights"** — no house point exists; free-form/structured variants returned 66 Avenue segments in Newton; times approximate.
- Measurements (4): walk Crescent Heights Academy (independent, Ministry-listed) 0.67/9.0; walk Katzie Elementary 0.86/11.5; drive Save-On-Foods (18710 Fraser Hwy) 2.16/3.8; drive Clayton Park 2.50/4.1.
- NOT CONFIRMED: named-point origin; catchments; frequencies; walk to Hazelgrove Elementary routed 1.68 km — over the walk cap, excluded; no Cloverdale bus exchange confirmed.

## 278. St. Andrews at Northview — 16421 64 Avenue (eight addresses) (cloverdale-bc; condos)
- File: st-andrews-at-northview--cloverdale-bc-nearby-2026-11-02.md — 2,660 B, 356 words. All sections written.
- Address/origin: roster first address; Nominatim house point. Multi-address (not a conflict): header carries all eight addresses exactly as the roster states them (16421, 16433, 16447, 16455, 16469, 16477, 16483 and 16499 64 Avenue); title/anchor = 16421 64 Avenue, anchor choice disclosed.
- Measurements (4): walk Bose Forest Park 0.64/9.2; walk A J McLellan Elementary 0.96/12.8; walk Cloverdale Athletic Park 1.24/16.5; drive Save-On-Foods (17745 64 Ave) 3.42/5.8.
- NOT CONFIRMED: anchor choice; catchments; frequencies; park destination named-point substitutions (as 276); no Cloverdale bus exchange confirmed.

## 279. Sunberry Court — 19250 65 Avenue (cloverdale-bc; townhomes)
- File: sunberry-court--cloverdale-bc-nearby-2026-11-02.md — 3,008 B, 364 words. All sections written.
- Address/origin: roster address; Nominatim house point "19250, 65 Avenue, Clayton Heights".
- Measurements (6): walk Katzie Elementary 1.04/13.9; walk Hazelgrove Elementary 1.27/16.9; walk Hazelgrove Park 1.46/19.4; drive Save-On-Foods (18710 Fraser Hwy) 1.71/3.2; drive Clayton Community Centre 2.23/3.6; drive Clayton Park 3.57/5.3.
- NOT CONFIRMED: catchments (no locator run); frequencies not stated; no bus exchange inside Cloverdale confirmed; walk to Save-On-Foods measured exactly 1.50 km — at the walk cap, excluded (drive listed); walk to Clayton Heights Secondary 1.60 km — over cap, excluded.

## 280. Waterstone — 6420 / 6440 194 Street (cloverdale-bc; condos)
- File: waterstone--cloverdale-bc-nearby-2026-11-02.md — 3,375 B, 425 words (OVER CAP +25 — the two required disclosures).
- Address/origin: **disclosed 194 Street segment-point origin** (Clayton Heights segment returned first by the structured queries for both addresses). No house-number geocode exists for 6420 or 6440 194 Street — repeated foreground variants (free-form, structured with postal code V4N 6J7, building-name search) returned only scattered 194 Street segment points (a first free-form attempt returned South Surrey segments, discarded). Times stated as approximate in §5 and NOT CONFIRMED. Multi-address: title/anchor = first address 6420 194 Street; header carries both addresses exactly; anchor choice disclosed.
- Measurements (5): walk Katzie Elementary 0.86/11.5; walk Hazelgrove Elementary 1.48/19.7; drive Save-On-Foods (18710 Fraser Hwy) 1.95/3.5; drive Clayton Heights Secondary 2.02/3.8; drive Clayton Community Centre 2.65/4.0.
- NOT CONFIRMED: multi-address anchor disclosure; no house-number geocode (roster address not proven wrong); catchments; frequencies; walks to Hazelgrove Park (1.66 km) and Clayton Heights Secondary (1.86 km) over the walk cap, excluded.

## 281. Avila — 560 Cardero Street (coal-harbour; condos)
- File: avila--coal-harbour-nearby-2026-11-02.md — 2,988 B, 375 words. All sections written.
- Address/origin: roster address; Nominatim house point.
- Measurements (6): walk New School at Coal Harbour (482 Broughton St) 0.35/4.6; walk Coal Harbour Community Centre 0.38/5.0; walk Devonian Harbour Park 0.62/8.2; walk Urban Fare (305 Bute St) 0.64/8.5; walk Harbour Green Park 0.76/10.3; drive Waterfront Station 1.65/3.5.
- NOT CONFIRMED: catchments; frequencies; no SkyTrain station inside Coal Harbour on the TransLink map read; no VPL branch inside Coal Harbour sourced.

## 282. Bauhinia — 535 Nicola Street (coal-harbour; condos)
- File: bauhinia--coal-harbour-nearby-2026-11-02.md — 2,999 B, 376 words. All sections written.
- Address/origin: roster address; Nominatim named building point "Bauhinia, 535 Nicola Street".
- Measurements (6): walk New School at Coal Harbour 0.24/3.2; walk Coal Harbour Community Centre 0.27/3.7; walk Urban Fare 0.54/7.2; walk Harbour Green Park 0.66/8.9; walk Devonian Harbour Park 0.70/9.4; drive Burrard Station 1.28/3.0.
- NOT CONFIRMED: as Avila.

## 283. Bayshore Tower 1 — 1790 Bayshore Drive (coal-harbour; condos)
- File: bayshore-tower-1--coal-harbour-nearby-2026-11-02.md — 3,061 B, 387 words. All sections written.
- Address/origin: roster address; Nominatim house point.
- Measurements (6): walk Devonian Harbour Park 0.19/2.6; walk King George Secondary 0.52/6.9; walk Coal Harbour Community Centre 0.73/9.8; walk Lord Roberts Elementary 0.94/12.6; walk Stanley Park Loop 1.13/15.1; drive Urban Fare (305 Bute St) 1.11/2.4.
- NOT CONFIRMED: as Avila. (In §1, Route 19's Stanley Park Loop terminus is referenced because its point is measured in §5; the cited source is the phase-1 TransLink stop page.)
