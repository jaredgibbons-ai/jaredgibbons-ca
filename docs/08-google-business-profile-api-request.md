# Google Business Profile API access request (reviews)

Purpose: show Jared's own Google reviews on jaredgibbons.ca/reviews.html (replaces Trustindex, BL-03).
Status: **Submitted 2026-10-31** (by Jared, via Grok). Awaiting Google. Check Cloud Console > Business Profile API quotas: 0 QPM = pending, 300 QPM = approved. Source of requirements: developers.google.com/my-business/content/prereqs (checked 2026-10-31).

## Before submitting
1. Business Profile is verified and active for 60+ days, and lists https://jaredgibbons.ca as its website.
2. A Google Cloud project exists under the Google account that owns/manages the profile. Copy its **Project Number** (Cloud Console > Dashboard > Project info).
3. Submit the form with an email that is an owner/manager of the profile.

## Form: "Application for Basic API Access" (GBP API contact form)
Field names may differ slightly. Paste:

**Business / API user:** Jared Gibbons (REALTOR®, Personal Real Estate Corporation), Royal LePage Little Oak Realty
**Website:** https://jaredgibbons.ca
**Business Profile name / URL:** [paste the profile name and its Google Maps link]
**Cloud project number:** [paste]
**Contact email:** [owner/manager email]
**Account type:** Direct owner of one Business Profile location (not an agency; no third-party locations).

**Use case:**
> I am the owner of the Google Business Profile for my real estate practice (Jared Gibbons, REALTOR®, Royal LePage Little Oak Realty, serving South Surrey, White Rock and Langley, BC). I am rebuilding my own website, jaredgibbons.ca, and want to display the reviews customers have left on my own Business Profile on my own reviews page. I will use the API read-only to list reviews for my single location (reviewer display name, star rating, review text, date, and my replies) on a scheduled basis, a few requests per day. Reviews will be shown unedited, attributed as Google reviews, with a link to my Google profile and a link inviting visitors to leave a review. I will not modify, filter, sell, or share review data, will not post or reply on my behalf through the API, and will not manage any locations other than my own. Access uses OAuth with the business.manage scope, authorized only by me.

## After approval (Cloud Console > APIs > Business Profile quotas: 0 QPM = pending, 300 QPM = approved)
1. Enable the Business Profile APIs on the project (Google My Business API, My Business Account Management API, My Business Business Information API).
2. Create an OAuth client ID. Jared authorizes once; the refresh token goes into Cloudflare secrets through the secure setup, never in chat or the repo.
3. Scheduled Worker pulls reviews, stores them, and the reviews page renders from the stored copy.
Interim: reviews.html uses the archived reviews as static content. No star-rating structured data for the business's own reviews (Google treats it as self-serving).

## Status 2026-11-03
- OAuth client "Jared Gibbons website reviews" (Web application) exists; Jared authorised `business.manage` once through the OAuth Playground with his own client.
- Worker secrets `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` are set by Jared on the Worker `jg-reviews` (placeholder Hello World Worker; the reviews code deploys over it and the secrets stay). No values are in the repo or docs.
- Jared to-do in Google Cloud: delete the older client secrets (keep only the one now in Cloudflare) and set the consent screen to In production so the refresh token does not expire after 7 days.
- The reviews Worker is not built yet. It is built and switched on only once the API quota shows 300 QPM.
