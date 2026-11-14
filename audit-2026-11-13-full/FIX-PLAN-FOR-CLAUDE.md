# Fix plan for the coding agent

Read `REPORT.md` first. Do not deploy until the copy in batches A and B matches the approved wording, because a fast deploy of the current footer would keep the wrong sentence on every page.

Approved ranking wording, use this and no other ranking sentence unless Jared confirms an award badge in writing:

> #1 REALTOR® in South Surrey / White Rock by FVREB Medallion Club points (2025 and 2026 YTD). #1 of the Top 25 individuals at Royal LePage Little Oak Realty (2025). Top 1% of Fraser Valley REALTORS®.

Rules that apply to every batch:

- Ranking text goes in a subheading (`h2`–`h6`) or in body copy. Never in an `h1`.
- Do not write “Top 1% of all REALTORS®”, “10 straight years”, “11+ years”, or “South Surrey's #1 Ranked Realtor”.
- REALTOR® tenure is “since 2015”, not a plus-year count.
- Reviews show initials only, the verbatim quote, a calendar date, and the source Google or Trustindex. Do not invent a date, a name, or a quote.
- Do not add `Review` or `AggregateRating` JSON-LD.
- Do not POST a real lead. Do not set `INDEXABLE` to anything but `"true"`.
- There is no UBC Sauder diploma sentence today. Do not add one.

Repo root is this site repo. Live host is `https://jaredgibbons.ca`.

## Batch A. Ranking copy

1. `src/components/Footer.astro` (the tag line near the phone). Replace “Top 1% of all REALTORS® in the Fraser Valley (Fraser Valley Real Estate Board)” with “Top 1% of Fraser Valley REALTORS®”. If the footer can hold one more line without becoming an `h1`, add the two `#1` sentences as a paragraph, not a heading. Remove the MyRealPage credit in the same file only if batch E is being done in this pass; otherwise leave that link for batch E.

2. `src/pages/index.astro`
   - Meta description: remove “10 straight years in the FVREB Medallion Club”. A safe description is the current one with that clause deleted, still under 160 characters.
   - H1 stays “JARED GIBBONS” / “South Surrey Realtor”. Do not add a ranking to it.
   - Change the H2 “South Surrey's #1 Ranked Realtor” to a subheading that uses the approved South Surrey / White Rock Medallion sentence, including 2025 and 2026 YTD.
   - The lede under that H2 is close. Change “#1 agent at Royal LePage Little Oak Realty in 2025” to “#1 of the Top 25 individuals at Royal LePage Little Oak Realty (2025)”.
   - Stat list: replace “10 / Straight years, FVREB Medallion Club” and “11+ / Years as a REALTOR®” with “REALTOR® since 2015” and the Top 1% line without “of all”. Keep the $500M stat only if Jared has already approved that number in writing; it is not in the approved ranking sentence. If you are not sure, leave the number and add a code comment that it was not part of this wording change, rather than deleting a figure you cannot verify.

3. `src/pages/fort-langley.astro` sign-off that says “Top 1% of all REALTORS®”. Same replacement as the footer.

4. Search `src/` (not `docs/`) for `Top 1% of all`, `10 straight years`, `11+ years`, and `#1 Ranked`. Update rendered copy in `src/components/GenericPage.astro`, `src/data/designed/`, `src/data/seo-final.json`, `src/data/seo-overrides.json`, and the local JSON that actually renders. FAQ answers that repeat the old sentence should use the approved sentence or drop the ranking clause. Do not edit `docs/research/` (those files record old checks).

5. `src/data/home.ts` award alts. Do not rewrite a badge’s alt to the FVREB sentence. Leave the image. If an alt says “National Top 2%” or “Top 5%” or “Top 35 Under 35”, leave it only when the image file is that badge. Do not add those phrases to titles, H1s, or meta descriptions.

Acceptance:

- A search of rendered output (or `rg` on `src/components`, `src/pages`, `src/layouts`, `src/data` excluding nothing that ships) finds no `Top 1% of all` and no `10 straight years`.
- The homepage H1 text does not contain `#1`, `Top 1%`, or `Medallion`.
- The homepage H2 or the paragraph under it contains “FVREB Medallion Club points” and “2025 and 2026”.
- Footer no longer contains the word “all” immediately before `REALTOR`.

Verify: `curl -sL https://jaredgibbons.ca/` after deploy and confirm the strings. Before deploy, render the homepage locally and read the H1, H2, and footer.

## Batch B. Reviews

1. `src/data/home.ts` `reviews` array. Replace each `name` with the initials already used for that same quote in `src/data/google-reviews.json` (Baljinder → the B.C. record, Natalie → N.K., and so on). Replace each `text` with the full verbatim string from that record, not the ellipsis cut. Keep a calendar date. Richard is “June 2026” only; if the Google export has no day, drop that card or show “June 2026” only after you have the day. Do not guess the day.

2. `src/data/google-reviews.json`. `when` is a relative phrase (“6 days ago”) captured 1 November 2026. Replace each `when` with a calendar date from the original Google export if that export is in the repo (`tools/data/google-reviews-2026-11-01.json` or similar). If the export has only the relative phrase, change `/reviews.html` so it does not print a relative time as if it were still true. The existing sentence “Times are as Google showed them on 1 November 2026” can stay until real dates exist. Prefer a date.

3. `src/data/review-excerpts.json`. 70 items have `when: "Google review"`. Add the calendar date from the same Google review, or remove the item from the array. Do not invent dates. Initials in `who` are already correct. `src/components/ReviewCards.astro` can stay.

4. `src/pages/reviews.astro` Places fallback (`fromPlaces`). It prints `authorAttribution.displayName`. Map that to initials (first letter of each word, or the first two letters if it is one token) before `render()`. Do not show the full Google name. The static 87 reviews already use initials; leave that.

5. `src/worker/index.js` `/api/reviews.json`. It returns 204 until `env.REVIEWS` serves JSON (BL-03). Either connect that worker with real Google Business Profile data that you then pass through as initials + date + verbatim text, or leave the 204 and do not pretend the block is live. Do not point the page at a public Google URL that dumps full names into the HTML.

6. Homepage “5.0 · 95 Google reviews” in `src/pages/index.astro` and the “95 reviews” line on `/reviews.html`. Leave the numbers if they match the 1 November export note. Add the date of the count (“as of 1 November 2026”) next to the 95 so it is not an undated live claim. Do not change 95 to 87; the page already says 87 of them have written comments.

Acceptance:

- Homepage cards show no full first name. A search of the homepage HTML finds no `Baljinder`, `Natalie`, `Savannah`, or `Kelly`.
- No homepage quote ends with the ellipsis character unless that character is inside the original Google text.
- A search of rendered review cards finds no `when` that is only “Google review”.
- `/reviews.html` does not show “6 days ago” unless the surrounding sentence still says the phrase is how Google displayed it on 1 November 2026 and you have not yet got calendar dates.
- `GET /api/reviews.json` is either 204 or a JSON body whose `name` fields are initials.

Verify with `curl` on `/` and `/reviews.html`, and `GET /api/reviews.json`. Do not submit the review form.

## Batch C. Map CLS and the calculator

1. Map. `/map-search.html` CLS was 0.158 mobile and 0.154 desktop. The console said Mapbox GL JS is missing `mapbox-gl.css` (`api.tiles.mapbox.com/mapbox-gl-js/v0.54.1`). The widget is the MyRealPage iframe (`src/components/IdxEmbed.astro` and the map page template). Give the iframe or its wrapper a reserved height before the script runs, and include the Mapbox stylesheet the widget asks for if you control that document. If the stylesheet is inside the iframe, fix it on the IDX template, not by adding a random CSS file to the parent. Re-run Lighthouse mobile on `/map-search.html`. Acceptance: CLS under 0.1, and the map still logs listings (this session saw `totalFound: 1743`).

2. Calculator. `src/pages` title for `/mortgage-calculator.html` includes “Stress Test”, and `src/data/seo-final.json` description says the tool shows how the stress test shapes the budget. `src/components/MortgageCalc.astro` does not compute a qualifying payment. Either:
   - add a row “Qualifying payment (stress test)” using the greater of the typed rate + 2.00 and 5.25, labeled as an estimate, or
   - remove “stress test” from the title and description.
   On load, `run()` marks an empty price `aria-invalid`. Only set that error after the field is blurred or the visitor clears a value they had typed. The empty state copy “Enter a home price to see the estimate.” is enough before that.
   Align the FAQ sentence “0.6% to 4.5%” in `src/data/local/mortgage-calculator.json` with `premiumPct()` in `src/lib/mortgage.js` (max 4.0 in code) after you re-read the CMHC premium table linked from the form. Do not change both to a number you have not checked.

   The $800,000 / 20% / 4.69% / 25-year case currently returns $3,610.14 and $14,000 property transfer tax. Keep that result.

Acceptance: Lighthouse CLS on the map is under 0.1. The calculator page title matches what the form actually computes. Loading the calculator does not set `aria-invalid` on an untouched price field. The $800,000 case is unchanged.

## Batch D. Small SEO and schema fixes

1. `src/worker/route.js` host check. Today `www` and `http` 301 to `https://jaredgibbons.ca`. Also 301 when the host is `jaredgibbons.ca` with any uppercase letter. `https://JaredGibbons.ca/about.html` is 200 today.

2. Broken sentence in FAQ JSON-LD, live on:
   - `/south-surrey-real-estate-agent-jared-gibbons-realtor.html`
   - `/morgan-crossing-homes-for-sale.html`
   The answer starts “Jared Gibbons to set up custom MLS listing alerts”. Add the missing verb (“Ask Jared Gibbons to set up…”) or delete the question. Find the string in the page’s data file (designed or pages JSON, not only `src/data/local/`, because the local file’s empty “What is this page?” is not what the live page emits).

3. Delete, do not publish, these source questions so a later template cannot emit them:
   - `src/data/local/south-surrey-real-estate-agent-jared-gibbons-realtor.json` question “What is this page?” with an empty answer.
   - `src/data/local/jared.json` empty “What is the jared.html page?”.
   - Every `faq` question matching `Can Jared show me homes in` (32 files under `src/data/local/`). They are not on the live calculator today.

4. Two listings with `Offer` and no price:
   - `/our-listings.html/listing.7-19696-telegraph-trail-langley-commercial-lease.107131830`
   - `/our-listings.html/listing.c8075374-104-19232-enterprise-way-surrey-bc-v3s-6j9.107690830`
   Find the JSON-LD builder for listings and omit `Offer` when the page has no numeric price. Do not invent a price for a lease.

5. External 404. Replace `https://www2.gov.bc.ca/gov/content/housing-tenancy/strata-housing/strata-property-act` on these four pages with the current BC government URL for the Strata Property Act (confirm the new URL returns 200):
   - `/bc-duplex-half-duplex-buying-rules.html`
   - `/coquitlam-55-plus-homes-for-sale.html`
   - `/cottonwood-mr-55-plus-homes-for-sale.html`
   - `/east-central-55-plus-homes-for-sale.html`

6. `lastmod`. Do not rewrite `src/data/lastmod.json` so every URL is today. `src/integrations/lastmod.mjs` should keep the previous day when `<main>` did not change. For a blog post, the visible date stays `datePublished`.

7. Optional, low: add `/favicon.ico` as a copy of or redirect to `/favicon.png`. A manifest is optional.

Acceptance:

- `curl -sI https://JaredGibbons.ca/about.html` is 301 to `https://jaredgibbons.ca/about.html` in one hop.
- The two FAQ pages’ JSON-LD has no sentence “Jared Gibbons to set up”.
- `rg "Can Jared show me homes in" src/data` returns nothing.
- Those two listing pages’ JSON-LD has no `Offer` with an empty price.
- The strata URL used on the four pages returns HTTP 200.

## Batch E. Images, MyRealPage leftovers, CSP

Do this after A–D.

1. Homepage cards still request `*-960.webp` for a small slot (`uses-responsive-images` estimated 440 KiB on `/`). In the homepage listing card (`src/pages/index.astro` and `src/worker/photos.js`), use the smaller derivative that already exists. Keep `width` and `height`. LCP image is `/img/Jared.webp` with a 480w srcset; confirm the `sizes` attribute matches the hero (it was about 377 CSS pixels wide on a mobile run).

2. 203 listing `og:image` values point at `iss-cdn.myrealpage.com`. Point `og:image` at a first-party image under `/listing-photos/` or `/img/og-default.jpg` when a local photo exists. Do not hotlink the CDN.

3. `src/components/Footer.astro` link “Real Estate Websites by myRealPage”. Remove it unless counsel or the brokerage requires the credit.

4. CSP. `src/worker/index.js` `SECURITY` is frame and base only. Do not add `script-src` in the same change as the tag work unless you have the full host list: `www.googletagmanager.com`, `www.google-analytics.com`, `www.googleadservices.com`, `googleads.g.doubleclick.net`, Mapbox tiles, `idx.myrealpage.com`, `res.myrealpage.com`, Turnstile, YouTube, and `static.cloudflareinsights.com`. A missed host breaks the map or the forms. Prefer a follow-up.

Acceptance: Lighthouse mobile on `/` still has LCP under 2.5 s and CLS under 0.1, and “properly size images” is well under 440 KiB. A listing page’s `og:image` host is `jaredgibbons.ca` when a local photo exists. The footer has no `myrealpage.com` link, unless you documented why it stayed.

## Batch F. Do not do these

The 13 November audit and the 12 November audit listed items that are not broken now.

- Do not chase a second origin. This session’s 1,905 URLs and the repeat probes were all `server: cloudflare`. If a later request returns `Apache` or `x-mrp-`, then the Cloudflare route is the fix, in the dashboard, not in page copy.
- Do not add internal links just to fix click depth. With every link counted, nothing in the sitemap is deeper than 3 clicks and nothing is an orphan.
- Do not merge price-band or city/type URLs. Titles and descriptions are unique.
- Do not set `INDEXABLE` to `"false"`.
- Do not bulk-rewrite listing alts. `Photo N:` was not found.
- Do not add `FAQPage` removal as an SEO project. Leave the visible questions. Do not expect FAQ rich results.
- Do not POST the contact, newsletter, quiz, or alert forms to “test” them.
- Do not add a terms page unless Jared asks. Privacy and the MLS disclaimer are already in the footer.
- Do not treat `thin-content.csv` rows under 700 words as articles to pad. The contact page is a form. The others are sold listings.

## Order and checks

1. Batch A, then read the homepage and one interior page.
2. Batch B, then read `/` and `/reviews.html` and `GET /api/reviews.json`.
3. Batch C, then Lighthouse mobile on `/map-search.html` and a manual look at the calculator with $800,000.
4. Batch D, then the curl checks listed there.
5. Batch E, then Lighthouse mobile on `/`.

Whole-plan acceptance:

- Footer and homepage do not say “Top 1% of all” or “10 straight years”.
- No H1 contains a ranking claim.
- Homepage review names are initials, and quotes are not the shortened homepage set.
- Excerpt cards are not dated only “Google review”.
- Map CLS is under 0.1.
- Mixed-case host 301s once.
- `INDEXABLE` stays `"true"`.
- No new `Review` or `AggregateRating` JSON-LD.
- No Sauder or UBC diploma sentence.
