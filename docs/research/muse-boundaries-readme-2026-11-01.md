# MLS Sub-Area Boundaries — Surrey + Fraser Valley (Priority 1 for Claude)

Prepared for Jared Gibbons · All web sources read 2026-11-01 · Companion file: `surrey-fraser-valley-boundaries.csv` (30 rows)

## The honest headline

**FVREB does not publish sub-area boundaries in any public text or downloadable-file form. Street-level boundaries confirmed from public board sources: 0 of 30 program rows.**

What the board *does* publish publicly is: the **names** of its areas and sub-areas (statistics packages, MLS® HPI reports, SnapStats reporting drawn from board data), the **list of communities** it serves, and — in a member-news article — confirmation that the actual sub-area boundaries exist as a **map layer inside Paragon and AUTOPROP**, both behind a member sign-in. There is no public FVREB area/sub-area map PDF, no public street-by-street boundary description, and no public shapefile/GeoJSON of FVREB sub-areas that any of the searches below could find.

So the boundary polygons Claude needs to place the 116 held-back schools **cannot be sourced from public board publications**. The realistic routes to them are member-side (see "What would unblock this" below): Paragon's own "FVREB Sub Areas" layer, read sub-area by sub-area by someone with Paragon access (Jared / Paragon Pete), or a boundary/shapefile export requested from the board.

Municipal neighbourhood boundaries were **not** substituted anywhere in the CSV. That matters here, because the two geographies genuinely differ — proven inside this program's own files:

- **Sunshine Hills Woods** (North Delta) is one board sub-area that *combines two* municipal neighbourhoods (Sunshine Hills + Sunshine Woods).
- **Willoughby Heights** is the board's name; the Township of Langley's planning name for the same ground is "Willoughby."
- **Surrey City Centre** is a City name; the board sub-area covering that ground is **Whalley**.
- **Mt Lehman** is a real Abbotsford community but is **not a board sub-area at all** — its listings are absorbed into Bradner/Matsqui.
- The board's Surrey list and the City of Surrey's six communities (Whalley/City Centre, Guildford, Fleetwood, Newton, Cloverdale, South Surrey) are different partitions of the same city.

## What FVREB actually publishes (sources found, all read 2026-11-01)

| Source | URL | What it contains | Boundaries? |
|---|---|---|---|
| FVREB member news, Tech Tip #18 "Navigating Areas and Sub Areas" (Dec 11, 2024) | https://news.fvreb.bc.ca/member-updates/tech-tip-18-map-of-the-bc-boards-areas-subareas/ | Instructions for turning on the **"FVREB Sub Areas" map layer** in Paragon Pro / Paragon Connect, and the **"Sub Areas" layer in AUTOPROP** (reached by signing in to Paragon → Resources → AUTOPROP). Screenshots are interface illustrations, not boundary documents for individual sub-areas, and carry no street lists. | **The boundaries live here — member-only map layer, no text, no public file** |
| FVREB public site, About page | https://www.fvreb.bc.ca/about/about-fvreb/ | The six communities FVREB serves: Surrey, Langley, White Rock, North Delta, Abbotsford, Mission. | No |
| FVREB Statistics Packages (monthly; copies of the board's own PDFs found on member/brokerage hosts) | e.g. August 2026: https://rightsizing123.ca/market-reports/2026-08/fraser-valley-august-2026.pdf · June 2026: https://crm.agentlocator.ca/UserFiles/7466/files/FV-Package-2026-06.pdf | Sales/listings/benchmark tables at **community (board "area") level only** — the board's 8 reporting areas: N. Delta, North Surrey, Surrey, South Surrey White Rock, Cloverdale, Langley, Abbotsford, Mission. No sub-area tables, no maps of sub-areas, no boundary text. | Names of areas only |
| MLS® HPI Detailed Reports (Altus Group for the board/CREA) | e.g. July 2026: http://bchousesforsale.com/reports/fvreb-market-report-2026-07.pdf | The board's area → sub-area **name hierarchy** with benchmark prices (e.g. Area: North Surrey → Bolivar Heights, Bridgeview, Cedar Hills, Fraser Heights, Guildford, Port Kells, Royal Heights, Whalley). This is the most complete public board-derived sub-area name list per area. | Names only — no boundaries, no codes, no streets |
| CREA national stats, FVREB board page | https://creastats.crea.ca/board/fras/ | Board-level release text; repeats the community list. | No |
| MLS® Residential Data Input Form (multi-board, incl. FVREB; rev. Mar 13, 2026) | https://bcflatfeelisting.com/assets/documents/residential-data-input-form.pdf | Shows listings carry field 080 AREA and field 084 SUB-AREA/COMMUNITY (both required for upload) — i.e. every listing is coded to a sub-area in Paragon — but the form publishes **no value list and no boundaries**. | No |
| SnapStats FVR reports (commercial product, data sourced from FVREB MLS®) | Sample Feb 2026: https://mcusercontent.com/f9e322413d7bb6d2425379254/files/70e118a2-1ca7-13ac-6f69-2c92bcde2435/IG_FVR_2026_Feb.pdf ; this program's full extraction: `../stats/subarea-stats-sep2026.csv` | Sub-area **names** with counts, by community — the source of the 60-name board universe used below. SnapStats itself states its data is sourced from the FVREB MLS®. | Names only |

### Partial code evidence (Paragon-facing public material — NOT board-published, NOT boundaries)

The sub-area code system is visible only in fragments outside the board's own publications:

- South Surrey/White Rock sub-areas are codes **F51–F59**: F51 Elgin Chantrell, F52 Sunnyside Park, F53 Crescent Beach Ocean Park, F54 White Rock, F55 King George Corridor, F56 Hazelmere, F57 Grandview ("Grandview Surrey"), F58 Morgan Creek, F59 Pacific Douglas — as stated in a Macdonald Realty market report analysing the board's September 2026 package and database ("sub-areas F51 to F59": https://www.hamishross.com/assets/docs/white-rock-south-surrey-stats-october-2026.pdf?v=8384c7cd9aaf) and in Jared's own published Paragon pull on jaredgibbons.ca.
- Langley sub-areas are **F60–F69 and F6A** (same publisher's Langley report: https://langley.ai/reports/editions/langley-market-report-2026-09.pdf?v=652a6a70135c).
- **Abbotsford East = F75**, from an AUTOPROP-generated property report for an Abbotsford East address (https://uplineappdatalrs.blob.core.windows.net/landingpage/352491/0140870a-9b7d-4213-9b7e-d5119aa70af6_AUTOPROP_R_36189_CASSANDRA_DR__Abbotsford_V3G_2M6.pdf) — AUTOPROP reports print the property's Area, Sub-Area and Sub-Area Code, which confirms codes exist per sub-area but publishes them one address at a time.

Codes were not added to the CSV (its schema has no code column); they are recorded here because they are the keys a Paragon-side boundary export would use.

## Coverage

### The board universe vs. the program

The board-data sub-area universe for the seven communities in scope (from `../stats/subarea-stats-sep2026.csv`, which is FVREB MLS® data via SnapStats, September 2026) is **60 sub-areas**:

- **Surrey (15):** Bear Creek Green Timbers, Bolivar Heights, Bridgeview, Cedar Hills, East Newton, Fleetwood Tynehead, Fraser Heights, Guildford, Panorama Ridge, Port Kells, Queen Mary Park, Royal Heights, Sullivan Station, West Newton, Whalley
- **S Surrey White Rock (9):** Crescent Beach Ocean Park, Elgin Chantrell, Grandview, Hazelmere, King George Corridor, Morgan Creek, Pacific Douglas, Sunnyside Park, White Rock
- **Cloverdale (3):** Clayton, Cloverdale, Serpentine
- **Langley (11):** Aldergrove, Brookswood, Campbell Valley, County Line Glen Valley, Fort Langley, Langley City, Murrayville, Otter District, Salmon River, Walnut Grove, Willoughby Heights
- **North Delta (4):** Annieville, Nordel, Scottsdale, Sunshine Hills Woods
- **Abbotsford (9):** Abbotsford East, Abbotsford West, Aberdeen, Bradner, Central Abbotsford, Matsqui, Poplar, Sumas Mountain, Sumas Prairie
- **Mission (9):** Dewdney Deroche, Durieu, Hatzic, Hemlock, Lake Errock, Mission, Mission West, Stave Falls, Steelhead

### What the CSV covers (30 rows)

The CSV is keyed by **program slug** (the research file stem in `batch-1..batch-8/` + `missing/`), per the brief. It contains every program file in those folders whose §1 identifies it as an FVREB sub-area in one of the seven communities:

- Surrey: `east-newton-guide`, `west-newton-guide`, `panorama-ridge-guide`, `sullivan-station`, `port-kells`, `surrey-city-centre` (= Whalley) — 6 rows
- S Surrey White Rock: `sunnyside-park-surrey`, `grandview-corners-condos-townhomes-for-sale` (= Grandview) — 2 rows
- Langley: `aldergrove-guide`, `aldergrove-langley`, `brookswood-langley`, `fort-langley-guide`, `salmon-river`, `willoughby-heights` — 6 rows
- North Delta: `annieville`, `nordel`, `scottsdale`, `sunshine-hills-woods` — 4 rows (the community is fully covered: all 4 board sub-areas have program files)
- Abbotsford: `abbotsford-east-guide`, `abbotsford-west-guide`, `aberdeen-guide`, `bradner-guide`, `bradner`, `central-abbotsford-guide`, `central-abbotsford`, `matsqui-guide`, `poplar-guide`, `poplar`, `sumas-mountain-guide` — 11 rows
- Plus `mt-lehman` — 1 row, included because the program researched it as an Abbotsford candidate; its status records that it is **not** a board sub-area.

That is **29 sub-area rows covering 25 distinct board sub-areas** (Aldergrove, Bradner, Central Abbotsford and Poplar each have two program files) **of the 60** in the seven communities, plus the 1 non-sub-area row.

**Status counts: CONFIRMED 0 · UNVERIFIED 30.** Every boundary cell is empty — deliberately. No street was inferred from a map image, a municipal plan, a school catchment or general knowledge.

### Gaps (named, so nothing looks covered that isn't)

- **Cloverdale: 0 program sub-area files** (Clayton, Cloverdale, Serpentine have no researched file in batches 1–8 or `missing/`), so no CSV rows — the community is in scope but unresearched so far, not boundary-checked and found empty.
- **Mission: 0 program sub-area files.** The program's Mission files are community/topic pages (`mission-homes-for-sale`, `mission-farms`, `mission-homes-under-1-8m`, `missionforeclosuresandcourtsales`), none of which is a single board sub-area; none of Mission's 9 board sub-areas has a researched file yet.
- **Board sub-areas in the other communities with no program file yet (35):** Surrey — Bear Creek Green Timbers, Bolivar Heights, Bridgeview, Cedar Hills, Fleetwood Tynehead, Fraser Heights, Guildford, Queen Mary Park, Royal Heights (9); S Surrey White Rock — Crescent Beach Ocean Park, Elgin Chantrell, Hazelmere, King George Corridor, Morgan Creek, Pacific Douglas, White Rock (7); Langley — Campbell Valley, County Line Glen Valley, Langley City, Murrayville, Otter District, Walnut Grove (6); Abbotsford — Sumas Prairie (1). When those files are researched, they will need rows too — and on today's evidence every one of them will land UNVERIFIED for street boundaries for the same reason.
- Topic/utility pages inside these communities (foreclosures, open houses, price-band pages, farms pages, calculators) are not sub-areas and were excluded by design.

## What would unblock this

1. **Paragon itself (member route — the board's own tool).** Tech Tip #18 documents the exact clicks: Paragon Pro → Search → Mapping → Layers → "FVREB Sub Areas" + labels on; or AUTOPROP via Paragon → Resources. A member (Jared, or Paragon Pete on the Paragon workstream) can read each sub-area's boundary streets off that layer and dictate them, sub-area by sub-area. That is a browser/member task — it cannot be done from public sources, and this pass did not attempt any sign-in.
2. **A board-supplied export.** FVREB (fvreb.bc.ca) could be asked for the sub-area layer as a file (shapefile/GeoJSON/KML) or a printed area/sub-area map; nothing on its public site offers one for download.
3. **AUTOPROP per-address designations** (also member-side) can settle which sub-area a *specific school address* falls in — which is arguably what the school-placement question actually needs (point-in-polygon per address rather than the full boundary) — but it answers one address at a time and still publishes no boundary streets.

Until one of those happens, the correct status for every sub-area boundary in this geography is the one in the CSV: the boundary exists, the board holds it, and it is not public in text form.

## Method

- Area list taken from the program's own files (`batch-1/` … `batch-8/`, `missing/`), §1 identity lines read for each candidate file; board sub-area universe and community groupings from the program's SnapStats September 2026 extraction (`../stats/subarea-stats-sep2026.csv`), cross-checked against the MLS® HPI name hierarchy.
- Web searches run 2026-11-01 for: FVREB MLS area/sub-area maps and boundary descriptions; fvreb.bc.ca statistics packages; the Paragon/AUTOPROP areas guidance (found: Tech Tip #18); sub-area code lists (F-codes); any public shapefile/GeoJSON of FVREB sub-areas (none found). FVREB's public homepage and About page were opened and read in full text.
- No 429s were hit in this pass. No boundary was traced from map pixels; the Tech Tip screenshots were treated as interface illustrations, per the brief.
