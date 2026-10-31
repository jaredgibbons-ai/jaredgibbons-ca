# Decisions, approvals and exceptions

Status key: **Approved** (Jared said so), **Applied – needs review** (done in the preview, flagged for Jared), **Proposed** (not applied).

## Approvals on record (2026-10-31)
| ID | Decision | Source |
|---|---|---|
| A-01 | Direction approved. Proceed on Cloudflare as proposed (§3–5 of `01-direction-for-approval.md`, including the interface wording). | Jared |
| A-02 | A free private GitHub repo under Jared's account is the source of truth. | Jared |
| A-03 | Expired listings: keep the page, label it "Expired", noindex it, link to similar active listings. Do not keep other brokerages' MLS photos/details on expired pages. Jared's own listings may keep fuller detail. | Jared |
| A-04 | Preview-first sequence: homepage plus one substantial community page (Fort Langley), then pause for review before scaling. | Brief |
| A-05 | No production DNS change or launch without explicit approval. | Brief |

## Applied in the preview – needs review
| ID | What | Why | Reversible |
|---|---|---|---|
| D-03 | Archive heading outline uses `##` for the page's top level. I read `##` = H1, `###` = H2, `####` = H3. | Only reading that gives one H1 per page. **Verify against `source.bin` when the baseline zips are available.** | Yes |
| D-04 | Primary-nav nesting (which links sit under which parent) is **inferred** from the flat link order plus visible text. Labels and URLs are verbatim. Nav is built by `tools/build_nav.py` from the archive record. | The record lists links flat. | Yes |
| D-05 | Home "OUR LISTINGS" cards and "Search by Area" names are **not** headings (the archive has none there). Fort Langley cards are H3 as in the archive. | Heading fidelity. | Yes |
| D-08 | "As Seen In": 8 image links to `/` with empty alt text are rendered as unlinked tiles. | Empty accessible name (WCAG 2.4.4/4.1.2) and the destination adds nothing. Needs your OK because it departs from exact link preservation. | Yes |
| D-09 | Fort Langley "Nearby …" headings link to the same destination as the card's image link. | Archive has image-only links; headings were not links. Needs your OK. | Yes |
| D-10 | MyRealPage vendor widgets are not rebuilt: Signup/Login, social-login, Contact/Extend/Verify, "Filters". | They exist only inside the MyRealPage IDX. Needs the IDX decision (blocker BL-04). | Yes |
| D-11 | Header brand link is plain text with a visual two-line treatment; the archive outline appears to carry it as an H2 plus an H3 tagline. Accessible name is the full archived string "Jared Gibbons – South Surrey Realtor". Brand link goes to `/` on the home page and `/index.html` on Fort Langley, as archived. | A heading in the chrome before the H1 is a hierarchy error. Recorded, not silently fixed. | Yes |
| D-12 | Fort Langley cards: the archive has two headings per card (full title, and "street postal area"). One heading is rendered. Full title text is preserved via the link's accessible name. | Duplicate heading. | Yes |
| D-13 | Footer keeps "Real Estate Websites by myRealPage" as archived. **This is no longer true once the site leaves MyRealPage.** Proposed: remove at launch. | Wording preservation versus accuracy. | Yes |
| D-14 | Footer and top bar social links have text labels (Facebook, Instagram, …). The archive links are icon-only with no accessible name. Labels are new interface wording. | WCAG 2.4.4. | Yes |
| D-15 | Hero "Search" is a link to `/recip.html`, not a form. The archived form (2 fields) posts to the IDX search. | Never present an unconnected feature as operational. | Yes |
| D-16 | Sticky mobile action bar ("Find a Home", "What's My Home Worth?", call) is rebuilt natively from the lead-tools script. Labels come from that script. | Approved in §10 direction. | Yes |
| D-17 | Preview-only chrome: banner, `.preview-flag` notes, `noindex` meta. All removed by one switch before launch. | Honesty in review. | Yes |
| D-18 | Archive "Edit sidebar contact & social media" is treated as an editor label, not visitor text, and not rendered (B-01). | Looks like admin UI text. | Yes |
| D-19 | **Review stars are gold, everywhere** (user-directed). One token `--star:#a67c00` (3.8:1 on white, 3.2:1 on cream, passes the 3:1 graphic threshold) and one `Stars` component/`.stars` class used for every review. Glyphs are `aria-hidden`; the accessible name is the sr-only "5 out of 5 stars". A brighter gold (e.g. #d4a017) would fail contrast on white (2.4:1), so this is the lightest gold that passes. | Jared's instruction; the archive CSS has no star colour. | Yes: shade |
| D-20 | **Award alt text (B-15).** Jared confirmed the five images are correct. Alt text now describes what each image shows (Years of Service, Top 35 Under 35 (Royal LePage Canada), Rookie of the Year, Top Ten, Red Diamond) instead of the mismatched archived text, so screen-reader and sighted users get the same award. Deliberate, approved exception to verbatim alt preservation (WCAG 1.1.1). | Images confirmed correct. | **Approved 2026-10-31** |
| D-21 | Header logo now uses the supplied logo image (`site-logo.webp`) with the archived alt text "Jared Gibbons – South Surrey Realtor", replacing my text lockup. The JG monogram PNG is used for favicon/apple-touch icon only (its archive location is unconfirmed, OI-13). | Archive header is an image. | Yes |
| D-22 | Trustindex dropped; reviews come from the Google Business Profile API once approved (docs/08). Interim static reviews on `reviews.html`. No star-rating structured data for own reviews. | Jared: "do it ourselves, connected to Google"; owns the profile. | Yes |

## Baseline notes (errors recorded, not corrected)
| ID | Note |
|---|---|
| B-01 | Home record contains "Edit sidebar contact & social media" in visible text. |
| B-07 | Home listings carousel repeats "6469 Meadow Place" as slide 11 (clone). Rendered once. |
| B-08 | Home "As Seen In" has 8 image links to `/` with empty alt. |
| B-09 | Fort Langley "Nearby …" headings are plain text; the first link in each card is an image link with empty text. |
| B-10 | Home nav lists "Buying a Chicken Farm in BC: Quota, BCCMB Transfers & Barn Values" and "…Quota, Costs & BCCMB Transfers" (same URL) and repeats Chicken/Broiler/Turkey/Egg farm links twice under Farms. Preserved. |
| B-11 | Home review text is truncated with "…" in 8 of 10 reviews, and one has a stray space ("informative , helpful"). Preserved exactly. |
| B-12 | Fort Langley FAQ phone link is `tel:6049281361`; all others are `tel:604-928-1361`. Preserved for the one in-text link. |
| B-13 | Home card for 116 Calgary Avenue shows one numeric value (beds vs baths unknown); not rendered. Cards for 12 5327 192 Street and 203 & 210 30610 Progressive Way show no beds/baths. |
| B-15 | Home awards: archived alt text (Award of Merit, Diamond Club, Top 100, Hall of Fame, Platinum Award, file order ww-img01/02/03/2/05) does not match the image content (Years of Service, Top 35 Under 35, Rookie of the Year, Top Ten Award, Red Diamond Award). Images were taken from the live site, not the baseline zips, so the live images may have been replaced after capture. |
| B-16 | `reviews.html` review by Ceilidh ends "3 times now !" (space before !). Preserved. |
| B-14 | Fort Langley and home pages both carry the line "Data was last updated …" / listing snapshot dates that are only true as of capture (2026-10-31). |


## Decisions added with the folder-09 page import (2026-10-31)
| ID | Decision |
|---|---|
| D-23 | Pages beyond the three bespoke previews are generated from the archived page records by `tools/import_pages.py` into JSON and rendered by one generic template. Wording is never edited; reading order is the visible-text order. See `09-content-pipeline.md`. |
| D-24 | The MLS listing grid on community pages (other brokerages' listings) is not retained (A-03). Each grid becomes a "Live MLS® listings … not connected in the preview" slot linking to the archived "Search Listings" destination. 169,626 archive lines fall in these regions. Revisit with the IDX decision (BL-04). |
| D-25 | MyRealPage login / extend / verify widget lines are dropped on every page (D-10): 6,312 lines. The IDX "Filters" control is dropped with the grid. |
| D-26 | The archived Google-review excerpt block (six excerpts, initials only) is kept verbatim as per-page data and rendered with gold stars (D-19). It is replaced by the Google Business Profile feed once approved. |
| D-27 | Forms found in page text (property check, contact form) render as inert stubs with an explicit "not connected" notice and disabled fields until the forms Worker and lead destinations (BL-05) exist. |
| D-28 | Blog posts (200) and the blog index are imported by the same pipeline as other pages (`tools/import_pages.py --kind blog`) into `src/data/posts/`, rendered by `GenericPage.astro`, emitted under `/internal/blog/` and served at `/blog.html/<slug>` by the Worker. Post byline ("Posted on <date> by <author>") is a styled paragraph with the archived text and the author link; post-list titles on the blog index are headings that are also links. | Approved by "keep going" (A-01/A-02 direction); review when you look at the preview |
| D-29 | Mid-clause line breaks caused by inline markup in the archive text (a sentence cut after "its" / "the" / "of" etc.) are re-joined into one paragraph; wording is untouched. | Presentation only |
| D-30 | Own-listing pages (200 records, `tools/import_listings.py`, `src/data/listings/`, emitted under `/internal/listings/`, served at `/our-listings.html/<slug>`) are rebuilt as a structured page: address H1, price/summary H2, label-value facts, room and bathroom tables, feature notes, agent card, "Listed by" credit and the MLS® reciprocity disclaimer, in archive order with no wording changed. Dropped as vendor widget chrome (9,377 lines): share buttons, Details/Photos/Map tabs, Contact/Send/Mortgage/Print buttons, map and Walk Score links, "Schedule a viewing" and add-to-calendar widgets, the lightbox photo captions (kept in the JSON for alt text), and the feed's "Data was last updated" stamp (it would be false on a static page). Exact repeats of a block already shown (summary facts, area statistics, agent card) are shown once. | Needs your OK (departs from line-for-line text) |
| D-31 | All 200 archived listing pages are treated as Jared's own listings (listed by Royal LePage Little Oak Realty or Royal LePage Northstar) and keep full detail under A-03. Three are co-listed with another brokerage (Crosina Realty Ltd., Macdonald Realty (Langley), Sutton Group-West Coast Realty): `listing.2623-216-street-langley-r2946489`, `listing.r2611042-7245-210-street-langley`, `listing.r2747692-4732-dunbar-street-vancouver`. | Confirm these three may keep full detail |
| D-32 | Listing photos (3,252 across 200 pages) are not hotlinked from the MyRealPage CDN. Each page shows a labelled "Photos are not imported in this preview" panel with the archived count until the files are imported from the baseline zips. Active listings carry a notice that status is as captured on 2026-10-31. | Avoids a dependency on the vendor being exited (BL-04) |

## Baseline notes from the page import (recorded, not corrected)
| ID | Note |
|---|---|
| B-17 | On some pages the heading outline order differs from the visible-text order (e.g. `cedar-hills.html`: "Who Cedar Hills suits" is early in the outline, late in the text). Visible-text order is used. |
| B-18 | `lake-city-industrial.html` has no H1 in the archive (outline begins with the brand heading). |
| B-19 | 83 of 634 generated pages carry more than one H1 (archive `##` repeated). Preserved per D-03. |
| B-20 | 6,411 outline headings do not appear in the visible text (hidden or duplicate card headings). Not rendered. |
| B-21 | Jump links such as `#aldergrove-guide-glance` point at section ids that are not in the text records. 1,031 of 1,500 same-page targets were attached to the matching heading; 469 are unmapped (OI-19). |
| B-22 | Three review-excerpt variants exist across 251 pages (200 / 43 / 8 pages). |
| B-23 | `seo.csv` "OG description" contains a literal backslash before an apostrophe (`Langley\'s`) in 98 rows (19 generated pages plus `fort-langley.html`). Preserved exactly as archived in `og:description`. |
| B-24 | On all 200 archived post pages the shared header/footer links are resolved relative to `/blog.html/`, so ~199 per post point to `https://jaredgibbons.ca/blog.html/<page>.html` (e.g. `/blog.html/abbotsford-condos-for-sale.html`), which the archive records as broken at source (403). Likewise `/blog.html/recip.html?showlogin`. The rebuild uses the site-root destinations in the shared header/footer. 39,800 link comparisons are classified `links_nav_relative` rather than missing. Needs your confirmation that the root destinations are what you want. | Open |
| B-25 | On all 200 own-listing pages the shared header/footer links also resolve relative to `/our-listings.html/` (e.g. `/our-listings.html/our-listings.html`), 40,000 comparisons; the rebuild uses the site-root destinations (same treatment as B-24). Two leased listings show an archived redacted rent, `$[***]/mth`, which is kept as archived. |
