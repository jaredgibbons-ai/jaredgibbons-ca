# Live site review, 17 November 2026

Report only. No page on the site was edited. The live site is https://www.jaredgibbons.ca, which redirects once to https://jaredgibbons.ca. The sitemap has **1,944** URLs (1,927 on 16 Nov). Source quotes are from `origin/main` at `89d75fe0`.

## Summary

The site loads. All 1,944 sitemap URLs returned 200. Phone, email, and office are right. There is no UBC Sauder diploma claim, no Suite 118, and no ranking claim in an H1. The homepage listings loaded, and the mortgage calculator opened with the 4.69% example rate.

The problems that matter are a shared sign-off that adds ranking lines Jared has not approved, review quotes that are cut off while the page says they are word for word, one article whose URL still describes a different condo, and three outside links that do not open a real page.

### Top 10

1. **About 133 pages add ranking lines that are not on the approved list.** The sign-off says he ranked "#8 of 5,061 Fraser Valley Realtors, Top 35 Under 35 at Royal LePage Canada, and Top 10 at Royal LePage British Columbia." Some pages also say "Diamond and Hall of Fame." The approved lines (number 1 in South Surrey / White Rock for 2025 and 2026 YTD, number 1 of the Top 25 at Little Oak for 2025, Top 1% of Fraser Valley REALTORS, 10 straight years, more than $500M, licensed since 2015) are still there and were not flagged. 116 of these pages show the extra lines in the visible text. The mortgage calculator shows them too.

2. **The same sign-off says "I'm back living here now" on pages that are not about Langley.** On the mortgage calculator and on the Annacis Island industrial page, "here" is not Langley. That sentence is part of the same block as the extra ranks.

3. **The review block says the quotes are word for word, and 42 of 78 are cut off.** The intro is "Quoted word for word; initials only." A quote from S.E. stops at "farther away…" while the full Google review keeps going. Initials, the calendar date, and "Google review" are on the quotes. The reviews API is fine: 94 reviews stored, 89 with text, average 5.0, total count 95. The page saying "All 89 written Google reviews" matches the 89 that have text. This block is on 1,521 pages. The homepage quotes that were checked are the full text.

4. **An Aldergrove condo article still lives at a South Surrey URL.** The address in the URL is 15735 Croydon Drive and a $619k price drop. The title, H1, and body are 301–27215 Aldergrove Town Centre Drive. This was already in the 16 Nov copy review.

5. **The Cloverdale guide and the Mission guide repeat the place name in the breadcrumb.** Each trail has the city twice, and the schema has an extra step. The first city link goes to the houses page, then the hub, then the guide. The Cloverdale and Mission hub pages themselves were fixed: the last crumb is now the current page, not a link away.

6. **Two Langley pages both say they are the homes-for-sale page.** `/langley-city.html` and `/city-of-langley-homes-for-sale.html`. Still open from the 16 Nov deep audit.

7. **The homepage title still names White Rock and Langley.** The H1 is only "South Surrey Realtor." Still open from the 16 Nov deep audit.

8. **178 blog posts still have no publisher logo in the article schema.** Still open. It was 202 posts on 16 Nov. Headline, date, and author are there.

9. **wildwoodmanufacturedhomes.com does not exist.** It is linked from the Coquitlam 55-plus page and the Coquitlam West page. The host does not resolve.

10. **willowbrookmall.com is a domain for sale, and Queen Mary Elementary's site returned 504.** The mall link is on the Clayton Waterstone blog post and ends at HugeDomains. `queenmary.sd44.ca` returned 504 on 17 Nov from the North Vancouver homes page. Other Willowbrook links that use shopwillowbrook.com are a different site and did not fail this way.

## What was checked and is clean

| Check | Result |
| --- | --- |
| Sitemap | 1,944 URLs, every one HTTP 200. No redirect loop on those URLs. |
| Internal links and files | Every href, image, script, canonical, og:image, and JSON-LD URL on this site was checked. A first pass that lowercased the paths produced false 404s, because `/img/Jared.webp` and the script files are case-sensitive. Rechecked at the original spelling: **0 internal 404s**. |
| Old .html addresses | The site uses .html on purpose. The ones in the sitemap resolve. Linked blog posts that are missing from the sitemap are marked noindex and return 200. |
| Phone, email, office | 604-928-1361, jaredgibbons@royallepage.ca, Suite 201 / #201 at 15272 Croydon Drive, Surrey. No Suite 118. |
| Years and sales | "Licensed since 2015" and "$500M+" are the lines in use. No Sauder or Urban Land Economics diploma. |
| Rankings in H1s | None. One H1 says Crescent Beach is one of Canada's top 10 beaches. That is about the beach, not a sales rank. |
| Reviews on the reviews page | Initials, ISO dates in the data, Google as the source. "All 89 written" matches 89 reviews that have text out of 94 stored. |
| Homepage listings | The "Our listings" section showed live listing cards. The "did not load" line is in the HTML but hidden, and it was not showing. |
| Mortgage calculator | Opens. Example rate 4.69% dated 12 Nov 2026. It asks for a home price before it shows a payment. |
| Outside links | 6,532 unique URLs. **0 confirmed 404s.** One domain does not exist (wildwood). One domain is parked (willowbrookmall.com). One school site returned 504. Blocks (403), certificate errors, and timeouts were not counted as dead. |

## Already fixed, so not listed again as open problems

These were wrong on 16 Nov and are right on the live site today:

- The sold Cloverdale Greenside post no longer describes a South Surrey open house. The title, H1, and description are the Cloverdale townhome.
- Abbotsford and Surrey homes pages: the last breadcrumb now matches the H1 ("Abbotsford Homes for Sale", "Surrey Homes for Sale").
- "Ask for the The Beverley" (and the same typo on the other buildings) now reads "Ask for The Beverley strata package."
- The six outside sites that returned 502 or 520 on 16 Nov answered this time: roundhouse.ca, surreyhistory.ca, building.ca, merrybright.ca, and fvmba.com returned 200 or a normal redirect. langleyheritage.ca returned 200 on a direct check after a flaky first lookup.
- Portrait and script files that looked missing were the lowercase copies of files that exist.

## Broken links

Full rows: `broken-links.csv`. **5 rows. 4 problems.**

| Page | Broken URL | Status | Fix |
| --- | --- | --- | --- |
| Coquitlam 55-plus and Coquitlam West | http://www.wildwoodmanufacturedhomes.com/ | Domain does not resolve | Remove or replace |
| Clayton Waterstone blog post | https://www.willowbrookmall.com/ | Redirects to a HugeDomains for-sale page | Link to the real mall site |
| North Vancouver homes | https://queenmary.sd44.ca/ | 504 | Recheck; use the school district page if it stays down |
| Clayton Cloverdale houses | Surrey West Clayton land-use PDF | 3 redirects, then 200. Still open from the 16 Nov deep audit | Link to the final URL |

No mailto or tel errors. The phone links are 604-928-1361. The email link is jaredgibbons@royallepage.ca. One choir email on a blog post is a different address and is a valid mailto.

Nineteen links are still `http://` rather than `https://`. They were listed on 16 Nov. They are not 404s, so they are not in the broken-link table except wildwood, which is dead.

## Mismatches

Full rows: `mismatches.csv`. **142 rows.** 133 of them are the extra ranking sign-off, one per page. The other 9 are below.

| Page | What does not match | Severity |
| --- | --- | --- |
| 133 pages, including the mortgage calculator and Annacis Island | Extra ranks: #8 of 5,061, Top 35 Under 35, Top 10 Royal LePage in BC, and on many pages Diamond and Hall of Fame | High |
| 1,521 pages with the review block (example: the South Surrey agent page) | "Quoted word for word" but 42 of 78 quotes end in … | High |
| Aldergrove article at the Croydon Drive URL | URL says South Surrey. Page says Aldergrove | High. Still present from the 16 Nov copy review |
| Cloverdale guide, Mission guide | Breadcrumb and schema repeat the city | Med. Still present from the 16 Nov copy review |
| Homepage | Title includes White Rock. H1 does not | Med. Still open from the deep audit |
| Langley City and City of Langley homes | Both are the homes-for-sale page | Med. Still open from the deep audit |
| 178 blog posts | Article schema has no publisher logo | Med. Still open from the deep audit |
| Grey whales blog post | URL says South Surrey. Title is White Rock and Crescent Beach | Low |

Office, phone, email, "since 2015", and "more than $500M" match across the pages that were checked. Canonicals match the page URL. Every title is present and 60 characters or under. Every page has an H1 and a meta description.

## Things that don't make sense

Full rows: `doesnt-make-sense.csv`. **5 rows.**

| Page | What is odd | Severity |
| --- | --- | --- |
| Mortgage calculator, and the same sign-off on the ranking pages | "I'm back living here now" when the page is not Langley | High |
| Annacis Island | An industrial Delta page ends with the Langley farm bio and the Fraser Valley rank list | Med |
| Fraser Valley buyer-advantage post | Headline says "in Favor of Buyers" | Low |
| New-construction city pages (example: Cloverdale) | Still the same shell with the city swapped. Still open from the deep audit. The sold-stat line under the listings is unique to each city | Med |
| Surrey, Vancouver, Burnaby, and Coquitlam presale pages | Still the same short opening with the city swapped. Still open from the deep audit | Med |

No lorem, TODO, or "Draft for Jared" text showed in the live page text. "TBD" on the seller FAQ is the real estate phrase "to be determined," not a placeholder. "Coming soon" on the Whalley houses page is the City describing a facility.

Quoted reviews were not marked up for the writer's grammar. One quote says "Jared was able sell my home." That is the client's sentence.

## How to read the counts

| File | Rows | What that means |
| --- | --- | --- |
| `broken-links.csv` | 5 | 3 destinations that fail, plus one redirect chain that still loads, with wildwood listed on both source pages |
| `mismatches.csv` | 142 | 133 ranking-sign-off pages, plus 9 other mismatches |
| `doesnt-make-sense.csv` | 5 | The "living here" sentence, the Annacis bio, one spelling, and two duplicate-page groups that are still open |

Items marked "Still open from the 16 Nov deep audit" were already in `reports/deep-audit-2026-11-16/`. Items marked "Still present from the 16 Nov copy review" were in `reports/seo-copy-2026-11-16/`.
