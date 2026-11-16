# How to fix the duplicate groups

16 November 2026. Options only. No page was edited.

This follows the deep audit in `reports/deep-audit-2026-11-16/`. Every group is in `groups.csv` with a recommended option. The write-ups below use figures already published on the site or in `src/data/local/`. Nothing new was calculated. Lines marked **confirm** should be checked by Jared before they are used in a title.

Options, used the same way in every table:

| | Option | SEO impact | Effort | Risk |
| --- | --- | --- | --- | --- |
| a | Rewrite each page with its own local paragraph | High, if the facts are real | A paragraph per page | Low if the fact is already on the page. High if a project or price is guessed |
| b | Merge into one page and 301 the others | High for one strong URL. You lose the other searches | One redirect map | High if the pages answer different questions (houses vs condos) |
| c | Canonical tag pointing at the main page | Tells Google which URL to keep. The other URL can stay for readers | A tag per duplicate | Medium. Google may ignore it if the pages are not really the same |
| d | noindex the extra page | The extra page drops out of Google | One meta tag | High if that page is the one buyers use |
| e | Split the intent in the title and H1 | Each URL keeps a job: hub, houses, or condos | Title edits | Low |
| f | Data template: each city fills the same fields (sold count, median, one project or street) | The pages stay related but stop matching | One template, fields that already exist | Low |

## Recommended plan, in order

1. **New-construction cities (12 pages, 94.9%).** Pick **f**, then a short **a**. Do not merge them. Each file already has its own sold line. Move that line above the shared form. Effort: one template, no new research.
2. **Presale pairs (Surrey/Vancouver at 90.2%, Burnaby/Coquitlam at 90.0%, plus the smaller presale clusters).** Pick **f**. Put the city’s own sold line, already in the data file, in the title, the H1 and the first sentence. **Confirm** any developer project name before it goes in a title. The Muse project lists are marked draft. Effort: one template.
3. **98 title pairs (hub vs houses, hub vs condos, houses vs condos).** Pick **e**. Keep every URL. Change the titles so only the hub says “homes for sale”. Effort: title and H1 edits in `src/data/seo-final.json`. No new facts.
4. **Homepage vs `/white-rock-realtor.html`.** Pick **e**. The homepage owns “South Surrey realtor”. The White Rock page owns “White Rock realtor”. Effort: one title change.
5. **City of Langley vs Langley City.** Pick **e**. `/langley-city.html` is the place page. `/city-of-langley-homes-for-sale.html` is the listings page. Effort: two titles. The bodies are already different.
6. **Listing clusters (80% and up).** Pick **f** and keep both URLs. The match is the sold-listing shell. Same-address pairs stay, with the MLS number in the title. Do not 301 a sold listing. Effort: check the duplicate-address rule, not a rewrite of every sold page.

## Group 1. Twelve new-construction city pages (94.9%)

**Why it is a problem.** Google sees twelve pages that open the same way: “New construction homes for sale in {city}”, then the same email-alert form, then “The live listings did not load.” A buyer cannot tell Ladner from Cloverdale in the first screen. The city-specific sold paragraph is already on the page, but it sits below that shared block, so it does not lead.

Pages: Cloverdale, North Vancouver, Mission, Ladner, Richmond, Port Moody, Sardis, Tsawwassen, Maple Ridge, New Westminster, Port Coquitlam, West Vancouver.

**Before, Cloverdale** (live page and `src/data/local/new-construction-cloverdale.json`)

- Title: Cloverdale New Construction Homes for Sale | Presales
- H1: New Construction Homes for Sale in Cloverdale
- Meta: New construction across Cloverdale: live MLS® listings, sold prices in Clayton, nearby presale projects and the new-home tax and presale rules to know.
- Opening: New Construction Homes for Sale in Cloverdale. Then the alert form.

**After, Cloverdale.** Uses the sentence already on the page. Source line on the page: Paragon closed sales, November 1, 2025 to October 22, 2026. Medians need 5 or more sales.

- Title: Cloverdale New Duplexes | 9 Sold, Median $1,173,000
- H1: New duplexes in Cloverdale
- Meta: From November 2025 to October 2026, the newest Cloverdale sales were duplexes: 9 sales, median year built 2024, median price $1,173,000.
- Opening: The newest homes to sell in Cloverdale, from November 2025 to October 2026, were duplexes. Nine sold. The median year built was 2024 and the median price was $1,173,000.

**After, Ladner.** From `src/data/local/new-construction-ladner.json`.

- Title: Ladner New Condos | Neilsen Grove, Median $840,000
- H1: New condos in Ladner
- Meta: From November 2025 to October 2026, the newest Ladner sales were condos in Neilsen Grove: 9 sales, median year built 2021, median price $840,000.
- Opening: In Ladner, the newest homes to sell over that same year were condos in Neilsen Grove. Nine sold, at a median of $840,000, with a median year built of 2021. No Ladner condo building or townhome complex built in 2022 or later had 3 or more resales in that year. Brand-new Ladner homes are usually the developer’s first sale, so they do not show up as resales.

**After, Mission.** From `src/data/local/new-construction-mission.json`.

- Title: Mission New Duplexes | 16 Sold, Median $935,595
- H1: New duplexes in Mission
- Meta: From November 2025 to October 2026, Mission’s newest sales were duplexes: 16 sold, median year built 2025, median price $935,595.
- Opening: The most recently built homes that sold in Mission in that year were duplexes. Sixteen sold at a median of $935,595. The median year built was 2025. Mission-West townhomes (median year 2022) were the next newest group with enough sales to measure.

**Confirm:** these medians are the ones already written into the local files and, for Cloverdale, visible on the live page. They should not be retyped into a title until Jared is happy with the November 2025–October 2026 window.

| Option | Pick? |
| --- | --- |
| a Rewrite | Use it for the opening, with the sentence that is already in the file |
| b 301 into one page | No. A Mission buyer should not land on a Cloverdale page |
| c Canonical | No. These are different cities |
| d noindex | No. Each city is a real search |
| e Intent split | Not the main issue. They already all mean “new homes” |
| **f Data template** | **Yes.** Fields already in each file: sub-area, home type, sales count, median price, median year built, date window |

**Template.** `src/data/local/new-construction-*.json`, rendered by `GenericPage.astro`. The shared pieces to leave shared are the alert form and the VIP box. The first heading and paragraph should be the city’s sold sentence, not “New construction homes for sale in {city}”. Fields each city needs, all present today: sub-area name, home type, sales count, median price, median year built, source window.

## Group 2. Presale pages (90% and the smaller presale clusters)

**Why it is a problem.** Surrey, Vancouver, Burnaby and Coquitlam open with the same definition of a presale and the same VIP box. Only the city name changes. The files underneath already name a different neighbourhood and a different median. Google, and a buyer, see the shared intro first.

Smaller clusters in `similarity-clusters.csv` (ranks 15 through 26) are the same kind of page for one neighbourhood at a time (Whalley, Clayton, Kitsilano, and so on). Same fix.

**Before, Surrey**

- Title: Surrey Presale Condos & Townhomes | Completing 2027–2029
- H1: Surrey Presale Condos and Townhomes, 2027–2029
- Opening: Presale means you buy a home before it is built, and you take possession when it completes. This page lists every Surrey presale project on my list that is scheduled to complete between 2027 and 2029…

**After, Surrey.** The unique lines in `src/data/local/surrey-presale-condos-and-townhomes.json` are: 25 projects on the list as of November 2026 (16 completing in 2027, 6 in 2028, 3 in 2029); 20 condo, 4 mixed, 1 townhome; largest named project Whalley Station at 550 homes. **Confirm** those counts. The file says “Draft for Jared’s approval. Built from Muse’s presale list (2026-11-01).” Do not put Whalley Station in a title until Jared confirms the list.

Safer after, using the counts but not a project name:

- Title: Surrey Presales Completing 2027–2029 | 25 Projects on My List
- H1: Surrey presales completing 2027 to 2029
- Meta: 25 Surrey presale projects are on my November 2026 list: 16 completing in 2027, 6 in 2028 and 3 in 2029. Mostly condos.
- Opening: I am tracking 25 Surrey presale projects scheduled to finish between 2027 and 2029. Sixteen are aimed at 2027. Twenty of the 25 are condo projects. **Confirm** the 25 before this goes live. The file still says the Paragon presale feed has not been merged.

**After, Vancouver.** From `src/data/local/vancouver-presale-condos-and-townhomes.json`. This sold line is Paragon-style, same window as the other city files.

- Title: Vancouver’s Newest Duplex Sales | Renfrew, Median $1,350,000
- H1: Newest duplex sales in Renfrew, Vancouver
- Meta: From November 2025 to October 2026, duplexes that sold in Renfrew had a median year built of 2026: 64 sales, median price $1,350,000.
- Opening: Renfrew led Vancouver for newness in that year. Duplexes that sold there had a median build year of 2026, with 64 sales at a median of $1,350,000.

**After, Burnaby and Coquitlam**, same file pattern.

- Burnaby: Forest Glen duplexes, median year built 2026, 13 sales, median $1,504,000.
- Coquitlam: Maillardville duplexes, median year built 2026, 21 sales, median $1,285,000.

**Confirm** those three sold lines the same way as Cloverdale: they are in the local files for November 2025 to October 2026. They are not in the shared opening a buyer sees first.

| Option | Pick? |
| --- | --- |
| a Rewrite | Yes, using the sentence already in the file |
| b 301 | No. Surrey and Vancouver are different searches |
| c Canonical | No |
| d noindex | No |
| e Intent split | Already the same intent. The cities are what must differ |
| **f Data template** | **Yes.** Fields: project count by year, home-type mix, one sub-area sold line (type, sales, median, year built) |

**Template.** `src/data/local/*presale*.json` and `src/data/local/new-construction-*.json` for the neighbourhood clusters. `GenericPage.astro` prints the shared “Presale means…” paragraph. Replace that first paragraph with the city’s first unique `p` block. Fields each city needs: completion-year counts, type mix, and one sold line. Project names stay out of titles until the draft flag is removed.

## Group 3. Hub versus houses versus condos (98 title pairs)

**Why it is a problem.** A buyer searching “Willingdon Heights houses” and a buyer searching “Willingdon Heights homes” can land on either page. Both titles say the neighbourhood, Burnaby, and “for sale”. Google has no clear main page. The pages are not copies. Willingdon’s hub is about 3,900 words and the houses page is about 2,000, with its own October counts. The titles are what collide.

This is the pattern for all 98 rows in `groups.csv` whose id starts with `title-pair`. Worked examples: Willingdon Heights, and the same rule for Whalley and Westwood Plateau.

**Before, Willingdon hub** `/willingdon-heights-burnaby.html`

- Title: Willingdon Heights, Burnaby Homes for Sale | Prices
- H1: Willingdon Heights, Burnaby Homes for Sale
- The page’s own October line, from `src/data/local/willingdon-heights-burnaby.json`: 17 houses and 17 condos and townhomes listed at the end of October, with 1 and 2 sold. One of 35 Burnaby communities in the Greater Vancouver REALTORS® figures.

**Before, Willingdon houses** `/willingdon-heights-burnaby-houses-for-sale.html`

- Title: Willingdon Heights Houses for Sale, Burnaby | Prices
- H1: Willingdon Heights Houses for Sale
- From the houses file: 17 houses listed at the end of October 2026 and 1 sold, a sales ratio of 6%, which that report reads as a buyers’ market. By listings, number 10 of 35 Burnaby communities for houses.

**After**

- Hub title: Willingdon Heights, Burnaby | Homes, Condos and Houses
- Hub H1: Willingdon Heights, Burnaby
- Hub opening: At the end of October, Willingdon Heights had 17 houses listed and 17 condos and townhomes listed. One house sold that month and two condos or townhomes sold. It is one of 35 Burnaby communities in those figures. For houses only, use the houses page. For condos and townhomes, use that page.
- Houses title: Willingdon Heights Houses for Sale | 17 Listed in October
- Houses H1: Houses for sale in Willingdon Heights
- Houses opening: Willingdon Heights had 17 houses listed at the end of October 2026 and 1 sold, a 6% sales ratio. By listings it was number 10 of 35 Burnaby communities for houses.

**Confirm** the October window and the “buyers’ market” label. Both are in the local files. The 6% reading is the file’s own scale, not a new claim.

**Whalley, same rule, no new numbers.** Hub `/whalley.html` title today: “Whalley Homes for Sale, Surrey | SkyTrain & City Centre”. Condos page: “Whalley Condos for Sale | Surrey City Centre SkyTrain”. After: hub keeps SkyTrain and City Centre and says “homes”. Condos title stays “condos” and drops “homes for sale”.

**Westwood Plateau, same rule.** Hub should not say “Houses” in the title if a separate houses page exists. Today the hub is “Westwood Plateau, Coquitlam Homes for Sale | Houses” and the houses page is “Westwood Plateau, Coquitlam Houses for Sale”. After: hub drops the word “Houses”. Houses page keeps it.

| Option | Pick? |
| --- | --- |
| a Full rewrite | No. The bodies already differ |
| b 301 the houses page into the hub | No. “Houses” is its own search |
| c Canonical | Only if two URLs are truly the same page. These are not |
| d noindex | No |
| **e Intent split** | **Yes.** Hub = homes. Houses = houses. Condos = condos. Distinct titles, H1s, and links between them |
| f Data template | Already there (October counts). Use those counts in the houses title when Jared confirms the month |

**Template.** Titles and H1s: `src/data/seo-final.json`. Do not change `GenericPage.astro` for this group. Each neighbourhood needs three labels only: hub name, houses name, condos name. Internal links: the hub links to houses and to condos with those words, not with a second “homes for sale”.

## Group 4. Homepage and `/white-rock-realtor.html`

**Why it is a problem.** The homepage title is “South Surrey Realtor | White Rock & Langley | Jared Gibbons”. The H1 is “JARED GIBBONS South Surrey Realtor”. A second page, H1 “White Rock Realtor Jared Gibbons”, was built for the White Rock search. Both titles can match “White Rock realtor”.

**Before, homepage.** Title as above. Opening on the page includes the approved lines in the hero, which is fine in a subheading: “Top 1% of Fraser Valley REALTORS®” and “#1 in South Surrey / White Rock by FVREB Medallion Club points (2025 and 2026 YTD)”.

**Before, White Rock page.** Title: White Rock Realtor Jared Gibbons | Top 1% Fraser Valley. Opening already on the page: condos in the Uptown towers, houses on the hillside, homes along Marine Drive. Office on Croydon Drive in South Surrey, a short drive from Uptown. Phone 604-928-1361. REALTOR® since 2015.

**After**

- Homepage title: South Surrey Realtor | Jared Gibbons
- Homepage H1: stays “JARED GIBBONS South Surrey Realtor”
- Homepage opening: unchanged. The #1 South Surrey / White Rock line stays in the subheading, not the H1.
- White Rock title: White Rock Realtor | Uptown, Hillside and Marine Drive
- White Rock H1: stays “White Rock Realtor Jared Gibbons”
- White Rock opening, already true on the page: I have sold homes in White Rock and South Surrey since 2015: condos in the Uptown towers, houses on the hillside and homes along Marine Drive. My office is on Croydon Drive in South Surrey.

The “Top 1%” line stays a subheading. It does not move into the H1.

| Option | Pick? |
| --- | --- |
| a Rewrite the White Rock page | Lightly. The opening is already specific. The title should name Uptown, the hillside or Marine Drive |
| b 301 | No. Do not fold White Rock into the homepage |
| c Canonical | No |
| d noindex | No |
| **e Intent split** | **Yes** |
| f Data template | Not needed |

**Template.** `src/pages/index.astro` for the homepage title. `src/data/seo-final.json` or the White Rock page’s `new_page.title` for the other. No new fields.

## Group 5. City of Langley and Langley City

**Why it is a problem.** `/city-of-langley-homes-for-sale.html` is titled “City of Langley Homes for Sale | Live MLS® Listings”. `/langley-city.html` is titled “Langley City Homes for Sale | Live MLS® Listings”. Same search, two long pages (about 3,900 and 3,800 words). The bodies are not copies. Langley City’s page already says Jared has sold homes there and links route 501 (Surrey Central via Fraser Highway), route 503 (Fraser Highway Express), Timms Community Centre and the library at 20399 Douglas Crescent, and Douglas Park Community School (K–5, SD35, 5409 206 Street; catchment to be confirmed with the district).

**After**

- `/langley-city.html` title: Langley City Neighbourhoods | Fraser Highway and Douglas Crescent
- H1: Living in Langley City
- Opening: Langley Centre is the end of bus route 501, along Fraser Highway to Surrey Central, and route 503, the Fraser Highway Express. Timms Community Centre and the library are at 20399 Douglas Crescent.
- `/city-of-langley-homes-for-sale.html` title: City of Langley Homes for Sale | Houses, Condos, Townhomes
- H1: Homes for sale in the City of Langley
- Opening: stays the listings page. First line should point at the live list, and link to the Langley City page for the buses, the library and the school.

**Confirm** the school catchment line. The file already says to confirm it with the district. Do not state a catchment as fact in the new title.

| Option | Pick? |
| --- | --- |
| a Rewrite both from scratch | No |
| b 301 one into the other | Only if Jared wants a single URL. Not the first choice. The place page and the listings page do different jobs |
| c Canonical | Possible later, if Search Console shows one page getting all the clicks. Not yet |
| d noindex | No |
| **e Intent split** | **Yes** |
| f Data template | The listings page can keep the MLS list. The place page keeps the bus and park facts |

**Template.** Titles in `src/data/seo-final.json`. Unique fields the place page already has: bus routes, civic address of Timms, school name. No new data file.

## Group 6. Listing clusters (80% and up)

**Why it is a problem, and why it is smaller.** Sold listing pages share a shell, so a Langley sold page and another Langley sold page score around 85%. That is the template, not two articles. Google can still tell them apart by the address.

The pairs that deserve a look are the same street twice:

- 2827 Woodland Drive, Langley, two MLS numbers (cluster 5, 88.6%).
- North Bluff Road, White Rock, units 305, 307 and 406 (cluster 4, 88.7%).
- 15219 Royal Avenue, White Rock, units 301 and 101 (cluster 6).

**Before.** Two sold pages for one street, titles that both lead with the address, body mostly the shared sold template.

**After.** Keep both URLs. Title and H1 include the MLS number, which the listing template already does when the same address appears twice. Example shape: “2827 Woodland Drive, Langley (MLS® R2632788)”. Do not merge the two sales into one page. A buyer looking up an old MLS number should still land on that sale.

| Option | Pick? |
| --- | --- |
| a Rewrite every sold page | No |
| b 301 | No, except a true duplicate of the same MLS |
| c Canonical | Only for the same MLS published at two URLs. **Confirm** there is no such pair before adding tags |
| d noindex | No |
| e Intent split | Not relevant |
| **f Data template** | **Yes.** Address, unit, MLS number, sold date, sold price. Those fields already exist |

**Template.** `src/components/ListingPage.astro`. The duplicate-address title rule is already in that file. The check is that Woodland Drive and the North Bluff units actually show the MLS number in the live title. No new fields.

## What not to do

Do not invent a presale project, a school catchment, or a median. Do not put a ranking line in an H1. The approved lines stay in subheadings. Do not edit review quotes. Do not add a UBC Sauder line. Do not noindex a city page to “solve” a duplicate.
