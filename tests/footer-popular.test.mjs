import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const dist = path.resolve('dist');
const html = (f) => fs.readFileSync(path.join(dist, f), 'utf8');

test('every page carries the Popular searches footer with 30 to 45 working links', () => {
  const pages = fs.readdirSync(dist).filter((f) => f.endsWith('.html'));
  for (const f of ['index.html', 'contact.html', 'south-surrey-homes-for-sale.html', 'fort-langley.html']) assert.ok(pages.includes(f), f);
  const bad = [];
  for (const f of pages) {
    const h = html(f);
    if (f === '404.html') continue;
    const m = h.match(/<nav class="footer__popular"[^>]*>([\s\S]*?)<\/nav>/);
    if (!m) { bad.push(`${f}: no popular searches footer`); continue; }
    const links = [...m[1].matchAll(/href="(\/[^"#]*)"/g)].map((x) => x[1]);
    if (links.length < 30 || links.length > 45) bad.push(`${f}: ${links.length} links`);
    if (new Set(links).size !== links.length) bad.push(`${f}: duplicate links`);
  }
  assert.deepEqual(bad.slice(0, 5), []);
});

test('every Popular searches link points at a built page', () => {
  const h = html('index.html');
  const m = h.match(/<nav class="footer__popular"[^>]*>([\s\S]*?)<\/nav>/);
  assert.ok(m, 'footer on home page');
  const missing = [...m[1].matchAll(/href="(\/[^"#]*)"/g)].map((x) => x[1]).filter((l) => !fs.existsSync(path.join(dist, l.slice(1))));
  assert.deepEqual(missing, []);
});
