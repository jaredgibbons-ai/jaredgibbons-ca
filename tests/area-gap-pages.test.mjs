// Area gap pages (2026-11-07): rules that must hold before these pages can go live.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const read = (f) => JSON.parse(fs.readFileSync(path.join(root, f), 'utf8'));
const local = (s) => read(`src/data/local/${s}.json`);
const seo = read('tools/seo_final/fix_02.json');
const NEW = ['north-vancouver-condos-for-sale', 'furry-creek-homes-for-sale', 'ocean-park-homes-for-sale', 'crescent-beach-homes-for-sale'];
const text = (o) => JSON.stringify(o);

test('area gap pages: drafts with a listings placeholder, own SEO entry and at least 3 inbound links', () => {
  const files = fs.readdirSync(path.join(root, 'src/data/local')).filter((f) => f.endsWith('.json'));
  for (const s of NEW) {
    const j = local(s);
    assert.equal(j.status, 'draft', s);
    assert.ok(j.blocks.some((b) => b.t === 'grid'), `${s} has no listings placeholder`);
    assert.ok(seo[s] && seo[s].h1.length >= 20, `${s} has no SEO entry`);
    const n = files.filter((f) => f !== `${s}.json` && text(read(`src/data/local/${f}`)).includes(`${s}.html`)).length;
    assert.ok(n >= 3, `${s} has only ${n} inbound links`);
  }
});

test('Ocean Park and Crescent Beach pages say the sold figures cover both communities and never claim a radius or a separate median', () => {
  for (const s of ['ocean-park-homes-for-sale', 'crescent-beach-homes-for-sale']) {
    const t = text(local(s));
    assert.match(t, /F53/);
    assert.match(t, /(together|both)/);
    assert.match(t, /(listing names|mentions|mention)/);
    assert.doesNotMatch(t, /within \d+ ?(km|metres|miles)/i);
  }
});

test('neighbourhood sold blocks: dated, sourced, medians only where at least 5 homes sold', () => {
  const nb = read('src/data/sold/neighbourhood-2026-11-07.json');
  for (const s of ['morgan-creek', 'grandview-surrey', 'crescent-beach-ocean-park-guide']) {
    const b = local(s).blocks.filter((x) => x.gen === 'nbsold');
    assert.ok(b.length >= 4, `${s} has no sold block`);
    const t = text(b);
    assert.match(t, /November 7, 2026/);
    assert.match(t, /Source:/);   // the 5-sale rule is stated once on the methodology page each source line links to (D-227)
  }
  assert.match(JSON.stringify(local('data-and-methodology')), /at least 5 homes sold/);
  for (const a of Object.values(nb.areas)) for (const g of Object.values(a.groups)) for (const k of ['12', '6']) assert.ok(Array.isArray(g[k]) && g[k].length === 2);
  const cb = local('crescent-beach-ocean-park-guide').blocks.find((x) => x.t === 'table' && x.gen === 'nbsold');
  const rows = cb.rows ?? [];
  for (const r of rows) { const n12 = Number(String(r[1]).replace(/,/g, '')); if (n12 < 5) assert.equal(r[2], '—', 'median shown under 5 sales'); }
});

test('Furry Creek page shows no median, because fewer than 5 homes sold', () => {
  const t = text(local('furry-creek-homes-for-sale'));
  assert.doesNotMatch(t, /median price of \$/i);
  assert.match(t, /at least 5 sales/);
});
