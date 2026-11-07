import test from 'node:test';
import assert from 'node:assert/strict';
import { handleForm, validate, leadEmail, checkAddress } from '../src/worker/forms.js';

const ORIGIN = 'https://jaredgibbons.ca';
const good = { name: 'Pat Example', email: 'pat@example.com', phone: '604-555-0100', subject: 'Hello', message: 'I would like to talk.', 'cf-turnstile-response': 'tok' };
const mk = (body, { path = '/api/forms/contact', origin = ORIGIN, method = 'POST', type = 'application/json' } = {}) =>
  new Request('https://jaredgibbons.ca' + path, { method, headers: { 'content-type': type, ...(origin ? { origin } : {}), 'cf-connecting-ip': '203.0.113.9' }, body: method === 'POST' ? (type.includes('json') ? JSON.stringify(body) : new URLSearchParams(body).toString()) : undefined });
const fakeDb = () => { const rows = []; return { rows, prepare: () => ({ bind: (...a) => ({ run: async () => { rows.push(a); } }) }) }; };
const captcha = (ok = true) => async (u, init) => (String(u).includes('turnstile') ? new Response(JSON.stringify({ success: ok })) : new Response('ok', { status: 200 }));
const env = (extra = {}) => ({ TURNSTILE_SECRET: 's', LEADS_DB: fakeDb(), ...extra });

test('valid contact lead is stored and acknowledged', async () => {
  const e = env(); const r = await handleForm(mk(good), e, { fetch: captcha() });
  assert.equal(r.status, 200); const j = await r.json(); assert.equal(j.ok, true); assert.ok(j.id);
  assert.equal(e.LEADS_DB.rows.length, 1); assert.equal(JSON.parse(e.LEADS_DB.rows[0][4]).email, 'pat@example.com');
});
test('form-encoded posts work too', async () => {
  const e = env(); const r = await handleForm(mk(good, { type: 'application/x-www-form-urlencoded' }), e, { fetch: captcha() });
  assert.equal(r.status, 200);
});
test('server-side validation returns field errors and stores nothing', async () => {
  const e = env(); const r = await handleForm(mk({ ...good, email: 'nope', name: '' }), e, { fetch: captcha() });
  assert.equal(r.status, 422); const j = await r.json();
  assert.match(j.errors.email, /valid email/); assert.match(j.errors.name, /required/); assert.equal(e.LEADS_DB.rows.length, 0);
});
test('not configured: no destination or no captcha secret answers 503, never a fake success', async () => {
  assert.equal((await handleForm(mk(good), { TURNSTILE_SECRET: 's' }, { fetch: captcha() })).status, 503);
  assert.equal((await handleForm(mk(good), { LEADS_DB: fakeDb() }, { fetch: captcha() })).status, 503);
});
test('captcha is mandatory and verified server-side', async () => {
  const { 'cf-turnstile-response': _t, ...nocap } = good;
  assert.equal((await handleForm(mk(nocap), env(), { fetch: captcha() })).status, 403);
  assert.equal((await handleForm(mk(good), env(), { fetch: captcha(false) })).status, 403);
});
test('honeypot looks accepted but stores nothing', async () => {
  const e = env(); const r = await handleForm(mk({ ...good, _hp_url: 'http://spam' }), e, { fetch: captcha() });
  assert.equal(r.status, 200); assert.equal(e.LEADS_DB.rows.length, 0);
});
test('origin, method, unknown form, size and rate limits', async () => {
  assert.equal((await handleForm(mk(good, { origin: 'https://evil.example' }), env(), { fetch: captcha() })).status, 403);
  assert.equal((await handleForm(mk(good, { origin: null }), env(), { fetch: captcha() })).status, 403);
  assert.equal((await handleForm(mk(null, { method: 'GET' }), env(), { fetch: captcha() })).status, 405);
  assert.equal((await handleForm(mk(good, { path: '/api/forms/nope' }), env(), { fetch: captcha() })).status, 404);
  assert.equal((await handleForm(mk({ ...good, message: 'x'.repeat(30000) }), env(), { fetch: captcha() })).status, 413);
  assert.equal((await handleForm(mk(good), env({ RATE: { limit: async () => ({ success: false }) } }), { fetch: captcha() })).status, 429);
});
test('delivery: webhook receives the lead; any failing destination is a 502 (not a false success)', async () => {
  const seen = [];
  const f = async (u, init) => { if (String(u).includes('turnstile')) return new Response(JSON.stringify({ success: true })); seen.push(JSON.parse(init.body)); return new Response('ok'); };
  const r = await handleForm(mk(good), { TURNSTILE_SECRET: 's', LEAD_WEBHOOK_URL: 'https://hooks.example/lead', LEAD_EMAIL_TO: 'a@example.com, b@example.com' }, { fetch: f });
  assert.equal(r.status, 200); assert.equal(seen[0].kind, 'contact'); assert.equal(seen[0].fields.name, 'Pat Example');
  assert.equal(seen[0].notify_to, 'a@example.com,b@example.com'); assert.match(seen[0].notify_subject, /Pat Example/); assert.match(seen[0].notify_text, /Name: Pat Example/); assert.ok('notify_reply_to' in seen[0]);
  const bad = async (u) => (String(u).includes('turnstile') ? new Response(JSON.stringify({ success: true })) : new Response('x', { status: 500 }));
  assert.equal((await handleForm(mk(good), { TURNSTILE_SECRET: 's', LEAD_WEBHOOK_URL: 'https://hooks.example/lead' }, { fetch: bad })).status, 502);
});
test('schemas: property check needs only an address; home evaluation needs contact details', () => {
  assert.deepEqual(validate('property-check', { address: '1 Main St' }).errors, {});
  assert.ok(validate('home-evaluation', { address: '1 Main St' }).errors.email);
});

const fakeMail = (failFor) => { const sent = []; return { sent, send: async (m) => { if (failFor && m.to === failFor) throw new Error('rejected'); sent.push(m); return { messageId: 'x' }; } }; };
const mailEnv = (mail, extra = {}) => ({ TURNSTILE_SECRET: 's', EMAIL: mail, LEAD_EMAIL_FROM: 'leads@example.test', LEAD_EMAIL_TO: 'crm-inbox@example.test, owner@example.test', ...extra });
test('email delivery: one message per recipient, reply-to is the lead, body is Label: value text', async () => {
  const mail = fakeMail(); const r = await handleForm(mk(good), mailEnv(mail), { fetch: captcha() });
  assert.equal(r.status, 200); assert.deepEqual(mail.sent.map((m) => m.to), ['crm-inbox@example.test', 'owner@example.test']);
  const m = mail.sent[0]; assert.equal(m.replyTo.email, 'pat@example.com'); assert.equal(m.from.email, 'leads@example.test');
  assert.match(m.text, /^Name: Pat Example$/m); assert.match(m.text, /^Email: pat@example\.com$/m); assert.match(m.text, /^Phone: 604-555-0100$/m); assert.match(m.text, /Message:\nI would like to talk\./);
});
test('email delivery: a rejected recipient makes the whole lead a 502', async () => {
  const mail = fakeMail('owner@example.test');
  assert.equal((await handleForm(mk(good), mailEnv(mail), { fetch: captcha() })).status, 502);
});
test('email delivery: incomplete email config alone is not a destination (503)', async () => {
  assert.equal((await handleForm(mk(good), mailEnv(fakeMail(), { LEAD_EMAIL_TO: '' }), { fetch: captcha() })).status, 503);
  assert.equal((await handleForm(mk(good), mailEnv(fakeMail(), { LEAD_EMAIL_FROM: '' }), { fetch: captcha() })).status, 503);
});
test('email content: header injection is neutralised; address-only leads have no reply-to', () => {
  const m = leadEmail({ kind: 'contact', received_at: 't', page: '/contact.html', fields: { name: 'Eve\r\nBcc: x@y.z', email: 'e@example.com', message: 'hi' } });
  assert.ok(!/[\r\n]/.test(m.subject)); assert.ok(!/[\r\n]/.test(m.replyTo.name));
  const p = leadEmail({ kind: 'property-check', received_at: 't', page: '', fields: { address: '1 Main St' } });
  assert.equal(p.replyTo, undefined); assert.match(p.text, /^Address: 1 Main St$/m);
});

const addrGood = { name: 'Pat Example', email: 'pat@example.com', address: '1 Main St, Surrey, BC', 'cf-turnstile-response': 'tok' };
const gfetch = (verdict, status = 200) => async (u, init) => {
  if (String(u).includes('turnstile')) return new Response(JSON.stringify({ success: true }));
  if (String(u).includes('addressvalidation.googleapis.com')) return new Response(JSON.stringify({ result: { verdict } }), { status });
  return new Response('ok');
};
test('address check: complete, needs-review and unchecked all reach the lead and never block it', async () => {
  const e = { GOOGLE_ADDRESS_VALIDATION_KEY: 'k' };
  assert.equal(await checkAddress('1 Main St', e, gfetch({ addressComplete: true })), 'complete');
  assert.equal(await checkAddress('1 Main St', e, gfetch({ addressComplete: true, hasUnconfirmedComponents: true })), 'check');
  assert.equal(await checkAddress('1 Main St', e, gfetch({})), 'check');
  assert.equal(await checkAddress('1 Main St', e, gfetch({}, 500)), 'unchecked');
  assert.equal(await checkAddress('1 Main St', {}, gfetch({ addressComplete: true })), 'unchecked');
  assert.equal(await checkAddress('1 Main St', e, async () => { throw new Error('down'); }), 'unchecked');
  const db = fakeDb();
  const r = await handleForm(mk(addrGood, { path: '/api/forms/home-evaluation' }), { TURNSTILE_SECRET: 's', LEADS_DB: db, GOOGLE_ADDRESS_VALIDATION_KEY: 'k' }, { fetch: gfetch({ addressComplete: false }) });
  assert.equal(r.status, 200);
  assert.equal(JSON.parse(db.rows[0][4]).address_check, 'check');
  const r2 = await handleForm(mk(addrGood, { path: '/api/forms/home-evaluation' }), { TURNSTILE_SECRET: 's', LEADS_DB: fakeDb() }, { fetch: gfetch({ addressComplete: true }) });
  assert.equal(r2.status, 200);
  const m = leadEmail({ kind: 'home-evaluation', received_at: 'x', fields: { name: 'P', address: '1 Main St' }, address_check: 'check' });
  assert.match(m.text, /Address check: could not be fully confirmed/);
  assert.ok(!/Address check/.test(leadEmail({ kind: 'contact', received_at: 'x', fields: { name: 'P' } }).text));
});

test('quiz lead is validated and the email lists every answer', async () => {
  const quiz = { name: 'Pat Example', email: 'pat@example.com', phone: '604-555-0100', starting: 'First home', types: 'Condo, Townhome', areas: 'South Surrey / White Rock, Langley', budget: '$500,000 to $750,000', timeline: 'In 1 to 3 months', message: 'Near transit please.', page: '/index.html', 'cf-turnstile-response': 'tok' };
  const sent = [];
  const e = env({ EMAIL: { send: async (m) => { sent.push(m); } }, LEAD_EMAIL_FROM: 'leads@jaredgibbons.ca', LEAD_EMAIL_TO: 'jaredgibbons@royallepage.ca' });
  const r = await handleForm(mk(quiz, { path: '/api/forms/quiz' }), e, { fetch: captcha() });
  assert.equal(r.status, 200); assert.equal(sent.length, 1);
  assert.match(sent[0].subject, /Home search quiz from Pat Example/);
  for (const v of ['First home', 'Condo, Townhome', 'South Surrey / White Rock, Langley', '$500,000 to $750,000', 'In 1 to 3 months', 'Near transit please.', 'pat@example.com', '604-555-0100']) assert.ok(sent[0].text.includes(v), v);
  const bad = await handleForm(mk({ ...quiz, starting: '', email: 'x' }, { path: '/api/forms/quiz' }), env(), { fetch: captcha() });
  assert.equal(bad.status, 422);
});

test('home evaluation keeps the extra fields in the email', async () => {
  const sent = [];
  const e = env({ EMAIL: { send: async (m) => { sent.push(m); } }, LEAD_EMAIL_FROM: 'leads@jaredgibbons.ca', LEAD_EMAIL_TO: 'a@example.com,b@example.com' });
  const body = { name: 'Pat', email: 'pat@example.com', phone: '604-555-0100', address: '1 Main St', city: 'Surrey', postal: 'V3T 1A1', bedrooms: '3', bathrooms: '2', size: '1800 sq. ft.', features: 'New roof', notes: 'Call after 5.', 'cf-turnstile-response': 'tok' };
  const r = await handleForm(mk(body, { path: '/api/forms/home-evaluation' }), e, { fetch: captcha() });
  assert.equal(r.status, 200); assert.equal(sent.length, 2);
  for (const v of ['Surrey', 'V3T 1A1', 'Bedrooms: 3', 'Size: 1800 sq. ft.', 'New roof', 'Call after 5.']) assert.ok(sent[0].text.includes(v), v);
});

test('delivery: direct email is best-effort when a webhook also took the lead, and required when it is the only destination', async () => {
  const f = async (u) => (String(u).includes('turnstile') ? new Response(JSON.stringify({ success: true })) : new Response('ok'));
  const failing = { send: async () => { throw new Error('no domain'); } };
  const base = { TURNSTILE_SECRET: 's', LEAD_EMAIL_TO: 'a@example.com', LEAD_EMAIL_FROM: 'x@example.com', EMAIL: failing };
  assert.equal((await handleForm(mk(good), { ...base, LEAD_WEBHOOK_URL: 'https://hooks.example/lead' }, { fetch: f })).status, 200);
  assert.equal((await handleForm(mk(good), base, { fetch: f })).status, 502);
});

// "Email me new listings" signup: consent is required, recorded server-side, and the search travels with the lead.
const alertGood = { email: 'pat@example.com', name: 'Pat', consent: 'yes', search: '2 Bedroom Condos for Sale in Abbotsford', search_id: '1451294', page: '/abbotsford-2-bedroom-condos-for-sale.html', 'cf-turnstile-response': 'tok' };
test('listing alert: needs a valid email and the consent box; nothing is stored without them', async () => {
  const e = env(); const P = { path: '/api/forms/listing-alert' };
  const noConsent = await handleForm(mk({ ...alertGood, consent: '' }, P), e, { fetch: captcha() });
  assert.equal(noConsent.status, 422); assert.match((await noConsent.json()).errors.consent, /tick the box/);
  assert.equal((await handleForm(mk({ ...alertGood, consent: 'no' }, P), e, { fetch: captcha() })).status, 422);
  assert.equal((await handleForm(mk({ ...alertGood, email: 'nope' }, P), e, { fetch: captcha() })).status, 422);
  assert.equal((await handleForm(mk({ ...alertGood, search_id: '12; drop' }, P), e, { fetch: captcha() })).status, 422);
  assert.equal(e.LEADS_DB.rows.length, 0);
  assert.equal((await handleForm(mk({ ...alertGood, name: '' }, P), e, { fetch: captcha() })).status, 200);
  assert.equal(e.LEADS_DB.rows.length, 1);
});
test('listing alert: the stored lead carries the server copy of the consent wording, and a spoofed one is ignored', async () => {
  const e = env(); const { ALERT_CONSENT_TEXT } = await import('../src/lib/listing-alert.js');
  await handleForm(mk({ ...alertGood, consent_text: 'I agree to anything' }, { path: '/api/forms/listing-alert' }), e, { fetch: captcha() });
  const stored = JSON.parse(e.LEADS_DB.rows[0][4]);
  assert.equal(stored.consent_text, ALERT_CONSENT_TEXT); assert.equal(stored.consent, 'yes'); assert.equal(stored.search_id, '1451294');
});
test('listing alert: webhook payload gives both inboxes the search, the page and the consent record', async () => {
  const seen = [];
  const f = async (u, init) => { if (String(u).includes('turnstile')) return new Response(JSON.stringify({ success: true })); seen.push(JSON.parse(init.body)); return new Response('ok'); };
  const r = await handleForm(mk(alertGood, { path: '/api/forms/listing-alert' }), { TURNSTILE_SECRET: 's', LEAD_WEBHOOK_URL: 'https://hooks.example/lead', LEAD_EMAIL_TO: 'a@example.com,b@example.com' }, { fetch: f });
  assert.equal(r.status, 200); const p = seen[0];
  assert.equal(p.kind, 'listing-alert'); assert.equal(p.notify_to, 'a@example.com,b@example.com'); assert.equal(p.notify_reply_to, 'pat@example.com');
  assert.match(p.notify_subject, /^New listing alert signup from Pat$/);
  for (const re of [/^Email: pat@example\.com$/m, /^Search: 2 Bedroom Condos for Sale in Abbotsford$/m, /^Search ID \(MyRealPage\): 1451294$/m, /^Search page: https:\/\/jaredgibbons\.ca\/abbotsford-2-bedroom-condos-for-sale\.html$/m, /^Consent: express, given by ticking an unticked box/m, /^Wording shown: "Yes, email me new listings/m]) assert.match(p.notify_text, re);
  const noName = leadEmail({ kind: 'listing-alert', received_at: 't', page: '/x.html', fields: { email: 'e@example.com', consent_text: 'c' } });
  assert.equal(noName.subject, 'New listing alert signup from e@example.com');
});
test('listing alert: captcha, honeypot and origin rules apply like every other form', async () => {
  const e = env(); const P = { path: '/api/forms/listing-alert' };
  const { 'cf-turnstile-response': _t, ...nocap } = alertGood;
  assert.equal((await handleForm(mk(nocap, P), e, { fetch: captcha() })).status, 403);
  assert.equal((await handleForm(mk(alertGood, P), e, { fetch: captcha(false) })).status, 403);
  assert.equal((await handleForm(mk({ ...alertGood, _hp_url: 'http://spam' }, P), e, { fetch: captcha() })).status, 200);
  assert.equal(e.LEADS_DB.rows.length, 0);
  assert.equal((await handleForm(mk(alertGood, { ...P, origin: 'https://evil.example' }), e, { fetch: captcha() })).status, 403);
});
