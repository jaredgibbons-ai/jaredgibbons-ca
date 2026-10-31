# Route inventory and validation status

Machine-readable: `routes.json` (seed). Full inventory needs `urls.csv` / `seo.csv` (BL-02). Archive totals as reported: sitemap 1,054 entries / 1,038 unique (637 page, 201 blog, 200 listing); 21,014 inventoried URLs.

| URL | Family | Status | Validation |
|---|---|---|---|
| `/` | home | **implemented (preview)** | Title, canonical, text and links match the archive; see `06-…` |
| `/fort-langley.html` | community | **implemented (preview)** | Matches except documented vendor widgets (D-10); listings are a static snapshot and not connected |
| everything else | — | not started | linked from nav; unbuilt until the importer runs |

Validated = automated archive comparison passes **and** Jared has reviewed. Nothing is "validated" yet.
