# Muse prompt (Nov 3, 2026)

Attach: `muse-input-areas-2026-11-03.csv` and `muse-keyword-rows-without-a-page-2026-11-01.csv`.

---

You are researching for jaredgibbons.ca (Jared Gibbons, REALTOR®, South Surrey, White Rock, Langley, Fraser Valley and Metro Vancouver). I attached two CSVs: `muse-input-areas-2026-11-03.csv` (219 areas: area, city, our page slug, and for 34 rows a claim to check) and `muse-keyword-rows-without-a-page-2026-11-01.csv` (60 keywords we have no page for yet). Work in batches of 25 areas and give me each output as a CSV I can paste into a spreadsheet. Return FOUR files:

1. **coordinates.csv**: `area, city, page, lat, lon, source_url, point_is`. One point for each area: the neighbourhood centre, or the municipality's point if the area has no official centre. Five decimals. The point must fall inside the named city. Source must be OpenStreetMap, Wikipedia or a municipal page. `point_is` says what the point marks (for example "OSM place node", "municipal hall").
2. **questions.csv**: `area, page, question, keyword, monthly_volume, intent`. For each area, 10 questions people actually search, from People Also Ask, autocomplete and related searches for "<area> homes for sale", "<area> real estate" and "<area> condos/townhomes" where the page is a condo page. Include the ones that name a street, complex, school, park or landmark. `intent` is buy, sell, rent, invest, schools, rules or lifestyle. Leave `monthly_volume` blank if your tool does not give it.
3. **headings.csv**: `area, page, heading, found_on_how_many_of_top5`. The section headings that appear on at least 2 of the top 5 ranking pages for "<area> homes for sale" and are NOT obvious boilerplate (no "Contact us", "Mortgage calculator").
4. **verify.csv**: for the 34 rows with a `claim_to_check`: `area, claim, verdict, corrected_wording, source_url, date_read`. Verdict is TRUE, FALSE, CORRECTED or UNCONFIRMED. Use only municipal, provincial, school district, TransLink, or other official pages, or the municipality's own heritage or history pages. If an official page does not state it, write UNCONFIRMED. Do not guess a year, number, distance or "only/oldest/largest" claim.
5. **keyword-volumes.csv**: for the 60 keywords in the second CSV: `keyword, monthly_volume, top_3_related_questions`.

Rules:
- Never use Google Maps/Places, Yelp, Walk Score, REW, Zolo, Zillow, zealty.ca, any MLS or listing site, or another agent's site as a source.
- Facts only. No prices, listing data or marketing words.
- If you cannot confirm something, write UNCONFIRMED. Never invent a coordinate, volume, source URL or date.
- Put a source URL on every row of coordinates.csv and verify.csv.
- After each batch of 25, tell me which rows came up short and why.
