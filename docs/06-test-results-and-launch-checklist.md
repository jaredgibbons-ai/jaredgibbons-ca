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
