import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const F = JSON.parse(readFileSync(new URL('../src/data/seo-final.json', import.meta.url), 'utf8'));
const rows = Object.entries(F);

test('seo-final covers the full public page set', () => {
  assert.ok(rows.length >= 1260, `only ${rows.length} entries`);
});
test('titles are 38-60 characters and unique', () => {
  const seen = new Map();
  for (const [s, e] of rows) {
    assert.ok(e.title.length >= 38 && e.title.length <= 60, `${s}: title ${e.title.length}`);
    assert.ok(!seen.has(e.title.toLowerCase()), `${s}: duplicate title with ${seen.get(e.title.toLowerCase())}`);
    seen.set(e.title.toLowerCase(), s);
  }
});
test('H1s are clean: 20-60 characters, no pipe', () => {
  for (const [s, e] of rows) {
    assert.ok(e.h1.length >= 20 && e.h1.length <= 60, `${s}: h1 ${e.h1.length}`);
    assert.ok(!e.h1.includes('|'), `${s}: pipe in h1`);
  }
});
test('descriptions are 135-158 characters, end in a full stop, are unique and carry no stale or banned wording', () => {
  const seen = new Map();
  for (const [s, e] of rows) {
    const d = e.description;
    assert.ok(d.length >= 135 && d.length <= 158, `${s}: description ${d.length}`);
    assert.ok(d.endsWith('.'), `${s}: description does not end in a full stop`);
    assert.ok(!seen.has(d.toLowerCase()), `${s}: duplicate description with ${seen.get(d.toLowerCase())}`);
    seen.set(d.toLowerCase(), s);
    assert.ok(!/sales ratio|snapstats|nothing listed|muse|in this pass|research note|…|\.\.\./i.test(d), `${s}: banned wording`);
    assert.ok(!/(January|February|March|April|May|June|July|August|September|October|November|December).*20\d\d/.test(d), `${s}: dated figure`);
  }
});
