// Run: npm run build && node --test tests/
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { buildIndex, route } from '../src/worker/route.js';

const rules = JSON.parse(fs.readFileSync('src/worker/rules.json', 'utf8'));
const DIST = 'dist';
const exists = (p) => { try { return fs.statSync(path.join(DIST, p)).isFile(); } catch { return false; } };
const idx = buildIndex(rules);
const R = (p) => route(`https://jaredgibbons.ca${p}`, idx, exists);

test('rules account for all 81 archive rows', () => {
  const n = [...rules.hostRules, ...rules.redirects, ...rules.gone].reduce((a, x) => a + x.rows, 0)
    + [...rules.conflicts, ...rules.ignored].reduce((a, x) => a + x.rows.length, 0);
  assert.equal(n, 81);
});
test('host rules: http and www go to https apex', () => {
  assert.deepEqual(route('http://jaredgibbons.ca/', idx, exists), { type: 'redirect', location: 'https://jaredgibbons.ca/', status: 301 });
  assert.deepEqual(route('https://www.jaredgibbons.ca/x.html?a=1', idx, exists), { type: 'redirect', location: 'https://jaredgibbons.ca/x.html?a=1', status: 301 });
});
test('every archive redirect row behaves as documented', () => {
  for (const r of rules.redirects) {
    const full = route(`https://jaredgibbons.ca${r.from}`, idx, exists);
    assert.deepEqual(full, { type: 'redirect', location: r.to, status: r.status }, r.from);
  }
});
test('every "broken at source" row and every conflict is a 404', () => {
  for (const g of rules.gone) assert.equal(R(g.from).type, 'notfound', g.from);
  for (const c of rules.conflicts) assert.equal(R(c.from).type, 'notfound', c.from);
});
test('home and built pages resolve to assets', () => {
  assert.deepEqual(R('/'), { type: 'asset', path: '/index.html' });
  for (const p of ['/fort-langley.html', '/cedar-hills.html', '/reviews.html', '/index.html']) assert.deepEqual(R(p), { type: 'asset', path: p });
});
test('explicit and generic legacy forms', () => {
  assert.equal(R('/contact').location, '/contact.html');
  assert.equal(R('/contact-us/').location, '/contact.html');
  assert.equal(R('/cedar-hills').location, '/cedar-hills.html');         // extensionless -> .html when it exists
  assert.equal(R('/cedar-hills.html/').location, '/cedar-hills.html');   // trailing slash
  assert.equal(R('/no-such-page').type, 'notfound');
});
test('tracking, CMS preview and pagination params serve the page (no redirect, analytics intact)', () => {
  assert.deepEqual(R('/brookswood.html?utm_source=chatgpt.com'), { type: 'asset', path: '/brookswood.html' });
  assert.deepEqual(R('/?p=42126&preview=true'), { type: 'asset', path: '/index.html' });
  assert.deepEqual(R('/fort-langley.html?_pg=2'), { type: 'asset', path: '/fort-langley.html' });
  assert.equal(R('/bayridge.html?_pg=2').type, 'notfound');              // documented 404 at source
});
test('archive 404 reference path is a real 404', () => {
  assert.equal(R('/this-page-does-not-exist-archive-check').type, 'notfound');
});
test('nested paths map to internal prefixes without clashing with their parent page', () => {
  const fake = (p) => ['/blog.html', '/_blog/some-post-123.html', '/_listings/listing.r1.1.html'].includes(p);
  assert.deepEqual(route('https://jaredgibbons.ca/blog.html', idx, fake), { type: 'asset', path: '/blog.html' });
  assert.deepEqual(route('https://jaredgibbons.ca/blog.html/some-post-123', idx, fake), { type: 'asset', path: '/_blog/some-post-123.html' });
  assert.deepEqual(route('https://jaredgibbons.ca/our-listings.html/listing.r1.1', idx, fake), { type: 'asset', path: '/_listings/listing.r1.1.html' });
  assert.equal(route('https://jaredgibbons.ca/blog.html/missing', idx, fake).type, 'notfound');
});

// ---- full Worker, bundled the way wrangler bundles it, with a fake ASSETS binding over dist/
const out = path.join('node_modules', '.cache-worker-test.mjs');
execFileSync('npx', ['esbuild', 'src/worker/index.js', '--bundle', '--format=esm', `--outfile=${out}`, '--log-level=error'], { stdio: 'inherit' });
const worker = (await import(path.resolve(out))).default;
const env = {
  PREVIEW: 'true',
  ASSETS: { async fetch(req) {
    const p = new URL(req.url).pathname;
    if (!exists(p)) return new Response('nope', { status: 404 });
    return new Response(req.method === 'HEAD' ? null : fs.readFileSync(path.join(DIST, p)), { status: 200, headers: { 'content-type': p.endsWith('.html') ? 'text/html; charset=utf-8' : 'application/octet-stream' } });
  } },
};
const call = (p, init) => worker.fetch(new Request(`https://jaredgibbons.ca${p}`, init), env);

test('worker: page 200, redirect headers, real 404 status + body, noindex header', async () => {
  let r = await call('/cedar-hills.html');
  assert.equal(r.status, 200); assert.match(await r.text(), /Cedar Hills Homes for Sale/);
  assert.equal(r.headers.get('x-robots-tag'), 'noindex, nofollow'); assert.equal(r.headers.get('x-content-type-options'), 'nosniff');
  r = await call('/contact', { redirect: 'manual' });
  assert.equal(r.status, 301); assert.equal(r.headers.get('location'), '/contact.html');
  r = await call('/this-page-does-not-exist-archive-check');
  assert.equal(r.status, 404); assert.match(await r.text(), /Page not found/);
  r = await call('/esplanade-grande-waterstone-condo-for-sale/');
  assert.equal(r.status, 404);
});
test('worker: only GET and HEAD', async () => {
  assert.equal((await call('/', { method: 'POST' })).status, 405);
  assert.equal((await call('/', { method: 'HEAD' })).status, 200);
});
