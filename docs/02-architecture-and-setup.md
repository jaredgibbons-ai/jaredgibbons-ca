# Architecture and setup

Full reasoning is in `01-direction-for-approval.md` §3. This file is the working summary.

## Stack
- **Astro 5**, static output, `build.format: 'file'` so `/fort-langley.html` is emitted as `dist/fort-langley.html`.
- **Cloudflare Workers with static assets** plus a thin Worker. (Confirm Workers vs Pages against current Cloudflare docs at setup.)
- Fonts self-hosted from `@fontsource` (copied to `public/fonts`). No third-party CSS/JS in the preview.
- Content: archived records → structured content files → page-family templates. Nothing is hand-copied except in this two-page preview; the importer replaces that.

## Why a Worker
`/blog.html` is a page *and* the parent of `/blog.html/<post>-<id>` (same for `/our-listings.html/listing…`, `/fort-langley.html/listing…`). A file host can't hold both. The Worker resolves the exact incoming path through `routes.json`, serves the matching static asset at the **original URL with 200**, handles `?_pg=N`, trailing slashes, `redirects.csv` redirects and a real 404.

## Forms (not built yet)
Worker endpoints → server validation → Turnstile → D1 (store first) → email notification → CRM later. Success is shown only after store + notification accepted.

## Listings / IDX (not connected)
MyRealPage `recip.html`, `/wps/rest/64736/…`, `res.myrealpage.com` and `iss-cdn.myrealpage.com` don't transfer. Needs board feed/licence (BL-04). Listing-detail URLs resolve dynamically. Expired rule: A-03.

## Repo layout
```
astro.config.mjs        site config
src/pages/              index.astro, fort-langley.astro (more via importer later)
src/components/         Header, NavLinks, Footer, PropertyCard (shared by all listing surfaces), Icon
src/layouts/Base.astro  head, skip link, preview chrome, sticky mobile action bar
src/styles/global.css   tokens + base + components
src/data/               nav.json (generated), home.ts, fort-langley-listings.json
tools/                  build_nav.py, compare.py, a11y_perf.py, interact.py, shoot.py
docs/                   project docs; archive-extracts/ = byte-identical copies of the two records used
routes.json             route manifest (seed)
```

## Setup
```
npm install
python3 -I tools/build_nav.py      # regenerates src/data/nav.json from the archive record
npm run build && npx astro preview # or serve dist/
```
Git remote: `origin` = github.com/jaredgibbons-ai/jaredgibbons-ca (`main`, source of truth, A-02). Cloudflare: nothing deployed (BL-07).


## Routing Worker (built 2026-10-31, not deployed)
- `wrangler.jsonc`: Workers with static assets from `dist/`, `run_worker_first: true`, `PREVIEW=true` (adds `X-Robots-Tag: noindex`). No Cloudflare account or token is connected yet (BL-07); nothing is deployed and DNS is untouched.
- `src/worker/route.js` (pure, unit-tested) + `src/worker/index.js` (Cloudflare glue). Rules are data: `src/worker/rules.json`, generated from `redirects.csv` by `npm run rules`.
- Order: host/protocol (http and www to https apex) → exact archive rules (redirect or 404) → trailing slash → static assets → extensionless name to `.html` when that page exists → real 404 (`/404.html`, status 404).
- Tracking (`utm_*`, `gclid`…), CMS preview (`?p=…&preview=true`) and `?_pg=N` params serve the page without redirecting, so analytics keeps the campaign parameters. `?_pg=N` returns the base page until listings are connected.
- Nested content cannot share a name with its parent page on a file system (`blog.html` is a page and the parent of `blog.html/<post>`). Posts are emitted under `/internal/blog/<slug>.html` (done, 200 posts) and own-listing pages will go under `/internal/listings/`; the Worker maps the public URL to them and returns 404 for any direct `/internal/*` request. (Astro ignores `_`-prefixed route folders, so the first-planned `/_blog/` prefix could not be used.)
- Tests: `npm test` (11 tests, node:test, bundles the Worker with esbuild and runs it against `dist/`).
