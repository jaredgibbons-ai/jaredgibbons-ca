# Google Maps key for the neighbourhood maps (D-102)

The key is a **browser key**: it is visible in the page source by design, so it is not a secret. What protects it is the website restriction and the spending cap below. Never put a card number or a Google password anywhere except Google's own pages.

1. Go to console.cloud.google.com and sign in with the Google account that should own the billing. Create a project (for example "jaredgibbons-ca").
2. Billing: link a billing account to the project. Google gives 10,000 free map loads a month for the Maps JavaScript API and charges US$7 per 1,000 after that (Google's pricing page, checked 2026-11-04).
3. APIs & Services > Library: enable **Maps JavaScript API** (nothing else is needed).
4. APIs & Services > Credentials > Create credentials > API key. Then edit the key:
   - Application restrictions: **Websites**. Add `https://jaredgibbons.ca/*`, `https://www.jaredgibbons.ca/*` and the preview address (for example `https://jaredgibbons-ca.<your-subdomain>.workers.dev/*`).
   - API restrictions: **Restrict key** > Maps JavaScript API only.
5. Spending guard: Billing > Budgets & alerts > create a budget (for example US$25 a month) with email alerts. Optional hard stop: APIs & Services > Maps JavaScript API > Quotas, lower "Map loads per day".
6. Give the key to the build as `PUBLIC_GOOGLE_MAPS_KEY`:
   - Building on your Mac: `PUBLIC_GOOGLE_MAPS_KEY=<the key> npm run build` (or put it in a file named `.env`, which git ignores).
   - Building on Cloudflare: Workers & Pages > the project > Settings > Variables and Secrets, add `PUBLIC_GOOGLE_MAPS_KEY` as a build variable.
7. Add one line to the privacy page saying the map loads from Google (I will write it).

Without the key the maps show a "not connected" note and the list of area links under each map still works.
