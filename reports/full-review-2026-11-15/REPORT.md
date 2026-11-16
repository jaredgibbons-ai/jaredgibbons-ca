# Full review: jaredgibbons.ca

16 November 2026. Read-only. No form was submitted. No site file was edited. Nothing was deployed.

Live site: `https://jaredgibbons.ca`, served by Cloudflare. Repo at `7e95ba51` (main, 15 November 2026). Sitemap this session: **1,926 URLs** (1,905 on 14 November; the 21 new URLs are condo-building pages).

Compared with the 14 November audit in the attached November 13 package. Each earlier finding is marked fixed, still open, or changed in the baseline section below.

## Plain-English summary

The site loads, the pages Google is asked to index all come back, and the phone, email and office are right. The calculator does the maths it claims to do. What still needs Jared's eye is mostly wording.

The ten problems that matter most:

1. **The ranking lines are still not the approved sentences.** The footer on every page says "Top 1% of all REALTORS®". Many pages, including About, still say "10 straight years" in the Medallion Club. The homepage heading that says he is #1 in South Surrey / White Rock now uses the approved sentence. Nothing in a main page title (the H1) makes a ranking claim.

2. **The newest reviews on the reviews page show first names and computer dates.** The older written reviews use initials, a normal date and "Google review", which is what was asked for. The live block under them prints dates like `2026-04-21T02:39:36Z` and replies such as "Thanks Kelly!!", "Savannah" and "Jovita".

3. **Two leased commercial listings show `$[***]/mth`.** That placeholder is in the Google description and, on the Telegraph Trail page, on the page itself.

4. **A security rule that is only being tested would break the map and the listing search if it were switched on as written.** It does not yet allow the MyRealPage scripts those pages need. Today it only reports the problem. It does not block anything.

5. **Photos are still heavier than the boxes they sit in.** The pages themselves are quick (the homepage settles in about 2.2 seconds on a simulated phone). Google's test still thinks several hundred kilobytes of photos could be smaller.

6. **On a phone, the map page can say the listings failed to load while they are still loading.** The code gives up after 10 seconds. The listing script was still starting at about 21 seconds in this test. On a wide screen the map did load, and it found 1,987 listings.

7. **"Open my active listings" does not open the map results.** It opens Jared's own listings. A buyer can reasonably think those are the homes they just saw on the map.

8. **Two outside links are dead.** A Chilliwack city page and a Surrey Schools page both return "page not found". The old BC strata link from the last audit is no longer used on the site.

9. **The sitemap tells Google that almost every page was updated on a build day**, not on the day the article was written. A February blog post is marked 14 November.

10. **The review counts do not match each other.** The reviews page says 87 written reviews and 94 on Google. The live Google feed says 95 in total and returns 94 records, 89 of them with text.

Nothing in this review was a broken site (no homepage outage, no wrong phone number, no diploma claim, no exposed password). There is no critical item.

| Severity | Open findings |
| --- | --- |
| Critical | 0 |
| High | 2 |
| Medium | 9 |
| Low | 7 |

## What is in good shape

- All **1,926** sitemap URLs returned HTTP 200 from `server: cloudflare`. One repeat of the old "two servers" problem did not appear. `http://`, `https://www` and a mixed-case host (`https://JaredGibbons.ca/about.html`) each redirect once to the https apex. `/index.html` redirects to `/`. `/contact` redirects to `/contact.html`. `/CONTACT.html` and `/404.html` are real 404s.
- Every sitemap URL has one H1, a title, a meta description and a canonical that matches the URL. Titles and descriptions are unique. No title over 60 characters (chart pages looked longer only because SVG drawings also use a `<title>` tag; the document title is normal, for example "Abbotsford Real Estate Market Stats | Prices & Trends", 57 characters). No description over 160 characters. `lang="en-CA"` everywhere. No hreflang, which is correct for a one-language site. No page is `noindex`.
- No heading skip in the crawl. No image missing an `alt` attribute. No alt matching `Photo N:`.
- Office, phone and email match the rules in the header, the footer and the homepage schema: `604-928-1361`, `jaredgibbons@royallepage.ca`, `#201, 15272 Croydon Drive`. No Suite 118. No UBC Sauder or Urban Land Economics diploma in the repo or on the rendered pages. No `alumniOf` in the JSON-LD.
- Homepage reviews now use initials, the full Google text and a calendar date (A.J., B.C., N.K., and the rest). The old full first names are gone. "11+" years as a REALTOR® is gone. The stat says "REALTOR® since 2015". "$500M+" is within the allowed sales line.
- The 70 review excerpts that had no date now have a calendar date. The reviews page no longer prints "6 days ago".
- `/api/reviews.json` is HTTP 200 with initials in the name field (it was an empty 204 on 14 November). `/api/instagram.json` is 200. GET on the form endpoints returns 405, which is what a POST-only form should do. No POST was sent.
- Click depth from the homepage, counting every internal link: 265 pages at depth 1, 1,466 at depth 2, 194 at depth 3. **0** sitemap URLs are orphans. **0** are unreachable.
- Listing share images are now on `jaredgibbons.ca`, not on the MyRealPage image host. The footer no longer carries the "Real Estate Websites by myRealPage" credit.
- The two listings that had an Offer in the schema with no price no longer emit an Offer. The mortgage calculator, before anyone types, no longer marks the price field as an error. For $800,000, 20% down, 4.69% and 25 years it shows a monthly payment of **$3,610.14**, property transfer tax of **$14,000**, and a qualifying payment at 6.69% of **$4,360.85**. The title's "stress test" is now a real row.
- Security headers on HTML: HSTS (`max-age=31536000`), `nosniff`, `SAMEORIGIN`, a referrer policy, a permissions policy, and the CSP noted above. `/favicon.ico` is 200. Debug paths that were probed (`/test.html`, `/debug.html`, `/admin`, `/.env`, `/wp-admin`, `/internal/`) are 404. The only values in the committed `.env.production` are public build flags and the Turnstile site key, which is meant to be in the page. No private key or lead-inbox address is in the repo.
- Layout: no sideways scroll on the homepage at 390, 768 and 1,280 pixels wide. The bottom action bar stays off the first screen until the visitor scrolls, then sits in the padding reserved for it. Contact fields have visible labels. The honeypot is hidden from view and from screen readers.

## Findings

### High

**1. Ranking copy is not the approved wording**

Approved wording, for every comparison below:

> #1 REALTOR® in South Surrey / White Rock by FVREB Medallion Club points (2025 and 2026 YTD). #1 of the Top 25 individuals at Royal LePage Little Oak Realty (2025). Top 1% of Fraser Valley REALTORS®.

| Where | What it says | File or URL |
| --- | --- | --- |
| Footer, every page | "Top 1% of all REALTORS® in the Fraser Valley (Fraser Valley Real Estate Board)" | `src/components/Footer.astro` |
| Homepage meta description | "10 straight years in the FVREB Medallion Club" | `src/pages/index.astro` |
| Homepage lede under the #1 heading | Approved second sentence, then "10 straight years…" and "Top 1% of all REALTORS®" | `src/pages/index.astro` |
| Homepage stat | "Top 1%" / "of all REALTORS® in the Fraser Valley" and "10" / "Straight years, FVREB Medallion Club" | `src/pages/index.astro` |
| About, and 196 other URLs | "has been in the Fraser Valley Real Estate Board Medallion Club for 10 straight years" | live `/about.html` and the crawl |
| Award alts | "Royal LePage National Top 2% 2025", "National Top 5%", "Top 35 Under 35" | `src/data/home.ts` |
| Fort Langley sign-off | "Top 1% of all REALTORS® in the Fraser Valley (FVREB)" | `src/pages/fort-langley.astro` |

The homepage H1 is "JARED GIBBONS South Surrey Realtor". The homepage H2 is the approved #1 sentence. The small line above the reviews link says "Top 1% of Fraser Valley REALTORS®", which matches the approved third sentence. "11+" is gone.

Suggested fix: use the three approved sentences, in a subheading or in body copy, and take out "of all" and "10 straight years". Keep an award image only when Jared has confirmed that year.

**2. The live review block shows computer dates and first names**

`GET /api/reviews.json` is now 200 (`fetchedAt` 2026-11-15T11:17:31Z, `averageRating` 5, `totalReviewCount` 95, 94 reviews, 89 with text, every `name` an initial such as `K.H.`). On `/reviews.html` the "Latest Google reviews" section rendered 24 of them.

Evidence from that block:

- The date line is the raw feed value, for example `K.H. 2026-04-21T02:39:36.956540Z · Google review`. All 94 feed dates are ISO timestamps. None is "21 April 2026".
- 66 reviews have a reply. 58 of those replies contain a capitalized name that is not "Jared" or "Thanks". Names in the feed replies include Kelly, Savannah and Jovita. The page shows "Reply from Jared: Thanks Kelly!!" beside the initials K.H.

The six featured reviews and the "All 87 written Google reviews" list do follow the rule: initials, a calendar date, and "Google review". Homepage cards match the full text in `src/data/google-reviews.json`.

The relative phrases ("6 days ago") are still stored in `google-reviews.json` as `when`, but the template prints `date` instead, so visitors do not see them.

Suggested fix: format the feed date before printing it. Do not print a reply that uses a client's first name, or swap that name for initials. Leave the static reviews alone.

### Medium

**3. The draft script policy would break the map and the listing search**

Enforced header, unchanged in substance from 14 November:

`content-security-policy: frame-ancestors 'self'; base-uri 'self'`

A report-only policy was added in `src/worker/index.js`. On `/map-search.html` the console recorded that these loads violate that policy and are only allowed because it is report-only:

- `https://idx.myrealpage.com/.../search-1450358.def/in.js`
- `https://res.myrealpage.com/wps/js/jquery-1.10.2.min.js`
- `https://res.myrealpage.com/wps/less/v2/listings/embeddable.less`

Lighthouse best-practices is 78 on map desktop, 79 on map mobile, 79 on `/south-surrey-homes-for-sale.html` and 79 on `/altus-white-rock-condos.html`, from third-party cookies (Google Ads). Homepage best-practices is 100 because the tag waits.

Suggested fix: add the MyRealPage hosts the console names before anyone copies the report-only policy into the enforcing header. Keep Google Ads on the pages where a conversion is actually measured.

**4. Sitemap `lastmod` is a build day**

| lastmod | URLs |
| --- | --- |
| 2026-11-14 | 1,061 |
| 2026-11-16 | 854 |
| 2026-11-15 | 10 |
| 2026-11-13 | 1 |

Every one of the 202 blog posts has a `datePublished` that is not that lastmod. Example: `/blog.html/115-9072-fleetwood-way-599k-8919895` was published 2026-02-10 and is lastmod 2026-11-14.

Suggested fix: change a date only when the visible page changes. For a post, keep the published date unless the article was edited.

**5. FAQ schema is on 1,525 ordinary pages**

1,525 sitemap URLs emit `FAQPage`. That is 20 more than on 14 November, in line with the new building pages. Google has not offered FAQ rich results to this kind of site since 2023. The questions can stay as text.

The two answers that were missing a verb now read "Ask Jared Gibbons to set up custom MLS listing alerts…". No empty question was in the live JSON-LD. The old "Can Jared show me homes in {page title}?" strings were not found in `src/`.

Suggested fix: keep the useful questions on the page. Remove the FAQPage block from pages that are not a real FAQ. Do not add `AggregateRating`.

**6. Photos are still larger than the slot**

Lighthouse 12.8.2, simulated throttling, this session. Contact and reviews did not finish: Chrome stopped those two runs with an interstitial. Those two pages were checked in the browser instead.

| URL | Form | Performance | LCP | CLS | Best practices |
| --- | --- | --- | --- | --- | --- |
| `/` | mobile | 97 | 2.2 s | 0 | 100 |
| `/` | desktop | 100 | 0.5 s | 0.004 | 100 |
| Meadow Place listing | mobile | 97 | 2.4 s | 0.001 | 100 |
| Meadow Place listing | desktop | 100 | 0.6 s | 0.003 | 100 |
| `/map-search.html` | mobile | 98 | 1.8 s | 0.004 | 79 |
| `/map-search.html` | desktop | 99 | 0.6 s | 0.051 | 78 |
| `/south-surrey-homes-for-sale.html` | mobile | 99 | 1.7 s | 0.004 | 79 |
| `/mortgage-calculator.html` | mobile | 90 | 1.4 s | 0 | 96 |
| `/altus-white-rock-condos.html` | mobile | 99 | 1.9 s | 0 | 79 |
| Fleetwood Way blog | mobile | 97 | 2.3 s | 0 | 100 |

"Properly size images" estimates about **584 KiB** on the listing (led by `*-960.webp` files), about **127 KiB** on the homepage mobile (led by `/img/Jared.webp`, 45 KiB of that) and about **290 KiB** on the homepage desktop. Map mobile reports one render-blocking stylesheet, `_astro/_slug_.C2OVl0qv.css`, at about 150 ms.

The map CLS that was 0.16 on 14 November is now under 0.1. The missing `mapbox-gl.css` warning is still in the console (finding 17).

Suggested fix: serve the size the slot uses. Re-run Lighthouse on `/` and one listing after that. Do not remove the analytics tag.

**7. Two lease listings publish `$[***]/mth`**

- `/our-listings.html/listing.7-19696-telegraph-trail-langley-commercial-lease.107131830`
  Description: "Leased Nov 2025 for $[***]/mth." The visible price line on the page is `$[***]/mth`.
- `/our-listings.html/listing.c8075374-104-19232-enterprise-way-surrey-bc-v3s-6j9.107690830`
  Description: "Leased Feb 2026 for $[***]/mth."

Neither page emits an `Offer` in JSON-LD, so the old "Offer with no price" error is fixed.

Suggested fix: drop the rent from the sentence, or print the real figure. Do not leave the mask on a public page.

**8. Phone listing cards give up too soon**

`src/components/IdxEmbed.astro` hides the listing box and shows "The live listings did not load" if nothing has rendered in 10 seconds. At a 390-pixel width that message was showing while the MyRealPage script was still loading (vendor logs at about 21 seconds). After the window was widened, the map iframe loaded (`iframe.idxmap`, about 1,185 by 702 pixels) and the console logged `totalFound: 1987`. There was no `OverQuotaMapError`.

Suggested fix: treat a slow script as still loading. Show the failure only on an error, or after a wait that matches the real load time.

**9. "My active listings" is Jared's own listings, and the map paragraph mixes two tools**

On `/map-search.html` the link text "my active listings" (and a nav-style "Active listings") points at `/our-listings.html`. The paragraph under the map also describes municipal GIS parcel lines and drawing a search boundary.

Suggested fix: label Jared's listings as his. Send a "homes from this map" link to the map. Keep the city-map explanation in its own paragraph.

**10. Two external links are confirmed 404s**

6,338 unique external URLs were requested with a one-byte range. 2,859 returned 200 and 2,295 returned 206. 707 returned 403 and 411 failed or timed out. A range request makes some servers answer 403 or 416, so those are **not** counted as broken. Two URLs returned 404, and a normal GET without a range confirmed both:

| URL | Linked from |
| --- | --- |
| `https://chilliwack.com/main/page.cfm?id=3171` | `/sardis-east-vedder-guide.html` |
| `https://surreyschools.ca/page/179729/xwepiteng-outdoor-land-based-learning-program-k-7` | `/blog.html/honoring-indigenous-culture-xwepiteng-elementary-in-south-surrey-8240648` |

The BC strata URL from the last audit (`www2.gov.bc.ca/.../strata-property-act`) still 404s if you open it, and it is no longer linked from this site.

Suggested fix: point the two pages at a current URL, or remove the link. Do not bulk-edit the 403s.

**11. Organic visibility is still thin. Building pages now exist.**

Semrush, Canada database, this session (10 API units):

| Metric | 16 Nov 2026 | 14 Nov 2026 |
| --- | --- | --- |
| Semrush rank | 338,929 | 348,452 |
| Organic keywords | 1,106 | 1,062 |
| Positions 1–3 | 13 | 13 |
| Positions 4–10 | 56 | 53 |
| Positions 11–20 | 123 | 117 |
| Estimated organic visits | 464 | 442 |
| Local pack keywords | 96 | 93 |
| AI overview keywords | 737 | 692 |
| Featured snippets | 0 | 0 |

Which URL ranks for which keyword was not pulled. The sitemap now includes 21 building pages that were not there on 14 November, for example `/altus-white-rock-condos.html` (HTTP 200, H1 "Altus Condos for Sale, White Rock", about 682 words). Draft banners in the source JSON ("Draft for Jared's approval") are stripped on the live site by `isDraftNote` in `src/lib/preview.ts` and were not in the live HTML.

Suggested fix: this is a content project after the ranking sentences are corrected. The building pages close the gap the last audit named. They have not moved the top-3 count.

### Low

**12. The web manifest URLs 404.** `/site.webmanifest` and `/manifest.webmanifest` are 404. `/favicon.ico` is now 200, as are `/favicon.png` and `/apple-touch-icon.png`.

**13. There is no terms page.** `/terms.html` is 404. `/privacy.html` is 200 and is linked from the footer, with the MLS disclaimer.

**14. Three sitemap URLs omit the robots meta:** `/`, `/fort-langley.html`, `/reviews.html`. They are indexable. No `x-robots-tag`. The other pages say `index, follow` (blog posts add `max-image-preview:large`).

**15. Blog H1s run long.** 24 H1s are over 80 characters. One is over 100. Title tags stay at or under 60. These are article headlines, not ranking claims.

**16. Fifty-three `http://` links** remain (city and business sites). They are not mixed-content scripts. Examples: `http://www.clearbrookvillage.info/`, `http://www.abbotsfordairport.ca/`.

**17. Mapbox CSS is still missing, and the shift is now small.** The console warning is the same one as on 14 November. CLS is 0.004 mobile and 0.051 desktop, both under the 0.1 line.

**18. The review counts disagree.** `/reviews.html` says "All 87 written Google reviews" and "5.0 on Google from 94 reviews". The feed's `totalReviewCount` is 95, with 94 records and 89 written. The code comment says one Google review is fake and is not used. The live summary line says "5.0 average on Google" and does not print 95.

## Forms, calculators and calls

No form was submitted. No lead was sent.

- **Contact** (`/contact.html`). Labels: Your email, Your name, Your phone number, Subject, Message. Submit button reads SUBMIT. Turnstile is on the form. The honeypot is off-screen and `aria-hidden`. Office line on the page: "#201, 15272 Croydon Drive". Mailto links use `jaredgibbons@royallepage.ca`. The contact schema does not require a consent checkbox (a person is writing to Jared). Listing alerts and the newsletter do require an unticked consent box; that checkbox is in `ListingAlert.astro` and `Newsletter.astro`.
- **Mortgage calculator.** Untouched form says "Enter a home price to see the estimate" and does not mark the field invalid. The case above matches `src/lib/mortgage.js`. The example rate is 4.69% 5-year fixed, labelled as of 12 November 2026 (RateHub). The FAQ now says CMHC premiums run from 0.6% to 4.0%, and mentions 4.5% only for a non-traditional down payment the calculator does not model.
- **Homepage quiz.** The "Sent. Thank you." heading is in the DOM and hidden until a successful send (`parent` is `hidden`). It was not submitted.
- **Map.** Desktop frame loaded and reported 1,987 listings. Phone cards hit the 10-second failure in finding 8. Phone number in the widget text is `604-928-1361`.
- **Bottom bar.** Call, text, Find a Home, Home Value. It stays translated off-screen until the visitor has scrolled, then it is fixed in the 3.25rem of padding the page reserves. At 390, 768 and 1,280 pixels the homepage did not scroll sideways.

## Structured data

| Type | Sitemap URLs |
| --- | --- |
| BreadcrumbList | 1,925 (homepage is the one without) |
| FAQPage | 1,525 |
| BlogPosting | 202 |
| RealEstateListing | 203 |
| WebPage | 155 |
| RealEstateAgent / Person / WebSite | homepage only |
| Review or AggregateRating | 0 |

`RealEstateAgent` was on 407 URLs on 14 November and is on the homepage only now. The homepage fields are telephone `+1-604-928-1361`, email `jaredgibbons@royallepage.ca`, street `#201, 15272 Croydon Drive`. No `alumniOf`. No JSON-LD parse error on the 1,926 pages. That reduction looks deliberate; it is not listed as a defect.

## Security

Present on Worker HTML: HSTS without `includeSubDomains` or `preload`, `nosniff`, `SAMEORIGIN`, referrer policy, permissions policy, CSP as in finding 3. Not present as enforcing rules: `script-src`, `object-src`, COOP, CORP. This was read from response headers, not from a penetration test.

Probed and 404 from Cloudflare: `/test.html`, `/debug.html`, `/admin`, `/.env`, `/wp-admin`, `/internal/`, `/internal/blog/`. `INDEXABLE` in `wrangler.jsonc` is `"true"`. No sitemap URL sent `x-robots-tag`.

## Baseline: 14 November audit

The attached package is the 13 November crawl, and its `REPORT.md` is the 14 November retest. Status below is against that 14 November report.

| 14 Nov finding | This session |
| --- | --- |
| Critical. Two origins | **Still not reproduced.** 1,926/1,926 Cloudflare. |
| High. Ranking wording | **Still open.** H2 and the hero "Top 1% of Fraser Valley" line now match. Footer, "10 straight years" and "of all" do not. |
| High. Homepage reviews use full names and cut quotes | **Fixed.** Initials, full text, calendar dates. Checked against `google-reviews.json`. |
| High. Review dates missing or relative | **Fixed on the static pages.** Excerpts have dates. The reviews page does not print "6 days ago". **New:** the live feed block prints ISO timestamps. |
| High. `/api/reviews.json` empty (204) | **Fixed.** HTTP 200, initials, 94 reviews. Replies in that feed reintroduce first names (finding 2). |
| High. Map CLS 0.16 | **Fixed on these runs.** Mobile 0.004, desktop 0.051. Mapbox CSS warning remains. |
| Medium. lastmod is a build day | **Still open.** Dates moved to 14 and 16 November. Still not the article date. |
| Medium. FAQPage on commercial URLs, two broken answers | **Schema still open** (1,525). **Broken answers fixed.** |
| Medium. CSP without script-src | **Still open**, and the new report-only list leaves out MyRealPage. |
| Medium. Homepage images oversized, LCP improved | **Still open** on bytes. LCP stayed in the same range (home mobile 2.2 s, was 2.1 s). |
| Medium. Stress test promised, form opened in an error state | **Fixed.** Untouched form is not in error. The stress-test row calculates. |
| Medium. Two Offers with no price | **Fixed** (no Offer). **New:** `$[***]/mth` on those two listings. |
| Medium. BC strata link 404 | **Fixed as a site link.** The URL still 404s. It is not in the crawl's external links or in `src/`. |
| Medium. Listing social images and footer depend on MyRealPage | **Fixed.** 0 of 393 `og:image` URLs are on `myrealpage.com`. Footer credit is gone. IDX search scripts still load from MyRealPage, which is expected. |
| Medium. Thin organic visibility, no building pages | **Visibility still thin** (13 keywords in positions 1–3). **Building pages added** (21 URLs). |
| Low. Mixed-case host returns 200 | **Fixed.** `https://JaredGibbons.ca/about.html` is a 301 to the lowercase host. |
| Low. No manifest, favicon.ico 404 | **Manifest still 404. favicon.ico is 200.** |
| Low. No terms page | **Still open.** |
| Low. Three pages omit robots meta | **Still open.** |
| Low. Long blog H1s | **Still open.** 24 H1s over 80 characters. |
| Low. Hardcoded "5.0 · 95 Google reviews" | **Changed, still inconsistent.** Homepage and reviews say 94. The feed says 95. The written list says 87. |
| Low. Contact under 300 words | **Still true** (215 words). It is a form page. |
| Low. Four linked URLs not in the sitemap | **Still true, and still noindex:** `/search.html`, `/subscribe-to-our-newsletter.html`, `/photo-credits.html`, `/testimonials.html`. |
| 13 Nov. Click depth over 3 and 3 orphans | **Still not reproduced.** Max depth 3, 0 orphans. |
| 13 Nov. Empty FAQ "What is this page?" | **Still not in the live HTML**, and the empty answer was not found in `src/` this session. |
| 12 Nov. Photo N alts, `/index.html` links, Maps quota, wrong widget phone | **Still not reproduced.** |

## Not verified

- Field Core Web Vitals (CrUX). The scores above are lab data.
- Lighthouse on `/contact.html` and `/reviews.html`. Chrome blocked those two runs with an interstitial. Both pages were opened in the browser and inspected.
- That every external URL which returned 403 or timed out is healthy for a person. Only non-200 results that survived a normal GET are called broken.
- That each of the 87 static reviews matches Google word for word beyond the nine homepage cards compared with `google-reviews.json`.
- That each award badge is accurate for the year printed.
- A completed form in email or Keyvera. No POST was sent.
- Keyboard order on every template. Skip-to-content is present. Contact and calculator labels were checked. Lighthouse accessibility was 100 on every run that finished.

## Method

- Sitemap downloaded 16 November 2026: 1,926 URLs, `application/xml`, HTTP 200, named from `robots.txt` (`Allow: /`, `Disallow: /internal/` and `/api/`).
- Full HTML crawl of those URLs (status, headers, title, description, H1, canonical, robots, JSON-LD, links, images, word count, the ranking phrases). Click depth uses every internal link.
- Variant probes: http, www, mixed-case host, trailing slash, `/index.html`, uppercase path, query-less API GETs, a handful of debug paths. No POSTs.
- Lighthouse 12.8.2 on 10 completed runs (8 mobile, 2 of those failed, 4 desktop including home, map and one listing), simulated throttling, headless Chrome.
- Browser pass at 390, 768 and 1,280 pixels: homepage, contact, mortgage calculator (one calculation), map search, reviews. Console recorded on the map page. No form submitted.
- External status: 6,338 URLs. The two 404s were confirmed with a normal GET. Image spot check: the sampled `og:image` URLs that answered returned 200; a one-byte range against listing photos was inconclusive, and a normal GET of one listing photo and one blog share image returned 200 (`image/webp`, `image/jpeg`).
- Semrush `domain_rank`, Canada.
- Repo scan of `src/` for Sauder, the wrong office, the ranking phrases, review names and secrets.
