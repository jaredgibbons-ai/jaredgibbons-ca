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

## Launch checklist (nothing here is done)
- [ ] Approval from Jared to launch, in writing
- [ ] Route manifest 100% classified; redirects reviewed; real 404
- [ ] IDX connected and Royal LePage sign-off, or listing surfaces explicitly scoped out
- [ ] Forms: server validation, Turnstile, stored in D1, notification delivered end to end (test messages received)
- [ ] Preview chrome removed; `noindex` removed; robots.txt and sitemap rules applied
- [ ] Meta descriptions restored from archive; canonical and redirect checks
- [ ] Analytics (GA4 `G-7YQYX2KPBR`, Ads `AW-10817976788`, Meta Pixel) verified firing once
- [ ] Core Web Vitals: lab and field reported separately; LCP ≤2.5 s, INP ≤200 ms, CLS ≤0.1
- [ ] WCAG 2.2 AA audit, including manual keyboard and screen-reader passes
- [ ] Rollback rehearsal; DNS change **only** with explicit approval

## Run 2026-10-31 (after asset integration)
- Archive-vs-render comparison: unchanged (home 1 line missing, Fort Langley known deviations only).
- axe (home, Fort Langley; desktop + mobile): 0 serious/critical; 1 moderate `heading-order` (archive heading hierarchy preserved, D-03).
- Lab only (local, no throttling; field data not yet available): LCP 48–112 ms, CLS ≤ 0.0005.
- Interaction: mega-menu hover/Enter/Esc, mobile menu open/close, no horizontal overflow at 390 px.
- Broken images: 0. All 10 review stars compute to rgb(166,124,0).

## Run 2026-10-31 (folder 09 page import, 634 generated pages)
- Build: 637 pages in about 5 s.
- Archive-vs-render (`tools/compare_all.py`, 635 pages incl. blog index): 648,212 archive text lines, **0 missing** (169,627 are the dropped IDX grid, 6,314 vendor-widget lines, both documented). Titles, canonicals and meta descriptions match on 635 of 635. Headings: 34 missing of 24,916 (card-internal), plus 6,411 outline-only hidden headings. Links: 50 destinations missing of 145,326 (<0.1%). **585 of 635 pages are fully clean**; 50 need review (OI-21).
- Blog posts (`--kind blog`, 200 posts, `docs/test-results/compare-posts.json`): 112,406 lines, **0 missing**; 2,099 headings, 0 missing; titles/canonicals/metas 200 of 200; links: 3 missing of 50,301 plus 39,800 shared-nav links classified as B-24 (archive resolves them to broken `/blog.html/<page>.html`). **197 of 200 clean.** Blog index axe: only the preserved heading-order (D-03) finding; lab LCP 192 ms, CLS 0.0005, no mobile overflow.
- axe on 20 sampled pages across 12 layout families, desktop and mobile (40 page-views): 0 serious/critical; moderate `heading-order` on all (archive hierarchy preserved, D-03). No horizontal overflow at 390 px.
- Lab only (local, unthrottled; no field data): max LCP 108 ms, max CLS 0.0009.
- Not yet run on all 634: axe and interaction tests (sampled only); visual review of every family. Forms, listings and redirects are not operational.

## Run 2026-10-31 (routing Worker)
- `npm test`: 11 of 11 pass. Every one of the 56 archive redirects returns its documented target and status; every "broken at source" and conflicting URL returns 404; built pages resolve; tracking/preview/pagination params serve the page; nested-path mapping; Worker run end to end against `dist/` (200, 301 with `Location`, real 404 status and body, `noindex` header, 405 for non-GET/HEAD).
- Not yet run: against Cloudflare itself (`wrangler dev`/deploy needs the account, BL-07); HTTPS and www rules at the zone level.
