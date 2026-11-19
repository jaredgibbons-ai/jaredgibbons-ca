# Full SEO audit: jaredgibbons.ca

14 November 2026. Read-only. No form was submitted. No site file was edited. Nothing was deployed.

Repo at `4f3b7ae0`. Live hosts checked: `https://jaredgibbons.ca` and `https://www.jaredgibbons.ca`. Sitemap size this morning: **1,905 URLs** (the 13 November audit had 1,900).

## Executive summary

The Worker is the only origin that answered this session. All 1,905 sitemap URLs returned HTTP 200 from `server: cloudflare`, with one H1, a unique title, a unique meta description, and a canonical that matches the URL. Nothing in the crawl was `noindex`. Phone, email, and office match the business rules. There is no UBC Sauder diploma claim. Internal links reach every sitemap URL within three clicks. Lighthouse mobile Largest Contentful Paint is now about 1.7–2.7 seconds on the templates that were over 4 seconds yesterday, because the Google tag waits for a scroll or 3.5 seconds.

The site is not yet using the approved ranking sentence, and the review blocks do not follow the review rule.

Approved ranking wording, for every comparison below:

> #1 REALTOR® in South Surrey / White Rock by FVREB Medallion Club points (2025 and 2026 YTD). #1 of the Top 25 individuals at Royal LePage Little Oak Realty (2025). Top 1% of Fraser Valley REALTORS®.

| Severity | Open findings |
| --- | --- |
| Critical | 0 |
| High | 5 |
| Medium | 10 |
| Low | 7 |

The 13 November critical finding (the old MyRealPage server still answering the hostname) was **not reproduced**. Thirty-two repeat requests and the full sitemap crawl never returned `Apache` or a MyRealPage header.

## Top findings

1. **High. The ranking lines on the site are not the approved wording.** The footer on every page says “Top 1% of all REALTORS® in the Fraser Valley.” The homepage H2 says “South Surrey's #1 Ranked Realtor.” The homepage meta description and a stat say “10 straight years” in the Medallion Club. A stat says “11+” years as a REALTOR®. Award image alts add Royal LePage National Top 2%, Top 5%, and Top 35 Under 35. None of those sentences is the approved wording. “Top 1% of all REALTORS®” and “10 straight years” are the ones this brief called out. No H1 contains a ranking claim. The homepage H1 is “JARED GIBBONS South Surrey Realtor.”

2. **High. Homepage reviews show full first names and shortened quotes.** `src/data/home.ts` names Baljinder, Natalie, Atta, Maryam, Richard, Jessica, Marilyn, Savannah, and Kelly. The same reviews in `src/data/google-reviews.json` use initials (B.C., N.K., A.Y., and so on) and a longer text. Several homepage quotes stop at an ellipsis. The rule is initials only, the words verbatim, a date, and a true source.

3. **High. Most other review dates are missing or are a relative phrase that is now wrong.** `src/data/review-excerpts.json` has 78 excerpts. Initials are used. **70** have `when` equal to “Google review” and no calendar date. `/reviews.html` prints 87 written Google reviews with phrases such as “6 days ago” and “a week ago,” and says those times are as Google showed them on 1 November 2026. On 14 November that relative time is no longer the date of the review. The six featured reviews on that page do use initials, a calendar date, and “Google review.”

4. **High. The live Google reviews feed is empty.** `GET /api/reviews.json` is **204** with `cache-control: no-store`. The reviews page keeps the “Latest Google reviews” block hidden and falls through to a browser Places request only if a Maps key is present. This session did not see that block fill in on first paint.

5. **High. Map search shifts after load.** Lighthouse 12.8.2, simulated throttling: `/map-search.html` CLS **0.158** mobile and **0.154** desktop. That is over the 0.1 Core Web Vitals line. The map itself did load (the console logged 1,743 listings found). It also warned that `mapbox-gl.css` is missing.

## What is in good shape

- `https://jaredgibbons.ca/sitemap.xml` is HTTP 200, `application/xml`, 1,905 URLs, and `robots.txt` names it. `robots.txt` allows `/` and disallows `/internal/` and `/api/`.
- 1,905 distinct titles and 1,905 distinct descriptions. No sitemap URL is missing either. No title is over 60 characters. No description is over 160. Canonical path matches the URL on every sitemap URL. `lang="en-CA"` on every sitemap URL. No `hreflang` (one language).
- One H1 on every sitemap URL. No heading-level skip in the crawl. No `img` without an `alt` attribute. No alt matching `Photo N:`.
- Security headers on Worker HTML: `strict-transport-security: max-age=31536000`, `x-content-type-options: nosniff`, `referrer-policy: strict-origin-when-cross-origin`, `x-frame-options: SAMEORIGIN`, `content-security-policy: frame-ancestors 'self'; base-uri 'self'`, and a permissions policy. HTML cache is `public, max-age=0, must-revalidate`.
- `http://jaredgibbons.ca/` and `https://www.jaredgibbons.ca/` 301 once to the https apex. `/index.html` 301s to `/`. `/contact` 301s to `/contact.html`. `/contact.html/` 301s to `/contact.html` from Cloudflare (yesterday this hop came from Apache). `/404.html` and `/CONTACT.html` are real 404s.
- Office, phone, and email in the header, footer, and homepage `RealEstateAgent` JSON-LD: `604-928-1361`, `jaredgibbons@royallepage.ca`, `#201, 15272 Croydon Drive, Surrey`. That is the same office as Suite 201 – 15272 Croydon Dr. The map iframe shows `604-928-1361`, not the old `1 (604) 9281361` string.
- No `Review` or `AggregateRating` JSON-LD on the 1,905 pages. No Sauder or UBC diploma sentence in `src/` or in the rendered pages that were checked. UBC hits in the repo are place names.
- Click depth from `/` with every internal link counted: 265 pages at depth 1, 1,466 at depth 2, 173 at depth 3. **0** sitemap URLs are orphans. **0** are unreachable.
- 1,302 checked images (every non-photo image, every `og:image`, and 200 listing photos) returned HTTP 200 or 206. None 404’d.
- Mortgage calculator arithmetic for one case matches the code: $800,000, 20% down, 4.69%, 25 years, monthly payment **$3,610.14**, property transfer tax **$14,000**.
- `GET /api/instagram.json` is 200. `GET` on `/api/forms/contact` and `/api/forms/newsletter` is 405. No POST was sent.
- `wrangler.jsonc` `INDEXABLE` is `"true"`. Sitemap responses had no `x-robots-tag`.

## Findings

### High

**1. Ranking copy is not the approved wording**

| Where | What it says | File |
| --- | --- | --- |
| Footer, every page | “Top 1% of all REALTORS® in the Fraser Valley (Fraser Valley Real Estate Board)” | `src/components/Footer.astro` |
| Homepage meta description | “10 straight years in the FVREB Medallion Club” | `src/pages/index.astro` |
| Homepage H2 | “South Surrey's #1 Ranked Realtor” | `src/pages/index.astro` |
| Homepage stat | “10” / “Straight years, FVREB Medallion Club” | `src/pages/index.astro` |
| Homepage stat | “11+” / “Years as a REALTOR®, since 2015” | `src/pages/index.astro` |
| Homepage lede | “#1 in South Surrey and White Rock by Fraser Valley Real Estate Board Medallion Club points, 2025 and 2026 to date. #1 agent at Royal LePage Little Oak Realty in 2025.” | `src/pages/index.astro` |
| Award alts | “Royal LePage National Top 2% 2025”, “National Top 5%”, “Top 35 Under 35” | `src/data/home.ts` |
| Visible main text | “Top 1% of all” on 88 URLs, “10 straight years” on 198 URLs, “11+ years” on 206 URLs | `content-rule-violations.csv` |
| FAQ JSON-LD | 27 answers include one of those claims. Example: `/south-surrey-real-estate-agent-jared-gibbons-realtor.html`, question “Why work with Jared Gibbons for South Surrey & White Rock real estate?” | live JSON-LD |

The H2 is a subheading, so the placement rule (ranking in a subheading, never an H1) is met. The words are not the approved sentence. “Top 1% of all REALTORS®” adds “all,” which the brief says not to use. “10 straight years” is the example the brief gave of an unverified claim. “11+” is more than “REALTOR® since 2015” and is easy to get wrong if the licence date is in 2015.

Suggested fix: put the approved three sentences in subheadings or the stat list, and remove “of all,” “10 straight years,” and “11+.” Keep award badges only if Jared confirms each year. Do not put any of this in an H1.

**2. Homepage reviews use full first names and cut quotes**

Live “What clients say” cards, from `src/data/home.ts`:

- “A J”, 10 October 2026, a shortened first sentence of the A.J. review.
- “Baljinder”, 9 October 2026. The same text is “B.C.” in `src/data/google-reviews.json`.
- “Natalie”, “Atta”, “Maryam”, “Richard”, “Jessica”, “Marilyn”, “Savannah”, “Kelly”, several ending in “…”.

The Google file has the longer verbatim text and initials. The homepage file both names people and drops the rest of the sentence. Source is labeled “Google review,” and most cards have a calendar date. Richard’s card says only “June 2026.”

Suggested fix: use the initials and the full verbatim text already in `src/data/google-reviews.json`, with a real calendar date. If the date is not in hand, do not show that card. Do not invent a date or a name.

**3. Other review dates fail the date rule**

- `src/data/review-excerpts.json`: 70 of 78 items. `who` is initials (`D.V.`, `S.A.`, `R.`). `when` is “Google review” with no day. `ReviewCards.astro` prints these on interior pages.
- `src/data/google-reviews.json` and `/reviews.html`: initials and the label “Google review,” but `when` is “6 days ago,” “a week ago,” “3 weeks ago,” “a month ago.” The page says the times are as Google showed them on 1 November 2026. That note is honest and still not a date. “6 days ago” is now false.
- The six featured items in `src/data/reviews.json` do have initials, a calendar date, and “Google review.” Leave those.

Suggested fix: replace relative `when` values with the calendar date from the Google export, or drop the review until the date is known. Do the same for the 70 excerpts.

**4. `/api/reviews.json` is empty**

`GET` and `HEAD` return 204, `cache-control: no-store`. `src/worker/index.js` returns 204 when `env.REVIEWS` is missing or the bound worker does not return JSON (comment BL-03). The reviews page then tries Google Places in the browser. On first paint the “Latest Google reviews” section stayed hidden. If Places does run, `reviews.astro` prints `authorAttribution.displayName`, which is a full Google name, not initials.

Suggested fix: connect the reviews worker, or stop calling the endpoint. If Places stays as a fallback, show initials, not the display name, and do not add `AggregateRating` JSON-LD.

**5. Map search CLS is 0.16**

| Run | Performance | LCP | CLS | Best practices |
| --- | --- | --- | --- | --- |
| `/map-search.html` mobile | 0.92 | 1.9 s | 0.158 | 0.79 |
| `/map-search.html` desktop | 0.77 | 1.8 s | 0.154 | 0.78 |

Console, this session: Mapbox GL warned that `mapbox-gl.css` is not on the page. The IDX script then logged `totalFound: 1743`. There was no `OverQuotaMapError`. The MyRealPage `.less` files that this page requested (`mrp-bootstrap.less`, `common.less`, `idx-form.less`) returned 200.

Suggested fix: load the Mapbox CSS the widget expects, or reserve the iframe height before the map script runs, and remeasure CLS. The cookie failure (finding 8) is separate.

### Medium

**6. Sitemap `lastmod` is a build day, not the page’s date**

980 URLs are `2026-11-13`. 925 are `2026-11-14`. `src/data/lastmod.json` stores a content hash and one of those two days. A post such as `/blog.html/115-9072-fleetwood-way-599k-8919895` still has an older visible published date. Google discounts `lastmod` when it does not track real edits.

Suggested fix: leave `src/integrations/lastmod.mjs` so a date changes only when `<main>` changes. Do not stamp every URL with today on the next build. For posts, keep the visible `datePublished` and, if `lastmod` is set, use that published date unless the body actually changed.

**7. FAQ JSON-LD is on 1,505 commercial URLs, and two answers are broken sentences**

Google has limited FAQ rich results to government and health sites since 2023. The questions can stay as visible copy. Do not plan traffic from the rich result.

Two live answers are missing a verb: “Jared Gibbons to set up custom MLS listing alerts…” on

- `/south-surrey-real-estate-agent-jared-gibbons-realtor.html`
- `/morgan-crossing-homes-for-sale.html`

The empty question “What is this page?” is still in `src/data/local/south-surrey-real-estate-agent-jared-gibbons-realtor.json` with `"a": ""`, and `src/data/local/jared.json` has an empty “What is the jared.html page?”. Neither string is in the live HTML or JSON-LD today. Thirty-two local JSON files still contain “Can Jared show me homes in …”, including “Can Jared show me homes in Mortgage Calculator?”. That sentence is **not** in the rendered calculator page. It will come back if a template starts printing the `local/*.json` `faq` array as-is.

Suggested fix: repair the two live sentences. Delete the empty questions and the “show me homes in {page title}” questions from the JSON so a later template cannot emit them. Keep useful FAQ copy on the page. Do not add `AggregateRating`.

**8. Content-Security-Policy does not limit scripts. IDX pages fail the cookie check.**

Every Worker HTML response checked sends only `frame-ancestors 'self'; base-uri 'self'`. `src/worker/index.js` says a script allowlist is a separate step. Lighthouse best-practices is 0.79 on `/south-surrey-homes-for-sale.html` and 0.78–0.79 on `/map-search.html` because of third-party cookies from Google Ads (`AW-10817976788`). Homepage best-practices is 1.0 in Lighthouse because the tag file is delayed (see finding 9). A real browser still loads `gtag/js` about 3.5 seconds after load, and the Ads view-through request returns 200.

Suggested fix: when the script list is stable, add `script-src` in `src/worker/index.js`. Include Maps, Turnstile, MyRealPage, and YouTube or the widgets break. Load Google Ads only where a conversion is measured.

**9. Homepage images are still larger than the slot. LCP itself is in a better range.**

Lighthouse 12.8.2, simulated throttling, this session:

| URL | Form | Performance | LCP | CLS | TBT |
| --- | --- | --- | --- | --- | --- |
| `/` | mobile | 0.98 | 2.1 s | 0.012 | 0 ms |
| `/` | desktop | 0.80 | 2.2 s | 0.039 | 0 ms |
| listing Angela Avenue | mobile | 0.96 | 2.7 s | 0.012 | 0 ms |
| listing Angela Avenue | desktop | 0.77 | 2.6 s | 0 | 0 ms |
| `/south-surrey-homes-for-sale.html` | mobile | 0.99 | 1.7 s | 0.004 | 0 ms |
| `/yorkson-langley-guide.html` | mobile | 0.98 | 2.0 s | 0 | 0 ms |
| blog Fleetwood Way | mobile | 0.98 | 2.2 s | 0.025 | 0 ms |
| `/contact.html` | mobile | 0.99 | 1.8 s | 0.029 | 0 ms |
| `/mortgage-calculator.html` | mobile | 0.98 | 1.8 s | 0.005 | 0 ms |

Homepage LCP element is `img` of `/img/Jared.webp`. “Properly size images” still estimates **440 KiB** savings, led by `/listing-photos/eff40a8c4d163dea-960.webp` (111 KB transferred) and `/img/Jared.webp` (59 KB). The Google tag in `src/layouts/Base.astro` now loads on the first scroll, tap, or key, or 3.5 seconds after load. That is why Lighthouse no longer reports ~410 ms of tag blocking. Field INP and CrUX were not measured.

Suggested fix: point the homepage listing cards at a smaller derivative than `*-960.webp` (`src/worker/photos.js`). Keep width and height. Re-run Lighthouse on `/` and one listing. Do not remove the analytics tag.

**10. The mortgage calculator’s title promises a stress test the form does not run, and the form opens in an error state**

Title: “Mortgage Calculator BC | Monthly Payments & Stress Test.” The form computes payment, default-insurance premium, and property transfer tax. The stress test (contract rate + 2 points, or 5.25%, whichever is higher) is only explained in the copy under the form. On load, before anyone types, the empty price field is `aria-invalid` and the alert says “Enter a home price.”

The maths that the form does run is right for the case that was checked ($800,000, 20% down, 4.69%, 25 years → $3,610.14 and $14,000 property transfer tax). Labels are plain: “Home price ($),” “Down payment (%),” “Interest rate (%).” The note says the figure is an estimate, not a quote. The FAQ in `src/data/local/mortgage-calculator.json` says CMHC premiums range from 0.6% to 4.5%. `src/lib/mortgage.js` tops out at 4.0%. Those two should be the same number, taken from the current CMHC table.

Suggested fix: either add a clearly labeled “qualifying payment” row, or take “stress test” out of the title. Do not mark the price field invalid until the visitor leaves it empty. Align the FAQ premium range with `premiumPct()` after checking the CMHC page.

**11. Two listing offers have no price in JSON-LD**

- `/our-listings.html/listing.7-19696-telegraph-trail-langley-commercial-lease.107131830`
- `/our-listings.html/listing.c8075374-104-19232-enterprise-way-surrey-bc-v3s-6j9.107690830`

`Offer.price` is missing. A lease may have no sale price. An empty price is still invalid Offer markup. Breadcrumb last-item URLs matched the page on the rest of the crawl. No empty FAQ `acceptedAnswer` was emitted.

Suggested fix: omit `Offer` when there is no price, or set `price` only when the page shows one. Do not invent a price.

**12. One confirmed broken external link**

6,339 unique external URLs were requested. 5,214 returned a success or a redirect. 43 that rejected a `Range` request returned 200 on a normal GET. 573 timed out under parallel load and were **not** retested one by one (inconclusive). Seven hosts returned 502 or 520 from this network (Cloudflare or origin errors; not confirmed as broken for a person).

Confirmed 404:

`https://www2.gov.bc.ca/gov/content/housing-tenancy/strata-housing/strata-property-act`

Linked from:

- `/bc-duplex-half-duplex-buying-rules.html`
- `/coquitlam-55-plus-homes-for-sale.html`
- `/cottonwood-mr-55-plus-homes-for-sale.html`
- `/east-central-55-plus-homes-for-sale.html`

Suggested fix: point those four pages at the current BC strata legislation URL. Do not bulk-edit the 573 timeouts.

**13. Listing social images and the footer still depend on MyRealPage**

203 listing `og:image` URLs are on `iss-cdn.myrealpage.com`. They returned 200 this session, so shares work today. The image URL embeds a base64 payload that starts with `aHR0cDov` (`http://`). If that CDN goes away, Facebook and X cards for those listings break. The footer on every page still links “Real Estate Websites by myRealPage” to `https://myrealpage.com/`.

Suggested fix: serve listing `og:image` from `/listing-photos/` or `/img/`. Remove the vendor credit from `src/components/Footer.astro` unless the brokerage requires it.

**14. Organic visibility is still thin, and there are no building pages**

Semrush, Canada database, this session (10 API units; the keyword list then failed with “API UNITS BALANCE IS ZERO”):

| Metric | Value |
| --- | --- |
| Semrush rank | 348,452 |
| Organic keywords | 1,062 |
| Positions 1–3 | 13 |
| Positions 4–10 | 53 |
| Positions 11–20 | 117 |
| Estimated organic visits | 442 |
| Local pack keywords | 93 |
| AI overview keywords | 692 |
| Featured snippets | 0 |

These totals match the 13 November snapshot exactly, so they may still describe the pre-rebuild URL set. Which URL ranks for which keyword was **not** returned. The sitemap has neighbourhood and city/type pages. It does not have a condo-building profile section (a pattern competitors in this market publish).

Suggested fix: this is a content project, after the ranking sentences are corrected. Do not merge the price-band URLs. All 1,905 titles are already unique. A building template needs a scope from Jared.

**15. A few hosting and URL edges are untidy, and none formed a two-hop chain**

Recorded in `redirects.csv`. Notable:

- `https://JaredGibbons.ca/about.html` is **200** from the Worker. Canonical is lowercase. `src/worker/route.js` 301s `www` and `http` only.
- `?utm_source=` and `?cat=SOLD` return 200 and canonicalize to the clean URL. Tracking parameters are kept on purpose.
- Hyphenated blog slugs and `/marketing-plan.html` 301 in one hop.
- 54 `http://` links in page HTML (city and business sites, plus `http://jaredgibbons.ca`). Browsers do not block an `http` link the way they block an `http` script. They are still worth moving to `https` when the target has https.

### Low

**16. `/favicon.ico` and both manifest URLs 404.** `/favicon.png` and `/apple-touch-icon.png` return 200. Browsers still request `/favicon.ico`.

**17. Three sitemap URLs omit the robots meta:** `/`, `/fort-langley.html`, `/reviews.html`. They are still indexable. No `x-robots-tag`. The other 1,902 say `index, follow` (some add `max-image-preview:large`).

**18. No terms-of-use URL** in the sitemap. Privacy and the MLS reciprocity disclaimer are in the footer.

**19. Blog H1s run long.** 24 H1s are over 80 characters. One is over 100 (“Buyer Love Letters Are Dead…”). Titles themselves stay at or under 60. These are blog headlines, not ranking H1s.

**20. “5.0 · 95 Google reviews” is hardcoded** on the homepage (`src/pages/index.astro`) and on `/reviews.html` (“5.0 on Google from 95 reviews” next to “All 87 written Google reviews”). The 87 versus 95 split is explained as written comments versus all ratings. The number will go stale because it is not read from `/api/reviews.json`.

**21. Contact is the only sitemap URL under 300 words** (217). That is a form page, not a thin article. Fourteen URLs are under 700 words; most are sold-listing templates.

**22. Four linked URLs are not in the sitemap,** each expected to be `noindex`: `/search.html` (every page), `/subscribe-to-our-newsletter.html` (every page), `/photo-credits.html` (every page), `/testimonials.html` (234 pages). They were not in yesterday’s sitemap either.

Sold-listing pairs share up to about 0.75 of an 8-word shingle sample because the template text is the same. Addresses and titles differ. Do not merge them.

## Plain language on the tools

- **Mortgage calculator.** Labels and the estimate table are in everyday words. The mismatch is the title and the stress-test copy (finding 10), and the error state on an untouched form.
- **Homepage quiz** (“Where are you starting?”) uses First home, Moving up, Downsizing, Investing, Selling first, Just exploring. “Next” stays disabled until a choice. That part is clear. It was not submitted.
- **Map search.** The iframe loaded listings. The paragraph under it talks about municipal GIS parcel lines and also about drawing a search boundary. A buyer can read those as the same tool. The sentence “When you find an area you like, open my active listings” sends them to `/our-listings.html`, which is Jared’s own listings, not the map results.
- **South Surrey homes.** The page returned 200, LCP 1.7 s, and the listing-alert form has a visible label and a consent checkbox. The IDX frame’s console was checked on the map page, not line by line on this URL.

## Structured data

| Type | Sitemap URLs |
| --- | --- |
| BreadcrumbList | 1,904 (homepage is the one without) |
| FAQPage | 1,505 |
| RealEstateAgent | 407 |
| BlogPosting | 202 |
| RealEstateListing / Offer | 203 |
| VideoObject | 116 |
| Review or AggregateRating | 0 |

Homepage agent fields checked: telephone `+1-604-928-1361`, email `jaredgibbons@royallepage.ca`, street with `15272`. No `alumniOf`. No JSON-LD parse errors on the 1,905 pages.

## Security headers

Present on Worker responses: HSTS (`max-age=31536000`, no `includeSubDomains`, no `preload`), `nosniff`, `SAMEORIGIN`, referrer policy, permissions policy, CSP limited to `frame-ancestors` and `base-uri`. Not present: `script-src`, `object-src`, COOP, CORP. Hashed assets are cached for a year in `cacheFor()` in `src/worker/route.js`. This was read from response headers, not from a penetration test.

## Baseline: 13 November audit

Status for each item is also in `baseline-status.csv`.

| 13 Nov finding | This session |
| --- | --- |
| Critical. Two origins | **Not reproduced.** 1,905/1,905 Cloudflare. `/contact.html/` is a Worker 301. |
| High. Mobile LCP over 4 s | **Fixed on these runs.** Home 2.1 s, listing 2.7 s, map 1.9 s, South Surrey homes 1.7 s. Image byte waste remains. |
| High. 70 excerpts with no date | **Still open.** Plus homepage names and relative dates, which that audit did not flag. |
| High. Depth over 3, 3 orphans | **Wrong on a full link graph.** Max depth 3, 0 orphans. Their crawl had short HTML. |
| Medium. Empty FAQ answer | **Not in the live HTML.** Still an empty string in the source JSON. |
| Medium. FAQPage on 1,502 URLs | **Still open** (1,505). |
| Medium. Every lastmod is 2026-11-13 | **Partly changed.** Two build dates now. Still not the article date. |
| Medium. CSP without script-src | **Still open.** |
| Medium. Top 1% and Medallion claims | **Still open**, and now checked against the approved sentence. |
| Medium. Semrush and no building pages | **Still open.** Same Semrush totals. Keyword rows not available. |
| Low. Mixed-case host 200 | **Still open.** |
| Low. No manifest | **Still open.** `/favicon.ico` is an extra 404. |
| Low. No terms page | **Still open.** |
| 12 Nov Photo N alts, `/index.html` links, listing breadcrumb bug | **Not reproduced.** |
| 12 Nov Maps quota and `embeddable.less` | **Not reproduced** on the map page. |
| 12 Nov widget phone format | **Not reproduced.** |
| `/api/reviews.json` empty | **Still open** (204, was 404 on 12 Nov). |
| `INDEXABLE` true | **Still fixed.** |

## Not verified

- Field INP, CLS, and LCP (CrUX). Lighthouse here is lab data.
- Which Cloudflare route, if any, can still reach MyRealPage. It did not answer during this crawl.
- That each review quote matches the Google review word for word, beyond the homepage cards compared with `google-reviews.json`.
- That the FVREB and Royal LePage award badges are accurate for the years printed.
- A completed form in email or Keyvera. No POST was sent.
- The 573 external URLs that timed out.
- Places API reviews after scrolling `/reviews.html` (the block was hidden on first paint).
- Keyboard order on every template, and the bottom bar at 375 / 390 / 430.
- Mortgage results other than the one $800,000 case.
- Semrush keyword-to-URL rows.

## Method

- Sitemap downloaded 14 Nov 2026: 1,905 URLs.
- Full HTML crawl of those URLs (status, headers, title, description, H1, canonical, robots, JSON-LD, links, images, word count). A second pass stored every internal link so click depth is not capped at the first 250 anchors.
- Variant probes: http, www, mixed-case host, trailing slash, `/index.html`, extensionless, uppercase path, query strings, API GETs. No POSTs.
- Lighthouse 12.8.2 on 11 runs (8 mobile, 3 desktop), simulated throttling, headless Chrome.
- Browser pass: homepage, map search, mortgage calculator (one calculation), one sold listing, reviews, South Surrey homes. Console and network recorded. No form submitted.
- Image status: 1,302 URLs. External status: 6,339 URLs, then a normal GET (no `Range` header) for every non-timeout failure.
- Semrush `domain_rank`, Canada. `resource_organic` was refused for zero API units.
- Repo text scan of `src/` for the ranking phrases, Sauder, the wrong email, and FAQ templates.
