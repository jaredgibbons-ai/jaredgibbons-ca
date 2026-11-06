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
  const n = [...rules.redirects.filter((x) => x.source !== 'live-observed'), ...rules.gone].reduce((a, x) => a + x.rows, 0)
    + [...rules.conflicts, ...rules.ignored].reduce((a, x) => a + x.rows.length, 0)
    + Object.values(rules.rows_in_code).reduce((a, x) => a + x, 0);
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
  assert.equal(rules.gone.some((g) => g.from.includes('archive-check')), false);   // the crawler probe is not shipped as a rule
});
test('D-140: no redirect target 404s; doubled-prefix pages, query strings, /404.html, the feed and the PTT page', () => {
  for (const r of rules.redirects) if (!r.to.includes('listing.')) { const t = r.to.split('?')[0]; assert.equal(R(t).type, 'asset', `${r.from} -> ${r.to}`); }
  assert.equal(rules.redirects.filter((r) => r.to.startsWith('/recip.html/')).length, 0);
  assert.deepEqual(R('/our-listings.html/white-rock-condos-for-sale.html'), { type: 'redirect', location: '/white-rock-condos-for-sale.html', status: 301 });
  assert.equal(R('/surrey-open-houses.html/not-a-real-page.html').type, 'notfound');
  assert.equal(R('/contact-us?utm_source=postcard').location, '/contact.html?utm_source=postcard');
  assert.equal(R('/404.html').type, 'notfound');
  assert.equal(R('/blog.html/blog.feed').status, 410);
  assert.equal(R('/bc-property-transfer-tax-calculator.html').location, '/first-time-buyer-calculator.html');
  assert.equal(R('/langley-condos-under-700k.html').location, '/langley-condos-for-sale.html');
});
test('nested paths map to internal prefixes without clashing with their parent page', () => {
  const fake = (p) => ['/blog.html', '/internal/blog/some-post-123.html', '/internal/listings/listing.r1.1.html'].includes(p);
  assert.deepEqual(route('https://jaredgibbons.ca/blog.html', idx, fake), { type: 'asset', path: '/blog.html' });
  assert.deepEqual(route('https://jaredgibbons.ca/blog.html/some-post-123', idx, fake), { type: 'asset', path: '/internal/blog/some-post-123.html' });
  assert.deepEqual(route('https://jaredgibbons.ca/our-listings.html/listing.r1.1', idx, fake), { type: 'asset', path: '/internal/listings/listing.r1.1.html' });
  assert.equal(route('https://jaredgibbons.ca/blog.html/missing', idx, fake).type, 'notfound');
  assert.equal(route('https://jaredgibbons.ca/internal/blog/some-post-123.html', idx, fake).type, 'notfound');   // not served directly
});

// ---- full Worker, bundled the way wrangler bundles it, with a fake ASSETS binding over dist/
const out = path.join('node_modules', '.cache-worker-test.mjs');
execFileSync('npx', ['esbuild', 'src/worker/index.js', '--bundle', '--format=esm', `--outfile=${out}`, '--log-level=error'], { stdio: 'inherit' });
const worker = (await import(path.resolve(out))).default;
const env = {
  INDEXABLE: 'false',
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
test('worker: blog post and own-listing pages are served at their public URLs; /internal is never public', async () => {
  const post = fs.readdirSync(path.join(DIST, 'internal/blog')).find((f) => f.includes('salmon-sessions'));
  let r = await call('/blog.html/' + post.replace(/\.html$/, ''));
  assert.equal(r.status, 200); assert.match(await r.text(), /<title>Salmon Sessions Music Festival Returns to South Surrey<\/title>/);
  const lst = fs.readdirSync(path.join(DIST, 'internal/listings')).find((f) => f.includes('similkameen'));
  r = await call('/our-listings.html/' + lst.replace(/\.html$/, ''));
  assert.equal(r.status, 200); assert.match(await r.text(), /511 Similkameen Ave Princeton BC \| MLS 10374265/);
  assert.equal((await call('/internal/blog/' + post)).status, 404);
  assert.equal((await call('/internal/listings/' + lst)).status, 404);
  assert.equal((await call('/blog.html/not-a-real-post-1')).status, 404);
  assert.equal((await call('/blog.html')).status, 200);
});
test('worker D-140: fail-safe noindex, security headers on every answer, redirect cache, real 404 status, trailing-slash nested path', async () => {
  const lst = fs.readdirSync(path.join(DIST, 'internal/listings')).find((f) => f.includes('similkameen')).replace(/\.html$/, '');
  let r = await call('/our-listings.html/' + lst + '/', { redirect: 'manual' });
  assert.equal(r.status, 301); assert.equal(r.headers.get('location'), '/our-listings.html/' + lst);
  r = await call('/contact-us?utm_source=postcard', { redirect: 'manual' });
  assert.equal(r.headers.get('location'), '/contact.html?utm_source=postcard'); assert.equal(r.headers.get('cache-control'), 'public, max-age=3600');
  assert.equal((await call('/404.html')).status, 404);
  assert.equal((await call('/blog.html/blog.feed')).status, 410);
  r = await call('/cedar-hills.html');
  for (const h of ['x-frame-options', 'content-security-policy', 'permissions-policy', 'strict-transport-security']) assert.ok(r.headers.get(h), h);
  // every answer is noindex unless INDEXABLE is exactly "true": a boolean, "TRUE", "1" or nothing all stay closed
  for (const v of [undefined, 'false', true, 'TRUE', '1', 'yes']) { r = await worker.fetch(new Request('https://jaredgibbons.ca/cedar-hills.html'), { ...env, INDEXABLE: v }); assert.equal(r.headers.get('x-robots-tag'), 'noindex, nofollow', String(v)); }
  r = await worker.fetch(new Request('https://jaredgibbons.ca/cedar-hills.html'), { ...env, INDEXABLE: 'true' });
  assert.equal(r.headers.get('x-robots-tag'), null);
  // API and photo answers carry the same headers
  r = await call('/api/reviews.json'); assert.equal(r.headers.get('x-robots-tag'), 'noindex, nofollow'); assert.ok(r.headers.get('x-frame-options'));
  r = await call('/listing-photos/abc-480.webp'); assert.equal(r.headers.get('x-robots-tag'), 'noindex, nofollow');
});
test('worker: only GET and HEAD', async () => {
  assert.equal((await call('/', { method: 'POST' })).status, 405);
  assert.equal((await call('/', { method: 'HEAD' })).status, 200);
});

test('live-observed redirects: alias to the full listing URL; gone listings to the MLS search page', () => {
  assert.deepEqual(R('/our-listings.html/listing.440-15850-26-avenue-surrey.106612252'), { type: 'redirect', location: '/our-listings.html/listing.r3036816-440-15850-26-avenue-surrey-bc-v3s-2n6.106612252', status: 301 });
  assert.equal(R('/our-listings.html/listing.145-2853-helc-place-surrey-bc-v3z-0n5-r3080492.107675553').location, '/recip.html');
  assert.equal(R('/mylistings.html/listing.220-15735-croydon-drive-surrey-bc-v3z-2l5-r3076297.107593610').location, '/recip.html');
});
test('recaptured pages are served', () => {
  for (const p of ['/about.html', '/testimonials.html', '/whalley-guide.html', '/metrotown-homes-for-sale.html', '/our-listings.html/listing.r2225442-117-14833-61-avenue-surrey-bc.102314544'])
    assert.equal(R(p).type, 'asset', p);
});

test('redirects added on the live site after the archive: old slugs reach live pages, none is a loop or a miss', () => {
  const pairs = { '/broiler-farms.html': '/broiler-farms-for-sale-bc.html', '/contact-us': '/contact.html', '/cloverdale.html': '/cloverdale-bc.html', '/brunette.html': '/new-westminster-homes-for-sale.html', '/west-meadows-pitt-meadows.html': '/west-meadows-pitt-meadows-guide.html', '/property-search.html': '/recip.html' };
  for (const [from, to] of Object.entries(pairs)) assert.deepEqual(R(from), { type: 'redirect', location: to, status: 301 }, from);
  for (const x of rules.redirects.filter((y) => y.source === 'live-observed' && !y.to.includes('listing.') && y.to !== '/recip.html')) {
    assert.ok(exists(x.to) || exists(x.to.replace(/\/?$/, '')), `${x.from} -> ${x.to} must be a built page`);
    assert.equal(R(x.to).type, 'asset', x.to);
  }
});

test('legacy blog month and filter URLs redirect to the blog index', () => {
  for (const p of ['/blog.html/archives/2026/10/', '/blog.html/archives/2025/04', '/blog.html/blog.html', '/blog.html/blog.html/archives/2026/10/']) {
    assert.deepEqual(R(p), { type: 'redirect', location: '/blog.html', status: 301 }, p);
  }
});
