# What's Nearby — Phase 2, Batch P2-26 Summary

Production date: 2026-11-02 (all measurements taken 2026-11-02).

**Roster range covered: entries 643–669 — 25 buildings produced** (entries 644–666, 668, 669). Extension to entry 669 was needed to reach 25 because two entries in the base range were skipped.

**Skipped problem entries (held for the final mop-up batch; addresses NOT researched):**
- 643. Capistrano (luxury-homes-for-sale-in-white-rock-south-surrey) — ADDRESS CONFLICT: 1441 Blackwood St, White Rock / 1460 Martin St, White Rock
- 667. Luther Place (mission-homes-for-sale) — ADDRESS CONFLICT: 7525 Martin Place / 32286 7th Avenue

Mop-up list to date: entries 52, 85, 86, 156, 188, 193, 195, 240, 415, 487, 535, 549–552, 627, 632, 643, 667.

**Areas:** lynnmour 8, mackenzie-heights 1, main 4, mid-meadows-pitt-meadows 4, mission-homes-for-sale 8.

**Measurements: 137 listed in §5 (56 walk, 81 drive)**, all measured 2026-11-02 starting at each building's own address or its disclosed origin; every kept walk inside the 4–6 km/h sanity band and the walk ≤1.5 km / drive ≤10 km caps. **HTTP 429s: none** across all five workers. **Roster lines proved wrong on the ground: none** — every error was in geocoder points, never in a roster address; the roster was never silently corrected.

**Four buildings could not be measured** — Coho (657), Cedar Valley Manor (664), Cherry Lane (665), Mission Manor (668): after repeated foreground variants no origin point reverse-geocoded to the roster address (Coho's only Barnston View Road point reverse-geocodes to 10973 Barnston View Road, a different building; Cherry Lane's points reverse-geocode to 33751 7th Avenue; Mission Manor produced three inconsistent unnumbered 2nd Avenue segment points; Cedar Valley Manor's Cedar Street segment point is shared with a different address and sits beside the 8955 Cedar St school point). Each file's §§1–4 are complete and §5 is the brief's single bullet "Travel times: not measured in this pass," with the failure disclosed in NOT CONFIRMED. A later harmonizing pass with a different geocoder or sourced civic points could recover all four.

**Geocode governance highlights (all disclosed in-file):**
- **Connect at Nature's Edge (648):** every civic-address geocode variant for 757 Orwell Street fell on the separate southern Orwell Street segment near Phibbs Exchange and was discarded; measurements use the OSM named feature "Connect at Nature's Edge" on the northern Orwell alignment below Mt Seymour Parkway (the Marquee/Lakeside named-building-point precedent), whose reverse-geocode names the adjacent Lynnmour Elementary School — disclosed in-file. Recorded here openly: a stricter reading of the reverse-geocode rule would make this file a §5 fallback instead; the named-feature point was kept because it is the building itself in OSM, not a neighbouring address.
- **Lynnmour South (650):** the first origin (1825 Purcell Way street point) reverse-geocoded to Skeena Road (a Capilano University bus stop) — a different street — so that point and all 6 pairs measured from it were discarded. A unit address inside the complex from the townhomes home file (1828 Purcell Way) geocoded to a point reverse-geocoding to 1923 Purcell Way, same street segment; §5 was re-measured from it, substitution disclosed in-file.
- **Worker 4 discarded a whole first geocode pass** (a run that backgrounded despite a foreground request returned house-number-style points inconsistent with street geometry); everything was re-run in small foreground chunks into an on-disk points file and §5 drafted only from it. Briskham Hill (662) and Briskham Manor (663) share the identical Briskham Street segment point Nominatim returns for both addresses — §5 sets are identical, disclosed in both files (toolchain limitation, not a copy error).
- **Discarded destination points:** Robson Park (reverse-geocoded to 3129 Kingsway, wrong segment — pair dropped, disclosed in 3333 Main Street's file); Bridgman Park (point reverse-geocoded to Mountain Hwy at Lynnterm Terminal — pair dropped, disclosed in Hunter's file); a "51 Bonson Road" point ~1 km north of Shoreline Park (replaced with the park's named-place point, disclosed in both Pitt Meadows files); Mission Senior Secondary / Fraserview Learning Centre points (both reverse-geocoded to 33751 7th Avenue — schools listed in §3 from the Ministry list, not measured, disclosed in Glenkirk Court's file).
- **Retained street/segment origins, each reverse-geocoding to the correct street and disclosed in-file:** Apex (point reverse-names 1550 Fern St, the adjacent Beacon tower), BrookLynn (1448 Charlotte Rd), Compass (650 Seylynn Cres), Hunter (1471 Hunter St, the same development's east tower), Wedgewood (873 Premier St), The Heights (637 West 37th Ave), Coho II (Fraser Way street point; a second point ~0.45 km east disclosed), all four W4 origins, Glenkirk Court and Montgomery Condos.
- **Multi-address entries** produced as one file each, first address as title/anchor, all addresses in the header exactly as rostered, anchor choice disclosed: Wedgewood (anchor 717 Premier Street), The Heights (anchor 2505 West 37th Avenue), The Independent (anchor 285 East 10th Avenue).
- **Source-vs-source discrepancy (not a roster item):** the townhomes home file gives Heritage Park Middle School as 33700 Bell Ave; the BC Ministry list read in this pass gives 33700 Prentis Ave, and the name-query geocode reverse-confirmed Prentis Ave — the Mission files use the Ministry address.

**Word-cap overages (10 of 25, disclosed; wording trimmed only, no cited fact or URL cut):** The Heights 534 (+134), 3333 Main Street 508 (+108), Hunter at Lynn Creek 492 (+92), Lynnmour South 490 (+90), Glenkirk Court 482 (+82), Wedgewood 469 (+69), Coho II 460 (+60), Connect at Nature's Edge 411 (+11), The Independent 407 (+7), Compass 406 (+6), Apex 404 (+4), BrookLynn 402 (+2) — driven by measurement density plus the mandated origin/multi-address disclosures. All other files 251–392 words.

## Per-building detail

### 644. Apex at Seylynn Village — 1500 Fern Street, North Vancouver (lynnmour; condos)
- File: apex-at-seylynn-village--lynnmour-nearby-2026-11-02.md — 3,199 B / 404 w (over +4)
- Origin: Fern Street point; reverse-geocode names 1550 Fern Street (adjacent Beacon tower) — retained as the Fern Street address point, disclosed.
- Measurements (5): walk Lynn Creek Community Recreation Centre 2.9 min/0.22 km; walk Seylynn Park 3.1/0.23; walk Lynnmour Elementary 9.3/0.70; drive Phibbs Exchange 3.5/2.64; drive Save-On-Foods (Park & Tilford) 2.4/1.28.
- NOT CONFIRMED: address-level catchment (no SD44 locator run); frequencies other than R2 unstated; no supermarket sourced inside Lynnmour (§4 anchors across Lynn Creek, disclosed).

### 645. Beacon at Seylynn Village — 1550 Fern Street (lynnmour; condos)
- File: beacon-at-seylynn-village--lynnmour-nearby-2026-11-02.md — 2,951 B / 364 w
- Origin: exact (reverse = 1550 Fern Street).
- Measurements (5): walk CRC 4.7/0.36; walk Seylynn Park 4.9/0.37; walk Lynnmour Elementary 8.6/0.65; drive Phibbs 3.5/2.60; drive Save-On-Foods 2.4/1.24.
- NOT CONFIRMED: same common Lynnmour items as 644.

### 646. BrookLynn — 1496 Charlotte Road (lynnmour; condos)
- File: brooklynn--lynnmour-nearby-2026-11-02.md — 3,218 B / 402 w (over +2)
- Origin: Charlotte Road point; reverse names 1448 Charlotte Road — retained as street point, disclosed.
- Measurements (5): walk CRC 2.3/0.18; walk Seylynn Park 4.1/0.31; walk Lynnmour Elementary 12.1/0.91; drive Phibbs 4.0/2.86; drive Save-On-Foods 2.9/1.50.
- NOT CONFIRMED: same common Lynnmour items.

### 647. Compass at Seylynn Village — 680 Seylynn Crescent (lynnmour; condos)
- File: compass-at-seylynn-village--lynnmour-nearby-2026-11-02.md — 3,246 B / 406 w (over +6)
- Origin: Seylynn Crescent point; reverse names 650 Seylynn Crescent (adjacent building, same crescent) — retained, disclosed.
- Measurements (5): walk CRC 3.9/0.29; walk Seylynn Park 4.1/0.31; walk Lynnmour Elementary 8.0/0.60; drive Phibbs 3.3/2.56; drive Save-On-Foods 2.2/1.20.
- NOT CONFIRMED: same common Lynnmour items.

### 648. Connect at Nature's Edge — 757 Orwell Street (lynnmour; townhomes)
- File: connect-at-natures-edge--lynnmour-nearby-2026-11-02.md — 3,355 B / 411 w (over +11)
- Origin: civic variants discarded (wrong southern Orwell segment); OSM named feature "Connect at Nature's Edge" used — see governance note above.
- Measurements (4): walk Lynnmour Elementary 1.4/0.10; walk Inter River Park 16.2/1.21; drive Phibbs 3.2/1.90; drive Save-On-Foods 4.0/2.29.
- NOT CONFIRMED: origin disclosure; catchment; frequencies; no in-Lynnmour supermarket.

### 649. Hunter at Lynn Creek (west tower) — 1401 Hunter Street (lynnmour; condos)
- File: hunter-at-lynn-creek--lynnmour-nearby-2026-11-02.md — 3,943 B / 492 w (over +92)
- Origin: Hunter Street point reverse-geocoding to 1471 Hunter Street (same development's east tower) — used, disclosed.
- Measurements (8): walk CRC 1.4/0.11; walk Seylynn Park 2.2/0.17; walk Lynnmour Elementary 10.4/0.77; walk Save-On-Foods 11.1/0.83; walk Phibbs 11.5/0.86; drive Save-On 3.0/1.52; drive Lynnmour Elementary 3.7/1.84; drive Phibbs 3.8/2.73. Excluded: degenerate adjacent-point drives (Seylynn Park 0.01 km, CRC 0.07 km); Bridgman Park pair discarded (wrong-segment destination point).
- NOT CONFIRMED: catchment; frequencies except R2; origin disclosure.

### 650. Lynnmour South — 1825 Purcell Way (lynnmour; townhomes)
- File: lynnmour-south--lynnmour-nearby-2026-11-02.md — 3,680 B / 490 w (over +90)
- Origin: substituted after discard — see governance note (1923 Purcell Way segment point, from the complex's 1828 Purcell Way unit address).
- Measurements (9): walk Capilano University 6.2/0.46; walk Inter River Park 9.3/0.68; walk Lynnmour Elementary 13.4/1.01; drive CapU 0.9/0.36; drive Lynnmour Elementary 3.3/1.33; drive Phibbs 3.7/2.12; drive Inter River 8.2/2.11; drive Save-On-Foods 4.8/2.65; drive Rice Lake/LSCR 9.5/4.77. Excluded over-cap walks: Phibbs 2.03 km, Save-On 2.22 km, Rice Lake 5.24 km.
- NOT CONFIRMED: catchment; no grocery anchor within 1 km (Save-On is drive-only); origin substitution.

### 651. Wedgewood (Wedgewood by Polygon) — 717 Premier Street / Orwell Street, V7J 0A5 (lynnmour; townhomes)
- File: wedgewood--lynnmour-nearby-2026-11-02.md — 3,642 B / 469 w (over +69)
- Multi-address: one file; anchor 717 Premier Street; header carries both addresses exactly; anchor choice disclosed.
- Origin: Premier Street segment point (reverse: 873 Premier Street) — used, disclosed.
- Measurements (9): walk Lynnmour Elementary 5.2/0.39; walk Inter River Park 10.7/0.78; walk Seylynn Park 13.3/0.99; drive Lynnmour Elementary 1.6/0.61; drive Seylynn Park 3.3/1.64; drive Phibbs 3.2/1.89; drive Save-On-Foods 4.4/2.43; drive Inter River 9.3/2.73; drive Windsor Secondary 5.9/3.30. Excluded over-cap walks: Phibbs 1.62 km, Save-On 1.69 km, Windsor 2.86 km.
- NOT CONFIRMED: multi-address anchor disclosure; catchment; origin segment disclosure.

### 652. The Heights (Crossmark Projects) — 2505 / 2507 West 37th Avenue, Vancouver (mackenzie-heights; townhomes)
- File: the-heights--mackenzie-heights-nearby-2026-11-02.md — 4,114 B / 534 w (over +134, the batch's largest — 9 kept measurements to Kerrisdale anchors plus disclosures)
- Multi-address: one file; anchor 2505 West 37th Avenue; header carries both addresses exactly; anchor choice disclosed.
- Origin: West 37th Avenue segment point (reverse: 637 West 37th Avenue; longitude fits the 2500 block) — used, disclosed.
- Measurements (9): walk Oakridge–41st Avenue Station 10.2/0.76; drive station 2.1/0.88; drive London Drugs 5.9/3.05; drive Maple Grove Elementary 6.1/3.10; drive Kerrisdale Community Centre 6.2/3.24; drive Magee Secondary 7.0/3.67; drive Save-On-Foods Kerrisdale 7.0/3.84; drive McKechnie Elementary 8.7/4.66; drive Maple Grove Park 8.5/4.73. Excluded over-cap walks: seven (2.99–4.64 km).
- NOT CONFIRMED: catchment; frequencies; Save-On-Foods Kerrisdale (6455 West Boulevard) from the retailer's own-domain search result — accepted fallback, disclosed in-file.

### 653. 3333 Main Street — 3333 Main Street, Vancouver (main; condos — unnamed in notes)
- File: 3333-main-street--main-nearby-2026-11-02.md — 3,855 B / 508 w (over +108)
- Origin: exact (reverse = 3333 Main Street).
- Measurements (10): walk Save-On-Foods Main 5.0/0.37; walk Mount Pleasant Community Centre 15.4/1.16; walk Tupper Secondary 15.6/1.17; walk Mount Pleasant Elementary 19.5/1.46; drive Save-On 1.3/0.49; drive MPCC 2.5/1.19; drive Tupper 3.2/1.29; drive MP Elementary 3.4/1.51; drive General Brock Elementary 3.7/1.72; drive Main St–Science World Station 3.8/2.06. Excluded: degenerate Shoppers pairs (0.01/0.06 km); over-cap walks (General Brock 1.62 km, station 2.00 km); Robson Park pair discarded (wrong-segment point).
- NOT CONFIRMED: catchment; no exchange/loop named on an operator page read; Save-On-Foods Main (2949 Main Street) from retailer own-domain search result — accepted fallback, disclosed.

### 654. Cartier Place — 3131 Main Street (main; condos)
- File: cartier-place--main-nearby-2026-11-02.md — 2,933 B / 373 w
- Origin: exact.
- Measurements (5): walk Shoppers Drug Mart (3303 Main) 2.6/0.20; walk Mount Pleasant Park 5.5/0.41; walk Mount Pleasant Elementary 16.8/1.26; drive MPCC 1.9/0.92; drive MP Elementary 2.8/1.24. Excluded: drive Shoppers 0.6/0.25 (walk listed instead).
- NOT CONFIRMED: catchment; frequencies; no exchange named; Safeway 1780 East Broadway is a retailer-search-result anchor beyond ~1 km (disclosed); no in-radius supermarket confirmed.

### 655. E15 Just Off Main — 322 East 15th Avenue, at Sophia Street (main; townhomes)
- File: e15-just-off-main--main-nearby-2026-11-02.md — 3,057 B / 392 w
- Origin: exact.
- Measurements (4): walk Shoppers 5.6/0.42; walk MPCC 13.0/0.97; walk MP Elementary 14.5/1.09; drive MPCC 2.7/1.21. Excluded: drive Shoppers (walk listed); a walk to 2390 Brunswick St (destination not carried in §§1–4).
- NOT CONFIRMED: same Main common items as 654.

### 656. The Independent (The Independent at Main) — 285 East 10th Avenue (also 2508 Watson Street) (main; condos)
- File: the-independent--main-nearby-2026-11-02.md — 3,193 B / 407 w (over +7)
- Multi-address: one file; anchor 285 East 10th Avenue; header carries both addresses exactly; anchor choice disclosed.
- Origin: exact.
- Measurements (5): walk MPCC 4.9/0.37; walk MP Elementary 7.9/0.60; walk Main St–Science World Station 17.7/1.33; drive MP Elementary 2.0/0.74; drive station 2.5/1.38. Excluded: drive MPCC (walk listed); Brunswick St walk (destination not carried).
- NOT CONFIRMED: same Main common items; filed under main only, as rostered.

### 657. Coho (Coho in Osprey Village) — 11067 Barnston View Road, Pitt Meadows (mid-meadows-pitt-meadows; townhomes)
- File: coho--mid-meadows-pitt-meadows-nearby-2026-11-02.md — 3,150 B / 380 w
- §5: NOT MEASURED (fallback bullet). Origin discarded: all four foreground variants returned the same Barnston View Road street point, which reverse-geocodes to 10973 Barnston View Road (a different building). Five computed pairs discarded with the origin; the Athletic Park walk (2.08 km) also exceeded the walk cap.
- NOT CONFIRMED: origin failure disclosed; catchment; frequencies; no Osprey Village grocery/pharmacy confirmed from a retailer's own site.

### 658. Coho II (Coho Chapter II) — 19572 Fraser Way, Pitt Meadows (mid-meadows-pitt-meadows; townhomes)
- File: coho-ii--mid-meadows-pitt-meadows-nearby-2026-11-02.md — 3,745 B / 460 w (over +60)
- Origin: Fraser Way street-level point (reverse: Fraser Way, Pitt Meadows); a second point ~0.45 km east from a structured variant disclosed in-file.
- Measurements (5): walk South Bonson Community Centre 10.7/0.81; drive Pitt Meadows Athletic Park 3.1/2.12; drive Pitt Meadows Secondary 4.3/2.38; drive Edith McDermott Elementary 5.1/3.57; drive Meadowtown Centre 6.2/4.61. Excluded: drive South Bonson (walk listed). Athletic Park destination is a Bonson Road street point (City page supplies 11431 Bonson Road), disclosed.
- NOT CONFIRMED: dual-point disclosure; catchment; no in-village grocery confirmed; Superstore carried from Meadowtown Centre's own site plan.

### 659. Nature's Walk (Onni Group) — 19451 Sutton Avenue, Pitt Meadows (mid-meadows-pitt-meadows; townhomes)
- File: natures-walk--mid-meadows-pitt-meadows-nearby-2026-11-02.md — 2,901 B / 341 w
- Origin: Sutton Avenue street-level point (reverse: Sutton Avenue, Pitt Meadows), disclosed.
- Measurements (5 listed of 7 routed): walk Shoreline Park 11.1/0.77; walk South Bonson CC 8.8/0.66; drive Athletic Park; drive Edith McDermott Elementary; drive Meadowtown Centre (drive distances/times in file). Two in-cap drives (Shoreline Park, South Bonson) measured but left unlisted for word count.
- NOT CONFIRMED: catchment; frequencies; no grocery within ~1 km from a retailer's own site.

### 660. Shoreline — 19452 Fraser Way, Pitt Meadows (mid-meadows-pitt-meadows; townhomes)
- File: shoreline--mid-meadows-pitt-meadows-nearby-2026-11-02.md — 3,038 B / 368 w
- Origin: Fraser Way street-level point, disclosed.
- Measurements (5): walk South Bonson CC 4.8/0.36; drive Shoreline Park; drive Athletic Park; drive Davie Jones Elementary; drive Meadowtown Centre. Excluded: walk to Shoreline Park 5.8 min/0.37 km ≈ 3.8 km/h — outside the sanity band, re-checked once with the identical result, walk discarded and drive kept (disclosed in-file).
- NOT CONFIRMED: catchment; the discarded walk; no in-radius grocery from a retailer's own site.

### 661. Archer Green — 8335 Nelson Street, Mission (mission-homes-for-sale; townhomes)
- File: archer-green--mission-homes-for-sale-nearby-2026-11-02.md — 2,734 B / 347 w
- Origin: Nelson Street street-level point (reverse: Nelson Street, West Heights, Mission), disclosed.
- Measurements (5): walk Mission Sports Park 18.0/1.35; drive West Heights Elementary; drive Kinsmen West Park; drive Mission Leisure Centre; drive Save-On-Foods. Excluded: walk to West Heights Elementary 2.48 km (over cap; drive kept).
- NOT CONFIRMED: catchment; frequencies; no grocery/shopping anchor within ~1 km confirmed; no exchange separate from Mission City Station confirmed on a BC Transit page.

### 662. Briskham Hill — 7540 Briskham Street, Mission (mission-homes-for-sale; townhomes)
- File: briskham-hill--mission-homes-for-sale-nearby-2026-11-02.md — 2,722 B / 344 w
- Origin: the identical Briskham Street segment point Nominatim returns for both 7540 and 7554 — shared with entry 663, disclosed in both files.
- Measurements (6): walk West Heights Elementary 19.5/1.46; walk Mission Leisure Centre 15.7/1.17; drive Save-On-Foods; drive Superstore; drive Griner Park; drive Mission Library. Also measured in-cap but unlisted: three drives. Excluded: walk to Save-On-Foods 2.64 km (over cap).
- NOT CONFIRMED: shared-origin disclosure; catchment; frequencies; Save-On-Foods address from retailer own-domain search result (accepted fallback, disclosed).

### 663. Briskham Manor — 7554 Briskham Street, Mission (mission-homes-for-sale; condos)
- File: briskham-manor--mission-homes-for-sale-nearby-2026-11-02.md — 2,721 B / 344 w
- Origin: same shared Briskham Street point as 662, disclosed.
- Measurements (6): identical §5 set to 662 by construction (same origin): walk West Heights Elementary 19.5/1.46; walk Mission Leisure Centre 15.7/1.17; drive Save-On-Foods; drive Superstore; drive Griner Park; drive Mission Library.
- NOT CONFIRMED: shared-origin disclosure; catchment; frequencies; Save-On fallback sourcing.

### 664. Cedar Valley Manor — 8358 Cedar St, Mission (mission-homes-for-sale; 55-plus, life lease class in header only)
- File: cedar-valley-manor--mission-homes-for-sale-nearby-2026-11-02.md — 2,424 B / 289 w
- §5: NOT MEASURED (fallback bullet). Origin discarded: Nominatim returned only a Cedar Street segment point also returned for a different Cedar St address, sitting beside the 8955 Cedar St school point.
- NOT CONFIRMED: origin failure disclosed; catchment; frequencies; Save-On-Foods cited as retailer own-domain search result (disclosed).

### 665. Cherry Lane — 32165 Seventh Avenue, Mission (mission-homes-for-sale; 55-plus + townhomes)
- File: cherry-lane--mission-homes-for-sale-nearby-2026-11-02.md — 2,595 B / 292 w
- §5: NOT MEASURED (fallback bullet). Origin discarded: points reverse-geocoded to 33751 7th Avenue (a different address) plus unnumbered 7th Ave segments inconsistent with the 32165 block.
- The file carries NO tenure or unit-count claims (the home file's open tenure/unit conflict was kept out per the facts-only scope).
- NOT CONFIRMED: origin failure disclosed; catchment; frequencies.

### 666. Glenkirk Court — 7436 Stave Lake Street, Mission (mission-homes-for-sale; condos)
- File: glenkirk-court--mission-homes-for-sale-nearby-2026-11-02.md — 3,651 B / 482 w (over +82 — 13 listed measurements)
- Origin: Stave Lake Street street-level point at the 7th Ave end, consistent with the 7436 block, disclosed.
- Measurements (13): walk Heritage Park Middle 5.8/0.43 + drive 1.0/0.40; walk Windebank Elementary 7.2/0.54 + drive 0.8/0.53; walk Fraser River Heritage Park 8.7/0.65 + drive 1.5/0.70; walk Leisure Centre 17.2/1.29 + drive 2.5/1.31; walk Library 16.7/1.25 + drive 2.5/1.38; drive Mission City Station 2.7/1.66; drive Centennial Park 3.5/1.76; drive Superstore 5.7/3.82. Excluded over-cap walks: Station 1.62 km, Centennial 1.55 km, West Heights 3.39 km, Superstore 3.65 km, Save-On 3.78 km; two in-cap drives measured but unlisted (disclosed).
- Destination discards: Mission Senior Secondary / Fraserview Learning Centre points (wrong building) — schools listed unmeasured. Heritage Park Middle carried at the Ministry address 33700 Prentis Ave (see source-discrepancy note above).
- NOT CONFIRMED: catchment (no SD75 locator run); frequencies; the unmeasured schools.

### 668. Mission Manor — 33165 2nd Avenue, Mission (mission-homes-for-sale; condos)
- File: mission-manor--mission-homes-for-sale-nearby-2026-11-02.md — 2,169 B / 251 w
- §5: NOT MEASURED (fallback bullet). Origin discarded: three unnumbered 2nd Avenue segment points at different positions, none reverse-geocoding to 33165 2nd Avenue.
- NOT CONFIRMED: origin failure disclosed; catchment; frequencies.

### 669. Montgomery Condos — 7375 Horne Street, Mission (mission-homes-for-sale; condos)
- File: montgomery-condos--mission-homes-for-sale-nearby-2026-11-02.md — 3,004 B / 382 w
- Origin: Horne Street street-level point, identical across freeform and structured queries, disclosed.
- Measurements (9): walk Mission City Station 8.8/0.66 + drive 2.9/1.20; walk Library 12.0/0.90 + drive 2.8/1.10; walk Mission Central Elementary 14.1/1.06 + drive 4.3/1.76; drive Leisure Centre 4.4/2.03; drive Save-On-Foods 5.8/2.83; drive Superstore 5.9/3.36. Excluded over-cap walks: Leisure Centre 1.71 km, Centennial Park 2.25 km, Save-On 2.26 km, Superstore 2.85 km; Centennial Park drive measured but unlisted (disclosed).
- NOT CONFIRMED: catchment; frequencies; Save-On fallback sourcing (disclosed).
