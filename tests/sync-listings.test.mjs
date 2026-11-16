// Daily price sync (D-298): the parser and the decisions, without the network.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { parseFeed, plan, apply, report, parseDetail, findSold, applySold, SOLD_FEED } from '../tools/sync_listings.mjs';

const li = (id, price, mls) => `<li class="mrp-listing-result listing-id-${id} status-ACTIVE photo-overlay" data-listing-id="${id}" data-share-url="https://idx.myrealpage.com/x/listing.${mls.toLowerCase()}-1-main-st.${id}"><h3 class="listing-item-entry-title"> 1 Main St in Surrey : MLS®# ${mls} </h3><div class="price"><span>${price}</span></div><dd>Taxes: $4,644.27</dd></li>`;
const html = `<ul>${li('109878342', '$1,049,000', 'R3168794')}${li('200', '$799,000', 'C8082741')}${li('999', '$650,000', 'R3999999')}</ul>`;
const site = [
  { file: 'a.json', id: '109878342', status: 'Active', price: '$1,099,000', title: '96 15500 Rosemary Heights', slug: 'listing.r3168794-96.109878342' },
  { file: 'b.json', id: '200', status: 'Active', price: '$799,000', title: '12 5327 192 St', slug: 'listing.c8082741-12.200' },
  { file: 'c.json', id: '300', status: 'Active', price: '$1,279,000', title: '116 Calgary Ave', slug: 'listing.x.300' },
  { file: 'd.json', id: '400', status: 'Sold', price: '$500,000', title: 'Sold one', slug: 'listing.y.400' },
];

test('the feed is read: id, price, status, MLS number', () => {
  const f = parseFeed(html);
  assert.equal(f.size, 3);
  assert.deepEqual(f.get('109878342'), { price: '$1,049,000', status: 'ACTIVE', mls: 'R3168794', url: 'https://idx.myrealpage.com/x/listing.r3168794-1-main-st.109878342' });
  assert.equal(parseFeed('<html>login</html>').size, 0);
});

test('a price change is planned; gone and new listings are reported, sold ones are left alone', () => {
  const p = plan(site, parseFeed(html));
  assert.deepEqual(p.changes.map((c) => [c.file, c.price, c.to]), [['a.json', '$1,099,000', '$1,049,000']]);
  assert.deepEqual(p.gone.map((g) => g.file), ['c.json']);
  assert.deepEqual(p.fresh.map((f) => f.mls), ['R3999999']);
  const text = report(p, true);
  assert.match(text, /^PRICE {2}96 15500 Rosemary Heights: \$1,099,000 -> \$1,049,000$/m);
  assert.match(text, /^GONE {3}116 Calgary Ave/m);
  assert.match(text, /^NEW {4}MLS R3999999/m);
  assert.equal(report(plan([site[1]], parseFeed(li('200', '$799,000', 'C8082741'))), true), 'All active listing prices match MLS.');
});

test('a listing on another board is left alone', () => {
  const p = plan([{ file: 'c.json', id: '109415142', status: 'Active', price: '$1,279,000', title: '116 Calgary Ave', slug: 'listing.x.109415142' }], parseFeed(html));
  assert.deepEqual([p.changes.length, p.gone.length, p.odd.length], [0, 0, 0]);
});

test('an implausible jump is reported, never written', () => {
  const p = plan([site[0]], parseFeed(li('109878342', '$104,900', 'R3168794')));
  assert.equal(p.changes.length, 0);
  assert.equal(p.odd.length, 1);
});

test('apply writes the headline price and the homepage card, and leaves Original Price alone', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'sync-'));
  fs.mkdirSync(path.join(root, 'src/data/listings'), { recursive: true });
  const json = '{"slug":"listing.r3168794-96.109878342","status":"Active","blocks":[{"t":"summary","lines":["$1,099,000","Residential"]},{"t":"facts","items":[{"k":"Original Price:","v":["$1,099,000"]}]}]}';
  fs.writeFileSync(path.join(root, 'src/data/listings/a.json'), json);
  fs.writeFileSync(path.join(root, 'src/data/home.ts'), "  { slug: 'r3168794-96.109878342', price: '$1,099,000', beds: 3 },\n  { slug: 'other.1', price: '$1,099,000' },\n");
  assert.equal(apply({ ...site[0], to: '$1,049,000' }, root), true);
  assert.equal(fs.readFileSync(path.join(root, 'src/data/listings/a.json'), 'utf8'), json.replace('"lines":["$1,099,000"', '"lines":["$1,049,000"'));
  assert.equal(fs.readFileSync(path.join(root, 'src/data/home.ts'), 'utf8'), "  { slug: 'r3168794-96.109878342', price: '$1,049,000', beds: 3 },\n  { slug: 'other.1', price: '$1,099,000' },\n");
});

test('the real listing files are readable by the sync', async () => {
  const { readListings } = await import('../tools/sync_listings.mjs');
  const all = readListings();
  const active = all.filter((l) => l.status === 'Active');
  assert.ok(all.length >= 200 && active.length >= 1);
  for (const l of active) { assert.match(l.id, /^\d{6,}$/, l.file); assert.match(l.price, /^\$[\d,]+$/, l.file); }
});

test('sold: real MyRealPage markup is read (list item and the listing page summary)', () => {
  const item = fs.readFileSync(new URL('./fixtures/mrp-sold-item.html', import.meta.url), 'utf8');
  const f = parseFeed(item).get('103799274');
  assert.equal(f.status, 'SOLD');
  assert.match(f.url, /^https:\/\/idx\.myrealpage\.com\/.+listing\.r2946489-2623-216-street-langley-v2z-1p4\.103799274$/);
  assert.deepEqual(parseDetail(fs.readFileSync(new URL('./fixtures/mrp-detail-sold-summary.html', import.meta.url), 'utf8')), { status: 'Sold', soldDate: 'Jun 20, 2025' });
  assert.deepEqual(parseDetail('<dt>Status:</dt> <dd >Active</dd>'), { status: 'Active', soldDate: '' });
});

test('sold: a listing in the sold list gets its date; one that is not stays reported as gone', async () => {
  const item = fs.readFileSync(new URL('./fixtures/mrp-sold-item.html', import.meta.url), 'utf8');
  const detail = fs.readFileSync(new URL('./fixtures/mrp-detail-sold-summary.html', import.meta.url), 'utf8');
  const calls = [];
  const get = async (url) => { calls.push(url); return url.startsWith(SOLD_FEED) ? (url.endsWith('_pg=1') ? item : '') : detail; };
  const gone = [{ file: 'a.json', id: '103799274', title: '2623 216 St' }, { file: 'b.json', id: '555', title: 'Expired one' }];
  const r = await findSold(gone, get);
  assert.deepEqual(r.sold.map((x) => [x.id, x.soldDate]), [['103799274', 'Jun 20, 2025']]);
  assert.deepEqual(r.gone.map((x) => x.id), ['555']);
  assert.match(report({ changes: [], odd: [], fresh: [], ...r }, true), /^SOLD {3}2623 216 St: sold Jun 20, 2025$/m);
  // a page that says Sold with no readable date is not trusted
  const r2 = await findSold([gone[0]], async (url) => (url.startsWith(SOLD_FEED) ? (url.endsWith('_pg=1') ? item : '') : '<dt>Status:</dt><dd>Sold</dd>'));
  assert.equal(r2.sold.length, 0);
});

test('sold: the page data is marked sold and the homepage card is removed', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'sold-'));
  fs.mkdirSync(path.join(root, 'src/data/listings'), { recursive: true });
  const json = '{"slug":"listing.r1-1-main.200","status":"Active","blocks":[{"t":"summary","lines":["$799,000"]},{"t":"facts","items":[{"k":"Status:","v":["Active"]},{"k":"MLS® Num:","v":["R1"]},{"k":"Bedrooms:","v":["3"]}]}]}';
  fs.writeFileSync(path.join(root, 'src/data/listings/b.json'), json);
  fs.writeFileSync(path.join(root, 'src/data/home.ts'), "export const listings = [\n  { slug: 'r1-1-main.200', price: '$799,000' },\n  { slug: 'other.1', price: '$1' },\n];\n");
  assert.equal(applySold({ file: 'b.json', slug: 'listing.r1-1-main.200', soldDate: 'Nov 20, 2026' }, root), true);
  const d = JSON.parse(fs.readFileSync(path.join(root, 'src/data/listings/b.json'), 'utf8'));
  assert.equal(d.status, 'Sold');
  assert.deepEqual(d.blocks[1].items.map((i) => `${i.k}${i.v[0]}`), ['Status:Sold', 'MLS® Num:R1', 'Sold Date:Nov 20, 2026', 'Bedrooms:3']);
  assert.equal(fs.readFileSync(path.join(root, 'src/data/home.ts'), 'utf8'), "export const listings = [\n  { slug: 'other.1', price: '$1' },\n];\n");
  // a file that does not have the expected lines is left exactly as it was
  fs.writeFileSync(path.join(root, 'src/data/listings/c.json'), '{"slug":"x","status":"Active","blocks":[]}');
  assert.equal(applySold({ file: 'c.json', slug: 'x', soldDate: 'Nov 20, 2026' }, root), false);
  assert.equal(fs.readFileSync(path.join(root, 'src/data/listings/c.json'), 'utf8'), '{"slug":"x","status":"Active","blocks":[]}');
});

test('sold: every active listing file on the site can be marked sold cleanly', async () => {
  const { readListings } = await import('../tools/sync_listings.mjs');
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'soldall-'));
  fs.mkdirSync(path.join(root, 'src/data/listings'), { recursive: true });
  fs.copyFileSync(new URL('../src/data/home.ts', import.meta.url), path.join(root, 'src/data/home.ts'));
  for (const l of readListings().filter((x) => x.status === 'Active')) {
    fs.copyFileSync(new URL(`../src/data/listings/${l.file}`, import.meta.url), path.join(root, 'src/data/listings', l.file));
    assert.equal(applySold({ ...l, soldDate: 'Nov 20, 2026' }, root), true, l.file);
  }
});
