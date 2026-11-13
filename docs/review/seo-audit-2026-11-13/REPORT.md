# SEO audit: jaredgibbons.ca

13 November 2026. Read-only. No forms were submitted with real personal data, no repo files were edited, and nothing was deployed.

The audit used the live site and the repo at `749277a0`. A worker-only crawl of the 1,900 sitemap URLs was taken once Cloudflare answered. A second, unfiltered crawl is cited only as evidence that the legacy origin still answers. Body-level counts from the worker snapshot (word count, H1 on short responses) moved again on recheck, so those figures are labelled as a snapshot.

## Executive summary

On the Cloudflare Worker, the on-page basics are in good shape: 1,900 sitemap URLs returned 200, each title and each meta description is unique, canonicals match the URL, and a recheck of the pages that had no H1 in the snapshot found an H1 on 81 of 83. Phone, email, and office address agree. There is no UBC Sauder diploma claim in the repo or in the snapshot text. `/index.html` now 301s to `/`.

The site is not safe to treat as one site. The same hostname is sometimes answered by the new Worker and sometimes by the legacy MyRealPage server (`Apache/2.4.46`, MyRealPage headers). Those two answers disagree: titles, byte size, and even status. Until every request goes through the Worker, Google can index the old site, a 404, or the new page for the same URL.

## Top 10

1. **Critical. Two origins answer jaredgibbons.ca.** DNS points only at Cloudflare, but some responses are the legacy Apache/MyRealPage app and some are the Worker. Verified examples: `https://jaredgibbons.ca/south-surrey-homes-for-sale.html` once returned Apache, 333KB, title “Homes for Sale in South Surrey, BC | New Listings Daily”; later requests were the Worker at about 123KB. `https://jaredgibbons.ca/contact.html/` returned `301` from `Apache/2.4.46`. One `POST /api/forms/newsletter` returned the MyRealPage 404 “the url you requested doesn't exist”; the next nine returned Worker `422`. An unfiltered crawl recorded 847 sitemap URLs as HTTP 404 with the legacy title “Page Not Found”; an immediate refetch of `https://jaredgibbons.ca/abbotsford-east-condos-townhomes-for-sale.html` was Worker `200`. A homepage fetch during the same window returned a 341KB page with no `<main>` and 31 images missing width/height; five later fetches were the Worker homepage at 169,120 bytes, with `<main>`, one H1, and dimensions on all 114 images. The Worker in `src/worker/index.js` never emits `server: Apache`. The split is in the Cloudflare route or origin, which this audit could not open. **Not verified:** the dashboard rule that still sends traffic to MyRealPage.

2. **High. Mobile Largest Contentful Paint is still over 4 seconds on the pages that matter.** Lighthouse 12, mobile, simulated throttling, this session: homepage LCP **4.20s** (performance 0.73), a listing page **5.60s** (0.77), map search **5.48s** (0.70). CLS is about 0 to 0.03. Homepage third-party JavaScript blocked the main thread for **410ms**, almost all Google Tag Manager (354KB transferred). “Properly size images” estimated **440KB** savings, led by `/listing-photos/*-960.webp` and `/img/Jared.webp`. Unused JavaScript was about **135KB** on every successful run. TTFB was 50–160ms, so the wait is after the first byte. South Surrey homes (`/south-surrey-homes-for-sale.html`) did not complete: Chrome reported `CHROME_INTERSTITIAL_ERROR`. **Not verified:** field INP, and a clean Lighthouse run of the South Surrey homes URL.

3. **High. Review excerpts break the site rule on dates.** `src/data/review-excerpts.json` has 78 excerpts. Initials are used (D.V., S.A., and single initials such as R.). **70 have no calendar date**; `when` is only “Google review”. Eight include a date. `GET /api/reviews.json` is **204** with `cache-control: no-store`, so the live Google block stays empty. The footer and homepage JSON-LD do not emit `Review` or `AggregateRating` (confirmed on the 1,900-page snapshot). **Not verified:** that each quote is verbatim against the Google review it cites.

4. **High. 151 sitemap URLs sit more than three clicks from the homepage in the snapshot link graph, and 3 have no internal links at all.** Depth from `/` using internal links in that HTML: 265 at depth 1, 1,242 at depth 2, 241 at depth 3, then 58 / 60 / 23 / 6 / 1 at depths 4 through 8. Unlinked: `/bc-landlord-tenant-resources.html`, `/blog.html/bchl-playoffs-surrey-eagles-face-crucial-road-games-in-penticton-8243016`, `/blog.html/cleanbc-rebates-in-bc-save-thousands-on-windows-heating-home-upgrades-8925479`. Four URLs are linked but not in the sitemap, and each is `noindex, follow`: `/search.html`, `/testimonials.html`, `/photo-credits.html`, `/subscribe-to-our-newsletter.html`. **Caveat:** some snapshot HTML was short (see thin-content.csv). Short pages omit links, so depth is an upper bound, not a final count.

5. **Medium. FAQ rich results should not be part of the plan, and one FAQ answer is empty.** 1,502 sitemap URLs emit `FAQPage`. Google has restricted FAQ rich results to well-known government and health sites since 2023, so this markup will not show questions under the listing for a realtor. Rechecked live: `/south-surrey-real-estate-agent-jared-gibbons-realtor.html` has nine FAQ questions and an empty `acceptedAnswer` on “What is this page?”. Breadcrumb JSON-LD on the worker snapshot had no last-item URL mismatches. The 12 Nov bug (listing breadcrumbs pointing at `/our-listings.html`) was not reproduced. Six other URLs lacked `BreadcrumbList` in the snapshot; a recheck of three (`steelhead.html`, `sardis-houses-for-sale.html`, `english-bluff-guide.html`) found the list present.

6. **Medium. Every sitemap `<lastmod>` is 2026-11-13.** Confirmed on the live sitemap (1,900 URLs, one date) and in `src/data/lastmod.json`. `src/integrations/lastmod.mjs` sets the date to the build day when the `<main>` hash changes, and this manifest was written on launch day, so the date is internally consistent and useless as a freshness signal. A checked post, `/blog.html/115-9072-fleetwood-way-599k-8919895`, has `datePublished` **2026-02-10**, which the sitemap does not reflect.

7. **Medium. Security headers are present but the content security policy does not limit scripts.** Every Worker HTML response checked sent `strict-transport-security: max-age=31536000`, `x-content-type-options: nosniff`, `referrer-policy: strict-origin-when-cross-origin`, `x-frame-options: SAMEORIGIN`, and `content-security-policy: frame-ancestors 'self'; base-uri 'self'`. There is no `script-src`. `src/worker/index.js` says a script allowlist is a separate step. Lighthouse best-practices was **0.79** on every successful run because of a Google Ads third-party cookie (`googleads.g.doubleclick.net` view-through conversion) and that same Issues-panel cookie finding. HTML is Brotli-compressed. Hashed assets are cached a year in `cacheFor()` in `src/worker/route.js`. The one short-cache third party Lighthouse named was `static.cloudflareinsights.com/beacon.min.js` (1 day).

8. **Medium. The footer ranks Jared on every page, and that claim was not checked against the board.** `src/components/Footer.astro` prints “Top 1% of all REALTORS® in the Fraser Valley (Fraser Valley Real Estate Board)” on every page. It is not an H1. The homepage meta description says “10 straight years in the FVREB Medallion Club.” **Not verified** against FVREB. No H1 in the snapshot contained a realtor ranking claim. A blog H1 “Crescent Beach Named One of Canada's Top 10 Beaches” is about the beach, not the agent.

9. **Medium. Semrush still shows a thin top of the market, and the keyword list could not be pulled.** Canada database, this session: Semrush rank 348,452, **1,062** organic keywords, **442** estimated organic visits, **13** keywords in positions 1–3, **53** in 4–10, **117** in 11–20, **93** local-pack keywords, **692** AI-overview keywords, **0** featured snippets. The next calls failed with `API UNITS BALANCE IS ZERO`, so which URLs rank, and which competitors share those keywords, were **not verified**. The figures can still describe the pre-rebuild URL set. The sitemap has no condo-building profile section. `realestatewhiterock.com` (from a web search for the same market, not a full crawl) advertises building profiles and a live inventory count. That gap is a content project, not a broken tag.

10. **Low. A few URL variants are untidy, and none of the checked ones formed a two-hop chain.** Mixed-case `https://JaredGibbons.ca/about.html` returns **200** from the Worker with canonical `https://jaredgibbons.ca/about.html`. `?utm_source=` and `?cat=SOLD` return 200 and canonicalize to the clean URL (Worker behaviour in `src/worker/route.js`: tracking parameters are kept). `https://jaredgibbons.ca/CONTACT.html` is a real 404. `https://jaredgibbons.ca/404.html` is a real 404, not a soft 200. `http://` and `www` 301 once to the https apex. `/index.html` 301s to `/`. Archive `rules.json` has 84 redirects and **no** target that is itself a redirect. Three archive conflicts are served 404 on purpose (`OI-10`).

## What is in good shape on the Worker

- Sitemap `https://jaredgibbons.ca/sitemap.xml` is HTTP 200, `application/xml`, 1,900 URLs, and it is named in `robots.txt`. `robots.txt` allows `/` and disallows `/internal/` and `/api/`. No sitemap URL in the worker-only crawl was `noindex`. `x-robots-tag` was absent, which matches `INDEXABLE: "true"` in `wrangler.jsonc`. The 12 Nov risk of a repo `"false"` shipping `noindex` is not the current file.
- 1,900 distinct titles and 1,900 distinct meta descriptions. None missing. One title is 61 characters (`/south-surrey-white-rock-55-plus-condos-for-sale.html`). Descriptions in the meta-issues file are inside the site’s 158-character fit. Canonical on every sitemap URL equals that URL.
- `lang="en-CA"` on the Worker homepage. Favicon `/favicon.png` and `/apple-touch-icon.png` return 200. There is no web app manifest (`/site.webmanifest` and `/manifest.webmanifest` are 404). No `hreflang`.
- Eight full Abbotsford condo URLs overlapped at most **0.16** on 8-word shingles. They are not copies. Titles already separate them. Merging them would throw away that work.
- Listing photo alts on a sampled listing (`511 Similkameen Avenue`) describe the picture (“Street view of the house…”, “Front of the house with covered porch…”). The snapshot had **0** alts matching `Photo N:`. The 12 Nov generic-alt finding was not reproduced.
- No image in the snapshot lacked an `alt` attribute. Empty `alt` (decorative) totalled 31,224. That is not a missing-alt bug.
- Forms, with `Origin: https://jaredgibbons.ca` and a browser user agent, and no real lead: missing `Origin` is `403 origin_not_allowed`; empty contact JSON is `422` with field errors; a bad email is `422`; a complete fake body with no Turnstile token is `403 captcha_required` and returns no id. The same empty-body `422` was confirmed for home-evaluation, property-check, quiz, listing-alert, and presale-vip. Unknown kinds return `404 unknown_form`. `GET` is `405`. Nothing with an id was returned. **Not verified:** the success screen in the browser, or that a real captcha-backed post arrives in email or Keyvera.
- Copyright in `Footer.astro` is 2026. Privacy policy is linked. The MLS reciprocity disclaimer is in the footer (GVR, FVREB, CADREB). No terms-of-use URL is in the sitemap.
- Office line in the footer and in homepage `RealEstateAgent` JSON-LD: phone `604-928-1361` / `+1-604-928-1361`, email `jaredgibbons@royallepage.ca`, `#201, 15272 Croydon Drive, Surrey, BC, V3Z 0Z5`. That is the same office as “Suite 201 - 15272 Croydon Dr, Surrey”; the punctuation differs. No contradictory phone or email was found in the checks that were run.
- `GET /api/instagram.json` returned 200 with posts for `jaredgibbonsrealestate`. The 12 Nov 404 was not reproduced. A `HEAD` during the first pass was inconsistent with `GET`; treat HEAD as unreliable for that route.

## Findings

| Issue | Severity | Affected URL count and examples | Why it matters | Exact fix |
| --- | --- | --- | --- | --- |
| Legacy MyRealPage origin still answers the hostname | Critical | Seen on at least 4 request shapes. Examples: `/south-surrey-homes-for-sale.html`, `/contact.html/`, `POST /api/forms/newsletter`, and 847 sitemap URLs in the unfiltered crawl | Google and users can get the old title, a legacy 404, or the new page for one URL. Canonicals on the new site do not control the old response | In Cloudflare, send every `jaredgibbons.ca` route through the Worker in `src/worker/index.js` and remove the MyRealPage origin. Retest the four examples until `server` is `cloudflare` and the security headers are present. Dashboard, not a repo file. **Not verified** which rule still points at Apache |
| Mobile LCP over 4s on home, listing, and map search | High | 3 of 7 completed Lighthouse URLs. Home 4.20s, listing 5.60s, `/map-search.html` 5.48s. Guide, blog, contact, and mortgage calculator were 2.18–3.93s | LCP over 4s is a poor Core Web Vital on the pages that start a search | Defer `gtag` in `src/layouts/Base.astro` until after first paint or on interaction. Serve a smaller derivative than `*-960.webp` for the homepage strip (`src/worker/photos.js`). The South Surrey homes run hit a Chrome interstitial and is **not verified** |
| Review excerpts missing a date; Google feed empty | High | 70 of 78 items in `src/data/review-excerpts.json`. `/api/reviews.json` is 204 | The site rule asks for initials, the verbatim quote, a date, and a true source. A source label without a date does not meet it | Add the Google review date to each `when`, or stop using excerpts that have no date. Connecting `workers/reviews` (comment BL-03 in `src/worker/index.js`) is what turns the 204 into a feed. **Not verified:** verbatim match to Google |
| Click depth over 3, plus 3 orphans | High | 151 URLs at depth 4–8 in the snapshot graph. Orphans listed above | Pages Google reaches only through a long chain, or not at all, get less internal equity | Link the three orphans from the relevant hub (`src/components/Footer.astro` popular list, or the parent guide). Recheck depth after a stable crawl; this graph undercounts links on short snapshot HTML |
| FAQPage on commercial pages, one empty answer | Medium | 1,502 URLs with `FAQPage`. One empty answer on `/south-surrey-real-estate-agent-jared-gibbons-realtor.html`, question “What is this page?” | Empty answers are invalid FAQ markup. The rest will not earn FAQ rich results | Fill or delete that question in the page’s FAQ source. Keep FAQ copy on the page. Do not plan rich-result traffic from `FAQPage` in `src/components/GenericPage.astro` |
| Sitemap lastmod is one date for every URL | Medium | 1,900 / 1,900, date 2026-11-13. Blog `datePublished` example 2026-02-10 | Google discounts lastmod when every URL shares a build date | Leave `src/integrations/lastmod.mjs` as it is for future edits. Do not rewrite all dates to “today” again. For posts, the visible date is already `article:published_time` |
| CSP has no script allowlist; Ads cookie trips best-practices | Medium | All Worker responses checked. Lighthouse best-practices 0.79 on 7 URLs | A policy of only `frame-ancestors` and `base-uri` does not limit injected scripts. The Ads cookie is a best-practices failure, not a ranking failure | When the script inventory is stable, extend the policy in `src/worker/index.js` (`SECURITY`). Load Google Ads only where a conversion is needed |
| “Top 1%” and “Medallion Club” claims | Medium | Footer on every page (`src/components/Footer.astro`). Homepage meta description | Unverified ranking language is a trust problem even when it is not in the H1 | Keep the sentence only with the FVREB source and the period it covers. This audit did **not** verify the award |
| No building-level pages; Semrush top-3 is 13 keywords | Medium | Sitemap has no building-profile pattern. Semrush Canada: 13 keywords in positions 1–3, 442 visits | Competitors in this market publish building pages and live inventory counts. Keyword-to-URL mapping was **not verified** (Semrush units ran out) | A building template is a content project, after the origin split is closed |
| Mixed-case host returns 200 | Low | `https://JaredGibbons.ca/about.html` verified. Canonical is lowercase | A second host form, even if Google usually lowercases it | 301 any non-lowercase host to `https://jaredgibbons.ca` in `src/worker/route.js` (the www and http branches are already there) |
| No web manifest | Low | `/site.webmanifest` and `/manifest.webmanifest` are 404. Icons 200 | Minor. Not a ranking requirement | Optional. Icons already exist |
| No terms-of-use URL | Low | Not in the 1,900 sitemap URLs. Privacy and the MLS disclaimer are present | The brief asked for terms as well as privacy | Add a terms page only if counsel wants one. Privacy and the board disclaimer are already in the footer |
| Three archive URLs with conflicting redirect and 404 | Low | `/esplanade-grande-waterstone-condo-for-sale/`, and two old `/recip.html/listing…` paths in `src/worker/rules.json` | The Worker 404s them on purpose so a bad redirect is not guessed | Leave the 404 unless Jared picks one target. Not a live loop |

## Quick wins

These are small once the origin is known. Closing the origin split itself is a Cloudflare change, not a one-line repo edit, and it is the one that matters.

- Point the whole zone at the Worker and retest the four split examples.
- Add a host-case 301 next to the www rule in `src/worker/route.js`.
- Delete or fill the empty FAQ question “What is this page?”.
- Put a real date on the 70 undated excerpts in `src/data/review-excerpts.json`, or remove them.
- Link the three orphan URLs from one hub.
- Defer the Google tag in `src/layouts/Base.astro` so it is not on the critical path.

## Bigger projects

- Image derivatives for homepage and listing heroes (`src/worker/photos.js`), then rerun Lighthouse on `/`, one listing, and `/map-search.html`.
- Decide whether map search should load Google Maps and the IDX embed on first paint. The 12 Nov audit reported `OverQuotaMapError` and a failed MyRealPage `embeddable.less`. **Neither was rechecked in the console this session.**
- Connect the Google reviews Worker (`workers/reviews`, BL-03) or stop requesting `/api/reviews.json`.
- A condo-building template, after rankings are re-pulled and the origin is stable.
- A script `content-security-policy` once the third-party list is final.
- Recompute click depth on a crawl taken when the origin is stable. Do not treat thin-content.csv as the current word counts.

## Still open from the 12 November audit

| 12 Nov finding | This session |
| --- | --- |
| Fixed bottom bar covers controls on ~1,100 pages | Code now hides `.action-bar` until `scrollY > 72` (`src/layouts/Base.astro`, `src/styles/global.css`). **Not remeasured** at 375 / 390 / 430 |
| LCP 4.2s home, 5.5s South Surrey homes, 7.8s neighbourhood guides | Home still **4.20s**. South Surrey homes Lighthouse **did not finish** (Chrome interstitial). `/neighbourhood-guides.html` is **404** and is not in the sitemap; per-city indexes such as `/surrey-neighbourhood-guides.html` exist. Yorkson guide LCP was 3.93s |
| 3,539 listing photos alt-texted `Photo N:` | **Not reproduced.** Snapshot generic-alt count 0. One listing’s alts describe the photo |
| Logo and breadcrumbs to `/index.html` | **Fixed.** `/index.html` is `301` to `/`. No internal link to `jaredgibbons.ca/index.html` in the worker snapshot |
| Listing breadcrumb schema points at `/our-listings.html` | **Not reproduced.** No breadcrumb last-item mismatches in the snapshot validator |
| 69 external 404s, mostly newwestcity.ca | **Not fully retested** (5,738 external URLs; 80 were fetched). 0 of those 80 were HTTP 404. Five newwestcity.ca URLs redirected to a 200. Eleven others returned 403 (tol.ca, vancouver.ca, statcan), which is often a bot block, not a confirmed human 404. One `laws.abbotsford.ca` URL failed TLS |
| Google Maps `OverQuotaMapError` on 138 pages | **Not verified** (no console pass this session) |
| MyRealPage `embeddable.less` fails on ~1,360 pages | **Not verified** |
| `.btn` is 40px | CSS is now `min-height: 2.75rem` in `src/styles/global.css`. **Not remeasured** in a browser |
| Back-to-top outside a landmark | Markup is now `<nav class="to-top-nav">`. **Axe was not re-run** |
| Review quote “jared.Selling” / “condo.Hope” | **Not found** in `src/data/review-excerpts.json` |
| “needs.Use” and “the The” | **Not found** by a text-node scan. Four “glued” hits were abbreviations (`Mt.Lehman`, `St.George`) |
| Three sitemap URLs with a leading hyphen | Redirect still works, one hop. Those hyphen URLs are **not** in the current sitemap |
| Widget phone `1 (604) 9281361` | **Not verified** (inside the IDX frame) |
| `/api/reviews.json` and `/api/instagram.json` 404 | Reviews is now **204** (still empty). Instagram **GET is 200** |
| `INDEXABLE` false in the repo | `wrangler.jsonc` is `"true"`. Worker responses had no `x-robots-tag` |
| Empty form posts rejected | Still true on the Worker: `422`, and `403 captcha_required` when fields are valid and the token is missing. No lead id |

## Not verified

- Field INP and CrUX.
- Lighthouse on `/south-surrey-homes-for-sale.html` (Chrome interstitial).
- Console errors, Maps quota, and the MyRealPage stylesheet, this session.
- A 1,900-page visual pass for the bottom bar, 44px targets, or horizontal scroll.
- Which Cloudflare rule still reaches MyRealPage.
- Semrush keyword and competitor tables (API units exhausted after the domain snapshot).
- That review quotes match Google word for word.
- The FVREB Top 1% and Medallion Club claims.
- A completed form arriving in email or Keyvera.
- Status of the other 5,658 external URLs.
- Mortgage-calculator arithmetic in the browser. The page returned 200 and Lighthouse performance was 0.93. The result of a calculation was not read back.
- Whether the hidden fallback “The live listings did not load.” (`src/components/IdxEmbed.astro`, attribute `hidden`) is shown to users. It is in the HTML of about 1,247 snapshot pages and is not evidence by itself that listings failed.

## Method

- Live sitemap downloaded 13 Nov 2026: 1,900 URLs, all `lastmod` 2026-11-13.
- Worker-only recrawl: a response was kept only when `server` contained `cloudflare` (retry up to 4). Result: **1,900 / 1,900 HTTP 200**.
- Unfiltered crawl of up to 8,000 URLs, used only to show legacy 404s and 403s.
- Lighthouse mobile on 8 templates. Seven produced scores.
- Form checks were empty or invalid JSON, or a fake complete body with no captcha token. No id was returned.
- External status check: 80 of 5,738 unique external URLs.
- Semrush domain rank, Canada database, before the unit balance hit zero.
