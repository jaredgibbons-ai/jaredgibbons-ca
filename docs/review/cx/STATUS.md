# CX brief (audit 2026-11-12): status

| # | Item | Status |
|---|---|---|
| 1 | Google Maps error on guide hubs | **Code done (D-261):** when Google shows its own error box the map is replaced by the area list. **Cause, likely:** the Maps JavaScript API daily cap of 400 map loads set on 2026-11-05 (docs/google-maps-key-setup.md), hit on launch day. Jared to sign in to Google Cloud and check Quotas; raise it (for example 2,000/day) if so. |
| 2 | Locked cards first in results | MyRealPage setting / support request (not in the repo). |
| 3 | "Signup" cells on MLS detail | MyRealPage setting / support request. |
| 4 | "SHOWING: 1-121,249" | **Done (D-261):** MyRealPage hides its "/" separator; idx-embed.css now shows " of ". Checked by injecting the rule on the live results page. |
| 5 | Raw message on Open Houses | **Done (D-261):** it was old widget text captured into six pages' archive text; dropped at render. |
| 6 | Hero search bar | **Done (D-261):** area + home type, straight to that live-listings page; Map search, Call and Email stay. |
| 7 | On-site map on phone | Done earlier (D-255 addendum): full-screen map overlay on the site. |
| 8 | Listings before copy | Done by D-255 (quick search and map button sit right under the H1). The "advanced filters" wording describes the map search, which has them. |
| 9 | Header search finds homes | Not done: needs MLS data the site does not have outside the widget. |
| 10 | Shorter phone homepage | **Partly (D-261):** reviews and listings swipe sideways on phones; page about 15,300px (was about 21,100), Search by Area at about 4,500px (was 11,500). Area link blocks kept for SEO. |
| 11 | Tappable communities | **Done (D-261):** names link to each community's all-homes page; type links are 44px chips. |
| 12 | Quiz instant result | **Done (D-261):** step 5 shows matching search pages first; the contact form is optional below. |
| 13 | Home evaluation form | **Partly (D-261):** form now right after the introduction (about 830px down on a phone), questions after it. Reply time added: "Jared replies the same day" (D-270). Two-step form done (D-271). |
| 14 | Own listing pages | **Partly (D-261):** Book a showing (email or text, filled in), Call, under the price. Video on the 8 active listings that have one, map on every listing (D-269). Floor plans on 42 listings, sold included (D-273); area pages show Jared's listing videos (D-273). 3D tours: none public; slot ready when Jared sends links. |
| 15 | Calculator example rate | **Done (D-269):** example 4.69% 5-yr fixed (RateHub, Nov 12, 2026) prefilled; src/data/example-rate.json, update monthly. |
| 16 | About page rewrite | Needs Jared (first-person copy, photo, video). |
| 17 | Alerts everywhere | **Partly (D-261):** the alert form is open by default everywhere it shows. |
| 18 | Log in / Saved homes | Needs MyRealPage: the account lives inside their frame. |
| 19 | Monthly posts current | October update done (D-257); blog points to the newest automatically. Things to Do for November–December 2026 written for White Rock/South Surrey and Langley (D-276). |
| 20 | Stats chart + report signup | **Done (D-276):** five-year benchmark chart and "Get the monthly market report" sign-up on all 22 market stats pages. |
| 21 | Blog cards | Done (D-258, D-259): photo, date, all posts by year. Category chips not done. |
