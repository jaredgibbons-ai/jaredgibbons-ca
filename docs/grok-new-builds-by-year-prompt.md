# Prompt for Jerry/Grok: new builds, one search per area (2026-11-04, v2)

Attach: `docs/idx-page-inventory.csv`, `src/data/snapstats/_mapping.json`, the last embed-list.xlsx.

```
TASK
Count, then build, MyRealPage saved searches for NEW BUILDS (Year Built 2027 or later) for each area we cover. One search per area, not one per year. Account 67649. Same worksheet format as embed-list.xlsx. Do not publish anything.

AREAS
Use the attached idx-page-inventory.csv (page slugs) and _mapping.json (our area names against the board's names). Start with every city: South Surrey, White Rock, Surrey, Cloverdale, Langley, Abbotsford, Mission, Chilliwack, Maple Ridge, Pitt Meadows, Delta (Tsawwassen, Ladner, North Delta), Coquitlam, Port Coquitlam, Port Moody, Burnaby, New Westminster, Richmond, Vancouver, and the rest of the attached list. Then neighbourhoods and sub-areas, but only inside a city that passes the count. Where my name and the board's name differ, use the board's value and tell me.

EXISTING PRESALE PAGES (use these first)
These pages already exist and need a search: abbotsford-presale-condos-and-townhomes, burnaby-presale-condos-and-townhomes, coquitlam-presale-condos-and-townhomes, new-construction-presales-in-langley-bc, presale-projects-fraser-valley-and-metro-vancouver, south-surrey-presale-condos, surrey-presale-condos-and-townhomes, vancouver-presale-condos-and-townhomes. south-surrey-new-construction-presales already has one. For a city that has an existing presale page, put the new search on that page's address. Do not create a second address for the same city.

STEP 1: CHECK THE TOOL (report before building)
1. Can a search filter on Year Built (a range, or "from 2027")? Name the exact field. If not, name the closest (new construction, under construction, completion date) and say how it behaves.
2. On an unbuilt home, is Year Built the agent's estimate? Say what the tool shows.
3. Can I limit to Active only and exclude land and income properties, as in the 18 searches built on Nov 4? Keep houses, townhomes and condos.
4. Can results be sorted by Year Built, earliest first?

STEP 2: COUNT
Two passes to save work.
Pass 1, by city: Active listings with Year Built 2027 or later. Also give the split by year (2027, 2028, 2029 or later) so I can see where a second search is worth it.
Pass 2, by neighbourhood and sub-area: only inside a city whose count is 5 or more (a sub-area can never exceed its city).
Return the counts as tables with the date of the counts.

STEP 3: DECIDE BY RULE
- An area gets a search only if its count of Year Built 2027 or later is 5 or more.
- A neighbourhood or sub-area gets its own search only if its own count is 5 or more AND it already has a page in idx-page-inventory.csv.
- If a city has 40 or more listings for 2027 or later, also build a second search "2028 or Later" for that city. Otherwise do not split by year.
- Anything under 5 is skipped: list it with its count. It will be covered on its city page.
- Do not change or copy existing searches. Do not reuse an address that already exists, except the existing presale pages above, which are the intended home for their city's search.

STEP 4: BUILD each qualifying search
- Name: "[Area] New Builds for Sale" (second search: "[Area] 2028 or Later New Builds for Sale").
- Filters as the 18 searches built on Nov 4: Active, houses, townhomes and condos, no land, no income properties, Year Built 2027 or later, sorted by Year Built earliest first if the tool allows.
- Page address: the existing presale page for that city if there is one. Otherwise suggest /new-builds-[area-slug].html using the slug from idx-page-inventory.csv without "-guide" (example /new-builds-fleetwood.html). H1: "New Builds for Sale in [Area]".
- Test the embed on one search and say whether it rendered, on what page, and what you saw.

STEP 5: RETURN
A worksheet with the same columns as embed-list.xlsx: Search name, New search ID, Old search ID (blank), Current page address(es), Full page URL(s), Type ("Existing page" for presale pages, "New page" otherwise), WordPress shortcode, Embed code, Notes. In Notes put the filter and the count on the date you built it. Add tabs "Counts" (city by year, then sub-areas) and "Skipped" (every area not built, with its count).

RULES
- Report only what the tool shows. If a field does not exist, say so. Do not guess.
- Never ask me for a password or key. If a login is needed, tell me and I will do it.
- Do not create accounts, change settings, or change any existing search.
- Presales are often not on the MLS. Count only what the MLS search returns, not developer sites.
- Keep it short. Tell me what you could not do.
```
