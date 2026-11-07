// "Homes for sale near a school" pages (wave 1): data rules that must hold before any of them can go live.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const read = (f) => JSON.parse(fs.readFileSync(path.join(root, f), 'utf8'));
const W = read('src/data/schools/wave1-pages.json');
const idx = read('src/data/idx-embeds.json');
const seo = read('tools/seo_final/fix_02.json');
const local = (s) => read(`src/data/local/${s}.json`);

test('school pages: every built page is a draft with its own saved search, title and description', () => {
  assert.ok(W.built.length >= 100);
  const titles = new Set(), descs = new Set();
  for (const s of W.built) {
    const j = local(s);
    assert.equal(j.status, 'draft', s);
    assert.ok(j.blocks.some((b) => b.t === 'grid'), `${s} has no listings placeholder`);
    assert.match(String(idx.pages[s] ?? ''), /^\d{7}$/, `${s} has no saved search`);
    assert.ok(seo[s], `${s} has no SEO entry`);
    assert.ok(!titles.has(seo[s].title) && !descs.has(seo[s].description), `${s} duplicates a title or description`);
    titles.add(seo[s].title); descs.add(seo[s].description);
    assert.match(seo[s].h1, /^Homes for Sale Near /);
  }
});

test('school pages: held pages (0 listings) are not built and not wired', () => {
  for (const h of W.held) {
    assert.ok(!fs.existsSync(path.join(root, `src/data/local/${h.slug}.json`)), `${h.slug} should be held`);
    assert.ok(!(h.slug in idx.pages), `${h.slug} should not be wired`);
  }
});

test('school pages: at least 3 pages link to every school page', () => {
  const inb = new Map();
  const walk = (o, src) => {
    if (Array.isArray(o)) o.forEach((v) => walk(v, src));
    else if (o && typeof o === 'object') {
      if (typeof o.h === 'string') { const m = o.h.match(/^\/(homes-near-[a-z0-9-]+)\.html$/); if (m && m[1] !== src) (inb.get(m[1]) ?? inb.set(m[1], new Set()).get(m[1])).add(src); }
      Object.values(o).forEach((v) => walk(v, src));
    }
  };
  for (const d of ['src/data/local', 'src/data/pages']) for (const f of fs.readdirSync(path.join(root, d))) if (f.endsWith('.json')) walk(read(`${d}/${f}`), f.slice(0, -5));
  for (const s of W.built) assert.ok((inb.get(s)?.size ?? 0) >= 3, `${s} has ${inb.get(s)?.size ?? 0} inbound links`);
});

test('school pages: no quality, ranking or catchment claims, and the radius is described honestly', () => {
  const bad = /\b(best school|top[- ]rated|top school|rated|ranking|ranked|fraser institute|guaranteed|in the catchment of|zoned for)\b/i;
  for (const s of W.built) {
    const j = local(s);
    const txt = JSON.stringify([j.blocks, j.faq, seo[s]]);
    assert.ok(!bad.test(txt), `${s} makes a claim we cannot back: ${txt.match(bad)?.[0]}`);
    assert.ok(/names? /i.test(txt) && /MLS®/.test(txt), `${s} does not explain how the search finds homes`);
  }
});

test('school pages: a sold section appears only with at least 10 sales and shows no addresses', () => {
  const sold = read('src/data/schools/radius-sold.json');
  for (const s of W.built) {
    const j = local(s); const has = j.blocks.some((b) => b.t === 'table' && /sold within/.test(b.caption ?? ''));
    const d = sold[s.replace(/^homes-near-/, '')];
    assert.equal(has, !!(d && d.n >= 10), s);
  }
  for (const d of Object.values(sold)) assert.ok(!('rows_detail' in d) && !JSON.stringify(d).match(/\bR\d{7}\b/), 'sold figures must not hold listing rows');
});
