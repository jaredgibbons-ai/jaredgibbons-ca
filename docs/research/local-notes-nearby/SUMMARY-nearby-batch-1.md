# What's Nearby — Phase 1, Batch N1 Summary

Batch N1: slugs 1–25 of the phase-1 list, in list order. Files dated 2026-11-02.
Counts = sourced-fact bullets per section (a bullet counts when it carries a source URL on an official or operator page read in this pass). "Measured times" = travel times measured in this pass with OSRM (router.project-osrm.org) after OpenStreetMap Nominatim geocoding, all dated 2026-11-02; the routing service does not publish an OSM data date, and each file states that.

Method notes for the whole batch:
- The OSRM demo server's foot profile returned car-speed durations in this pass, so no walk time is quoted anywhere in the batch; section 5 is drive-only, and the affected files note this under NOT CONFIRMED.
- School catchments were not confirmed anywhere in this batch: no district catchment locator was run, so files state "catchment not confirmed" (a locator run is the fix in a later pass).
- Bus frequencies are stated only where an operator timetable page read in this pass states them; otherwise they sit under NOT CONFIRMED.
- Save-On-Foods' own store pages repeatedly rendered without a street address in the page text; those stores were left unsourced under NOT CONFIRMED rather than cited from a third party.

| # | Slug | §1 Transit | §2 Parks/Rec | §3 Schools | §4 Grocery | §5 Measured times | Gaps |
|---|---|---|---|---|---|---|---|
| 1 | abbotsford-east-guide | 5 | 5 | 6 | 3 | 2 | Yes — see list |
| 2 | abbotsford-west-guide | 5 | 4 | 5 | 3 | 3 | Yes — see list |
| 3 | aberdeen-guide | 4 | 1 | 1 | omitted | 1 | Yes — see list |
| 4 | aldergrove-guide | 4 | 3 | 5 | 0 | 3 | Yes — see list |
| 5 | bradner-guide | 3 | 2 | 1 | omitted | 2 | Yes — see list |
| 6 | central-abbotsford-guide | 5 | 5 | 5 | 3 | 3 | Yes — see list |
| 7 | delta-manor-guide | 5 | 2 | 3 | 1 | 4 | Yes — see list |
| 8 | east-newton-guide | 5 | 5 | 4 | 2 | 3 | Yes — see list |
| 9 | english-bluff-guide | 5 | 4 | 3 | 1 | 3 | Yes — see list |
| 10 | fort-langley-guide | 3 | 1 | 3 | 0 | 3 | Yes — see list |
| 11 | hawthorne-guide | 5 | 3 | 2 | 1 | 4 | Yes — see list |
| 12 | holly-guide | 4 | 2 | 2 | 1 | 4 | Yes — see list |
| 13 | ladner-elementary-guide | 4 | 2 | 3 | 1 | 4 | Yes — see list |
| 14 | matsqui-guide | 3 | 3 | 3 | 0 | 2 | Yes — see list |
| 15 | neilsen-grove-guide | 4 | 3 | 2 | 1 | 4 | Yes — see list |
| 16 | panorama-ridge-guide | 5 | 5 | 4 | 2 | 2 | Yes — see list |
| 17 | poplar-guide | 2 | 4 | 4 | 0 | 3 | Yes — see list |
| 18 | port-guichon-guide | 5 | 3 | 3 | omitted | 3 | Yes — see list |
| 19 | sumas-mountain-guide | 3 | 5 | 4 | 0 | 2 | Yes — see list |
| 20 | tsawwassen-central-guide | 5 | 3 | 3 | 1 | 3 | Yes — see list |
| 21 | tsawwassen-east-guide | 4 | 4 | 3 | 1 | 3 | Yes — see list |
| 22 | tsawwassen-north-guide | 4 | 3 | 4 | 2 | 3 | Yes — see list |
| 23 | west-chilliwack-guide | 3 | 1 | 3 | 2 | 3 | Yes — see list |
| 24 | west-newton-guide | 6 | 5 | 3 | 2 | 4 | Yes — see list |
| 25 | annacis-island | 3 | omitted | omitted | omitted | 1 | Yes — see list |

## Gaps by slug

- **abbotsford-east-guide** — Save-On-Foods (Whatcom Road) address not displayed on the retailer's store page as read; school catchments not confirmed; bus frequencies not stated (timetables not read route by route).
- **abbotsford-west-guide** — School catchments not confirmed; bus frequencies not stated; Save-On-Foods (Clearbrook) address not displayed on the retailer's page as read.
- **aberdeen-guide** — Section 4 omitted: no supermarket or shopping centre inside Aberdeen confirmed on an allowed source. No city park in the area on the Abbotsford parks list read; no municipal page for a recreation centre in Aberdeen; no middle or secondary school in the area on the Ministry list; catchment not confirmed; route 21 frequency not stated.
- **aldergrove-guide** — No sourced §4 anchor: the FreshCo store page was not read in this pass (page-fetch rate limit), so the anchor sits under NOT CONFIRMED. Aldergrove Regional Park street address not shown on the page portion read; future SkyTrain stations not confirmed (none presented as operating); catchments not confirmed.
- **bradner-guide** — Section 4 omitted: no supermarket or shopping centre inside Bradner confirmed on an allowed source. No bus route through Bradner's interior roads confirmed; no municipal page for a recreation centre in Bradner; no middle or secondary school in the area; catchment not confirmed.
- **central-abbotsford-guide** — School catchments not confirmed; bus frequencies not stated; Save-On-Foods (Clearbrook) address not displayed on the retailer's page as read.
- **delta-manor-guide** — Catchment not confirmed; Memorial Park address not stated (the City of Delta park search page could not be read); Save-On-Foods Ladner address not shown on the retailer's page; no walk times quoted (OSRM foot profile returned driving durations).
- **east-newton-guide** — No grocery store east of King George Boulevard inside East Newton confirmed on a retailer's own site; school catchments not confirmed.
- **english-bluff-guide** — Catchments not confirmed; South Delta Exchange street address not stated on the timetables read; no supermarket inside English Bluff itself (the listed anchor is in the Tsawwassen town centre).
- **fort-langley-guide** — Named parks not listed: no Township of Langley parks page was read in this pass (page-fetch rate limit). Lee's Market not listed (no retailer or Township page read); nearest recreation centre address not confirmed; future SkyTrain stations not presented as operating; catchments not confirmed.
- **hawthorne-guide** — Catchment not confirmed; Save-On-Foods Ladner address not shown; no supermarket inside Hawthorne itself; no walk times quoted (OSRM foot profile).
- **holly-guide** — Catchment not confirmed; no park inside Holly confirmed by official City of Delta name; no bus route with a stop inside Holly itself confirmed; Save-On-Foods Ladner address not shown; no walk times quoted (OSRM foot profile).
- **ladner-elementary-guide** — Catchment not confirmed; Memorial Park address not stated (Delta park search page could not be read); Save-On-Foods Ladner address not shown; no supermarket inside the area itself; no walk times quoted (OSRM foot profile).
- **matsqui-guide** — Rapid transit inside Abbotsford: no official page read states it either way, so no station is named. No sourced §4 anchor (no retailer or municipal commercial page read); catchments not confirmed; Matsqui Trail Regional Park address not sourced.
- **neilsen-grove-guide** — Catchment not confirmed; no park inside Neilsen Grove confirmed by official City of Delta name; Save-On-Foods Ladner address not shown; no supermarket inside Neilsen Grove itself; no walk times quoted (OSRM foot profile).
- **panorama-ridge-guide** — No grocery store inside Panorama Ridge confirmed on a retailer's own site; no recreation centre or library inside the area confirmed on a municipal page; no official City boundary for Panorama Ridge found (measured from the 64 Avenue and 144 Street intersection); catchments not confirmed; no walk times quoted (OSRM foot profile).
- **poplar-guide** — BC Transit route pages for the local Poplar routes were not read in this pass, so §1 carries no route bullets; rapid transit in Abbotsford not stated on any page read; no sourced §4 anchor; catchments not confirmed.
- **port-guichon-guide** — Section 4 omitted: the Save-On-Foods Ladner store-locator page as read displayed no street address. Catchments not confirmed; Ladner Harbour Park street address not shown on the Delta park page read; Ladner Exchange street address not stated on the timetables read.
- **sumas-mountain-guide** — Sumas Mountain Regional Park page not read (page-fetch rate limit); BC Transit route 9 and 15 pages not read (rate limit); rapid transit in Abbotsford not stated on any page read; no sourced §4 anchor; catchments not confirmed; Abbotsford Recreation Centre address not read on a municipal page.
- **tsawwassen-central-guide** — Catchments not confirmed; Winskill Park street address not shown on the Delta park page read; South Delta Exchange street address not stated on the timetables read.
- **tsawwassen-east-guide** — Catchments not confirmed; no supermarket inside Tsawwassen East itself (anchor listed is in the town centre); South Delta Exchange street address not stated.
- **tsawwassen-north-guide** — Catchments not confirmed; Winskill Park street address not shown; South Delta Exchange street address not stated; no official City boundary for Tsawwassen North found (measurements from the Tsawwassen Mills point, stated in the file).
- **west-chilliwack-guide** — No rapid-transit station named for Chilliwack on an official page read; no park inside West Chilliwack confirmed on a City parks page; no recreation centre inside the area confirmed; no grocery store on Evans Road or inside the area confirmed; catchments not confirmed; no City-published boundary found.
- **west-newton-guide** — No grocery store west of King George Boulevard confirmed on a retailer's own site (confirmed anchors are at the King George Boulevard / 72 Avenue edge); catchments not confirmed; no walk times quoted (OSRM foot profile).
- **annacis-island** — Sections 2, 3 and 4 omitted: no City of Delta park, recreation centre, arena or library on the island confirmed on a municipal page; no school on the island confirmed on a Ministry or SD37 page; no supermarket, shopping centre or pharmacy on the island confirmed on a retailer's own site. No bus exchange on the island confirmed; only one travel time fell within the distance caps.
