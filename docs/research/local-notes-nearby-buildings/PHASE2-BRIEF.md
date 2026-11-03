# What's Nearby — Phase 2 BASE BRIEF (per-building files)

Written Nov 2, 2026 for batch P2-1; read by every later phase-2 batch. Phase 2 = one What's Nearby file per NAMED BUILDING in the 55-plus / condos / townhomes local notes, same 5 sections as phase 1, scoped to the building's street address + ~1 km walking radius, every measured time starting at the building's address.

## The roster governs

- Roster: `~/workspace/local-notes/nearby/PHASE2-ROSTER.md` (995 unique buildings, continuous numbering, grouped by home area slug alphabetically, buildings alphabetical within). READ the roster intro and every entry you produce from, in full, before writing.
- A batch = the next numbered entries THAT CARRY A STREET ADDRESS, in roster order, until the batch count is met. Entries marked ADDRESS NOT IN NOTES or ADDRESS CONFLICT are NOT produced in running batches — skip them, list them in the batch report, and note them for the final mop-up batch. Do NOT research addresses for skipped entries in a running batch.
- Building name, street address, home slug and program(s) come from the roster line ONLY. Never look up, substitute or "correct" an address. If a roster line proves wrong on the ground (bad address, building not at that address), flag it in the batch summary and report — never silently correct it.
- Multi-address roster lines that are NOT marked ADDRESS CONFLICT (component splits, e.g. separate condo/townhome addresses) are produced as ONE file: the title and measurement anchor use the first address; the header line carries all addresses exactly as the roster states them; the anchor choice is disclosed in the file's NOT CONFIRMED list and the batch summary.

## Before writing each file, read

1. The phase-1 area file for the home slug: `~/workspace/local-notes/nearby/<home-slug>-nearby-2026-11-02.md` — your starting map of sourced anchors.
2. The building's program home file(s) in `~/workspace/local-notes/55-plus/`, `~/workspace/local-notes/condos/`, `~/workspace/local-notes/townhomes/` (file for the home slug in each program the roster lists) — for the building's own facts.
3. Every fact in the building file must rest on its own cited source read in this pass, or carried from the phase-1 file's cited source. When in doubt, re-read the source.

## File format

- Title: `# <Building name> — <street address> — What's Nearby: Local Notes`
- Header line directly under the title: `Building: <name>, <address> (<home area slug>; <program(s)>).` — facts from the roster line only.
- FIVE sections IN ORDER, as `## 1. TRANSIT` … `## 5. MEASURED TRAVEL TIMES`, bullets, a source URL after EVERY fact.
- Then `## NOT CONFIRMED`: everything material checked but not confirmed (address-level catchment, exchange name, a route, an anchor's address, an unmeasured time).

### 1. TRANSIT
- Nearest rapid-transit station (if any) and/or bus exchange/loop BY NAME — an exchange/loop is named ONLY if an operator page you read supports the name.
- Up to 5 bus routes serving the stop(s) nearest the building. Frequency only if an operator page states it.
- Sources: TransLink / BC Transit / municipal pages ONLY.

### 2. PARKS AND RECREATION
- Parks from the municipal parks list; recreation centres / libraries / arenas WITH street addresses.
- Regional/provincial parks only from Metro Vancouver / FVRD / BC Parks pages.

### 3. SCHOOLS
- Schools within the radius, from the BC Ministry school list or the district site.
- Independent schools only if Ministry-listed, and marked "independent".
- Catchment ONLY if a district locator/policy page confirms it for the building's address. No locator runs are pre-done in this program — if you do not run one for this address, catchments stay unconfirmed and that is stated.
- NO ratings. Garbled / encoding-artifact Ministry names are excluded, never guessed.

### 4. GROCERY AND SHOPPING ANCHORS
- Grocery stores + shopping centres WITH street address, from the retailer's/centre's own locator or site, or municipal commercial-centre pages.
- NO restaurants, cafés or services.
- BANNED sources: Google Maps/Places, Yelp, Walk Score, REW, Zolo, Zillow, TripAdvisor, zealty.ca, any MLS/listing site. A retailer own-domain search RESULT is an accepted fallback for that retailer's address, disclosed in-file as such.

### 5. MEASURED TRAVEL TIMES
- Only times measured in this pass. EVERY measurement starts at the building's street address.
- Toolchain: Nominatim geocode (use the roster's civic address; if it fails, a sourced civic address for the same building); OSRM demo server (router.project-osrm.org) for DRIVING; routing.openstreetmap.de routed-foot for WALKING (the OSRM foot profile is broken; the Valhalla demo is unresponsive).
- Walk sanity ~4–6 km/h — discard/re-check any walk outside it. Include only walk ≤1.5 km / drive ≤10 km pairs.
- State on the section: measurement date 2026-11-02 and "OSM data date not published by the service" — never invent an OSM data date.
- RATE LIMITS: pace Nominatim/OSRM requests (~1/sec). On HTTP 429 from Nominatim/OSRM, STOP using that service, note it in the summary/report, and continue with the other sections — never retry through a 429.
- If the routing toolchain is unavailable, §5 is a single bullet: "Travel times: not measured in this pass."
- Work in an ISOLATED scratch dir unique to your batch/worker (a phase-1 worker once imported stale points from a shared /tmp script). Re-verify any point you did not geocode yourself.

## Scope and style discipline

- §§1–4 anchors within roughly 1 km walking radius of the building where possible.
- FACTS ONLY: no marketing words, no prices, no listing data, no rental/strata rules, no age-restriction claims. A 55-plus building is identified by name/class only, in the header line, from the roster.
- Under ~400 words INCLUDING URLs. Trim WORDING only — never drop a cited fact or its URL. Overage happens; disclose it in the batch summary rather than cut facts.

## Outputs per batch

- Building files: `~/workspace/local-notes/nearby/buildings/<building-name-slug>--<home-slug>-nearby-2026-11-02.md` (building name slugified lowercase-hyphenated, parenthetical qualifiers dropped; the roster number is NOT in the filename).
- Batch summary: `~/workspace/local-notes/nearby/SUMMARY-nearby-buildings-batch-<N>.md` — per building: address used, sections written/omitted + why, measurements taken (mode + distance + time), NOT CONFIRMED items, over-cap flag. Plus: exact roster entry range covered, skipped entries (ADDRESS NOT IN NOTES / CONFLICT) with their numbers, 429s encountered, roster lines that proved wrong on the ground.
- Batch zip: `~/workspace/local-notes/nearby-buildings-batch-<N>.zip` containing exactly that batch's building files.

## Reporting

Final report per batch: files created with sizes (ls-verified), exact roster entry range covered, skipped entries, any addressed entry that could NOT be completed and why, total measurement count, 429s encountered, any roster line that proved wrong on the ground (flagged, never silently corrected).
