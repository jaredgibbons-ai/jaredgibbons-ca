// Daily price sync for Jared's own listing pages (D-298).
// The search pages read MyRealPage live, but the pages under /our-listings.html are files in this repository, so a price change on MLS did not reach them.
// This reads Jared's active listings from his public MyRealPage page and, where an Active listing here shows a different price, writes the new price into
// src/data/listings/<file>.json (the headline price line) and the homepage card in src/data/home.ts. "Original Price" is never touched.
// A listing that left the active list and is in Jared's sold list is marked sold with its sold date (D-299) and comes off the homepage cards.
// One that left without selling (expired, cancelled), or a new listing that has no page yet, is reported, not edited.
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

export function report({ changes, gone, odd, fresh, sold = [] }, written) {
  const L = [];
  for (const c of sold) L.push(`SOLD   ${c.title}: sold ${c.soldDate}${written ? '' : ' (not written)'}`);
  for (const c of changes) L.push(`PRICE  ${c.title}: ${c.price} -> ${c.to}${written ? '' : ' (not written)'}`);
  for (const c of odd) L.push(`CHECK  ${c.title}: site ${c.price}, MLS ${c.to}. Too big a jump to change automatically.`);
  for (const g of gone) L.push(`GONE   ${g.title}: Active on the site, not in the MLS active list and not in the sold list (expired, cancelled or pending?).`);
  for (const f of fresh) L.push(`NEW    MLS ${f.mls || f.id} at ${f.price}: active on MLS, no page on the site yet.`);
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
  const get = async (url) => (await fetch(url, { headers: { 'user-agent': 'jaredgibbons.ca listing sync' } })).text();
  // Listings that left the active list: sold ones are marked sold with their date; the rest are reported.
  if (fi < 0) Object.assign(p, await findSold(p.gone, get));
  p.sold = p.sold || [];
  if (!dry) { for (const c of p.changes) apply(c); p.sold = p.sold.filter((c) => applySold(c) || (p.gone.push(c), false)); }
  const text = report(p, !dry);
  console.log(text);
  if (process.env.GITHUB_OUTPUT) {
    fs.appendFileSync(process.env.GITHUB_OUTPUT, `changed=${!dry && p.changes.length + p.sold.length > 0}\nattention=${p.gone.length + p.odd.length + p.fresh.length > 0}\n`);
    fs.writeFileSync('sync-report.txt', text + '\n');
  }
}
