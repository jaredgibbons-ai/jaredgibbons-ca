# Content pipeline: archive page records → pages (2026-10-31)

Source: archive folder **09 — Page Text, SEO and Redirects for Claude** (Drive folder `1q8z_ti2AjQ53XZKjSDjxgwZzdc7PX5PY`).
Bulk data is **not** committed (about 29 MB of zips/CSVs). It lives in Drive and in the working cache `cache09/`; only the manifest, `redirects.csv` and generated content are in git.

| Drive file | Bytes (verified) | Use |
|---|---|---|
| `page-text-part-01..05.zip` | 2,899,262 / 2,873,254 / 2,879,329 / 2,900,029 / 2,403,102 | 1,038 `.md` page records |
| `page-text-manifest.csv` | 126,191 | SHA-256 + byte count per record (committed: `docs/archive-extracts/page-text-manifest.csv`) |
| `seo-part-01..06.csv` | 2,899,413 / 2,899,750 / 2,898,649 / 2,899,701 / 2,899,031 / 1,936,635 | full `seo.csv`, header repeated |
| `redirects.csv` | 11,117 | 81 rows (committed: `docs/archive-extracts/redirects.csv`) |

## Verification performed
- Every download matched the Drive byte count. 1,038 of 1,038 page records matched the manifest SHA-256 and byte count (0 missing, 0 extra, 0 duplicate names).
- `seo.csv` rebuilt from the six parts: 13,496 data rows, 15 columns on every row, 13,496 unique URLs (matches the stated total).
- `redirects.csv`: Drive's text view adds two trailing spaces per line and escapes `_`; the file was rebuilt without those artifacts with CRLF endings and checked at exactly 11,117 bytes, 81 data rows, 4 columns, with both ends matching the inline base64 payload.

## Reproduce
```
python3 -I tools/import_pages.py --pages <cache09>/pages --seo <cache09>/seo.csv --out src/data/pages
npx astro build
python3 -I tools/compare_all.py --pages <cache09>/pages --dist dist --out docs/test-results/compare-all.json
python3 -I tools/build_manifest.py
```

## What the importer does (never edits wording)
1. Parses each record (`tools/records.py`): metadata, heading outline (`##`=H1 per D-03), visible-text lines, ordered LINK/FORM/IFRAME list. Section order in the files varies, so sections are sliced by position.
2. Cuts the body from the end of the shared 446-line header nav to the "Ready to get started?" CTA; the shared footer and CTA come from layout components.
3. Drops the MLS listing grid (sort control to reciprocity disclaimer) — other brokerages' data, not retained (A-03, D-24) — and replaces it with a "not connected" slot. Drops MyRealPage login/extend/verify lines (D-10).
4. Matches headings by text (case-insensitive multiset; multi-line headings joined). Visible-text order is the reading order.
5. Re-joins inline links into sentences by aligning the visible-text line sequence with the record's ordered link labels (difflib longest-matching-blocks), plus multi-line anchors as card links.
6. Parses the Google-review excerpt block into six items per page (three variants across 251 pages), recurring form label sets into inert form stubs, and attaches same-page `#fragment` ids to headings where the label clearly matches.
7. Attaches each page's `seo.csv` row (meta description, OG title/description/image, robots, dates) exactly as archived, including trailing spaces.

Generated: `src/data/pages/<slug>.json` (634 files, about 9 MB, rendered by `src/pages/[...slug].astro`); report in `src/data/pages-report.json`.
