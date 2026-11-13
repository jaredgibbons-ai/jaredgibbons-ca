// Checks the built pages in dist/ (run after `npm run build`): every internal link lands on a page, one H1 per page, heading levels in order,
// a title and a meta description, image alt text and dimensions. Skipped when dist/ is not built.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const DIST = path.join(path.dirname(new URL(import.meta.url).pathname), '..', 'dist');
const built = fs.existsSync(path.join(DIST, 'index.html'));
const WORKER_SERVED = /^\/(?:listing-photos\/|blog\.html\/|our-listings\.html\/|recip\.html\/|mylistings\.html\/|fort-langley\.html\/listing\.|[a-z0-9-]+\.html\/listing\.)/;
const pages = built ? fs.readdirSync(DIST).filter((f) => f.endsWith('.html') && f !== '404.html') : [];
const html = (f) => fs.readFileSync(path.join(DIST, f), 'utf8');
const exists = (p) => { const q = decodeURI(p).replace(/^\//, ''); return !q || fs.existsSync(path.join(DIST, q)) || fs.existsSync(path.join(DIST, q + '.html')); };

test('built pages: every internal link lands on a page the site serves', { skip: !built }, () => {
  const bad = [];
  for (const f of pages) for (const m of html(f).matchAll(/<a\b[^>]*\shref="(\/[^"#?]*)/g)) if (!m[1].startsWith('//') && !WORKER_SERVED.test(m[1]) && !exists(m[1])) bad.push(`${f} -> ${m[1]}`);
  assert.equal(bad.length, 0, `broken internal links: ${bad.slice(0, 8).join('; ')}`);
});

test('built pages: one H1, heading levels in order, title and meta description present', { skip: !built }, () => {
  const bad = [];
  for (const f of pages) {
    const t = html(f); const main = t.slice(t.indexOf('<main'), t.indexOf('</main>') + 1);
    if ((main.match(/<h1\b/g) || []).length !== 1) bad.push(`${f}: h1 count`);
    let prev = 0; for (const m of main.matchAll(/<h([1-6])\b/g)) { const l = +m[1]; if (prev && l > prev + 1) { bad.push(`${f}: h${prev} to h${l}`); break; } prev = l; }
    if (!/<title>[^<]{5,}<\/title>/.test(t)) bad.push(`${f}: title`);
    if (!/<meta name="description" content="[^"]{40,}"/.test(t)) bad.push(`${f}: meta`);
  }
  assert.equal(bad.length, 0, bad.slice(0, 8).join('; '));
});

test('built pages: every image has alt text and dimensions (listing photos excepted)', { skip: !built }, () => {
  const bad = [];
  for (const f of pages) for (const m of html(f).matchAll(/<img\b([^>]*)>/g)) { const a = m[1]; if (!/\balt=/.test(a) || (!/\bwidth=/.test(a) && !/listing-photos/.test(a))) bad.push(`${f}: ${a.slice(0, 60)}`); }
  assert.equal(bad.length, 0, bad.slice(0, 5).join('; '));
});

test('built pages: each listing search block names a numeric search id, loads from the vendor host only, and reserves its height', { skip: !built }, () => {
  const bad = [];
  const data = JSON.parse(fs.readFileSync(path.join(DIST, '..', 'src/data/idx-embeds.json'), 'utf8')); const ids = data.pages; const special = data.special || {};
  for (const f of pages) {
    const t = html(f); const m = t.match(/data-idx-src="([^"]*)"/);
    if (!m) continue;
    const slug = f.replace(/\.html$/, '');
    // The two open-map pages show a saved search as photo cards on phones (D-255); that block names the South Surrey search.
    if (/class="idxphone"/.test(t)) { if (!m[1].endsWith(`/-/search-${ids['south-surrey-homes-for-sale']}.def/in.js`)) bad.push(`${f}: wrong phone search`); }
    else if (special[slug]) { if (m[1] !== `https://idx.myrealpage.com/wps/rest/${data.account}/l/idx2/${special[slug]}`) bad.push(`${f}: wrong special src`); }
    else if (!/^https:\/\/idx\.myrealpage\.com\/wps\/rest\/\d+\/l\/idx2\/recip\/[^"]*\/-\/search-\d+\.def\/in\.js$/.test(m[1])) bad.push(`${f}: src ${m[1]}`);
    if (ids[f.replace(/\.html$/, '')] && !m[1].includes(`search-${ids[f.replace(/\.html$/, '')]}.def`)) bad.push(`${f}: wrong id`);
    if (/<script[^>]+src="https:\/\/idx\.myrealpage/.test(t)) bad.push(`${f}: vendor script is not lazy`);
  }
  assert.equal(bad.length, 0, bad.slice(0, 5).join('; '));
});

// Every page that runs a saved listing search carries exactly one "Email me new listings" box above the results, with a consent box that starts unticked,
// a labelled email field, the sender details and an unsubscribe statement. The three widget pages (open map search, my listings, sold) do not.
test('built pages: each saved-search page has one correct "Email me new listings" box', { skip: !built }, () => {
  const bad = []; let n = 0;
  for (const f of pages) {
    const t = html(f); const hasIdx = /class="idx"[^>]*data-idx-id="/.test(t) && !/class="idxphone"/.test(t); const forms = t.match(/<form class="la"/g) || [];
    if (!hasIdx) { if (forms.length && !(forms.length === 1 && /data-search="[^"]+ guide"/.test(t))) bad.push(`${f}: box on a non-search page`); continue; }   // a guide with no search carries one area alert (D-220)
    n++;
    if (forms.length !== 1) { bad.push(`${f}: ${forms.length} boxes`); continue; }
    const box = t.slice(t.indexOf('<form class="la"'), t.indexOf('</form>', t.indexOf('<form class="la"')));
    if (!/data-search="[^"]{5,}"/.test(box) || !/data-search-id="\d+"/.test(box)) bad.push(`${f}: search name or id`);
    if (!/<label[^>]*for="la-email"/.test(box) || !/<label[^>]*for="la-consent"/.test(box)) bad.push(`${f}: labels`);
    if (/name="consent"[^>]*checked/.test(box)) bad.push(`${f}: consent pre-ticked`);
    if (!/Royal LePage Little Oak Realty/.test(box) || !/unsubscribe/i.test(box) || !/\/privacy\.html/.test(box)) bad.push(`${f}: sender or unsubscribe wording`);
    if (t.indexOf('<form class="la"') > t.indexOf('class="idx"')) bad.push(`${f}: box is below the results`);
  }
  assert.ok(n > 1000 || n === 0, `only ${n} search pages found`);
  assert.equal(bad.length, 0, bad.slice(0, 8).join('; '));
});

test('built pages: guides open with quick facts, reference sections fold, the alert box is a one-line bar (D-197)', { skip: !built }, () => {
  const bad = []; let guides = 0;
  for (const f of pages) {
    const t = html(f);
    if (f.endsWith('-guide.html')) { guides++; if (!/class="qf"/.test(t) && /<h2[^>]*>Homes for sale in /.test(t)) bad.push(`${f}: no quick facts`); }
    if (/<h2[^>]*class="h2[^"]*"[^>]*>Sources\b[^<]*<\/h2>/.test(t) && !/<summary class="fold__s"[^>]*><h2[^>]*>Sources\b/.test(t)) bad.push(`${f}: sources not folded`);
    if (/<form class="la"/.test(t) && !/<details class="la-d"/.test(t)) bad.push(`${f}: alert box not collapsible`);
  }
  assert.ok(guides > 100 || guides === 0, `only ${guides} guides`);
  assert.equal(bad.length, 0, bad.slice(0, 8).join('; '));
});

test('built pages: every guide with Jared’s notes shows one "Jared’s take" card under the quick facts (D-198)', { skip: !built }, () => {
  const jv = JSON.parse(fs.readFileSync('src/data/jared-voice.json', 'utf8'));
  const bad = [];
  for (const [slug, v] of Object.entries(jv)) {
    const f = pages.find((p) => p.endsWith(`/${slug}.html`) || p === `${slug}.html`);
    if (!f) { bad.push(`${slug}: page not built`); continue; }
    const t = html(f);
    if ((t.match(/id="jareds-take"/g) || []).length !== 1) bad.push(`${slug}: card count`);
    if ((t.match(/Jared’s take on /g) || []).length !== 1 || /Jared's take on /.test(t)) bad.push(`${slug}: more than one "Jared's take" heading`);
    const qf = t.indexOf('class="qf"'), card = t.indexOf('id="jareds-take"');
    if (qf > -1 && card < qf) bad.push(`${slug}: card above quick facts`);
    if (!v.suits || !v.friend) bad.push(`${slug}: missing text`);
  }
  assert.ok(Object.keys(jv).length > 100, 'jared-voice.json looks empty');
  assert.equal(bad.length, 0, bad.slice(0, 8).join('; '));
});

test('robots.txt opens on the same launch switch as the pages (D-200)', () => {
  const t = fs.readFileSync('src/pages/robots.txt.ts', 'utf8');
  assert.match(t, /import \{ isPreview \} from '\.\.\/lib\/preview'/);
  assert.doesNotMatch(t, /import.meta.env.PUBLIC_LAUNCH/);
});

test('built pages: links to other agents\' and brokerages\' sites carry rel="nofollow" (D-200)', { skip: !built }, () => {
  const bad = [];
  for (const f of pages) {
    for (const m of html(f).matchAll(/<a\b[^>]*href="https?:\/\/(?:www\.)?(?:bccondosandhomes\.com|mikestewart\.ca|danmarusin\.com|bentruscottrealestate\.com)[^"]*"[^>]*>/g))
      if (!/\brel="[^"]*\bnofollow\b/.test(m[0])) bad.push(`${f}: ${m[0].slice(0, 90)}`);
  }
  assert.equal(bad.length, 0, bad.slice(0, 5).join('; '));
});

test('built pages: no link points at another agent\'s, brokerage\'s or listing portal\'s page (D-204, D-209)', { skip: !built }, () => {
  const bad = [];
  const doms = JSON.parse(fs.readFileSync(new URL('../src/data/other-agent-domains.json', import.meta.url), 'utf8')).domains;   // D-209: the whole list
  const rx = new RegExp(`<a\\b[^>]*href="https?:\\/\\/(?:[a-z0-9-]+\\.)*(?:${doms.map((d) => d.replace(/[.]/g, '\\.')).join('|')})[/"?#]`, 'gi');
  for (const f of pages) for (const m of html(f).matchAll(rx)) bad.push(`${f}: ${m[0].slice(0, 90)}`);
  assert.equal(bad.length, 0, bad.slice(0, 5).join('; '));
});

test('built pages: sold cards carry no price, and guides list the homes Jared sold there (D-211)', { skip: !built }, () => {
  for (const f of ['willoughby-guide.html', 'sold-properties.html', 'murrayville-guide.html']) {
    for (const card of html(f).split('<li class="pcard"').slice(1).map((c) => c.split('</li>')[0]))
      if (/pcard__tag[^>]*>\s*Sold\s*</.test(card)) assert.ok(!card.includes('pcard__price'), `${f}: a sold card shows a price`);
  }
  assert.ok(html('willoughby-guide.html').includes('Homes Jared has sold in'), 'Willoughby guide lists Jared’s sales');
});

test('built pages: guide format v2 renders on Murrayville (D-205)', { skip: !built }, () => {
  const h = html('murrayville-guide.html');
  for (const s of ['class="qa"', 'Jared’s verdict:', 'class="pc"', 'right for you?', 'https://calendly.com/jaredgibbons', 'Drive, off-peak', 'Is Murrayville a good place to live?'])
    assert.ok(h.includes(s), `missing ${s}`);
  assert.ok(h.indexOf('class="qa"') < h.indexOf('class="qf"'), 'quick answer comes before quick facts');
});
