import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { execSync } from 'node:child_process';
import gate from '../src/data/inventory/gate.json' with { type: 'json' };
import uniq from '../src/data/inventory/uniqueness.json' with { type: 'json' };

const held = uniq.enforce ? Object.entries(uniq.scores).filter(([, v]) => v < uniq.min_unique).map(([k]) => k) : [];

test('every slug in the listing gate is a real page and history is dated', () => {
  for (const [slug, v] of Object.entries(gate.pages)) {
    assert.ok(existsSync(new URL(`../src/data/pages/${slug}.json`, import.meta.url)), slug + ' exists');
    assert.ok(v.history.length >= 1 && v.history.every((h) => /^\d{4}-\d{2}$/.test(h.month)));
  }
});

test('one month of counts never gates a page (rolling 3-month average)', { skip: !existsSync(new URL('../dist/sitemap.xml', import.meta.url)) }, () => {
  const xml = readFileSync(new URL('../dist/sitemap.xml', import.meta.url), 'utf8');
  for (const [slug, v] of Object.entries(gate.pages)) if (v.history.length < gate.min_months) assert.ok(xml.includes(`/${slug}.html<`), slug + ' must stay in the sitemap');
});

test('new pages under the uniqueness threshold are left out of the sitemap', { skip: !existsSync(new URL('../dist/sitemap.xml', import.meta.url)) }, () => {
  const xml = readFileSync(new URL('../dist/sitemap.xml', import.meta.url), 'utf8');
  for (const slug of held) assert.ok(!xml.includes(`/${slug}.html<`), slug + ' must not be in the sitemap');
  assert.ok(xml.includes('/sell-my-house-in-mission.html<'));
});

test('a launch-mode build emits each page its own robots value; normal builds stay closed', { timeout: 120000 }, () => {
  execSync('npx astro build --outDir /tmp/launch-check', { env: { ...process.env, PUBLIC_PREVIEW: 'false' }, stdio: 'ignore' });
  const meta = (dir, f) => (/<meta name="robots" content="([^"]*)"/.exec(readFileSync(`${dir}/${f}.html`, 'utf8')) || [])[1];
  assert.equal(meta('/tmp/launch-check', 'sell-my-house-in-mission'), 'index, follow');
  assert.equal(meta('/tmp/launch-check', '404'), 'noindex');
  for (const slug of held.slice(0, 3)) assert.equal(meta('/tmp/launch-check', slug), 'noindex, follow');
  assert.equal(meta('dist', 'sell-my-house-in-mission'), 'noindex, nofollow', 'normal builds stay fully closed');
});
