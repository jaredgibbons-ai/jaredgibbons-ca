import test from 'node:test';
import assert from 'node:assert/strict';
import { handleForm, validate } from '../src/worker/forms.js';

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
  const e = env(); const r = await handleForm(mk({ ...good, website: 'http://spam' }), e, { fetch: captcha() });
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
  const r = await handleForm(mk(good), { TURNSTILE_SECRET: 's', LEAD_WEBHOOK_URL: 'https://hooks.example/lead' }, { fetch: f });
  assert.equal(r.status, 200); assert.equal(seen[0].kind, 'contact'); assert.equal(seen[0].fields.name, 'Pat Example');
  const bad = async (u) => (String(u).includes('turnstile') ? new Response(JSON.stringify({ success: true })) : new Response('x', { status: 500 }));
  assert.equal((await handleForm(mk(good), { TURNSTILE_SECRET: 's', LEAD_WEBHOOK_URL: 'https://hooks.example/lead' }, { fetch: bad })).status, 502);
});
test('schemas: property check needs only an address; home evaluation needs contact details', () => {
  assert.deepEqual(validate('property-check', { address: '1 Main St' }).errors, {});
  assert.ok(validate('home-evaluation', { address: '1 Main St' }).errors.email);
});
