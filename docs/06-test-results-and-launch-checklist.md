# Test results and launch checklist

## Preview test results (2026-10-31, local lab, Chromium via Playwright; **not** field data)
Reproduce: `npm run build`, serve `dist/` on :4321, then `python3 tools/compare.py`, `tools/a11y_perf.py`, `tools/interact.py`, `tools/shoot.py`. Raw output is in `docs/test-results/`.

| Check | Home | Fort Langley | Notes |
|---|---|---|---|
| Title matches archive | pass | pass | exact string |
| Canonical matches archive | pass | pass | `noindex` added for preview only (D-17) |
| Archive visible-text lines present in render | 839 of 840 | 1067 of 1068 | the 1 each is the `<title>` string, which is checked above. Documented non-rendered lines are in `KNOWN` in `tools/compare.py`. |
| Archive link destinations present | 265/265 | 249/251 | missing: `recip.html?showsignup`, `?showlogin` (D-10) |
| Archive headings present | 27/29 | see compare JSON | remaining: header/footer chrome headings; footer ones exist outside `<main>` |
| axe (WCAG 2.0–2.2 A/AA + best-practice) | 0 critical/serious; 1 moderate (heading-order) | 0 critical/serious; 1 moderate (heading-order) | heading-order comes from the archived structure (H1 followed by H3), recorded not corrected |
| Horizontal overflow at 390 px | none | none | |
| Keyboard nav | pass | pass | toggle opens with Enter, Esc closes and returns focus, mega panel closes on mouseleave/Esc, mobile menu opens/closes with label change |
| Lab LCP / CLS (unthrottled, local) | ~60–90 ms / ≤0.001 | ~40–70 ms / 0 | meaningless as a budget check: no images are loaded yet. **Re-measure with real images, throttled.** Field data: none (not live). |

Bugs found and fixed during this pass: mobile menu overlay covered its own toggle; stray "0" on cards; hero name broke mid-word; brand/nav misaligned; landmark duplicates.

Not yet tested: forms (none in preview), real images, INP, Safari/Firefox, screen reader, reduced-motion visual pass, print.

## Launch checklist (updated 2026-11-07; nothing is launched)
Approval pack: `docs/review/launch/launch-approval-2026-11-07.csv` (one row per new page, in batches) and `docs/review/launch/README.md`.

**Needs Jared**
- [ ] Written approval to launch, batch by batch (A: 479 pages ready, E: 164 auto-generated pages)
- [ ] Confirm the 312 neighbourhood-map outlines in 21 regions (`src/data/maps/*.json`, status draft to confirmed). The launch build refuses to run while any outline is draft (`AreaMap.astro`)
- [ ] Launch build setting `PUBLIC_PREVIEW=false` (removes review notes, `noindex` on the preview, applies holds)
- [ ] `PUBLIC_GOOGLE_MAPS_KEY` build variable (maps, address suggestions, commute times)
- [ ] IDX: Royal LePage sign-off or the new feed route (BL-04); GBP reviews feed (BL-03); newsletter form destination (BL-05); privacy page confirmations
- [ ] Forms live: Turnstile site key and secret set by Jared, `PUBLIC_FORMS_LIVE=true`, test messages received at both addresses
- [ ] Analytics (GA4 `G-7YQYX2KPBR`, Ads `AW-10817976788`, Meta Pixel) verified firing once
- [ ] DNS change, only with explicit approval

**Waiting on others (held pages: `src/data/launch/holds.json`)**
- [ ] Jerry's saved searches: 97 held pages (price bands 20, area pages 33, condos and townhomes 21, acreage 14, guides 8, 55+ 1). Five main-menu hubs are in this list: Richmond, Vancouver, Burnaby, New Westminster and Coquitlam neighbourhood guides
- [ ] Pete's school exports: 76 held school pages

**Done**
- [x] Route manifest classified, redirects implemented (OI-10a)
- [x] Uniqueness gate: 0 of 816 new pages under 70%
- [x] Link, SEO, markup and accessibility scans clean (D-171)
- [x] Holds: a held page is noindex, out of the sitemap, footer and generated link lists in the launch build (tested 2026-11-07: sitemap 1,871 to 1,698 URLs, 0 draft notes left)
- [ ] Core Web Vitals with real images, throttled; Safari and Firefox; screen reader pass; rollback rehearsal (not yet done)

## Run 2026-10-31 (after asset integration)
- Archive-vs-render comparison: unchanged (home 1 line missing, Fort Langley known deviations only).
- axe (home, Fort Langley; desktop + mobile): 0 serious/critical; 1 moderate `heading-order` (archive heading hierarchy preserved, D-03).
- Lab only (local, no throttling; field data not yet available): LCP 48–112 ms, CLS ≤ 0.0005.
- Interaction: mega-menu hover/Enter/Esc, mobile menu open/close, no horizontal overflow at 390 px.
- Broken images: 0. All 10 review stars compute to rgb(166,124,0).

## Run 2026-10-31 (folder 09 page import, 634 generated pages)
- Build: 637 pages in about 5 s.
- Archive-vs-render (`tools/compare_all.py`, 650 pages incl. blog index and the 15 re-captured pages): 662,461 archive text lines, **0 missing** (169,627 are the dropped IDX grid, 6,314 vendor-widget lines, both documented). Titles, canonicals and meta descriptions match on 650 of 650. Headings: 3 missing of 25,504, plus 6,411 outline-only hidden headings. Links: 53 destinations missing of 148,833 (<0.1%). **621 of 650 pages are fully clean**; 29 need review (OI-21). Of the 15 re-captured pages 13 are fully clean; the other two have one missing heading and three image-only links (OI-21 class).
- Blog posts (`--kind blog`, 200 posts, `docs/test-results/compare-posts.json`): 112,406 lines, **0 missing**; 2,099 headings, 0 missing; titles/canonicals/metas 200 of 200; links: 3 missing of 50,301 plus 39,800 shared-nav links classified as B-24 (archive resolves them to broken `/blog.html/<page>.html`). **197 of 200 clean.** Blog index axe: only the preserved heading-order (D-03) finding; lab LCP 192 ms, CLS 0.0005, no mobile overflow.
- Own listings (`--kind listing`, 200 pages, `docs/test-results/compare-listings.json`): 127,665 lines, **0 missing** (9,377 are widget chrome, D-30); 1,422 headings, 0 missing; titles/canonicals/metas 200 of 200; links 0 missing of 42,800 plus 40,000 shared-nav links classified as B-25. **203 of 203 clean (200 plus the 3 re-captured listings).** Axe + lab metrics on 26 sampled posts/listings (`a11y-posts-listings-sample.json`): only the preserved heading-order finding; max LCP 96 ms, max CLS 0.0006, no horizontal overflow.
- Re-captured pages (`a11y-recaptured.json`, 15 pages + 3 listings, desktop and mobile): 0 serious/critical, no overflow, max LCP 116 ms, max CLS 0.0005; only the preserved heading-order finding (D-03).
- Worker tests: 27/27 (worker routing 18, forms 13 incl. email delivery; blog post and listing public URLs return 200 through the Worker, `/internal/*` returns 404, live-observed redirects and re-captured pages are served).
- axe on 20 sampled pages across 12 layout families, desktop and mobile (40 page-views): 0 serious/critical; moderate `heading-order` on all (archive hierarchy preserved, D-03). No horizontal overflow at 390 px.
- Lab only (local, unthrottled; no field data): max LCP 108 ms, max CLS 0.0009.
- Not yet run on all 634: axe and interaction tests (sampled only); visual review of every family. Forms, listings and redirects are not operational.

## Run 2026-10-31 (routing Worker)
- `npm test`: 11 of 11 pass. Every one of the 56 archive redirects returns its documented target and status; every "broken at source" and conflicting URL returns 404; built pages resolve; tracking/preview/pagination params serve the page; nested-path mapping; Worker run end to end against `dist/` (200, 301 with `Location`, real 404 status and body, `noindex` header, 405 for non-GET/HEAD).
- Not yet run: against Cloudflare itself (`wrangler dev`/deploy needs the account, BL-07); HTTPS and www rules at the zone level.

- **Full-site axe (WCAG 2.0–2.2 A/AA + best-practice), `tools/a11y_all.py`, 1,039 pages × desktop and mobile = 2,078 page-views (`docs/test-results/a11y-all.json`; run on the build before the IDX search-bar change, which only removes content):** 0 serious/critical violations, 0 horizontal overflow, 0 console or network errors. Only two findings: `heading-order` (moderate) on every page-view, the preserved archive heading hierarchy (D-03); and `page-has-heading-one` (moderate) on `lake-city-industrial`, which has no H1 in the archive (B-18).
