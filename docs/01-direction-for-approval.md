# jaredgibbons.ca rebuild: first deliverable (direction for approval)

Status: DRAFT for Jared's approval. No production pages built.
Date: 2026-10-31. Source: archive captured 2026-10-31 (monitoring window runs to about 2026-11-14).

---

## Revision 2 (2026-10-31, after the archive owner's fixes)

Read after the fixes landed: rebuilt START HERE guide, LEAD-TOOLS-NOTE.md, TRIPLE-CHECK-FINAL.md, and `jg-lead-tools-v2.js` itself (I decoded the Drive copy: 57,571 bytes, 316 lines, SHA-256 `fac61b30458138b9447bf4988257f80099bb8e823a1043de0fdaa464f638c5eb`; static reading only, never executed).

- **Confirmed fixed:** master guide now shows 21,014 / 13,675 captured / 7,264 pending / 63 redirect / 12 broken, matching the coverage report; folder-03 and screenshots wording corrected.
- **Reported, not verified by me:** 13,509 of 13,509 records hash-match, homepage included (TRIPLE-CHECK-FINAL.md). This replaces the "6,832 of 6,833" figure. I still cannot recompute it until the zips and manifest are on disk (B1). I did not re-read the rebuilt Sheet or urls.csv, so those counts are also unchecked.
- **Not accepted as fully explained:** the gap between 13,675 captured URLs and 13,509 record files is now 166 (it was 179 against 13,496). The explanation offered (robots, sitemaps, feed have no parsed record) covers about five files, not 166. Needs a list of captured URLs with no record, from urls.csv.
- **Script reach corrected:** all 13,509 pages, not 4,675. Analysis in section 10.

---

## 0. What I could and could not inspect

| Source | Result |
|---|---|
| Master guide (Google Doc) | Read in full |
| Archive root + folders 00 to 08 | Listed. Folder 02 confirmed to hold per-page `<slug>.html.md` records (~60 to 115 KB each). I did not count them, so "all 1,038 present" is **unverified** |
| COVERAGE-REPORT.md, backend-gaps.md, FUNCTIONALITY.md, LINKS-REGISTER-NOTE.md, README-03/04/08 | Read in full |
| Folder 07: triple-check-report.md, gap-report.md, crawl.log, robots-live.txt, sitemap-index.xml | Read in full |
| redirects.csv | Read in full (81 rows) |
| Inventory spreadsheet (9 tabs) | **Partial.** Connector returned header, row count and 5 sample rows per tab only. No value counts (status, kind, redirect codes, failure categories) |
| links.csv.gz (121 MB), images.csv (421 MB), forms.csv, seo.csv, urls.csv, failures.csv, assets.csv, assets-manifest.json, SHA256-MANIFEST.txt (14 MB) | **Not read.** Too large for the Drive connector |
| baseline-part01 to 11.zip (~1.6 GB) | **Not opened** |
| `jg-lead-tools-v2.js` | First pass: not read (assets were only in the zips). **Revision 2: now filed in folder 03 and read in full**, see section 10 |
| Homepage PDF (folder 04) | Not opened |
| Page screenshots | Do not exist (documented) |
| Gold star shade, CSS, fonts as archived | Not extracted (CSS is inside the zips) |

Consequence: the hash audit, the lead-tools script analysis, the page-family counts, and the link/image/SEO baselines cannot be verified or finalized until the archive is on a disk I can read. See Blocker B1.

---

## 1. Coverage and count reconciliation

### 1.1 Sitemap math
- Sitemap entries: 653 (page) + 201 (blog) + 200 (listings) = **1,054**.
- 16 duplicates (15 repeated inside page-sitemap.xml, plus `blog.html` in both page and blog sitemaps) leave **1,038 unique URLs**.
- Unique by class per gap-report.md: 637 page + 201 blog + 200 listing = 1,038.
- **The brief's "1,038 = 653 + 201 + 200" does not add up** (that sums to 1,054). The correct breakdown is 637 / 201 / 200.

### 1.2 Routes vs captures vs records
| Term | Figure | Source |
|---|---|---|
| Unique sitemap routes | 1,038 | gap-report.md |
| URLs in inventory (urls.csv, "URLs and status" tab) | 21,014 | Sheet range A1:J21015 |
| Fully captured | 13,675 | COVERAGE-REPORT.md |
| Structured page records (record.json + .md) | 13,496 | COVERAGE-REPORT.md; matches Titles-and-SEO tab (13,496 rows) and per-page Links tab (13,496 rows) |
| Files in backup zips | 89,455 | README-08.md |
| Crawler "phantom" double-path URLs removed from inventory | 7,723 | COVERAGE-REPORT.md; list in phantom-urls.json |

13,675 captured vs 13,496 records: a 179 gap that the docs do not explain (non-HTML captures such as `blog.feed` explain at least 1). Open item.

### 1.3 Status totals: four different snapshots
| Document | Fully captured | Pending retry | Redirect | Broken | Other |
|---|---|---|---|---|---|
| Master guide (first version, since replaced) | 11,699 | 5,714 | 34 | 11 | 3,556 "Excluded dynamic listing content" |
| Master guide (Revision 2) | 13,675 | 7,264 | 63 | 12 | label retired |
| gap-report.md (merged, 20,990 URLs) | 12,848 | 8,077 | 60 | 5 | none |
| COVERAGE-REPORT.md (21,014) | 13,675 | 7,264 | 63 | 12 | none |

Assessment: these are snapshots of a crawl that kept running. **The master guide's numbers are stale** and its "Excluded dynamic listing content: 3,556" bucket does not exist in the later report (that label is applied to listing photos/inventory, not pages). The gap-report and coverage report reconcile: gap-report has 814 non-listing pending, the coverage report says "818 of 819 resolved in the final sweep" (814 + 5 retry-only = 819), leaving the 7,263 listing-detail URLs plus 1 pagination variant pending. I cannot confirm final per-status counts because the Sheet tabs would not return values.

FUNCTIONALITY.md counts are also earlier snapshots: links.csv 6.06M rows (vs 7,181,914), forms 12,797 (vs 15,320), images 1.13M (vs 1.31M), 12,694 parsed records (vs 13,496).

### 1.4 What the 7,263 "pending" listing URLs mean
These are MLS-fed listing-detail URLs. The 1,038 sitemap seeds are all captured, so **no sitemap route is missing**. The pending set is dynamic inventory the rebuild cannot and should not reproduce as static pages (see section 3.4).

### 1.5 Redirects
- Sheet and redirects.csv: **81 rows**. By my count: 65 redirect rows (including one exact duplicate `http://jaredgibbons.ca/`, one duplicate `https://www.jaredgibbons.ca/`, and one malformed concatenated-URL 302) and 16 broken rows (403/404).
- Reported elsewhere: 63, 60, 34, 32. None matches. Unresolved.
- **Conflicting evidence to flag, not guess:**
  - `/esplanade-grande-waterstone-condo-for-sale/` appears as both 301 to `.../notfound.html` and 404.
  - `/recip.html/listing.1550-227-street-langley.105844005` appears as both 301 (to an `?offmarket=true` URL) and 404.
  - `/recip.html/listing.401-15137-33-avenue-surrey-bc-v3z-0y1-r3068640.107376713` same pattern.
  - Expired listings redirect to the generic `/recip.html` (soft-404 behaviour).
  - Two rows are crawler concatenation artifacts (`...our-listings.htmlhttps://...`) and should be discarded, not implemented.
  - `/bc-property-transfer-tax-calculator.html` returns 404 at source.
- Clear, usable page-level redirects: `/contact`, `/contact-us/` to `/contact.html`; `/schools.html` to `/south-surrey-school-catchments.html`; `/mylistings.html` to `/our-listings.html`; the poultry/egg/turkey renames; one blog slug rename; `blog.feed` to `blog.html`; http/www to https apex.

---

## 2. Archive defects and risks

1. **(Superseded by Revision 2: owner reports a full 13,509/13,509 re-run, 0 mismatches; unverified by me.) Original finding: hash audit was weaker than reported.** The "6,832 of 6,833" figure was taken mid-crawl (the check ran while the archive held ~6,519 records and was growing), not against the final 13,496. It is not a sample of the final set; roughly half the final records were never hash-audited per the docs. Re-verification against SHA256-MANIFEST.txt is required.
2. **(Reported fixed in Revision 2: the homepage record now matches its source; to be re-checked from the manifest.) The one mismatch was the homepage**, caused by five URL variants sharing the slug `home` and interleaving writes (record.json from one response, source.bin 339,281 bytes from another). triple-check-report.md lists the fix as pending; the coverage report says it was fixed and verified. I cannot confirm. The live homepage also truncated under load, so a full-body live comparison was never completed.
3. **Master guide is stale** (see 1.3) and says per-page screenshots are in folder 04. Only a homepage PDF is.
4. **Folder 03 does not contain the assets** as individual files. Only manifests and assets.csv. Assets are inside the zips.
5. **crawl.log is a 1 KB fragment** containing a Python crash traceback ("dictionary changed size during iteration") and no completion summary. Folder 07 is not a complete crawl log.
6. **`jg-lead-tools-v2.js` reach was understated.** Reported on "at least 4,675 pages"; the archive owner has since counted it on all 13,509 page records. My earlier inference (about 11.5k) was also low. It is sitewide template code.
7. **Preview URLs in the page set:** `/?p=NNNNN&preview=true` pages duplicate homepage content with their own canonicals (legacy WordPress-era remnants; `post_type=aios-listings` also appears). Not real routes.
8. **Home URL variants** (http/https, www, with and without slash) are separate inventory rows. Trailing-slash forms also exist for `/contact-us/` and `/esplanade.../`.
9. **Sheet quirks:** "Redirect" capture status paired with HTTP 200 (column likely holds the final status); a `data:` GIF listed as an asset URL; Assets-downloaded URLs truncated with "..." in the Sheet; Changes tab empty (monitoring just started).
10. **robots/sitemap naming:** robots.txt points to `/sitemap.xml`; the preserved index is named `sitemap-index.xml`. Confirm they are the same document. `robots.txt` also disallows `/notfound.html`.
11. **Structured data (from FUNCTIONALITY.md counts):** `RealEstateAgent` appears about twice per page; FAQPage on 2,352 pages; `RealEstateListing` on only 12 pages. I have not read the JSON-LD itself, so I cannot yet say whether claims in it match visible content.
12. **`mailto:` lead form on 295 guide pages** posts to the visitor's own mail client: no server, no record of use, unreliable. Must be replaced, which changes behaviour (flag for approval).
13. **Content licensing risk:** archived listing-detail pages contain MLS data. Re-publishing archived listing text or photos as static pages needs board/brokerage permission. See 3.4.

---

## 3. Recommended architecture

### 3.1 Principle
Static-first, content from the archive, with one small Worker for routing, forms and listings. No database-driven CMS.

### 3.2 Stack
- **Astro (static output)** on **Cloudflare Workers with static assets**. Cloudflare is steering new projects from Pages to Workers; confirm against current docs at setup.
- **Import pipeline:** a script reads archived `record.json` + source HTML and writes one structured content file per route (frontmatter: title, meta description, canonical, headings, FAQ, links; body: preserved content blocks in original order). Pages are rendered from page-family templates, never hand-built.
- **Route manifest** (`routes.json`): one row per inventoried URL: exact path, source record, page family, canonical, redirect target if any, implementation status, validation result.

### 3.3 Routing: why a Worker is needed
The URL scheme has `/blog.html` as a page **and** `/blog.html/<post>-<id>` beneath it, and `/our-listings.html/listing.r...`. A static file host cannot hold a file and a directory both named `blog.html`. So:
- Build pages to normalized internal keys (e.g. `/_p/<key>/index.html`).
- A thin Worker resolves the exact incoming path (including `.html`, nested paths, `?_pg=N`) through the manifest and serves the page at the **original URL with 200, no redirect**. Redirects come from a reviewed `redirects.csv` loaded by the same Worker.
- Canonical and trailing-slash behaviour follow the manifest, per route.
- Custom 404 served with a real 404 status.

### 3.4 Listings (needs a decision)
- Search (`recip.html`), the `/wps/rest/64736/...` endpoints, `res.myrealpage.com` widgets and the `iss-cdn.myrealpage.com` image CDN are all MyRealPage-hosted. **They do not move with the site.** Leaving MyRealPage ends the IDX unless a replacement is licensed.
- Recommendation: **do not statically recreate ~17k listing-detail URLs.** Use archived listing pages as the template reference only. Listing URLs (`/<parent>.html/listing.r<MLS#>-<address>.<id>`) resolve dynamically through the new IDX provider; unknown or expired listings follow one rule (to be approved: noindex "no longer available" page with link to the parent search, versus 301 to the parent as MyRealPage does today).
- Provider options to evaluate (none verified yet): a board data licence/feed through FVREB; a board-approved IDX vendor; the national DDF route. Each needs permission, attribution and display-rule checks, plus Royal LePage brokerage sign-off.
- Until then the site ships with search and listing blocks **clearly marked not connected** in staging, and never presented as live.

### 3.5 Forms
Forms are Worker endpoints with: server-side validation, Cloudflare Turnstile, a database record of every submission (D1) as the system of record so no lead is lost, an email notification, and (once chosen) a push to the CRM. Success is shown only after the record is stored and the notification is accepted. Acceptance requires a real end-to-end delivery test.
- Contact form fields as archived: Your email*, Your name*, Your phone number, Subject, Message*.
- Home-evaluation fields as archived: email*, name*, phone, Address, City, Postal / Zip code, Bedrooms, Bathrooms, Size, Features, Notes.
- Guide-page "free property check" (address, name): rebuilt as a real form on the same endpoint, flagged as a behaviour change.
- Routing destinations are unknown (gap #3). Decision needed.

### 3.6 Assets
Original assets in R2 (or committed to the repo if small), served with Cloudflare image resizing for responsive widths. Explicit width/height on every image. Check current Cloudflare image pricing before committing. Fonts self-hosted (Montserrat, Lato) with `font-display: swap` and preloaded subsets.

### 3.7 Editing workflow
No hosted CMS needed. Content lives as Markdown/JSON in Git. Options, in order of recommendation:
1. **Git-backed editor** (Decap CMS or Pages CMS): free, non-technical editing for blog posts and metadata, every change a reviewable commit. Full export is the repo itself.
2. **Claude-assisted edits** via pull requests (fast for you and your assistant).
3. Redirects: one `redirects.csv` in the repo, validated at build (no loops, no chains, no conflicts).
Recurring costs to confirm: Cloudflare Workers plan (likely the paid tier given page volume; verify), email-sending service, IDX provider, domain, Trustindex (if kept). Portability: everything except the IDX is exportable.

### 3.8 Deployment
Git repository, preview deployments per branch (noindex + analytics disabled), production only on your explicit approval. Rollback: keep the previous Worker version and the last good build; one-command redeploy, rehearsed before launch. DNS is not touched without your approval.

---

## 4. Page families (provisional)

Families are inferred from URL patterns and documents read. Per-family counts need seo.csv/urls.csv on disk (Blocker B1).

| Family | Evidence | Examples |
|---|---|---|
| Home | Single route; large page (~339 KB) | `/` |
| Community / neighbourhood pages | Large long-form pages with listing block, FAQ, maps | `/fort-langley.html`, `/seafair.html`, `/king-george-corridor.html` |
| Neighbourhood guides (`-guide.html`) | Long-form guide plus "free property check" form | `/white-rock-guide.html`, `/aberdeen-guide.html` |
| City/neighbourhood indexes | Index lists | `/surrey-neighbourhood-guides.html`, `/south-surrey-neighbourhoods.html` |
| Market / property-type pages | Listing blocks with `_pg` pagination | `/south-surrey-houses-for-sale.html`, `/langley-condos-under-499k.html`, `/farms.html` |
| Farm / acreage / equestrian niche | Farm specific pages | `/chilliwack-poultry-farms-for-sale.html`, `/langley-horse-properties-...html` |
| Open houses | Dynamic listing blocks | `/langley-open-houses.html` |
| Blog index and monthly archives | Large (about 46k words) | `/blog.html`, `/blog.html/archives/2025/04/` |
| Blog posts | 201 in sitemap | `/blog.html/<slug>-<id>` |
| Listing parent pages | Parents of listing routes | `/our-listings.html` (sold via `?cat=SOLD`) |
| Listing detail | MLS-fed | `/our-listings.html/listing.r...` |
| Search app | MyRealPage app | `/recip.html` |
| Lead pages | Self-POST block forms | `/contact.html`, `/home-evaluation.html` |
| Tools | Calculators | `/mortgage-calculator.html`, `/first-time-buyer-calculator.html` (workers.dev iframe) |
| Profile / reviews | Specialised | `/jared.html`, `/reviews.html` (Trustindex widget) |
| Resource / article | Specialised JSON-LD | `/gst-rebate-in-bc.html`, `/bc-landlord-tenant-resources.html` |
| Utility | 404 and redirects | custom 404 |

Non-route captures (preview URLs, `?_pg` variants beyond the real page count, phantom URLs) are tracked in the manifest as "not a route."

---

## 5. Visual direction (uses only the supplied brand)

**Concept: "editorial local guide."** The site reads like a well-set magazine about one place, written by one person.

- **Colour:** #0a0a0a text, headings, buttons, hairline rules; #ffffff base; #f0ece4 for alternating bands and quiet panels; #606060 secondary text only where contrast passes (my calculation: about 6.3:1 on white, about 5.3:1 on cream; to be verified by tooling). Gold only for review stars (archived shade to be extracted from the CSS; stars are never the sole carrier of the rating).
- **Type:** Montserrat for headings, labels, buttons; Lato for body. Fluid scale with a large display heading, tracked small-caps style labels, body 17 to 19px, 62 to 70 character measure. No replacement fonts.
- **Layout:** 12-column grid; wide margins; each page opens with a full-width photograph and a short, well-spaced title block. Long community pages use a narrow reading column with a quiet "on this page" index on desktop and a collapsible one on mobile. Alternating white and cream bands separate sections; 1px black rules, not shadows.
- **Shapes:** square corners everywhere. Black underlined links. Black buttons with an inverted hover state and a 3px offset focus ring.
- **Property cards (one component for buy and sold):** 3:2 image, price in Montserrat semibold, address in Lato, one line of specs, text status label. The Sold variant only swaps status and sold fields. Same type, spacing, borders and buttons.
- **Photography:** deliberate art-directed crops (4:5 mobile, 3:2 and 16:9 desktop); above-the-fold image eager with `fetchpriority=high`, others lazy; explicit dimensions.
- **Navigation:** slim sticky header; search always reachable; on mobile a full-screen menu with three clear paths (Buy, Sell, Communities) plus a persistent search/call bar. Labels reuse archived menu text exactly.
- **Motion:** only subtle fade/translate on reveal and menu transitions; all disabled under `prefers-reduced-motion`.
- **States:** hover, focus-visible, loading skeletons, empty (no listings), error and success, all designed.

### Differences from the archive (to document)
Visual presentation, layout, components and motion change. Content, headings, order and links do not. Archived CSS and the homepage PDF will be compared before build.

### Proposed new interface wording (needs your approval; nothing here replaces archived copy)
- Skip link: "Skip to content"
- Menu button: "Menu" / "Close menu"
- Form states: "Sending…", "Thank you. Your message has been received.", "Something went wrong. Please try again or call 604-928-1361."
- Field errors: "Enter a valid email address.", "This field is required."
- Listings not connected (staging only): "Listings are not connected in this preview."
- Empty listings: "No listings match right now."
- Table-of-contents label on long pages: "On this page"

---

## 6. Blockers vs launch requirements

### Immediate blockers (stop independent work)
- **B1. Archive on disk.** I cannot read the zips, manifest or CSVs through Drive. Needed: the baseline zips and folder 01 CSVs downloaded to a folder on your computer and shared with me (device folder access), or a ZIP uploaded to this chat. Unblocks: hash verification, `jg-lead-tools-v2.js` analysis, family counts, SEO/link baselines, CSS and gold shade.
- **B2. Approval of this direction.**

### Not blockers (do not hold design/migration work)
IDX provider, form routing, DNS, analytics account access.

### Launch requirements
- IDX/MLS licence, display rules and Royal LePage approval
- Verified form destinations and an end-to-end delivery test
- Redirects reconciled
- Production robots.txt and sitemaps generated from the approved route list
- Analytics verified (one GA4/Ads config, one Meta Pixel, no double page views)
- DNS, SSL, monitoring, rollback rehearsal, and your explicit go-ahead

---

## 7. Exports, decisions and secure configuration

### From MyRealPage (authorized export or account access)
1. Pages incl. drafts and scheduled posts
2. Redirect rule table
3. Form definitions and notification settings (recipients, autoresponders, spam settings)
4. Media library originals not publicly referenced
5. Admin user list (for the decommission checklist)

### Not obtainable from MyRealPage (other parties)
- IDX/Paragon feed terms and any saved-search definitions (FVREB/brokerage)
- GA4, Google Ads, Meta account-level settings and conversions (those accounts)
- DNS, SSL, registrar access, email SPF/DKIM/DMARC (registrar/host)
- Trustindex widget account (reviews)

### Decisions from you
1. Are you leaving MyRealPage entirely, and is there a contract/notice period and an export clause?
2. IDX route (see 3.4) and who at Royal LePage approves it.
3. Lead destination(s) for the contact, home-evaluation and guide forms.
4. Expired-listing behaviour (noindex notice vs 301).
5. Keep or replace the Trustindex widget; keep the workers.dev calculator iframe or move it into the site.
6. Approve behaviour change for the `mailto:` guide form.
7. Approve the interface wording in section 5.

### Secure configuration (never pasted in chat)
Cloudflare API token (scoped), Turnstile site/secret keys, email-service API key, IDX credentials, CRM credentials: all set as Worker secrets or in the provider dashboard.

---

## 8. Acceptance criteria and implementation sequence

### Acceptance criteria (measurable)
- **Routes:** 100% of the 1,038 sitemap routes in the manifest; every one served at its exact original URL with the correct status; zero unexplained 404s from the archived link register.
- **Content fidelity:** automated comparison against each archived record: title, meta description, canonical, H1/H2 order, visible text, link text and href. Zero unexplained differences. Only documented equivalences (HTML entity encoding) normalized.
- **Redirects:** every documented redirect passes; conflicting evidence listed, not implemented.
- **Forms:** server-side validation tests; spam test; real delivery to a verified destination for each form, with timestamps.
- **Analytics:** exactly one page view per navigation; GA4, Ads and Meta IDs match archived source; staging sends nothing.
- **Indexing:** staging noindex plus authentication; production robots and sitemaps generated from the manifest and checked at launch.
- **Performance (lab, representative templates):** LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1. Field data reported separately at the 75th percentile when available.
- **Accessibility:** WCAG 2.2 AA checks (keyboard, focus, contrast, labels, errors, targets, reduced motion, 200% text); automated scan plus manual pass on each family.
- **Status reporting:** each page marked implemented, validated, blocked or failed. Compiling is not completion.

### Sequence
0. Approval of this document; archive onto disk (B1).
1. Verify archive: manifest hashes, homepage re-capture, final counts, script review. Repo and project docs created.
2. Import pipeline and manifest; family classification with real counts.
3. Design tokens and components.
4. **Private preview:** homepage plus one substantial community page (desktop and mobile, nav, search UI, FAQ, form states). **Pause for your review.**
5. Scale by family (guides, markets, blog, utility), validating each against its record.
6. Forms, calculators, redirects, 404.
7. IDX integration when licensed; listing routes.
8. Analytics, SEO outputs, performance and accessibility passes.
9. Launch checklist, rollback rehearsal, your approval. DNS only then.

---

## 9. What I need from you now
1. Approve (or change) sections 3 to 5.
2. Put the archive on your computer and share the folder with me (B1).
3. Answer decisions 1 to 4 in section 7 when you can; none blocks the first preview.
4. Decide the lead-tools items in section 10.

---

## 10. `jg-lead-tools-v2.js`: what it does and what to do with it

Evidence: the script itself (316 lines, read in full) plus the archive owner's note. It is sitewide on all 13,509 captured pages. It is **not** in the archived static HTML; it builds its UI at runtime, so none of this appears in the folder-02 records.

**Dependencies.** No third-party endpoints and no external URLs. It uses the page's own MyRealPage form system, `fetch`, `DOMParser`, `IntersectionObserver`, `localStorage` (keys `jglt_pv`, `jglt_done`, `jglt_closed`, `jglt_auto`), and `window.gtag` if present. No Meta Pixel calls.

| Part | What it does | Evidence | Recommendation |
|---|---|---|---|
| Sticky quick-actions bar (`#jg-cta`) | "Find a Home · Home Value" tab opening Find a Home (`/map-search.html`), What's My Home Worth? (`/home-evaluation.html`) and a call link (604-928-1361). Opens on hover and click, closes on Escape/outside click; docks aside on the homepage as sections scroll in | Lines 2 to 24 | **Rebuild natively** as part of the header/mobile bar (server-rendered, keyboard-first, no hover-only behaviour). Keep labels exactly. Confirm `/map-search.html` exists as a route in the manifest (not yet checked) |
| Slug-based lead modules | Classifies each page from its URL slug (area, city, property type; listing-detail URLs excluded) and inserts modules | `JGLT_detect` rules | **Rebuild as build-time config per page family**, not runtime slug sniffing |
| Listing-alerts box | "Get new [area] [type] emailed to you / Be first to see new listings. No spam, unsubscribe any time." Confirmation starts "You're on the list." | Lines 142 to 144 | **Hold.** The script does not create any alert subscription; it posts a message into the contact form. The copy promises an alert feed and unsubscribe that this code does not provide. Needs your decision: connect it to a real alert system (IDX saved search or CRM) or reword. Wording changes need your approval |
| First-time-buyer tap quiz | Multi-step quiz, placed only on condo/townhome feeds, calculator, mortgage, rebate, PTT and first-time-buyer pages; never on seller, evaluation, contact, acreage, farm or 55+ pages | Quiz code | **Rebuild** as an accessible component on the same placement rules, submitting to the new form endpoint |
| Review quotes | Four Google-review excerpts (buy, sell, first-time, downsizing) hard-coded in the script, two truncated with "…" | `REV` object | **Port as static data** only after you confirm they are current and may be shown; keep wording exactly, truncations included. Do not extend or complete them |
| Call link plus Text link | Adds a "Text" link beside in-content call links | `addText` | **Rebuild natively** |
| Auto-prompt dialog | After 2+ page views or about 45 seconds (desktop; phones wait for a second page view and about 8 seconds), once per visitor, with a 30-day quiet period after closing; never on contact or evaluation pages | `autoPrompt` | **Recommend not porting by default.** It is an unrequested interruption that works against the brief's restraint and hurts INP and accessibility. Port only if you want it |
| Form submission (`mrpPost`) | Fetches `/contact.html`, extracts the form token, and POSTs to the MyRealPage "Get in touch" form; on failure falls back to a `mailto:` (jaredgibbons@royallepage.ca) or SMS "One more tap to send" screen | Lines 239 to 270 | **Do not port. Replace** with the Worker form endpoint. This also confirms the contact form "Get in touch" is the real lead path, but not where it routes |
| GA4 events | `jglt_popup_open` and `jglt_lead` (via `mrp` or `mailto`) | Lines 181, 259 | **Keep the event names** so reporting continues; whether they are marked conversions in GA4 or Ads is not in the archive |

**Defects and risks found in the script**
1. Its header comment says "v1 (MOCKUP, not live)" but it is live sitewide.
2. Outside `jaredgibbons.ca` it runs in `demo` mode and **shows a "Thanks, got it!" success without sending anything**. This is exactly the fake-success pattern the brief forbids; the rebuild must never do this, including on staging.
3. Success on the live site is judged only from response headers (`X-Success-Message`, `X-Success-URL` or a redirect). Delivery to a person is unproven by the archive.
4. A failed or timed-out (12 s) post silently opens the visitor's mail app and shows "One more tap to send"; there is no record on your side when that happens.
5. Several modules write page-derived text (area names from the URL) into the page with `innerHTML`; low risk since it comes from the slug, but a port must escape it.

**Acceptance test for any ported part:** behaves identically to the archived source on the same page family (placement rules, copy, dismissal), passes keyboard and screen-reader checks, and each form submission reaches a verified destination in a live delivery test.
