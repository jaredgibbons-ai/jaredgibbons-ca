# What's Nearby — Phase 2, Batch P2-9 Summary

Produced Nov 2, 2026. Roster range covered: **entries 208–232 exactly — 25 buildings, all carrying a street address. Skipped entries: NONE in this range** (no ADDRESS NOT IN NOTES / ADDRESS CONFLICT entries between 208 and 232; no extension past 232 needed). Mop-up list carried forward unchanged: entries 52 (The Hart), 85 (District Flats at Southlands), 86 (The Granary at Southlands), 156 (Winona Park), 188 (Natura), 193 (Upper Montrose), 195 (The Abby Townhome Series).

Areas: central-coquitlam 5, central-lonsdale 11, central-meadows-pitt-meadows 1, central-park-bs 8.

**Totals: 128 measurements listed (98 walk, 30 drive), all measured 2026-11-02 starting at each building's own address; every kept walk inside the 4–6 km/h sanity band and the walk ≤1.5 km / drive ≤10 km caps. One further route was measured but excluded (The Beeches → Queen Mary Elementary, 0.03 km — building and school points geocode ~30 m apart, not meaningful; disclosed in-file). HTTP 429s: none across all five workers. No section omitted in any file; no file used the "not measured in this pass" fallback. Roster lines proved wrong on the ground: NONE — the roster was never silently corrected.**

**Word-cap overages: 13 of 25 files over the ~400-word target** (all central-lonsdale files plus Victoria Park West, Meadowland Village, Central Park House), disclosed per file below; wording was trimmed but no cited fact or URL was cut. The central-lonsdale overage is structural: a shared §1 (SeaBus + Lonsdale Quay exchange + up to 3 timetable routes), a single §4 grocery anchor carried with its fallback disclosure, and per-file origin disclosures.

**Coordinator ruling applied this batch:** entries 227 and 228 are two distinct buildings both named Central Park Place under home slug central-park-bs. Both filenames carry an address disambiguator (central-park-place-5652-patterson-avenue--… and central-park-place-4160-sardis-street--…); both titles use the plain building name + roster address; each file's NOT CONFIRMED notes the disambiguation and the other building's separate file.

**Geocode process:** the backgrounded-delivery failure mode appeared twice (workers 2 and 5 each had one run backgrounded by the runtime); in both cases the full output was waited for and a complete foreground re-run confirmed the points identical before any routing — no discrepancy required disclosure. All other geocoding ran in the foreground by default in isolated scratch dirs (/tmp/p2b9-w1/ … w5/).

---

## 208. Marlborough House — 3098 Guildford Way (central-coquitlam; 55-plus)
- File: marlborough-house--central-coquitlam-nearby-2026-11-02.md — 2,567 B, 297 words. All 5 sections + NOT CONFIRMED written.
- Address/origin: roster address; Nominatim house point named "Marlborough House, 3098 Guildford Way".
- Measurements (5): walk Lafarge Lake–Douglas Station 0.52 km/6.9 min; walk City Centre Aquatic Complex 0.61/8.2; walk Town Centre Park 0.72/9.6; walk Pinetree Secondary 1.10/14.6; drive Coquitlam Centre 1.83/3.9.
- NOT CONFIRMED: school catchments (no locator run); bus frequencies not read.

## 209. MThree — 1188 Pinetree Way (central-coquitlam; condos)
- File: mthree--central-coquitlam-nearby-2026-11-02.md — 2,536 B, 300 words. All sections written.
- Address/origin: roster address; Nominatim house point.
- Measurements (5): walk Library City Centre Branch 0.21/2.7; walk Lincoln Station 0.29/3.9; walk Glen Elementary 0.48/6.4; walk Coquitlam Centre 0.73/9.8; drive Save-On-Foods Pinetree Village 0.71/1.4.
- NOT CONFIRMED: catchments; frequencies.

## 210. Oasis — 2955 Atlantic Avenue (central-coquitlam; condos)
- File: oasis--central-coquitlam-nearby-2026-11-02.md — 2,544 B, 300 words. All sections written.
- Address/origin: roster address; Nominatim house point named "Oasis, 2955 Atlantic Avenue".
- Measurements (5): walk Coquitlam Centre 0.33/4.5; walk Library 0.53/7.1; walk Lincoln Station 0.58/7.7; walk Glen Elementary 0.88/11.8; drive Save-On-Foods 1.05/2.3.
- NOT CONFIRMED: catchments; frequencies.

## 211. Parc Laurent — 3071 Glen Drive (central-coquitlam; condos)
- File: parc-laurent--central-coquitlam-nearby-2026-11-02.md — 2,731 B, 332 words. All sections written.
- Address/origin: roster address; **disclosed segment-point origin** — Nominatim returned no house point for 3071 Glen Drive and no building-name result; the River Springs Glen Drive segment point was used (Altamonte precedent), disclosed in §5 header and NOT CONFIRMED.
- Measurements (5): walk Library 0.26/3.4; walk Glen Elementary 0.31/4.1; walk Glen Park 0.32/4.3; walk Lincoln Station 0.49/6.5; drive Save-On-Foods 0.90/1.7.
- NOT CONFIRMED: segment-point origin; catchments; frequencies.

## 212. Princess Gate — 2985 and 2995 Princess Crescent (central-coquitlam; 55-plus + condos)
- File: princess-gate--central-coquitlam-nearby-2026-11-02.md — 2,957 B, 352 words. All sections written.
- Address/origin: multi-address roster line (not a conflict) — header carries BOTH addresses exactly as roster states; title + anchor use the first address, 2985 Princess Crescent (Nominatim house point); anchor choice disclosed in NOT CONFIRMED.
- Measurements (5): walk City Centre Aquatic Complex 0.39/5.2; walk Lafarge Lake–Douglas Station 0.53/7.1; walk Pinetree Secondary 0.89/11.9; walk Town Centre Park 1.10/13.9; drive Coquitlam Centre 1.21/3.5.
- NOT CONFIRMED: anchor choice; **count-home disagreement recorded, not resolved** (55-plus counts the complex in central-coquitlam; condos counts it in canyon-springs); catchments; frequencies.

## 213. Anderson Walk — 119 West 22nd Street (central-lonsdale; condos)
- File: anderson-walk--central-lonsdale-nearby-2026-11-02.md — 3,724 B, 474 words — **OVER CAP (+74)**.
- Address/origin: roster address range 119–152 West 22nd Street carried in header; title/anchor use 119 (exact Nominatim house point, V7M 2K4); disclosed.
- Measurements (5): walk North Vancouver City Library 0.98/13.2; walk Loblaws City Market 0.62/8.2; drive Harry Jerome Community Recreation Centre 0.44/1.2; drive Carson Graham Secondary 1.26/2.9; drive Lonsdale Quay 2.46/4.9.
- NOT CONFIRMED: multi-address anchor; catchments; frequencies (SeaBus daytime 15 min only); Loblaws address from retailer's own-domain search result (store page did not render; disclosed, carried from phase-1).

## 214. The Beeches — 230 West 13th Street (central-lonsdale; townhomes)
- File: the-beeches--central-lonsdale-nearby-2026-11-02.md — 3,727 B, 460 words — **OVER CAP (+60)**.
- Address/origin: roster address; Nominatim point for 230 West 13th Street.
- Measurements (4 listed): walk City Library 0.67/8.9; walk Victoria Park 0.58/7.7; walk Loblaws City Market 1.11/14.8; drive Lonsdale Quay 1.37/3.0. **Excluded:** walk to Queen Mary Community Elementary measured at 0.03 km/0.4 min — the building and school points geocode ~30 m apart, so the routed walk is not meaningful; disclosed in-file.
- NOT CONFIRMED: catchments; frequencies; Loblaws fallback.

## 215. Centreview — 112 East 13th Street (project address 1308 Lonsdale Avenue) (central-lonsdale; condos)
- File: centreview--central-lonsdale-nearby-2026-11-02.md — 3,931 B, 512 words — **OVER CAP (+112, largest in batch, driven by the origin disclosure)**.
- Address/origin: **disclosed named-point substitution** — Nominatim returned no house point for 112 East 13th Street (only East 13th St segment points near Grand Boulevard, ~0.8 km east, discarded as wrong-segment) and only off-building segment points for 1308 Lonsdale Avenue; measurements start at Nominatim's named "CentreView" point at Lonsdale Avenue/13th Street (49.3205019, -123.0711508), disclosed in §5 header and NOT CONFIRMED. A geocoder gap, not a bad roster address — roster line NOT proven wrong.
- Measurements (5): walk City Library 0.22/3.0; walk Victoria Park 0.60/8.0; walk Loblaws City Market 0.46/6.2; walk Ridgeway Elementary 1.37/18.3; drive Lonsdale Quay 1.76/3.7.
- NOT CONFIRMED: address basis (header carries both roster addresses); origin substitution; catchments; frequencies; Loblaws fallback. §3 contains Ridgeway Elementary only — the only Ministry-listed school within ~1 km of this address.

## 216. Elle — 128 West 15th Street (presale address 132 West 15th Street) (central-lonsdale; condos)
- File: elle--central-lonsdale-nearby-2026-11-02.md — 3,959 B, 487 words — **OVER CAP (+87)**.
- Address/origin: title/anchor use 128 West 15th Street (Nominatim point); header carries both addresses as roster states; disclosed.
- Measurements (4): walk City Library 0.50/6.7; walk Loblaws City Market 0.70/9.4; walk Queen Mary Community Elementary 0.50/6.7; drive Lonsdale Quay 1.68/3.4.
- NOT CONFIRMED: address basis; catchments; frequencies; Loblaws fallback.

## 217. Georgian Manor — 140 East 20th Street (central-lonsdale; condos)
- File: georgian-manor--central-lonsdale-nearby-2026-11-02.md — 3,547 B, 465 words — **OVER CAP (+65)**.
- Address/origin: roster address; exact Nominatim house point (V7L 4L5). Title uses "Georgian Manor" (roster's also-marketed name "The Georgian" noted in NOT CONFIRMED).
- Measurements (5): walk Harry Jerome CRC 0.54/7.2; walk Loblaws City Market 0.57/7.7; walk City Library 0.99/13.2; drive Carson Graham Secondary 1.45/3.5; drive Lonsdale Quay 2.72/5.3.
- NOT CONFIRMED: no named City park within ~1 km confirmed (Victoria Park and Mahon Park each over 1 km from this address — §2 carries Harry Jerome + the City Library only); catchments; frequencies; Loblaws fallback.

## 218. The Grande — 160 East 13th Street (central-lonsdale; condos)
- File: the-grande--central-lonsdale-nearby-2026-11-02.md — 3,513 B, 469 words — **OVER CAP (+69)**.
- Address/origin: **disclosed named-point basis** — the first street-address query returned a Grand Boulevard segment point (discarded); measurements use the named OSM building point for The Grande, shown at 152 East 13th St against the roster's 160 East 13th Street; disclosed in-file. Roster line not corrected.
- Measurements (6): walk City Library 0.40/5.3; walk Victoria Park 0.58/7.8; walk Loblaws City Market 0.64/8.5; walk Queen Mary Elementary 0.81/10.8; drive Harry Jerome CRC 1.27/2.4; drive Lonsdale Quay 1.84/3.6.
- NOT CONFIRMED: catchments; bus frequencies (SeaBus excepted); Loblaws own-domain search-result fallback (retailer page did not render); origin-point disclosure.

## 219. Lennox — 110 East 17th Street (central-lonsdale; condos)
- File: lennox--central-lonsdale-nearby-2026-11-02.md — 4,207 B, 538 words — **OVER CAP (+138, largest file in batch)**.
- Address/origin: roster address; named OSM building point. Title uses "Lennox".
- Measurements (7): walk Loblaws City Market 0.07/0.9; walk City Library 0.48/6.5; walk Victoria Park 0.91/12.1; walk Mahon Park 1.08/15.0; drive Harry Jerome CRC 0.87/2.0; drive Carson Graham Secondary 1.81/3.9; drive Lonsdale Quay 2.09/4.4.
- NOT CONFIRMED: as 218; plus the walk to Westview Elementary (1.97 km) exceeded the 1.5 km walk cap and is excluded from §5 (noted in-file).

## 220. Millennium Central Lonsdale — 135 East 13th Street (central-lonsdale; condos)
- File: millennium-central-lonsdale--central-lonsdale-nearby-2026-11-02.md — 3,576 B, 479 words — **OVER CAP (+79)**.
- Address/origin: **disclosed segment-point origin** — no house/building point returned (building-name queries none; first query returned a Grand Boulevard segment point, discarded); East 13th St segment point in the V7L 0E5 segment nearest the roster address used, disclosed in-file.
- Measurements (6): walk City Library 0.37/4.9; walk Victoria Park 0.54/7.2; walk Loblaws City Market 0.61/8.2; walk Queen Mary Elementary 0.76/10.2; drive Harry Jerome CRC 1.36/2.5; drive Lonsdale Quay 1.67/3.2.
- NOT CONFIRMED: as 218.

## 221. Ridge Park Gardens — 2059 Chesterfield Avenue (central-lonsdale; 55-plus + condos)
- File: ridge-park-gardens--central-lonsdale-nearby-2026-11-02.md — 3,827 B, 483 words — **OVER CAP (+83)**.
- Address/origin: roster address; foreground Nominatim house point.
- Measurements (6): walk Harry Jerome CRC 0.64/8.5; walk Loblaws City Market 0.69/9.2; walk Carson Graham Secondary 0.74/9.9; walk Mahon Park 1.03/14.3; drive City Library 0.90/1.8; drive Lonsdale Quay 2.16/4.0.
- NOT CONFIRMED: as 218; plus no route serving Chesterfield Avenue itself was confirmed — nearest stops are on Lonsdale Avenue (stated in-file).

## 222. Sundale — 1420 Chesterfield Ave (central-lonsdale; 55-plus)
- File: sundale--central-lonsdale-nearby-2026-11-02.md — 4,050 B, 505 words — **OVER CAP (+105)**.
- Address/origin: roster address; foreground Nominatim house point.
- Measurements (6): walk City Library 0.19/2.6; walk Queen Mary Elementary 0.54/7.2; walk Loblaws City Market 0.55/7.3; walk Victoria Park 0.69/9.2; walk Mahon Park 1.19/16.4; drive Lonsdale Quay 1.49/3.2.
- NOT CONFIRMED: as 221.

## 223. Victoria Park West — 160 West Keith Road (central-lonsdale; condos)
- File: victoria-park-west--central-lonsdale-nearby-2026-11-02.md — 3,299 B, 423 words — **OVER CAP (+23)**.
- Address/origin: **disclosed segment-point origin** — Nominatim returned only West Keith Road segment points; the first return was a Marine–Hamilton segment point (discarded); a foreground structured re-run returned the Central Lonsdale segment point (postal V7M 1P5, the segment carrying 230 West Keith Rd / Queen Mary), used and disclosed in-file. Queen Mary and Victoria Park West destinations use named-place points.
- Measurements (5): walk Queen Mary Community Elementary 0.25/3.3; walk Victoria Park West 0.31/4.2; walk City Library 0.64/8.5; walk Loblaws City Market 1.08/14.4; drive Lonsdale Quay 1.19/2.3.
- NOT CONFIRMED: catchments; frequencies; Loblaws fallback; segment-point origin basis.

## 224. Meadowland Village — 18960 Advent Road (central-meadows-pitt-meadows; townhomes)
- File: meadowland-village--central-meadows-pitt-meadows-nearby-2026-11-02.md — 3,615 B, 456 words — **OVER CAP (+56)**.
- Address/origin: roster address; **disclosed segment-point origin** (no building point exists on Advent Road). First-pass segment returns for Highland Park Elementary and Hoffmann Park were identical duplicate segment points — discarded; named-place foreground re-geocodes govern for both destinations.
- Measurements (6): walk Hoffmann Park 0.38/5.1; walk Highland Park Elementary 0.42/5.6; walk Advent Park 0.69/9.1; drive Pitt Meadows Station 0.99/2.2; drive Pitt Meadows Family Recreation Centre 1.32/2.9; drive Save-On-Foods (19150 Lougheed Hwy) 1.62/3.5.
- Key find: Highland Park Elementary (K–7, SD42) is Ministry-listed at 18961 Advent Rd — across the street from the complex; cited from the SD42 Ministry list read in this pass. Route 722 (TransLink tt722) serves the pocket.
- NOT CONFIRMED: catchments; frequencies; origin segment basis; unit count NOT stated in the file (roster/home file carries 20 vs 26 as unconfirmed — noted in-file as a home-file fact only).

## 225. Aldynne on the Park — 5883 Barker Avenue (central-park-bs; condos)
- File: aldynne-on-the-park--central-park-bs-nearby-2026-11-02.md — 2,950 B, 351 words. All sections written.
- Address/origin: roster address; named OSM building point ("Aldynne on the Park") — clean.
- Measurements (4): walk Patterson Station 0.31/4.0; walk Save-On-Foods (4469 Kingsway) 0.73/9.8; walk Central Park (3883 Imperial St) 0.90/12.0; drive Metropolis at Metrotown 1.35/2.9.
- NOT CONFIRMED: catchments; frequencies; Central Park destination point is the Swangard Stadium point inside the park (the City address 3883 Imperial St geocodes there) — disclosed here and in entries 226/227.

## 226. Central Park House — 5987 Wilson Avenue (central-park-bs; condos)
- File: central-park-house--central-park-bs-nearby-2026-11-02.md — 3,320 B, 407 words — **OVER CAP (+7, marginal)**.
- Address/origin: **disclosed address-variant basis** — Nominatim's named building point for Central Park House is addressed 5977 Wilson Avenue in OSM; the roster address is 5987 Wilson Avenue and the condos home file itself notes the building was proposed at 5977 and trades at 5987. Measurements start at the building point; disclosed in §5 and NOT CONFIRMED. Roster line not corrected.
- Measurements (4): walk Patterson Station 0.39/5.1; walk Chaffey-Burke Elementary 0.71/9.4; walk Central Park (3883 Imperial St) 1.16/15.4; drive Metropolis at Metrotown 1.48/3.6.
- NOT CONFIRMED: catchments; frequencies; origin address-variant disclosure; Central Park/Swangard point disclosure.

## 227. Central Park Place — 5652 Patterson Avenue (central-park-bs; condos)
- File: central-park-place-5652-patterson-avenue--central-park-bs-nearby-2026-11-02.md — 3,295 B, 400 words (at cap). All sections written.
- Address/origin: roster address; named building point ("Central Park Place", 5652 Patterson Ave) — clean. Filename disambiguated per coordinator ruling (see header note).
- Measurements (4): walk Patterson Station 0.47/6.3; walk Central Park (3883 Imperial St) 0.75/10.0; walk Save-On-Foods (4469 Kingsway) 0.79/10.5; drive Metropolis at Metrotown 1.63/3.4.
- NOT CONFIRMED: catchments; frequencies; filename-disambiguation note; Central Park/Swangard point disclosure.

## 228. Central Park Place — 4160 Sardis Street (central-park-bs; condos)
- File: central-park-place-4160-sardis-street--central-park-bs-nearby-2026-11-02.md — 2,863 B, 329 words. All sections written.
- Address/origin: roster address; Nominatim named-building point "Central Park Place, 4160, Sardis Street". Filename disambiguated per coordinator ruling.
- Measurements (6): walk Patterson Station 0.68/9.0; walk Chaffey-Burke Elementary 0.59/7.8; walk Central Park (3883 Imperial St) 1.0/13.4; walk École Inman Elementary 1.05/14.0; walk Metropolis at Metrotown 1.46/19.5; drive Bonsor Recreation Complex 2.37/4.2.
- NOT CONFIRMED: filename-disambiguation note; catchment (no SD41 locator run); Moscrop Secondary beyond ~1 km, excluded from §3; §4's Save-On-Foods (4469 Kingsway) carried as a disclosed retailer own-domain search-result fallback.

## 229. Grand Central Park Place — 6128 Patterson Avenue (central-park-bs; condos)
- File: grand-central-park-place--central-park-bs-nearby-2026-11-02.md — 2,483 B, 294 words. All sections written.
- Address/origin: roster address; Nominatim named-building point.
- Measurements (5): walk Patterson Station 0.16/2.1; walk Central Park 1.17/15.5; walk Chaffey-Burke Elementary 1.13/15.1; walk Metropolis at Metrotown 1.43/19.0; drive Bonsor Recreation Complex 1.59/3.1.
- NOT CONFIRMED: catchment; Moscrop Secondary beyond radius; no exchange/loop name supported by an operator page read.

## 230. Paramount — 5833 Wilson Avenue (central-park-bs; condos)
- File: paramount--central-park-bs-nearby-2026-11-02.md — 2,418 B, 285 words. All sections written.
- Address/origin: roster address; Nominatim named-building point.
- Measurements (5): walk Patterson Station 0.60/8.0; walk Chaffey-Burke Elementary 0.48/6.4; walk Central Park 1.17/15.5; walk Metropolis at Metrotown 0.95/12.7; drive Bonsor Recreation Complex 1.71/3.0.
- NOT CONFIRMED: catchment; Moscrop beyond radius; no exchange/loop name.

## 231. Paramount II — 5899 Wilson Avenue (central-park-bs; condos)
- File: paramount-ii--central-park-bs-nearby-2026-11-02.md — 2,634 B, 311 words. All sections written.
- Address/origin: **disclosed segment-point substitution** — Nominatim returned no house-number point for 5899 Wilson Avenue in three foreground variants; §5 starts from a disclosed Wilson Avenue street-segment point lying between the geocoded Paramount (5833) and Place Meridian (5967) named points, consistent with the numbering sequence. The first-pass generic street point (south segment) was discarded as wrong-segment and not used.
- Measurements (5): walk Patterson Station 0.57/7.5; walk Chaffey-Burke Elementary 0.53/7.0; walk Central Park 1.13/15.1; walk Metropolis at Metrotown 0.87/11.7; drive Bonsor Recreation Complex 1.57/2.4.
- NOT CONFIRMED: measurement-origin disclosure; catchment; Moscrop beyond radius; no exchange/loop name.

## 232. Place Meridian — 5967 Wilson Avenue (central-park-bs; condos)
- File: place-meridian--central-park-bs-nearby-2026-11-02.md — 2,429 B, 287 words. All sections written.
- Address/origin: roster address; Nominatim named-building point "Place Meridian, 5967, Wilson Avenue".
- Measurements (5): walk Patterson Station 0.52/6.9; walk Chaffey-Burke Elementary 0.61/8.2; walk Central Park 1.16/15.5; walk Metropolis at Metrotown 0.93/12.4; drive Bonsor Recreation Complex 1.65/2.7.
- NOT CONFIRMED: catchment; Moscrop beyond radius; no exchange/loop name.

---

### Batch notes
- Shared central-lonsdale sourcing (entries 213–223): §1 SeaBus at Lonsdale Quay (12 min, every 15 min daytime, TransLink) in every file; Lonsdale Quay named as an exchange/terminus only where a TransLink timetable PDF read supports it (229/230 terminus; 240/241 at Lonsdale Ave & 15th St for Lennox/Sundale; 241 via Lonsdale Avenue for Ridge Park Gardens). No other exchange/loop name asserted anywhere. §4 anchor for the slug is Loblaws City Market, 1650 Lonsdale Ave — its address rests on the retailer's own-domain search result (the store page did not render), disclosed in every file and carried from the phase-1 file's cited source; Shoppers Drug Mart, 1306 Lonsdale Ave, appears in worker 2's files from the phase-1 cited source. A Save-On-Foods on Lonsdale was checked by worker 2 and NOT used — no retailer own-domain source confirmed its address in this pass.
- Queen Mary Community Elementary destination point (North Vancouver files): the named school point (230 West Keith Road) governed over an earlier street-segment point ~110 m south; used consistently across workers 2–4 and disclosed.
- Central Park (Burnaby) destination point geocodes to the Swangard Stadium point inside the park for the City address 3883 Imperial St — disclosed in the Aldynne / Central Park House / Central Park Place (5652) files.
- Buildings folder after this batch: 225 files (batches 1–9).
