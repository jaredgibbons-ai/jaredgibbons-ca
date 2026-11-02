# What's Nearby — Phase 1, Batch N5 Summary

Batch N5: slugs 101–125 of the phase-1 list, in list order. Files dated 2026-11-02.
Counts = sourced-fact bullets per section (a bullet counts when it carries a source URL on an official or operator page read in this pass). "Measured times" = travel times measured in this pass, all dated 2026-11-02; the routing services do not publish an OSM data date, and each file states that.

Method notes for the whole batch:
- Driving was measured with OSRM (router.project-osrm.org). Walking was measured with the OpenStreetMap routed-foot service (routing.openstreetmap.de); kept walks imply ~4.3–5.8 km/h, inside the plausible walking range. The OSRM demo server's foot profile was not used for walking. Walks beyond the 1.5 km walk cap and drives beyond the 10 km cap were dropped and noted in the file.
- School catchments were not confirmed anywhere in this batch: no district catchment locator was run, so files state "catchment not confirmed".
- Bus frequencies are stated only where an operator page read in this pass states them (the SeaBus 15-minute daytime frequency in cedardale and calverhall); otherwise they sit under NOT CONFIRMED.
- Save-On-Foods' own store pages repeatedly rendered without a street address; those stores were left unsourced under NOT CONFIRMED rather than cited from a third party (east-burnaby, hockaday, lower-landing, and the omitted §4 sections in riverdale-ri and big-bend).
- No fetch 429s were hit anywhere in this batch.
- Two walks were dropped for implausible routed-foot speed and disclosed in their file: both east-burnaby walks (Edmonds Station at ~3.4 km/h and Edmonds Community Centre at ~3.9 km/h, below the plausible walking range).
- One worker group caught a scratch-file collision with a parallel session that had fed it another session's geocodes; it re-verified every point from its own Nominatim queries, re-routed all measurements, and corrected its five files (cariboo, cedardale, central-lonsdale, collingwood-ve, delbrook) in place. The corrected figures are the ones in those files.
- Geography locks held against fresh official sources throughout: brunette and fraserview-nw written as New Westminster; hockaday and eagle-ridge-cq as Coquitlam; calverhall from City of North Vancouver sources only; cedardale and bayridge name the District of West Vancouver plainly (page names, not confirmed official neighbourhood names); lower-landing is titled London Landing, Steveston, as the sources name it; riverdale-ri states both names (the pocket is Riverdale; the City plans and serves it as Thompson).
- All 25 files are at or under 400 words including URLs (range 311–400). Ten files were trimmed by the coordinator after the workers reported — wording only; no sourced fact, source URL, measured time or NOT CONFIRMED item was dropped.
- Total §5 measured times in this batch: 97.

| # | Slug | §1 Transit | §2 Parks/Rec | §3 Schools | §4 Grocery | §5 Measured times | Gaps |
|---|---|---|---|---|---|---|---|
| 101 | cariboo | 3 | 2 | 3 | 2 | 4 | Yes — see list |
| 102 | cedardale | 3 | 4 | 3 | 3 | 3 | Yes — see list |
| 103 | central-lonsdale | 4 | 2 | 3 | 2 | 4 | Yes — see list |
| 104 | collingwood-ve | 5 | 4 | 5 | 1 | 4 | Yes — see list |
| 105 | delbrook | 3 | 3 | 3 | 1 | 3 | Yes — see list |
| 106 | downtown-ve | 2 | 2 | 3 | 1 | 4 | Yes — see list |
| 107 | eagle-ridge-cq | 3 | 2 | 3 | 2 | 3 | Yes — see list |
| 108 | east-burnaby | 3 | 1 | 3 | 1 | 2 | Yes — see list |
| 109 | fairview-vw | 2 | 2 | 3 | 2 | 3 | Yes — see list |
| 110 | forest-glen-bs | 3 | 2 | 3 | 1 | 4 | Yes — see list |
| 111 | fraserview-nw | 4 | 4 | 3 | 1 | 5 | Yes — see list |
| 112 | government-road | 3 | 2 | 3 | 2 | 5 | Yes — see list |
| 113 | grandview-woodland | 5 | 5 | 4 | 1 | 3 | Yes — see list |
| 114 | hockaday | 4 | 3 | 4 | 1 | 5 | Yes — see list |
| 115 | lower-landing | 4 | 3 | 3 | 2 | 4 | Yes — see list |
| 116 | parkcrest | 5 | 3 | 3 | 1 | 4 | Yes — see list |
| 117 | queensborough | 4 | 4 | 2 | 1 | 4 | Yes — see list |
| 118 | riverdale-ri | 3 | 4 | 3 | omitted | 4 | Yes — see list |
| 119 | bayridge | 3 | 4 | 2 | 1 | 5 | Yes — see list |
| 120 | big-bend | 3 | 2 | 2 | omitted | 4 | Yes — see list |
| 121 | blueridge-nv | 3 | 3 | 3 | 1 | 4 | Yes — see list |
| 122 | brentwood-park | 4 | 3 | 3 | 1 | 4 | Yes — see list |
| 123 | brunette | 3 | 3 | 4 | 2 | 4 | Yes — see list |
| 124 | burke-mountain | 2 | 2 | 4 | 1 | 4 | Yes — see list |
| 125 | calverhall | 3 | 3 | 2 | 2 | 4 | Yes — see list |

## Gaps by slug

- **cariboo** — Catchments and bus frequencies not confirmed.
- **cedardale** — No walks kept: walks to Cedardale Park (1.79 km) and West Vancouver Secondary (2.36 km) exceed the 1.5 km cap and are noted in-file, drives reported; West Vancouver Community Centre street address not shown on the facility page read; park street addresses and boundary streets not confirmed; catchments not confirmed.
- **central-lonsdale** — Catchments and bus frequencies not confirmed.
- **collingwood-ve** — Catchments and bus frequencies not confirmed.
- **delbrook** — Queensdale Market drive withdrawn: 3030 Lonsdale Ave would not resolve to a verified numbered point (road segments only), so no time is stated and the gap is noted in-file; walk to Braemar Elementary (1.83 km) dropped over the walk cap; catchments not confirmed.
- **downtown-ve** — No bus exchange named: no TransLink page read supports one as the area's anchor; the T&T Supermarket (Chinatown) address is sourced from a search result on the retailer's own domain; catchments not confirmed.
- **eagle-ridge-cq** — Walk to the area park dropped over the walk cap (1.86 km); City Centre Aquatic Complex appears only as a §5 drive target; catchments not confirmed.
- **east-burnaby** — Section 4 is a pharmacy anchor only, disclosed in-file; Save-On-Foods Highgate sits under NOT CONFIRMED (its store page carried no street address); both walks dropped for implausible routed-foot speed (3.4 and 3.9 km/h) and noted in-file; catchments not confirmed.
- **fairview-vw** — No bus exchange named (same ground as downtown-ve); walks to the station (2.07 km) and Whole Foods (1.57 km) omitted over the walk cap; catchments not confirmed.
- **forest-glen-bs** — Catchments and bus frequencies not confirmed.
- **fraserview-nw** — Catchments not confirmed.
- **government-road** — Walk Seaforth Elementary → Burnaby Lake Park dropped over the walk cap (2.26 km); nearest station settled by measurement (Production Way–University at 2.46 km, ahead of Sperling–Burnaby Lake and Lougheed); catchments not confirmed.
- **grandview-woodland** — Walks from Britannia Community Centre to Commercial-Broadway Station (1.62 km) and to Safeway (1.66 km) dropped over the walk cap; Grandview ʔuuqinak'uuh Elementary left out because the Ministry page renders its name with a character-encoding artifact that could not be copied with certainty; catchments not confirmed.
- **hockaday** — Save-On-Foods (Coquitlam) sits under NOT CONFIRMED (store page renders without a street address); walk Pinetree Secondary → Mundy Park dropped (5.89 km on park-centroid routing); nearest station settled by measurement (Lafarge Lake–Douglas at 0.85 km); catchments not confirmed.
- **lower-landing** — No City of Richmond page uses "Lower Landing"; the file names the area London Landing / Steveston and flags this in-file; Save-On-Foods Steveston sits under NOT CONFIRMED (no street address on its page); walk London's Wharf → Westwind Elementary dropped over the walk cap (2.00 km); the City lists Steveston Community Centre at 4111 Moncton St (used in §2) while OpenStreetMap places it at 4320 Moncton St (the Easthope Hub site) — the §5 library measurement was routed to the 4320 Moncton point and labelled as the library; catchments not confirmed.
- **parkcrest** — No bus exchange named (no TransLink page read supports one); the Safeway address comes from its safeway.ca search result because the store page read rendered without the street address — disclosed in-file; exact boundary streets not confirmed; catchments and frequencies not confirmed.
- **queensborough** — No secondary school on the island (the Ministry list read shows none); the SkyTrain station and bus exchange are on the mainland side of the Queensborough Bridge, stated in-file; catchments and frequencies not confirmed.
- **riverdale-ri** — Section 4 omitted: no supermarket or centre inside the pocket was confirmed on a retailer's or centre's own page, and the Save-On-Foods page checked renders without a street address; "Riverdale" is not confirmed as a City planning name (City pages use Thompson); no bus exchange named; catchments not confirmed.
- **bayridge** — No rapid-transit station serves the area (bus only), stated in-file; Benbow Park and West Bay Park addresses come from search results on the District's domain because its parks page read did not list them; catchments and frequencies not confirmed.
- **big-bend** — Section 4 omitted: the Save-On-Foods (Market Crossing) page checked renders without a street address and no in-area anchor was confirmed; no public school inside Big Bend itself confirmed (the schools listed sit on Marine Drive and up the south slope); no bus exchange named; catchments not confirmed.
- **blueridge-nv** — Section 4 carries the nearest supermarket (Save-On-Foods Park & Tilford, from the retailer's own store list) with an in-file disclosure that no in-neighbourhood supermarket was confirmed; catchments not confirmed.
- **brentwood-park** — Section 4 is a shopping-centre anchor (The Amazing Brentwood, from the centre's own site) with an in-file disclosure that no supermarket inside the centre was confirmed; Brentwood Community Centre is a future City project, not yet open, so it is not listed as a current anchor; catchments and frequencies not confirmed.
- **brunette** — Whether Sapperton Station has direct bus connections is not stated on any TransLink page read; Hume Park's civic address is not on a City facility page read (the measured point used the Hume Park outdoor pool on E. Columbia St); route 155 frequency not in the timetable extract read; the Brewery District tenant fact comes from a search result on the centre owner's domain because the page itself sat behind a verification screen — flagged in-file; catchments not confirmed.
- **burke-mountain** — Section 4 is a shopping-centre anchor (Coquitlam Centre) with an in-file disclosure that no Burke Mountain supermarket was confirmed open (City material describes one as anticipated in the future village centre); route 188 timetable not opened in this pass; no Lafarge Lake–Douglas Station measurement is reported because the station-name geocode landed outside Coquitlam — the Coquitlam Central Station measurement is the station figure used, disclosed in-file; catchments not confirmed.
- **calverhall** — Walks to the City Library (1.76 km) and Shoppers Drug Mart (1.78 km) exceeded the walk cap, so driving times are reported instead; only route 230 was verified from a TransLink timetable at the Lonsdale Quay loop; Calverhall's exact boundary is not stated on a City page read (measurements use the Harry Jerome Centre as the from-point); catchments not confirmed.
