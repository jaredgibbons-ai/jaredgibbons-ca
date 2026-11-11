# Full site audit: SEO value and errors (prompt for Cursor)

You are auditing the rebuilt jaredgibbons.ca, an Astro 5 static site for Jared Gibbons, REALTOR® (PREC), Royal LePage Little Oak Realty, Fraser Valley and Metro Vancouver, BC. About 1,500 pages. Your job is to find every page and element with low SEO value or an error, and write it all up. Be thorough: check every page, not a sample.

## Ground rules (do not break these)

- **Report only.** Don't edit any file under `src/`, `tools/` or `tests/`, and don't change copy or data. The only files you create are the two report files below. Work on a new branch called `cursor-audit-YYYY-MM-DD`. Never push to `main`, never deploy, and never touch DNS, domains, Cloudflare or any account setting.
- **No secrets.** Don't print, copy or commit any key, token, password or `.env` value. If you find one in the repo, report the file and line only, not the value.
- **Read before you judge.** First read `docs/04-decisions-and-exceptions.md` (the D-numbered decisions). Many things that look odd are deliberate. Some examples:
  - links to other agents and brokerages are unlinked on purpose (D-204, D-209)
  - realtor.ca links get `nofollow`
  - "Draft for Jared" notices are hidden in the launch build
  - city-wide rules live once on `/<city>-home-buying-rules.html` (D-202, D-214)
  - thin pages are held at launch by `tools/launch_pack.py`

  Don't flag a documented decision as an error. If you think a decision is hurting SEO, list it separately under "Decisions worth revisiting" with your reasoning.
- **Jared's voice.** Text in `src/data/jared-voice.json` and anything marked "Jared" is his own words. Don't propose rewrites of it. Only flag factual or spelling errors.
- **Brand:** black, white and grey only. Use plain English. No unsourced superlatives ("best", "#1", "top") unless a source is on the page.

## How the site is built (so you check the right output)

- Data:
  - `src/data/pages/*.json` is the archive of the old site.
  - `src/data/local/*.json` is the local layer. Pages with `new_page` are brand-new.
  - `src/data/guide-plus.json` holds the guide format v2 (quick answer, verdict, pros and cons).
  - `src/data/sold/sold-12m.json` holds sold prices.
  - `src/data/seo-final.json` holds final titles, metas and H1s.
- The renderer is `src/components/GenericPage.astro`, with post-build fixes in `src/integrations/fix-links.mjs`.
- Build the preview with `npm run build`, which outputs to `dist/`.
- Build the launch version with `PUBLIC_PREVIEW=false npx astro build --outDir dist-launch`. **Audit the launch build first.** It is what Google will see. Then note anything that differs in the preview.
- Existing checks:
  - `npm test` (162 tests)
  - `python3 -I tools/uniqueness.py --csv /tmp/uq.csv` (8-word shingle uniqueness)
  - `python3 -I tools/launch_pack.py --uq /tmp/uq.csv` (launch holds)

  Run them and use their output, but don't stop there.
- Serve `dist-launch/` locally (`npx serve dist-launch` or `python3 -m http.server`) and use Playwright (installed) for rendered checks.

## What to check on every page

### 1. Titles, metas and headings
- `<title>` must be present, 30–60 characters, and not cut off mid-word. It must be unique across the site. Flag duplicates, and near-duplicates that differ only by a city name with nothing else unique.
- Meta description must be 120–158 characters, a full sentence, and unique. Flag any that are missing or truncated (ending without punctuation, or ending on "|" or "…").
- There must be exactly one `<h1>`, and it must match the page's intent. Flag pages whose H1 and title target different keywords.
- Heading order must not skip levels (H2 to H4), headings must not be empty, and a heading must not be followed directly by another heading of the same level with no content between them.
- Flag headings and titles in ALL CAPS in the source text. CSS uppercase is fine.

### 2. Indexing and canonicals
- Every indexable page needs a self-referencing absolute `<link rel="canonical">` on `https://jaredgibbons.ca/`. Flag canonicals pointing to the workers.dev preview, to another page without a reason, or to a 404.
- Check `meta robots`:
  - The launch build must not carry `noindex` on pages that are approved in `docs/review/launch/approvals.json`.
  - Pages held by `launch_pack.py` must be `noindex` and out of the sitemap.
- Sitemap (`/sitemap.xml`):
  - every URL returns 200 in `dist-launch`
  - no noindex pages
  - no duplicates
  - `lastmod` present and sane (not in the future, not before 2015)
- `robots.txt` must allow the site, point to the sitemap, and must not block CSS, JS or images.
- Check `.html` URL consistency: internal links must use the same form as the canonical.

### 3. Links
- Crawl every internal link in `dist-launch`.
  - Report every 404, including anchors (`#id`) that don't exist on the target page.
  - Report links to pages that are held or noindex.
  - Report redirect chains if any redirects are defined.
- Orphans: pages that are indexable but have 0 or 1 internal links pointing to them.
- Thin linking: guides with fewer than 5 internal links out. Hubs that don't link to all their children.
- External links:
  - no links to other agents, brokerages or listing portals (the list is in `src/data/other-agent-domains.json`; realtor.ca is allowed, with `nofollow`)
  - no `http://` links where `https://` exists
  - no links to Google cache, archive.org (unless labelled "archived"), localhost or workers.dev
- Check anchor text: flag "click here", "here", "this page", raw URLs used as link text, and the same anchor text pointing to two different pages.

### 4. Content value (low SEO value)
- **Thin pages:** fewer than 300 words of main content, excluding nav, footer, reviews and link lists. Also flag pages that are mostly a listings widget, a form or a table with almost no text.
- **Duplicate and near-duplicate content:**
  - use the uniqueness tool and flag pages under 0.70
  - also flag pairs of pages over 60% similar
  - report the overlapping passages, so it is clear what to cut from where
- **Keyword cannibalization:** two or more pages targeting the same search. Examples:
  - "Langley townhomes for sale" vs "Langley townhouses"
  - a guide and an area page with the same title intent

  List each cluster and say which page should be the main one.
- **Search intent mismatch:** a page titled "X homes for sale" with no listings, or a "guide" with no guide content.
- **Leftover research or process text** that a reader would find odd. For example:
  - "verified", "per the directory", "flagged", "queued", "counted", "not asserted", "batch", "source says"
  - "D-1xx" decision numbers
  - "Muse", "Pete", "Jerry", "Claude"
  - TODO, TBD, lorem, placeholder brackets like `[NEEDS …]`
  - doubled words, sentence fragments, mid-sentence cut-offs, stray single-word headings

  Search the rendered HTML text, not just the JSON.
- **Stale or contradictory facts:**
  - dates in the past presented as upcoming
  - "2025" figures labelled as current
  - the same fact with different numbers on two pages (tax due dates, suite caps, SkyTrain opening year "late 2029", bus routes, school names and addresses)
  - prices with no date or source next to them
- **Unsourced claims:** superlatives, rankings or statistics without a source on the page.
- **Spelling and grammar** across all visible text. Canadian spelling: neighbourhood, centre, metres.

### 5. Structured data
- Validate every JSON-LD block: it must parse, and its types must be valid schema.org (RealEstateAgent, BreadcrumbList, FAQPage, Article and so on).
- FAQPage must only contain questions and answers that are visible on the page, word for word.
- BreadcrumbList must match the visible breadcrumbs and use valid URLs.
- No duplicate or conflicting Organization or RealEstateAgent blocks. Name, address and phone must be the same everywhere: Suite 201 – 15272 Croydon Dr, Surrey; 604-928-1361.
- No review or aggregateRating markup that breaks Google's self-serving review rules.

### 6. Images and media
- Every content `<img>` needs a meaningful `alt` (empty `alt` only for decorative images). Flag filenames used as alt text.
- Images need `width` and `height` set, or another way to prevent layout shift. Below-the-fold images should be lazy-loaded; the hero/LCP image should not be.
- Flag oversized images (over 300 KB) and images served larger than displayed.
- No broken image URLs. Photos served by the Worker from R2 (`/listing-photos/…`) will 404 locally. Note them, but don't count them as errors.

### 7. Rendering, mobile and accessibility
Use Playwright at 390 × 844 and 1280 × 900 on every template type, plus a sample of at least 100 pages across all groups.
- No horizontal scroll at 390 px. Report the element causing it.
- No text cut off or overlapping, tables must scroll inside their own box, and tap targets must be at least 44 px.
- Colour contrast must meet WCAG AA. Focus must be visible. The skip link must work. Form fields need labels.
- No console errors, and no failed network requests apart from the R2 photos.
- Compare the launch and preview builds: preview-only notices must not appear in the launch build.

### 8. Performance
- Run Lighthouse (mobile) on the home page, one page of each template type and the 10 heaviest pages by HTML size. Report LCP, CLS, TBT and total weight.
- Flag render-blocking resources, unused CSS or JS, fonts without `font-display`, and HTML over 300 KB.

### 9. Legal and trust
- Pages showing listing or sold data must carry the MLS® and REALTOR® trademark wording and the brokerage name.
- The brokerage name "Royal LePage Little Oak Realty" must be spelled consistently.
- No "Draft", "preview" or internal notes in the launch build.
- The privacy and contact forms must be present and working (don't submit them; just check that they render and have labels).

## Output

Write two files on the audit branch, and commit only these:

1. `docs/review/cursor-audit-YYYY-MM-DD.md`, containing:
   - a summary at the top: the totals by severity, and the 10 fixes that would gain the most SEO value
   - then one section per check area above
   - each finding should give the page(s), what's wrong, the evidence (a quoted snippet or measured value) and a suggested fix in one line
   - a separate section called "Decisions worth revisiting"
2. `docs/review/cursor-audit-YYYY-MM-DD.csv`, one row per finding, with these columns: `severity` (critical / high / medium / low), `area` (the check area number), `slug`, `url`, `issue`, `evidence`, `suggested_fix`, `source_file` (the JSON or component the fix belongs in, if you can tell).

Severity guide:
- **critical:** breaks indexing or shows wrong or private information
- **high:** 404s, duplicate titles, noindex mistakes, broken structured data, thin or duplicate pages that are approved for launch
- **medium:** weak titles or metas, cannibalization, missing alt text, research text left on the page
- **low:** polish

Before you finish, re-check a random 10% of your findings against the built HTML, so that every finding is real. Then give a short summary in chat with the counts and the path to the report.
