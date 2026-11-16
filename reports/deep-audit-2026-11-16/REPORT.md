# Deep audit: overlap, links, schema, accessibility

16 November 2026. Report only. No page was edited.

Live sitemap: **1,927 URLs**, all HTTP 200. Main text excludes the nav, the footer, the listing-search widget and the review cards.

**Google Search Console was not available.** No query or click numbers below come from Google. They are on-page overlaps only. The export that would confirm them is Search Console, Performance, Search results, with both the Query and Page dimensions, downloaded as a spreadsheet (the Pages and Queries tables, or the combined query-plus-page export).

## Summary

| Check | Headline |
| --- | --- |
| Cannibalization | **98** pairs of area, guide or homes pages whose titles target the same search. No Google click data. |
| Near-duplicate text | Every page has a closest match in `similarity.csv`. **125** pages are at least 80% the same as another page. The worst cluster is **12 new-construction pages at 94.9%**. |
| Outbound links | **6,334** unique links. **0** confirmed dead (no 4xx other than blocks). **6** hosts returned 502 or 520. **1** timeout. **4** http links have a working https version. **1,208** were blocked or did not answer and are unverified, not dead. |
| Structured data | Checked locally against Google's required fields. Rich Results Test was not run. **0** structural errors. **202** blog posts are missing a publisher logo, which Article rich results ask for. No review or star schema. |
| Accessibility | Lighthouse accessibility (axe-core), mobile and desktop, one page per template. Scored pages are **100**. One real issue: **64** zoning links in a blog table whose accessible name does not match the visible text. |

### Top 15 fixes, by impact

1. Rewrite the shared new-construction template. Twelve city pages (`/new-construction-cloverdale.html` and the eleven listed with it) are 94.9% the same text.
2. Rewrite the short presale pages. Surrey and Vancouver are 90.2% the same. Burnaby and Coquitlam are 90.0% the same.
3. Stop neighbourhood hubs and their houses or condos pages from using the same title. 98 pairs. Example: "Willingdon Heights Houses for Sale, Burnaby | Prices" and "Willingdon Heights, Burnaby Homes for Sale | Prices".
4. The homepage title still says "White Rock". `/white-rock-realtor.html` was built for that search. The homepage can lead with South Surrey and leave White Rock to that page.
5. "City of Langley Homes for Sale" and "Langley City Homes for Sale" are the same search on two URLs.
6. Give each neighbourhood one primary URL for "homes for sale" and let the houses page and the condos page target those narrower words, not the same title.
7. Add a publisher logo to the BlogPosting schema on all 202 posts if Article rich results are wanted. The posts already have a headline, a date and an author.
8. Replace or recheck six outside sites that returned 502 or 520 from this network: roundhouse.ca, surreyhistory.ca, building.ca, langleyheritage.ca, merrybright.ca, fvmba.com.
9. Switch four http links to https. Those https addresses already answer: discoverbridalfalls.com, globalawards.news, whiterockshopping.com, and the Lasso brochure.
10. On the acreage blog post, 64 zoning links have an aria-label that does not include the visible text. Screen-reader users hear a different name than sighted users read.
11. Listing pages are 80% or more the same because they share a sold-listing template. That is expected. Do not rewrite them one by one. If a cluster is the same address listed twice, keep both only if the MLS number is what a searcher needs.
12. Do not delete FAQ schema. All 1,526 FAQ blocks have a question and an answer. Google does not show FAQ rich results for a realtor site. The markup is there for AI search, on purpose.
13. A few civic PDFs and a BC Ferries queue take three or four redirects. Low. Leave them unless a file starts failing.
14. Three http links did not answer on https from this network (clearbrookvillage.info, denebmanagement.com, the Sumas Mountain PDF). Leave them on http until https works.
15. Do not treat the 1,208 blocked or silent hosts as dead. They returned 403, 429, or nothing. LinkedIn's profile link returns 999 to bots. Recheck any of them in a normal browser before removing the link.

## 1. Keyword cannibalization

No Search Console connection was available, so there are no impressions or clicks in this section.

On-page method: among area, guide, presale and other non-blog, non-listing pages, a pair is listed when the meaningful words in the two titles overlap by at least 72%. That is `cannibalization.csv` (98 pairs).

What the pairs look like:

- A neighbourhood hub and its houses page: Willingdon Heights, Suncrest, Glenbrooke North, Westwood Plateau.
- A hub and its condos page: Whalley, Silver Valley, Uptown New Westminster.
- Houses and condos pages in the same pocket with the same place words: Upper Eagle Ridge, Mary Hill, Heritage Mountain.
- A guide and a homes page: Furry Creek.
- Two price bands: "Maple Ridge Homes Under $1.2M" and "Maple Ridge Homes Under $1M".
- The homepage and `/white-rock-realtor.html`. The homepage title is "South Surrey Realtor | White Rock & Langley | Jared Gibbons". The other page is "White Rock Realtor Jared Gibbons".

These are different pages a searcher could land on for one query. Google Search Console would show which query actually splits its clicks. Export Performance, Search results, with Query and Page, for the last 3 months, and look for queries whose clicks are split across two of the URLs in the CSV.

Suggested fix: for each neighbourhood, one page should own "homes for sale". The houses page and the condos page should say houses or condos in the title, not a second "homes for sale" title for the same place.

## 2. Near-duplicate text

Method: five-word shingles of the main text, MinHash to find the nearest page, then the exact overlap of those shingles as the percentage. Nav, footer, listing widget and review cards are not in the text.

`similarity.csv` has all 1,927 pages: url, closest match, similarity %, word count, template type.

| Similarity to the nearest other page | Pages |
| --- | --- |
| 90% or more | 16 |
| 80% or more | 125 |
| 60% or more | 223 |

Worst clusters (`similarity-clusters.csv`), fix these first:

1. **12 new-construction pages, 94.9%.** Cloverdale, North Vancouver, Mission, Ladner, Richmond, Port Moody, Sardis, Tsawwassen, Maple Ridge, New Westminster, Port Coquitlam, West Vancouver. One template with the city name swapped.
2. **Surrey and Vancouver presale pages, 90.2%.**
3. **Burnaby and Coquitlam presale pages, 90.0%.**
4. The rest of the 80% clusters are listing pages. They share the sold-listing template. Same-address pairs (Woodland Drive listed twice, North Bluff Road units) are the ones worth a look. The rest are the template, not copied articles.

## 3. Dead outbound links

6,334 unique http and https links. Each was requested with a normal browser-like GET, and redirects were followed up to six hops.

| Result | Links |
| --- | --- |
| OK (200 or a short redirect to 200) | 5,118 |
| Unverified (403, 429, connection closed, or LinkedIn 999) | 1,208 |
| Server error (502 or 520) | 6 |
| Timeout | 1 |
| Confirmed dead (404 or other 4xx that is not a block) | 0 |
| http links | 11 (4 of them work on https) |
| Chains of 3 or more redirects | 9 |

The six server errors, and a page that links them:

| Host | Status | Example page |
| --- | --- | --- |
| merrybright.ca | 502 | Langley holiday events post |
| roundhouse.ca | 520 | Downtown Vancouver condos, Yaletown, downtown-vw |
| surreyhistory.ca/placenames.html | 520 | Elgin Chantrell houses |
| building.ca (old cinema condo story) | 520 | Grandview Woodland |
| langleyheritage.ca mapping post | 520 | Otter district guide |
| fvmba.com | 502 | Vedder Mountain guide |

These failed from this network. A 520 can be the host or a block. Open each once before deleting it.

The timeout was `transit.land` (TransLink operator page), linked from several condo and townhome pages.

http links that already work on https: Discover Bridal Falls, Global Awards, White Rock Shopping, and the Lasso brochure on hyde-park. The other three http links did not answer on https from here.

No redirect loop. The longer chains are civic file downloads, a Microsoft login URL, Loblaws (which then returned 403), and a BC Ferries queue. Low.

Full rows are in `links.csv`.

## 4. Structured data

Method: every JSON-LD block on all 1,927 pages was parsed and checked against the required and recommended properties Google publishes for rich results. Google's Rich Results Test was not called. Schema.org types that Google does not use for a rich result were checked for empty required fields only.

| Type | Pages | Errors | What to know |
| --- | --- | --- | --- |
| BreadcrumbList | 1,926 | 0 | Names, positions and item URLs are present. The homepage correctly has none. |
| FAQPage | 1,526 | 0 | Every question has an answer. Google does not give FAQ rich results to this kind of site. Keep the markup. It is not a removal task. |
| BlogPosting | 202 | 0 errors, 1 warning on each | Missing `publisher.logo`. Headline, datePublished and author are present. |
| RealEstateAgent | homepage | 0 | Name, phone `+1-604-928-1361`, street `#201, 15272 Croydon Drive`. No diploma. |
| Offer | 201 | 0 | Price and CAD are set. Pages with no price do not emit an Offer. |
| VideoObject | 116 | 0 | Name, thumbnail and upload date are set. |
| RealEstateListing | 203 | 0 | Address is set. |
| Review | 0 | 0 | Not used. Reviews on the page stay verbatim, with initials. |
| AggregateRating | 0 | 0 | Not used. |

Listing offers point at the agent with `@id` only. That is a reference to the homepage entity, not a second agent with a missing name.

## 5. Accessibility

Method: Lighthouse 12 accessibility, which runs axe-core. One page of each template, mobile and desktop. Two runs did not finish because Chrome showed an interstitial: the Altus building page on mobile, and the mortgage calculator on desktop. The other form factor of each of those templates scored 100.

| Template | Mobile | Desktop | Violations |
| --- | --- | --- | --- |
| Homepage | 100 | 100 | none |
| Area (Surrey homes) | 100 | 100 | none |
| Guide (Hawthorne) | 100 | 100 | none |
| Listing (Meadow Place) | 100 | 100 | none |
| Building (Altus) | not completed | 100 | none on the completed run |
| Contact | 100 | 100 | none |
| Reviews | 100 | 100 | none |
| Map search | 100 | 100 | none |
| Mortgage calculator | 100 | not completed | none on the completed run |
| Blog (Langley acreage) | 100 | 100 | 64 serious name mismatches, not counted in the score |

The blog issue is axe rule `label-content-name-mismatch`. Selector `tbody > tr > td > a`. The sample link goes to `/zonings.html#zd-abbotsford-a1` with `aria-label="A1 Agricultural One Zone: what it allows"`, and the visible text is not part of that name. Lighthouse gives this rule weight 0, so the score stays 100. It is still a screen-reader bug: the name they hear is not the words on the screen. It showed on mobile and desktop, 64 links, on this blog template's zoning table.

## Files

| File | What it is |
| --- | --- |
| `cannibalization.csv` | 98 title pairs that can compete for one search |
| `similarity.csv` | all 1,927 pages, closest match and similarity % |
| `similarity-clusters.csv` | groups at 80% or above, worst first |
| `links.csv` | server errors, timeouts, http links, and long redirect chains |
| `schema.csv` | one row per schema type |
| `accessibility.csv` | one row per template and screen size |
