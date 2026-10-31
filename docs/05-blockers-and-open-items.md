# Blockers and open items

## Blockers (need Jared / archive owner)
| ID | Blocker | Blocks | Who |
|---|---|---|---|
| BL-01 | Create an **empty private** GitHub repo (suggest `jaredgibbons-ca`, no README) and tell me its name. The sandbox GitHub token is invalid, so I can't create it. Work is committed locally and will be pushed once the repo is attached. | Source of truth | Jared |
| BL-02 | **Update 2026-10-31:** files are in Drive (`baseline-part01…11.zip`, ~1.6 GB; `urls.csv` in folder 01 is newer than the zip copy). The Drive connector can't move anything over about a few MB (`urls.csv` 7 MB and `seo.csv` 16 MB both fail; zips are 107–177 MB each) and the shell can't reach Drive (403). Needs small extracts instead, see `07-…`. `redirects.csv` (11 KB) did come through. Original ask: put the baseline zips (HTML/CSS/images) and the folder-01 CSVs (`seo.csv`, `urls.csv`, `redirects.csv`) where I can read them. The Drive connector can't pull large CSVs, zips or the 14 MB manifest. | Image/logo assets, archived CSS (star gold), meta descriptions, family counts, full redirect map | Archive owner |
| BL-03 | Trustindex: keep the widget on `reviews.html` or drop it. **Recommendation: keep it for now, loaded lazily.** Home reviews are in the archive as plain text, but `reviews.html` is not yet read. | Reviews page | Jared |
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
