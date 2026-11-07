import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const dist = path.resolve('dist');
const html = (f) => fs.readFileSync(path.join(dist, f), 'utf8');
const pages = fs.readdirSync(dist).filter((f) => f.endsWith('.html'));

test('search pages carry the quiz, seller pages carry the home value form, never both', () => {
  const both = [];
  let quiz = 0, hv = 0;
  for (const f of pages) {
    const h = html(f);
    const q = f !== 'index.html' && h.includes('data-quiz'), v = /id="h-hv"/.test(h);
    if (q) quiz++; if (v) hv++;
    if (q && v) both.push(f);
  }
  assert.deepEqual(both, []);
  assert.ok(quiz > 900, `quiz on ${quiz} pages`);
  assert.ok(hv > 150, `home value form on ${hv} pages`);
  assert.ok(html('south-surrey-condos-for-sale.html').includes('data-quiz'));
  assert.match(html('hazelmere-guide.html'), /What is your Hazelmere home worth\?/);
});

test('pages that already have their own form or calculator get neither block', () => {
  for (const f of ['home-evaluation.html', 'contact.html', 'privacy.html', 'mortgage-calculator.html']) {
    if (!fs.existsSync(path.join(dist, f))) continue;
    const h = html(f);
    assert.ok(!h.includes('data-quiz') && !/id="h-hv"/.test(h), f);
  }
});

test('the home value form posts the fields the Worker requires', () => {
  const h = html('hazelmere-guide.html');
  const m = h.match(/<section class="section section--cream hv"[\s\S]*?<\/section>/);
  assert.ok(m);
  for (const n of ['name="name"', 'name="email"', 'name="address"']) assert.ok(m[0].includes(n), n);
});
