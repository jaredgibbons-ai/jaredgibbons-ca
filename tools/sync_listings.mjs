// Daily price sync for Jared's own listing pages (D-298).
// The search pages read MyRealPage live, but the pages under /our-listings.html are files in this repository, so a price change on MLS did not reach them.
// This reads Jared's active listings from his public MyRealPage page and, where an Active listing here shows a different price, writes the new price into
// src/data/listings/<file>.json (the headline price line) and the homepage card in src/data/home.ts. "Original Price" is never touched.
// A listing that left the active list and is in Jared's sold list is marked sold with its sold date (D-299) and comes off the homepage cards.
// A listing that is active on MLS and has no page here gets one, built from its own MyRealPage page (D-302); its photos load from
// MyRealPage's photo server until they are processed like the rest. One that left without selling (expired, cancelled) is reported, not edited.
//   node tools/sync_listings.mjs            fetch, apply, print a report (exit 0)
//   node tools/sync_listings.mjs --dry      fetch and report, write nothing
//   node tools/sync_listings.mjs --file x   read the MyRealPage HTML from a file (tests)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const FEED = 'https://idx.myrealpage.com/wps/-/tmpl~v2,noframe~true/mylistings/67649/mylistings(active).def/SearchResults.form';
const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');

/** MyRealPage results page -> Map(listing id -> { price: '$1,049,000', status: 'ACTIVE', mls: 'R3168794' }). */
export function parseFeed(html) {
  const out = new Map();
  for (const chunk of String(html).split('<li class="mrp-listing-result').slice(1)) {
    const id = (chunk.match(/data-listing-id="(\d+)"/) || chunk.match(/listing-id-(\d+)/) || [])[1];
    const price = (chunk.match(/\$\d{1,3}(?:,\d{3})+/) || [])[0];
    if (!id || !price) continue;
    out.set(id, { price, status: (chunk.match(/status-([A-Z]+)/) || [])[1] || '', mls: (chunk.match(/MLS®#\s*([A-Z]\d+)/) || [])[1] || '', url: (chunk.match(/data-share-url="(https:\/\/idx\.myrealpage\.com\/[^"]+)"/) || [])[1] || '' });
  }
  return out;
}
// Listings on another real estate board, which Jared's MyRealPage feed does not carry. They are kept by hand and never reported as gone or changed.
// 109415142: 116 Calgary Avenue, Penticton (Okanagan board). Jared, Nov 15 2026: for sale, re-listed at $1,279,000.
export const OFF_FEED = new Set(['109415142']);
const num = (p) => Number(String(p).replace(/[^\d]/g, ''));

/** Pure decision: what to change and what to report. listings: [{ file, id, status, price, title }]. */
export function plan(listings, feed) {
  const changes = [], gone = [], odd = [];
  const here = new Set();
  for (const l of listings) {
    here.add(l.id);
    if (l.status !== 'Active' || OFF_FEED.has(l.id)) continue;
    const f = feed.get(l.id);
    if (!f) { gone.push(l); continue; }
    if (num(f.price) === num(l.price)) continue;
    // A change of more than half either way is more likely a parsing mistake than a price change: report it, do not write it.
    const ratio = num(f.price) / (num(l.price) || 1);
    (ratio < 0.5 || ratio > 1.5 ? odd : changes).push({ ...l, to: f.price });
  }
  const fresh = [...feed.entries()].filter(([id]) => !here.has(id)).map(([id, f]) => ({ id, ...f }));
  return { changes, gone, odd, fresh };
}

export const SOLD_FEED = FEED.replace('mylistings(active)', 'mylistings(sold)');

/** A listing's own MyRealPage page -> { status: 'Sold', soldDate: 'Jun 20, 2025' } (either may be ''). */
export function parseDetail(html) {
  const line = (label) => { const m = new RegExp(`<dt>${label}:</dt>\\s*<dd[^>]*>([\\s\\S]*?)</dd>`).exec(String(html)); return m ? m[1].replace(/<[^>]+>/g, '').trim() : ''; };
  return { status: line('Status'), soldDate: line('Sold Date') };
}

/** Which of the listings that left the active list have sold. Reads the sold list (a few pages), then each one's own page for the sold date.
 *  get(url) -> html. Returns { sold: [{ ...listing, soldDate }], gone: [the rest] }. A date that does not read as "Jun 20, 2025" is not trusted. */
export async function findSold(gone, get, maxPages = 8) {
  if (!gone.length) return { sold: [], gone: [] };
  const want = new Set(gone.map((g) => g.id)), found = new Map();
  for (let pg = 1; pg <= maxPages && found.size < want.size; pg++) {
    const feed = parseFeed(await get(`${SOLD_FEED}?_pg=${pg}`));
    if (!feed.size) break;
    for (const [id, f] of feed) if (want.has(id) && f.status === 'SOLD' && f.url) found.set(id, f.url);
  }
  const sold = [], rest = [];
  for (const g of gone) {
    const url = found.get(g.id);
    const d = url ? parseDetail(await get(url)) : null;
    if (d && d.status === 'Sold' && /^[A-Z][a-z]{2} \d{1,2}, 20\d\d$/.test(d.soldDate)) sold.push({ ...g, soldDate: d.soldDate }); else rest.push(g);
  }
  return { sold, gone: rest };
}

/** Marks one listing sold: the status, the Status line, a Sold Date line after the MLS® number, and off the homepage's active cards.
 *  Text replacement (the files are one-line JSON), checked by parsing the result; anything unexpected leaves the files untouched. */
export function applySold(l, root = ROOT) {
  const p = path.join(root, 'src/data/listings', l.file);
  const s = fs.readFileSync(p, 'utf8');
  const sp = /"status": "Active"/.test(s) ? ' ' : '';
  let t = s.replace(`"status":${sp}"Active"`, `"status":${sp}"Sold"`).replace(`{"k":${sp}"Status:",${sp}"v":${sp}["Active"]}`, `{"k":${sp}"Status:",${sp}"v":${sp}["Sold"]}`);
  t = t.replace(/(\{"k": ?"MLS(?:®|\\u00ae) Num:", ?"v": ?\["[^"]+"\]\})/, (m) => `${m},${sp}{"k":${sp}"Sold Date:",${sp}"v":${sp}["${l.soldDate}"]}`);
  let ok = false;
  try {
    const d = JSON.parse(t);
    const facts = (d.blocks || []).filter((b) => b.t === 'facts').flatMap((b) => b.items);
    ok = d.status === 'Sold' && facts.some((f) => f.k === 'Status:' && f.v[0] === 'Sold') && facts.filter((f) => f.k === 'Sold Date:' && f.v[0] === l.soldDate).length === 1;
  } catch { ok = false; }
  if (!ok) return false;
  fs.writeFileSync(p, t);
  const hp = path.join(root, 'src/data/home.ts');
  const short = String(l.slug).replace(/^listing\./, '');
  fs.writeFileSync(hp, fs.readFileSync(hp, 'utf8').split('\n').filter((line) => !line.includes(`slug: '${short}'`)).join('\n'));
  return true;
}

// ---- New listings (D-302): a listing that is active on MLS and has no page here gets one, built from its own MyRealPage page. ----
const ent = (t) => String(t).replace(/&reg;/g, '®').replace(/&amp;/g, '&').replace(/&times;/g, '×').replace(/&nbsp;/g, ' ').replace(/&quot;/g, '"').replace(/&#0?39;|&apos;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
// Visible text of a fragment: metric twins (hidden on MyRealPage) and tags dropped, whitespace collapsed.
const txt = (h) => ent(String(h).replace(/<span class="mrp-m-unit"[\s\S]*?<\/span>/g, '').replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
const cls = (html, c) => { const m = new RegExp(`class="${c}"[^>]*>([\\s\\S]*?)</(?:span|div|h1|h2)>`).exec(html); return m ? txt(m[1]) : ''; };
const pairs = (h) => [...String(h).matchAll(/<dt>([\s\S]*?)<\/dt>\s*<dd[^>]*>([\s\S]*?)<\/dd>/g)].map((m) => ({ k: txt(m[1]), v: [txt(m[2])] })).filter((x) => x.k && x.v[0]);

/** A listing's MyRealPage page -> { page, photos } in this site's own shapes, or { error } when something a page needs is missing.
 *  item: { id, slug ('listing.r…-….<id>'), mls }. tail: the agent and disclaimer blocks of an existing listing file. */
export function buildListing(html, item, tail = []) {
  const h = String(html);
  const t1 = /<h1 class="mrp-listing-title">([\s\S]*?)<\/h1>/.exec(h);
  if (!t1) return { error: 'no title' };
  const street = txt(t1[1].split('<div')[0]);
  const subarea = cls(t1[1], 'subarea'), city = cls(t1[1], 'city'), postal = cls(t1[1], 'postal-code');
  const pi = (/<h2 class="mrp-listing-price-info">([\s\S]*?)<\/h2>/.exec(h) || [])[1] || '';
  const price = (cls(pi, 'price').match(/^\$\d{1,3}(?:,\d{3})+$/) || [])[0];
  const di = h.indexOf('class="mrp-listing-description"');
  const desc = di > 0 ? txt((/class="mrp-listing-description"[^>]*>([\s\S]*?)<\/div>/.exec(h.slice(di - 5)) || [])[1] || '') : '';
  const top = pairs(h.slice(0, di > 0 ? di : 0)).filter((x, i, a) => a.findIndex((y) => y.k === x.k) === i);
  const status = (top.find((x) => x.k === 'Status:') || { v: [''] }).v[0];
  if (!street || !city || !price || !desc || status !== 'Active') return { error: `missing ${[!street && 'street', !city && 'city', !price && 'price', !desc && 'description', status !== 'Active' && 'Active status'].filter(Boolean).join(', ')}` };

  // Photos: the full-size address and caption from the photo tab, the 320-wide address from the thumbnail strip.
  const small = new Map([...h.matchAll(/<img\s+src="(https:\/\/iss-cdn\.myrealpage\.com\/[^"]+)"\s+data-full-src="(https:\/\/iss-cdn\.myrealpage\.com\/[^"]+)"/g)].map((m) => [m[2], m[1]]));
  const pc = h.indexOf('mrp-listing-details-all-photos-container');
  const photos = [];
  if (pc > 0) for (const li of h.slice(pc, h.indexOf('</ul>', pc)).split('<li>').slice(1)) {
    const l = (/data-src="(https:\/\/iss-cdn\.myrealpage\.com\/[^"]+)"/.exec(li) || [])[1];
    if (!l) continue;
    const cap = txt((/class="mrp-listing-full-size-description">([\s\S]*?)<\/div>\s*<\/div>/.exec(li) || [])[1] || '');
    const ph = { p: photos.length + 1, w: 1600, h: 1067, g: 1, u: small.get(l) ? { s: small.get(l), l } : { l } };
    if (cap) ph.cap = cap;
    photos.push(ph);
  }
  if (!photos.length) return { error: 'no photos' };

  const beds = cls(pi, 'beds').replace(/^beds:\s*/, ''), baths = cls(pi, 'baths').replace(/^baths:\s*/, ''), area = cls(pi, 'floor-area'), year = cls(pi, 'year').replace(/^built:\s*/, ''), ptype = cls(pi, 'property-type');
  const lines = [price];
  if (ptype) lines.push(ptype);
  if (beds) lines.push('beds:', beds);
  if (baths) lines.push('baths:', baths);
  if (area) lines.push(area);
  if (year) lines.push('built:', year);
  const h1 = [street, subarea, city, postal].filter(Boolean).join(' ');
  const blocks = [{ t: 'h', level: 1, text: h1 }, { t: 'summary', lines, heading_n: lines.length }, { t: 'facts', items: top }, { t: 'p', parts: [{ t: desc }] }];
  // The fact sections ("General Info:", "Land Info:" …) and the room tables, in the order MyRealPage shows them. Area statistics are left out: they go stale.
  const end = h.indexOf('mrp-listing-attribution-container');
  for (const sec of h.slice(di, end > di ? end : undefined).split(/<div class="(?=mrp-listing-(?:wide-)?info-section|room-info-section|bathroom-info-section)/).slice(1)) {
    const label = txt((/<label class="section-head[^"]*">([\s\S]*?)<\/label>/.exec(sec) || [])[1] || '').replace(/:$/, '');
    if (!label) continue;
    if (/^(bath)?room-info-section/.test(sec)) {
      const dls = [...sec.split(/<div class="mrp-/)[0].matchAll(/<dl[^>]*>([\s\S]*?)<\/dl>/g)].map((m) => m[1]);
      const head = [...(dls[0] || '').matchAll(/<dt>([\s\S]*?)<\/dt>/g)].map((m) => txt(m[1]));
      const rows = dls.slice(1).map((d) => [...d.matchAll(/<dd[^>]*>([\s\S]*?)<\/dd>/g)].map((m) => txt(m[1]))).filter((r) => r.length);
      if (head.length && rows.length) blocks.push({ t: 'table', caption: label, head, rows });
      continue;
    }
    const own = sec.split('</div>')[0];
    // A wide section is one labelled value ("Interior Features: …"): it joins the facts above it, as on the older pages.
    if (sec.startsWith('mrp-listing-wide-info-section')) {
      const v = txt((/<dd[^>]*>([\s\S]*?)<\/dd>/.exec(own) || [])[1] || ''), last = blocks[blocks.length - 1];
      if (v && last.t === 'facts' && !last.items.some((x) => x.k === `${label}:`)) last.items.push({ k: `${label}:`, v: [v] });
      continue;
    }
    const items = pairs(own).filter((x) => x.k !== 'Previous Price:');
    if (items.length) blocks.push({ t: 'h', level: 3, text: label }, { t: 'facts', items });
  }
  const brokerage = txt((/class="mrp-listing-attribution-container"[^>]*>([\s\S]*?)<\/div>/.exec(h) || [])[1] || '').replace(/^Listed by\s*/, '').replace(/ROYAL LEPAGE NORTHSTAR \(W\.R\.\)|Royal LePage Northstar Realty \(S\. Surrey\)/g, 'Royal LePage Little Oak Realty') || 'Royal LePage Little Oak Realty'; // feed still shows the brokerage's old name on some listings
  // The agent block and the board's disclaimer are copied from an existing listing file (tail), not typed here.
  for (const b of tail) if (b.t === 'agent') blocks.push(b);
  blocks.push({ t: 'credit', text: `Listed by ${brokerage}` });
  for (const b of tail) if (b.t === 'disclaimer') blocks.push(b);

  const fact = (k) => (blocks.filter((b) => b.t === 'facts').flatMap((b) => b.items).find((x) => x.k === k) || { v: [''] }).v[0];
  const kind = fact('Dwelling Type:') || ptype || 'Home';
  const where = subarea && subarea !== city ? `${subarea}, ${city}` : city;
  const title = `${street}, ${city} | ${subarea && subarea !== city ? `${subarea} ` : ''}${kind} for Sale`;
  const bb = [beds && `${beds} bed`, baths && `${String(baths).replace(/\.0$/, '')} bath`].filter(Boolean).join(', ');
  // Search description, 160 characters at most: the longest form that fits.
  const lead = `${street}, ${city}: ${bb ? `${bb} ` : ''}${kind.toLowerCase()} for sale in ${where}`, sz = area ? `, ${area.replace(/\.$/, '')}` : '', num = `MLS® ${item.mls || fact('MLS® Num:')}`;
  const meta = [`${lead}${sz}. ${num}. Listed by Jared Gibbons, Royal LePage Little Oak Realty.`, `${lead}${sz}. ${num}. Listed by Jared Gibbons, REALTOR®.`, `${lead}. ${num}. Listed by Jared Gibbons, REALTOR®.`, `${lead}. ${num}.`].find((m) => m.length <= 160) || `${street}, ${city}: ${kind.toLowerCase()} for sale. ${num}.`;
  const url = `https://jaredgibbons.ca/our-listings.html/${item.slug}`;
  const page = {
    slug: item.slug, path: `/our-listings.html/${item.slug}`, url, kind: 'listing', title, canonical: url,
    seo: { Title: title, 'Meta description': meta, H1: h1, Canonical: url, 'Meta robots': 'index, follow', 'OG title': title, 'OG description': meta, 'OG image': '', Published: '', Modified: '' },
    status: 'Active', brokerage, photos: { count: photos.length, alts: photos.map((ph) => `Photo ${ph.p}: ${ph.cap || `${street}, ${city}`}`), captions: photos.map((ph) => ph.cap || '') }, blocks,
  };
  const video = (/youtube\.com\/embed\/([\w-]{11})/.exec(h) || [])[1] || '';
  return { page, photos, card: { street, city, postal, price, beds, baths, area, brokerage }, video };
}

/** Width and height of a JPEG, PNG or WebP from its first bytes, or null. */
export function imageSize(b) {
  if (b.length > 24 && b[0] === 0x89 && b[1] === 0x50) return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
  if (b.length > 30 && b.toString('ascii', 0, 4) === 'RIFF' && b.toString('ascii', 8, 12) === 'WEBP') {
    const k = b.toString('ascii', 12, 16);
    if (k === 'VP8X') return { w: 1 + b.readUIntLE(24, 3), h: 1 + b.readUIntLE(27, 3) };
    if (k === 'VP8 ') return { w: b.readUInt16LE(26) & 0x3fff, h: b.readUInt16LE(28) & 0x3fff };
    if (k === 'VP8L') { const n = b.readUInt32LE(21); return { w: 1 + (n & 0x3fff), h: 1 + ((n >> 14) & 0x3fff) }; }
    return null;
  }
  if (b[0] !== 0xff || b[1] !== 0xd8) return null;
  for (let i = 2; i + 9 < b.length;) {
    if (b[i] !== 0xff) return null;
    const m = b[i + 1];
    if (m >= 0xc0 && m <= 0xcf && m !== 0xc4 && m !== 0xc8 && m !== 0xcc) return { w: b.readUInt16BE(i + 7), h: b.readUInt16BE(i + 5) };
    i += 2 + b.readUInt16BE(i + 2);
  }
  return null;
}

/** Writes a new listing: its page file, photo list, the old-address redirect id, postal code, video and a homepage card. Returns false (nothing written) if the page exists. */
export function writeListing({ page, photos, card, video }, id, root = ROOT) {
  const p = path.join(root, 'src/data/listings', `${page.slug}.json`);
  if (fs.existsSync(p)) return false;
  fs.writeFileSync(p, JSON.stringify(page));
  fs.mkdirSync(path.join(root, 'src/data/listing-photos'), { recursive: true });
  fs.writeFileSync(path.join(root, 'src/data/listing-photos', `${page.slug}.json`), JSON.stringify(photos));
  const addKey = (file, key, value) => {
    const fp = path.join(root, file);
    if (!fs.existsSync(fp)) return;
    const s = fs.readFileSync(fp, 'utf8'), at = s.lastIndexOf('}');
    if (at < 0 || s.includes(`"${key}":`)) return;
    const t = `${s.slice(0, at).replace(/\s*$/, '')},\n${JSON.stringify(key)}: ${JSON.stringify(value)}\n}${s.slice(at + 1)}`;
    try { JSON.parse(t); fs.writeFileSync(fp, t); } catch { /* leave the file as it was */ }
  };
  addKey('src/worker/listing-ids.json', String(id), page.slug);
  if (card.postal) addKey('src/data/listing-postal.json', page.slug, card.postal);
  if (video) addKey('src/data/listing-media.json', page.slug, { video });
  const hp = path.join(root, 'src/data/home.ts');
  if (fs.existsSync(hp)) {
    const q = (v) => `'${String(v).replace(/\\/g, '\\\\').replace(/'/g, "\\'")}'`;
    const f = [`slug: ${q(page.slug.replace(/^listing\./, ''))}`, `street: ${q(card.street)}`, `city: ${q(card.city)}`, `brokerage: ${q(card.brokerage)}`, `price: ${q(card.price)}`];
    if (/^\d+$/.test(card.beds)) f.push(`beds: ${card.beds}`);
    if (/^\d+(\.0)?$/.test(card.baths)) f.push(`baths: ${Number(card.baths)}`);
    if (card.area) f.push(`sqft: ${q(card.area.replace(/\s*sq\.? ?ft\.?/i, 'sqft'))}`);
    const s = fs.readFileSync(hp, 'utf8');
    if (s.includes('export const listings = [\n')) fs.writeFileSync(hp, s.replace('export const listings = [\n', `export const listings = [\n  { ${f.join(', ')} },\n`));
  }
  return true;
}

export function readListings(root = ROOT) {
  const dir = path.join(root, 'src/data/listings');
  return fs.readdirSync(dir).filter((f) => f.endsWith('.json')).map((file) => {
    const d = JSON.parse(fs.readFileSync(path.join(dir, file), 'utf8'));
    const sum = (d.blocks || []).find((b) => b.t === 'summary');
    return { file, id: String(d.slug).split('.').pop(), status: d.status, price: (sum?.lines || []).find((x) => /^\$[\d,]+$/.test(x)) || '', title: d.title, slug: d.slug };
  });
}

/** Writes one price change. Text replacement, so the one-line JSON files keep their exact formatting. */
export function apply(change, root = ROOT) {
  const p = path.join(root, 'src/data/listings', change.file);
  const s = fs.readFileSync(p, 'utf8');
  const a = `"t":"summary","lines":["${change.price}"`, b = `"t":"summary","lines":["${change.to}"`;
  const a2 = `"t": "summary", "lines": ["${change.price}"`, b2 = `"t": "summary", "lines": ["${change.to}"`;
  if (!s.includes(a) && !s.includes(a2)) return false;
  fs.writeFileSync(p, s.replace(a, b).replace(a2, b2));
  const hp = path.join(root, 'src/data/home.ts');
  const short = String(change.slug).replace(/^listing\./, '');
  const home = fs.readFileSync(hp, 'utf8').split('\n').map((line) => line.includes(`slug: '${short}'`) ? line.replace(`price: '${change.price}'`, `price: '${change.to}'`) : line).join('\n');
  fs.writeFileSync(hp, home);
  return true;
}

export function report({ changes, gone, odd, fresh, sold = [], made = [] }, written) {
  const L = [];
  for (const m of made) L.push(`PAGE   ${m.title}: new listing, page made from MyRealPage${written ? '' : ' (not written)'}. Photos load from MyRealPage until they are processed.`);
  for (const c of sold) L.push(`SOLD   ${c.title}: sold ${c.soldDate}${written ? '' : ' (not written)'}`);
  for (const c of changes) L.push(`PRICE  ${c.title}: ${c.price} -> ${c.to}${written ? '' : ' (not written)'}`);
  for (const c of odd) L.push(`CHECK  ${c.title}: site ${c.price}, MLS ${c.to}. Too big a jump to change automatically.`);
  for (const g of gone) L.push(`GONE   ${g.title}: Active on the site, not in the MLS active list and not in the sold list (expired, cancelled or pending?).`);
  for (const f of fresh) L.push(`NEW    MLS ${f.mls || f.id} at ${f.price}: active on MLS, no page on the site yet${f.why ? ` (a page could not be made: ${f.why})` : ''}.`);
  return L.length ? L.join('\n') : 'All active listing prices match MLS.';
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  const dry = process.argv.includes('--dry');
  const fi = process.argv.indexOf('--file');
  const html = fi > 0 ? fs.readFileSync(process.argv[fi + 1], 'utf8') : await (await fetch(FEED, { headers: { 'user-agent': 'jaredgibbons.ca listing sync' } })).text();
  const feed = parseFeed(html);
  // An empty or broken page must never read as "everything left the market".
  if (feed.size === 0) { console.error('No listings could be read from MyRealPage. Nothing changed.'); process.exit(1); }
  const p = plan(readListings(), feed);
  // Most of the site's active listings missing at once reads as a broken or half-loaded page, not a real change: stop before marking anything.
  const active = readListings().filter((l) => l.status === 'Active' && !OFF_FEED.has(l.id)).length;
  if (active >= 4 && p.gone.length > active / 2) { console.error(`${p.gone.length} of ${active} active listings are missing from the MyRealPage list. That looks like a bad read. Nothing changed.`); process.exit(1); }
  const get = async (url) => (await fetch(url, { headers: { 'user-agent': 'jaredgibbons.ca listing sync' } })).text();
  // Listings that left the active list: sold ones are marked sold with their date; the rest are reported.
  if (fi < 0) Object.assign(p, await findSold(p.gone, get));
  p.sold = p.sold || [];
  // New listings: build each one's page from its own MyRealPage page. One that cannot be built stays in the report as NEW.
  p.made = [];
  if (fi < 0 && p.fresh.length) {
    const all = readListings();
    const dfile = all.filter((l) => l.status === 'Active' && !OFF_FEED.has(l.id)).map((l) => JSON.parse(fs.readFileSync(path.join(ROOT, 'src/data/listings', l.file), 'utf8')).blocks.filter((b) => b.t === 'agent' || b.t === 'disclaimer')).find((t) => t.length === 2) || [];
    const left = [];
    for (const f of p.fresh) {
      const slug = (String(f.url).match(/\/(listing\.[a-z0-9-]+\.\d+)$/) || [])[1];
      let b = slug && slug.endsWith(`.${f.id}`) ? buildListing(await get(f.url), { id: f.id, slug, mls: f.mls }, dfile) : { error: 'no page address' };
      if (b.error) { left.push({ ...f, why: b.error }); continue; }
      // Real photo shapes, read from the small copies (a few kB each). A photo that cannot be read keeps the usual 3:2.
      await Promise.all(b.photos.map(async (ph) => { try { const r = await fetch(ph.u.s || ph.u.l, { headers: { accept: 'image/jpeg,image/png', range: 'bytes=0-65535' } }); const z = imageSize(Buffer.from(await r.arrayBuffer())); if (z && z.w > 50 && z.h > 50) { ph.h = Math.round(1600 * z.h / z.w); delete ph.g; } } catch { /* keep the guess */ } }));
      if (dry || writeListing(b, f.id)) p.made.push({ title: b.page.title }); else left.push({ ...f, why: 'a page file with that name already exists' });
    }
    p.fresh = left;
  }
  if (!dry) { for (const c of p.changes) apply(c); p.sold = p.sold.filter((c) => applySold(c) || (p.gone.push(c), false)); }
  const text = report(p, !dry);
  console.log(text);
  if (process.env.GITHUB_OUTPUT) {
    fs.appendFileSync(process.env.GITHUB_OUTPUT, `changed=${!dry && p.changes.length + p.sold.length + p.made.length > 0}\nattention=${p.gone.length + p.odd.length + p.fresh.length + p.made.length > 0}\n`);
    fs.writeFileSync('sync-report.txt', text + '\n');
  }
}
