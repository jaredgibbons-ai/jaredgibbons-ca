import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { MIN_SALES, figures, classify, rampColor, contrast, textOn, legend, fmt, fmtShort } from '../src/lib/choropleth.js';

const sold = JSON.parse(fs.readFileSync(new URL('../src/data/sold/sold-12m.json', import.meta.url), 'utf8'));

test('figures need 5 closed sales of a type and all three numbers', () => {
  const f = figures({ groups: { house: { n: 45, price: 1960000, ppsf: 489, dom: 30 }, condo: { n: 4, price: null, ppsf: 600, dom: 20 }, townhome: { n: 6, price: 700000, ppsf: null, dom: 20 } } });
  assert.deepEqual(f.house, { n: 45, price: 1960000, ppsf: 489, dom: 30 });
  assert.equal(f.condo, null);
  assert.equal(f.townhome, null);
  assert.equal(MIN_SALES, 5);
  assert.deepEqual(figures(undefined), { house: null, condo: null, townhome: null });
});

test('classify splits into groups and keeps order', () => {
  const c = classify([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
  assert.equal(c.k, 5);
  assert.equal(c.classOf(1), 0); assert.equal(c.classOf(10), 4);
  assert.ok(c.classOf(5) <= c.classOf(6));
  const few = classify([100, 200]);
  assert.equal(few.k, 2);
  const same = classify([5, 5, 5]);
  assert.equal(same.k, 1); assert.equal(same.classOf(5), 0);
});

test('ramp runs light to dark and labels stay readable', () => {
  const k = 5;
  for (let i = 0; i < k; i++) {
    const fill = rampColor(i, k), t = textOn(fill);
    assert.ok(contrast(fill, t === '#111111' ? 'rgb(17,17,17)' : 'rgb(255,255,255)') >= 4.5, `${fill} ${t}`);
  }
  assert.ok(contrast(rampColor(0, 5), rampColor(4, 5)) > 8);
  assert.ok(contrast(rampColor(1, 5), rampColor(0, 5)) > 1.1);
});

test('legend text uses the metric format', () => {
  const l = legend('price', classify([500000, 600000, 700000, 800000, 900000, 1000000]));
  assert.match(l[0].label, /^Under \$/);
  assert.match(l[l.length - 1].label, /and over$/);
  assert.equal(fmt('dom', 21), '21 days');
  assert.equal(fmt('ppsf', 489), '$489');
  assert.equal(fmtShort('price', 1960000), '$1.96M'); assert.equal(fmtShort('price', 1500000), '$1.5M'); assert.equal(fmtShort('price', 785000), '$785K');
  assert.equal(fmtShort('dom', 21), '21 days'); assert.equal(fmtShort('ppsf', 489.4), '$489');
});

// Every area that names a sold-12m sub-area must name one that exists (map files live in src/data/maps).
test('map files point at real sold-12m sub-areas', () => {
  const dir = new URL('../src/data/maps/', import.meta.url);
  for (const f of fs.readdirSync(dir).filter((x) => x.endsWith('.json'))) {
    const r = JSON.parse(fs.readFileSync(new URL(f, dir), 'utf8'));
    for (const a of r.areas) if (a.sold) assert.ok(sold.sub[a.sold], `${f}: ${a.id} -> ${a.sold} not in sold-12m`);
  }
});
