# What's Nearby — Phase 2, Batch P2-7 Summary

Produced 2026-11-02 under PHASE2-BRIEF.md. Roster range covered: **entries 154–179 — 25 buildings produced.** Skipped: **entry 156, Winona Park Chateau Parkside Residences (cambie; townhomes) — ADDRESS CONFLICT** (344 West 62nd Avenue / 322 West 62nd Avenue), held for the final mop-up batch; its address was not researched. Extension to entry 179 was needed to reach 25 addressed buildings. **Mop-up list to date: entries 52 (The Hart), 85 (District Flats at Southlands), 86 (The Granary at Southlands), 156 (Winona Park).**

Areas: cambie 2, canyon-springs 5, capilano-nv 2, capitol-hill-bn 9, cariboo 5, caulfeild 1, central-abbotsford 1. All five sections + NOT CONFIRMED written in every file — **no sections omitted anywhere**.

**Measurements: 109 kept (63 walk, 46 drive)**, all measured 2026-11-02 starting at each building's own address; every kept walk inside the 4–6 km/h sanity band (one walk at exactly 6.0 km/h, flagged per building below) and the walk ≤1.5 km / drive ≤10 km caps; over-cap routes measured, discarded and disclosed in-file (noted per building below). **HTTP 429s: none** across all five workers (Nominatim, OSRM driving, routed-foot).

**Roster lines proved wrong on the ground: none** — the roster was never silently corrected.

**Two process incidents, both self-caught, corrected in the foreground before delivery, and disclosed in the affected files (the P2-5/P2-6 backgrounded-geocode failure mode, twice more):**
1. Worker C (entries 165–169): a completed geocode run returned named OSM points for Capitol Hill Elementary School and Burnaby North Secondary School that differ from the first-pass anchor points. The six affected school walks (Alto, Capitol Hill 388 Ellesmere, Cedarwood) were re-measured in the foreground to the named points, which govern; the discrepancy is disclosed in each file's NOT CONFIRMED. Its Cassia disclosure was also corrected: plain-address interpolation for 6965 Hastings Street proved unstable in both directions across runs; the postal-code segment point used is unchanged and its three walks stand.
2. Worker D (entries 170–174): the full output of its first geocode script arrived late and disagreed with the Capitol Hill points it had routed from. Centrale, Hilltop Greene and Saturna were re-geocoded in the foreground (Nominatim returns only street-segment points for these Hastings/Ellesmere addresses — no house points), every measurement re-taken from the governed points, the three files rewritten, and the discrepancy disclosed in each file's NOT CONFIRMED; the earlier Capitol Hill values are withdrawn and appear nowhere in the delivered files. Its two Cariboo files stand unchanged — their foreground re-run points match the late-arriving full output exactly.
This coordinator spot-checked the corrected Centrale and Alto files in full on disk; the corrected figures and disclosures are what the files carry.

**Word-cap overages (disclosed; wording trimmed only, no cited fact or URL cut):** Alameda Court 566 (+166), Strathmore Towers 509 (+109), Strathmore Lane 506 (+106), Caulfeild Cove 491 (+91), Kirkstone Gardens 489 (+89), Brookside Park 483 (+83), Balmoral House 445 (+45), Barclay Woods 430 (+30), West 41 Oakridge 424 (+24), Brookside Court 419 (+19), Canyon Park 411 (+11), The Jefferson 408 (+8). The overages are driven by required geocode/anchor disclosures, multi-address headers, and scope disclosures where no anchor sits within ~1 km (Kirkstone Gardens, Caulfeild Cove, Alameda Court). All other files 305–380 words.

---

## Per-building detail

### 154. OPAL by Element — 438 West King Edward Avenue (cambie; condos)
- File: opal-by-element--cambie-nearby-2026-11-02.md — 2,580 B; 335 words — within cap
- Origin: exact OSM house point for 438 West King Edward Avenue
- Measurements (6): walk King Edward Station 0.24 km / 3.1 min; walk Edith Cavell Elementary 0.76 / 10.2; walk Safeway King Edward Mall (990 King Edward Ave, verified on Safeway's own store page) 0.77 / 10.3; walk Douglas Park Community Centre 0.84 / 11.2; walk Queen Elizabeth Park 1.21 / 16.8; drive Eric Hamber Secondary 1.51 / 3.1
- NOT CONFIRMED: SD39 catchments (no locator run); bus frequencies; no second grocery anchor within ~1 km confirmed
- Roster note carried: OPAL is also presented as counted in the south-cambie file; counted once here, in the cambie file's verified roster

### 155. West 41 Oakridge — 655 West 41st Avenue and 677 West 41st Avenue (cambie; condos) — MULTI-ADDRESS
- File: west-41-oakridge--cambie-nearby-2026-11-02.md — 3,185 B; 424 words — OVER cap (disclosed)
- Title/anchor use the FIRST address (655 West 41st Avenue); header carries both addresses exactly as roster states; anchor choice disclosed in NOT CONFIRMED
- Origin: West 41st Avenue segment point — no OSM house point exists for 655 W 41st Ave, so times are approximate (disclosed in-file)
- Measurements (6): walk Oakridge–41st Avenue Station 0.41 km / 5.5 min; walk Oakridge Park (650 W 41st) 0.54 / 7.3; drive Van Horne Elementary 1.24 / 2.7; drive Osler Elementary 1.53 / 3.4; drive Hillcrest Centre 2.41 / 4.6; drive Churchill Secondary 2.70 / 5.0
- NOT CONFIRMED: anchor choice; SD39 catchments; frequencies; R4 timetable not read; no municipal park within ~1 km confirmed (QE Park/Hillcrest used, scope disclosed)

### 157. Balmoral House — 960 Lynn Valley Rd (canyon-springs; 55-plus)
- File: balmoral-house--canyon-springs-nearby-2026-11-02.md — 3,345 B; 445 words — OVER cap (disclosed)
- Origin: exact OSM house point for 960 Lynn Valley Rd
- Measurements (6): walk Karen Magnussen Community Recreation Centre (2300 Kirkstone Rd, NVRC-verified) 0.27 km / 3.7 min; walk Kirkstone Park 0.51 / 6.8; walk Lynn Valley Centre 0.77 / 10.2; walk Lynn Valley Library (1277 Lynn Valley Rd) 0.90 / 12.0; drive Lynn Valley Elementary 1.51 / 2.6; drive Argyle Secondary 2.07 / 4.0
- NOT CONFIRMED: slug mismatch — the phase-1 canyon-springs file is Coquitlam ground and was NOT used as this building's anchor map (the building is Lynn Valley, North Vancouver, per the 55-plus home file); researched fresh and noted in-file; SD44 catchments; frequencies; Molly Nye House street address (operator page fetch failed); nearest individual bus stop. Routes cited from TransLink timetables only: 228, 229, 210/209; Phibbs Exchange as named on the 210 timetable. Save-On-Foods Lynn Valley address (2770 Valley Centre Ave) rests on the retailer's own-domain search-result fallback, disclosed in-file. No age-restriction claims in the body

### 158. The Jefferson — 2960 Princess Crescent (canyon-springs; condos)
- File: the-jefferson--canyon-springs-nearby-2026-11-02.md — 3,344 B; 408 words — marginally OVER cap (disclosed)
- Origin: exact OSM building point for 2960 Princess Crescent. Geocode discrepancy disclosed in-file: the first Nominatim query form returned no result; the fuller province form returned the building point, which governs
- Measurements (9): walk Walton Elementary 0.37 km / 3.7 min (walk speed computes to exactly 6.0 km/h — top edge of the 4–6 sanity band, kept and flagged); walk City Centre Aquatic Complex 0.41 / 5.5; walk Lafarge Lake–Douglas Station 0.55 / 7.3; drive Pinetree Secondary 0.93 / 3.3; walk Glen Elementary 1.06 / 14.1; walk Town Centre Park 1.13 / 14.3; drive Coquitlam Centre 1.28 / 3.7; walk Glen Park 1.28 / 17.1; drive Save-On-Foods Pinetree Village 1.51 / 3.0
- NOT CONFIRMED: SD43 catchments incl. the middle tier (no locator run); bus frequencies

### 159. Kirkstone Gardens — 2020 Cedar Village Cres (canyon-springs; 55-plus)
- File: kirkstone-gardens--canyon-springs-nearby-2026-11-02.md — 3,638 B; 489 words — OVER cap (disclosed; the building has no anchors within ~1 km, so every section carries scope disclosures plus 12 cited URLs)
- Origin: exact OSM house point for 2020 Cedar Village Cres
- Measurements (5, all drive): drive École Ross Road Elementary (2875 Bushnell Place per the BC Ministry SD44 list) 1.62 km / 4.2 min; drive Argyle Secondary 1.82 / 4.7; drive Lynn Valley Elementary 1.83 / 3.9; drive Lynn Valley Centre 2.02 / 4.4; drive Karen Magnussen CRC 2.74 / 5.4. Walk to Ross Road Elementary measured 2.84 km — over the 1.5 km walk cap, excluded and stated in-file
- NOT CONFIRMED: slug mismatch (same as Balmoral House — phase-1 canyon-springs file is Coquitlam ground, not used as anchor map); SD44 catchments; frequencies; no park/recreation/grocery anchor within ~1 km confirmed (nearest confirmed used, scope disclosed); nearest individual bus stop. No age-restriction claims in the body

### 160. The Madison — 2990 Princess Crescent (canyon-springs; condos)
- File: the-madison--canyon-springs-nearby-2026-11-02.md — 2,701 B; 315 words — within cap
- Origin: exact building point (Nominatim named point "The Madison, 2990 Princess Crescent")
- Measurements (4): walk City Centre Aquatic Complex 0.18 km / 2.4 min; walk Glen Elementary 0.82 / 11.0; walk Coquitlam Centre 1.02 / 13.6; drive Coquitlam Central Station 1.74 / 3.5
- NOT CONFIRMED: school catchments (no locator run); bus frequencies not stated; Town Centre Park travel time not measured

### 161. The Montclaire — 2970 Princess Crescent (canyon-springs; condos)
- File: the-montclaire--canyon-springs-nearby-2026-11-02.md — 2,644 B; 305 words — within cap
- Origin: exact building point ("Montclaire, 2970 Princess Crescent")
- Measurements (3): walk City Centre Aquatic Complex 0.28 km / 3.8 min; walk Coquitlam Centre 0.99 / 13.2; drive Coquitlam Central Station 1.88 / 4.0
- NOT CONFIRMED: school catchments; bus frequencies; Town Centre Park travel time not measured

### 162. Canyon Park — 2832 Capilano Road (capilano-nv; condos)
- File: canyon-park--capilano-nv-nearby-2026-11-02.md — 3,261 B; 411 words — OVER cap (disclosed)
- Origin: segment/address point, disclosed in-file — Nominatim holds no named building point for 2832 Capilano Road; it returned a Capilano Road address point, and all measurements start there
- Measurements (4): walk Murdo Frazer Park (Paisley Road point) 0.65 km / 8.6 min; drive Thrifty Foods Edgemont Market 1.01 / 1.9; walk Capilano Library 1.27 / 17.0; drive Lonsdale Quay 5.53 / 8.9
- NOT CONFIRMED: origin-point substitution (above); school catchments + no school confirmed within the 1 km radius (nearest Ministry-listed schools named instead); bus frequencies; Murdo Frazer Park civic address not read on a District page (park's District status cited to a DNV council report; measurement used the Paisley Road point). Thrifty address rests on a thriftyfoods.com own-domain search result (store page fetch returned 403), disclosed in-file

### 163. Highland House — 3088 Highland Blvd (capilano-nv; 55-plus)
- File: highland-house--capilano-nv-nearby-2026-11-02.md — 3,038 B; 380 words — within cap
- Origin: exact building point ("Highland House, 3088 Highland Boulevard")
- Measurements (4): walk Capilano Library 0.14 km / 1.9 min; walk Thrifty Foods Edgemont Market 0.21 / 2.8; walk Highlands Elementary 0.57 / 7.6; walk Murdo Frazer Park (Paisley Road point) 1.30 / 17.3
- NOT CONFIRMED: **the building's 55-plus status rests on a single realtor guide per the program home file — carried in NOT CONFIRMED as instructed; no age-restriction claim anywhere in the body**; school catchments; bus frequencies; Murdo Frazer civic address (same Paisley Road point note). Thrifty address via own-domain search-result fallback, disclosed in-file

### 164. Altezza — 4710 Hastings Street (capitol-hill-bn; condos)
- File: altezza--capitol-hill-bn-nearby-2026-11-02.md — 2,818 B; 338 words — within cap
- Origin: exact building point ("Altezza, 4710 Hastings Street")
- Measurements (4): walk Justin's NOFRILLS 0.06 km / 0.8 min; walk Confederation Park Elementary 0.42 / 5.9; walk McGill Library 0.46 / 6.1; walk Safeway (Burnaby Heights) 0.56 / 7.5
- NOT CONFIRMED: school catchments; bus frequencies; Confederation Park travel time not measured — the Nominatim point for 250 Willingdon Ave fell on a Willingdon Ave segment well south of the park and was discarded. NOFRILLS address rests on a nofrills.ca own-domain search result (store page fetch returned no address text), disclosed in-file; Safeway 4440 Hastings was read directly on safeway.ca

### 165. Alto on Capitol Hill — 5535 Hastings Street (capitol-hill-bn; condos)
- File: alto-on-capitol-hill--capitol-hill-bn-nearby-2026-11-02.md — 2,738 B; 349 words — within cap
- Origin: Nominatim named house point for Alto on Capitol Hill. Geocode discrepancy disclosed in-file: a plain-address geocode returned a point ~1.1 km east; the postal-code re-run returned the named house point used, and the re-run governs
- Measurements (3, all walk): walk Capitol Hill Elementary 0.40 km / 5.3 min; walk Kensington Park 0.63 / 9.1; walk Burnaby North Secondary 1.05 / 14.0 — **school walks are the CORRECTED values** (re-measured to the named school points returned by the completed re-run; first-pass values superseded, disclosure in NOT CONFIRMED)
- NOT CONFIRMED: school catchments; bus frequencies; Safeway Kensington Square travel time not measured; the two geocode discrepancies above

### 166. Beta — 4721 Hastings Street (capitol-hill-bn; condos)
- File: beta--capitol-hill-bn-nearby-2026-11-02.md — 2,827 B; 343 words — within cap
- Origin: as geocoded in the foreground pass (see file)
- Measurements (3, all walk): walk Confederation Park Elementary 0.44 km / 6.2 min; walk McGill Library 0.48 / 6.3; walk Safeway, Burnaby Heights 0.62 / 8.3
- NOT CONFIRMED: school catchments; bus frequencies (per worker report; full list in the file)

### 167. Capitol Hill (building-directory name) — 388 Ellesmere Avenue (capitol-hill-bn; townhomes)
- File: capitol-hill--capitol-hill-bn-nearby-2026-11-02.md — 2,799 B; 353 words — within cap
- Origin: 388 Ellesmere segment point (confirmed identical by the completed geocode run)
- Measurements (2, all walk): walk Capitol Hill Elementary 0.38 km / 5.0 min; walk Burnaby North Secondary 1.01 / 13.5 — **CORRECTED values** (re-measured to the named school points; first-pass values superseded, disclosure in NOT CONFIRMED)
- NOT CONFIRMED: school catchments; bus frequencies; the school-anchor discrepancy (per worker report; full list in the file)

### 168. Cassia (Guildford Brook Estates) — 6965 Hastings Street (capitol-hill-bn; townhomes)
- File: cassia--capitol-hill-bn-nearby-2026-11-02.md — 2,493 B; 319 words — within cap
- Origin: postal-code segment point. Disclosure corrected in-file: plain-address geocode for 6965 Hastings returned different segments across runs (one near Willingdon, ~3.4 km west) — plain-address interpolation for this address is unstable in both directions; the postal-code segment point used is unchanged
- Measurements (3, all walk): walk Westridge Elementary 0.24 km / 3.2 min; walk Westridge Park 0.28 / 3.7; walk Safeway, Kensington Square 0.49 / 6.5
- NOT CONFIRMED: the geocode instability above; school catchments; bus frequencies (per worker report; full list in the file)

### 169. Cedarwood — 5340 Hastings Street (capitol-hill-bn; condos)
- File: cedarwood--capitol-hill-bn-nearby-2026-11-02.md — 2,711 B; 341 words — within cap
- Origin: as geocoded in the foreground pass (confirmed identical by the completed geocode run)
- Measurements (3, all walk): walk Capitol Hill Elementary 0.62 km / 8.3 min; walk Kensington Park 0.80 / 11.4; walk Burnaby North Secondary 1.22 / 16.3 — **school walks are the CORRECTED values** (re-measured to the named school points; first-pass values superseded, disclosure in NOT CONFIRMED)
- NOT CONFIRMED: school catchments; bus frequencies; the school-anchor discrepancy (per worker report; full list in the file)

### 170. Centrale — 4488 Hastings Street (capitol-hill-bn; condos) — CORRECTED FILE
- File: centrale--capitol-hill-bn-nearby-2026-11-02.md — 3,025 B; 376 words — within cap
- Origin: Hastings Street segment point nearest Willingdon Avenue — Nominatim offered only segment candidates scattered along Hastings; the V5C 5G4 candidate by the Willingdon intersection named in the home file was used. **An earlier measurement set taken from a superseded point ~1.2 km west was discarded and re-measured; the foreground re-run governs (disclosed in NOT CONFIRMED; coordinator spot-checked this file in full)**
- Measurements (3): walk McGill Library 0.35 km / 4.7 min; walk Confederation Park Elementary 0.74 / 10.1; drive Confederation Park Elementary 0.91 / 1.7
- NOT CONFIRMED: presale status carried only as the home file states it (presale; boundary-flagged), no completion date confirmed; measurement-origin substitution (above); school catchments; bus frequencies other than the R2 (stated from the operator page in §1)

### 171. Hilltop Greene — 368 Ellesmere Avenue (capitol-hill-bn; townhomes) — CORRECTED FILE
- File: hilltop-greene--capitol-hill-bn-nearby-2026-11-02.md — 2,827 B; 352 words — within cap
- Origin: Ellesmere Avenue segment point at the Hastings Street end — Nominatim returned no house point for 368 Ellesmere in either foreground run; the segment point sits roughly 0.3 km north of the building (disclosed in §5 and NOT CONFIRMED). Measurements re-taken from the governed foreground point; earlier values withdrawn
- Measurements (2, all walk): walk Capitol Hill Elementary 0.38 km / 5.0 min; walk Burnaby North Secondary 1.01 / 13.5
- NOT CONFIRMED: origin-point substitution and offset (above); school catchments; bus frequencies (per worker report; full list in the file)

### 172. Saturna — 5988 Hastings Street (capitol-hill-bn; condos) — CORRECTED FILE
- File: saturna--capitol-hill-bn-nearby-2026-11-02.md — 2,624 B; 312 words — within cap
- Origin: Hastings Street segment point in the building's block (V5B 1S0 candidate). Measurements re-taken from the governed foreground point; earlier values withdrawn (the Safeway anchor point also moved ~180 m east to the named Safeway point at 6564 Hastings)
- Measurements (4, all walk): walk Safeway Kensington Square 0.39 km / 5.2 min; walk Burnaby North Secondary 0.49 / 6.8; walk Capitol Hill Elementary 0.76 / 10.2; walk Kensington Park 0.82 / 11.2
- NOT CONFIRMED: origin-point substitution (above); school catchments; bus frequencies (per worker report; full list in the file)

### 173. Barclay Woods — 9847 / 9857 / 9867 Manchester Drive (cariboo; condos) — MULTI-ADDRESS
- File: barclay-woods--cariboo-nearby-2026-11-02.md — 3,397 B; 430 words — OVER cap (disclosed, disclosure-driven)
- Title/anchor use the FIRST address (9847 Manchester Drive); header carries all three addresses exactly as roster states; anchor choice disclosed in NOT CONFIRMED
- Origin: street-segment point (as stated in the file's §5 header line)
- Measurements (3): walk Lougheed Town Centre Station 0.52 km / 7.0 min; drive Lougheed Town Centre Station 1.20 / 1.7; drive The City of Lougheed Shopping Centre 2.06 / 5.4
- NOT CONFIRMED: anchor choice; segment-point origin (per worker report; full list in the file). File stands unchanged after the batch's geocode corrections — its foreground points match the late full output exactly

### 174. Brookside Court — 9880 / 9890 Manchester Drive (cariboo; condos) — MULTI-ADDRESS
- File: brookside-court--cariboo-nearby-2026-11-02.md — 3,327 B; 419 words — OVER cap (disclosed, disclosure-driven)
- Title/anchor use the FIRST address (9880 Manchester Drive); header carries both addresses exactly as roster states; anchor choice disclosed in NOT CONFIRMED
- Origin: exact address point (as stated in the file's §5 header line)
- Measurements (3): walk Lougheed Town Centre Station 0.71 km / 9.4 min; drive Lougheed Town Centre Station 1.38 / 2.2; drive The City of Lougheed Shopping Centre 2.24 / 5.9
- NOT CONFIRMED: anchor choice (per worker report; full list in the file). File stands unchanged after the batch's geocode corrections — its foreground points match the late full output exactly

### 175. Brookside Park — 9584 Manchester Drive (cariboo; condos)
- File: brookside-park--cariboo-nearby-2026-11-02.md — 3,566 B; 483 words — OVER cap (disclosed)
- Origin: exact house point, foreground Nominatim "Brookside Park, 9584 Manchester Drive" (49.246655, −122.8988303). An earlier backgrounded Manchester Drive segment point differed; the foreground house point governs — disclosed in NOT CONFIRMED
- Measurements (6): walk Lougheed Town Centre Station 0.50 km / 6.7 min; drive station 1.16 / 1.6; walk Cameron Park 1.05 / 14.0; drive Cameron Park 1.71 / 3.0; drive City of Lougheed 2.03 / 5.3; drive Lyndhurst Elementary 2.13 / 4.3. Walk to Lyndhurst (1.78 km) routed but excluded over the 1.5 km walk cap
- NOT CONFIRMED: school catchments (no locator run); bus frequencies; Cameron Park street address; origin-point discrepancy (above); excluded Lyndhurst walk

### 176. Strathmore Lane (townhouse component) — 3379 and 3368 Morrey Court (cariboo; townhomes) — MULTI-ADDRESS
- File: strathmore-lane--cariboo-nearby-2026-11-02.md — 3,751 B; 506 words — OVER cap (disclosed)
- Title/anchor use the FIRST address (3379 Morrey Court); header carries "3379 and 3368 Morrey Court" exactly as roster states; anchor choice disclosed in NOT CONFIRMED
- Origin: Morrey Court segment point (49.253899, −122.8962979; no house-number point returned); an earlier backgrounded segment point ~90 m east differed — foreground governs, disclosed
- Measurements (7): walk Cameron Park 0.38 km / 5.1 min; drive Cameron Park 0.39 / 1.1; drive City of Lougheed 0.71 / 3.2; walk Lyndhurst Elementary 0.84 / 11.2; walk Lougheed Station 0.99 / 13.2; drive Lyndhurst 1.49 / 3.6; drive station 1.47 / 2.0
- NOT CONFIRMED: anchor choice; segment-point discrepancy; catchments; frequencies; Cameron Park street address

### 177. Strathmore Towers — 9603 / 9623 / 9633 Manchester Drive (cariboo; condos) — MULTI-ADDRESS
- File: strathmore-towers--cariboo-nearby-2026-11-02.md — 3,753 B; 509 words — OVER cap (disclosed)
- Title/anchor use the FIRST address (9603 Manchester Drive); header carries "9603 / 9623 / 9633 Manchester Drive" exactly as roster states; anchor choice disclosed in NOT CONFIRMED
- Origin: exact house-number point for 9603 Manchester Drive (49.2474687, −122.898617) — **OSM labels that point "Emerald Manor," a name differing from the roster name; the address number matches the roster anchor — disclosed in-file, roster name NOT corrected**. Earlier backgrounded segment point differed; foreground governs
- Measurements (5): walk Lougheed Station 0.42 km / 5.5 min; drive station 1.05 / 1.4; walk Cameron Park 0.96 / 12.9; drive Cameron Park 1.60 / 2.9; drive Lyndhurst Elementary 2.01 / 4.2. Walk to Lyndhurst (1.69 km) excluded over cap
- NOT CONFIRMED: anchor choice; OSM name label on origin point; catchments; frequencies; Cameron Park street address; excluded walk

### 178. Caulfeild Cove — 4957 Marine Drive (caulfeild; townhomes)
- File: caulfeild-cove--caulfeild-nearby-2026-11-02.md — 3,564 B; 491 words — OVER cap (disclosed)
- Origin: Marine Drive segment point from the foreground postal-code query (49.3455435, −123.2660637; segment postal code V7W 2R4 vs building's V7W 2P5; no house-number point returned). An earlier backgrounded segment point ~1.5 km east differed — foreground governs, disclosed in-file. Caulfeild Elementary: the address+postal query fell back to a Keith Road segment near Horseshoe Bay (wrong segment); measurements use the foreground named school point instead — disclosed in-file
- Measurements (5, all drive): drive Lighthouse Park 1.16 km / 3.3 min; drive Caulfeild Park 1.91 / 4.0; drive Caulfeild Elementary 2.56 / 4.9; drive Rockridge Secondary 2.84 / 5.1; drive Caulfeild Village Shopping Centre 2.85 / 5.0. Walks to Lighthouse Park (1.53 km), Caulfeild Elementary (1.76 km), Caulfeild Village (1.98 km) and Caulfeild Park (2.01 km) all exceeded the 1.5 km cap and were excluded
- NOT CONFIRMED: origin segment + discrepancy; elementary point fallback; catchments; frequencies; excluded walks; grocery store inside Caulfeild Village not confirmed from a retailer locator (the centre itself is listed); West Vancouver Community Centre/Library beyond radius

### 179. Alameda Court — 2277/2279 McCallum Rd (central-abbotsford; 55-plus) — MULTI-CIVIC
- File: alameda-court--central-abbotsford-nearby-2026-11-02.md — 4,510 B; 566 words — OVER cap (disclosed)
- Title/anchor use 2277 McCallum Rd; header carries "2277/2279 McCallum Rd" exactly as roster states (listings use both civic numbers, per the home file); anchor choice disclosed in NOT CONFIRMED. Header identifies the building by class only ("55-plus"); no age-restriction claims in the body
- Origin: exact house point for 2277 McCallum Road (49.0430842, −122.294248), confirmed identical on the foreground postal-code (V2S 3N7) re-run. An earlier backgrounded McCallum Road segment point near George Ferguson Way differed — foreground house point governs, disclosed. The Mill Lake Park point also differed between background and foreground runs; the foreground named park point governs, disclosed
- Measurements (6, all drive): drive Abbotsford Senior Secondary 0.89 km / 2.6 min; drive Godson Elementary 1.86 / 3.7; drive Bourquin Exchange 2.21 / 4.1; drive Mill Lake Park 2.61 / 5.4; drive Sevenoaks Shopping Centre 2.84 / 5.7; drive Clearbrook Library 3.95 / 7.6. Walks to Godson (1.60 km), Mill Lake Park (1.90 km), Bourquin (1.98 km) and Sevenoaks (2.37 km) excluded over cap. Save-On-Foods address in §4 rests on a retailer own-domain (saveonfoods.com) search result, disclosed in-file as such
- NOT CONFIRMED: anchor choice; origin + Mill Lake Park point discrepancies; catchments; frequencies; excluded walks
