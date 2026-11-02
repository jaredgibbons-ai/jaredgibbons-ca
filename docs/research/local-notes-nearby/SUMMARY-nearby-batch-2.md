# What's Nearby — Phase 1, Batch N2 Summary

Batch N2: slugs 26–50 of the phase-1 list, in list order. Files dated 2026-11-02.
Counts = sourced-fact bullets per section (a bullet counts when it carries a source URL on an official or operator page read in this pass). "Measured times" = travel times measured in this pass, all dated 2026-11-02; the routing services do not publish an OSM data date, and each file states that.

Method notes for the whole batch:
- Driving was measured with OSRM (router.project-osrm.org). Walking was measured with the OpenStreetMap routed-foot service (routing.openstreetmap.de); every included walk implies ~4.5 km/h, inside the plausible walking range. The OSRM demo server's foot profile was not used for walking (it returns car-speed durations). Walks that measured beyond the 1.5 km walk cap were dropped and noted in the file; drives beyond the 10 km cap likewise.
- Walks are included in 17 of the 25 files this batch (N1 was drive-only): annieville, central-abbotsford, chilliwack-mountain, east-central-maple-ridge-guide, mission-homes-for-sale, nordel, north-vancouver-homes-for-sale, pitt-meadows-homes-for-sale, scottsdale, southwest-maple-ridge, sunshine-hills-woods, west-vancouver-homes-for-sale, burnaby-hospital, canyon-heights-nv, capitol-hill-bn, caulfeild, central-coquitlam.
- School catchments were not confirmed anywhere in this batch: no district catchment locator was run, so files state "catchment not confirmed".
- Bus frequencies are stated only where an operator page read in this pass states them (the SeaBus daytime frequency, in the two North Shore city files); otherwise they sit under NOT CONFIRMED.
- Save-On-Foods' own store pages repeatedly rendered without a street address; those stores were left unsourced under NOT CONFIRMED rather than cited from a third party. FreshCo/Safeway pages had the same problem in places, and a few retailer/centre pages returned fetch 429s (noted per slug) and were not retried.
- Two files were trimmed after drafting to hold the ~400-word cap; all 25 files are at or under 400 words including URLs.

| # | Slug | §1 Transit | §2 Parks/Rec | §3 Schools | §4 Grocery | §5 Measured times | Gaps |
|---|---|---|---|---|---|---|---|
| 26 | annieville | 2 | 3 | 2 | 2 | 3 | Yes — see list |
| 27 | central-abbotsford | 3 | 3 | 4 | 3 | 4 | Yes — see list |
| 28 | chilliwack-mountain | 3 | 3 | 4 | 1 | 4 | Yes — see list |
| 29 | cottonwood-mr | 3 | 1 | 4 | omitted | 3 | Yes — see list |
| 30 | east-central-maple-ridge-guide | 5 | 2 | 3 | 1 | 4 | Yes — see list |
| 31 | mission-homes-for-sale | 4 | 4 | 3 | 1 | 7 | Yes — see list |
| 32 | nordel | 4 | 3 | 3 | 1 | 6 | Yes — see list |
| 33 | north-vancouver-homes-for-sale | 5 | 4 | 3 | 1 | 3 | Yes — see list |
| 34 | pitt-meadows-homes-for-sale | 4 | 3 | 3 | 1 | 7 | Yes — see list |
| 35 | salmon-river | 3 | 1 | 3 | omitted | 2 | Yes — see list |
| 36 | scottsdale | 4 | 3 | 3 | 1 | 4 | Yes — see list |
| 37 | southwest-maple-ridge | 4 | 3 | 3 | 1 | 4 | Yes — see list |
| 38 | sunnyside-park-surrey | 4 | 3 | 3 | 1 | 2 | Yes — see list |
| 39 | sunshine-hills-woods | 4 | 3 | 3 | 1 | 3 | Yes — see list |
| 40 | tilbury | 2 | omitted | omitted | omitted | 0 | Yes — see list |
| 41 | tsawwassen-north | 4 | 1 | 3 | omitted | 2 | Yes — see list |
| 42 | west-vancouver-homes-for-sale | 5 | 3 | 3 | 1 | 3 | Yes — see list |
| 43 | willoughby-heights | 4 | 1 | 4 | 1 | 3 | Yes — see list |
| 44 | altamont | 4 | 2 | 3 | 1 | 2 | Yes — see list |
| 45 | braemar | 3 | 2 | 3 | 1 | 2 | Yes — see list |
| 46 | burnaby-hospital | 4 | 3 | 3 | 1 | 4 | Yes — see list |
| 47 | canyon-heights-nv | 4 | 3 | 3 | 1 | 3 | Yes — see list |
| 48 | capitol-hill-bn | 5 | 3 | 3 | 1 | 2 | Yes — see list |
| 49 | caulfeild | 3 | 4 | 3 | 2 | 3 | Yes — see list |
| 50 | central-coquitlam | 5 | 3 | 3 | 1 | 4 | Yes — see list |

## Gaps by slug

- **annieville** — Real Canadian Superstore (Scottsdale) store page returned no readable content, so no address; catchments not confirmed; route 312 frequency not stated.
- **central-abbotsford** — No grocery chain store page with a readable central Abbotsford address was read, though §4 carries three shopping-centre anchors; catchments not confirmed; bus frequencies not stated.
- **chilliwack-mountain** — Cottonwood Centre's own site did not display its street address (the centre address in §5 is via the London Drugs page at the centre); supermarket address not confirmed on an allowed source; catchments and frequencies not confirmed/stated.
- **cottonwood-mr** — Section 4 omitted: Save-On-Foods page showed no street address and no other anchor confirmed. Walk to Thomas Haney Secondary measured 1.83 km, over the walk cap, dropped. No City park inside Cottonwood confirmed; catchments not confirmed.
- **east-central-maple-ridge-guide** — Port Haney Station drive not measured (station address geocode did not resolve to the station site); Save-On-Foods at Valley Fair not listed (no address on its page); catchments not confirmed.
- **mission-homes-for-sale** — No bus exchange separate from Mission City Station confirmed; Mission City Hall address not sourced, so not used as the from-point; Superstore walk dropped (2.35 km, over cap); catchments not confirmed.
- **nordel** — Save-On-Foods Scottsdale address not read on the retailer's page; Scott Road Station travel time not measured; catchments not confirmed.
- **north-vancouver-homes-for-sale** — City ground only (District neighbourhoods not covered). Real Canadian Superstore page could not be read (fetch 429), no address given. Phibbs Exchange and Queen Mary Elementary travel times not measured (not attempted / geocode results disagreed). Catchments not confirmed.
- **pitt-meadows-homes-for-sale** — Pitt Meadows Arena address not read on a City page; Superstore walk dropped (2.54 km, over cap); three routes (701, 595, 719/722) not read on a timetable; catchments not confirmed.
- **salmon-river** — Section 4 omitted: no anchor confirmed on a retailer's own site. No Township-published street boundary read (measurements start at the school); no recreation centre/library or Salmon River Natural Area confirmed on a Township page; nearest operating rapid-transit station not confirmed on an official page; walks all over the cap.
- **scottsdale** — Save-On-Foods Scottsdale address not read on the retailer's page; catchments not confirmed; frequencies not stated. (TransLink tt321/tt314 PDFs returned fetch 429s on open; route facts were taken from those same PDFs' content returned by search.)
- **southwest-maple-ridge** — Maple Ridge Library street address not read on an FVRL/municipal page; Fairview Park and Hammond Community Park addresses not shown on the City pages read; catchments not confirmed. (The Maple Ridge Leisure Centre page returned a fetch 429 on open; its address came from the mapleridge.ca search result.)
- **sunnyside-park-surrey** — Safeway Peninsula Village address not read on the retailer's page; walk to Jessie Lee Elementary 1.54 km (over cap, dropped); King George Station drive over the 10 km cap (dropped); nearest station still named as King George Station per the South Surrey rule. Catchments not confirmed.
- **sunshine-hills-woods** — Safeway Sunshine Hills address not read on the retailer's page; Scott Road Station drive over the 10 km cap (dropped); catchments not confirmed.
- **tilbury** — Sections 2, 3 and 4 omitted: no City of Delta park, recreation centre, arena or library in Tilbury confirmed on a municipal page; no school in Tilbury confirmed on a Ministry or SD37 page; no supermarket, shopping centre or pharmacy in Tilbury confirmed on a retailer's own site. No bus exchange in Tilbury confirmed. §5 lists no time: the one drive measured (to Scott Road Station, 13.17 km) exceeded the 10 km cap and was dropped.
- **tsawwassen-north** — Section 4 omitted: the Tsawwassen Mills and Walmart store pages could not be read (fetch 429) and no anchor was addressed from another source. South Delta Recreation Centre's City page also returned 429, so the centre is not listed in §2. No City boundary found (measurements from the library point); catchments not confirmed.
- **west-vancouver-homes-for-sale** — No supermarket address obtained from a retailer's own store page; §4 rests on the Park Royal centre address from the centre's own site. Catchments not confirmed; frequencies not stated except the SeaBus daytime frequency.
- **willoughby-heights** — No library branch address read; Carvolth Exchange street address not on the timetables read (no time measured to it); Yorkson Creek walk 2.05 km, over cap, dropped; catchments not confirmed.
- **altamont** — No District boundary read (measurements from the Caulfeild Elementary point); no park inside Altamont itself confirmed (§2 lists the nearest sourced District facilities); catchments not confirmed.
- **braemar** — Phibbs Exchange could not be sourced as this area's anchor on a TransLink page read in this pass, so §1 names no exchange for Braemar (gap carried in the file); walk to Carisbrooke Elementary 1.61 km, over cap, dropped; no library branch address read for the Braemar/Delbrook area; exact boundaries not read (measurements from Braemar Elementary).
- **burnaby-hospital** — Save-On-Foods near Metrotown not listed (no address on its page); sub-area boundary streets not published by the City (measurements use the hospital address); catchments not confirmed.
- **canyon-heights-nv** — Walk to Capilano Library 2.17 km, over cap (drive used instead); SeaBus beyond the drive cap from the from-point, no measurement; catchments not confirmed.
- **capitol-hill-bn** — Walk to McGill Library 1.91 km, over cap (drive used instead); Kootenay Loop and the Safeway address would not geocode, so no times for them; Eileen Dailly street number not read on a City page; catchments not confirmed.
- **caulfeild** — Route 253's "West Vancouver Blue Bus" operator wording not read on a TransLink/municipal page (bullet says TransLink only); SeaBus beyond the drive cap, no measurement; boundary streets not published (measurements use the school address); catchments not confirmed.
- **central-coquitlam** — Save-On-Foods (Austin Avenue) not listed (no address on its page); §4's Coquitlam Centre address (2929 Barnet Highway) is cited to the centre's own store page on its site; no City neighbourhood-plan boundary confirmed (measurements use the library address); catchments not confirmed.
