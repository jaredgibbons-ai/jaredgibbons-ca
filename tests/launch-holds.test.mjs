// Launch approval pack (2026-11-07): holds.json and the approval CSV agree, and a held page is a real new page.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const holds = JSON.parse(fs.readFileSync(path.join(root, 'src/data/launch/holds.json'), 'utf8'));
const csv = fs.readdirSync(path.join(root, 'docs/review/launch')).filter((f) => f.startsWith('launch-approval-') && f.endsWith('.csv')).sort().pop();
const rows = fs.readFileSync(path.join(root, 'docs/review/launch', csv), 'utf8').trim().split('\n').slice(1);

test('every held page is a new page with a reason', () => {
  for (const [slug, why] of Object.entries(holds)) {
    const f = path.join(root, `src/data/local/${slug}.json`);
    assert.ok(fs.existsSync(f), `${slug} has no local page`);
    assert.ok(JSON.parse(fs.readFileSync(f, 'utf8')).new_page, `${slug} is not a new page`);
    assert.ok(String(why).length > 20, `${slug} has no reason`);
  }
});

test('approval CSV lists every new page once and its Hold rows match holds.json', () => {
  const slugs = rows.map((r) => r.split(',').find((c) => /^[a-z0-9-]+$/.test(c) && fs.existsSync(path.join(root, `src/data/local/${c}.json`))));
  assert.equal(new Set(slugs).size, rows.length);
  const heldInCsv = rows.filter((r) => /,Hold,/.test(r)).length;
  assert.equal(heldInCsv, Object.keys(holds).length);
  const newPages = fs.readdirSync(path.join(root, 'src/data/local')).filter((f) => f.endsWith('.json')).filter((f) => JSON.parse(fs.readFileSync(path.join(root, 'src/data/local', f), 'utf8')).new_page).length;
  assert.equal(rows.length, newPages);
});
