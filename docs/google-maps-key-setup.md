# Google Maps key for the neighbourhood maps (D-102, D-103)

Done 2026-11-04 in the Google Cloud console (project **jaredgibbons-ca-maps**, linked to the existing billing account):

- APIs on: **Maps JavaScript API**, **Places API (New)**, **Routes API**. (Address Validation is a server call and needs its own server key, see below.)
- Key **"jaredgibbons.ca browser key"**: restricted to those three APIs and to the websites `https://jaredgibbons.ca/*` and `https://www.jaredgibbons.ca/*`.
- Budget **"jaredgibbons.ca maps"**: US$25 a month for this project only, email alerts at 50%, 90% and 100% to billing admins.
- The older project "Website map" has an unrestricted key from 2024 that is not ours; leave it alone, but consider restricting it if it is not in use.

The key is a **browser key**: it is visible in the page source by design, so it is not a secret. The website restriction and the spending alert are what protect it. Never put a card number or a Google password anywhere except Google's own pages.

## Still to do (Jared, at the private preview deploy)
1. ~~Add the preview address to the key's website list~~ Done 2026-11-05 by Claude in Jared's console: `https://jaredgibbons-ca.jaredgibbons.workers.dev/*` is now on the key (it can take up to 5 minutes to take effect).
2. Give the key to the build as `PUBLIC_GOOGLE_MAPS_KEY`: a build variable in Cloudflare (Workers & Pages > project > Settings > Build > Variables and secrets), or a `.env` file next to `package.json` when building on the Mac (git ignores it). The private preview now exists (see docs/02), so this is the next step: Jared sets it in the Worker's build settings and retries the latest build. Claude does not type API keys into fields.
3. Hard stop (done 2026-11-05 by Claude in Jared's Google Cloud console): Maps JavaScript API > Quotas, "Map loads per day" lowered from unlimited to **400** (about 12,000 a month, which keeps a bad month near the US$25 budget). Raise it if real traffic needs more. "3D Map loads per day" (flyover) is still unlimited.
4. Optional hard stop for the nearby-places buttons: APIs & Services > Places API (New) > Quotas, lower the Nearby Search requests per day. Each button press is one request (name and position only), so cost follows clicks, not page views.

## Address checking on forms (optional, later)
The forms add a suggestion list to address fields with the browser key above. A second, **server** key can also tick "Address check" onto each lead: create a key restricted to the **Address Validation API** only (enable that API first), and add it to the Worker as the secret `GOOGLE_ADDRESS_VALIDATION_KEY`. Without it the lead says "Address check: not checked". Never paste that key in chat.

Without the browser key the maps show a "not connected" note and the list of area links under each map still works.
