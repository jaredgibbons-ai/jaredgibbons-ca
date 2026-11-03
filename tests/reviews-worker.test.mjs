import test from 'node:test';
import assert from 'node:assert/strict';
import worker, { cleanComment, normalizeReview, refresh, handle, accessToken } from '../workers/reviews/src/index.js';

const kv = () => { const m = new Map(); return { m, get: async (k) => m.get(k) ?? null, put: async (k, v) => { m.set(k, v); } }; };
const ENV = () => ({ GOOGLE_CLIENT_ID: 'id', GOOGLE_CLIENT_SECRET: 'sec', GOOGLE_REFRESH_TOKEN: 'ref', GBP_LOCATION: '', REVIEWS_KV: kv() });
const json = (o, status = 200) => new Response(JSON.stringify(o), { status, headers: { 'content-type': 'application/json' } });

function fakeGoogle({ locations = [{ name: 'locations/9', title: 'Jared', metadata: { mapsUri: 'https://maps.google.com/?cid=1', newReviewUri: 'https://search.google.com/local/writereview?placeid=x' } }], pages = 1, tokenStatus = 200, tokenError } = {}) {
  const calls = [];
  const fn = async (url, init = {}) => {
    const u = String(url); calls.push(u);
    if (u.startsWith('https://oauth2.googleapis.com/token')) return tokenStatus === 200 ? json({ access_token: 'at' }) : json({ error: tokenError || 'invalid_grant' }, tokenStatus);
    assert.equal(init.headers?.authorization, 'Bearer at', 'API calls carry the access token');
    if (u.includes('mybusinessaccountmanagement')) return json({ accounts: [{ name: 'accounts/1' }] });
    if (u.includes('mybusinessbusinessinformation')) return json({ locations });
    if (u.includes('/reviews')) {
      const p = Number(new URL(u).searchParams.get('pageToken') || 0);
      return json({
        averageRating: 4.9, totalReviewCount: 3,
        reviews: [{ reviewId: 'r' + p, reviewer: { displayName: 'Sam B.', profilePhotoUrl: 'https://x/p.jpg' }, starRating: 'FIVE', comment: 'Great.', createTime: '2026-10-01T00:00:00Z', reviewReply: { comment: 'Thanks!', updateTime: '2026-10-02T00:00:00Z' } }],
        nextPageToken: p + 1 < pages ? String(p + 1) : undefined,
      });
    }
    return json({}, 404);
  };
  fn.calls = calls; return fn;
}

test('cleanComment keeps the reviewer\'s original words, not the machine translation', () => {
  assert.equal(cleanComment('(Translated by Google) Very good\n\n(Original)\nTrès bien'), 'Très bien');
  assert.equal(cleanComment('  Plain text  '), 'Plain text');
  assert.equal(cleanComment(undefined), '');
});
test('normalizeReview keeps public fields only', () => {
  const n = normalizeReview({ reviewId: 'secret-id', reviewer: { displayName: 'Sam B.', profilePhotoUrl: 'https://x/p.jpg' }, starRating: 'FOUR', comment: 'ok', createTime: '2026-10-01T00:00:00Z' });
  assert.deepEqual(n, { name: 'Sam B.', rating: 4, text: 'ok', date: '2026-10-01T00:00:00Z' });
  assert.equal(normalizeReview({ reviewer: { isAnonymous: true }, starRating: 'FIVE' }).name, 'A Google user');
  assert.equal(normalizeReview({ starRating: 'STAR_RATING_UNSPECIFIED' }), null);
});
test('refresh pulls all pages, stores a public-only copy and reports ok', async () => {
  const env = ENV(); const g = fakeGoogle({ pages: 3 });
  const r = await refresh(env, g);
  assert.deepEqual(r, { ok: true, count: 3 });
  const stored = JSON.parse(env.REVIEWS_KV.m.get('reviews:v1'));
  assert.equal(stored.reviews.length, 3);
  assert.equal(stored.averageRating, 4.9);
  assert.equal(stored.reviewUrl, 'https://search.google.com/local/writereview?placeid=x');
  const text = JSON.stringify(stored);
  for (const secret of ['sec', 'ref', 'accounts/1', 'locations/9', 'profilePhotoUrl', 'p.jpg', 'reviewId']) assert.ok(!text.includes(secret), `leaked ${secret}`);
});
test('a failed pull keeps the old copy and records only an error code', async () => {
  const env = ENV(); await refresh(env, fakeGoogle());
  const before = env.REVIEWS_KV.m.get('reviews:v1');
  const r = await refresh(env, fakeGoogle({ tokenStatus: 400, tokenError: 'invalid_grant' }));
  assert.deepEqual(r, { ok: false, code: 'token_invalid' });
  assert.equal(env.REVIEWS_KV.m.get('reviews:v1'), before);
  const st = JSON.parse(env.REVIEWS_KV.m.get('status:v1'));
  assert.equal(st.ok, false); assert.equal(st.code, 'token_invalid');
  assert.ok(!JSON.stringify(st).includes('ref'));
});
test('wrong client id/secret and missing secrets are told apart', async () => {
  assert.equal((await refresh(ENV(), fakeGoogle({ tokenStatus: 401, tokenError: 'invalid_client' }))).code, 'client_invalid');
  const env = ENV(); delete env.GOOGLE_REFRESH_TOKEN;
  assert.equal((await refresh(env, fakeGoogle())).code, 'missing_secret');
  await assert.rejects(accessToken({}, fakeGoogle()), /not set/);
});
test('several locations need GBP_LOCATION; setting it picks the right one', async () => {
  const locs = [{ name: 'locations/1', title: 'A' }, { name: 'locations/2', title: 'B' }];
  assert.equal((await refresh(ENV(), fakeGoogle({ locations: locs }))).code, 'multiple_locations');
  const env = ENV(); env.GBP_LOCATION = 'locations/2';
  assert.equal((await refresh(env, fakeGoogle({ locations: locs }))).ok, true);
});
test('an empty result never replaces a good copy', async () => {
  const env = ENV(); await refresh(env, fakeGoogle());
  const before = env.REVIEWS_KV.m.get('reviews:v1');
  const empty = async (u) => String(u).includes('/reviews') ? json({ reviews: [] }) : fakeGoogle()(u, { headers: { authorization: 'Bearer at' } });
  const r = await refresh(env, async (u, i) => String(u).includes('oauth2') ? json({ access_token: 'at' }) : empty(u, i));
  assert.equal(r.code, 'empty'); assert.equal(env.REVIEWS_KV.m.get('reviews:v1'), before);
});
test('GET /reviews.json serves the stored copy; 404 before the first pull; no writes', async () => {
  const env = ENV();
  assert.equal((await handle(new Request('https://x/reviews.json'), env)).status, 404);
  await refresh(env, fakeGoogle());
  const res = await handle(new Request('https://x/reviews.json'), env);
  assert.equal(res.status, 200); assert.match(res.headers.get('cache-control'), /max-age=900/);
  assert.equal((await res.json()).reviews.length, 1);
  assert.equal((await handle(new Request('https://x/reviews.json', { method: 'POST' }), env)).status, 405);
  assert.equal((await handle(new Request('https://x/other'), env)).status, 404);
});
test('scheduled handler runs a refresh', async () => {
  const env = ENV(); const orig = globalThis.fetch; globalThis.fetch = fakeGoogle();
  try { let p; await worker.scheduled({}, env, { waitUntil: (x) => { p = x; } }); assert.deepEqual(await p, { ok: true, count: 1 }); }
  finally { globalThis.fetch = orig; }
});

test('site Worker: /api/reviews.json passes through the service binding, and 404s without it', async () => {
  const { build } = await import('esbuild');
  const os = await import('node:os'); const path = await import('node:path'); const fs = await import('node:fs');
  const out = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'site-worker-')), 'w.mjs');
  await build({ entryPoints: ['src/worker/index.js'], bundle: true, format: 'esm', outfile: out, logLevel: 'silent' });
  const site = (await import(out)).default;
  const req = (m = 'GET') => new Request('https://jaredgibbons.ca/api/reviews.json', { method: m });
  assert.equal((await site.fetch(req(), {})).status, 404);
  const REVIEWS = { fetch: async (r) => { assert.equal(new URL(r.url).pathname, '/reviews.json'); return json({ reviews: [{ name: 'A', rating: 5, text: 'x' }] }); } };
  const ok = await site.fetch(req(), { REVIEWS });
  assert.equal(ok.status, 200); assert.equal((await ok.json()).reviews.length, 1);
  assert.equal((await site.fetch(req('POST'), { REVIEWS })).status, 404);
  const down = { fetch: async () => { throw new Error('down'); } };
  assert.equal((await site.fetch(req(), { REVIEWS: down })).status, 404);
});
