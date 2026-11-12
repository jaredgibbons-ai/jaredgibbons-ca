// Server-side form handling (not connected until lead destinations are confirmed: BL-05).
// POST /api/forms/<kind>  ->  JSON { ok, id? , errors? }
//
// Nothing here pretends to be live: with no destination bound the endpoint answers 503
// "not_configured" and the page forms stay disabled. Destinations are bindings/vars set through
// `wrangler` or the Cloudflare dashboard (never in the repo):
//   LEADS_DB            D1 database (table `leads`, see migrations/0001_leads.sql)
//   LEAD_WEBHOOK_URL    HTTPS endpoint that receives the lead as JSON (CRM / automation)
//   EMAIL               Cloudflare Email Service `send_email` binding (outbound lead emails)
//   LEAD_EMAIL_TO       secret: comma-separated recipients (Keyvera lead address + Jared's inbox).
//                       The Keyvera address is treated like a password: set it as a Worker secret only.
//   LEAD_EMAIL_FROM     sender on a domain onboarded to Email Sending, e.g. leads@jaredgibbons.ca
//   TURNSTILE_SECRET    Cloudflare Turnstile secret (required: no unprotected public form)
//   ALLOWED_ORIGINS     comma-separated origins allowed to post (default https://jaredgibbons.ca)
//   RATE                optional Workers rate-limiting binding
//   GOOGLE_ADDRESS_VALIDATION_KEY  optional secret: a SERVER key (restricted to Address Validation API) that adds one "Address check" line to the lead.
//                       It never blocks or changes a lead; with no key, or on any error, the line says "not checked". Set as a Worker secret only.

import { ALERT_CONSENT_TEXT } from '../lib/listing-alert.js';
import { NEWSLETTER_CONSENT_TEXT } from '../lib/newsletter.js';

const MAX_BODY = 20 * 1024;
const FORM_TITLES = { contact: 'Contact form', 'home-evaluation': 'Home evaluation request', 'property-check': 'Property check request', quiz: 'Home search quiz', 'listing-alert': 'New listing alert signup', newsletter: 'Newsletter signup', 'presale-vip': 'Presale VIP floorplans request' };
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

// Fields follow the labels captured in the archive (`Your name:`, `Your email:` ...). The archive did
// not capture the 8 hidden/field names of the original POST forms, so only visible labels are modelled.
export const SCHEMAS = {
  contact: {
    name: { label: 'Your name', required: true, max: 100 },
    email: { label: 'Your email', required: true, max: 200, email: true },
    phone: { label: 'Your phone number', max: 30, phone: true },
    subject: { label: 'Subject', max: 150 },
    message: { label: 'Message', required: true, max: 5000 },
  },
  'home-evaluation': {
    name: { label: 'Your name', required: true, max: 100 },
    email: { label: 'Your email', required: true, max: 200, email: true },
    phone: { label: 'Your phone number', max: 30, phone: true },
    address: { label: 'Address', required: true, max: 200 },
    city: { label: 'City', max: 80 },
    postal: { label: 'Postal code', max: 12 },
    bedrooms: { label: 'Bedrooms', max: 10 },
    bathrooms: { label: 'Bathrooms', max: 10 },
    size: { label: 'Size', max: 30 },
    features: { label: 'Features', max: 300 },
    notes: { label: 'Notes', max: 3000 },
  },
  'property-check': {
    address: { label: 'Property address', required: true, max: 200 },
    name: { label: 'Your name (optional)', max: 100 },
  },
  // Home page "Where are you starting?" quiz. Multi-choice answers arrive as one comma-separated line.
  quiz: {
    name: { label: 'Your name', required: true, max: 100 },
    email: { label: 'Your email', required: true, max: 200, email: true },
    phone: { label: 'Your phone number', max: 30, phone: true },
    starting: { label: 'Where they are starting', required: true, max: 80 },
    types: { label: 'Looking for', max: 300 },
    areas: { label: 'Areas', max: 300 },
    budget: { label: 'Budget', max: 80 },
    timeline: { label: 'Timing', max: 80 },
    message: { label: 'Anything else', max: 2000 },
  },
  // "Email me new listings" box above the listing search on every search page. Consent is an unticked box; the wording shown is recorded by the Worker (see handleForm).
  'listing-alert': {
    email: { label: 'Your email', required: true, max: 200, email: true },
    name: { label: 'Your first name', max: 100 },
    search: { label: 'Search', max: 200 },
    search_id: { label: 'Search ID', max: 20, digits: true },
    consent: { label: 'Consent', required: true, max: 5, must: 'yes', mustMsg: 'Please tick the box so Jared can email you.' },
  },
  // "Request VIP floorplans & pricing" on the presale and new-construction pages. Name, email and phone are all needed so Jared can send the package and call.
  'presale-vip': {
    name: { label: 'Your name', required: true, max: 100 },
    email: { label: 'Your email', required: true, max: 200, email: true },
    phone: { label: 'Your phone number', required: true, max: 30, phone: true },
    project: { label: 'Project', max: 150 },
  },
  // Monthly newsletter sign-up page. Same consent rules as the listing alert.
  newsletter: {
    email: { label: 'Your email', required: true, max: 200, email: true },
    name: { label: 'Your name', max: 100 },
    consent: { label: 'Consent', required: true, max: 5, must: 'yes', mustMsg: 'Please tick the box so Jared can email you.' },
  },
};
const QUIZ_ORDER = ['starting', 'types', 'areas', 'budget', 'timeline'];

export function validate(kind, input) {
  const schema = SCHEMAS[kind];
  const clean = {}, errors = {};
  for (const [k, f] of Object.entries(schema)) {
    let v = input[k];
    v = typeof v === 'string' ? v.replace(/\r\n/g, '\n').trim() : '';
    if (!v) { if (f.required) errors[k] = f.mustMsg || `${f.label} is required.`; continue; }
    if (v.length > f.max) { errors[k] = `${f.label} is too long (maximum ${f.max} characters).`; continue; }
    if (f.email && !EMAIL.test(v)) { errors[k] = `${f.label} must be a valid email address.`; continue; }
    if (f.digits && !/^[0-9]+$/.test(v)) { errors[k] = `${f.label} is not valid.`; continue; }
    if (f.must && v !== f.must) { errors[k] = f.mustMsg || `${f.label} is required.`; continue; }
    if (f.phone && !/^[0-9+().\-\s]{7,30}$/.test(v)) { errors[k] = `${f.label} must be a valid phone number.`; continue; }
    if (/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/.test(v)) { errors[k] = `${f.label} contains invalid characters.`; continue; }
    clean[k] = v;
  }
  return { clean, errors };
}

/** 'complete' | 'check' | 'unchecked'. Asks Google's Address Validation API whether the typed address is a complete, confirmed Canadian address. Never throws, never blocks a lead. */
export async function checkAddress(address, env, doFetch = fetch) {
  const key = env && env.GOOGLE_ADDRESS_VALIDATION_KEY;
  if (!key || !address) return 'unchecked';
  const ctl = new AbortController(); const timer = setTimeout(() => ctl.abort(), 2500);
  try {
    const r = await doFetch(`https://addressvalidation.googleapis.com/v1:validateAddress?key=${encodeURIComponent(key)}`, {
      method: 'POST', headers: { 'content-type': 'application/json' }, signal: ctl.signal,
      body: JSON.stringify({ address: { regionCode: 'CA', addressLines: [address] } }),
    });
    if (!r.ok) return 'unchecked';
    const v = (await r.json())?.result?.verdict;
    if (!v || typeof v !== 'object') return 'unchecked';
    return v.addressComplete === true && !v.hasUnconfirmedComponents ? 'complete' : 'check';
  } catch { return 'unchecked'; } finally { clearTimeout(timer); }
}
const CHECK_TEXT = { complete: 'confirmed as a complete address', check: 'could not be fully confirmed, please check it', unchecked: 'not checked' };

const oneLine = (v) => String(v || '').replace(/[\r\n\u2028\u2029]+/g, ' ').trim();

// Plain text laid out as "Label: value" lines so Keyvera can read the name, email, phone, message and the
// home asked about. Multi-line messages go last, after the single-line fields.
export function leadEmail(lead) {
  const f = lead.fields;
  const lines = [FORM_TITLES[lead.kind] || lead.kind, ''];
  if (f.name) lines.push(`Name: ${oneLine(f.name)}`);
  if (f.email) lines.push(`Email: ${oneLine(f.email)}`);
  if (f.phone) lines.push(`Phone: ${oneLine(f.phone)}`);
  if (f.address) lines.push(`Address: ${oneLine(f.address)}`);
  if (f.address && lead.address_check) lines.push(`Address check: ${CHECK_TEXT[lead.address_check] || 'not checked'}`);
  if (f.subject) lines.push(`Subject: ${oneLine(f.subject)}`);
  if (lead.kind === 'presale-vip') { lines.push(`Project: ${oneLine(f.project) || 'not named (general presale request)'}`); lines.push('Wants: VIP floorplans and pricing'); }
  if (lead.kind === 'home-evaluation') for (const k of ['city', 'postal', 'bedrooms', 'bathrooms', 'size', 'features']) if (f[k]) lines.push(`${SCHEMAS['home-evaluation'][k].label}: ${oneLine(f[k])}`);
  if (lead.kind === 'quiz') for (const k of QUIZ_ORDER) if (f[k]) lines.push(`${SCHEMAS.quiz[k].label}: ${oneLine(f[k])}`);
  if (lead.kind === 'listing-alert') {
    if (f.search) lines.push(`Search: ${oneLine(f.search)}`);
    if (f.search_id) lines.push(`Search ID (MyRealPage): ${oneLine(f.search_id)}`);
    if (lead.page) lines.push(`Search page: ${oneLine(lead.page).startsWith("/") ? "https://jaredgibbons.ca" : ""}${oneLine(lead.page)}`);
    lines.push('Wants: email alerts of new listings that match this search');
    lines.push(`Consent: express, given by ticking an unticked box on the search page at ${lead.received_at}`);
    lines.push(`Wording shown: "${oneLine(f.consent_text)}"`);
  } else if (lead.kind === 'newsletter') {
    if (lead.page) lines.push(`Page: ${oneLine(lead.page).startsWith('/') ? 'https://jaredgibbons.ca' : ''}${oneLine(lead.page)}`);
    lines.push('Wants: the monthly newsletter by email');
    lines.push(`Consent: express, given by ticking an unticked box on the newsletter page at ${lead.received_at}`);
    lines.push(`Wording shown: "${oneLine(f.consent_text)}"`);
  } else if (lead.page) lines.push(`Page: ${oneLine(lead.page)}`);
  lines.push(`Received: ${lead.received_at}`);
  if (f.message) lines.push('', 'Message:', f.message);
  if (f.notes) lines.push('', 'Notes:', f.notes);
  const who = oneLine(f.name) || oneLine(f.email) || 'website visitor';
  return {
    subject: `${FORM_TITLES[lead.kind] || 'Website lead'} from ${who}`.slice(0, 200),
    text: lines.join('\n'),
    replyTo: f.email ? { email: oneLine(f.email), ...(f.name ? { name: oneLine(f.name).replace(/["<>]/g, '') } : {}) } : undefined,
  };
}

// Extra flat fields on the webhook payload so an automation (Zapier) can email the lead without holding any address itself:
// the recipients come from the LEAD_EMAIL_TO secret, the wording from leadEmail().
export function notifyFields(lead, emailTo) {
  const m = leadEmail(lead);
  return { notify_to: emailTo.join(','), notify_subject: m.subject, notify_text: m.text, notify_reply_to: m.replyTo ? m.replyTo.email : '' };
}

const json = (status, body, extra = {}) =>
  new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...extra } });

async function readBody(request) {
  const len = Number(request.headers.get('content-length') || 0);
  if (len > MAX_BODY) return { tooLarge: true };
  const text = await request.text();
  if (text.length > MAX_BODY) return { tooLarge: true };
  const ct = (request.headers.get('content-type') || '').toLowerCase();
  try {
    if (ct.includes('application/json')) return { data: JSON.parse(text) };
    if (ct.includes('application/x-www-form-urlencoded')) return { data: Object.fromEntries(new URLSearchParams(text)) };
  } catch { return { bad: true }; }
  return { bad: true };
}

export async function handleForm(request, env, deps = {}) {
  const doFetch = deps.fetch || fetch;
  const url = new URL(request.url);
  const kind = url.pathname.replace(/^\/api\/forms\//, '');
  if (!Object.hasOwn(SCHEMAS, kind)) return json(404, { ok: false, error: 'unknown_form' });
  if (request.method !== 'POST') return json(405, { ok: false, error: 'method_not_allowed' }, { allow: 'POST' });

  const allowed = (env.ALLOWED_ORIGINS || 'https://jaredgibbons.ca').split(',').map((s) => s.trim());
  const origin = request.headers.get('origin');
  if (!origin || !allowed.includes(origin)) return json(403, { ok: false, error: 'origin_not_allowed' });

  // Never accept leads we cannot deliver or protect.
  const emailTo = String(env.LEAD_EMAIL_TO || '').split(',').map((a) => a.trim()).filter(Boolean);
  const emailReady = !!(env.EMAIL && env.LEAD_EMAIL_FROM && emailTo.length);
  if (!env.TURNSTILE_SECRET || !(env.LEADS_DB || env.LEAD_WEBHOOK_URL || emailReady)) return json(503, { ok: false, error: 'not_configured' });

  const ip = request.headers.get('cf-connecting-ip') || '';
  if (env.RATE) {
    const { success } = await env.RATE.limit({ key: ip || 'unknown' });
    if (!success) return json(429, { ok: false, error: 'rate_limited' }, { 'retry-after': '60' });
  }

  const body = await readBody(request);
  if (body.tooLarge) return json(413, { ok: false, error: 'too_large' });
  if (body.bad || typeof body.data !== 'object' || body.data === null) return json(400, { ok: false, error: 'bad_request' });
  const input = body.data;

  // honeypot (named _hp_url because browsers and password managers autofill fields called "website"): real people never fill it; answer as if accepted so bots learn nothing
  if (typeof input._hp_url === 'string' && input._hp_url.trim() !== '') return json(200, { ok: true });

  const token = input['cf-turnstile-response'];
  if (typeof token !== 'string' || !token) {
    // No check yet: name the missing or wrong fields first (D-246), so an empty form is not answered with only "complete the check". Nothing is stored or sent here.
    const early = validate(kind, input).errors;
    if (Object.keys(early).length) return json(422, { ok: false, errors: early });
    return json(403, { ok: false, error: 'captcha_required' });
  }
  const ver = await doFetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ secret: env.TURNSTILE_SECRET, response: token, ...(ip ? { remoteip: ip } : {}) }),
  }).then((r) => r.json()).catch(() => ({ success: false }));
  if (!ver.success) return json(403, { ok: false, error: 'captcha_failed' });

  const { clean, errors } = validate(kind, input);
  if (Object.keys(errors).length) return json(422, { ok: false, errors });
  // The consent wording is the server's own copy of what the page showed, never taken from the visitor.
  if (kind === 'listing-alert') { clean.consent = 'yes'; clean.consent_text = ALERT_CONSENT_TEXT; }
  if (kind === 'newsletter') { clean.consent = 'yes'; clean.consent_text = NEWSLETTER_CONSENT_TEXT; }

  const id = crypto.randomUUID();
  const lead = { id, kind, received_at: new Date().toISOString(), page: String(input.page || '').slice(0, 300), fields: clean };
  if (clean.address) lead.address_check = await checkAddress(clean.address, env, doFetch);
  const results = [], mail = [];
  if (env.LEADS_DB) {
    results.push(env.LEADS_DB.prepare('INSERT INTO leads (id, kind, received_at, page, fields) VALUES (?, ?, ?, ?, ?)')
      .bind(id, kind, lead.received_at, lead.page, JSON.stringify(lead.address_check ? { ...clean, address_check: lead.address_check } : clean)).run().then(() => true, () => false));
  }
  if (env.LEAD_WEBHOOK_URL) {
    results.push(doFetch(env.LEAD_WEBHOOK_URL, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ ...lead, ...notifyFields(lead, emailTo) }) })
      .then((r) => r.ok, () => false));
  }
  if (emailReady) {
    // One message per recipient so a failure for one inbox is never hidden by success for another.
    const msg = leadEmail(lead);
    for (const to of emailTo) {
      mail.push(Promise.resolve().then(() => env.EMAIL.send({ to, from: { email: env.LEAD_EMAIL_FROM, name: 'Jared Gibbons website' }, ...msg })).then(() => true, () => false));
    }
  }
  const ok = await Promise.all(results);
  const mailOk = await Promise.all(mail);
  // A lead counts as received only when every configured destination accepted it. Direct email is the exception when a database or webhook also took
  // the lead: then it is best-effort, so a sending domain that is not set up yet cannot turn a delivered lead into an error for the visitor.
  if (ok.some((x) => !x) || (!results.length && mailOk.some((x) => !x))) return json(502, { ok: false, error: 'delivery_failed' });
  return json(200, { ok: true, id });
}
