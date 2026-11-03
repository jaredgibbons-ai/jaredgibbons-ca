# What's Nearby — Phase 2, Batch P2-31 Summary

Built Nov 2, 2026 (measurement date 2026-11-02) under PHASE2-BRIEF.md. One file per building in `~/workspace/local-notes/nearby/buildings/`; this batch's files are also in `~/workspace/local-notes/nearby-buildings-batch-31.zip`.

## Batch scope

- **Roster entries covered: 771–796** — 25 addressed buildings produced (quay 10, queen-mary-park-surrey 15).
- **Skipped: entry 780, Riviera (quay, condos) — ADDRESS CONFLICT: 1245 Quayside Drive / 1185 Quayside Drive.** Not produced; held for the final mop-up batch. Extension to entry 796 (Tamaron) was needed to reach 25. Entry 797 (Westwood Estates, ADDRESS CONFLICT) was not reached and remains in the unproduced range.
- **Mop-up list to date: entries 52, 85, 86, 156, 188, 193, 195, 240, 415, 487, 535, 549–552, 627, 632, 643, 667, 699, 780.**
- **Measurements listed in §5: 233 (91 walk, 142 drive)**, all measured 2026-11-02 from each building's own address or its disclosed origin; every kept walk inside the 4–6 km/h sanity band and the walk ≤1.5 km / drive ≤10 km caps.
- **HTTP 429s: none** (Nominatim, OSRM, routed-foot all clean).
- **Roster lines proved wrong on the ground: none** — the roster was never silently corrected. No file used the §5 fallback; every building was measured.
- **Process note:** the first routing run's output file was lost before it could be read (the write had not been flushed to disk when the session closed); the full pass was re-run with an fsync'd write and read back from disk before drafting. All §5 figures come from the completed on-disk output.

## Geocode governance (all disclosed in-file)

- Four origins are **segment-interpolated** under the P2-30 method (Gabriel 787, Galilea 788, Kennedy Trail 790, Quinn 794): Nominatim holds no house point for these addresses — only whole-street segments, and name/structured/postal variants returned nothing usable. Each origin sits on the building's own street segment, bracketed by real OSM address points on that street, and reverse-geocodes to that street (787 → 13461 94A Ave; 788 → 13454 95 Ave; 790 → 8343 121A St; 794 → 13437 94A Ave). All four are recorded as re-measurement candidates if a sourced civic point set becomes available. No neighbouring or same-masterplan building's point was substituted for any origin.
- **Pier West (773):** measured from the building's own named OSM point 'Pier West 2' at the roster address 660 Quayside Drive (Marquee/Lakeside named-point precedent). The condos home file records that address as the project sales centre and the completion status as UNCONFIRMED; the file flags this and confirms nothing about completion.
- **Kennedy Trail Elementary address variant:** the townhomes home file prints 8305 122A Street; the Ministry list form and the OSM point both give 8305 121A Street. The Ministry form is used in all ten southern-cluster files and the variant is disclosed in each file's NOT CONFIRMED.
- **Walks discarded on the sanity band:** Gabriel → Queen Elizabeth Meadows (6.57 km/h) and Quinn → Queen Elizabeth Meadows (6.23 km/h) — drives listed, discards disclosed in-file. All other over-cap walks are disclosed in-file as drives only.
- **Bear Creek Park drives** (787, 788, 794) route to the Surrey Arts Centre point at the park's civic address, 13750 88 Avenue — disclosed in-file.
- **Sterling Court (795)** carries the condos home file's classification conflict in NOT CONFIRMED (West Newton listing vs Queen Mary Park directory); the roster home stands, unresolved.
- **Quinn (794)** also carries the home file's 'Surrey City Centre' marketing-name flag; the roster home stands.
- Multi-address anchors, all disclosed in-file: Laguna Landing (771, anchor 10 Laguna Court), Tiffany Shores (781, anchor 1210 Quayside Drive), Quinn (794, anchor 13439 94A Avenue; the second address, 9456 134 Street, was probe-verified as segment-only too).

## Word-cap overages (disclosed; wording trimmed only, no cited fact or URL cut)

Files over the ~400-word cap: entry 771 Laguna Landing 531 (+131); entry 772 Murano Lofts 505 (+105); entry 773 Pier West 515 (+115); entry 774 The Promenade 507 (+107); entry 775 The Q 509 (+109); entry 776 Quay West 487 (+87); entry 777 Quayside Terrace 497 (+97); entry 778 RiverSky 1 476 (+76); entry 779 RiverSky 2 476 (+76); entry 781 Tiffany Shores 523 (+123); entry 782 Barkerville II 405 (+5); entry 784 Bonnydoon Village 465 (+65); entry 787 Gabriel 441 (+41); entry 788 Galilea 424 (+24); entry 790 Kennedy Trail (Kennedy Trails) 445 (+45); entry 791 Kennedy Woods 405 (+5); entry 792 Lakewood Grove 405 (+5); entry 794 Quinn by Porte (Quinn by Porte Homes) 519 (+119); entry 795 Sterling Court 428 (+28). All are driven by measurement density (10–13 listed measurements in the Quay files) on top of the mandated origin/multi-address disclosures. All other files are at or under 405 words (782, 791, 792 at 405, +5).

## Per-building detail

### 771. Laguna Landing — 10 Laguna Court (anchor of 10 and 12 Laguna Court)
- File: `laguna-landing--quay-nearby-2026-11-02.md` — 3732 bytes, 531 words (OVER CAP +131). Sections 1–5 all written; none omitted.
- Origin: House point, reverse-geocode confirms the roster address.
- Measurements (3 walk, 7 drive): Walk to New Westminster Station: 14.1 min, 1.05 km; Drive to New Westminster Station: 3.3 min, 1.38 km; Drive to Columbia Station: 4.5 min, 1.84 km; Drive to Westminster Pier Park: 5.2 min, 1.82 km; Walk to Anvil Centre, 777 Columbia St: 16.0 min, 1.2 km; Drive to Anvil Centre, 777 Columbia St: 3.2 min, 1.35 km; Walk to Shops at New West, 800 Carnarvon St: 14.4 min, 1.08 km; Drive to Shops at New West, 800 Carnarvon St: 3.3 min, 1.38 km; Drive to École Qayqayt Elementary, 85 Merivale St: 4.9 min, 2.38 km; Drive to Fraser River Middle, 800 Queens Ave: 4.0 min, 1.6 km.
- NOT CONFIRMED highlights: Catchments; frequencies; Save-On-Foods Columbia Square + River Market addresses unconfirmed (phase-1); multi-address anchor disclosure; over-cap walks to Columbia Station, Westminster Pier Park and École Qayqayt listed as drives only.

### 772. Murano Lofts — 7 Rialto Court
- File: `murano-lofts--quay-nearby-2026-11-02.md` — 3571 bytes, 505 words (OVER CAP +105). Sections 1–5 all written; none omitted.
- Origin: House point, reverse-geocode confirms the roster address.
- Measurements (3 walk, 7 drive): Walk to New Westminster Station: 15.9 min, 1.19 km; Drive to New Westminster Station: 4.0 min, 1.89 km; Drive to Columbia Station: 4.5 min, 2.34 km; Drive to Westminster Pier Park: 5.1 min, 2.37 km; Walk to Anvil Centre, 777 Columbia St: 17.8 min, 1.34 km; Drive to Anvil Centre, 777 Columbia St: 3.4 min, 1.63 km; Walk to Shops at New West, 800 Carnarvon St: 16.2 min, 1.22 km; Drive to Shops at New West, 800 Carnarvon St: 4.0 min, 1.89 km; Drive to École Qayqayt Elementary, 85 Merivale St: 4.6 min, 2.31 km; Drive to Fraser River Middle, 800 Queens Ave: 3.2 min, 1.31 km.
- NOT CONFIRMED highlights: Catchments; frequencies; Save-On-Foods Columbia Square + River Market addresses unconfirmed (phase-1); over-cap walks to Columbia Station, Westminster Pier Park and École Qayqayt listed as drives only.

### 773. Pier West — 660 Quayside Drive
- File: `pier-west--quay-nearby-2026-11-02.md` — 3689 bytes, 515 words (OVER CAP +115). Sections 1–5 all written; none omitted.
- Origin: The building's own named OSM point 'Pier West 2' at the roster address; roster stands (home file records the address as the sales-centre address, completion UNCONFIRMED — flagged in-file).
- Measurements (6 walk, 7 drive): Walk to New Westminster Station: 5.7 min, 0.43 km; Drive to New Westminster Station: 1.5 min, 0.42 km; Walk to Columbia Station: 8.4 min, 0.63 km; Drive to Columbia Station: 2.7 min, 0.92 km; Walk to Westminster Pier Park: 4.1 min, 0.31 km; Drive to Westminster Pier Park: 2.6 min, 0.7 km; Walk to Anvil Centre, 777 Columbia St: 3.8 min, 0.29 km; Drive to Anvil Centre, 777 Columbia St: 1.1 min, 0.28 km; Walk to Shops at New West, 800 Carnarvon St: 6.3 min, 0.47 km; Drive to Shops at New West, 800 Carnarvon St: 1.5 min, 0.42 km; Walk to École Qayqayt Elementary, 85 Merivale St: 14.9 min, 1.12 km; Drive to École Qayqayt Elementary, 85 Merivale St: 3.4 min, 1.34 km; Drive to Fraser River Middle, 800 Queens Ave: 2.6 min, 0.94 km.
- NOT CONFIRMED highlights: Catchments; frequencies; completion status of the building UNCONFIRMED per the condos home file (roster address is the sales-centre address).

### 774. The Promenade — 1250 Quayside Drive
- File: `the-promenade--quay-nearby-2026-11-02.md` — 3605 bytes, 507 words (OVER CAP +107). Sections 1–5 all written; none omitted.
- Origin: House point, reverse-geocode confirms the roster address.
- Measurements (3 walk, 7 drive): Walk to New Westminster Station: 13.1 min, 0.98 km; Drive to New Westminster Station: 3.0 min, 1.21 km; Drive to Columbia Station: 4.2 min, 1.66 km; Drive to Westminster Pier Park: 4.8 min, 1.65 km; Walk to Anvil Centre, 777 Columbia St: 15.0 min, 1.13 km; Drive to Anvil Centre, 777 Columbia St: 2.9 min, 1.17 km; Walk to Shops at New West, 800 Carnarvon St: 13.4 min, 1.01 km; Drive to Shops at New West, 800 Carnarvon St: 2.9 min, 1.2 km; Drive to École Qayqayt Elementary, 85 Merivale St: 4.6 min, 2.2 km; Drive to Fraser River Middle, 800 Queens Ave: 3.5 min, 1.5 km.
- NOT CONFIRMED highlights: Catchments; frequencies; Save-On-Foods Columbia Square + River Market addresses unconfirmed (phase-1); over-cap walks to Columbia Station, Westminster Pier Park and École Qayqayt listed as drives only.

### 775. The Q — 1 Renaissance Square
- File: `the-q--quay-nearby-2026-11-02.md` — 3602 bytes, 509 words (OVER CAP +109). Sections 1–5 all written; none omitted.
- Origin: House point, reverse-geocode confirms the roster address.
- Measurements (3 walk, 7 drive): Walk to New Westminster Station: 14.4 min, 1.08 km; Drive to New Westminster Station: 3.9 min, 1.54 km; Drive to Columbia Station: 5.4 min, 2.58 km; Drive to Westminster Pier Park: 5.8 min, 1.98 km; Walk to Anvil Centre, 777 Columbia St: 16.3 min, 1.22 km; Drive to Anvil Centre, 777 Columbia St: 3.8 min, 1.5 km; Walk to Shops at New West, 800 Carnarvon St: 14.7 min, 1.1 km; Drive to Shops at New West, 800 Carnarvon St: 3.8 min, 1.53 km; Drive to École Qayqayt Elementary, 85 Merivale St: 5.5 min, 2.56 km; Drive to Fraser River Middle, 800 Queens Ave: 4.1 min, 1.56 km.
- NOT CONFIRMED highlights: Catchments; frequencies; Save-On-Foods Columbia Square + River Market addresses unconfirmed (phase-1); over-cap walks to Columbia Station, Westminster Pier Park and École Qayqayt listed as drives only.

### 776. Quay West — 31 Reliance Court
- File: `quay-west--quay-nearby-2026-11-02.md` — 3507 bytes, 487 words (OVER CAP +87). Sections 1–5 all written; none omitted.
- Origin: House point, reverse-geocode confirms the roster address.
- Measurements (5 walk, 7 drive): Walk to New Westminster Station: 8.5 min, 0.63 km; Drive to New Westminster Station: 2.3 min, 0.98 km; Walk to Columbia Station: 18.4 min, 1.38 km; Drive to Columbia Station: 3.5 min, 1.43 km; Walk to Westminster Pier Park: 16.5 min, 1.24 km; Drive to Westminster Pier Park: 4.2 min, 1.42 km; Walk to Anvil Centre, 777 Columbia St: 10.4 min, 0.78 km; Drive to Anvil Centre, 777 Columbia St: 2.2 min, 0.94 km; Walk to Shops at New West, 800 Carnarvon St: 8.8 min, 0.66 km; Drive to Shops at New West, 800 Carnarvon St: 2.3 min, 0.98 km; Drive to École Qayqayt Elementary, 85 Merivale St: 3.9 min, 1.97 km; Drive to Fraser River Middle, 800 Queens Ave: 2.8 min, 1.27 km.
- NOT CONFIRMED highlights: Catchments; frequencies; Save-On-Foods Columbia Square + River Market addresses unconfirmed (phase-1); over-cap walk to École Qayqayt listed as drive only.

### 777. Quayside Terrace — 5 K de K Court
- File: `quayside-terrace--quay-nearby-2026-11-02.md` — 3524 bytes, 497 words (OVER CAP +97). Sections 1–5 all written; none omitted.
- Origin: House point, reverse-geocode confirms the roster address.
- Measurements (5 walk, 7 drive): Walk to New Westminster Station: 6.0 min, 0.45 km; Drive to New Westminster Station: 2.1 min, 0.85 km; Walk to Columbia Station: 15.9 min, 1.2 km; Drive to Columbia Station: 3.3 min, 1.3 km; Walk to Westminster Pier Park: 12.9 min, 0.97 km; Drive to Westminster Pier Park: 3.8 min, 1.29 km; Walk to Anvil Centre, 777 Columbia St: 7.9 min, 0.59 km; Drive to Anvil Centre, 777 Columbia St: 2.3 min, 0.87 km; Walk to Shops at New West, 800 Carnarvon St: 6.3 min, 0.47 km; Drive to Shops at New West, 800 Carnarvon St: 2.0 min, 0.85 km; Drive to École Qayqayt Elementary, 85 Merivale St: 3.7 min, 1.84 km; Drive to Fraser River Middle, 800 Queens Ave: 2.6 min, 1.14 km.
- NOT CONFIRMED highlights: Catchments; frequencies; Save-On-Foods Columbia Square + River Market addresses unconfirmed (phase-1); over-cap walk to École Qayqayt listed as drive only.

### 778. RiverSky 1 — 908 Quayside Drive
- File: `riversky-1--quay-nearby-2026-11-02.md` — 3467 bytes, 476 words (OVER CAP +76). Sections 1–5 all written; none omitted.
- Origin: House point, reverse-geocode confirms the roster address.
- Measurements (6 walk, 7 drive): Walk to New Westminster Station: 3.2 min, 0.24 km; Drive to New Westminster Station: 1.8 min, 0.67 km; Walk to Columbia Station: 13.2 min, 0.99 km; Drive to Columbia Station: 3.0 min, 1.17 km; Walk to Westminster Pier Park: 11.2 min, 0.84 km; Drive to Westminster Pier Park: 2.9 min, 0.95 km; Walk to Anvil Centre, 777 Columbia St: 5.2 min, 0.39 km; Drive to Anvil Centre, 777 Columbia St: 1.4 min, 0.53 km; Walk to Shops at New West, 800 Carnarvon St: 3.5 min, 0.27 km; Drive to Shops at New West, 800 Carnarvon St: 1.8 min, 0.67 km; Walk to École Qayqayt Elementary, 85 Merivale St: 19.1 min, 1.44 km; Drive to École Qayqayt Elementary, 85 Merivale St: 3.7 min, 1.6 km; Drive to Fraser River Middle, 800 Queens Ave: 2.9 min, 1.19 km.
- NOT CONFIRMED highlights: Catchments; frequencies; Save-On-Foods Columbia Square + River Market addresses unconfirmed (phase-1); no walk drops — all routed walks were in cap and in band.

### 779. RiverSky 2 — 988 Quayside Drive
- File: `riversky-2--quay-nearby-2026-11-02.md` — 3468 bytes, 476 words (OVER CAP +76). Sections 1–5 all written; none omitted.
- Origin: House point, reverse-geocode confirms the roster address.
- Measurements (6 walk, 7 drive): Walk to New Westminster Station: 3.1 min, 0.23 km; Drive to New Westminster Station: 1.4 min, 0.58 km; Walk to Columbia Station: 13.0 min, 0.98 km; Drive to Columbia Station: 2.6 min, 1.03 km; Walk to Westminster Pier Park: 11.1 min, 0.83 km; Drive to Westminster Pier Park: 3.0 min, 1.06 km; Walk to Anvil Centre, 777 Columbia St: 5.0 min, 0.38 km; Drive to Anvil Centre, 777 Columbia St: 1.3 min, 0.54 km; Walk to Shops at New West, 800 Carnarvon St: 3.4 min, 0.25 km; Drive to Shops at New West, 800 Carnarvon St: 1.4 min, 0.57 km; Walk to École Qayqayt Elementary, 85 Merivale St: 19.0 min, 1.42 km; Drive to École Qayqayt Elementary, 85 Merivale St: 3.0 min, 1.57 km; Drive to Fraser River Middle, 800 Queens Ave: 1.9 min, 0.87 km.
- NOT CONFIRMED highlights: Catchments; frequencies; Save-On-Foods Columbia Square + River Market addresses unconfirmed (phase-1); no walk drops — all routed walks were in cap and in band.

### 781. Tiffany Shores — 1210 Quayside Drive (anchor of 1210/1220/1230/1240)
- File: `tiffany-shores--quay-nearby-2026-11-02.md` — 3748 bytes, 523 words (OVER CAP +123). Sections 1–5 all written; none omitted.
- Origin: House point at the first rostered address, reverse-geocode confirms it.
- Measurements (5 walk, 7 drive): Walk to New Westminster Station: 9.6 min, 0.72 km; Drive to New Westminster Station: 2.4 min, 1.05 km; Walk to Columbia Station: 19.5 min, 1.46 km; Drive to Columbia Station: 3.7 min, 1.5 km; Walk to Westminster Pier Park: 17.6 min, 1.32 km; Drive to Westminster Pier Park: 4.3 min, 1.49 km; Walk to Anvil Centre, 777 Columbia St: 11.5 min, 0.86 km; Drive to Anvil Centre, 777 Columbia St: 2.4 min, 1.02 km; Walk to Shops at New West, 800 Carnarvon St: 9.9 min, 0.74 km; Drive to Shops at New West, 800 Carnarvon St: 2.4 min, 1.05 km; Drive to École Qayqayt Elementary, 85 Merivale St: 4.1 min, 2.05 km; Drive to Fraser River Middle, 800 Queens Ave: 3.0 min, 1.34 km.
- NOT CONFIRMED highlights: Catchments; frequencies; multi-address anchor disclosure; over-cap walk to École Qayqayt listed as drive only.

### 782. Barkerville II — 8220 121A Street
- File: `barkerville-ii--queen-mary-park-surrey-nearby-2026-11-02.md` — 2832 bytes, 405 words (OVER CAP +5). Sections 1–5 all written; none omitted.
- Origin: House point, reverse-geocode confirms the roster address.
- Measurements (3 walk, 4 drive): Walk to Kennedy Trail Elementary, 8305 121A St: 5.7 min, 0.42 km; Drive to Kennedy Trail Elementary, 8305 121A St: 1.6 min, 0.58 km; Walk to Kennedy Trail Park, 12237 82 Ave: 3.5 min, 0.26 km; Drive to Kennedy Trail Park, 12237 82 Ave: 0.7 min, 0.29 km; Drive to Strawberry Hill Park, 7676 122 St: 3.5 min, 1.8 km; Walk to Real Canadian Superstore, 8195 120 St: 6.6 min, 0.49 km; Drive to Real Canadian Superstore, 8195 120 St: 2.0 min, 0.73 km.
- NOT CONFIRMED highlights: Catchments; frequencies; Kennedy Trail Elementary address variant (as per 790); over-cap walk to Strawberry Hill Park listed as drive only; no grocery anchor within 1 km confirmed from an allowed source.

### 783. The Birches — 8139 121A Street
- File: `the-birches--queen-mary-park-surrey-nearby-2026-11-02.md` — 2761 bytes, 391 words. Sections 1–5 all written; none omitted.
- Origin: House point, reverse-geocode confirms the roster address.
- Measurements (4 walk, 4 drive): Walk to Kennedy Trail Elementary, 8305 121A St: 7.4 min, 0.55 km; Drive to Kennedy Trail Elementary, 8305 121A St: 1.6 min, 0.64 km; Walk to Kennedy Trail Park, 12237 82 Ave: 4.8 min, 0.36 km; Drive to Kennedy Trail Park, 12237 82 Ave: 0.7 min, 0.35 km; Walk to Strawberry Hill Park, 7676 122 St: 20.0 min, 1.5 km; Drive to Strawberry Hill Park, 7676 122 St: 3.5 min, 1.86 km; Walk to Real Canadian Superstore, 8195 120 St: 7.4 min, 0.55 km; Drive to Real Canadian Superstore, 8195 120 St: 2.1 min, 0.8 km.
- NOT CONFIRMED highlights: Catchments; frequencies; Kennedy Trail Elementary address variant (as per 790); no grocery anchor within 1 km confirmed from an allowed source.

### 784. Bonnydoon Village — 9378 122 Street
- File: `bonnydoon-village--queen-mary-park-surrey-nearby-2026-11-02.md` — 3324 bytes, 465 words (OVER CAP +65). Sections 1–5 all written; none omitted.
- Origin: House point, reverse-geocode confirms the roster address.
- Measurements (1 walk, 8 drive): Drive to Queen Mary Park, 8972 Queen Mary Blvd: 5.8 min, 3.35 km; Walk to L.A. Matheson Secondary, 9484 122 St: 4.2 min, 0.31 km; Drive to L.A. Matheson Secondary, 9484 122 St: 1.8 min, 0.5 km; Drive to David Brankin Elementary, 9160 128 St: 3.3 min, 1.77 km; Drive to Kirkbride Elementary, 12150 92 Ave: 1.3 min, 0.48 km; Drive to Kennedy Trail Park, 12237 82 Ave: 5.1 min, 3.25 km; Drive to Real Canadian Superstore, 8195 120 St: 5.3 min, 3.15 km; Drive to King George Station: 6.7 min, 3.97 km; Drive to Queen Elizabeth Secondary, 9457 King George Blvd: 6.5 min, 3.74 km.
- NOT CONFIRMED highlights: Catchments; frequencies; listings also recorded at 9370/9400/9402 122 St (roster address stands); over-cap walk to Queen Mary Park listed as drive only.

### 785. The Crossing — 8115 121A Street
- File: `the-crossing--queen-mary-park-surrey-nearby-2026-11-02.md` — 2762 bytes, 391 words. Sections 1–5 all written; none omitted.
- Origin: House point, reverse-geocode confirms the roster address.
- Measurements (4 walk, 4 drive): Walk to Kennedy Trail Elementary, 8305 121A St: 8.0 min, 0.6 km; Drive to Kennedy Trail Elementary, 8305 121A St: 1.9 min, 0.7 km; Walk to Kennedy Trail Park, 12237 82 Ave: 5.4 min, 0.41 km; Drive to Kennedy Trail Park, 12237 82 Ave: 0.9 min, 0.41 km; Walk to Strawberry Hill Park, 7676 122 St: 19.3 min, 1.45 km; Drive to Strawberry Hill Park, 7676 122 St: 3.7 min, 1.92 km; Walk to Real Canadian Superstore, 8195 120 St: 8.0 min, 0.6 km; Drive to Real Canadian Superstore, 8195 120 St: 2.3 min, 0.85 km.
- NOT CONFIRMED highlights: Catchments; frequencies; Kennedy Trail Elementary address variant (as per 790); no grocery anchor within 1 km confirmed from an allowed source.

### 786. Eclipse — 8084 120A Street
- File: `eclipse--queen-mary-park-surrey-nearby-2026-11-02.md` — 2755 bytes, 389 words. Sections 1–5 all written; none omitted.
- Origin: House point, reverse-geocode confirms the roster address.
- Measurements (4 walk, 4 drive): Walk to Kennedy Trail Elementary, 8305 121A St: 9.6 min, 0.72 km; Drive to Kennedy Trail Elementary, 8305 121A St: 1.9 min, 0.91 km; Walk to Kennedy Trail Park, 12237 82 Ave: 7.0 min, 0.52 km; Drive to Kennedy Trail Park, 12237 82 Ave: 1.0 min, 0.61 km; Walk to Strawberry Hill Park, 7676 122 St: 17.6 min, 1.32 km; Drive to Strawberry Hill Park, 7676 122 St: 2.6 min, 1.16 km; Walk to Real Canadian Superstore, 8195 120 St: 7.4 min, 0.55 km; Drive to Real Canadian Superstore, 8195 120 St: 1.7 min, 0.72 km.
- NOT CONFIRMED highlights: Catchments; frequencies; Kennedy Trail Elementary address variant (as per 790); no grocery anchor within 1 km confirmed from an allowed source.

### 787. Gabriel — 13455 94A Avenue (interpolated segment origin, reverse: 13461 94A Ave)
- File: `gabriel--queen-mary-park-surrey-nearby-2026-11-02.md` — 3075 bytes, 441 words (OVER CAP +41). Sections 1–5 all written; none omitted.
- Origin: No Nominatim house point exists for 13455 94A Ave; P2-30 segment interpolation between OSM address points 13427 and 13605 94A Ave, disclosed in-file. Segment-grade origin — candidate for re-measurement if a sourced civic point set becomes available.
- Measurements (2 walk, 6 drive): Drive to Queen Elizabeth Meadows, 9400 134 St: 1.8 min, 0.78 km; Walk to Queen Elizabeth Secondary, 9457 King George Blvd: 3.8 min, 0.28 km; Drive to Queen Elizabeth Secondary, 9457 King George Blvd: 2.0 min, 0.64 km; Drive to Bear Creek Park, 13750 88 Ave: 3.6 min, 2.18 km; Walk to King George Station: 18.1 min, 1.36 km; Drive to King George Station: 2.2 min, 1.24 km; Drive to Surrey Central Station: 4.0 min, 2.16 km; Drive to Central City, 10153 King George Blvd: 4.8 min, 2.05 km.
- NOT CONFIRMED highlights: Catchments; frequencies; R1 RapidBus not confirmed from an operator page read; walk to Queen Elizabeth Meadows discarded (6.57 km/h, outside the sanity band), drive listed; Bear Creek Park routed to the Surrey Arts Centre point at the park's civic address.

### 788. Galilea — 13458 95 Avenue (interpolated segment origin, reverse: 13454 95 Ave)
- File: `galilea--queen-mary-park-surrey-nearby-2026-11-02.md` — 2977 bytes, 424 words (OVER CAP +24). Sections 1–5 all written; none omitted.
- Origin: No Nominatim house point exists for 13458 95 Ave; P2-30 segment interpolation between OSM address points 13445 and 13474 95 Ave, disclosed in-file. Segment-grade origin — re-measurement candidate as above.
- Measurements (3 walk, 6 drive): Walk to Queen Elizabeth Meadows, 9400 134 St: 3.4 min, 0.33 km; Drive to Queen Elizabeth Meadows, 9400 134 St: 1.9 min, 0.87 km; Walk to Queen Elizabeth Secondary, 9457 King George Blvd: 5.1 min, 0.38 km; Drive to Queen Elizabeth Secondary, 9457 King George Blvd: 1.7 min, 0.54 km; Drive to Bear Creek Park, 13750 88 Ave: 3.8 min, 2.27 km; Walk to King George Station: 16.9 min, 1.27 km; Drive to King George Station: 2.0 min, 1.15 km; Drive to Surrey Central Station: 3.8 min, 2.08 km; Drive to Central City, 10153 King George Blvd: 4.6 min, 1.96 km.
- NOT CONFIRMED highlights: Catchments; frequencies; R1 not confirmed from an operator page read; Bear Creek Park routed to the Surrey Arts Centre point at the park's civic address.

### 789. Hadley Green — 8060 121A Street
- File: `hadley-green--queen-mary-park-surrey-nearby-2026-11-02.md` — 2768 bytes, 391 words. Sections 1–5 all written; none omitted.
- Origin: House point, reverse-geocode confirms the roster address.
- Measurements (4 walk, 4 drive): Walk to Kennedy Trail Elementary, 8305 121A St: 10.0 min, 0.75 km; Drive to Kennedy Trail Elementary, 8305 121A St: 2.7 min, 1.27 km; Walk to Kennedy Trail Park, 12237 82 Ave: 7.4 min, 0.56 km; Drive to Kennedy Trail Park, 12237 82 Ave: 1.7 min, 0.98 km; Walk to Strawberry Hill Park, 7676 122 St: 17.0 min, 1.27 km; Drive to Strawberry Hill Park, 7676 122 St: 2.9 min, 1.22 km; Walk to Real Canadian Superstore, 8195 120 St: 9.4 min, 0.7 km; Drive to Real Canadian Superstore, 8195 120 St: 1.8 min, 0.78 km.
- NOT CONFIRMED highlights: Catchments; frequencies; Kennedy Trail Elementary address variant (as per 790); no grocery anchor within 1 km confirmed from an allowed source.

### 790. Kennedy Trail (Kennedy Trails) — 8358 121A Street (interpolated segment origin, reverse: 8343 121A St)
- File: `kennedy-trail--queen-mary-park-surrey-nearby-2026-11-02.md` — 3091 bytes, 445 words (OVER CAP +45). Sections 1–5 all written; none omitted.
- Origin: No Nominatim house point exists for 8358 121A St; P2-30 segment interpolation between OSM address points 8343 and 8363 121A St, disclosed in-file. Segment-grade origin — re-measurement candidate as above.
- Measurements (3 walk, 4 drive): Walk to Kennedy Trail Elementary, 8305 121A St: 4.9 min, 0.37 km; Drive to Kennedy Trail Elementary, 8305 121A St: 1.7 min, 0.75 km; Walk to Kennedy Trail Park, 12237 82 Ave: 7.3 min, 0.55 km; Drive to Kennedy Trail Park, 12237 82 Ave: 1.1 min, 0.53 km; Drive to Strawberry Hill Park, 7676 122 St: 3.9 min, 2.04 km; Walk to Real Canadian Superstore, 8195 120 St: 10.4 min, 0.78 km; Drive to Real Canadian Superstore, 8195 120 St: 2.4 min, 0.97 km.
- NOT CONFIRMED highlights: Catchments; frequencies; interpolated origin disclosed; over-cap walk to Strawberry Hill Park listed as drive only; Kennedy Trail Elementary address variant (home file 8305 122A St vs Ministry 8305 121A St — Ministry form used).

### 791. Kennedy Woods — 8289 121A Street
- File: `kennedy-woods--queen-mary-park-surrey-nearby-2026-11-02.md` — 2830 bytes, 405 words (OVER CAP +5). Sections 1–5 all written; none omitted.
- Origin: House point, reverse-geocode confirms the roster address.
- Measurements (3 walk, 4 drive): Walk to Kennedy Trail Elementary, 8305 121A St: 4.3 min, 0.32 km; Drive to Kennedy Trail Elementary, 8305 121A St: 2.1 min, 0.74 km; Walk to Kennedy Trail Park, 12237 82 Ave: 5.8 min, 0.44 km; Drive to Kennedy Trail Park, 12237 82 Ave: 1.1 min, 0.45 km; Drive to Strawberry Hill Park, 7676 122 St: 3.9 min, 1.97 km; Walk to Real Canadian Superstore, 8195 120 St: 8.9 min, 0.67 km; Drive to Real Canadian Superstore, 8195 120 St: 2.5 min, 0.9 km.
- NOT CONFIRMED highlights: Catchments; frequencies; Kennedy Trail Elementary address variant (as per 790); over-cap walk to Strawberry Hill Park listed as drive only; no grocery anchor within 1 km confirmed from an allowed source.

### 792. Lakewood Grove — 8257 121A Street
- File: `lakewood-grove--queen-mary-park-surrey-nearby-2026-11-02.md` — 2832 bytes, 405 words (OVER CAP +5). Sections 1–5 all written; none omitted.
- Origin: House point, reverse-geocode confirms the roster address.
- Measurements (3 walk, 4 drive): Walk to Kennedy Trail Elementary, 8305 121A St: 5.0 min, 0.37 km; Drive to Kennedy Trail Elementary, 8305 121A St: 1.7 min, 0.64 km; Walk to Kennedy Trail Park, 12237 82 Ave: 4.9 min, 0.36 km; Drive to Kennedy Trail Park, 12237 82 Ave: 0.8 min, 0.35 km; Drive to Strawberry Hill Park, 7676 122 St: 3.5 min, 1.87 km; Walk to Real Canadian Superstore, 8195 120 St: 7.9 min, 0.59 km; Drive to Real Canadian Superstore, 8195 120 St: 2.1 min, 0.8 km.
- NOT CONFIRMED highlights: Catchments; frequencies; Kennedy Trail Elementary address variant (as per 790); over-cap walk to Strawberry Hill Park listed as drive only; no grocery anchor within 1 km confirmed from an allowed source.

### 793. Melrose Place — 8068 120A Street
- File: `melrose-place--queen-mary-park-surrey-nearby-2026-11-02.md` — 2767 bytes, 391 words. Sections 1–5 all written; none omitted.
- Origin: House point, reverse-geocode confirms the roster address.
- Measurements (4 walk, 4 drive): Walk to Kennedy Trail Elementary, 8305 121A St: 9.5 min, 0.71 km; Drive to Kennedy Trail Elementary, 8305 121A St: 2.2 min, 1.03 km; Walk to Kennedy Trail Park, 12237 82 Ave: 6.9 min, 0.52 km; Drive to Kennedy Trail Park, 12237 82 Ave: 1.3 min, 0.74 km; Walk to Strawberry Hill Park, 7676 122 St: 17.7 min, 1.33 km; Drive to Strawberry Hill Park, 7676 122 St: 2.7 min, 1.12 km; Walk to Real Canadian Superstore, 8195 120 St: 7.4 min, 0.56 km; Drive to Real Canadian Superstore, 8195 120 St: 1.8 min, 0.68 km.
- NOT CONFIRMED highlights: Catchments; frequencies; Kennedy Trail Elementary address variant (as per 790); no grocery anchor within 1 km confirmed from an allowed source.

### 794. Quinn by Porte (Quinn by Porte Homes) — 13439 94A Avenue (anchor; interpolated segment origin, reverse: 13437 94A Ave)
- File: `quinn-by-porte--queen-mary-park-surrey-nearby-2026-11-02.md` — 3567 bytes, 519 words (OVER CAP +119). Sections 1–5 all written; none omitted.
- Origin: No Nominatim house point exists for either rostered address; P2-30 segment interpolation on 94A Ave between OSM address points 13427 and 13605, disclosed in-file. Segment-grade origin — re-measurement candidate as above.
- Measurements (2 walk, 6 drive): Drive to Queen Elizabeth Meadows, 9400 134 St: 1.7 min, 0.75 km; Walk to Queen Elizabeth Secondary, 9457 King George Blvd: 4.2 min, 0.32 km; Drive to Queen Elizabeth Secondary, 9457 King George Blvd: 2.1 min, 0.65 km; Drive to Bear Creek Park, 13750 88 Ave: 3.6 min, 2.15 km; Walk to King George Station: 18.3 min, 1.37 km; Drive to King George Station: 2.3 min, 1.25 km; Drive to Surrey Central Station: 4.1 min, 2.18 km; Drive to Central City, 10153 King George Blvd: 4.9 min, 2.06 km.
- NOT CONFIRMED highlights: Catchments; frequencies; R1 not confirmed from an operator page read; multi-address anchor disclosure (second address also segment-only, probe-verified); 'Surrey City Centre' marketing-name flag from the condos home file; walk to Queen Elizabeth Meadows discarded (6.23 km/h, outside the sanity band), drive listed; Bear Creek Park routed to the Surrey Arts Centre point.

### 795. Sterling Court — 8142 120A Street
- File: `sterling-court--queen-mary-park-surrey-nearby-2026-11-02.md` — 3013 bytes, 428 words (OVER CAP +28). Sections 1–5 all written; none omitted.
- Origin: House point, reverse-geocode confirms the roster address.
- Measurements (4 walk, 4 drive): Walk to Kennedy Trail Elementary, 8305 121A St: 8.9 min, 0.67 km; Drive to Kennedy Trail Elementary, 8305 121A St: 1.7 min, 0.78 km; Walk to Kennedy Trail Park, 12237 82 Ave: 6.3 min, 0.47 km; Drive to Kennedy Trail Park, 12237 82 Ave: 0.8 min, 0.49 km; Walk to Strawberry Hill Park, 7676 122 St: 19.0 min, 1.43 km; Drive to Strawberry Hill Park, 7676 122 St: 2.8 min, 1.29 km; Walk to Real Canadian Superstore, 8195 120 St: 5.8 min, 0.44 km; Drive to Real Canadian Superstore, 8195 120 St: 1.8 min, 0.67 km.
- NOT CONFIRMED highlights: Catchments; frequencies; classification conflict flagged from the condos home file (listing files the building under West Newton; directory under Queen Mary Park Surrey) — roster home stands; Kennedy Trail Elementary address variant as per 790.

### 796. Tamaron (The Tamaron) — 12083 92A Avenue
- File: `tamaron--queen-mary-park-surrey-nearby-2026-11-02.md` — 2838 bytes, 380 words. Sections 1–5 all written; none omitted.
- Origin: House point, reverse-geocode confirms the roster address.
- Measurements (2 walk, 6 drive): Drive to Queen Mary Park, 8972 Queen Mary Blvd: 6.0 min, 3.41 km; Walk to L.A. Matheson Secondary, 9484 122 St: 12.3 min, 0.92 km; Drive to L.A. Matheson Secondary, 9484 122 St: 3.2 min, 1.16 km; Walk to Kirkbride Elementary, 12150 92 Ave: 5.8 min, 0.44 km; Drive to Kirkbride Elementary, 12150 92 Ave: 1.5 min, 0.49 km; Drive to David Brankin Elementary, 9160 128 St: 3.6 min, 1.83 km; Drive to Real Canadian Superstore, 8195 120 St: 4.6 min, 2.67 km; Drive to King George Station: 7.1 min, 4.68 km.
- NOT CONFIRMED highlights: Catchments; frequencies; over-cap walk to Queen Mary Park listed as drive only.

**Batch totals: 25 files; 91 walk + 142 drive = 233 measurements listed.**
