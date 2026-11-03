# What's Nearby — Phase 2, Batch P2-28 Summary

Production date: 2026-11-02 (all measurements taken 2026-11-02).

**Roster range covered: entries 695–720 — 25 buildings produced.** One entry in the range was skipped (entry 699), so the batch extended one entry past 719 to entry 720 to reach 25 addressed buildings.

**Skipped problem entries in range: entry 699, South Pointe (neilsen-grove; 55-plus) — ADDRESS NOT IN NOTES** (bare-land strata, plan NWS2528; the home file states no single civic address, only the street group Regatta Way / Jibset Bay / Tidewater Bay off Ferry Road). Held for the mop-up batch; its address was not researched. Mop-up list to date: entries 52, 85, 86, 156, 188, 193, 195, 240, 415, 487, 535, 549–552, 627, 632, 643, 667, **699 (new)**.

**Areas:** murrayville 2, neilsen-grove 2, neilsen-grove-guide 6, nordel 13, norgate 2.

**Measurements: 113 listed in §5 (40 walk, 73 drive)**, all measured 2026-11-02 starting at each building's own address or its disclosed origin; every kept walk inside the 4–6 km/h sanity band and the walk ≤1.5 km / drive ≤10 km caps. **HTTP 429s: none** across all five workers. **Roster lines proved wrong on the ground: none** — the roster was never silently corrected. **Word-cap overages: none** (largest file 394 words by disk `wc -w`; a few worker word counts ran 3–6 words above the disk count — immaterial, all files under cap on both counts).

**Seven buildings could not be measured** — Orangewood Country Homes (695), Winchester (696), Fairwinds (703), Westhampton (704), Delta Gardens (708), Delta Gardens townhomes (709) and The Ivy (720): after repeated foreground variants no origin point verified to the building (Murrayville's 48/50 Avenue and Ladner's Admiral Way return only whole-street segments in Nominatim; Winchester's only segments sit in the City of Langley, the wrong municipality, and were discarded; both Delta Gardens addresses — 11501 and 11507 84 Avenue — and 8447 115 Street returned only street segments, so the component-address fallback had nothing to anchor to either; The Ivy's Marine Drive segments centre east of Capilano Mall, inconsistent with the 1273 numbering, and a guessed-postal-code variant returned Nova Scotia points, discarded unused). Each file's §§1–4 are complete and §5 is the brief's single bullet "Travel times: not measured in this pass," with the failure disclosed in NOT CONFIRMED. No neighbouring or adjacent feature's point was substituted for any of them — candidates for a later harmonizing/mop-up pass if a sourced civic point is obtained.

**Multi-address entry:** Delta Gardens (708) — one file; title and (unmeasured) anchor on the first rostered address, 11501 84 Avenue; header carries both addresses exactly as rostered ("11501 84 Avenue (also listed as 11507 84 Avenue)"); anchor choice disclosed in NOT CONFIRMED. Delta Gardens townhomes (709, 8447 115 Street) is a different building and was produced as its own file, kept separate per the roster.

**OSM name-spelling variants (flagged in-file, roster names stand):**
- Pilothouse at Hampton Cove (697): the building's own OSM point is named "Pilot House."
- Equinox (712): OSM name variant "Equinox At Sunstone."
- Lakeside (714): the house point at the exact roster address 10500 Delsom Crescent carries an OSM display segment reading "Eclipse At Sunstone" (the complex across the street); the point is the roster-address house point, used unchanged, flag in NOT CONFIRMED.
- Sunbury Terrace (717): OSM reverse-geocode spells the §3 school "Brook Elementary"; the Ministry name "Brooke Elementary" stands, flagged in-file.

**Other disclosed items:**
- The Admiral Way / Hampton Cove pocket (697, 700–705) sits beyond the 1.5 km walk cap from its anchors: all published times there are drives; the walks that were measured in-band (Charterhouse, Chesapeake Landing, Woodward Landing) are recorded as excluded in each file's NOT CONFIRMED.
- Save-On-Foods addresses rest on the retailer own-domain search-result fallback in the Ladner and Nordel files, disclosed in-file as such (per the brief). A road-name discrepancy is carried in the Neilsen Grove files NOT CONFIRMED: OSM names the Save-On-Foods point's road Ladner Trunk Road at 5186, the retailer's own site states 5186 48th Avenue — the retailer address is what §4 states.
- Neilson Grove Elementary (5500 Admiral Blvd) has no verifiable OSM point (Admiral Boulevard segments only); it appears in §3 from the Ministry list and was not used as a measurement destination in the Ladner files.
- Sunbury Terrace §2: the Sunbury Park destination point is Sunbury Hall, which sits at the park's City address (10409 Dunlop Road) — disclosed in-file. Sunstone Park's named point reverse-geocodes to a playground on Delsom Crescent inside the park area (716/718) and to its playground feature in the named park relation (711–715 set) — same park, points used as-is, disclosed.
- Nordel grocery anchors (Scottsdale Centre / Save-On-Foods Scottsdale) sit ~5.4–7.0 km by measured drive from the Delsom-pocket buildings — the nearest phase-1-confirmed anchors; the files state no grocery within ~1 km was confirmed.
- School catchments are in NOT CONFIRMED in every file (no district locator run for these addresses); bus frequencies likewise unless an operator page read stated them (the R2 RapidBus and SeaBus frequencies in the Norgate files are TransLink-stated).

## Per-building detail

### 695. Orangewood Country Homes (Orangewood) — 21937 48 Avenue, Murrayville, Township of Langley (murrayville; townhomes)
- File: orangewood-country-homes--murrayville-nearby-2026-11-02.md — 2,694 B / 311 w
- Origin: NONE usable — six foreground variants returned only 48 Avenue road segments; wrong-municipality City of Langley segments discarded. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); SD35 catchments; bus frequencies.

### 696. Winchester — 21867 50 Avenue, Murrayville, Township of Langley (murrayville; townhomes)
- File: winchester--murrayville-nearby-2026-11-02.md — 2,665 B / 309 w
- Origin: NONE usable — five variants returned no point at the address; the only returns were City of Langley 50 Avenue segments (wrong municipality), discarded and disclosed. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); SD35 catchments; bus frequencies.

### 697. Pilothouse at Hampton Cove — 5535 Admiral Way, Ladner, Delta (neilsen-grove; condos)
- File: pilothouse-at-hampton-cove--neilsen-grove-nearby-2026-11-02.md — 2,951 B / 380 w
- Origin: the building's own OSM apartments point; reverse-geocoded exactly to 5535 Admiral Way. OSM name variant "Pilot House" flagged; roster name stands.
- Measurements (5, all drive): Ladner Exchange 3.51 km/5.7 min; Save-On-Foods 3.44/6.1; Ladner Pioneer Library 3.46/6.1; Ladner Leisure Centre 3.99/6.7; Delta Secondary 3.79/7.2.
- NOT CONFIRMED: name variant; SD37 catchments; Neilson Grove Elementary point unverifiable (segments only, not measured); Save-On road-name discrepancy; bus frequencies.

### 698. Shorewalk — 4955 River Road, Ladner, Delta (neilsen-grove; condos)
- File: shorewalk--neilsen-grove-nearby-2026-11-02.md — 2,835 B / 355 w
- Origin: OSM house-number point; reverse-geocoded exactly to 4955 River Road.
- Measurements (5): walk Ladner Pioneer Library 0.81 km/10.8 min; walk Save-On-Foods 0.82/10.9; walk Ladner Harbour Park 1.29/17.3; drive Ladner Exchange 2.26/4.6; drive Ladner Leisure Centre 2.74/5.6.
- NOT CONFIRMED: SD37 catchments; Neilson Grove Elementary point unverifiable; Save-On road-name discrepancy; bus frequencies.

### 700. Beaufort Landing — 5551 Admiral Way, Ladner, Delta (neilsen-grove-guide; townhomes)
- File: beaufort-landing--neilsen-grove-guide-nearby-2026-11-02.md — 2,965 B / 369 w
- Origin: OSM house point; reverse-geocoded exactly to 5551 Admiral Way.
- Measurements (4, all drive): Ladner Exchange 3.55 km/5.8 min; Save-On-Foods 3.48/6.1; Ladner Pioneer Library 3.50/6.1; Ladner Leisure Centre 4.03/6.8.
- NOT CONFIRMED: SD37 catchments; Neilson Grove Elementary point unverifiable; Save-On road-name discrepancy; bus frequencies.

### 701. Charterhouse — 5510 Admiral Way, Ladner, Delta (neilsen-grove-guide; townhomes)
- File: charterhouse--neilsen-grove-guide-nearby-2026-11-02.md — 2,741 B / 333 w
- Origin: OSM house node; reverse-geocoded exactly to 5510 Admiral Way.
- Measurements (5, all drive): Ladner Harbour Park 3.42 km/6.1 min; Ladner Exchange 3.70/6.0; Save-On-Foods 3.64/6.4; Delta Secondary 3.98/7.5; Ladner Leisure Centre 4.18/7.0. Walks to both parks measured in-band (3.13 / 2.86 km) but excluded over the walk cap, disclosed.
- NOT CONFIRMED: SD37 catchments; the excluded walks.

### 702. Chesapeake Landing — 5900 Ferry Road, Ladner, Delta (neilsen-grove-guide; townhomes)
- File: chesapeake-landing--neilsen-grove-guide-nearby-2026-11-02.md — 3,045 B / 363 w
- Origin: OSM house node; reverse-geocoded exactly to 5900 Ferry Road.
- Measurements (5, all drive): Ladner Harbour Park 2.43 km/4.5 min; Save-On-Foods 2.69/5.0; Ladner Exchange 3.37/5.8; Delta Secondary 3.04/6.0; Ladner Leisure Centre 3.85/6.8. Walks to Lions Park (2.24 km) and Harbour Park (2.46 km) measured but excluded over cap, disclosed.
- NOT CONFIRMED: SD37 catchments; the excluded walks.

### 703. Fairwinds — 5550 Admiral Way, Ladner, Delta (neilsen-grove-guide; townhomes)
- File: fairwinds--neilsen-grove-guide-nearby-2026-11-02.md — 2,443 B / 288 w
- Origin: NONE available — five foreground variants returned only the Admiral Way road way; no house or named building point for 5550 Admiral Way exists in the service. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); SD37 catchments.

### 704. Westhampton — 5311 Admiral Way, Ladner, Delta (neilsen-grove-guide; townhomes)
- File: westhampton--neilsen-grove-guide-nearby-2026-11-02.md — 2,460 B / 289 w
- Origin: NONE available — six foreground variants (incl. sourced postal code and unit variants) returned only the Admiral Way road segment. §5 = not-measured fallback.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); SD37 catchments.

### 705. Woodward Landing — 5300 Admiral Way, Ladner, Delta (neilsen-grove-guide; townhomes)
- File: woodward-landing--neilsen-grove-guide-nearby-2026-11-02.md — 2,749 B / 335 w
- Origin: OSM house node; reverse-geocoded exactly to 5300 Admiral Way.
- Measurements (5, all drive): Ladner Harbour Park 2.91 km/5.2 min; Save-On-Foods 3.17/5.7; Ladner Exchange 3.50/5.7; Delta Secondary 3.52/6.7; Ladner Leisure Centre 3.98/6.7. Walks to Lions Park (2.66 km) and Harbour Park (2.89 km) measured in-band but excluded over cap, disclosed.
- NOT CONFIRMED: SD37 catchments; the excluded walks.

### 706. Capella — 10595 Delsom Crescent, North Delta, Delta (nordel; townhomes)
- File: capella--nordel-nearby-2026-11-02.md — 2,899 B / 355 w
- Origin: Nominatim house point; reverse-geocoded exactly to 10595 Delsom Crescent.
- Measurements (8): walk Sunstone Park 0.32 km/4.2 min, drive 0.38/0.7; walk Sands Secondary 0.55/6.7, drive 1.69/3.9; walk Gray Elementary 1.03/13.1, drive 2.71/4.7; drive North Delta Recreation Centre 1.78/3.3; drive Scottsdale Centre 5.69/9.3. Walks to the Rec Centre (1.80 km) and Scottsdale over cap — measured, excluded, disclosed.
- NOT CONFIRMED: SD37 catchments; bus frequencies; the excluded walks.

### 707. Cardinal Pointe — 10605 Delsom Crescent, North Delta, Delta (nordel; townhomes)
- File: cardinal-pointe--nordel-nearby-2026-11-02.md — 2,915 B / 357 w
- Origin: Nominatim house point; reverse-geocoded exactly to 10605 Delsom Crescent.
- Measurements (8): walk Sunstone Park 0.23 km/3.0 min, drive 0.22/0.4; walk Sands Secondary 0.64/8.6, drive 1.53/3.6; walk Gray Elementary 1.12/14.9, drive 2.55/4.3; drive Rec Centre 1.61/2.9; drive Scottsdale Centre 5.53/9.0. Walk to Rec Centre (1.64 km) over cap — excluded, disclosed.
- NOT CONFIRMED: SD37 catchments; bus frequencies; the excluded walk.

### 708. Delta Gardens — 11501 84 Avenue (also listed as 11507 84 Avenue), North Delta, Delta (nordel; condos)
- File: delta-gardens--nordel-nearby-2026-11-02.md — 2,268 B / 266 w
- Origin: NONE usable — free-form, postal-code and structured searches for BOTH rostered addresses returned only whole-street 84 Avenue segments; no verifying house point for either, so the component-address fallback could not anchor. A neighbouring building's point was not used. §5 = not-measured fallback; anchor choice (title = first address; header carries both) disclosed in NOT CONFIRMED.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); SD37 catchments; bus frequencies.

### 709. Delta Gardens townhomes — 8447 115 Street, North Delta, Delta (nordel; townhomes)
- File: delta-gardens-townhomes--nordel-nearby-2026-11-02.md — 2,170 B / 249 w
- Origin: NONE usable — free-form and structured searches returned only 115 Street road segments (none at 8447). §5 = not-measured fallback. Kept fully separate from entry 708, as rostered.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); SD37 catchments; bus frequencies.

### 710. Delta Ridge — 11490 84 Avenue, North Delta, Delta (nordel; townhomes)
- File: delta-ridge--nordel-nearby-2026-11-02.md — 3,084 B / 377 w
- Origin: Nominatim terrace point; reverse-geocoded exactly to 11490 84 Avenue.
- Measurements (11): walk Rec Centre 0.28 km/3.8 min, drive 0.29/1.0; walk Richardson Elementary 0.44/5.8, drive 0.54/1.6; walk North Delta Community Park 0.48/6.4, drive 0.47/1.0; walk George Mackie Library 0.68/9.1, drive 0.58/1.2; walk North Delta Secondary 0.92/12.2, drive 0.78/2.0; drive Scottsdale Centre 3.87/6.4.
- NOT CONFIRMED: SD37 catchments; bus frequencies.

### 711. Eclipse at Sunstone — 10489 Delsom Crescent, North Delta, Delta (nordel; townhomes)
- File: eclipse-at-sunstone--nordel-nearby-2026-11-02.md — 2,963 B / 371 w
- Origin: Nominatim house point at 10489 Delsom Crescent, reverse-verified (display includes "Eclipse At Sunstone").
- Measurements (5): walk Sunstone Park 0.30 km/4.0 min; walk Sands Secondary 0.83/10.5; drive Gray Elementary 2.96/5.1; drive Rec Centre 2.03/3.7; drive Scottsdale Centre 5.94/9.7.
- NOT CONFIRMED: SD37 catchments; bus frequencies / nearest stop; no grocery within ~1 km confirmed.

### 712. Equinox — 10415 Delsom Crescent, North Delta, Delta (nordel; townhomes)
- File: equinox--nordel-nearby-2026-11-02.md — 3,063 B / 384 w
- Origin: Nominatim residential building point at 10415 Delsom Crescent, reverse-verified. OSM name variant "Equinox At Sunstone" flagged; roster name stands.
- Measurements (5): walk Sunstone Park 0.17 km/2.3 min; walk Sands Secondary 0.92/12.3; walk George Mackie Library 1.42/19.0; drive Gray Elementary 2.80/5.0; drive Scottsdale Centre 5.78/9.7.
- NOT CONFIRMED: name variant; SD37 catchments; bus frequencies / nearest stop; no grocery within ~1 km confirmed.

### 713. Kaleido — 10735 84 Avenue, North Delta, Delta (nordel; townhomes)
- File: kaleido--nordel-nearby-2026-11-02.md — 3,017 B / 380 w
- Origin: house point at 10735 84 Avenue, reverse-verified.
- Measurements (6): walk Sunstone Park 0.56 km/7.5 min; walk Sands Secondary 0.70/9.3; walk George Mackie Library 0.92/12.3; walk Rec Centre 1.34/17.8; drive Gray Elementary 2.91/5.1; drive Scottsdale Centre 6.50/8.7.
- NOT CONFIRMED: SD37 catchments; bus frequencies / nearest stop; no grocery within ~1 km confirmed.

### 714. Lakeside — 10500 Delsom Crescent, North Delta, Delta (nordel; townhomes)
- File: lakeside--nordel-nearby-2026-11-02.md — 3,100 B / 394 w
- Origin: house point at exactly 10500 Delsom Crescent, reverse-verified; its OSM display segment reads "Eclipse At Sunstone" (the complex across the street) — disclosed in NOT CONFIRMED; roster address/name used unchanged.
- Measurements (5): walk Sunstone Park 0.28 km/3.8 min; walk Sands Secondary 0.81/10.2; drive Gray Elementary 2.96/5.0; drive Rec Centre 2.02/3.6; drive Scottsdale Centre 5.94/9.7.
- NOT CONFIRMED: the display-segment quirk; SD37 catchments; bus frequencies / nearest stop; no grocery within ~1 km confirmed.

### 715. Radiance at Sunstone — 8385 Delsom Way, North Delta, Delta (nordel; townhomes)
- File: radiance-at-sunstone--nordel-nearby-2026-11-02.md — 3,037 B / 384 w
- Origin: house point at 8385 Delsom Way, reverse-verified.
- Measurements (6): walk Sunstone Park 0.41 km/5.5 min; walk Sands Secondary 0.90/12.0; walk George Mackie Library 1.17/15.6; drive Rec Centre 1.53/2.9; drive Gray Elementary 2.46/4.3; drive Scottsdale Centre 5.44/9.0.
- NOT CONFIRMED: SD37 catchments; bus frequencies / nearest stop; no grocery within ~1 km confirmed.

### 716. The Residences at Sunstone Village — 8360 Delsom Way, North Delta, Delta (nordel; condos)
- File: the-residences-at-sunstone-village--nordel-nearby-2026-11-02.md — 2,539 B / 321 w
- Origin: Nominatim apartments point at 8360 Delsom Way; reverse-geocoded exactly to that address.
- Measurements (8): walk Sunstone Park 0.41 km/5.5 min, drive 0.28/0.7; walk Sands Secondary 0.88/11.8, drive 1.50/3.7; walk Gray Elementary 1.36/18.1, drive 2.52/4.5; drive Rec Centre 1.58/3.1; drive Scottsdale Centre 5.49/9.1. Walks to Rec Centre (1.62 km) and Scottsdale (5.12 km) measured but excluded over cap, disclosed.
- NOT CONFIRMED: SD37 catchments; bus frequencies; the excluded walks.

### 717. Sunbury Terrace — 8376 Centre Street, North Delta, Delta (nordel; townhomes)
- File: sunbury-terrace--nordel-nearby-2026-11-02.md — 2,613 B / 333 w
- Origin: house point at 8376 Centre Street; reverse-geocoded exactly to that address.
- Measurements (6): walk Sunbury Park 0.13 km/1.8 min, drive 0.33/0.9; walk Brooke Elementary 1.48/19.7, drive 1.42/2.6; drive Sands Secondary 3.21/6.3; drive Scottsdale Centre 7.00/10.4. Walk to Sands (1.64 km) excluded over cap, disclosed.
- NOT CONFIRMED: SD37 catchments; bus frequencies; OSM spells the school "Brook Elementary" (Ministry name "Brooke Elementary" stands, flagged); Sunbury Park destination point is Sunbury Hall at the park's City address, 10409 Dunlop Road (disclosed).

### 718. Sunstone — 8355 Delsom Way, North Delta, Delta (nordel; townhomes)
- File: sunstone--nordel-nearby-2026-11-02.md — 2,485 B / 313 w
- Origin: house point at 8355 Delsom Way; reverse-geocoded exactly to that address.
- Measurements (8): walk Sunstone Park 0.32 km/4.3 min, drive 0.21/0.4; walk Sands Secondary 0.82/10.9, drive 1.61/3.8; walk Gray Elementary 1.30/17.3, drive 2.62/4.5; drive Rec Centre 1.69/3.1; drive Scottsdale Centre 5.60/9.2. Walks to Rec Centre (1.62 km) and Scottsdale (5.05 km) measured but excluded over cap, disclosed.
- NOT CONFIRMED: SD37 catchments; bus frequencies; the excluded walks.

### 719. The Drive — 1177 Marine Drive, North Vancouver (norgate; condos)
- File: the-drive--norgate-nearby-2026-11-02.md — 2,790 B / 339 w
- Origin: house point at 1177 Marine Drive; reverse-geocoded exactly to that address. Destination points reverse-verified (Capilano Mall and Lions Gate Recreation points reverse to tenants/grounds at the same civic addresses; Norgate Park and Norgate Elementary points reverse to features inside the park/school grounds).
- Measurements (8): walk Norgate Elementary 0.75 km/9.9 min; walk Capilano Mall 0.86/11.4, drive 0.89/1.5; walk Save-On-Foods (879 Marine) 0.86/11.4; walk Norgate Park 0.96/12.8; walk Lions Gate Community Recreation Centre 1.47/19.6, drive 1.70/2.9; drive Carson Graham Secondary 2.06/3.5. Walk to Carson Graham (2.09 km) excluded over cap, disclosed.
- NOT CONFIRMED: SD44 catchments; the excluded walk.

### 720. The Ivy — 1273 Marine Drive, North Vancouver (norgate; condos)
- File: the-ivy--norgate-nearby-2026-11-02.md — 2,300 B / 263 w
- Origin: NONE reliable — repeated foreground variants returned only Marine Drive road segments centred east of Capilano Mall, inconsistent with the 1273 numbering (1177 Marine reverse-verifies west of the mall); a guessed-postal-code variant returned Nova Scotia house points, discarded unused. §5 = not-measured fallback, failure disclosed in NOT CONFIRMED. Roster name/address stand as given.
- Measurements (0).
- NOT CONFIRMED: travel times (origin failure); SD44 catchments.
