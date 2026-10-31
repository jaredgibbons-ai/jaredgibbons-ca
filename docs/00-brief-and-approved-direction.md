# Brief and approved direction

Rebuild jaredgibbons.ca (Jared Gibbons, REALTOR®/PREC, Royal LePage Little Oak Realty) on Cloudflare from the preservation archive captured 2026-10-31 (Drive folder `1Sqv4exg0SzwOFPOMT7PKPEyYrw2cFLFz`, master guide `1jyQAkKCK0RYN1FaQyGJyVihkZ43iJ4oouORh4Q1ACF0`).

## Rules that govern every page
- **Preservation:** archived wording, punctuation, titles, headings, link text and URLs (including `.html` and `/<page>.html/listing.r<MLS#>-<address>.<id>`) are kept exactly. Errors are recorded in `04-decisions-and-exceptions.md`, not silently fixed. Nothing is invented. Uncaptured items stay open items.
- **Brand:** `#0a0a0a` text and buttons, `#ffffff` background, cream `#f0ece4` panels, grey `#606060` secondary text (only where contrast passes), archived gold for stars. Montserrat headings/labels/buttons, Lato body (self-hosted). Square-edged cards, black underlined links, black buttons. No gradients, no distracting motion, reduced motion respected. Full hover/focus/loading/empty/error/success states.
- **Cards:** sold-property cards match buy-page cards; only status-specific content differs.
- **Forms:** server-side validation, spam protection, accessible feedback, verified destinations, end-to-end delivery tests. A success screen is not proof. Unconnected features are never shown as working.
- **Targets:** WCAG 2.2 AA; LCP ≤2.5 s, INP ≤200 ms, CLS ≤0.1 (lab and field reported separately). Pages reported as implemented, validated, blocked or failed.
- **Safety:** no launch and no production DNS change without explicit approval. No secrets in chat.
- **Sequence:** direction → approval → private preview of homepage + one community page → review → scale.

## Approved (see `04-decisions-and-exceptions.md` A-01…A-05)
Cloudflare as proposed (§3–5 of `01-direction-for-approval.md`, incl. interface wording); free private GitHub repo as source of truth; expired-listing rule.

## Interface wording (approved)
"Skip to content"; "Menu"/"Close menu"; "Sending…"; "Thank you. Your message has been received."; "Something went wrong. Please try again or call 604-928-1361."; "Enter a valid email address."; "This field is required."; "Listings are not connected in this preview."; "No listings match right now."; "On this page".
