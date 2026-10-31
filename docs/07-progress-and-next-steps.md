# Progress and next steps (2026-10-31)

## Done
- First deliverable + Revision 2 (`01-…`), approved.
- Project scaffold, design tokens, shared components, generated nav, two preview pages.
- Automated archive-vs-render comparison, axe, interaction tests, screenshots (`shots/`, not committed).

- Assets integrated (31 Oct): portrait, header logo, 5 award images, 8 As Seen In logos, MLS Reciprocity gif, favicon; all byte-length and decode verified. Fort Langley SEO meta restored. Gold stars (D-19).

- Route manifest (21,014 URLs, 854 canonical routes) and `reviews.html` (third preview page, archive-verified).

## Waiting on Jared
BL-02 (zips + CSVs), BL-03 (Trustindex), BL-04–06. Review of D-08, D-09, D-13, D-15.

## Next, after preview review
1. Importer: archived records → content files; real route manifest; family counts.
2. Forms Worker (contact, home evaluation, guide property check) with delivery tests.
3. Redirects + custom 404 + routing Worker.
4. Remaining page families, then blog, then listing detail once IDX is decided.
5. Images/assets from the baseline zips; Core Web Vitals with real images.
6. Launch checklist (`06-…`). No DNS or launch without explicit approval.

## Update 2026-10-31 (folder 09)
- 634 more pages generated from the archive records (community, guide, price/type search, farm, resource and tool pages), with archive SEO applied. 562 pass the archive comparison with no differences beyond the documented drops; 72 are listed for review.
- Still to do: 200 blog posts + blog index (needs the routing Worker for `/blog.html/<post>`), 207 own-listing pages, redirects/404 Worker (`redirects.csv`, 81 rows), forms Worker, guide-page components (OI-20), review feed, IDX decision.
- Routing Worker + 404 built and tested locally (not deployed): see `02-architecture-and-setup.md`. Blog index and 200 posts are built (`/internal/blog/`, mapped by the Worker). 200 own-listing pages are built (`/internal/listings/`). Next: guide-page components (OI-20), forms Worker, review sync, remaining 50 review pages, forms Worker.
