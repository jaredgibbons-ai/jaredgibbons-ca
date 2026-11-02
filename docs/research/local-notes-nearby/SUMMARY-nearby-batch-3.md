# What's Nearby — Phase 1, Batch N3 Summary

Batch N3: slugs 51–75 of the phase-1 list, in list order. Files dated 2026-11-02.
Counts = sourced-fact bullets per section (a bullet counts when it carries a source URL on an official or operator page read in this pass). "Measured times" = travel times measured in this pass, all dated 2026-11-02; the routing services do not publish an OSM data date, and each file states that.

Method notes for the whole batch:
- Driving was measured with OSRM (router.project-osrm.org). Walking was measured with the OpenStreetMap routed-foot service (routing.openstreetmap.de); every included walk implies ~4.3–4.7 km/h, inside the plausible walking range. The OSRM demo server's foot profile was not used for walking. Walks beyond the 1.5 km walk cap and drives beyond the 10 km cap were dropped and noted in the file.
- School catchments were not confirmed anywhere in this batch: no district catchment locator was run, so files state "catchment not confirmed".
- Bus frequencies are stated only where an operator page read in this pass states them (West Coast Express timetable departures in the Pitt Meadows files; the SeaBus 15-minute daytime frequency in ambleside); otherwise they sit under NOT CONFIRMED.
- Save-On-Foods' own store pages repeatedly rendered without a street address; those stores were left unsourced under NOT CONFIRMED rather than cited from a third party. No fetch 429s were hit in this batch; two retailer store pages returned no extractable content (Real Canadian Superstore, Meadowtown and Pitt Meadows) and were not retried — the Meadowtown Superstore is sourced from Meadowtown Centre's own site plan instead.
- Canyon Springs: fresh official sources confirm the Coquitlam placement (SD43 schools, TransLink route 183, Coquitlam geocode) — no conflict with the program's slug record; the North Vancouver Canyon Springs did not surface in any official source used.
- Garden Village: the research record places it in Burnaby (Patterson Station / Central Park / Maywood); the file follows that.
- All 25 files are at or under 400 words including URLs (range 255–399).

| # | Slug | §1 Transit | §2 Parks/Rec | §3 Schools | §4 Grocery | §5 Measured times | Gaps |
|---|---|---|---|---|---|---|---|
| 51 | central-meadows-pitt-meadows | 4 | 3 | 3 | 1 | 4 | Yes — see list |
| 52 | chelsea-park | 4 | 3 | 3 | 1 | 4 | Yes — see list |
| 53 | connaught-heights | 5 | 2 | 3 | 1 | 4 | Yes — see list |
| 54 | coquitlam-west | 5 | 3 | 3 | 2 | 4 | Yes — see list |
| 55 | deer-lake | 3 | 3 | 2 | 1 | 4 | Yes — see list |
| 56 | east-cambie | 3 | 3 | 2 | 1 | 3 | Yes — see list |
| 57 | edmonds-be | 4 | 2 | 2 | omitted | 3 | Yes — see list |
| 58 | fraser-ve | 4 | 2 | 2 | 1 | 2 | Yes — see list |
| 59 | garden-village | 3 | 1 | 2 | 1 | 2 | Yes — see list |
| 60 | killarney-ve | 5 | 3 | 3 | omitted | 3 | Yes — see list |
| 61 | kitsilano | 5 | 3 | 3 | 1 | 5 | Yes — see list |
| 62 | mid-meadows-pitt-meadows | 5 | 3 | 3 | 3 | 5 | Yes — see list |
| 63 | montecito | 5 | 4 | 3 | 1 | 3 | Yes — see list |
| 64 | moody-park | 4 | 4 | 3 | 2 | 4 | Yes — see list |
| 65 | quay | 4 | 3 | 3 | 2 | 4 | Yes — see list |
| 66 | quilchena-ri | 4 | 3 | 3 | 1 | 3 | Yes — see list |
| 67 | west-cambie | 3 | 2 | 3 | 1 | 3 | Yes — see list |
| 68 | west-meadows-pitt-meadows | 3 | 3 | 3 | 2 | 3 | Yes — see list |
| 69 | ambleside | 5 | 3 | 3 | 2 | 3 | Yes — see list |
| 70 | arbutus | 5 | 3 | 3 | 1 | 2 | Yes — see list |
| 71 | buckingham-heights | 4 | 2 | 2 | 2 | 3 | Yes — see list |
| 72 | canterbury-wv | 4 | 3 | 2 | 1 | 3 | Yes — see list |
| 73 | canyon-springs | 4 | 3 | 3 | 2 | 3 | Yes — see list |
| 74 | capilano-nv | 3 | 2 | 2 | 1 | 3 | Yes — see list |
| 75 | champlain-heights | 3 | 2 | 3 | 1 | 2 | Yes — see list |

## Gaps by slug

- **central-meadows-pitt-meadows** — Save-On-Foods Pitt Meadows page rendered without a street address; catchments and frequencies not confirmed.
- **chelsea-park** — "Chelsea Park" not confirmed as a District of West Vancouver neighbourhood name (municipality named plainly); no District park inside Chelsea Park itself read; walk to West Vancouver Secondary 2.20 km, over cap, dropped (drive listed instead); catchments not confirmed.
- **connaught-heights** — təməsew̓txʷ centre street address not read on a City page, so not listed in §2; Save-On-Foods Columbia Square page rendered without an address; catchments not confirmed.
- **coquitlam-west** — Catchments and frequencies not confirmed.
- **deer-lake** — Bonsor Recreation Complex address not read on a City page; catchments not confirmed.
- **east-cambie** — No supermarket address read on a retailer's own page (§4 carries Shoppers Drug Mart only); boundary streets, catchments and frequencies not confirmed. King George Secondary was not placed here (it is a Vancouver school).
- **edmonds-be** — Section 4 omitted: Highgate Save-On-Foods and Kings Crossing PriceSmart Foods pages displayed no street address. Catchments not confirmed.
- **fraser-ve** — No supermarket anchor confirmed; corridor boundary not confirmed (spans several City local areas); catchments not confirmed.
- **garden-village** — Section 2 carries Central Park only; walk to Central Park measured 1.68 km, over the walk cap, dropped; catchments not confirmed.
- **killarney-ve** — Section 4 omitted: Champlain Square's own site loaded with no street address. Catchments not confirmed.
- **kitsilano** — Safeway West 4th Avenue not listed (its own page rendered no street address); catchments not confirmed.
- **mid-meadows-pitt-meadows** — Superstore's own store page unreadable this pass (listed from Meadowtown Centre's own site plan); Osprey Village grocery/pharmacy unconfirmed; catchments not confirmed.
- **montecito** — Safeway Kensington Square not listed (own page showed no address); Montecito Park walk 1.75 km, over cap, so a drive is listed; the pharmacy address would not geocode, so no measurement to it; catchments not confirmed.
- **moody-park** — Royal City Centre's own pages printed no street address (610 6th St taken from its Shoppers store page, flagged in-file); Save-On-Foods at the centre not listed (no address on the chain's page); catchments not confirmed.
- **quay** — River Market not listed (the market's own site served no readable address); Save-On-Foods Columbia Square not listed; catchments not confirmed.
- **quilchena-ri** — Walks to Terra Nova Rural Park (2.76 km) and Terra Nova Village (1.81 km) over the walk cap, dropped; catchments and frequencies not confirmed.
- **west-cambie** — Bridgeport Station's bus exchange was not named on any TransLink page read, so Richmond–Brighouse (route 410 terminus) is the named exchange; only route 410 was read on a timetable; catchments not confirmed.
- **west-meadows-pitt-meadows** — Catchments not confirmed.
- **ambleside** — Ambleside Park's street address is not on the District park page, so the §5 drive destination carries no address; catchments not confirmed.
- **arbutus** — Safeway Arbutus (Arbutus Village) rendered without a street address on its own store page (the addressed anchor used is Safeway King Edward Mall); walk to Prince of Wales Secondary 2.03 km, over cap, dropped; catchments not confirmed.
- **buckingham-heights** — Catchments and frequencies not confirmed. Measured drives put Sperling–Burnaby Lake Station (4.49 km) marginally closer than Metrotown Station (4.62 km), so Sperling is named nearest.
- **canterbury-wv** — "Canterbury" not confirmed as an official District neighbourhood name (municipality named plainly); SeaBus unmeasured (beyond the drive cap); catchments not confirmed.
- **canyon-springs** — Walk to Glen Park measured 1.51 km, beyond the walk cap, dropped; catchments and frequencies not confirmed.
- **capilano-nv** — Catchments and frequencies not confirmed.
- **champlain-heights** — Your Independent Grocer walk 1.60 km, over cap, dropped; Champlain Square centre address not confirmed (the centre's own site rendered only "Loading…"); catchments not confirmed.
