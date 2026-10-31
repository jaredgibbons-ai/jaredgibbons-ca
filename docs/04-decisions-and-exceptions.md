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
| D-20 | **Award alt text vs image content (B-15).** Archived alt text kept verbatim for now. Recommend changing the alt to describe what each image shows, because screen-reader users currently hear a different award than sighted users see. | Preservation rule vs WCAG 1.1.1. | **Needs decision** |
| D-21 | Header logo now uses the supplied logo image (`site-logo.webp`) with the archived alt text "Jared Gibbons – South Surrey Realtor", replacing my text lockup. The JG monogram PNG is used for favicon/apple-touch icon only (its archive location is unconfirmed, OI-13). | Archive header is an image. | Yes |

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
| B-14 | Fort Langley and home pages both carry the line "Data was last updated …" / listing snapshot dates that are only true as of capture (2026-10-31). |
