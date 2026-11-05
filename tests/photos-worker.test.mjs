import test from 'node:test';
import assert from 'node:assert/strict';
import { handlePhoto, photoKey } from '../src/worker/photos.js';

const store = new Map([['ae8d7fd2e938b2d2-960.webp', { body: 'IMG', size: 3, etag: 'abc', httpEtag: '"abc"' }]]);
const env = { PHOTOS: { get: async (k) => store.get(k) ?? null, head: async (k) => store.get(k) ?? null } };
const req = (m = 'GET', h = {}) => new Request('https://x.test/listing-photos/ae8d7fd2e938b2d2-960.webp', { method: m, headers: h });
const P = '/listing-photos/ae8d7fd2e938b2d2-960.webp';

test('photoKey accepts only hash-size.webp names', () => {
  assert.equal(photoKey(P), 'ae8d7fd2e938b2d2-960.webp');
  for (const bad of ['/listing-photos/../x.webp', '/listing-photos/ae8d7fd2e938b2d2-700.webp', '/listing-photos/AE8D7FD2E938B2D2-960.webp', '/listing-photos/a/b-960.webp', '/listing-photos/']) assert.equal(photoKey(bad), null);
});
test('serves a stored photo with long cache and etag', async () => {
  const r = await handlePhoto(req(), env, P);
  assert.equal(r.status, 200);
  assert.equal(r.headers.get('content-type'), 'image/webp');
  assert.match(r.headers.get('cache-control'), /immutable/);
  assert.equal(await r.text(), 'IMG');
});
test('HEAD has no body, If-None-Match gives 304', async () => {
  const h = await handlePhoto(req('HEAD'), env, P);
  assert.equal(h.status, 200); assert.equal(h.headers.get('content-length'), '3');
  const n = await handlePhoto(req('GET', { 'if-none-match': '"abc"' }), env, P);
  assert.equal(n.status, 304);
});
test('unknown photo, bad name, no binding and wrong method', async () => {
  assert.equal((await handlePhoto(req(), env, '/listing-photos/0000000000000000-960.webp')).status, 404);
  assert.equal((await handlePhoto(req(), env, '/listing-photos/x.webp')).status, 404);
  assert.equal((await handlePhoto(req(), {}, P)).status, 404);
  assert.equal((await handlePhoto(req('POST'), env, P)).status, 405);
});
