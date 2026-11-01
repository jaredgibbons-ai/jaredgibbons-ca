import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { execSync } from 'node:child_process';
import gate from '../src/data/inventory/gate.json' with { type: 'json' };

const gated = Object.entries(gate.pages).filter(([, v]) => v.action === 'noindex').map(([k]) => k);

test('every gated page is a real page and every one is under 5 active listings', () => {
  for (const [slug, v] of Object.entries(gate.pages)) {
    assert.ok(existsSync(new URL(`../src/data/pages/${slug}.json`, import.meta.url)), slug + ' exists');
    assert.ok(v.active < 5, slug + ' is under the 5-listing rule');
  }
});

test('gated pages are left out of the sitemap and the rest of the site is not', { skip: !existsSync(new URL('../dist/sitemap.xml', import.meta.url)) }, () => {
  const xml = readFileSync(new URL('../dist/sitemap.xml', import.meta.url), 'utf8');
  for (const slug of gated) assert.ok(!xml.includes(`/${slug}.html<`), slug + ' must not be in the sitemap');
  assert.ok(xml.includes('/sell-my-house-in-mission.html<'));
  assert.ok(xml.includes('/westham-island-guide.html<'), 'guides flagged keep stay in the sitemap');
});

test('a launch-mode build gives gated pages noindex, follow and ordinary pages index, follow', { timeout: 120000 }, () => {
  execSync('npx astro build --outDir /tmp/launch-check', { env: { ...process.env, PUBLIC_PREVIEW: 'false' }, stdio: 'ignore' });
  const meta = (f) => (/<meta name="robots" content="([^"]*)"/.exec(readFileSync(`/tmp/launch-check/${f}.html`, 'utf8')) || [])[1];
  assert.equal(meta('big-bend'), 'noindex, follow');
  assert.equal(meta('sell-my-house-in-mission'), 'index, follow');
  assert.equal(meta('404'), 'noindex');
  const preview = (/<meta name="robots" content="([^"]*)"/.exec(readFileSync('dist/big-bend.html', 'utf8')) || [])[1];
  assert.equal(preview, 'noindex, nofollow', 'normal builds stay fully closed');
});
