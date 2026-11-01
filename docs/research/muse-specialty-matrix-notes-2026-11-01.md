# Specialty-Search Matrix — Notes

Built 2026-11-01. Companion to `specialty-matrix.csv` (101 rows: batch-1 25 + missing 53 + batch-2 23; one row per research FILE — the two dual-slug batch-2 files, salmon-river and poultry-farms, carry both slugs in the slug cell).

## Method — how REAL was decided

- Every cell was judged from that area's own research file only — Sections 4–5 first, then 1/6/7. General knowledge of an area was never used. If the file is silent on a specialty, the cell is "—" even where the stock almost certainly exists.
- **REAL** = the file documents that housing stock/feature as present in the area (zoning that permits it as a live value path, a named project, a documented housing form, or a §6 pricing/value tip). The cell holds the exact buyer search phrase, following the conventions in `keywords.csv` / `METHOD.md` (e.g. "Bradner acreage for sale", "Cultus Lake leasehold homes for sale", "homes with multiplex potential in Nordel", "condos near King George Station"-style anchors).
- **UNVERIFIED** = the file raises the stock but marks it UNVERIFIED itself (most often presale projects the file could not confirm on a City/developer source).
- **"—"** = not applicable or not documented in the file.
- Two anchor columns were held to a higher bar: school-catchment-anchor is REAL only where the file frames a named school/catchment as a demand or pricing factor (merely listing catchments = "—"); transit-anchor is REAL only where a SkyTrain/West Coast Express station or a major transit exchange sits IN the area (RapidBus-only corridors and stations just outside the boundary = "—").
- A secondary suite permitted inside a farm residence under ALC rules counts as homes-with-suites; an accessory farm dwelling unit (AFDU) does not — it is neither a suite nor a carriage house.
- Community/rec-centre pools never count: the pool column is about homes with pools, and no file documents that stock.

## REAL counts per specialty (of 101 areas)

| Specialty | REAL | UNVERIFIED |
|---|---|---|
| multiplex-ssmuh-potential | 50 | 5 |
| homes-with-suites | 48 | 1 |
| carriage-coach-house | 30 | 1 |
| acreage-large-lots | 29 | 0 |
| new-construction-presale | 21 | 19 |
| transit-anchor | 19 | 0 |
| alr-farm | 17 | 17 |
| waterfront | 10 | 0 |
| views | 9 | 0 |
| school-catchment-anchor | 8 | 0 |
| subdivision-potential | 7 | 0 |
| leasehold | 5 | 3 |
| manufactured-mobile | 4 | 0 |
| shop-barn | 3 | 0 |
| corner-ravine-greenbelt | 3 | 0 |
| luxury | 2 | 0 |
| bare-land-lots | 1 | 0 |
| foreclosures | 1 | 0 |
| pool | 0 | 0 |
| fixer-upper | 0 | 0 |
| 55-plus | 0 | 1 |
| pet-friendly-strata | 0 | 0 |
| rentals-allowed-strata | 0 | 0 |

**Widespread:** multiplex/SSMUH potential (50) and homes with suites (48) dominate — nearly every municipal file documents Bill 44 SSMUH rules and secondary-suite rules after the 2024–2026 bylaw rounds. Carriage/coach houses (30) and acreage (29) follow.

**Rare but real:** waterfront (10, all genuinely documented shoreline stock), views (9), catchment anchors (8), subdivision potential (7 — only where a file frames splitting as a live value path; large ALR minimum lot sizes kill it in most farm areas), leasehold (5 — Cultus Lake, UniverCity, UBC, Heather Lands in South Cambie), manufactured/mobile (4).

**Zero evidence anywhere:** pool, fixer-upper, pet-friendly-strata and rentals-allowed-strata scored ZERO REAL across all 101 files. The research files simply never document strata pet/rental bylaws or homes-with-pools stock — these are listing-level facts, not area-research facts, so no page should be built on them until listing data exists. 55-plus appears once, as UNVERIFIED in the mobile-home topic guide (55+ parks discussed; park names unverified).

## Strongest region-wide opportunities

1. **Multiplex / SSMUH potential — REAL in 50 of 101 areas, no dedicated page exists.** This is the single biggest gap the matrix reveals. The files document unit counts, zone rules and "check before paying for multiplex potential" advice in area after area (Delta, DNV, Port Moody, Port Coquitlam, Maple Ridge, Surrey, Vancouver R1-1, Burnaby R1, Abbotsford s.140). A region-wide multiplex-potential hub, or SSMUH sections rolled into the existing area pages, would cover documented demand no competitor page currently organizes. (Existing topic files cover farms, poultry, foreclosures, mobile homes and open houses — nothing covers SSMUH.)
2. **Homes with suites (48 REAL) and coach/carriage houses (30 REAL) — no dedicated page exists.** Suites are the classic investor/owner-occupier search and the files document the rules everywhere, including farm areas where an ALC-permitted suite inside the residence is REAL (Bradner, Aberdeen, Matsqui). A "homes with suites" specialty layer across the Fraser Valley files is the second-biggest uncovered block.
3. **Acreage (29 REAL) beyond Langley.** Farm topics are covered — `langley-farms` (acreage, ALR, bare land, barns all REAL) and `poultry-farms` exist, and foreclosures has its Langley topic page (the only REAL in that column). But acreage as a specialty is documented just as strongly in Abbotsford (Bradner, Matsqui, Aberdeen, Sumas Mountain), Chilliwack and Maple Ridge/Pitt Meadows, where no acreage hub exists. An Abbotsford/Valley acreage page is the natural extension of the Langley farms model.
4. **Transit anchors — REAL in 19 areas** (Surrey Central, King George corridor, Oakridge–41st, Sapperton, Moody Centre, Port Coquitlam, Port Haney, Maple Meadows, Pitt Meadows, Mission City, Lonsdale Quay, Brighouse, plus the Park Royal / SFU / UBC exchanges and two future Broadway Subway stations). No transit-oriented specialty page exists; the phrases are already in the matrix for page copy.
5. **New construction / presale — REAL 21 but UNVERIFIED 19.** Demand is documented almost as often as confirmed supply. Nearly half the files could not verify a single selling project from an official/developer source, so build presale pages only where the cell is REAL, and re-verify the UNVERIFIED cells at build time rather than treating them as stock.

## Files too thin or special to judge normally

- **Annacis Island, Tilbury** — industrial files; both document that there is essentially no residential market. All "—" is a finding, not thinness.
- **Furry Creek** — all "—": the file documents SSMUH exemption by provincial ruling and negates the other specialties.
- **Sea Island** — all "—": only the Burkeville housing pocket exists; the Canada Line stations serve YVR, not the pocket, so no transit anchor.
- **Surrey Open Houses** — a feed/topic file covering all Surrey property types; no area-specific stock to judge.
- **Cultus Lake South** — nearly empty file; the only non-"—" cell is alr-farm UNVERIFIED.
- **Mount Currie** — Líl̓wat Nation reserve land. Manufactured/mobile is REAL per its §5 (modular/manufactured homes in the Nation Housing Plan), but standard MLS sale and foreclosure mechanics do not apply (the file documents Ministerial Loan Guarantee financing), so the rest of the row is "—" by structure, not by absence of housing.
- **Panorama Ridge (a caution, not thin)** — the file never documents views despite the name, so views = "—". A reminder that every cell follows the file, not the area's reputation.
