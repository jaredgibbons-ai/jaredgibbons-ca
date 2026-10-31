// Server-side form handling (not connected until lead destinations are confirmed: BL-05).
// POST /api/forms/<kind>  ->  JSON { ok, id? , errors? }
//
// Nothing here pretends to be live: with no destination bound the endpoint answers 503
// "not_configured" and the page forms stay disabled. Destinations are bindings/vars set through
// `wrangler` or the Cloudflare dashboard (never in the repo):
//   LEADS_DB            D1 database (table `leads`, see migrations/0001_leads.sql)
//   LEAD_WEBHOOK_URL    HTTPS endpoint that receives the lead as JSON (CRM / automation)
//   TURNSTILE_SECRET    Cloudflare Turnstile secret (required: no unprotected public form)
//   ALLOWED_ORIGINS     comma-separated origins allowed to post (default https://jaredgibbons.ca)
//   RATE                optional Workers rate-limiting binding

const MAX_BODY = 20 * 1024;
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
  },
  'property-check': {
    address: { label: 'Property address', required: true, max: 200 },
    name: { label: 'Your name (optional)', max: 100 },
  },
};

export function validate(kind, input) {
  const schema = SCHEMAS[kind];
  const clean = {}, errors = {};
  for (const [k, f] of Object.entries(schema)) {
    let v = input[k];
    v = typeof v === 'string' ? v.replace(/\r\n/g, '\n').trim() : '';
    if (!v) { if (f.required) errors[k] = `${f.label} is required.`; continue; }
    if (v.length > f.max) { errors[k] = `${f.label} is too long (maximum ${f.max} characters).`; continue; }
    if (f.email && !EMAIL.test(v)) { errors[k] = `${f.label} must be a valid email address.`; continue; }
    if (f.phone && !/^[0-9+().\-\s]{7,30}$/.test(v)) { errors[k] = `${f.label} must be a valid phone number.`; continue; }
    if (/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/.test(v)) { errors[k] = `${f.label} contains invalid characters.`; continue; }
    clean[k] = v;
  }
  return { clean, errors };
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
  if (!env.TURNSTILE_SECRET || !(env.LEADS_DB || env.LEAD_WEBHOOK_URL)) return json(503, { ok: false, error: 'not_configured' });

  const ip = request.headers.get('cf-connecting-ip') || '';
  if (env.RATE) {
    const { success } = await env.RATE.limit({ key: ip || 'unknown' });
    if (!success) return json(429, { ok: false, error: 'rate_limited' }, { 'retry-after': '60' });
  }

  const body = await readBody(request);
  if (body.tooLarge) return json(413, { ok: false, error: 'too_large' });
  if (body.bad || typeof body.data !== 'object' || body.data === null) return json(400, { ok: false, error: 'bad_request' });
  const input = body.data;

  // honeypot: real people never fill it; answer as if accepted so bots learn nothing
  if (typeof input.website === 'string' && input.website.trim() !== '') return json(200, { ok: true });

  const token = input['cf-turnstile-response'];
  if (typeof token !== 'string' || !token) return json(403, { ok: false, error: 'captcha_required' });
  const ver = await doFetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ secret: env.TURNSTILE_SECRET, response: token, ...(ip ? { remoteip: ip } : {}) }),
  }).then((r) => r.json()).catch(() => ({ success: false }));
  if (!ver.success) return json(403, { ok: false, error: 'captcha_failed' });

  const { clean, errors } = validate(kind, input);
  if (Object.keys(errors).length) return json(422, { ok: false, errors });

  const id = crypto.randomUUID();
  const lead = { id, kind, received_at: new Date().toISOString(), page: String(input.page || '').slice(0, 300), fields: clean };
  const results = [];
  if (env.LEADS_DB) {
    results.push(env.LEADS_DB.prepare('INSERT INTO leads (id, kind, received_at, page, fields) VALUES (?, ?, ?, ?, ?)')
      .bind(id, kind, lead.received_at, lead.page, JSON.stringify(clean)).run().then(() => true, () => false));
  }
  if (env.LEAD_WEBHOOK_URL) {
    results.push(doFetch(env.LEAD_WEBHOOK_URL, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(lead) })
      .then((r) => r.ok, () => false));
  }
  const ok = await Promise.all(results);
  // A lead counts as received only when every configured destination accepted it.
  if (ok.some((x) => !x)) return json(502, { ok: false, error: 'delivery_failed' });
  return json(200, { ok: true, id });
}
