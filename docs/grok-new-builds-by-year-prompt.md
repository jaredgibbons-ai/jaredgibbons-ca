# Prompt for Jerry/Grok: new builds by completion year (2026-11-04)

```
TASK
Count, then build, MyRealPage saved searches for new builds by completion year (2027, 2028, 2029) in each city. Account 67649. Same worksheet format as embed-list.xlsx. Do not publish anything.

STEP 1: CHECK THE TOOL (report before building)
1. Can a search filter on Year Built (a range or exact year)? Name the exact field. If not, say what the closest field is (new construction, under construction, completion date) and how it behaves.
2. Is Year Built on an unbuilt home the agent's estimate? Say what the tool shows.
3. Can I limit to Active only, and exclude land and income properties as in the other 18 searches? Keep houses, townhomes and condos.

STEP 2: COUNT (do this for every city before creating anything)
Cities: South Surrey/White Rock, Surrey, Langley, Abbotsford, Chilliwack, Maple Ridge, Mission, Delta (Tsawwassen, Ladner, North Delta), Coquitlam, Burnaby.
For each city, give the number of Active listings with Year Built 2026, 2027, 2028 and 2029 or later. Use one table: city by year. State the date of the counts.

STEP 3: DECIDE (by rule, not by feel)
- A year in a city gets its own search only if its count is 5 or more.
- If 2028 and 2029+ are each under 5 but together are 5 or more, build one search "2028 or later".
- If a city has fewer than 5 for 2027 or later in total, build nothing for it and list it as skipped with its count.
- Do not touch or copy the existing searches. Do not use the same address as an existing presale or new-construction page.

STEP 4: BUILD each qualifying search
- Name: "[City] 2027 New Builds for Sale" (or 2028, 2029, "2028 or Later").
- Same filters as the 18 searches built today: Active, houses, townhomes and condos, no land, no income properties.
- Suggested page address: /new-builds-2027-[city].html (for example /new-builds-2027-surrey.html). H1: "2027 New Builds for Sale in [City]".
- Test the embed on one search and say whether it rendered, on what page, and what you saw.

STEP 5: RETURN
A worksheet with the same columns as embed-list.xlsx (Search name, New search ID, Old search ID [blank], Current page address(es) [the suggested address], Full page URL(s), Type ["New page"], WordPress shortcode, Embed code, Notes). In Notes put the filter you used and the count on the date you built it. Add a second tab "Counts" with the city by year table, and a third "Skipped" listing every city and year not built with its count.

RULES
- Report only what the tool shows. If a field does not exist, say so. Do not guess.
- Never ask me for a password or key. If a login is needed, tell me and I will do it.
- Do not create accounts, change settings, or change any existing search.
- Presales are often not on the MLS. Do not add anything from developer sites. Count only what the MLS search returns.
- Keep it short. Tell me what you could not do.
```
