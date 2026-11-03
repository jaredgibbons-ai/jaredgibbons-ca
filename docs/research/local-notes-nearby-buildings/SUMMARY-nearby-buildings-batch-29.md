# What's Nearby — Phase 2, Batch P2-29 Summary

Production date: 2026-11-02 (all measurements taken 2026-11-02).

**Roster range covered: entries 721–745 — 25 buildings produced.** Every entry in 721–745 carries a street address, so nothing was skipped and no extension was needed.

**Skipped problem entries in range: none.** Mop-up list to date (unchanged): entries 52, 85, 86, 156, 188, 193, 195, 240, 415, 487, 535, 549–552, 627, 632, 643, 667, 699.

**Areas:** norgate 1, north-delta-homes-for-sale 1, north-maple-ridge 3, north-meadows-pitt-meadows-guide 1, northwest-maple-ridge 1, oakridge-vw 1, pacific-douglas 2, panorama-ridge 3, panorama-ridge-guide 4, park-royal 2, pemberton-nv 5, pitt-meadows-homes-for-sale 1.

**Measurements: 59 listed in §5 (15 walk, 44 drive)**, tallied from the files on disk, all measured 2026-11-02 starting at each building's own address or its disclosed origin; every kept walk inside the 4–6 km/h sanity band and the walk ≤1.5 km / drive ≤10 km caps. **HTTP 429s: none** across all five workers. **Roster lines proved wrong on the ground: none** — the roster was never silently corrected.

**Seventeen buildings could not be measured** — X61 and Sunridge Estates measured; the unmeasured set is Archstone Rockridge (723), Brighton (724), Windfall (725), The Fairways (726), Westbrooke (727), Douglas Point (730), Amson Bloc (731), Nora (734), Panorama Mews (735), Steller Panorama (736), Evelyn by Onni (738), The WestRoyal (739), Belle Isle by Citimark (740), The Drive by Onni (741), Ebb & Flow (742), Mason by Cressey (743) and 12350 Harris Road (745): after repeated foreground variants (free-form, name, structured, sourced-postal-code) Nominatim returned only whole-street road segments for each of these addresses — no house or building point exists in the service — and no neighbouring or adjacent feature's point was substituted for any of them. Each file's §§1–4 are complete and §5 is the brief's single bullet "Travel times: not measured in this pass," with the failure disclosed in NOT CONFIRMED. All seventeen are candidates for a later harmonizing/mop-up pass if a sourced civic point is obtained. The three Silver Valley buildings (723–725) are the densest cluster; Maple Ridge's newer subdivisions are systematically segment-only in the geocoder, as are the Panorama Ridge guide streets (62 Ave / 129 St / 132 St) and the Pemberton NV pocket (Curling Rd / Glenaire Dr / Marine Dr).

**Word-cap overages (3 of 25, disclosed; wording trimmed only, no cited fact or URL cut):** Oakhaus 500 (+100 — 8 measurements, 5 transit routes, 4 schools and the mandated anchor disclosure), Park West at Lions Gate 490 (+90 — the full multi-address header, 10 measurements and the anchor disclosure; trimmed from 552), Berkeley Village 419 (+19). Sunridge Estates was trimmed wording-only from 441 to 399 to land under cap. All other files 257–399 words by disk `wc -w`.

**Multi-address entries (4):**
- The Fairways (726) — one file; title on the first address, 19673 Meadow Gardens Way; header carries both addresses exactly as rostered; neither address has a verifying point, so §5 is the fallback and the anchor choice is disclosed.
- Oakhaus (728) — one file; title keeps the first address (135 West 41st Avenue) but that address has NO verifying house point (only West 41st Avenue road segments centred in Kerrisdale/Shaughnessy, discarded and disclosed), so measurements anchor on the other rostered address, 128 Woodstock Avenue (house point, reverse-geocoded exactly); header carries both exactly as rostered; anchor choice disclosed in NOT CONFIRMED.
- Evelyn by Onni (738) — one file; title + anchor on the first address (768 Arthur Erickson Place); header carries the address exactly as rostered including the parenthetical. A building point exists for a different residence in the same masterplan (866 Arthur Erickson Place, OSM "Evelyn 5 - Forest Edge 2") — a neighbouring residence's point, NOT used, disclosed.
- The WestRoyal (739) — one file; header carries both Taylor Way addresses exactly as rostered; BOTH addresses returned segments only, so neither could anchor — §5 fallback, disclosed.
- Park West at Lions Gate (744) — one file; title on the first address (1633 Capilano Road) but that address has no verifying house point (segments only, discarded), so measurements anchor on the rostered tower address 1632 Lions Gate Lane (house point, reverse-geocoded exactly); the second tower address, 1675 Lions Gate Lane, also reverse-verifies; anchor choice disclosed in NOT CONFIRMED.

**Same-name / separateness handling:** The Drive by Onni (741, pemberton-nv) is a different building from entry 719's The Drive (1177 Marine Drive, norgate, produced in P2-28) — separate file, separation stated in-file. Lakewood Heights (732) and Lakewood Place (733) are separate complexes on the same drive per the roster notes; each origin reverse-geocoded exactly to its OWN address and the separateness is stated in both files.

**OSM name-spelling variants (flagged in-file, roster names stand):**
- Lakewood Heights / Lakewood Place (732/733): OSM reverse-geocode spells the road "Boundary Drive West"; the roster's "W Boundary Drive" stands.
- Berkeley Village (729): the building's own OSM landuse point is named "Berkeley Village Townhomes"; roster name stands.
- Evelyn by Onni (738): the unused 866 Arthur Erickson Place point is OSM-named "Evelyn 5 - Forest Edge 2" (noted only as the reason it was not used).

**Other disclosed items:**
- Destination-point notes: Capilano Mall's point reverse-geocodes to a tenant at 935 Marine Drive and the Save-On-Foods (879 Marine) point reverse-geocodes under Hanes Avenue in the Park West file — both disclosed in-file as the points for those civic addresses; park/school destination points in several files reverse to features inside their own grounds (stated where it occurs).
- Sunridge Estates (722): destination address-level geocodes returned only road segments and were discarded; named school/park feature points were used instead, disclosed. Save-On-Foods 7015 120 St rests on the retailer own-domain search-result fallback, disclosed in-file.
- Berkeley Village (729): Dufferin Park measured to the 2 Avenue segment point at the park's City address (17355 2 Avenue), disclosed in-file; all walks from this building exceeded the walk cap, so §5 is drives only, with the in-band Earl Marriott walk (2.12 km) recorded as excluded.
- Grocery coverage: several files confirm no grocery within ~1 km on an allowed source and carry the area's phase-1-confirmed anchor instead (Maple Ridge files: Save-On-Foods 23981 Dewdney Trunk Rd; Panorama files: Panorama Village, 15127 Highway 10, from the centre's leasing brochure carried from phase 1; 12350 Harris Road: Meadowtown Real Canadian Superstore, 19800 Lougheed Hwy).
- School catchments are in NOT CONFIRMED in every file (no district locator run for these addresses); bus frequencies likewise unless an operator page read stated them (TransLink-stated R2/R6 figures appear where read; TransLink route 733 was read this pass for the north-maple-ridge files).
- The Uplands (737): a Newton Recreation Centre drive (5.15 km / 8.3 min) was measured but not listed, to hold the word cap — noted here for completeness. Worker B's report header tallied its own split as 5 walk / 9 drive; the per-file detail and the disk tally both give 3 walk / 11 drive for that worker's files, and the disk figures govern this summary.

## Per-building detail

### 721. X61 — 1061 Marine Drive, North Vancouver (norgate; condos)
- File: x61--norgate-nearby-2026-11-02.md — 3,080 B / 381 w
- Origin: the building's own OSM apartments point named "X61"; reverse-geocoded exactly to 1061 Marine Drive.
- Measurements (7): walk Capilano Mall 0.69 km/9.2 min; drive Capilano Mall 0.81/2.0; walk Save-On-Foods (879 Marine) 0.69/9.2; walk Norgate Community Elementary 0.94/12.6; walk Norgate Park 1.23/16.4; drive Lions Gate Community Recreation Centre 1.73/3.2; drive Carson Graham Secondary 1.98/4.0.
- NOT CONFIRMED: SD44 catchments; in-band walks to Lions Gate Rec Centre (1.74 km) and Carson Graham (1.93 km) excluded over the walk cap; destination-point disclosures (Capilano Mall point reverse-geocodes to a tenant at 935 Marine Drive; park/school points reverse to features inside their grounds).

### 722. Sunridge Estates — 6712 Baker Road, North Delta, Delta (north-delta-homes-for-sale; townhomes)
- File: sunridge-estates--north-delta-homes-for-sale-nearby-2026-11-02.md — 3,435 B / 399 w
- Origin: Nominatim house point; reverse-geocoded exactly to 6712 Baker Road.
- Measurements (9): walk Cougar Canyon Elementary 0.81 km/10.7 min; walk Seaquam Secondary 1.19/15.9; walk Scottsdale Centre 1.44/19.2; drive Scottsdale Centre 1.29/2.8; drive Sunshine Hills Elementary 1.99/3.9; drive Heath Elementary 2.77/4.7; drive Sunshine Hills Park 2.53/4.8; drive Watershed Park 3.71/5.0; drive Sungod Recreation Centre 5.09/8.3.
- NOT CONFIRMED: SD37 catchments; bus frequencies other than the TransLink-stated R6; five in-band walks excluded over cap (drives published); destination address-level segments discarded, named feature points used; Save-On-Foods 7015 120 St on the retailer own-domain search-result fallback.

### 723. Archstone Rockridge — 13260 236 Street, Maple Ridge (north-maple-ridge; townhomes)
- File: archstone-rockridge--north-maple-ridge-nearby-2026-11-02.md — 2,714 B / 326 w
- Origin: NONE usable — free-form, name, structured and sourced-postal-code variants returned only 236 Street road segments. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); SD42 catchments; bus frequencies; no grocery within ~1 km confirmed (§4 carries the phase-1 Save-On-Foods, 23981 Dewdney Trunk Rd).

### 724. Brighton — 13819 232 Street, Maple Ridge (north-maple-ridge; townhomes)
- File: brighton--north-maple-ridge-nearby-2026-11-02.md — 2,894 B / 345 w
- Origin: NONE usable — same variant classes returned only 232 Street segments; a name search also returned a Brighton, Michigan result, discarded unused. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); SD42 catchments; bus frequencies; no grocery within ~1 km confirmed.

### 725. Windfall — 23183 136 Avenue, Maple Ridge (north-maple-ridge; townhomes)
- File: windfall--north-maple-ridge-nearby-2026-11-02.md — 2,819 B / 334 w
- Origin: NONE usable — free-form, name, structured and postal-code variants returned only 136 Avenue road segments. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); SD42 catchments; bus frequencies; no grocery within ~1 km confirmed.

### 726. The Fairways — 19673 and 19677 Meadow Gardens Way, Pitt Meadows (north-meadows-pitt-meadows-guide; condos)
- File: the-fairways--north-meadows-pitt-meadows-guide-nearby-2026-11-02.md — 2,346 B / 265 w
- Origin: NONE usable — searches for BOTH rostered addresses returned only the Meadow Gardens Way road segment. §5 = not-measured fallback; anchor choice (first address) disclosed.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); anchor choice; SD42 catchments; bus frequencies.

### 727. Westbrooke — 12020 207A Street, Maple Ridge (northwest-maple-ridge; condos)
- File: westbrooke--northwest-maple-ridge-nearby-2026-11-02.md — 2,300 B / 257 w
- Origin: NONE usable — free-form, structured and name searches returned only 207A Street road segments. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); SD42 catchments; bus frequencies.

### 728. Oakhaus — 135 West 41st Avenue / 128 Woodstock Avenue, Vancouver (oakridge-vw; townhomes)
- File: oakhaus--oakridge-vw-nearby-2026-11-02.md — 4,019 B / 500 w — OVER the ~400-word cap, disclosed (wording trimmed twice; no cited fact or URL dropped).
- Origin: the rostered 128 Woodstock Avenue house point, reverse-geocoded exactly to 128 West Woodstock Avenue; the first address (135 W 41st Ave) has no verifying house point — its Kerrisdale/Shaughnessy-centred segments were discarded and disclosed; anchor choice disclosed in NOT CONFIRMED. Title keeps the first address; header carries both.
- Measurements (8): walk Oakridge–41st Avenue Station 0.69 km/9.2 min; drive Station 0.66/1.5; walk Oakridge Park 0.81/10.8; drive Oakridge Park 0.82/1.7; walk Queen Elizabeth Park 1.19/15.9; drive QE Park 1.86/5.4; drive Eric Hamber Secondary 2.06/3.8; drive Sir William Osler Elementary 2.30/4.7.
- NOT CONFIRMED: anchor choice + discarded segments; in-band walks to Hamber (2.03 km) and Osler (2.09 km) excluded over the walk cap; SD39 catchments; bus frequencies.

### 729. Berkeley Village — 16433 19 Avenue, Surrey (pacific-douglas; townhomes)
- File: berkeley-village--pacific-douglas-nearby-2026-11-02.md — 3,195 B / 419 w — OVER the ~400-word cap, disclosed.
- Origin: the building's own OSM landuse point named "Berkeley Village Townhomes" (OSM name variant; roster name stands); reverse-geocode lands on a playground on 19 Avenue inside the complex grounds.
- Measurements (6, all drive): Earl Marriott Secondary 3.69 km/6.8 min; Peninsula Village 3.61/6.8; White Rock Centre 4.93/8.6; South Surrey Recreation & Arts Centre 5.45/9.7; Douglas Elementary 6.27/9.5; Dufferin Park 6.59/9.5 (destination = the 2 Avenue segment point at the park's City address 17355 2 Avenue, disclosed in-file).
- NOT CONFIRMED: OSM name variant; the in-band Earl Marriott walk (2.12 km) and all other walks excluded over the walk cap; SD36 catchments; bus frequencies; no supermarket inside the Douglas ground confirmed.

### 730. Douglas Point — 17516 4 Avenue, Surrey (pacific-douglas; townhomes)
- File: douglas-point--pacific-douglas-nearby-2026-11-02.md — 2,466 B / 290 w
- Origin: NONE usable — all variant classes returned only 4 Avenue road segments in Douglas. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); SD36 catchments; bus frequencies; no supermarket inside the Douglas ground confirmed.

### 731. Amson Bloc — 5937 144 St, Surrey (panorama-ridge; condos)
- File: amson-bloc--panorama-ridge-nearby-2026-11-02.md — 2,380 B / 280 w
- Origin: NONE usable — free-form, name and structured searches returned only 144 Street road segments. §5 = not-measured fallback. (Presale per the roster note.)
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); SD36 catchments; bus frequencies; no grocery within ~1 km confirmed.

### 732. Lakewood Heights — 6211 W Boundary Drive, Surrey (panorama-ridge; 55-plus + townhomes)
- File: lakewood-heights--panorama-ridge-nearby-2026-11-02.md — 3,105 B / 389 w
- Origin: Nominatim house point; reverse-geocoded exactly to 6211 Boundary Drive West — its OWN address, verified distinct from Lakewood Place's point.
- Measurements (7): walk Boundary Park 0.62 km/8.3 min; drive Boundary Park 1.27/2.9; drive Colebrook Elementary 3.24/5.7; drive École Panorama Ridge Secondary 3.12/5.0; drive Newton Exchange 5.50/8.0; drive Panorama Village 7.85/9.8; drive Colebrook Park 6.98/11.5.
- NOT CONFIRMED: SD36 catchments; bus frequencies; OSM road-name variant "Boundary Drive West" (roster stands); 5 in-band walks over the walk cap excluded, disclosed; separateness from Lakewood Place stated.

### 733. Lakewood Place — 6061 W Boundary Drive, Surrey (panorama-ridge; 55-plus + townhomes)
- File: lakewood-place--panorama-ridge-nearby-2026-11-02.md — 3,104 B / 389 w
- Origin: Nominatim house point; reverse-geocoded exactly to 6061 Boundary Drive West — its OWN address, verified distinct from Lakewood Heights' point.
- Measurements (7): walk Boundary Park 0.82 km/10.9 min; drive Boundary Park 1.30/3.5; drive Colebrook Elementary 2.78/4.6; drive École Panorama Ridge Secondary 3.59/5.3; drive Newton Exchange 5.97/8.3; drive Panorama Village 7.38/8.6; drive Colebrook Park 6.51/10.4.
- NOT CONFIRMED: SD36 catchments; bus frequencies; OSM road-name variant "Boundary Drive West" (roster stands); 5 in-band walks over cap excluded, disclosed; separateness from Lakewood Heights stated.

### 734. Nora — 12830 62 Ave, Surrey (panorama-ridge-guide; townhomes)
- File: nora--panorama-ridge-guide-nearby-2026-11-02.md — 2,753 B / 305 w
- Origin: NONE usable — free-form, name and structured (postal-code V3X 0K8, sourced from the program file) searches returned only 62 Avenue road segments. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); SD36 catchments; bus frequencies.

### 735. Panorama Mews — 5867 129 St, Surrey (panorama-ridge-guide; townhomes)
- File: panorama-mews--panorama-ridge-guide-nearby-2026-11-02.md — 2,622 B / 291 w
- Origin: NONE usable — free-form, name and structured (postal-code V3X 0J4, sourced from the program file) searches returned only 129 Street road segments. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); SD36 catchments; bus frequencies.

### 736. Steller Panorama — 5858 132 St, Surrey (panorama-ridge-guide; townhomes)
- File: steller-panorama--panorama-ridge-guide-nearby-2026-11-02.md — 2,495 B / 279 w
- Origin: NONE usable — free-form, structured and postal-code variants returned only 132 Street road segments (reverse-geocoding to other house numbers); name search returned nothing. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); SD36 catchments; bus frequencies; no grocery within ~1 km confirmed (§4 anchor is Panorama Village, 15127 Highway 10, from the centre's leasing brochure).

### 737. The Uplands (Uplands at Panorama Ridge) — 15152 62A Ave, Surrey (panorama-ridge-guide; townhomes)
- File: the-uplands--panorama-ridge-guide-nearby-2026-11-02.md — 3,121 B / 374 w
- Origin: Nominatim house point; reverse-geocoded exactly to 15152 62A Avenue.
- Measurements (5, all drive): Sullivan Heights Park 2.38 km/4.8 min; North Ridge Elementary 4.46/7.6; École Panorama Ridge Secondary 4.79/7.7; Newton Exchange 5.14/8.3; Tamanawis Park 5.82/8.7. (A Newton Recreation Centre drive, 5.15 km/8.3 min, was also measured but not listed, to hold the word cap.)
- NOT CONFIRMED: SD36 catchments; bus frequencies; in-band walks to Sullivan Heights Park (1.67 km) and North Ridge Elementary (3.85 km) excluded over the walk cap; no grocery within ~1 km confirmed.

### 738. Evelyn by Onni — 768 Arthur Erickson Place (with residences also addressed on Arthur Erickson Place, including 788 and 866), West Vancouver (park-royal; condos)
- File: evelyn-by-onni--park-royal-nearby-2026-11-02.md — 2,952 B / 355 w
- Origin: NONE usable — repeated foreground variants for 768 (and 788) returned only Arthur Erickson Place road segments. A building point exists for a different residence in the same masterplan (866 Arthur Erickson Place, OSM "Evelyn 5 - Forest Edge 2") — a neighbouring residence's point, NOT used, disclosed. §5 = not-measured fallback; title + anchor on the first address; header carries the address exactly as rostered including the parenthetical; anchor choice disclosed.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure + anchor disclosure); SD45 catchments; bus frequencies beyond TransLink-stated R2 figures.

### 739. The WestRoyal — 328 Taylor Way and 338 Taylor Way, West Vancouver (park-royal; condos)
- File: the-westroyal--park-royal-nearby-2026-11-02.md — 2,710 B / 319 w
- Origin: NONE usable — repeated foreground variants for BOTH rostered addresses returned only Taylor Way road segments, so neither could anchor. §5 = not-measured fallback; header carries both addresses exactly as rostered; anchor position disclosed.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure at both addresses + anchor disclosure); SD45 catchments; bus frequencies beyond R2 figures.

### 740. Belle Isle by Citimark — 2060 Curling Road, North Vancouver (pemberton-nv; townhomes)
- File: belle-isle-by-citimark--pemberton-nv-nearby-2026-11-02.md — 2,800 B / 321 w
- Origin: NONE usable — free-form, name, postal-code (V7P 0E1, from the home file) and structured variants returned only Curling Road road segments (reverse-geocoding to 2020 Curling Road), discarded and disclosed. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); SD44 catchments; bus frequencies beyond R2/SeaBus figures.

### 741. The Drive by Onni — 1330 Marine Drive, North Vancouver (pemberton-nv; condos)
- File: the-drive-by-onni--pemberton-nv-nearby-2026-11-02.md — 3,060 B / 368 w
- Origin: NONE usable — repeated foreground variants returned only Marine Drive road segments. §5 = not-measured fallback. Kept fully separate from entry 719's The Drive (1177 Marine Drive, norgate); the separation is stated in the file.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); SD44 catchments; bus frequencies other than the R2's; no grocery within ~1 km confirmed (§4 anchors are the area's confirmed anchors, east on Marine Drive).

### 742. Ebb & Flow — 2035 Glenaire Drive, North Vancouver (pemberton-nv; townhomes)
- File: ebb-flow--pemberton-nv-nearby-2026-11-02.md — 3,020 B / 363 w
- Origin: NONE usable — all variant classes returned only Glenaire Drive road segments. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); the roster's DISCLOSED-BASIS flag (basis disclosed in the townhomes home file, noted in-file); SD44 catchments; bus frequencies other than the R2's; no grocery within ~1 km confirmed.

### 743. Mason by Cressey — 2070 Curling Road, North Vancouver (pemberton-nv; townhomes)
- File: mason-by-cressey--pemberton-nv-nearby-2026-11-02.md — 2,964 B / 354 w
- Origin: NONE usable — six foreground variants including a postal-code variant (V7P 0C9, from the home file) and name search returned only Curling Road road segments. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); SD44 catchments; bus frequencies other than the R2's; no grocery within ~1 km confirmed.

### 744. Park West at Lions Gate (by Keltic Canada Development) — 1633 Capilano Road, with tower addresses at 1632 Lions Gate Lane and 1675 Lions Gate Lane, North Vancouver (pemberton-nv; condos)
- File: park-west-at-lions-gate--pemberton-nv-nearby-2026-11-02.md — 3,819 B / 490 w — OVER the ~400-word cap, disclosed (trimmed twice by wording only, from 552; no cited fact or URL dropped).
- Origin: title anchors on the first rostered address (1633 Capilano Road), which has NO verifying house point (road segments only, discarded); measurements anchor on the rostered tower address 1632 Lions Gate Lane — OSM house point, reverse-geocoded exactly to that address; the second tower address (1675 Lions Gate Lane) also reverse-verifies as a house point. Anchor choice disclosed in NOT CONFIRMED. Header carries the address exactly as rostered including the tower addresses.
- Measurements (10): walk Lions Gate Community Recreation Centre 0.24 km/3.2 min, drive 0.19/0.7; walk Capilano Elementary 1.27/16.9, drive 2.01/3.9; walk Park Royal Exchange 1.43/19.0, drive 1.48/2.5; drive Carson Graham Secondary 3.49/5.7; drive Save-On-Foods (879 Marine) 2.37/3.9; drive Capilano Mall 2.32/3.7; drive Sowden Park 2.18/4.1. All walks in the 4.43–4.50 km/h band.
- NOT CONFIRMED: anchor disclosure; in-band walks excluded over the walk cap (Carson Graham 3.29 km, Save-On-Foods 2.09 km, Capilano Mall 2.09 km, Sowden Park 1.89 km); destination-point notes (Capilano Mall point reverse-geocodes to a tenant at 935 Marine Drive; Save-On-Foods point reverse-geocodes under Hanes Avenue — both disclosed in-file); SD44 catchments; bus frequencies other than the R2's.

### 745. 12350 Harris Road — 12350 Harris Road, Pitt Meadows (pitt-meadows-homes-for-sale; condos)
- File: 12350-harris-road--pitt-meadows-homes-for-sale-nearby-2026-11-02.md — 2,883 B / 335 w
- Origin: NONE usable — free-form, structured, abbreviated-street and viewbox-bounded variants returned only Harris Road road segments. §5 = not-measured fallback. Title/header use the address as the name, exactly as rostered (UNNAMED IN NOTES; precedent: entry 299).
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); building name unconfirmed in the home file (address used as name, stated in-file); SD42 catchments; bus frequencies; no grocery within ~1 km confirmed (§4 anchor is the Meadowtown Real Canadian Superstore, 19800 Lougheed Hwy).
