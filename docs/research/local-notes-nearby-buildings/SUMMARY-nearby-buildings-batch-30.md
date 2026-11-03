# What's Nearby — Phase 2, Batch P2-30 Summary

Production date: 2026-11-02 (all measurements taken 2026-11-02).

**Roster range covered: entries 746–770 — 25 buildings produced.** Every entry in 746–770 carries a street address, so nothing was skipped and no extension was needed.

**Skipped problem entries in range: none.** Mop-up list to date (unchanged): entries 52, 85, 86, 156, 188, 193, 195, 240, 415, 487, 535, 549–552, 627, 632, 643, 667, 699.

**Areas:** pitt-meadows-homes-for-sale 5, poplar 6, poplar-guide 3, port-coquitlam-homes-for-sale 5, port-moody-centre 4, quay 2.

**Measurements: 137 listed in §5 (66 walk, 71 drive)**, tallied from the files on disk (four further "Walk to" bullets sit in NOT CONFIRMED sections as over-cap exclusion notes and are NOT counted); all measured 2026-11-02 starting at each building's own address or its disclosed origin; every kept walk inside the 4–6 km/h sanity band and the walk ≤1.5 km / drive ≤10 km caps. **HTTP 429s: none** across all five workers. **Roster lines proved wrong on the ground: none** — the roster was never silently corrected.

**Five buildings could not be measured** — Kings Crossing (758), Kingsview Estates (759), Citadel Pointe (760), Luxora (761) and Platform by Aragon (768): after repeated foreground variants Nominatim returned only whole-street segments for each address (for Citadel Pointe, for BOTH rostered addresses, 678 and 688 Citadel Drive; for Luxora the segment points reverse-geocode to 2550/2536 Shaughnessy Street — different addresses — and were discarded). No neighbouring or adjacent feature's point was substituted for any of them. Each file's §§1–4 are complete and §5 is the brief's single bullet "Travel times: not measured in this pass," with the failure disclosed in NOT CONFIRMED. All five are candidates for a later harmonizing pass if a sourced civic point is obtained.

**Pitt Meadows interpolation method (new, fully disclosed in-file):** Nominatim has NO building points for any of the five pitt-meadows-homes-for-sale addresses (746–750) — only road segments, several centred kilometres away on the same street (the same Harris Road coverage gap that left entry 745 unmeasurable in P2-29). Worker 1 discarded all wrong-segment points, probed OSM address nodes and cross-streets along each road by reverse-geocode (~85 probe calls, saved to its scratch dir), and interpolated each building's own point on its own street segment between bracketing OSM address points/crossings; every interpolated origin reverse-geocodes to the building's own street and postal area and the method is disclosed in each file's §5 origin line and NOT CONFIRMED. Orion (749) used the Nominatim 191 Street segment point for its own 12400 block. These five origins are segment-grade, not house-point-grade — flagged here as the batch's one method extension, and as candidates for re-measurement if a sourced civic point set becomes available.

**Word-cap overages (7 of 25, disclosed; wording trimmed only, no cited fact or URL cut):** The Grande by Onni 482 (+82), Boardwalk at Klahanie 446 (+46), Liv42 432 (+32), Anchor Pointe 431 (+31), Origin 427 (+27), Solaris at Meadows Gate 426 (+26), The Excelsior 426 (+26) — driven by measurement density on top of the mandated origin/multi-address disclosures. All other files 278–397 words by disk `wc -w`.

**Multi-address entries (2):**
- Citadel Pointe (760) — one file; title on the first address, 678 Citadel Drive; header carries "678/688 Citadel Drive" exactly as rostered; NEITHER address has a verifying point, so §5 is the fallback and the anchor failure is disclosed.
- Boardwalk at Klahanie (Polygon) (766) — one file; title on the first address, 600 Klahanie Drive; header carries both addresses exactly as rostered; anchor = 600 (the building's own named OSM point, reverse-geocoded exactly); the 700 Klahanie Drive point also verified but not used; anchor choice disclosed in NOT CONFIRMED.

**Component-address anchor (1):** The Grande by Onni (767) — title/header on the rostered civic address, 300 Morrissey Road; the free-form geocode for 300 returned a Morrissey Road segment point whose reverse went to a TD bank node at 110 Brew Street (discarded, disclosed); measurements anchor on the 305 Morrissey Road point of the building named "The Grande" — 305 is one of the rostered unit addresses for this same building (units also addressed 305 and 308 Morrissey Road) — disclosed in NOT CONFIRMED with the 305/308 note carried.

**Same-name / separateness handling:**
- College Park (753, 33708 King Road, poplar) produced separately from College Park (33728 King Road, home central-abbotsford, earlier batch) — the roster's flagged possible-duplicate pair, kept as two files, separateness stated in-file; College Park Place (754, 33718 King Road) is a third, separate building, stated in both King Road files. All four King Road origins (751–754) were individually reverse-verified against their OWN roster addresses — no cross-building point reuse.
- Kings Crossing (758, poplar-guide) produced separately from Kings Crossing 1/2 (edmonds-be, earlier batches); separateness stated in-file. No tenure claim made (tenure UNCONFIRMED in the notes).
- The Shaughnessy (763) and Shaughnessy Square (764) are different buildings on different streets; each origin verified against its own address.
- Maplewood Estates (756) — the name trap was checked: the origin is the park's own named caravan_site point at 2035 Martens St, NOT Maplewood Manor (strata) or Maplewood House (care).

**Other disclosed resolutions:**
- Central Heights Manor (752): no house point exists; the origin is the building's own named landuse feature "Central Heights Manor, 33535," whose centroid reverse-geocodes to Kirk Avenue (the rear street) — disclosed in-file, with the discarded segment points (including one reverse-geocoding to 33556 King Road) also disclosed.
- Mayfair Terrace (762): the roster's COUNT-HOME DISAGREEMENT is recorded in NOT CONFIRMED exactly as a disagreement, not resolved (condos counts it in port-coquitlam-homes-for-sale; 55-plus counts it through the standalone exemplar file). Origin is a disclosed Atkins Avenue segment point reverse-geocoding to 2265 Atkins Avenue, the frontage across from 2266. A Lions Park destination point was discarded in both Port Coquitlam files that attempted it (a Lions Way street segment, not the park at 2300 Lions Way); the park stays in §2 from the City directory, unmeasured.
- Solaris at Meadows Gate (750): the complex's second address, 12079 Harris Road (from the condos home file), is disclosed in NOT CONFIRMED; the roster address 12069 was used as the origin.
- 50 Electronic (765): title/header carry the full roster name "50 Electronic (50 Electronic Avenue)" with the roster address 55 Klahanie Drive; the origin is the building point named "55 Klahanie," reverse-geocoded exactly. Both grocery addresses rest on the disclosed retailer own-domain search-result fallback.
- Grocery fallbacks: the Pitt Meadows files' Save-On-Foods (19150 Lougheed Hwy) and the Poplar files' Real Canadian Superstore (2855 Gladwin Rd) rest on retailer own-domain search results carried from phase 1 / read this pass, disclosed in-file. Citadel Pointe's §4 omits Save-On-Foods Port Coquitlam because its retailer page shows no street address (per the phase-1 finding), disclosed in NOT CONFIRMED.
- School catchments are in NOT CONFIRMED in every file (no district locator run for these addresses); bus frequencies likewise unless an operator page read stated them.

## Per-building detail

### 746. Cedar Downs — 12565 190A Street, Pitt Meadows (pitt-meadows-homes-for-sale; condos)
- File: cedar-downs--pitt-meadows-homes-for-sale-nearby-2026-11-02.md — 3,225 B / 391 w
- Origin: interpolated point on 190A Street bracketed by OSM cross-streets (McMyn Rd / Lougheed Hwy); reverse-geocodes to 190A Street, Pitt Meadows. Segment-only geocode coverage; wrong-segment points discarded, disclosed.
- Measurements (7): walk Save-On-Foods 0.45 km/6.0 min; drive Save-On-Foods 0.34/1.5; walk Pitt Meadows Station 1.16/15.5; drive Station 1.34/3.0; drive Library 1.41/2.6; drive Recreation Centre 1.66/3.4; drive Real Canadian Superstore 2.55/4.9.
- NOT CONFIRMED: SD42 catchments; segment-only geocode + discards; Harris Road Park has no OSM point (unmeasured); over-cap walks excluded (Library 1.51 km, Rec Centre 1.70 km, Superstore 3.08 km).

### 747. Liv42 — 12409 Harris Road, Pitt Meadows (pitt-meadows-homes-for-sale; condos)
- File: liv42--pitt-meadows-homes-for-sale-nearby-2026-11-02.md — 3,452 B / 432 w (overage +32)
- Origin: interpolated point on Harris Road between OSM address points 12277 and 12465; reverse-geocodes to Harris Road, Pitt Meadows.
- Measurements (12): walk Pitt Meadows Station 0.44/5.9; drive Station 0.59/1.2; walk Save-On-Foods 0.43/5.8; drive Save-On-Foods 0.61/1.9; walk Library 0.78/10.4; drive Library 0.65/0.9; walk Recreation Centre 0.97/13.0; drive Rec Centre 0.91/1.7; walk Davie Jones Elementary 1.21/16.1; drive Davie Jones 1.19/2.3; walk Pitt Meadows Elementary 1.13/15.2; drive Superstore 2.54/4.5.
- NOT CONFIRMED: catchments; far-segment discards; Harris Road Park no OSM point; over-cap walk to Superstore (2.36 km) excluded.

### 748. Origin — 11950 Harris Road, Pitt Meadows (pitt-meadows-homes-for-sale; condos)
- File: origin--pitt-meadows-homes-for-sale-nearby-2026-11-02.md — 3,466 B / 427 w (overage +27)
- Origin: interpolated point on Harris Road between the 119 Avenue crossing and 12007 Harris Road; reverse-geocodes to Harris Road, Pitt Meadows.
- Measurements (12): walk Pitt Meadows Elementary 0.24/3.2; drive PM Elementary 0.60/1.5; walk Recreation Centre 0.32/4.3; drive Rec Centre 0.43/1.3; walk Library 0.39/5.2; walk Station 0.97/13.0; drive Station 0.88/1.6; walk Davie Jones Elementary 0.79/10.6; drive Davie Jones 0.73/1.4; walk Pitt Meadows Secondary 1.12/14.9; drive Save-On-Foods 1.49/2.8; drive Superstore 2.47/4.9.
- NOT CONFIRMED: catchments; discards; bus frequencies unstated; over-cap walk to Superstore (2.62 km) excluded.

### 749. Orion — 12460 191 Street, Pitt Meadows (pitt-meadows-homes-for-sale; condos)
- File: orion--pitt-meadows-homes-for-sale-nearby-2026-11-02.md — 3,179 B / 392 w
- Origin: the Nominatim 191 Street segment point for the 12400 block (postal code matching the address); reverse-geocodes to 191 Street, Pitt Meadows.
- Measurements (9): walk Save-On-Foods 0.37/4.9; drive Save-On-Foods 0.37/1.2; walk Station 0.72/9.7; drive Station 0.89/1.7; walk Library 1.07/14.3; drive Library 0.95/1.4; walk Recreation Centre 1.27/16.9; drive Rec Centre 1.21/2.2; drive Superstore 2.50/4.3.
- NOT CONFIRMED: catchments; segment-only geocode; Harris Road Park no OSM point; over-cap walk to Superstore (2.64 km) excluded.

### 750. Solaris at Meadows Gate — 12069 Harris Road, Pitt Meadows (pitt-meadows-homes-for-sale; condos)
- File: solaris-at-meadows-gate--pitt-meadows-homes-for-sale-nearby-2026-11-02.md — 3,397 B / 426 w (overage +26)
- Origin: interpolated point on Harris Road between OSM address points 12007 and 12099; reverse-geocodes to Harris Road, the building's own civic block.
- Measurements (11): walk Recreation Centre 0.20/2.7; drive Rec Centre 0.18/0.8; walk Library 0.18/2.4; walk Pitt Meadows Elementary 0.35/4.8; drive PM Elementary 0.43/1.7; walk Station 0.69/9.2; drive Station 0.66/1.3; walk Davie Jones Elementary 0.70/9.3; walk Save-On-Foods 1.16/15.4; drive Save-On-Foods 1.27/2.6; drive Superstore 3.20/5.2.
- NOT CONFIRMED: catchments; discards; the complex's second address 12079 Harris Road disclosed, not used as origin; frequencies; over-cap walk to Superstore (2.53 km) excluded.

### 751. 33738 King Road — 33738 King Road, Abbotsford (poplar; condos)
- File: 33738-king-road--poplar-nearby-2026-11-02.md — 2,843 B / 324 w
- Origin: building way point; reverse-geocodes exactly to 33738 King Road. The building is unnamed in the notes — title and header use the street address as the name (entry-299 precedent).
- Measurements (5): walk Rogers Forum 0.21/2.8; walk McCallum Park & Ride 0.33/4.5; walk University of the Fraser Valley 0.86/11.5; walk Jackson Elementary 1.23/16.5; drive Real Canadian Superstore 4.35/8.1.
- NOT CONFIRMED: SD34 catchments; bus frequencies unstated; building name (none in the notes).

### 752. Central Heights Manor — 33535 King Rd, Abbotsford (poplar; 55-plus)
- File: central-heights-manor--poplar-nearby-2026-11-02.md — 3,103 B / 360 w
- Origin: the building's own named landuse feature "Central Heights Manor, 33535"; its centroid reverse-geocodes to Kirk Avenue (rear street), disclosed. Free-form/structured searches returned King Road segments only; a segment point at the building's postal code reverse-geocoded to 33556 King Road and was discarded.
- Measurements (5): walk McCallum Park & Ride 0.33/4.5; walk Rogers Forum 0.60/8.0; walk Jackson Elementary 0.85/11.3; walk UFV 1.24/16.6; drive Superstore 4.39/8.4.
- NOT CONFIRMED: catchments; frequencies; origin-point caveat above.

### 753. College Park — 33708 King Road, Abbotsford (poplar; condos)
- File: college-park--poplar-nearby-2026-11-02.md — 2,994 B / 348 w
- Origin: building way point; reverse-geocodes exactly to 33708 King Road.
- Measurements (5): walk McCallum Park & Ride 0.52/6.9; walk Rogers Forum 0.76/10.1; walk UFV 1.18/15.7; walk Jackson Elementary 1.29/17.3; drive Superstore 4.71/9.2.
- NOT CONFIRMED: catchments; frequencies; separateness from the different College Park at 33728 King Road (home central-abbotsford, earlier batch; roster possible-duplicate flag) stated in-file.

### 754. College Park Place — 33718 King Road, Abbotsford (poplar; condos)
- File: college-park-place--poplar-nearby-2026-11-02.md — 2,980 B / 348 w
- Origin: building way point; reverse-geocodes exactly to 33718 King Road.
- Measurements (5): walk Rogers Forum 0.11/1.5; walk UFV 0.58/7.7; walk McCallum Park & Ride 0.65/8.7; drive Jackson Elementary 1.56/3.2; drive Superstore 4.71/9.3.
- NOT CONFIRMED: catchments; frequencies; separateness from College Park (33708) stated; over-cap walk to Jackson Elementary (1.55 km/20.8 min) excluded and noted.

### 755. Crown Point — 1450 McCallum Road, Abbotsford (poplar; 55-plus + townhomes)
- File: crown-point--poplar-nearby-2026-11-02.md — 3,073 B / 357 w
- Origin: address point; reverse-geocodes exactly to 1450 McCallum Road. Both program home files read.
- Measurements (6): walk UFV 0.46/6.1; walk Rogers Forum 0.47/6.3; walk McCallum Park & Ride 0.88/11.7; drive Jubilee Park 2.54/4.9; drive South Poplar Traditional Elementary 3.20/4.6; drive Superstore 4.91/9.2.
- NOT CONFIRMED: catchments; frequencies; Jubilee Park destination point is the park's named feature whose centroid reverse-geocodes to Pauline Lane (disclosed; §2 address from the City parks amenities list).

### 756. Maplewood Estates — 2035 Martens St, Abbotsford (poplar; 55-plus, manufactured-home park)
- File: maplewood-estates--poplar-nearby-2026-11-02.md — 2,772 B / 338 w
- Origin: the park's own named caravan_site point; reverse-geocodes to "Maplewood Estates, 2035, Martens Street" — NOT Maplewood Manor or Maplewood House; no discard needed.
- Measurements (5, all drive): Jackson Elementary 4.07/6.5; South Poplar Traditional Elementary 5.18/7.6; Real Canadian Superstore (2855 Gladwin Rd) 4.55/8.2; Clearbrook Library 3.61/6.7; Matsqui Recreation Centre 3.95/7.6.
- NOT CONFIRMED: catchment for 2035 Martens St; nearest bus stop/routes/frequency; over-cap walk to South Poplar Traditional (5.16 km/68.8 min) noted, not listed.

### 757. The Argyle — 34248 King Road, Abbotsford (poplar-guide; townhomes)
- File: the-argyle--poplar-guide-nearby-2026-11-02.md — 2,821 B / 344 w
- Origin: house point; reverse-geocodes exactly to 34248 King Road.
- Measurements (5, all drive): Jackson Elementary 2.15/3.6; South Poplar Traditional 4.52/6.6; Real Canadian Superstore 5.21/9.2; Clearbrook Library 7.60/10.5; Matsqui Recreation Centre 7.65/11.1.
- NOT CONFIRMED: catchment; nearest stop/routes/frequency; over-cap walk to Jackson Elementary (2.20 km/29.4 min, in band) noted, not listed.

### 758. Kings Crossing — 1641 King Crescent, Abbotsford (poplar-guide; townhomes)
- File: kings-crossing--poplar-guide-nearby-2026-11-02.md — 2,657 B / 316 w
- Origin: NONE — free-form, name and structured searches returned only the King Crescent road segment. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: origin failure; separateness from Kings Crossing 1/2 (edmonds-be) stated; catchment; nearest stop; no tenure claim (tenure UNCONFIRMED in the notes).

### 759. Kingsview Estates — 33922 King Road, Abbotsford (poplar-guide; townhomes)
- File: kingsview-estates--poplar-guide-nearby-2026-11-02.md — 2,427 B / 278 w
- Origin: NONE — free-form, name and structured searches returned only King Road road segments (including segments in other parts of Abbotsford, discarded and disclosed). §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: origin failure + discards; catchment; nearest stop/routes/frequency.

### 760. Citadel Pointe — 678/688 Citadel Drive, Port Coquitlam (port-coquitlam-homes-for-sale; townhomes)
- File: citadel-pointe--port-coquitlam-homes-for-sale-nearby-2026-11-02.md — 2,747 B / 300 w
- Origin: NONE — both rostered addresses returned only the Citadel Drive road segment across all variants, so neither could anchor; anchor failure for both addresses disclosed. (Destination points for Citadel Middle, Castle Park Elementary and Costco were verified but unused without an origin.) §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: anchor failure (678 and 688); SD43 catchment; nearest-stop routes/frequencies; Save-On-Foods omitted from §4 (retailer page showed no street address, per phase 1).

### 761. Luxora — 2368 Shaughnessy Street, Port Coquitlam (port-coquitlam-homes-for-sale; condos)
- File: luxora--port-coquitlam-homes-for-sale-nearby-2026-11-02.md — 2,649 B / 287 w
- Origin: NONE usable — free-form, name, structured, postal-code and bounded variants returned only Shaughnessy Street segment points; the top segment point reverse-geocodes to 2550 Shaughnessy Street and its south end to 2536 Shaughnessy Street — different addresses — discarded; name search returned no result. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: origin failure; school catchments; bus frequencies.

### 762. Mayfair Terrace — 2266 Atkins Avenue, Port Coquitlam (port-coquitlam-homes-for-sale; 55-plus + condos)
- File: mayfair-terrace--port-coquitlam-homes-for-sale-nearby-2026-11-02.md — 3,309 B / 389 w
- Origin: Nominatim Atkins Avenue segment point reverse-geocoding to 2265 Atkins Avenue — the frontage across from 2266; name search returned no building point; disclosed in-file.
- Measurements (5): walk Port Coquitlam Community Centre 0.48/6.3; walk Port Coquitlam Station 0.66/8.8; walk Central Elementary 0.85/11.3; drive Save-On-Foods (2385 Ottawa St) 3.80/6.4; drive Costco (2370 Ottawa St) 4.11/7.0.
- NOT CONFIRMED: COUNT-HOME DISAGREEMENT recorded, not resolved (condos counts it in port-coquitlam-homes-for-sale; 55-plus counts it through the standalone exemplar file); origin segment-point disclosure; catchments; frequencies; Lions Park destination point discarded (Lions Way segment, not the park at 2300 Lions Way; park listed in §2 unmeasured).

### 763. The Shaughnessy — 2789 Shaughnessy Street, Port Coquitlam (port-coquitlam-homes-for-sale; condos)
- File: the-shaughnessy--port-coquitlam-homes-for-sale-nearby-2026-11-02.md — 2,946 B / 341 w
- Origin: Nominatim building point named "The Shaughnessy"; reverse-geocodes exactly to 2789 Shaughnessy Street.
- Measurements (3): walk Port Coquitlam Station 0.97/12.9; walk Port Coquitlam Community Centre 1.24/16.6; drive Costco 3.29/5.5.
- NOT CONFIRMED: over-cap walk to Central Elementary (1.57 km) excluded and noted; Lions Park point discarded (same segment problem as 762); catchments; frequencies.

### 764. Shaughnessy Square — 2099 Lougheed Highway, Port Coquitlam (port-coquitlam-homes-for-sale; condos)
- File: shaughnessy-square--port-coquitlam-homes-for-sale-nearby-2026-11-02.md — 2,978 B / 345 w
- Origin: Nominatim point at 2099 Lougheed Highway (a retail unit in the complex); reverse-geocodes exactly to the building's own civic address; name search returned no separate residential point (disclosed). Kept fully separate from The Shaughnessy (763).
- Measurements (3): walk Port Coquitlam Station 1.30/17.4; drive Gates Park (2300 Reeve St) 1.99/3.5; drive Costco 3.26/5.3.
- NOT CONFIRMED: over-cap walks (Community Centre 1.58 km, Central Elementary 1.91 km) excluded and noted; origin disclosure; catchments; frequencies.

### 765. 50 Electronic (50 Electronic Avenue) — 55 Klahanie Drive, Port Moody (port-moody-centre; condos)
- File: 50-electronic--port-moody-centre-nearby-2026-11-02.md — 3,288 B / 397 w
- Origin: Nominatim building point named "55 Klahanie"; reverse-geocodes exactly to 55 Klahanie Drive.
- Measurements (6): walk Moody Elementary (110 Buller St) 0.76/10.1; walk Port Moody Recreation Complex (300 Ioco Rd) 1.09/14.6; walk Save-On-Foods (221 Ioco Rd) 1.36/18.1; drive Thrifty Foods (170 Brew St) 0.99/2.4; drive Inlet Centre Station 1.76/4.1; drive Rocky Point Park 1.55/4.2.
- NOT CONFIRMED: catchments; frequencies; a first Moody Elementary geocode at a different location was discarded (point used reverse-geocodes to the school at 110 Buller Street); both grocery addresses disclosed in-file as retailer own-domain search results.

### 766. Boardwalk at Klahanie (Polygon) — 600 Klahanie Drive and 700 Klahanie Drive, Port Moody (port-moody-centre; condos)
- File: boardwalk-at-klahanie--port-moody-centre-nearby-2026-11-02.md — 3,451 B / 446 w (overage +46)
- Origin: 600 Klahanie Drive — the building's own named OSM point ("Boardwalk, 600, Klahanie Drive"), reverse-geocoded exactly. The 700 Klahanie Drive point also verified ("Boardwalk, 700, Klahanie Drive") but not used; anchor choice disclosed.
- Measurements (8): walk Inlet Centre Station 1.02/13.6; drive Inlet Centre 1.39/3.2; walk Thrifty Foods (170 Brew St) 0.63/8.4; drive Thrifty 0.62/1.4; walk Port Moody Recreation Complex 0.76/10.1; drive Rec Complex 1.14/2.6; walk Port Moody Public Library 0.91/12.1; drive Library 0.94/2.1.
- NOT CONFIRMED: anchor choice (600 vs 700); school catchments; bus frequencies unstated on operator pages read.

### 767. The Grande by Onni — 300 Morrissey Road, Port Moody (port-moody-centre; condos)
- File: the-grande-by-onni--port-moody-centre-nearby-2026-11-02.md — 3,636 B / 482 w (overage +82)
- Origin: the 305 Morrissey Road point of the building named "The Grande" (a rostered unit address of this same building); the free-form 300 Morrissey Road result was a road segment (reverse to a TD bank node at 110 Brew St) and was discarded; discard + anchor choice disclosed in-file.
- Measurements (8): walk Inlet Centre Station 0.36/4.8; drive Inlet Centre 0.73/2.0; walk Thrifty Foods 0.20/2.7; drive Thrifty 0.24/0.7; walk Port Moody Recreation Complex 0.85/11.4; drive Rec Complex 0.85/2.2; walk Port Moody Public Library 0.65/8.6; drive Library 0.65/1.6.
- NOT CONFIRMED: units also addressed 305 and 308 Morrissey Road (roster note carried); origin discard/choice; catchments; frequencies.

### 768. Platform by Aragon — 83 Moody Street, Port Moody (port-moody-centre; condos)
- File: platform-by-aragon--port-moody-centre-nearby-2026-11-02.md — 2,725 B / 328 w
- Origin: NONE reliable — free-form, structured and three name-search variants returned only a Moody Street road segment (reverse: Moody Street, Pleasantside) or empty results; segment point discarded. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: origin failure; catchments; frequencies.

### 769. Anchor Pointe — 1135 Quayside Drive, New Westminster (quay; condos)
- File: anchor-pointe--quay-nearby-2026-11-02.md — 3,205 B / 431 w (overage +31)
- Origin: the building's own named OSM point; reverse-geocodes to "Anchor Pointe, 1135, Quayside Drive."
- Measurements (9): walk New Westminster Station 0.59/7.9; drive Station 0.93/2.1; walk Westminster Pier Park 1.17/15.7; drive Pier Park 1.37/4.0; drive École Qayqayt Elementary 1.92/3.8; walk Shops at New West 0.62/8.3; drive Shops 0.92/2.1; walk Anvil Centre 0.74/9.9; drive Anvil 0.89/2.1.
- NOT CONFIRMED: over-cap walk to Qayqayt (1.79 km) excluded, drive kept; catchments; frequencies; New Westminster Public Library address (716 6th Ave) returned no Nominatim result, so no time to it was measured.

### 770. The Excelsior — 8 Laguna Court, New Westminster (quay; condos)
- File: the-excelsior--quay-nearby-2026-11-02.md — 3,165 B / 426 w (overage +26)
- Origin: own address point; reverse-geocodes exactly to 8 Laguna Court.
- Measurements (8): walk New Westminster Station 1.11/14.8; drive Station 1.43/3.4; drive Westminster Pier Park 1.87/5.3; drive École Qayqayt Elementary 2.42/5.1; walk Shops at New West 1.13/15.1; drive Shops 1.43/3.4; walk Anvil Centre 1.25/16.7; drive Anvil 1.39/3.4.
- NOT CONFIRMED: over-cap walks (Pier Park 1.70 km, Qayqayt 2.30 km) excluded, drives kept; catchments; frequencies; New Westminster Public Library ungeocoded as in 769.
