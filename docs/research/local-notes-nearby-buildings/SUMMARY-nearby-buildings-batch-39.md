# What's Nearby — Phase 2, Batch P2-39 (FINAL production batch) — Summary

Produced 2026-11-02 (measurement date 2026-11-02). Roster: `~/workspace/local-notes/nearby/PHASE2-ROSTER.md`.

## Range and counts

- **Exact roster range covered: entries 977–995** — the end of the roster. **18 buildings produced:** 977, 978, 980, 981, 982, 983, 984, 985, 986, 987, 988, 989, 990, 991, 992, 993, 994, 995.
- **Skipped (1): entry 979, Westbrooke freehold row homes (willoughby-heights; townhomes) — ADDRESS NOT IN NOTES**, held for the final mop-up batch; address not researched. There were no further entries to extend into. **Mop-up list is now 27 entries: 52, 85, 86, 156, 188, 193, 195, 240, 415, 487, 535, 549–552, 627, 632, 643, 667, 699, 780, 797, 837, 909, 910, 914, 979.**
- Areas: willoughby-heights 8, yaletown-condos-for-sale 10.
- **Measurements listed in §5: 168** (Willoughby 60; Yaletown 108). A further **60 in-cap drive times were measured in this pass but not listed** in the Yaletown files (drives to David Lam Park, George Wainborn Park, Roundhouse Community Centre, Elsie Roy Elementary, Urban Fare and Choices Markets from each Yaletown building — 6 per building × 10); they are recorded per building below and the non-listing is disclosed in each file's NOT CONFIRMED. **Total in-cap measurements taken: 228.**
- **HTTP 429s: none** across Nominatim, OSRM and routing.openstreetmap.de. OSRM returned HTTP 400 for every drive to the Carvolth Exchange point (bus-loop point it cannot snap to) — not a 429; those drives are unmeasured and disclosed in-file.
- **Roster lines proved wrong on the ground: none** — the roster was never silently corrected.
- **Process note:** the first geocode run's output file was lost when its scratch environment was reset; per the standing rule the whole pass was re-run in the foreground, fsynced to disk and read back before §5 drafting. No figure in any file comes from the lost run. Nominatim result sets varied between runs (street-segment ways ranked ahead of house points on the re-run); every point used was reverse-geocoded in this pass and verified against the roster address, a named feature, or its own street segment, as disclosed per file.
- Cumulative phase-2 totals after P2-39: **968 building files** (all addressed roster entries produced); the 27 problem entries remain for the mop-up batch.

## Origin governance (all disclosed in-file)

- **Named-point origins** (no house-number point returned; the complex's own named OSM point used, Marquee/Lakeside precedent): Union Park (977), Walnut Park (978 — roster states an intersection, not a civic number; the named point sits at that intersection), Willow Park Estates (980), Yorkson Downs (984).
- **Segment-grade origins** (street-segment point at the address's grid position on its own street, reverse-geocoding to that street; P2-30/P2-38 pattern; re-measurement candidates if a sourced civic point set becomes available): Yorkson Creek condos (981, 207A St), Yorkson Creek townhomes (982, 84 Ave), Yorkson Creek Parkside 2 (983, 207 St), Yorkson Park (985, 86 Ave). Bracketing checks: the only verified address points near these streets (8429 207A St; 20615 84 Ave; 20427 86 Ave) bracket on one side only, so full interpolation was not available; grid-position segment points were used and disclosed instead. An earlier computed point for 985 reverse-geocoded to a business at 20376 86 Avenue and was moved west and re-verified to plain 86 Avenue before use.
- **Exact house points, reverse-geocoded to the roster address:** all ten Yaletown buildings (986–995).
- **Multi-address entry:** Yorkson Park (985) — one file; header carries all four rostered addresses exactly (20328 86 Avenue, 20290 86 Avenue, 20376 86 Avenue, 8561 203A Street); anchor is the first address, disclosed.
- **Same-name separateness:** Yorkson Creek condos (981, 8328 207A St) and Yorkson Creek (Quadra Homes) townhomes (982, 20738 84 Ave) each have their own file; the townhomes file carries the address disambiguator `yorkson-creek-20738-84-avenue` in its filename; separateness is stated in both files.
- **Destination points:** Yorkson Creek Middle School's own named school point; Lynn Fripps Elementary, R.E. Mountain Secondary (7633 202A St exact this pass), Langley Events Centre (7888 200 St), Hakam's/Willoughby Town Centre (20678 WTC Dr), Muriel Arnason Library, Willowbrook Shopping Centre (19705 Fraser Hwy), Carvolth Exchange named point — all reverse-geocoded. David Lam Park's own park point used (a first candidate at 750 Pacific Blvd was discarded). Crosstown Elementary's point reverse-geocodes to 56 Expo Blvd; the Ministry address (55 Expo Blvd) governs in §3, disclosed in every Yaletown file.
- **Willoughby Elementary could not be measured:** no verifiable OSM point for 20766 80 Ave was returned in this pass (street segments only); it is listed in §3 from the Ministry list and the gap disclosed in every Willoughby file.

## Word-cap overages (all 18 files, disclosed; wording trimmed only, no cited fact or URL cut)

Union Park 460 (+60), Walnut Park 511 (+111), Willow Park Estates 499 (+99), Yorkson Creek 485 (+85), Yorkson Creek TH 546 (+146), Parkside 2 464 (+64), Yorkson Downs 468 (+68), Yorkson Park 508 (+108), Azura 2 474 (+74), The Bentley 471 (+71), City Crest 493 (+93), Crestmark I 471 (+71), Crestmark II 492 (+92), King's Landing 509 (+109), The Murchies 485 (+85), Pacific Landmark II 498 (+98), Waterworks 469 (+69), Yaletown Park 3 518 (+118) — driven by measurement density (6–11 listed per file) plus the mandated origin/multi-address disclosures and the shared sourced §§1–4 sets. No section was omitted in any file; no file used the §5 fallback.

## Per-building detail

Listed = §5 bullets in the file (mode, km, min). "Also measured" = in-cap drives measured in this pass, not listed (Yaletown only).

### 977. Union Park (Polygon) — 8150 207 Street, Langley (willoughby-heights; condos) — 3,292 B / 460 w
- Origin: OSM point named "Union Park" (see governance). Sections: all five written.
- Listed (8): Walk YCMS 0.89/12.0; Drive YCMS 1.12/3.3; Walk Lynn Fripps 1.22/16.3; Drive Lynn Fripps 1.21/3.1; Drive R.E. Mountain 2.43/5.3; Drive LEC 2.21/5.2; Walk Hakam's 1.42/19.0; Drive Hakam's 1.45/3.2.
- NOT CONFIRMED: catchments; frequencies; Carvolth street address + drive HTTP 400; Willoughby Elementary unmeasured.

### 978. Walnut Park (Quadra Homes) — 208 Street and 83 Avenue, Yorkson (willoughby-heights; condos) — 3,587 B / 511 w
- Origin: OSM point named "Walnut Park" at the roster's stated intersection. Sections: all five written.
- Listed (8): Walk YCMS 0.77/10.2; Drive YCMS 0.92/1.9; Walk Lynn Fripps 0.68/9.1; Drive Lynn Fripps 0.69/1.5; Drive R.E. Mountain 2.67/4.5; Drive LEC 2.45/4.4; Walk Hakam's 1.05/14.0; Drive Hakam's 1.25/2.2.
- NOT CONFIRMED: catchments; frequencies; Carvolth; **no civic number exists in the roster/notes (intersection only), none researched**; completion status and final unit count UNCONFIRMED (home file); Willoughby Elementary unmeasured.

### 980. Willow Park Estates — 6467 197 Street, Langley (willoughby-heights; 55-plus + townhomes) — 3,576 B / 499 w
- Origin: OSM point named "Willow Park Estates". Sections: all five written. Identified by program in the header only; no age-restriction claim in the text.
- Listed (7): Walk Willowbrook 1.26/16.8; Drive Willowbrook 1.37/3.6; Drive Arnason Library 1.75/3.2; Drive LEC 3.60/5.6; Drive R.E. Mountain 3.91/6.6; Drive Hakam's 5.37/7.6; Drive YCMS 5.91/8.6.
- NOT CONFIRMED: catchments; frequencies; Carvolth; "Willowpark Estates" name variant (roster note); Willoughby Elementary unmeasured; library walk 1.86 km over cap, not listed.

### 981. Yorkson Creek — 8328 207A Street, Langley (willoughby-heights; condos) — 3,464 B / 485 w
- Origin: segment point on 207A St at the 8328 grid position (segment-grade). Sections: all five written.
- Listed (8): Walk YCMS 0.42/5.6; Drive YCMS 0.65/1.6; Walk Lynn Fripps 0.93/12.4; Drive Lynn Fripps 0.98/2.0; Drive R.E. Mountain 2.33/4.1; Drive LEC 2.09/4.1; Walk Hakam's 1.17/15.6; Drive Hakam's 1.22/2.0.
- NOT CONFIRMED: catchments; frequencies; Carvolth; separateness from entry 982 stated; Willoughby Elementary unmeasured.

### 982. Yorkson Creek (Quadra Homes) — 20738 84 Avenue, Langley (willoughby-heights; townhomes) — 3,849 B / 546 w
- Origin: segment point on 84 Ave at the 20738 grid position (segment-grade). Filename carries the address disambiguator. Sections: all five written.
- Listed (8): Walk YCMS 0.10/1.4; Drive YCMS 0.28/0.8; Walk Lynn Fripps 0.99/13.3; Drive Lynn Fripps 1.63/3.0; Drive R.E. Mountain 2.63/4.3; Drive LEC 2.41/4.4; Drive Hakam's 2.17/3.4; Walk Carvolth Exchange 1.36/18.1.
- NOT CONFIRMED: catchments; frequencies; Carvolth street address + drive HTTP 400; separateness from entry 981 stated; unit count conflict (171 vs 152 in the home file) recorded unresolved; Hakam's walk 1.52 km over cap, not listed; Willoughby Elementary unmeasured.

### 983. Yorkson Creek Parkside 2 — 8157 207 Street, Langley (willoughby-heights; condos) — 3,330 B / 464 w
- Origin: segment point on 207 St at the 8157 grid position (segment-grade). Sections: all five written.
- Listed (8): Walk YCMS 0.75/10.0; Drive YCMS 0.94/2.3; Walk Lynn Fripps 1.13/15.1; Drive Lynn Fripps 1.02/2.1; Drive R.E. Mountain 1.98/3.6; Drive LEC 1.76/3.5; Walk Hakam's 0.87/11.6; Drive Hakam's 0.93/2.0.
- NOT CONFIRMED: catchments; frequencies; Carvolth; Willoughby Elementary unmeasured.

### 984. Yorkson Downs (Quadra) — 20716 Willoughby Town Centre Drive, Langley (willoughby-heights; condos) — 3,391 B / 468 w
- Origin: OSM point named "Yorkson Downs". Sections: all five written.
- Listed (6): Walk Hakam's 0.18/2.4; Drive Hakam's 0.24/1.1; Drive YCMS 1.89/3.5; Drive Lynn Fripps 1.66/3.2; Drive R.E. Mountain 2.16/4.6; Drive LEC 1.94/4.5.
- NOT CONFIRMED: catchments; frequencies; Carvolth; walks to YCMS (1.66), Lynn Fripps (1.61) and R.E. Mountain (1.57) over the walk cap, not listed; Willoughby Elementary unmeasured.

### 985. Yorkson Park (Quadra Homes) — 20328 86 Avenue (+ 20290 86 Avenue, 20376 86 Avenue, 8561 203A Street), Langley (willoughby-heights; condos) — 3,613 B / 508 w
- Origin: segment point on 86 Ave at the 20328 position (segment-grade); anchor = first rostered address, disclosed; header carries all four addresses exactly as rostered. Sections: all five written.
- Listed (7): Walk YCMS 1.08/14.4; Drive YCMS 1.05/2.0; Walk Carvolth Exchange 0.20/2.7; Drive Lynn Fripps 2.13/3.7; Drive R.E. Mountain 2.58/4.3; Drive LEC 2.34/4.0; Drive Hakam's 2.34/3.8.
- NOT CONFIRMED: catchments; frequencies; Carvolth street address (walk listed; drive HTTP 400); anchor disclosure; group-wide unit count UNCONFIRMED (31-unit directory figure is for 20328 only); Willoughby Elementary unmeasured.

### 986. Azura 2 — 1495 Richards Street, Vancouver (yaletown-condos-for-sale; condos) — 3,408 B / 474 w
- Origin: exact house point (OSM name "Azura Two" — variant flagged in-file, roster name stands). Sections: all five written.
- Listed (10): Walk Station 0.61/8.2; Drive Station 1.26/2.8; Walk David Lam 0.36/4.8; Walk Wainborn 0.16/2.1; Walk Roundhouse CC 0.54/7.1; Walk Elsie Roy 0.53/7.1; Walk Urban Fare 0.62/8.3; Walk Choices 0.38/5.1; Drive Crosstown 1.92/3.5; Drive King George 2.51/4.8.
- Also measured, not listed (6 drives): David Lam 0.26/0.7; Wainborn 0.13/0.3; Roundhouse CC 0.47/1.0; Elsie Roy 0.55/1.3; Urban Fare 0.82/1.5; Choices 0.58/1.2.
- NOT CONFIRMED: catchments; frequencies; no operator-named exchange/loop; Crosstown 55/56 Expo variant.

### 987. The Bentley — 1001 Homer Street, Vancouver (yaletown-condos-for-sale; condos) — 3,391 B / 471 w
- Origin: exact house point. Sections: all five written.
- Listed (11): Walk Station 0.45/6.0; Drive Station 0.52/1.4; Walk David Lam 0.81/10.8; Walk Wainborn 0.91/12.2; Walk Roundhouse CC 0.71/9.6; Walk Elsie Roy 0.80/10.7; Walk Crosstown 1.26/16.8; Drive Crosstown 1.52/3.1; Walk Urban Fare 0.57/7.6; Walk Choices 0.38/5.1; Drive King George 2.43/5.0.
- Also measured, not listed (6 drives): David Lam 0.83/1.8; Wainborn 1.02/2.1; Roundhouse CC 0.83/2.0; Elsie Roy 0.92/2.2; Urban Fare 0.91/2.0; Choices 0.51/1.2.
- NOT CONFIRMED: as 986.

### 988. City Crest — 1155 Homer Street, Vancouver (yaletown-condos-for-sale; condos) — 3,512 B / 493 w
- Origin: exact house point. Sections: all five written.
- Listed (11): Walk Station 0.20/2.7; Drive Station 0.72/1.6; Walk David Lam 0.55/7.4; Walk Wainborn 0.66/8.8; Walk Roundhouse CC 0.46/6.2; Walk Elsie Roy 0.55/7.3; Walk Crosstown 1.50/20.0; Drive Crosstown 1.64/3.2; Walk Urban Fare 0.32/4.3; Walk Choices 0.13/1.7; Drive King George 2.44/5.0.
- Also measured, not listed (6 drives): David Lam 0.45/1.0; Wainborn 0.64/1.3; Roundhouse CC 0.45/1.1; Elsie Roy 0.54/1.3; Urban Fare 0.53/1.1; Choices 0.13/0.3.
- NOT CONFIRMED: as 986, plus unit-count conflict (143 vs 135 in the home file's sources) recorded unresolved.

### 989. Crestmark I — 1288 Marinaside Crescent, Vancouver (yaletown-condos-for-sale; condos) — 3,411 B / 471 w
- Origin: exact house point. Sections: all five written.
- Listed (11): Walk Station 0.43/5.7; Drive Station 1.18/2.9; Walk David Lam 0.44/5.9; Walk Wainborn 0.82/11.0; Walk Roundhouse CC 0.29/3.9; Walk Elsie Roy 0.21/2.9; Walk Crosstown 1.47/19.6; Drive Crosstown 1.71/3.3; Walk Urban Fare 0.25/3.3; Walk Choices 0.59/7.9; Drive King George 3.03/5.9.
- Also measured, not listed (6 drives): David Lam 0.53/1.4; Wainborn 0.73/1.8; Roundhouse CC 0.22/0.7; Elsie Roy 0.11/0.4; Urban Fare 0.26/0.6; Choices 0.62/1.3.
- NOT CONFIRMED: as 986.

### 990. Crestmark II — 1228 Marinaside Crescent, Vancouver (yaletown-condos-for-sale; condos) — 3,535 B / 492 w
- Origin: exact house point. Sections: all five written.
- Listed (11): Walk Station 0.36/4.5; Drive Station 1.16/2.9; Walk David Lam 0.52/6.9; Walk Wainborn 0.89/11.6; Walk Roundhouse CC 0.33/4.1; Walk Elsie Roy 0.31/3.8; Walk Crosstown 1.38/18.3; Drive Crosstown 1.70/3.4; Walk Urban Fare 0.18/2.1; Walk Choices 0.53/6.7; Drive King George 2.91/6.1.
- Also measured, not listed (6 drives): David Lam 0.59/1.6; Wainborn 0.79/2.1; Roundhouse CC 0.28/1.0; Elsie Roy 0.17/0.7; Urban Fare 0.24/0.6; Choices 0.60/1.4.
- NOT CONFIRMED: as 986, plus build-year conflict (1997 vs 1998) recorded unresolved.

### 991. King's Landing West Tower — 428 Beach Crescent, Vancouver (yaletown-condos-for-sale; condos) — 3,620 B / 509 w
- Origin: exact house point. Sections: all five written.
- Listed (10): Walk Station 0.72/9.6; Drive Station 1.37/3.2; Walk David Lam 0.32/4.3; Walk Wainborn 0.17/2.3; Walk Roundhouse CC 0.58/7.7; Walk Elsie Roy 0.58/7.7; Walk Urban Fare 0.70/9.4; Walk Choices 0.60/8.0; Drive Crosstown 2.03/4.1; Drive King George 2.75/5.5.
- Also measured, not listed (6 drives): David Lam 0.20/0.6; Wainborn 0.11/0.4; Roundhouse CC 0.57/1.6; Elsie Roy 0.66/1.9; Urban Fare 0.92/2.1; Choices 0.69/1.8.
- NOT CONFIRMED: as 986, plus the wider complex's 1515 Homer Mews address (listings, home file) flagged — this file covers the roster's 428 Beach Crescent building only; Crosstown walk 1.93 km over cap, not listed.

### 992. The Murchies — 1216 Homer Street, Vancouver (yaletown-condos-for-sale; condos) — 3,475 B / 485 w
- Origin: exact house point (OSM name "The Murchies Building" — flagged in-file, roster name stands). Sections: all five written.
- Listed (11): Walk Station 0.19/2.5; Drive Station 0.79/1.8; Walk David Lam 0.47/6.2; Walk Wainborn 0.61/8.1; Walk Roundhouse CC 0.42/5.7; Walk Elsie Roy 0.46/6.1; Walk Crosstown 1.48/19.8; Drive Crosstown 1.63/3.1; Walk Urban Fare 0.30/4.0; Walk Choices 0.12/1.5; Drive King George 2.43/5.0.
- Also measured, not listed (6 drives): David Lam 0.38/0.8; Wainborn 0.58/1.3; Roundhouse CC 0.38/0.9; Elsie Roy 0.46/1.2; Urban Fare 0.52/1.1; Choices 0.12/0.3.
- NOT CONFIRMED: as 986.

### 993. Pacific Landmark II (Pacific Place Landmark II) — 930 Cambie Street, Vancouver (yaletown-condos-for-sale; condos) — 3,568 B / 498 w
- Origin: exact house point (OSM name "Pacific Place Landmark II" = the roster's alias — flagged in-file). Sections: all five written.
- Listed (11): Walk Station 0.57/7.6; Drive Station 0.61/1.6; Walk David Lam 0.95/12.7; Walk Wainborn 1.17/15.6; Walk Roundhouse CC 0.72/9.7; Walk Elsie Roy 0.79/10.6; Walk Crosstown 0.89/11.8; Drive Crosstown 1.55/2.5; Walk Urban Fare 0.56/7.4; Walk Choices 0.76/10.1; Drive King George 2.41/4.7.
- Also measured, not listed (6 drives): David Lam 0.94/1.7; Wainborn 1.14/2.1; Roundhouse CC 0.80/1.5; Elsie Roy 0.89/1.8; Urban Fare 0.80/1.4; Choices 0.77/1.3.
- NOT CONFIRMED: as 986.

### 994. Waterworks — 1008 Cambie Street, Vancouver (yaletown-condos-for-sale; condos) — 3,392 B / 469 w
- Origin: exact house point. Sections: all five written.
- Listed (11): Walk Station 0.41/5.5; Drive Station 0.83/2.1; Walk David Lam 0.78/10.5; Walk Wainborn 1.01/13.4; Walk Roundhouse CC 0.56/7.5; Walk Elsie Roy 0.63/8.4; Walk Crosstown 1.09/14.5; Drive Crosstown 1.32/2.8; Walk Urban Fare 0.39/5.2; Walk Choices 0.61/8.1; Drive King George 2.63/5.2.
- Also measured, not listed (6 drives): David Lam 1.17/2.5; Wainborn 1.55/2.9; Roundhouse CC 1.04/2.4; Elsie Roy 1.12/2.6; Urban Fare 1.03/2.2; Choices 1.06/2.1.
- NOT CONFIRMED: as 986.

### 995. Yaletown Park 3 — 977 Mainland Street, Vancouver (yaletown-condos-for-sale; condos) — 3,684 B / 518 w
- Origin: exact house point (OSM name "Yaletown Park III" — flagged in-file, roster name stands). Sections: all five written.
- Listed (11): Walk Station 0.45/6.0; Drive Station 0.60/1.8; Walk David Lam 0.91/12.1; Walk Wainborn 1.07/14.3; Walk Roundhouse CC 0.72/9.6; Walk Elsie Roy 0.81/10.9; Walk Crosstown 1.09/14.6; Drive Crosstown 1.60/3.5; Walk Urban Fare 0.57/7.6; Walk Choices 0.56/7.4; Drive King George 2.33/4.8.
- Also measured, not listed (6 drives): David Lam 0.90/2.1; Wainborn 1.10/2.4; Roundhouse CC 0.91/2.3; Elsie Roy 0.99/2.5; Urban Fare 0.98/2.3; Choices 0.58/1.5.
- NOT CONFIRMED: as 986, plus unit-count/strata-plan conflict (266 units / BCS2143 vs 272 units / BCS2103) recorded unresolved.
