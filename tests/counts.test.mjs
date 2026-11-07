// A count of exactly 1 must take the singular noun in the local data layer (run tools/fix_counts.py after any generator).
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const dir = path.resolve(import.meta.dirname, '../src/data/local');
const NOUNS = 'condos and townhomes|houses|condos|townhomes|homes|sales|listings|days|neighbourhoods|buildings|schools';
const PAT = new RegExp(`(?<![\\w\\-/$.,#:])1 (${NOUNS})\\b`, 'g');
const LABEL = /(Phase|Hive|Tower|Building|Block|Stage|Wave|Lot|Unit|Zone|Type|Level|Floor|Option|Step|Plan|Schedule|Part|Group|Class|Grade|Category|Section|Rule|Rank|No\.|Number) $/;

test('no "1 houses" style counts in local pages', () => {
  const bad = [];
  for (const f of fs.readdirSync(dir).filter((x) => x.endsWith('.json'))) {
    const t = fs.readFileSync(path.join(dir, f), 'utf8');
    for (const m of t.matchAll(PAT)) if (!LABEL.test(t.slice(Math.max(0, m.index - 12), m.index))) bad.push(`${f}: ${m[0]}`);
  }
  assert.deepEqual(bad.slice(0, 10), []);
});
