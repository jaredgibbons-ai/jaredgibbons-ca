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

test('55+ notes pages: no MLS numbers, no listing-level links, 5+ FAQ and 5+ links', () => {
  let pages = 0;
  for (const [f, t] of texts) {
    const d = JSON.parse(t);
    if (!(d.blocks || []).some((b) => b.gen === 'n55')) continue;
    if (!d.n55_page) continue;
    pages++;
    assert.ok(!/\bR[23]\d{6}\b/.test(t), `${f}: MLS number published`);
    assert.ok(!/zolo\.ca|estateblock|realtor\.ca|soldbycraig|zealty|rew\.ca\/properties|plsrealestate/i.test(t), `${f}: listing-level link`);
    assert.ok(!/\*\*|Section [1-5]\b(?![\d.]\d)|base guide/.test(t.replace(/Zoning Bylaw[^"]{0,40}Section \d+|Section \d{3}/g, '')), `${f}: note markup left in text`);
    assert.ok(!/\d+ (attached|detached) listings/.test(t), `${f}: board listing count published`);
    assert.ok((d.faq || []).length >= 5, `${f}: fewer than 5 FAQ`);
    const links = t.match(/"h": "\//g) || [];
    assert.ok(links.length >= 5, `${f}: fewer than 5 internal links`);
  }
  assert.ok(pages >= 20, 'expected the 55+ notes pages');
});

test('55+ park sections on mobile-home pages: no MLS numbers, listing links, note markup or board counts', () => {
  let n = 0;
  for (const [f, t] of texts) {
    if (!t.includes('"n55mh"')) continue;
    n++;
    const d = JSON.parse(t);
    const mine = JSON.stringify([(d.blocks || []).filter((b) => b.gen === 'n55mh'), (d.faq || []).filter((x) => x.gen === 'n55mh')]);
    assert.ok(!/\bR[23]\d{6}\b/.test(mine), `${f}: MLS number published`);
    assert.ok(!/zolo\.ca|estateblock|realtor\.ca|soldbycraig|zealty|rew\.ca\/properties|plsrealestate/i.test(mine), `${f}: listing-level link`);
    assert.ok(!/\*\*|\bSection [1-5]\b(?![\d.]\d)|base guide|\d+ (attached|detached) listings/.test(mine), `${f}: note markup or board count`);
  }
  assert.ok(n >= 6, 'expected the mobile-home park sections');
});

test('condo, townhome and land sections (gen tn): no MLS numbers, listing links, note references or board counts', () => {
  let n = 0, hubs = 0;
  for (const [f, t] of texts) {
    const d = JSON.parse(t);
    const mine = JSON.stringify([(d.blocks || []).filter((b) => b.gen === 'tn'), (d.faq || []).filter((x) => x.gen === 'tn')]);
    if (d.tn_page) { hubs++; assert.ok((d.faq || []).length >= 5, `${f}: fewer than 5 FAQ`); assert.ok((t.match(/"h": "\//g) || []).length >= 5, `${f}: fewer than 5 links`); }
    if (mine.length < 30) continue;
    n++;
    assert.ok(!/\bR[23]\d{6}\b/.test(mine), `${f}: MLS number published`);
    assert.ok(!/zolo\.ca|estateblock|realtor\.ca|soldbycraig|zealty|rew\.ca\/properties|plsrealestate/i.test(mine), `${f}: listing-level link`);
    assert.ok(!/\*\*|`|§|FILE STATUS|\bsiblings?\b|~\/|\bSection [1-5]\b(?![\d.]\d)|\d+ (attached|detached|active) listings|\b\d+ (listings|sales)\b/.test(mine.replace(/"h":"[^"]*"/g, '')), `${f}: note reference or board count`);
  }
  assert.ok(n >= 150, 'expected the type-note sections');
  assert.ok(hubs >= 30, "3 rules pages and the new community guides");
});

test('no research-team chatter or the wrong contact email reaches published text', () => {
  for (const [f, t] of texts) {
    const d = JSON.parse(t);
    const mine = JSON.stringify([(d.blocks || []).filter((b) => ['tn', 'n55', 'n55mh', 'n55fold'].includes(b.gen)), (d.faq || []).filter((x) => ['tn', 'n55', 'n55mh', 'n55fold'].includes(x.gen))]);
    assert.ok(!/Jerry|sweep item|jared@jaredgibbons|\bfooter\b|\bbyline\b|Contact check|Filing position|conforming pass|home file|this file/i.test(mine), `${f}: research chatter in published text`);
  }
});

test('city-wide 55+ sections (Surrey, Burnaby, Coquitlam): ownership table or a stated none, no note markup, URLs only as links, 8+ FAQ', () => {
  const bad = /roster|re-consolidation|consolidat|\bqueue\b|this series|calibration|sibling|\bbatch\b|Section \d|~\/|FILE DEFECT|\*\*|workspace/i;
  for (const s of ['surrey', 'burnaby', 'coquitlam']) {
    const j = JSON.parse(fs.readFileSync(path.join(LOCAL, `${s}-55-plus-homes-for-sale.json`), 'utf8'));
    const mine = j.blocks.filter(b => b.gen === 'n55city');
    assert.ok(mine.length >= 8, `${s}: city section missing`);
    const txt = JSON.stringify(mine.concat(j.faq.filter(f => f.gen === 'n55city'))).replace(/"h":"[^"]*"/g, '');
    assert.ok(!bad.test(txt), `${s}: note text leaked: ${(txt.match(bad) || [])[0]}`);
    assert.ok(!/https?:\/\//.test(txt), `${s}: raw URL in text`);
    assert.ok(!/R[23]\d{6}/.test(txt), `${s}: MLS number`);
    assert.ok(j.faq.length >= 8, `${s}: only ${j.faq.length} FAQ`);
    if (s === 'burnaby') assert.ok(/no[tn]? .*(age-restricted|55\+ strata)|Not in an age-restricted/i.test(txt), 'burnaby must say plainly that nothing 55+ is for sale');
    else assert.ok(mine.some(b => b.t === 'table' && b.head.includes('Evidence') && b.rows.length >= 4), `${s}: ownership table too short`);
  }
});

test('MLS 55+ flag sections (n55mls): names, type and title only; no numbers from the export; hub explains the flag', () => {
  let pages = 0, rows = 0;
  for (const [f, t] of texts) {
    if (!t.includes('"n55mls"')) continue;
    const d = JSON.parse(t);
    const mine = (d.blocks || []).filter((b) => b.gen === 'n55mls');
    const tbls = mine.filter((b) => b.t === 'table');
    if (tbls.length) pages++;
    for (const b of tbls) { assert.deepEqual(b.head, ['Building', 'Type', 'Title', 'Built', 'Storeys', 'Building amenities'], `${f}: table columns`); rows += b.rows.length; for (const r of b.rows) { assert.ok(/^(—|(19|20)\d\d)$/.test(r[3]) && /^(—|\d{1,2})$/.test(r[4]), `${f}: built or storeys ${r.join('|')}`); assert.ok(!/\d|\$/.test(r[5]), `${f}: number in amenities`); } }
    assert.ok(!/R[23]\d{6}|\$\d/.test(JSON.stringify(mine)), `${f}: MLS number or price`);
  }
  assert.ok(pages >= 20 && rows >= 100, `expected the flag tables on 20+ pages, got ${pages} / ${rows} rows`);
  const hub = JSON.parse(fs.readFileSync(path.join(LOCAL, 'bc-55-plus-strata-rules.json'), 'utf8'));
  assert.ok(hub.blocks.some((b) => b.id === 'mls-flag'), 'hub explainer missing');
});

test('acreage sections (acre): rural areas only, no note markup, no board counts, no listing-feed text; rules page explains the ALR, farm class and GST', () => {
  let pages = 0;
  const bad = /FILE STATUS|UNVERIFIED|UNCONFIRMED|\bsiblings?\b|\bslug\b|\bfeed\b|SnapStats|~\/|(?:see|in|\(|read) Section [1-5]\b|\bthe research\b|lots-and-land|\b\d+ \/ \d+ \/ (?:\d+%|NA)|R[23]\d{6}|https?:\/\//;
  for (const [f, t] of texts) {
    if (!t.includes('"acre"')) continue;
    const d = JSON.parse(t);
    const mine = (d.blocks || []).filter((b) => b.gen === 'acre').concat((d.faq || []).filter((q) => q.gen === 'acre'));
    if (f === 'bc-acreage-buying-rules.json') continue;
    const txt = JSON.stringify(mine).replace(/"h":"[^"]*"/g, '');
    assert.ok(!bad.test(txt), `${f}: acreage text leaked: ${(txt.match(bad) || [])[0]}`);
    assert.ok(mine.some((b) => b.t === 'list' && b.items.some((i) => i[0].h === '/bc-acreage-buying-rules.html')), `${f}: no link to the rules page`);
    pages++;
  }
  assert.ok(pages >= 60, `expected acreage sections on 60+ pages, got ${pages}`);
  const hub = JSON.parse(fs.readFileSync(path.join(LOCAL, 'bc-acreage-buying-rules.json'), 'utf8'));
  const h = JSON.stringify(hub);
  for (const w of ['Agricultural Land Reserve', '500 m²', '90 m²', '186 m²', '$10,000', 'October 31', 'GI-003']) assert.ok(h.includes(w), `rules page missing ${w}`);
  assert.ok(hub.faq.length >= 5 && hub.new_page && hub.new_page.title.length <= 66, 'rules page FAQ or title');
  assert.ok(!bad.test(h.replace(/"slug"/g, '"s"').replace(/https?:\/\/[^"]*/g, '')), 'rules page has note markup');
});

test('mobile-home sections (mh): no note markup or research wording, no pad-rent dollar figures, link to the rules page; rules page covers chattel, MHPTA assignment, pad-rent cap and s.42 closures', () => {
  let pages = 0;
  const bad = /FILE STATUS|UNVERIFIED|UNCONFIRMED|\bsiblings?\b|\bslug\b|\bfeed\b|SnapStats|~\/|(?:see|in|\(|read) Section [1-5]\b|\bthe research\b|commissioning|standing correction|R[23]\d{6}|\$\d[\d,]*\s*(?:\/|per) ?month|https?:\/\//;
  for (const [f, t] of texts) {
    if (!t.includes('"mh"')) continue;
    const d = JSON.parse(t);
    const mine = (d.blocks || []).filter((b) => b.gen === 'mh').concat((d.faq || []).filter((q) => q.gen === 'mh'));
    if (f === 'bc-mobile-home-buying-rules.json') continue;
    const txt = JSON.stringify(mine).replace(/"h":"[^"]*"/g, '');
    assert.ok(!bad.test(txt), `${f}: mobile-home text leaked: ${(txt.match(bad) || [])[0]}`);
    assert.ok(mine.some((b) => b.t === 'list' && b.items.some((i) => i[0].h === '/bc-mobile-home-buying-rules.html')), `${f}: no link to the rules page`);
    pages++;
  }
  assert.ok(pages >= 35, `expected mobile-home sections on 35+ pages, got ${pages}`);
  const hub = JSON.parse(fs.readFileSync(path.join(LOCAL, 'bc-mobile-home-buying-rules.json'), 'utf8'));
  const h = JSON.stringify(hub);
  for (const w of ['chattel', 'Manufactured Home Park Tenancy Act', '2.3%', '$20,000', 'Residential Tenancy Branch']) assert.ok(h.includes(w), `mobile-home rules page missing ${w}`);
  assert.ok(hub.faq.length >= 5 && hub.new_page && hub.new_page.title.length <= 66, 'rules page FAQ or title');
});

test('duplex sections (dx): no note markup or research wording, no listing counts, link to the rules page; rules page covers the two legal forms, the 5-lot depreciation threshold, the 55+ age bylaw and property transfer tax', () => {
  let pages = 0;
  const bad = /FILE STATUS|UNVERIFIED|UNCONFIRMED|\bsiblings?\b|\bslug\b|\bfeed\b|SnapStats|~\/|(?:see|in|\(|read) Section [1-5]\b|\bthe research\b|\bresearched\b|search miss|\bNEVER\b|\bVERIFIED\b|R[23]\d{6}|https?:\/\//;
  for (const [f, t] of texts) {
    if (!t.includes('"dx"')) continue;
    const d = JSON.parse(t);
    const mine = (d.blocks || []).filter((b) => b.gen === 'dx').concat((d.faq || []).filter((q) => q.gen === 'dx'));
    if (f === 'bc-duplex-half-duplex-buying-rules.json') continue;
    const txt = JSON.stringify(mine).replace(/"h":"[^"]*"/g, '');
    assert.ok(!bad.test(txt), `${f}: duplex text leaked: ${(txt.match(bad) || [])[0]}`);
    if (f === 'bc-55-plus-strata-rules.json' || f === 'townhomes-for-sale.json') continue;
    assert.ok(mine.some((b) => b.t === 'list' && b.items.some((i) => i[0].h === '/bc-duplex-half-duplex-buying-rules.html')), `${f}: no link to the rules page`);
    pages++;
  }
  assert.ok(pages >= 100, `expected duplex sections on 100+ pages, got ${pages}`);
  const hub = JSON.parse(fs.readFileSync(path.join(LOCAL, 'bc-duplex-half-duplex-buying-rules.json'), 'utf8'));
  const h = JSON.stringify(hub);
  for (const w of ['fee-simple half duplex', 'five or more lots', '55+ age bylaw', '$800,000 is $14,000', 'Approving Officer']) assert.ok(h.includes(w), `duplex rules page missing ${w}`);
  assert.ok(hub.faq.length >= 5 && hub.new_page && hub.new_page.title.length <= 66, 'duplex rules page FAQ or title');
});

test("building-by-building nearby sections (nbb): no URLs, note markup or research wording; a 5-column table with plausible speeds; walks up to 1.5 km, drives up to 10 km", () => {
  let pages = 0, rows = 0;
  const bad = /FILE STATUS|UNVERIFIED|UNCONFIRMED|\bsiblings?\b|\bslug\b|SnapStats|~\/|in this (?:pass|note)|rate limit|Nominatim|geocod|ADDRESS NOT|ADDRESS CONFLICT|R[23]\d{6}|https?:\/\//;
  for (const [f, t] of texts) {
    if (!t.includes('"nbb"')) continue;
    const d = JSON.parse(t);
    const mine = (d.blocks || []).filter((b) => b.gen === 'nbb');
    const txt = JSON.stringify(mine).replace(/"h":"[^"]*"/g, '');
    assert.ok(!bad.test(txt), `${f}: building nearby text leaked: ${(txt.match(bad) || [])[0]}`);
    for (const b of mine.filter((x) => x.t === 'table')) {
      assert.deepEqual(b.head, ['Building', 'To', 'How', 'Minutes', 'Distance (km)'], `${f}: table columns`);
      for (const r of b.rows) {
        const m = +r[3], km = +r[4]; rows++;
        assert.ok(m >= 1 && m <= 90 && km > 0, `${f}: ${r.join('|')}`);
        const sp = km / (m / 60);
        assert.ok(r[2] === 'Walk' ? km <= 1.6 && sp >= 3 && sp <= 7 : km <= 10.1 && sp >= 4 && sp <= 95, `${f}: speed ${r.join('|')}`);
      }
    }
    pages++;
  }
  assert.ok(pages >= 150 && rows >= 1800, `expected 150+ pages and 1800+ rows, got ${pages} / ${rows}`);
});

test("what's nearby blocks (nb): no URLs, note markup or research wording in text; times only in a four-column table with a start point; plausible speeds", () => {
  let pages = 0, rows = 0;
  const bad = /FILE STATUS|UNVERIFIED|UNCONFIRMED|\bsiblings?\b|\bslug\b|SnapStats|~\/|in this (?:pass|note)|rate limit|Nominatim|geocod|R[23]\d{6}|https?:\/\//;
  for (const [f, t] of texts) {
    if (!t.includes('"nb"')) continue;
    const d = JSON.parse(t);
    const mine = (d.blocks || []).filter((b) => b.gen === 'nb');
    const txt = JSON.stringify(mine).replace(/"h":"[^"]*"/g, '');
    assert.ok(!bad.test(txt), `${f}: nearby text leaked: ${(txt.match(bad) || [])[0]}`);
    for (const b of mine.filter((x) => x.t === 'table')) {
      assert.deepEqual(b.head, ['To', 'How', 'Minutes', 'Distance (km)'], `${f}: table columns`);
      assert.ok(/ from .{3,}/.test(b.caption) && b.rows.length >= 2, `${f}: table needs a start point and 2+ rows`);
      for (const r of b.rows) {
        const m = +r[2], km = +r[3]; rows++;
        assert.ok(m >= 1 && m <= 90 && km > 0, `${f}: ${r.join('|')}`);
        const sp = km / (m / 60);
        assert.ok(r[1] === 'Walk' ? km <= 1.6 && sp >= 3 && sp <= 7 : km <= 10.1 && sp >= 4 && sp <= 95, `${f}: speed ${r.join('|')}`);
      }
    }
    pages++;
  }
  assert.ok(pages >= 200 && rows >= 500, `expected nearby blocks on 200+ pages, got ${pages} / ${rows} rows`);
});

test('no research-process wording on any page: no UNCONFIRMED / UNVERIFIED tags, sibling files, batch numbers, "in this research", locator results or "Jared\'s reports" in any block or FAQ', () => {
  const bad = /UNCONFIRMED|UNVERIFIED|\bsiblings?\b|\bbatch[- ]?\d|\bslug\b|research file|Jared.s reports|\bthe notes\b|\bthis research\b|\blocator (?:returned|result)|\bpage text read|reading was/i;
  const walk = (o, hits, f) => {
    if (typeof o === 'string') { const m = o.match(bad); if (m && !(/^(unconfirmed|unverified)$/i.test(m[0]) && !/UN(?:CONFIRMED|VERIFIED)/.test(o))) hits.push(`${f}: ${o.slice(Math.max(0, m.index - 30), m.index + 60)}`); }
    else if (Array.isArray(o)) o.forEach((x) => walk(x, hits, f));
    else if (o && typeof o === 'object') for (const [k, v] of Object.entries(o)) if (!['h', 'slug', 'gen', 'needs_from_muse'].includes(k)) walk(v, hits, f);
  };
  const hits = [];
  for (const [f, t] of texts) { const d = JSON.parse(t); walk(d.blocks || [], hits, f); walk(d.faq || [], hits, f); }
  assert.deepEqual(hits.slice(0, 5), [], `${hits.length} strings with research wording`);
});

test("uniqueness sections (uq): no URLs outside links, no research wording, no slug-style cross-references; the wrong-place note (lower-landing) is not published; Holly and Hawthorne notes name Ladner or Delta and never Langley", () => {
  let pages = 0, faqs = 0;
  const bad = /UNVERIFIED|UNCONFIRMED|\bunconfirmed\b|\bsiblings?\b|\bslug\b|\bbrief\b|this pass|Read: 20\d\d|~\/|Jared to confirm|https?:\/\//;
  for (const [f, t] of texts) {
    if (!t.includes('"uq"')) continue;
    const d = JSON.parse(t);
    assert.ok(!['lower-landing.json'].includes(f.split('/').pop()), `${f}: wrong-place note published`);
    const mine = (d.blocks || []).filter((b) => b.gen === 'uq');
    if (/(^|\/)(holly|hawthorne-guide)\.json$/.test(f)) assert.ok(/Ladner|Delta/.test(JSON.stringify(mine)) && !/Langley/.test(JSON.stringify(mine)), `${f}: wrong place`);
    const txt = JSON.stringify(mine).replace(/"h":"[^"]*"/g, '');
    assert.ok(!bad.test(txt), `${f}: uq text leaked: ${(txt.match(bad) || [])[0]}`);
    for (const q of (d.faq || []).filter((x) => x.gen === 'uq')) { faqs++; assert.ok(!bad.test(q.q + ' ' + q.a), `${f}: uq FAQ leaked`); }
    pages++;
  }
  assert.ok(pages >= 450 && faqs >= 1200, `expected 450+ pages and 1200+ FAQ entries, got ${pages} / ${faqs}`);
});
