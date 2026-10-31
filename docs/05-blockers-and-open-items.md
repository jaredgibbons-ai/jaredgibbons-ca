# Blockers and open items

## Blockers (need Jared / archive owner)
| ID | Blocker | Blocks | Who |
|---|---|---|---|
| BL-01 | ~~GitHub repo~~ **Resolved 31 Oct:** `jaredgibbons-ai/jaredgibbons-ca` attached; full history pushed to `main`. (Confirm it is set to private.) |
| BL-02 | **Update 2026-10-31:** files are in Drive (`baseline-part01…11.zip`, ~1.6 GB; `urls.csv` in folder 01 is newer than the zip copy). The Drive connector can't move anything over about a few MB (`urls.csv` 7 MB and `seo.csv` 16 MB both fail; zips are 107–177 MB each) and the shell can't reach Drive (403). Needs small extracts instead, see `07-…`. `redirects.csv` (11 KB) did come through. Original ask: put the baseline zips (HTML/CSS/images) and the folder-01 CSVs (`seo.csv`, `urls.csv`, `redirects.csv`) where I can read them. The Drive connector can't pull large CSVs, zips or the 14 MB manifest. | Image/logo assets, archived CSS (star gold), meta descriptions, family counts, full redirect map | Archive owner |
| BL-03 | **Decision 2026-10-31: drop Trustindex; use Google Business Profile API (access request in `docs/08-…`, Jared submitting).** Interim: archived reviews shown as static content. Original: | Trustindex: keep the widget on `reviews.html` or drop it. **Recommendation: keep it for now, loaded lazily.** Home reviews are in the archive as plain text, but `reviews.html` is not yet read. | Reviews page | Jared |
| BL-04 | IDX route: new board feed/licence, or another provider, with Royal LePage sign-off. Is Jared leaving MyRealPage entirely? | Every listing surface, search, map, signup/login | Jared / brokerage |
| BL-05 | Lead destinations: where should contact, home-evaluation, newsletter and the free-property-check form submissions go (email address, CRM)? | Forms go-live | Jared |
| BL-06 | Lead-tools decisions: listing-alerts box (no alert system exists), review quotes, auto-popup. | Native rebuild of those modules | Jared |
| BL-07 | Cloudflare: a scoped API token entered through Cloudflare's/my secure setup (never in chat) for a live private preview URL. Not needed for screenshots. | Live preview URL | Jared |

## Open items
| ID | Item |
|---|---|
| OI-01 | Hash verification: 13,509/13,509 reported by the archive owner, not independently re-verified by me. |
| OI-02 | Gap of 166 between captured URLs and record files; the explanation offered covers only about 5. |
| OI-03 | ~~Fort Langley meta~~ **Resolved.** Title, description, robots, OG title/description/image restored from `seo-home-and-fort-langley.csv`. Description keeps its trailing space. The CSV viewer shows `Langley\'s` and `\_media`; I treated the backslashes as export escaping (same pattern as `\#1` in the home row). Confirm against the raw `seo.csv` when it is available. |
| OI-04 | Page-family counts need `seo.csv` / `urls.csv` on disk. |
| OI-05 | ~~Gold star shade~~ **Resolved by instruction** (D-19): `#a67c00`. |
| OI-06 | Whether `/map-search.html` is a route in the manifest (it is linked sitewide). |
| OI-07 | Home "OUR PROVEN PERFORMANCE" figures and award images were not captured as text. |
| OI-08 | Portrait, logo (header), "As Seen In" logos, award images, Reciprocity logo: images are in the baseline zips. Preview shows labelled placeholders. |
| OI-09 | Heading level mapping (D-03) to be confirmed against `source.bin`. |
| OI-10 | Redirect row counts disagree across reports (81 rows; about 65 redirects + 16 broken by my count). Three conflicting 301-vs-404 rows listed in `01-direction-for-approval.md`. |
| OI-11 | Hero "Search" form fields (2 fields) unknown until `source.bin` is available. |
| OI-12 | As Seen In logo order follows the supplied file numbering (craigslist, REW, realtylink, LoopNet, Spacelist, REALTOR.ca, Royal LePage, kijiji); confirm against the live carousel. Logos are trimmed of white space and converted to WebP. |
| OI-13 | JG monogram PNG: archive location unknown (used for favicon only). Header logo `site-logo.webp` is 370×166. |
| OI-14 | Award image set is on dark tiles because the artwork is white on transparent; confirm the archive's tile background. |
| OI-15 | `reviews.html`: no star ratings in the archived text for the six reviews. Stars are not rendered until confirmed (will be gold, D-19). The home page's ten reviews do carry ★★★★★ in the archive. |
| OI-16 | `reviews.html` says "More reviews are shown below" but only six reviews were captured; the rest were loaded by the Trustindex script. Replaced by the Google feed (BL-03). |
| OI-17 | `reviews.html` meta description, robots and OG tags are in `seo.csv` (16 MB) and not yet retrievable. Title and canonical are applied. The same gap applies to all ~850 pages. |
| OI-18 | **Page content for the other ~850 pages:** readable `.md` records for all 1,038 sitemap pages are in archive folder 02, one file each. Fetching them one by one through the connector would mean hand-copying text, which risks breaking the verbatim rule. Needs a bundle (see message to Jared). |

| OI-17a | **Resolved 2026-10-31:** `seo.csv` is in folder 09; meta description, robots and OG tags are applied to all 634 generated pages (0 mismatches). `reviews.html` and `fort-langley.html` meta restored from it (reviews: description, OG title, OG image; robots empty in the archive). |
| OI-18a | **Resolved 2026-10-31:** page records for all 1,038 sitemap pages are in folder 09 and hash-verified. 634 pages are generated; 200 blog posts and 200 own-listing records are next. |
| OI-19 | 469 same-page `#fragment` link targets (e.g. `jg-overview`, `jg-market-snapshot`, `jg-related-areas`, `jg-seller-cta`, `jg-local-guide`) have no matching heading in the text record. Links work as page links but do not scroll to a section until the source ids are known. |
| OI-20 | Guide and market pages (about 150) use components that arrive as flat text: label/value cards, school/park cards, tables, the property-check form. Text, headings and links are complete, but the layout is the generic text rendering. Bespoke components are the next design pass. |
| OI-21 | 50 link destinations (<0.1%) and 34 card-internal headings are not yet rendered (was 292 before the second-pass link pairing): image-only links with no label (e.g. "nearby area" image cards) and external links inside school/park cards. Listed per page in `docs/test-results/compare-all.json`. |
| OI-22 | Forms in page text: 149 eight-field POST forms, 48 mailto forms, 53 twelve-field GET search forms and others. All inert until the forms Worker (BL-05). |
| OI-23 | 16 pages exist only in discovery (no sitemap record): `/about.html`, `/bolivar-heights-guide.html`, `/bridgeview-guide.html`, `/cedar-hills-guide.html` and 12 more. Content not captured; need records from Jared. |
| OI-10a | **Redirect rules implemented 2026-10-31** from `redirects.csv` (all 81 rows accounted for): 3 host rows, 56 path redirects, 12 "broken at source" (404), 3 conflicting rows, 2 malformed rows. **Decision needed:** the 3 conflicting URLs (`/esplanade-grande-waterstone-condo-for-sale/`, `/recip.html/listing.1550-227-street-langley.105844005`, `/recip.html/listing.401-15137-33-avenue-surrey-bc-v3z-0y1-r3068640.107376713`) list both a 301 and a 404; the Worker serves 404 until you choose. The 2 malformed rows (two URLs glued together by the crawl) are ignored. 23 of the 56 redirects point at `/recip.html/listing.*` IDX pages that will 404 until listings are connected (BL-04). |
| OI-24 | `404.html` is new copy (not archived): "Page not found", a one-line explanation, links to Home / Search Listings / Contact and the phone number. Please approve or edit. |
