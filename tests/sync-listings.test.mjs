// Daily price sync (D-298): the parser and the decisions, without the network.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { parseFeed, plan, apply, report } from '../tools/sync_listings.mjs';

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
  assert.deepEqual(f.get('109878342'), { price: '$1,049,000', status: 'ACTIVE', mls: 'R3168794' });
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
