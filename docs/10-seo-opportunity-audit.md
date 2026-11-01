# 10 — Commercial SEO opportunity audit (2026-11-01)

Written as a commercial SEO specialist would: what exists, what is missing, what each gap is worth, what it takes, and what blocks it. Companion files: `tools/coverage_audit.py` (re-runnable), `docs/research/coverage-matrix-2026-11-01.csv`, Muse's keyword plan (`docs/research/muse-keywords-2026-11-01.csv`, now 78 rows with Uptown NW and Sapperton added) and the five competitor-gap files.

## 1. What the site has today
- 853 archive pages and posts. 122 are neighbourhood guides; 148 neighbourhood pages are under 300 words.
- Coverage is concentrated in Surrey, South Surrey, Langley, Abbotsford, Chilliwack, Maple Ridge, Mission, Ladner and Tsawwassen.
- Audit matrix (36 places × 18 page types): 156 of 648 cells are present. The matrix over-counts gaps in two places: combined pages such as `south-surrey-white-rock-*` are not credited to White Rock, and many cells (a mobile-home page for Whistler) are not real opportunities. Use it to find patterns, not as a to-do list.

## 2. The gaps that matter, in order of commercial value
| Rank | Opportunity | Why it ranks here | Needs |
|---|---|---|---|
| 1 | **Seller pages per city** (`/sell-my-house-in-<city>.html`). None exist except Langley's "sell fast" page. | Highest-intent searches ("sell my house in X", "X home evaluation", "best realtor in X"); every city in Muse's plan carries these keywords; leads convert to listings. | City facts from official sources, board price data (built), Jared's own terms and process wording, tax page |
| 2 | **Missing sub-areas under correct parent** (51 from `missing-areas.csv`, 2 new in the latest plan). Hope, Harrison Hot Springs, Agassiz, Kent and Cultus Lake areas have no pages at all. | Searches for these places currently land on other agents' pages; Muse's competitor files show thin competition in the east valley. | Official area lists (board check done), local facts |
| 3 | **Guides below the 70% uniqueness target** (99 of 122). | Duplicated text across same-city guides is the main quality risk. | Board and Paragon numbers; first-hand notes from Jared |
| 4 | **Market-stats pages per city, refreshed monthly.** One exists for the Fraser Valley. | Repeat-visit and link-earning content; the data layer now exists (`tools/parse_market.py`, `tools/apply_market.py`). | Monthly board packages; Paragon for CADREB areas |
| 5 | **Property-type depth in strong cities**: duplexes, 55+, mobile homes, acreages for Fort Langley, Aldergrove, Walnut Grove, Willoughby, Murrayville, Langley City, White Rock, North Delta, Mission. | Long-tail volume; mobile homes especially (see D-39/D-43). | **IDX route (BL-04)**. Without live listings these are content pages only, so build them only where there is original, sourced content (rules, costs, parks). |
| 6 | **Moving-to, commute, and school-catchment pages** (Surrey, Langley, Abbotsford, Chilliwack, Maple Ridge, Delta). | Relocation searchers; strong internal-link hubs. | District catchment maps and TransLink/Highway data (sourced) |
| 7 | **New construction / presale pages** (only South Surrey and Langley exist). | Buyer intent with fewer good local sources. | Developer/project data; verify before naming projects |
| 8 | **Metro Vancouver pages** (Burnaby, Richmond, Coquitlam, Tri-Cities, North Shore, Vancouver). Home-for-sale pages only. | Large volume, heavy competition, outside Jared's core market. Built last but to the same bar (D-42, D-44). | Same as above; Muse gap files exist |

## 3. Technical and structural items
- **Done:** sitemap.xml and robots.txt endpoints (closed in preview, open with `PUBLIC_LAUNCH=1`); FAQPage and BreadcrumbList JSON-LD on local-layer pages; new-page loader (a new page is one `src/data/local/<slug>.json` with a `new_page` header).
- **To do:** `RealEstateAgent` and `WebSite` JSON-LD on the home page (no self-serving aggregate rating); automatic breadcrumbs on all pages; hub pages linking every child (city hubs → sub-areas → sell page); `llms.txt`; image alt/size review; remove preview noindex at launch only with Jared's approval.
- **Speed:** cache headers (immutable hashed assets, revalidated HTML), delayed analytics loader, speculation rules, performance budget tests, R2 photo route.

## 4. Rules for creating pages (so volume does not become thin content)
1. No page ships as indexable without original, sourced content: each page carries sections that exist on no other page, and numbers carry date and source.
2. A page needs a real reason to exist. If a listing grid is the only content (IDX pending), it waits.
3. No claim about Jared (fees, process, awards, volume) unless he supplied it.
4. Metro Vancouver pages are built last but not as lesser pages.
5. Pages start as `status: draft` with a visible notice until approved.

## 5. Built so far from this audit
- Page loader for new pages and sitemap inclusion.
- `/sell-my-house-in-maple-ridge.html` (draft pilot; template for the remaining seller pages) and `/sell-my-house-in-pitt-meadows.html` (draft, D-52); Mission, Abbotsford and Delta followed (D-53), then Surrey, South Surrey and White Rock, and Langley (D-54); Chilliwack is the remaining city.
- Market data layer feeding four guides and the pilot.
- `/homes-with-multiplex-potential-fraser-valley.html` (draft): the matrix's biggest gap, with verified city rules and links to 21 neighbourhood guides (D-48). Backlog of 25 areas with no page recorded.
- Presale pages (draft): hub of 134 projects plus Surrey, Abbotsford, Burnaby, Coquitlam and Vancouver pages, and project tables on the Langley and South Surrey presale pages (D-47). Closes most of rank 7.
- `/fraser-valley-short-term-rental-and-suite-rules.html` (draft): verified short-term rental and multi-unit zoning rules for six eastern and Fraser Valley places (D-46).
- `/fraser-valley-commercial-market-report.html` (draft): GVR Commercial Edge Q2 2026 and Avison Young industrial Q3 2026, three tables, linked from `/commercial.html` (D-45). Commercial is a side mission (Jared, 2026-11-01), not a main line. It is a new opportunity row: no competitor-gap research exists for it yet, so it needs a Muse pass before per-city industrial pages are built.

## 6. Open items that block the next tier
- A fetch of the CRA principal-residence page was declined; the tax section waits for Jared to approve a source or supply wording (OI-31).
- Paragon sold-history exports for medians, days on market and sale-to-list ratio (Muse/Jared).
- Jared's seller terms and marketing package wording.
