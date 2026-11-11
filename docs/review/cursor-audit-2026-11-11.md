# Cursor audit, 11 November 2026

Report-only audit of the local launch build (`PUBLIC_PREVIEW=false`, output `dist-launch`). The live jaredgibbons.ca site was not opened. Nothing under `src/`, `tools/` or `tests/` was edited.

## Summary

887 findings after a second pass that dropped checker mistakes and documented decisions. By severity: **critical** 1, **high** 199, **medium** 599, **low** 88.

| Severity | Count | What it means here |
| --- | --- | --- |
| critical | 1 | A title that names the wrong property |
| high | 199 | Wrong article titles, thin or near-duplicate pages that are indexable, listings nobody links to, FAQ schema that does not match the page |
| medium | 599 | Weak or cut-off titles and descriptions, http source links, research notes a buyer can read, the unsourced "Top 1%" line |
| low | 88 | Polish: titles of 61–65 characters, a short menu button, a few photos that should be lazy-loaded |

The launch build is in good shape on the things that decide whether Google can crawl it. 1,905 HTML pages, 1,902 of them indexable. The sitemap has those 1,902 URLs, each with `lastmod` 2026-11-11, and none of them is noindex. `robots.txt` allows the site, points at the sitemap, and does not block CSS, JS or images. Every indexable page has one H1 and a self-referencing canonical on `https://jaredgibbons.ca/`. The only held page, Mt Lehman, is noindex and out of the sitemap. `npm test` passed 160 tests and skipped 2. The uniqueness tool found no new page and no guide under 0.70.

### The 10 fixes that would gain the most SEO value

1. **Fix the listing title that names the wrong house.** `listing.r2722542` is 20543 28th Avenue, Langley. Its title says 20441 2 Avenue, Brookswood.
2. **Make three blog titles match the article.** The South Surrey price-drop title is an Aldergrove listing. The Chilliwack housing-targets title wears a Bank of Canada H1. "March 2025 Real Estate News" is a Coquitlam presale post.
3. **Give the city-swap titles a real hook.** 33 title patterns differ only by the place name. Ten cities share "Condos under $600,000 | Apartments for sale". Twelve share "Houses with suites for sale | Prices and rules".
4. **Stop cutting blog titles and descriptions.** 36 titles are over 65 characters, 3 end mid-word on an ellipsis, 7 are under 30 characters, 78 descriptions end on "…", and 50 descriptions are under 120 characters.
5. **Raise or noindex the 8 indexable pages under 0.70 unique wording.** Lowest is Maple Ridge farms at 0.673. The uniqueness gate is switched off (D-56), so these stay in the sitemap.
6. **Link the 91 own-listing pages that nothing points to, and thicken the thin pages.** Testimonials is 63 words. The subscribe page is 172. Contact is 213. Seventeen blog posts are under 300. `our-listings.html` links 23 listings.
7. **Make the FAQ schema match the words on the page.** 24 pages mark up a question or answer that is not on the page word for word, so the FAQ rich result is not valid.
8. **Remove the research notes a buyer can still read.** "Not asserted", "Queued", "in this batch", "flagged:", and "Page-statement check / Approved claims" are still in the launch HTML on a few dozen pages.
9. **Switch 288 http:// source URLs to https://.** Those URLs are used 775 times, mostly on city, school-district and provincial sites. www.delta.ca accounts for 29 of the distinct URLs.
10. **Name the basis for "Top 1%" and compress the heavy files.** The footer and the home hero state the ranking with no source beside it. Thirteen photos are over 300 KB. `zonings.html` is 333 KB of HTML. Search and school pages download about 1.7–2.0 MB because of the MyRealPage embed.

## 1. Titles, metas and headings

Checked all 1,905 pages. No missing titles, no missing descriptions, no duplicate titles, no duplicate descriptions, and no page with more than one H1. Archive pages that used to repeat an H1 (B-19) do not do so in this build.

What is wrong:

- One listing title names a different house (critical, above).
- Three blog posts whose title and H1 are different articles (high).
- 3 titles cut off mid-word: "Home in Lan…", "Elegant 6-…", "Just Sold! Thr…".
- 36 blog titles longer than 65 characters, so the fitter could not shorten them (they have no ` | ` segment left to drop). Example: "$12.7M Surrey Water Main & Road Project Unlocks Major South Surrey Growth" is 73 characters.
- 7 titles under 30 characters, including "2024 Inclusion Conference" (25) and "Morgan Heights Real Estate" (26).
- 29 titles of 61–65 characters. The fitter’s cap is 65 (D-200). Google often cuts off nearer 60, so these are polish, not errors.
- 33 title templates that differ only by the city or the school name. The largest are condos under $600,000 (10 pages) and houses with suites (12 pages).
- 78 meta descriptions end on "…" or without a full stop. `fitMeta` in `src/lib/seo.ts` does this when a description will not fit in 158 characters at a sentence end.
- 50 descriptions are shorter than 120 characters. The shortest measured here are in the mid-90s.
- Headings in ALL CAPS in the HTML, not only via CSS: "FIND HOMES BY LANGLEY COMMUNITY", "WHY WORK WITH US", "OUR LISTINGS", "THE BOTTOM LINE", and the home H1 "JARED GIBBONS".
- An h3 whose text is only "Look at", on 55 pages (first seen on the Albion guide, after "Detached Houses").

## 2. Indexing and canonicals

Clean on the rules that decide indexation.

- Launch `robots.txt` is `Allow: /`, `Disallow: /internal/` and `Disallow: /api/`, plus `Sitemap: https://jaredgibbons.ca/sitemap.xml`. It does not block CSS, JS or images.
- Sitemap: 1,902 URLs, no duplicates, every URL is a file in the build, no noindex URL, every indexable page is included. `lastmod` is 2026-11-11 on every URL. That date is the build date. The stored manifest (`src/data/lastmod.json`) is still 2026-11-06 for 1,668 URLs, and this build’s content hashes did not match it, so the integration stamped today. The dates are not in the future and not before 2015.
- Canonicals are absolute and self-referencing on `https://jaredgibbons.ca/`. None point at workers.dev, localhost, or another page. Internal links use the `.html` form the canonical uses. Blog and listing canonicals omit a trailing `.html` (`/blog.html/<slug>`, `/our-listings.html/<slug>`), which matches the worker route.
- Approved pages are not noindex. The held page `mt-lehman-abbotsford-guide` is `noindex, follow` and is not in the sitemap. `404.html` and `photo-credits.html` are noindex. The listing gate currently holds no feed page (none has a 3-month average under 5). No listing in the data is status Expired (A-03). Statuses are Sold 190, Active 11, Leased 2.
- `launch_pack.py` agrees: 848 new pages, 1 held (Mt Lehman, waiting for Jerry’s saved search).

The preview build (`dist/`) is the opposite, on purpose: home is `noindex, nofollow`, `robots.txt` is `Disallow: /`, the preview banner is present, and Mt Lehman shows "Held at launch". None of that is in the launch build.

## 3. Links

Crawled every internal link in the launch HTML.

- No internal link 404s, once `sms:` links and `/listing-photos/…` are set aside. Those photo URLs are served from R2 by the worker and 404 on a local static server. There are 3,706 of them. They are not counted as errors.
- No redirect chains. `src/worker/rules.json` has 84 redirects, each a single hop, and each target is a file in the build.
- No links to other agents, brokerages or listing portals on the `other-agent-domains.json` list. The one `realtor.ca` link carries `nofollow`.
- No links to workers.dev, localhost, Google cache, or an unlabelled archive.org URL.
- 288 distinct `http://` source URLs (775 uses across the pages). Top hosts:

| Host | Distinct URLs |
| --- | --- |
| www.delta.ca | 29 |
| www.city.burnaby.bc.ca | 12 |
| www.portmoody.ca | 11 |
| www.surrey.ca | 11 |
| infomaps.translink.ca | 11 |
| www.burnaby.ca | 10 |
| vancouver.ca | 9 |
| www.vpl.ca | 9 |
| covapp.vancouver.ca | 7 |
| www.mapleridge.ca | 6 |
| www.portcoquitlam.ca | 6 |
| www.fvrd.ca | 6 |

- Anchor text: a handful of links use the raw URL as the text (ALC and Township of Langley pages), and one uses "learn more".
- Orphans: 91 own-listing pages have zero inbound links. 174 blog posts are linked only from the blog index. 76 other listings have a single inbound link. Lake City Industrial has one.
- Guides: none has fewer than 5 internal links out.
- Ten fragment links point at an id that is not on the page (`#aberdeen-guide-schools` and four `#jgl-` ids on the landlord-tenant page, among them). B-21 recorded this class of jump link as unmapped. The ten that remain are listed under decisions.

## 4. Content value

Uniqueness (`python3 -I tools/uniqueness.py --csv /tmp/uq.csv`): 1,498 scored pages, 8 under 0.70, all indexable. No guide and no brand-new page is under 0.70. The eight:

| Page | Unique | Words |
| --- | --- | --- |
| maple-ridge-farms | 0.673 | 1,671 |
| greentree-village | 0.676 | 1,393 |
| brownstones-at-morgan-crossing | 0.686 | 2,504 |
| maple-ridge-homes-under-1-8m | 0.689 | 1,801 |
| silver-valley | 0.698 | 2,842 |
| abbotsford-duplexes-for-sale | 0.699 | 1,100 |
| aberdeen | 0.699 | 2,904 |
| ladner-condos-for-sale | 0.699 | 1,761 |

Near-duplicates: 902 page pairs share at least 60% of their mid-frequency 8-word phrases (phrases that appear on 2 to 25 pages). Below 90% the long shared run is usually the listing-alert form or the home-value form, which is the same tool on many pages, not a paragraph to delete. 50 pairs are at 90% or more, including three at 100% where two blog posts share the same listing description. Those 90%+ pairs are rows in the CSV. The shared passage is quoted on each row.

Thin pages (20), main text only, nav, footer, reviews and link-only lists removed:

| Page | Words |
| --- | --- |
| testimonials | 63 |
| subscribe-to-our-newsletter | 172 |
| contact | 213 |
| several blog posts | 209–299 |

Keyword cannibalization that is the same search, not just the same city: About Jared (about.html and jared.html), Downtown Vancouver condos (downtown-vw.html and downtown-vancouver-condos-for-sale.html), Burke Mountain homes for sale (the for-sale page and the area page).

Research and process text still visible:

- "not asserted" on 5 guides (Mount Currie, Shaughnessy, SFU, South Arm, S.W. Marine).
- "Queued" as a label on complexes that were not published (Hazelwood Grove, Avalon Mews, The Meadows, and others).
- "in this batch" (or "in the batch") on Caulfeild, Downtown Vancouver, Fairview, Grandview-Woodland, Stave Falls, Websters Corners and the Tsawwassen under-$1.8M page.
- "flagged:" as a researcher’s mark on conflict notes (Kiwanis Manor, Big Bend’s repealed bylaw, boundary flags).
- "Page-statement check" / "Approved claims" on Cloverdale BC, Altamont, Tsawwassen Central, Tsawwassen East, Bridal Falls and Uptown New Westminster. A buyer can read the internal claim list.
- "Muse's file records Zoning Bylaw Amendment Bylaw 2024, No. 5395" on the Chilliwack selling page.
- Kitsilano: "Flags the conflict rather than resolving it."

"Pending sales are not counted" is ordinary methodology, not a leftover note, and is not listed. Chilliwack’s "D-1" to "D-10" are Official Community Plan permit areas, not decision numbers. "Jerry Sulina Park" is a park. "TBD" on the seller FAQ is advice about offer terms.

Superlatives: "The Most Recommended realtor", "Top 1% Fraser Valley" and the h2 "South Surrey's #1 Ranked Realtor" on the home page have no source in the same line. The footer repeats "Top 1% of All Realtors in the Fraser Valley" on every page. Google review quotes that say "the best" are the reviewer’s words and are not listed. Jared’s own tips ("if the best part of the yard…") are his voice and are not rewritten here.

Spelling: no "neighborhood". Hits on "Gray" are Gray Elementary. Hits on "meter" are water meters, which is the device, not the unit metre. "Village Center" is the name on the Cultus Lake Park Board documents.

## 5. Structured data

Every JSON-LD block parses. Types are schema.org types in use here (WebSite, WebPage, RealEstateAgent, FAQPage, BreadcrumbList, Question, Answer, and the address and place types nested under them). No `aggregateRating` and no `Review` markup (D-22).

The RealEstateAgent block on the home page is the only one. Name Jared Gibbons, phone +1-604-928-1361, address #201, 15272 Croydon Drive, Surrey, parent organisation Royal LePage Little Oak Realty. That is the same office as Suite 201 – 15272 Croydon Drive. No second phone or street appears in the schema.

BreadcrumbList names match the visible crumbs. 24 FAQPage blocks contain a question or an answer that is not in the visible text word for word. Example: the landlord-tenant page’s schema says the 2026 rent increase is "up to 2.3%" in a sentence that is not the sentence on the page. The CSV quotes the missing sentence.

## 6. Images and media

- Award images in the marquee have real alt text ("Royal LePage Top 35 Under 35 2025", "Royal LePage Red Diamond Award", and the rest). The looping copy is `aria-hidden` with empty alt, which is the right treatment for a decorative duplicate (D-20).
- Content images carry width and height.
- 13 photos are over 300 KB, all under `/img/areas/`, between 308 KB and 366 KB. The largest is `chineside_01-1280.webp` at 366 KB.
- Eight area photos that sit below the first screen are not `loading="lazy"`.
- `/listing-photos/…` 404s locally. Noted, not counted.
- No content image points at a file that is missing from the build.

## 7. Rendering, mobile and accessibility

Served `dist-launch` on localhost only. Playwright at 390×844 and 1280×900 on 17 templates (home, Fort Langley, a guide, a rules page, a search page, market stats, a school page, reviews, contact, privacy, home evaluation, testimonials, sold, buying, zonings, a blog post, a listing), plus 105 further pages at 390 px across guides, rules, for-sale, schools, stats, blogs and listings.

- No horizontal scroll on any of them.
- Skip link is present and moves to `#main`.
- Contact, privacy and home evaluation render. Their fields have labels. Nothing was submitted.
- No axe-core colour-contrast failures on the templates (WCAG 2 AA).
- The MENU button is 40 px tall, under the 44 px target. Breadcrumb links are about 16 px tall.
- The IDX embed’s frame has no title (axe `frame-title`, serious) on the Langley search page, the school page, and 7 of the sampled pages.
- Console errors on search and school pages are the MyRealPage widget requesting `http://res.myrealpage.com/.../embeddable.less`, which the browser blocks as cross-origin from localhost. Reviews requests `/api/reviews.json`, which the worker serves and a static folder does not. Listing-photo 404s are the R2 paths. No other failed requests.

Preview versus launch: the preview banner, the "Held at launch" note, and `noindex, nofollow` are in `dist/` and absent from `dist-launch`.

## 8. Performance

Lighthouse, mobile, against the local launch server. Lab TBT is 0 ms on these pages (a quiet CPU). CLS is 0 to 0.029.

| Page | Score | LCP | CLS | TBT | Weight |
| --- | --- | --- | --- | --- | --- |
| Home | 94 | 3.0 s | 0 | 0 ms | 336 KiB |
| Fort Langley | 100 | 1.2 s | 0 | 0 ms | 214 KiB |
| Murrayville guide | 96 | 2.3 s | 0.027 | 0 ms | 378 KiB |
| Langley homes for sale | 98 | 1.8 s | 0 | 0 ms | 1,741 KiB |
| Abbotsford buying rules | 98 | 1.8 s | 0 | 0 ms | 277 KiB |
| Surrey market stats | 98 | 2.0 s | 0.007 | 0 ms | 296 KiB |
| Homes near a school | 98 | 2.0 s | 0 | 0 ms | 1,991 KiB |
| Blog post | 99 | 1.7 s | 0.024 | 0 ms | 256 KiB |
| Contact | 98 | 1.8 s | 0.029 | 0 ms | 223 KiB |
| Zonings (heaviest HTML) | 87 | 3.2 s | 0 | 0 ms | 551 KiB |

The home page’s LCP is 3.0 s and zonings is 3.2 s. Search and school pages score well on LCP but weigh 1.7 MB and 2.0 MB because the MyRealPage embed downloads with the page. Fonts are `font-display: swap`. The home page did not flag a render-blocking request. The only HTML file over 300 KB is `zonings.html` at 333 KB.

## 9. Legal and trust

The footer on every page carries "REALTOR® with Royal LePage Little Oak Realty", the office address, the phone, and the MLS® reciprocity paragraph naming GVR, FVREB and CADREB. Listing and sold pages include that footer. The brokerage name is spelled the same way throughout.

The footer also says "Real Estate Websites by myRealPage" and "Top 1% of All Realtors in the Fraser Valley". The ranking has no source beside it. The myRealPage line is discussed under decisions (D-13).

No "Draft", "Private working preview", "preview-flag" or "Held at launch" text is in the launch HTML.

## Decisions worth revisiting

These are choices already written down. They are not listed above as errors.

- **D-13.** The footer still says "Real Estate Websites by myRealPage". The decision says that stops being true once the site leaves MyRealPage, and removal was proposed for launch. It is still in this launch build.
- **D-10 and the IDX embed.** Search pages still load `https://idx.myrealpage.com`. That is why those pages weigh about 2 MB, why the frame has no title, and why the widget then requests an `http://` stylesheet. A native search would remove that dependency.
- **D-56.** The uniqueness gate is off, so the 8 pages under 0.70 stay in the sitemap. Turning the gate on, or rewriting those 8, is the choice.
- **D-200 / `fitTitle`.** Titles are allowed to 65 characters, and a title with nothing left to cut stays over 65. Meta descriptions that cannot break on a sentence end in "…". Both show up in section 1.
- **B-21.** Ten in-page links still point at an id that was never added (`#aberdeen-guide-schools`, `#english-bluff-guide-schools`, `#hawthorne-guide-schools`, `#holly-guide-schools`, and `#jgl-starting`, `#jgl-rent-increases`, `#jgl-ending`, `#jgl-buying-selling` on the landlord-tenant page).
- **D-30 and the listings index.** The rebuild was meant to link Jared’s own listings from `our-listings.html`. That page links 23 of them. The other indexable listings have zero or one inbound link, so they are weak in the crawl even though they are in the sitemap.
- **City-template titles.** They come from the search matrix and they are unique as strings. They are also the pattern the brief asked to flag: the same title with only the city changed. A hook per city would separate them in search results.
- **The approved "Top 1%" claim.** Internal notes say the claim may be used in a form that includes "#1 in South Surrey/White Rock by MLS points for 2025 and 2026 YTD". The public line drops the MLS-points basis. Adding that basis would make the claim checkable.

## What was checked and came back clean

Tests: 160 passed, 2 skipped, 0 failed. Uniqueness: 0 guides and 0 new pages under the 0.70 and 300-word bars. Launch pack: 1 page held, and the launch build noindexes that page. No secrets are printed in this report. A pattern scan for keys and passwords hit test fixtures, form-field names and a GIS page; none of those are credentials, and no value is copied here.

## Spot check

A random 10% of the CSV rows (88 of 887) was checked again against the built HTML. 0 of those checks failed. Rows that did not survive the second pass (false hits on "Royal LePage", award-marquee clones, `sms:` links, listing-photo URLs, "pending sales are not counted", Chilliwack D-1 to D-10 permit areas, and the email-form overlap below 90%) were not written to the CSV.
