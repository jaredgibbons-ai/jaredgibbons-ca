# Fix plan for the coding agent

Read `REPORT.md` first. Do not treat `thin-content.csv` word counts as the current page text. The site was being served by two origins during the audit, and some HTML in the worker snapshot was a short copy that later requests replaced.

Work in the order below. After each batch, run the acceptance checks before starting the next. Do not deploy until batch A passes on the live host, because a correct repo can still be hidden by the legacy origin.

Repo paths are relative to the site repo. Live host is `https://jaredgibbons.ca`.

## Batch A. One origin

The Worker in `src/worker/index.js` is not the only thing answering the hostname. Confirmed live:

- `GET /south-surrey-homes-for-sale.html` has returned `server: Apache/2.4.46` with a different title and a ~333KB body, and later `server: cloudflare` at ~123KB.
- `GET /contact.html/` has returned `301` from Apache.
- `POST /api/forms/newsletter` has returned the MyRealPage sentence “the url you requested doesn't exist”, and later Worker `422`.
- An unfiltered crawl saw 847 sitemap URLs answer with the legacy title “Page Not Found”.

The Worker code does not proxy to Apache. The fix is the Cloudflare route for this zone: every request for `jaredgibbons.ca` and `www.jaredgibbons.ca` must hit the Worker (`run_worker_first` is already set in `wrangler.jsonc`). Remove or bypass the MyRealPage origin.

Acceptance:

- Ten repeats of `GET /`, `GET /south-surrey-homes-for-sale.html`, `GET /contact.html/`, and `POST /api/forms/newsletter` with `Origin: https://jaredgibbons.ca` and body `{}` all show `server: cloudflare`, the security headers from `src/worker/index.js`, and never `Apache` or `x-mrp-`.
- The newsletter POST returns `422` JSON naming email and consent, not the MyRealPage sentence.
- `GET /south-surrey-homes-for-sale.html` title is stable across the ten repeats.

Do not change page copy in this batch.

## Batch B. Small Worker and content fixes

1. In `src/worker/route.js`, the host check already 301s `www` and `http`. Add a 301 to `https://jaredgibbons.ca` when the host is `jaredgibbons.ca` with any uppercase letter. Today `https://JaredGibbons.ca/about.html` is `200` with the right canonical.

2. Empty FAQ answer. Live page `https://jaredgibbons.ca/south-surrey-real-estate-agent-jared-gibbons-realtor.html` emits `FAQPage` with question “What is this page?” and an empty `acceptedAnswer`. Find that question in the page’s data (local JSON or the component that builds FAQs in `src/components/GenericPage.astro`) and either write the answer or delete the question. Do not add `AggregateRating` or `Review` schema.

3. Dates on reviews. `src/data/review-excerpts.json`: 70 of 78 items have `when` equal to “Google review” and no calendar date. The rule is initials, verbatim quote, a date, and a true source. Add the date from the Google review, or remove the excerpt. Do not invent dates. If the date is not in hand, drop the excerpt from rotation until it is.

4. Orphans. These sitemap URLs had no internal link in the worker snapshot. Link each from the obvious hub:

   - `/bc-landlord-tenant-resources.html`
   - `/blog.html/bchl-playoffs-surrey-eagles-face-crucial-road-games-in-penticton-8243016`
   - `/blog.html/cleanbc-rebates-in-bc-save-thousands-on-windows-heating-home-upgrades-8925479`

   A footer or “related” link is enough. Do not noindex them.

Acceptance:

- `curl -I https://JaredGibbons.ca/about.html` is `301` to `https://jaredgibbons.ca/about.html` (one hop).
- The agent page’s FAQ JSON-LD has no empty `acceptedAnswer`.
- A search of rendered review cards finds no excerpt whose only time label is “Google review”, unless you intentionally left a documented list of ones still waiting on a date.
- Each orphan URL appears as an `<a href>` on at least one other sitemap page.

## Batch C. Performance on three templates

Lighthouse mobile, this session, simulated throttling:

| URL | Performance | LCP | CLS | TBT |
| --- | --- | --- | --- | --- |
| `/` | 0.73 | 4.20s | 0 | 340ms |
| listing `…/listing.139-143-angela-avenue-princeton-10352922.106171503` | 0.77 | 5.60s | 0.012 | 130ms |
| `/map-search.html` | 0.70 | 5.48s | ~0 | 120ms |
| `/yorkson-langley-guide.html` | 0.86 | 3.93s | 0 | 140ms |
| blog `…/115-9072-fleetwood-way-599k-8919895` | 0.97 | 2.18s | 0.025 | 120ms |
| `/contact.html` | 0.94 | 2.85s | 0.029 | 110ms |
| `/mortgage-calculator.html` | 0.93 | 2.86s | 0.005 | 120ms |

Homepage specifics from that run:

- Google Tag Manager transferred ~354KB and blocked the main thread ~410ms. The tag is the inline gtag block in `src/layouts/Base.astro` (`G-7YQYX2KPBR` and `AW-10817976788`).
- “Properly size images” estimated 440KB savings. Largest items were `/listing-photos/eff40a8c4d163dea-960.webp`, `85e0dedd94aee852-960.webp`, `a39bf980935f689b-960.webp`, `a6dd497c2d378272-960.webp`, and `/img/Jared.webp`.
- Unused JavaScript ~135KB on each successful run.

Do this, and nothing broader:

- Load the analytics tag after first paint or on the first scroll or click. Keep it off the preview build (that guard already exists).
- On the homepage, do not use the 960-wide listing photo when the slot is a small card. `src/worker/photos.js` already has sizes. Point the card at the smaller one and keep width and height attributes.
- Re-run Lighthouse mobile on `/`, the listing URL above, and `/map-search.html`.

Acceptance: LCP under 4.0s on those three, CLS still under 0.1, and the pages still send the analytics event after interaction. Do not remove the tag entirely.

`/south-surrey-homes-for-sale.html` hit `CHROME_INTERSTITIAL_ERROR` and was not scored. After batch A, run Lighthouse on it once and record the number. Do not “fix” that page from the interstitial alone.

## Batch D. Do not do these unless a recheck shows they are still wrong

The 12 Nov audit listed these. This session’s evidence:

- `/index.html` already 301s to `/`. No internal links to `https://jaredgibbons.ca/index.html`.
- Listing breadcrumb JSON-LD did not point the current page at `/our-listings.html`.
- `.btn` min-height in `src/styles/global.css` is `2.75rem`, not `2.5rem`.
- `.action-bar` is off-screen until `scrollY > 72` (`src/layouts/Base.astro`). The overlap was not remeasured. Do not restyle it unless a phone check at 375, 390, and 430 still shows it covering a control on first paint.
- Back-to-top is inside `<nav class="to-top-nav">`. Axe was not re-run.
- `wrangler.jsonc` `INDEXABLE` is `"true"`. Do not set it to `"false"`.
- Generic `Photo N:` alts were not found. Do not rewrite listing alts in bulk.
- Hyphenated blog URLs redirect in one hop and are not in the sitemap. Leave the redirect in `MOVED` in `src/worker/route.js`.
- `/api/instagram.json` GET returned 200. `/api/reviews.json` is 204 by design until `workers/reviews` is connected. Do not point the page at a public Google URL.

## Batch E. Content, only after A–C

- Do not merge the Abbotsford condo URLs. Eight full ones overlapped at most 0.16 on 8-word shingles, and all 1,900 titles and descriptions in the snapshot were unique.
- Sitemap `lastmod` is `2026-11-13` for every URL because `src/data/lastmod.json` was written on launch day (`src/integrations/lastmod.mjs`). Leave the integration. Do not stamp every URL with a new date on the next build unless `<main>` actually changed.
- A condo-building section is a new template, not a fix. `realestatewhiterock.com` publishes building profiles; this sitemap does not. Scope it with Jared before building it. Semrush Canada (this session, before the API unit balance hit zero): 1,062 keywords, 442 estimated visits, 13 keywords in positions 1–3. The keyword list itself was not returned.
- Footer line “Top 1% of all REALTORS® in the Fraser Valley (Fraser Valley Real Estate Board)” is on every page via `src/components/Footer.astro`. Homepage meta description says “10 straight years in the FVREB Medallion Club.” Do not delete them in this pass. Ask Jared for the board source and the years. They are not in any H1 that was checked.
- There is no terms page in the sitemap. Privacy and the MLS disclaimer are already in the footer. Add terms only if Jared asks.

## Batch F. Forms and schema, no live leads

Already true on the Worker, with `Origin: https://jaredgibbons.ca`:

- Empty JSON to `/api/forms/contact` is `422` with name, email, and message errors.
- A syntactically complete body and no `cf-turnstile-response` is `403` `captcha_required` and has no `id`.
- The same empty-body `422` holds for `home-evaluation`, `property-check`, `quiz`, `listing-alert`, and `presale-vip`.

Do not POST a real name, email, or a valid Turnstile token. Do not “test” delivery.

`src/worker/index.js` documents that the content security policy is only `frame-ancestors` and `base-uri`. Leave it until the script list is stable. A full `script-src` in the same change as the tag deferral will break Maps, Turnstile, or the IDX embed if one host is missed.

## Acceptance for the whole plan

- Ten requests to the four URLs in batch A never show Apache or MyRealPage headers.
- Mixed-case host 301s once.
- The empty FAQ answer is gone.
- Undated review excerpts are dated or removed.
- The three orphans have an inbound link.
- Lighthouse mobile LCP is under 4s on `/`, the listing URL in batch C, and `/map-search.html`, with CLS under 0.1.
- `INDEXABLE` stays `"true"`.
- No new `Review` or `AggregateRating` JSON-LD.
- No Sauder or UBC diploma sentence anywhere. There is none in the repo or the snapshot text today.
