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

// D-255: on phones the two map pages offer a quick search (area + home type) and open the map full screen on the page itself.
test('built pages: the map pages offer a quick search whose every choice is a real page, and a full-screen map (D-255)', { skip: !built }, () => {
  for (const f of ['recip.html', 'map-search.html']) {
    const t = html(f);
    const m = t.match(/<form class="qs"[^>]*data-qs="([^"]*)"/);
    assert.ok(m, `${f}: quick search missing`);
    const data = JSON.parse(m[1].replace(/&quot;/g, '"').replace(/&#34;/g, '"').replace(/&amp;/g, '&'));
    const areas = Object.keys(data);
    assert.ok(areas.length >= 15, `${f}: only ${areas.length} areas`);
    for (const a of areas) {
      assert.equal(data[a][0][0], 'All homes', `${f}: ${a} does not start with All homes`);
      for (const [, href] of data[a]) assert.ok(/^\/[a-z0-9-]+\.html$/.test(href) && fs.existsSync(path.join(DIST, href.slice(1))), `${f}: ${a} -> ${href} is not a built page`);
    }
    assert.ok(/<a class="btn btn--ghost"[^>]*href="https:\/\/idx\.myrealpage\.com\/[^"]*idx\.search"[^>]*data-map-open/.test(t), `${f}: map button missing or not a plain link`);
    assert.ok(/<div class="mapfs" id="mapfs" role="dialog" aria-modal="true"[^>]*data-src="https:\/\/idx\.myrealpage\.com\/[^"]*"[^>]*hidden/.test(t), `${f}: full-screen map container missing`);
    assert.ok(!/<iframe[^>]*class="idxmap"[^>]*\ssrc=/.test(t), `${f}: the desktop map frame must not load until the screen is wide enough`);
  }
});

// D-256: the selling page is the marketing plan; the old address forwards and nothing links to it.
test('built pages: Marketing Plan opens the selling page, and Home Evaluation carries the big link to it (D-256)', { skip: !built }, () => {
  assert.ok(!fs.existsSync(path.join(DIST, 'marketing-plan.html')), 'marketing-plan.html is still built');
  const home = html('index.html');
  assert.ok(/<a href="\/selling\.html"[^>]*>Marketing Plan<\/a>/.test(home), 'menu: Marketing Plan does not open /selling.html');
  assert.ok(!/Selling Resources/.test(home), 'menu still says Selling Resources');
  for (const f of pages) assert.ok(!html(f).includes('/marketing-plan.html'), `${f} still links to /marketing-plan.html`);
  assert.ok(!fs.readFileSync(path.join(DIST, 'sitemap.xml'), 'utf8').includes('marketing-plan'), 'sitemap lists the retired page');
  const he = html('home-evaluation.html');
  assert.ok(/<a class="biglink" href="\/selling\.html"/.test(he) && he.indexOf('class="biglink"') < he.indexOf('<form'), 'home evaluation: big marketing-plan link missing or below the form');
  const sell = html('selling.html');
  for (const w of ['Classifieds', 'Local news', 'REALTOR.ca', 'How long until my home is on the market?', 'Where will my home be advertised?', 'about 5 days after you sign']) assert.ok(sell.includes(w), `selling page lost "${w}" from the old marketing plan`);
});

// D-257 / D-258: the monthly market update is a real page with tables, and the blog index is an index (not 50 stacked posts).
test('built pages: blog index features the newest market update, shows dated cards and lists every post once by year (D-258)', { skip: !built }, () => {
  const t = html('blog.html');
  const posts = fs.readdirSync(path.join(DIST, 'internal', 'blog')).filter((f) => f.endsWith('.html')).map((f) => '/blog.html/' + f.replace(/\.html$/, ''));
  const feature = t.match(/<div class="mkf[^"]*"[\s\S]*?<h2 class="mkf__h"[^>]*><a href="([^"]+)"/);
  assert.ok(feature && /^\/[a-z]+-20\d\d-market-update-[a-z-]+\.html$/.test(feature[1]) && fs.existsSync(path.join(DIST, feature[1].slice(1))), 'no market update featured, or it is not a built page');
  const locals = fs.readdirSync('src/data/local').filter((f) => /-market-update-/.test(f)).map((f) => JSON.parse(fs.readFileSync(`src/data/local/${f}`, 'utf8'))).filter((l) => l.market_update);
  const newest = locals.sort((a, b) => String(b.market_update).localeCompare(String(a.market_update)))[0];
  assert.equal(feature[1], `/${newest.slug}.html`, 'the featured market update is not the newest one');
  const cards = [...t.matchAll(/<li class="post"[^>]*>([\s\S]*?)<\/li>/g)].map((m) => m[1]);
  assert.equal(cards.length, 24, `${cards.length} cards`);
  for (const c of cards) assert.ok(/<time datetime="20\d\d-\d\d-\d\d"/.test(c) && /<h3 class="post__t"[^>]*><a href="\/blog\.html\/[^"]+"/.test(c), 'a card has no date or no link');
  const listed = [...t.matchAll(/<ul class="py__list"[^>]*>([\s\S]*?)<\/ul>/g)].flatMap((m) => [...m[1].matchAll(/href="(\/blog\.html\/[^"]+)"/g)].map((x) => x[1]));
  assert.equal(listed.length, posts.length, `${listed.length} posts listed by year, ${posts.length} built`);
  assert.deepEqual([...new Set(listed)].sort(), posts.sort(), 'the by-year list and the built posts differ');
  assert.ok(!/\?blog=\d+/.test(t), 'old category filters (they changed nothing) are back');
  assert.ok(!/Read the full post/.test(t), 'the stacked-post layout is back');
});

test('built pages: the October 2026 market update has its tables, sources and questions, and no share image points at the old host (D-257, D-258)', { skip: !built }, () => {
  const f = 'october-2026-market-update-south-surrey-white-rock-langley.html';
  const t = html(f);
  assert.equal((t.match(/<table class="tbl"/g) || []).length, 5, 'tables');
  for (const w of ['1,051', '9,164', '$860,000', '$1,606,500', '29.2%', 'fvreb.bc.ca/statistics/Package202610.pdf', 'bankofcanada.ca/2026/10/fad-press-release-2026-10-28/', '"@type":"FAQPage"']) assert.ok(t.includes(w), `missing ${w}`);
  assert.ok(fs.readFileSync(path.join(DIST, 'sitemap.xml'), 'utf8').includes(`/${f}<`), 'not in the sitemap');
  const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) => (e.isDirectory() ? walk(path.join(d, e.name)) : e.name.endsWith('.html') ? [path.join(d, e.name)] : []));
  const bad = walk(DIST).filter((p) => /property="og:image" content="[^"]*\/(?:wps\/rest|_media)\//.test(fs.readFileSync(p, 'utf8')));
  assert.equal(bad.length, 0, `share image on the old host: ${bad.slice(0, 3).join(', ')}`);
});

test('blog post photos: each has its files and alt text; posts show the photo, their own share card and BlogPosting markup; index cards carry it (D-259)', { skip: !built }, () => {
  const IMG = JSON.parse(fs.readFileSync('src/data/post-images.json', 'utf8'));
  const posts = fs.readdirSync('src/data/posts').map((f) => f.replace(/\.json$/, ''));
  const unesc = (s) => s.replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n)).replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
  const attr = (tag, name) => { const m = tag.match(new RegExp(`\\s${name}="([^"]*)"`)); return m ? unesc(m[1]) : null; };
  const SITE = 'https://jaredgibbons.ca';
  assert.ok(Object.keys(IMG).length >= 198, 'post photos went missing from src/data/post-images.json');
  const bad = [];
  for (const slug of posts) {
    const r = IMG[slug];
    const t = fs.readFileSync(path.join(DIST, 'internal/blog', slug + '.html'), 'utf8');
    const head = t.slice(0, t.indexOf('</head>'));
    const og = (head.match(/<meta property="og:image" content="([^"]*)"/) || [])[1];
    const ld = [...head.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)].map((m) => JSON.parse(m[1])).find((j) => j['@type'] === 'BlogPosting');
    const figs = [...t.matchAll(/<figure class="phero"[^>]*>\s*<img\b([^>]*)>/g)];
    if (!ld || !ld.headline || !ld.datePublished || ld.author?.name !== 'Jared Gibbons' || ld.mainEntityOfPage?.['@id'] !== `${SITE}/blog.html/${slug}`) { bad.push(`${slug}: BlogPosting markup`); continue; }
    if (!head.includes(`<meta property="article:published_time" content="${ld.datePublished}"`) || !head.includes('<meta property="og:type" content="article"')) bad.push(`${slug}: article tags`);
    if (!r) {   // a post with no photo of its own: no picture, the default card, no image line
      if (figs.length || ld.image || og !== `${SITE}/img/og-default.jpg`) bad.push(`${slug}: has no photo record but shows one`);
      continue;
    }
    if (typeof r.alt !== 'string' || r.alt.length < 25 || r.alt.length > 170 || /^(an? )?(image|photo|picture) of\b/i.test(r.alt) || /[.\s]$/.test(r.alt) || /\s{2}/.test(r.alt)) bad.push(`${slug}: alt text "${r.alt}"`);
    if (r.widths[r.widths.length - 1] !== r.w || r.w > 1200 || r.widths.some((w, i) => i && w <= r.widths[i - 1])) bad.push(`${slug}: sizes`);
    for (const w of r.widths) if (!fs.existsSync(path.join(DIST, 'img/blog', `${slug}-${w}.webp`))) bad.push(`${slug}: ${w}.webp is missing`);
    if (!!r.og !== fs.existsSync(path.join(DIST, 'img/blog', `${slug}-og.jpg`))) bad.push(`${slug}: share card file`);
    if (figs.length !== 1) { bad.push(`${slug}: ${figs.length} lead photos`); continue; }
    const img = figs[0][1];
    if (attr(img, 'alt') !== r.alt || attr(img, 'width') !== String(r.w) || attr(img, 'height') !== String(r.h) || attr(img, 'fetchpriority') !== 'high' || /\sloading="lazy"/.test(img)) bad.push(`${slug}: lead photo attributes`);
    if (attr(img, 'srcset') !== r.widths.map((w) => `/img/blog/${slug}-${w}.webp ${w}w`).join(', ')) bad.push(`${slug}: srcset`);
    if (!(t.indexOf('class="byline"') < figs[0].index && figs[0].index < t.indexOf('</figure>'))) bad.push(`${slug}: photo is not under the byline`);
    if (og !== (r.og ? `${SITE}/img/blog/${slug}-og.jpg` : `${SITE}/img/og-default.jpg`)) bad.push(`${slug}: og:image ${og}`);
    if (r.og && (!head.includes(`<meta property="og:image:width" content="${r.og[0]}"`) || !head.includes(`<meta property="og:image:height" content="${r.og[1]}"`) || !/<meta property="og:image:alt" content="[^"]{25,}"/.test(head))) bad.push(`${slug}: share card size or alt`);
    if (JSON.stringify(ld.image) !== JSON.stringify([...(r.og ? [`${SITE}/img/blog/${slug}-og.jpg`] : []), `${SITE}/img/blog/${slug}-${r.w}.webp`])) bad.push(`${slug}: BlogPosting image`);
    if (!/<meta name="robots" content="[^"]*max-image-preview:large/.test(head)) bad.push(`${slug}: robots`);
  }
  for (const slug of Object.keys(IMG)) if (!posts.includes(slug)) bad.push(`${slug}: a photo for a post that does not exist`);
  assert.equal(bad.length, 0, bad.slice(0, 8).join('; '));
  // the index: every card has a picture box; a post with a photo shows it with its alt text, a post without shows the monogram tile
  const cards = [...html('blog.html').matchAll(/<li class="post"[^>]*>([\s\S]*?)<\/li>/g)].map((m) => m[1]);
  for (const c of cards) {
    const slug = c.match(/href="\/blog\.html\/([^"]+)"/)[1]; const r = IMG[slug];
    const box = c.match(/<div class="post__ph([^"]*)"[^>]*>\s*<img\b([^>]*)>/);
    assert.ok(box, `${slug}: card has no picture box`);
    if (!r) { assert.ok(/post__ph--none/.test(box[1]) && attr(box[2], 'alt') === '', `${slug}: no photo, but the card is not the plain tile`); continue; }
    assert.equal(attr(box[2], 'alt'), r.alt, `${slug}: card alt text`);
    assert.ok(attr(box[2], 'srcset').includes(`/img/blog/${slug}-${r.widths[0]}.webp ${r.widths[0]}w`) && attr(box[2], 'loading') === 'lazy' && attr(box[2], 'width') && attr(box[2], 'height'), `${slug}: card photo attributes`);
    assert.equal(/post__ph--whole/.test(box[1]), r.fit === 'contain', `${slug}: card crop`);
  }
});
