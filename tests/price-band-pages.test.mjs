// Price-band pages (2026-11-07): drafts, own SEO, hub links, data rules.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const read = (f) => JSON.parse(fs.readFileSync(path.join(root, f), 'utf8'));
const dir = path.join(root, 'src/data/local');
const files = fs.readdirSync(dir).filter((f) => f.endsWith('.json'));
const slugs = files.map((f) => f.replace('.json', '')).filter((s) => /^[a-z-]+-(homes-under-1m|homes-under-1-2m|condos-under-600k)$/.test(s) && read(`src/data/local/${s}.json`).search_page?.kind === 'price');
const seo = read('tools/seo_final/fix_02.json');

test('price-band pages: 20 drafts, listings placeholder, own SEO entry, inbound links', () => {
  assert.equal(slugs.length, 20);
  for (const s of slugs) {
    const j = read(`src/data/local/${s}.json`);
    assert.equal(j.status, 'draft', s);
    assert.ok(j.blocks.some((b) => b.t === 'grid'), `${s} no listings placeholder`);
    assert.ok(seo[s] && seo[s].h1.length >= 20 && seo[s].description.length <= 160, `${s} SEO`);
    assert.ok(j.faq.length >= 3, `${s} faq`);
    const n = files.filter((f) => f !== `${s}.json` && JSON.stringify(read(`src/data/local/${f}`)).includes(`${s}.html`)).length;
    assert.ok(n >= 2, `${s} has ${n} inbound links`);
  }
});

test('price-band pages: dated, sourced, tables never show a median under 5 sales', () => {
  for (const s of slugs) {
    const j = read(`src/data/local/${s}.json`);
    const t = JSON.stringify(j);
    assert.match(t, /October 31, 2026/);
    assert.match(t, /Paragon MLS/);
    for (const b of j.blocks.filter((x) => x.t === 'table' && /neighbourhoods/.test(x.caption))) {
      for (const r of b.rows) assert.ok(Number(r[1]) >= 5, `${s} ${r[0]} has ${r[1]} sales`);
    }
  }
});
