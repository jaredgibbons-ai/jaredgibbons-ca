# Prompt for Grok: IDX / listing-embed research (2026-11-02)

Send with: `docs/idx-page-inventory.csv` (654 search, area and building pages by type), `src/data/snapstats/_mapping.json` (our area names vs board names), and screenshots from the listing tool (see "Before you send").

```
ROLE
You are a research analyst for a BC real estate website rebuild. Read official documentation, board rule pages and vendor pages, and report only what a source states. Cite the URL and the date you read it for every fact. Where something is not public, say "not public" and list what the account holder must click or screenshot inside the tool. Never guess a code, a rule number or a disclaimer. Never ask for passwords, API keys or tokens. Do not scrape listings.

CONTEXT
- The site is jaredgibbons.ca: Jared Gibbons PREC, REALTOR®, Royal LePage Little Oak Realty (Surrey, BC). It is being rebuilt as a static Astro site on Cloudflare (no WordPress). About 1,480 pages. Brand: black, white, cream, grey; Montserrat and Lato; square cards.
- Coverage: South Surrey, White Rock, Langley, Surrey, Abbotsford, Chilliwack, Mission, Maple Ridge, Pitt Meadows, Delta, Tsawwassen, Ladner, Coquitlam, Port Coquitlam, Port Moody, Burnaby, New Westminster, Richmond, Vancouver, the North Shore and the eastern valley (Kent, Hope, Agassiz). Boards involved: Fraser Valley Real Estate Board (FVREB), Real Estate Board of Greater Vancouver (REBGV), Chilliwack and District Real Estate Board (CADREB). Confirm which board each of my areas belongs to.
- Jared currently uses a listing tool called "Embeddable Code Generator" with three tabs: Listing Set (Active, Sold, By MLS® Number; listing groups My Listings, Office, Searches; custom sort; show filters), Individual Listing, and Listing Search. [PASTE THE TOOL'S NAME, VENDOR AND LOGIN-PAGE URL HERE. If you can identify the vendor from the screenshots, say so and state how sure you are.]
- Performance and accessibility targets: LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less, WCAG 2.2 AA.
- Goal: put live listings on the right pages without hurting SEO, speed, accessibility or board compliance.

PART A: THE EMBED TOOL (from official docs, help pages and the vendor's site)
1. Vendor, product, documentation URL, pricing and limits, and whether it is a board product, a brokerage product (Royal LePage) or a third party.
2. What each embed outputs: iframe, JavaScript widget, web component or server-rendered HTML. Show the snippet structure with placeholders, not live keys.
3. Every parameter each embed accepts: area, municipality, community or sub-area, property type, status, price min and max, beds, baths, square feet, lot size, year built, keyword, sort, rows per page, map or grid view, open-house filter, listing agent or office. For the area and community parameters, say whether they take names or codes and whether several can be combined.
4. "Searches" listing group: where saved searches live, whether they can be referenced by ID in an embed, and whether I can create 600+ of them.
5. SEO: does the embed put listing text in HTML that crawlers can read, or only in JavaScript or an iframe? Do individual listings get their own indexable URL, on our domain or the vendor's? Is there a sitemap, structured data (RealEstateListing / Product / Offer schema), a canonical tag, or deep-link query strings?
6. Performance: script weight, how many third-party requests, whether the iframe resizes itself (postMessage), lazy loading, effect on CLS and LCP, and the Content-Security-Policy hosts it needs (script-src, frame-src, connect-src, img-src).
7. Styling: can it be themed to our palette and square cards, with custom CSS or CSS variables? Does it meet WCAG 2.2 AA (keyboard use, focus order, contrast, labels)? Does it work on mobile?
8. Leads: does it force sign-in or registration? Where do leads go (which CRM)? Can I hook in my own form or a webhook? Consent and privacy handling (CASL, PIPEDA).
9. Domain authorization: how a site domain is whitelisted, including a Cloudflare preview domain such as *.workers.dev or *.pages.dev, and whether the embed breaks on unlisted domains.
10. Data: refresh frequency, status types included (Active, Pending, Sold, Expired), the sold-data window, and whether sold prices show publicly or only after registration.
11. Is there a JSON or RESO Web API behind it that I could use to render listing HTML on my own pages instead of an embed? List the terms, the cost and who approves it (board, brokerage or vendor).

PART B: BOARD AND BROKERAGE RULES (FVREB, REBGV, CADREB, CREA, Royal LePage)
For each board, from the board's own rules, IDX policy and data licence:
1. Required disclaimer text. Quote it verbatim with the source URL, and say where it must appear (on every page with listings, in each embed, in the footer).
2. Attribution: listing brokerage name, "courtesy of", logos, the MLS® and REALTOR® trademark wording.
3. Display limits: minimum and maximum fields, photo rules, how stale data can be, and what must be hidden (for example, seller-restricted or opted-out listings).
4. Sold data: VOW or sold-display rules, whether registration is required, how far back, and whether sold prices can be shown or only used.
5. Prohibited uses: scraping, AI use, republishing, derived statistics, and whether listing data may be indexed by search engines.
6. Whether I can publish grouped sold statistics (for example, "median sold price in an area this month") from the feed, and what the board's data-use policy says about it. Also the terms for SnapStats and board monthly statistics.
7. Is brokerage approval needed (Royal LePage Little Oak Realty, Royal LePage corporate) before listings go on a personal site? List the form or process and who to contact.
8. Rules for open-house, foreclosure and court-ordered flags, new-construction and presale listings, and 55+ or age-restricted fields.
9. Penalties or compliance audits, if stated.

PART C: PER-PAGE CONFIGURATION
I will attach docs/idx-page-inventory.csv (columns: slug, page_type) and _mapping.json. For every page type in the CSV, give the exact embed or search configuration, using the tool's own field names and the board's own area and property-type values:
- City and area pages (homes, condos): the area codes or names, the property types.
- Price-band pages: Houses under $1.8M, Houses over $1.8M, Condos under $800K, Townhomes under $1.2M, Condos under $500K, Townhomes under $900K, Houses under $1.5M, Langley condos under $399K and $499K. State the price filters and the status.
- 55+ pages: the field that marks age-restricted listings and how to filter on it.
- Lots and land, acreages (a home on 1 to 10 acres), farms (over 10 acres), poultry and equestrian: which property types, lot-size filters and keyword filters work.
- Mobile and manufactured homes: the type and any pad-rental field.
- Foreclosures and court-ordered sales; open houses; new construction and presales; luxury homes; houses with suites or coach houses.
- Community pages, neighbourhood guides and building pages: map each of my area and sub-area slugs to the board's area and sub-area values. List every place where my name differs from the board's name (for example, Poplar and South Poplar, Cottonwood, Walnut Grove).
- Site-wide pages: map search, our listings (My Listings), sold properties, individual listing pages.
Group slugs that share a configuration instead of repeating rows.

PART D: ANYTHING ELSE I SHOULD KNOW
- Listing detail pages: who hosts them, URL structure, whether they can live on jaredgibbons.ca.
- Alerts and saved-search emails, favourites and sign-in: how they work and who owns the leads.
- Open-house schedule feed.
- Listing-photo and video hosting and any license terms.
- Anything in the board or vendor rules that would break the plan to put listings on about 650 area, search and building pages.
- Alternatives if the current tool cannot do it, with the cost and the approval steps.

OUTPUT
1. TOOL-BRIEF.md: Parts A and D, each answer tagged VERIFIED (source and date), INFERRED, or NOT PUBLIC (with what to check inside the tool).
2. COMPLIANCE.md: Part B, one section per board, with verbatim disclaimers and rule citations.
3. idx-config.csv: columns slug, page_type, board, embed_type, area_values, property_types, price_min, price_max, other_filters, sort, rows_per_page, notes. Use "GROUP:<name>" in slug for shared configurations and list the group's members in a second sheet idx-groups.csv.
4. EMBED-TEMPLATE.md: the embed snippet pattern with placeholders, plus the CSP hosts needed.
5. OPEN-QUESTIONS.md: everything I must confirm inside the tool or with a board, as a numbered checklist of exact clicks or screenshots.
Be exact and brief. Do not pad. Do not invent anything.
```

## Before you send it
- Add the tool's name, vendor and login URL where the prompt says to.
- Screenshots of all three tabs, and the dropdown lists (area, community, property type) copied as text.
- One example embed code per tab with any key or token blanked out.
- The names of your IDX / VOW agreements and which boards you belong to.
