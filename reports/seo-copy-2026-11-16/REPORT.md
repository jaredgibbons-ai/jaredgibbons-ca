# Breadcrumbs, titles, descriptions, length and spelling

16 November 2026. Report only. No page was edited.

Live sitemap: **1,927 URLs**, all HTTP 200. Checked against the live HTML (visible breadcrumb, title, meta description, H1, and the words inside `<main>`, leaving out the nav, the footer, the listing search widget and the review quotes). Source of truth for "what is on the site now" is the live site, which matches `origin/main` at `fdb178c3`.

Jared's confirmed lines were not flagged: "10 straight years" in the Medallion Club, "Top 1% of all REALTORS® in the Fraser Valley", the three approved ranking sentences, "$500M" in sales, and the 94-review count. No ranking claim sits in an H1. No UBC Sauder diploma claim. Quoted reviews were not spell-checked; none of the spelling hits below are inside a review.

## Summary

| Category | What turned up |
| --- | --- |
| Breadcrumbs | Every page except the homepage has one. The schema matches the visible trail on all but 4 pages. **4 high**, **93 medium**, **77 low**. |
| Titles | **1 high**. Otherwise clean: 1,927 unique titles, every one between 30 and 60 characters. None missing, none duplicated, none cut off. |
| Meta descriptions | **1 high**, **33 low**. Otherwise clean: all present, all unique, all between 98 and 158 characters. |
| Word count | Median main text is about **2,080 words**. No neighbourhood guide is under 300. **9 presale pages** are thin (70 to 280 words). Four of them are the same short page with the city swapped. |
| Spelling and grammar | **4 medium**, **1 low**. No review quotes were changed or flagged as errors. |

### Top 20 fixes, by impact

1. **Cloverdale hub.** The last crumb is a link to `/cloverdale-houses-for-sale.html`, so the trail never lands on `/cloverdale-bc.html`. The schema also inserts an extra "Cloverdale".
2. **Cloverdale guide.** The visible trail is Home > Cloverdale > Cloverdale guide. The schema inserts a second Cloverdale.
3. **Mission hub.** Same bug as Cloverdale. The last crumb links to `/mission-homes-for-sale.html` instead of staying on `/mission-bc.html`.
4. **Mission guide.** The schema inserts an extra Mission that the visible trail does not have.
5. **Wrong URL on an Aldergrove article.** `/blog.html/10k-price-drop-south-surrey-condo-at-15735-croydon-dr-619k-8934508` still says South Surrey and Croydon Drive. The title, H1 and body are about 301–27215 Aldergrove Town Centre Drive.
6. **Wrong description on a sold Cloverdale post.** `/blog.html/sold-in-cloverdale-modern-3-bedroom-in-greenside-8701040` describes a South Surrey open house on May 31. The page is a sold townhome in Greenside, Cloverdale.
7. **Abbotsford homes.** Last crumb is "Every active Abbotsford home listing, newest first". The H1 is "Abbotsford Homes for Sale".
8. **Surrey homes.** Last crumb is "MLS Listings, Houses, Townhomes & Condos in Surrey". The H1 is "Surrey Homes for Sale".
9. **Vancouver homes.** Last crumb is the old "MLS Listings, Condos, Townhomes & Detached Houses…" line. The H1 is "Vancouver Homes for Sale".
10. **Coquitlam, Richmond, New Westminster, North Vancouver, West Vancouver, Port Coquitlam, Port Moody and Maple Ridge homes.** Same pattern: the last crumb is the old "MLS Listings…" sentence, the H1 is the short "Homes for Sale" line.
11. **Steveston, Rosedale, Burke Mountain, Chilliwack under $1.8M, and the other rows marked medium in `breadcrumbs.csv`.** The last crumb was left behind when the H1 was rewritten. One fix covers them: set the last crumb (and the schema name) to the current H1.
12. **Open houses.** Crumb says "Upcoming Open Houses in South Surrey, Langley & Surrounding Areas". H1 says "Open Houses in the Fraser Valley & Lower Mainland".
13. **Nine thin presale pages.** Abbotsford, Burnaby, Coquitlam, Surrey and Vancouver are 70 to 120 words, and the last four are the same short text with the city swapped. Langley new-construction, the Fraser Valley presale roundup, and two South Surrey presale pages are 212 to 280 words.
14. **Four building pages** say "Ask for the The Beverley / Heights / Semiah / Summit strata package."
15. **77 neighbourhood pages** end the trail with "Belcarra real estate" (and the same shape for the others) while the H1 says "Belcarra Homes for Sale". The place is right. The label does not match the H1. Low.
16. **33 price-band descriptions** use one sentence shape ("Search [city] condos for sale under $[price]…") with that city's own numbers filled in. Not copies, but they read alike. Low, and optional.
17. One blog headline says "in Favor of Buyers". Canadian spelling is "favour", if that line is Jared's and not a quoted headline.
18. Do not regenerate titles to chase a 60-character limit. None are over 60.
19. Do not rewrite descriptions for length. None are over 160 or under 70, and none are duplicated word for word.
20. Do not add breadcrumbs to the homepage. It is the one page that correctly has none.

## Breadcrumbs

The visible trail is a `nav` labelled Breadcrumb. The JSON-LD `BreadcrumbList` is built from the same list. The homepage has neither, which is correct. Every other sitemap URL has a trail. Parent links all point at a page that is in the sitemap.

**High. The trail does not land on the page, or the schema adds a step.**

| Page | Visible | Schema |
| --- | --- | --- |
| `/cloverdale-bc.html` | Home > Cloverdale, and Cloverdale links to `/cloverdale-houses-for-sale.html` | Home > Cloverdale > Cloverdale |
| `/cloverdale-bc-guide.html` | Home > Cloverdale > Cloverdale guide | Home > Cloverdale > Cloverdale > Cloverdale guide |
| `/mission-bc.html` | Home > Mission, and Mission links to `/mission-homes-for-sale.html` | Home > Mission > Mission |
| `/mission-bc-mission-guide.html` | Home > Mission > Mission guide | Home > Mission > Mission > Mission guide |

**Medium. The last label is an older sentence, not the H1.** 93 pages. The schema repeats that older sentence, so it matches the visible crumb and both disagree with the H1. Examples:

- `/abbotsford-homes-for-sale.html`: crumb "Every active Abbotsford home listing, newest first", H1 "Abbotsford Homes for Sale".
- `/surrey-homes-for-sale.html`: crumb "MLS Listings, Houses, Townhomes & Condos in Surrey", H1 "Surrey Homes for Sale".
- `/open-houses.html`: crumb "Upcoming Open Houses in South Surrey, Langley & Surrounding Areas", H1 "Open Houses in the Fraser Valley & Lower Mainland".

The full list is `breadcrumbs.csv`. Blog posts are not in this list. On a post, the crumb is the title and the H1 is the article headline. Those two often differ in wording and still describe the same story, so they were left alone.

**Low. "X real estate" versus "X Homes for Sale".** 77 neighbourhood pages, for example Belcarra, Yaletown, Steveston is not in this set (Steveston is in the medium set). The place name is in both. The wording does not match.

Suggested fix for the medium and low rows: when the H1 changes, set the last breadcrumb name to that H1, in both the visible trail and the schema.

## Titles

1,927 titles. Shortest 30 characters, longest 60, median 52. No missing title, no duplicate, no title over 60, no title that ends mid-word, no ranking claim in an H1.

**One title problem, and it is the address of the page rather than the title text.**

`/blog.html/10k-price-drop-south-surrey-condo-at-15735-croydon-dr-619k-8934508`

The title is "Aldergrove Strata Condo: 301–27215 Aldergrove Town Centre Dr". The H1 and the body are about that Aldergrove condo. The URL still names a South Surrey price drop at 15735 Croydon Drive. Suggested fix: publish it at an Aldergrove URL and redirect the old one.

A sold listing at 5835 179 Street, Surrey, has the title "Single Family Home Sold in Cloverdale". Cloverdale is in Surrey, so that was not counted as a wrong place name.

## Meta descriptions

All 1,927 pages have one. Shortest 98 characters, longest 158, median 152. No duplicates. None over 160. None under 70. None are placeholders.

**High. One description describes a different event.**

`/blog.html/sold-in-cloverdale-modern-3-bedroom-in-greenside-8701040`

Current description: "Stop by our open house May 31 from 1–3 PM. Explore South Surrey condos and ask questions with Jared Gibbons on site."

The H1 is the sold Greenside townhome in Cloverdale. Suggested fix: describe that sale.

**Low. 33 price-band pages share a sentence shape.** Six groups, for example "Search Abbotsford condos for sale under $600,000. 84% of the 510 sold…" and the same sentence for Burnaby, Langley and the others, with that city's counts filled in. The numbers are not copied. The wording is. Optional to add one local detail. Listed in `metas.csv`.

## Word count

Counted in `<main>` only. Nav, footer, the MyRealPage listing widget and the review cards are not included.

| | Words |
| --- | --- |
| Shortest page | 49 |
| 10th percentile | 734 |
| Median | 2,080 |

No guide URL and no `homes-for-sale` URL is under 300 words.

Thin pages, all presale or new-construction:

| Words | Page |
| --- | --- |
| 70 | `/abbotsford-presale-condos-and-townhomes.html` |
| 118 | `/burnaby-presale-condos-and-townhomes.html` |
| 118 | `/coquitlam-presale-condos-and-townhomes.html` |
| 120 | `/surrey-presale-condos-and-townhomes.html` |
| 120 | `/vancouver-presale-condos-and-townhomes.html` |
| 212 | `/presale-projects-fraser-valley-and-metro-vancouver.html` |
| 237 | `/new-construction-presales-in-langley-bc.html` |
| 274 | `/south-surrey-new-construction-presales.html` |
| 280 | `/south-surrey-presale-condos.html` |

Burnaby, Coquitlam, Surrey and Vancouver are the same short page with the city name swapped. Suggested fix: a few paragraphs that name what is actually selling in that city.

## Spelling and grammar

Canadian spelling was treated as correct (`neighbourhood`, `centre`, `favour`, `colour`, and the rest). REALTOR®, MLS®, and place and street names were not flagged. Text inside a review quote was not flagged. No review quote in this pass contained one of the errors below.

| Page | Wrong text | Suggested fix |
| --- | --- | --- |
| `/beverley-white-rock-condos.html` | Ask for the The Beverley strata package | Ask for the Beverley strata package |
| `/heights-grandview-south-surrey-condos.html` | Ask for the The Heights strata package | Ask for the Heights strata package |
| `/semiah-white-rock-condos.html` | Ask for the The Semiah strata package | Ask for the Semiah strata package |
| `/summit-white-rock-condos.html` | Ask for the The Summit strata package | Ask for the Summit strata package |
| `/blog.html/fraser-valley-market-shifts-buyer-advantage-8243031` | in Favor of Buyers | in favour of buyers, if this line is Jared's |

## Files

| File | Rows |
| --- | --- |
| `pages.csv` | 1,927 pages: title, title length, meta, meta length, H1, breadcrumb, word count |
| `breadcrumbs.csv` | 174 |
| `titles.csv` | 1 |
| `metas.csv` | 34 |
| `wordcount.csv` | 13 rows, 9 pages (four copied presale pages are listed twice: thin, and a copy) |
| `spelling.csv` | 5 |

## What this pass did not treat as a defect

Ranking lines Jared has confirmed. FAQ markup. Early search rankings. A missing terms page. A missing robots tag. Long blog headlines. The 94 versus 95 review count. Breadcrumb wording on blog posts where the crumb is the title and the H1 is the article headline about the same story.
