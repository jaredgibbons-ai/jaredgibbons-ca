// Thin-trend rule, methodology page and net-proceeds calculator guards (Jared, 2026-11-01).
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const LOCAL = 'src/data/local';
const texts = [];
for (const f of fs.readdirSync(LOCAL)) {
  if (!f.endsWith('.json')) continue;
  texts.push([f, fs.readFileSync(path.join(LOCAL, f), 'utf8')]);
}

test('no listing-count rise or fall is stated on counts under 3 or a change under 1.5%', () => {
  const re = /(?:rose|fell) from ([\d,]+) in (\w+) to ([\d,]+) in (\w+)/g;
  let n = 0;
  for (const [f, t] of texts) {
    for (const m of t.matchAll(re)) {
      const a = +m[1].replace(/,/g, ''), b = +m[3].replace(/,/g, ''); n++;
      assert.ok(a >= 3 && b >= 3, `${f}: ${m[0]} uses a count under 3`);
      assert.ok(Math.abs((100 * (b - a)) / a) >= 1.5, `${f}: ${m[0]} is under 1.5%`);
    }
  }
  assert.ok(n > 50, 'expected generated rise/fall sentences to check');
});

test('no "held" or "unchanged" count wording left from the old generators', () => {
  for (const [f, t] of texts) {
    if (!/"gen": "(snapstats|communitypage|typepage|condopage|musefaq|gap|brentwood)"/.test(t)) continue;
    assert.ok(!/ held (from|at) [\d,]+/.test(t), `${f} still says "held"`);
  }
});

test('methodology page exists, is linked from the footer and states both rules', () => {
  const html = fs.readFileSync('dist/data-and-methodology.html', 'utf8');
  assert.match(html, /1\.5%/); assert.match(html, /under 3/);
  for (const p of ['dist/index.html', 'dist/surrey-homes-for-sale.html']) {
    if (fs.existsSync(p)) assert.match(fs.readFileSync(p, 'utf8'), /href="\/data-and-methodology\.html"/);
  }
});

test('net-proceeds calculator ships with no default values or built-in rates', () => {
  const html = fs.readFileSync('dist/seller-net-proceeds-calculator.html', 'utf8');
  const inputs = [...html.matchAll(/<input[^>]*data-k="[^"]+"[^>]*>/g)].map((m) => m[0]);
  assert.ok(inputs.length >= 8);
  for (const i of inputs) assert.ok(!/\svalue=/.test(i), `input has a default value: ${i}`);
  assert.ok(!/action=|method="post"/i.test(html.match(/<form class="npc"[^>]*>/)[0]), 'calculator form must not submit anywhere');
  assert.match(html, /no commission, legal or closing-cost rates are built in/i);
});

test('sold layer holds grouped figures only: no MLS numbers, addresses or single-sale prices', () => {
  const raw = fs.readFileSync('src/data/sold/sold-12m.json', 'utf8');
  assert.ok(!/\bR[23]\d{6}\b/.test(raw), 'an MLS number is in the sold aggregate');
  assert.ok(!/"Sold Price"|"ML #"|"Status"/.test(raw), 'raw column names found in the sold aggregate');
  const agg = JSON.parse(raw);
  for (const [k, v] of Object.entries(agg.sub)) for (const [g, s] of Object.entries(v.groups)) {
    if (s.n < 5) assert.ok(s.price === undefined || s.n >= 3, `${k} ${g}`);
    if (s.n < 3) assert.ok(s.price === undefined, `${k} ${g} has a price on fewer than 3 sales`);
  }
  for (const [k, v] of Object.entries(agg.sub)) for (const c of Object.values(v.complexes)) for (const b of c) assert.ok(b.n >= 3, `${k} ${b.name}`);
});

test('sold tables never show a price for fewer than 5 sales and name buildings only with 5+', () => {
  let tables = 0;
  for (const [f, t] of texts) {
    const j = JSON.parse(t);
    for (const b of j.blocks || []) {
      if (b.gen !== 'sold' || b.t !== 'table') continue;
      tables++;
      for (const r of b.rows) {
        const n = parseInt(String(r[1]).replace(/,/g, ''), 10);
        if (/buildings and complexes/.test(b.caption)) assert.ok(n >= 5, `${f}: building with ${n} sales named`);
        else if (n < 5) assert.match(r[2], /Too few/, `${f}: a price is shown for ${n} sales`);
      }
    }
  }
  assert.ok(tables > 100, 'expected sold tables to check');
});
