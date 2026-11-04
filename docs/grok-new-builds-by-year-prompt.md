# Prompt for Jerry/Grok: new builds by completion year, every area (2026-11-04)

Attach: `docs/idx-page-inventory.csv`, `src/data/snapstats/_mapping.json`, the last embed-list.xlsx.

```
TASK
Count, then build, MyRealPage saved searches for new builds by completion year (2027, 2028, 2029) for EVERY area: each city and each neighbourhood or sub-area we cover. Account 67649. Same worksheet format as embed-list.xlsx. Do not publish anything.

AREAS
Use the attached idx-page-inventory.csv (page slugs) and _mapping.json (our area names against the board's names). Cover every city, every neighbourhood and every sub-area in them: South Surrey, White Rock, Surrey, Cloverdale, Langley, Abbotsford, Mission, Chilliwack, Maple Ridge, Pitt Meadows, Delta (Tsawwassen, Ladner, North Delta), Coquitlam, Port Coquitlam, Port Moody, Burnaby, New Westminster, Richmond, and the rest of the attached list. Where my name and the board's name differ, use the board's value and tell me.

STEP 1: CHECK THE TOOL (report before building)
1. Can a search filter on Year Built (a range or exact year)? Name the exact field. If not, name the closest (new construction, under construction, completion date) and say how it behaves.
2. On an unbuilt home, is Year Built the agent's estimate? Say what the tool shows.
3. Can I limit to Active only and exclude land and income properties, as in the 18 searches built on Nov 4? Keep houses, townhomes and condos.

STEP 2: COUNT
Do it in two passes to save work.
Pass 1, by city: Active listings with Year Built 2026, 2027, 2028 and 2029 or later.
Pass 2, by neighbourhood and sub-area: only for a city and year where the city count is 5 or more (a sub-area can never exceed its city).
Return the counts as tables (area by year) with the date of the counts.

STEP 3: DECIDE BY RULE
- An area and year gets its own search only if its count is 5 or more. 2027, 2028 and 2029 are each their own search.
- If 2028 and 2029 are each under 5 in an area but together 5 or more, build one search "2028 or Later" for that area.
- If an area has under 5 for 2027 or later in total, build nothing for it and list it as skipped with its count. We will cover it on its city page.
- Do not change or copy existing searches. Do not reuse an address that already exists (check against idx-page-inventory.csv) or any existing presale or new-construction page.

STEP 4: BUILD each qualifying search
- Name: "[Area] 2027 New Builds for Sale" (or 2028, 2029, "2028 or Later").
- Filters as the 18 searches built on Nov 4: Active, houses, townhomes and condos, no land, no income properties.
- Suggested address: /new-builds-2027-[area-slug].html using the slug from idx-page-inventory.csv without "-guide" (example /new-builds-2027-surrey.html, /new-builds-2028-fleetwood.html). H1: "2027 New Builds for Sale in [Area]".
- Test the embed on one search and say whether it rendered, on what page, and what you saw.

STEP 5: RETURN
A worksheet with the same columns as embed-list.xlsx: Search name, New search ID, Old search ID (blank), Current page address(es) (the suggested address), Full page URL(s), Type ("New page"), WordPress shortcode, Embed code, Notes. In Notes put the filter and the count on the date you built it. Add tabs "Counts" (area by year, city level first) and "Skipped" (every area and year not built, with its count).

RULES
- Report only what the tool shows. If a field does not exist, say so. Do not guess.
- Never ask me for a password or key. If a login is needed, tell me and I will do it.
- Do not create accounts, change settings, or change any existing search.
- Presales are often not on the MLS. Count only what the MLS search returns, not developer sites.
- Keep it short. Tell me what you could not do.
```
