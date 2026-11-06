# Forms go-live: what to set, in order

The code is finished and tested: the home page quiz, the contact forms, the home evaluation form and the address-check forms all post to the Worker (`/api/forms/<quiz|contact|home-evaluation|property-check>`). Nothing is live until the values below are set. Never put the Keyvera address or any secret in the repo or in chat.

## 1. Turnstile (the spam check)
Cloudflare dashboard > Turnstile > Add widget.
- Name: jaredgibbons.ca forms
- Hostnames: `jaredgibbons.ca` and `jaredgibbons-ca.jaredgibbons.workers.dev` (the second lets you test on the preview)
- Mode: Managed
- Copy the **Site key** (public) and the **Secret key**.

## 2. Worker secrets
Workers & Pages > jaredgibbons-ca > Settings > Variables and Secrets > Add, type **Secret**:

| Name | Value |
|---|---|
| `TURNSTILE_SECRET` | the Secret key from step 1 |
| `LEAD_EMAIL_TO` | `jaredgibbons@royallepage.ca,<Keyvera website-lead address>` (comma, no space) |
| `LEAD_EMAIL_FROM` | an address on the sending domain, for example `leads@jaredgibbons.ca` |
| `ALLOWED_ORIGINS` | `https://jaredgibbons.ca,https://jaredgibbons-ca.jaredgibbons.workers.dev` (drop the second at launch) |

## 3. Build variables
Workers & Pages > jaredgibbons-ca > Settings > Build > Variables and secrets (build variables, plain text):

| Name | Value |
|---|---|
| `PUBLIC_FORMS_LIVE` | `true` |
| `PUBLIC_TURNSTILE_SITEKEY` | the Site key from step 1 |

Then push any commit (or "Retry build"): the forms switch from the "not connected" stubs to live forms. Without `PUBLIC_FORMS_LIVE=true` every form stays inert, so the preview cannot send anything by accident.

## 4. Sending domain
Outbound email uses Cloudflare Email Service (`EMAIL` binding in `wrangler.jsonc`). The sending domain must be onboarded to it first, which needs that domain's DNS on Cloudflare. If `jaredgibbons.ca` is not on Cloudflare until launch, either onboard another domain you already have there for sending (the From address only needs to be on an onboarded domain, and replies still go to the visitor) or tell me and I will switch delivery to a webhook (`LEAD_WEBHOOK_URL`, already supported) feeding your inbox.

## 5. Test on the preview
Submit the quiz and one contact form. Expect an email at both addresses with the visitor as reply-to. If Send shows "not sent" with the email button, delivery is not set up yet; the answers are in the ready-written email.

## 6. Still open
Newsletter form destination (BL-05). The testimonials form stays inert (it has no message field).
