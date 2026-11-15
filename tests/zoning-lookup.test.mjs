// Address -> zoning lookup (D-285): the Worker's decisions, with the public map services mocked.
import test from 'node:test';
import assert from 'node:assert/strict';
import { lookup, handleZoning, ringArea, MUNIS } from '../src/worker/zoning.js';

const geo = (over = {}) => ({ features: [{ geometry: { coordinates: [-122.69, 49.05] }, properties: { civicNumber: 2725, streetName: '192', streetType: 'St', streetDirection: '', localityName: 'Surrey', matchPrecision: 'CIVIC_NUMBER', ...over } }] });
const sq = [[[0, 0], [100, 0], [100, 50], [0, 50], [0, 0]]];   // 5,000 m²
function mock(routes, calls = []) {
  return async (url) => {
    calls.push(url);
    for (const [k, v] of routes) if (url.includes(k)) return new Response(JSON.stringify(typeof v === 'function' ? v(url) : v), { status: 200 });
    return new Response('{}', { status: 500 });
  };
}

test('exact address: zone, bylaw, ALR and lot size come back', async () => {
  const r = await lookup('2725 192 St Surrey', mock([
    ['geocoder.api.gov.bc.ca', geo()],
    ['Planning/MapServer/18', { features: [{ attributes: { ZONING_TEXT: 'CD', ZONING: 'Comprehensive Development Zone', BY_LAW_01: 'B/L 16074', WEBLINK: 'https://cosmos.surrey.ca/x.pdf#nameddest=CD' } }] }],
    ['Planning/MapServer/0', { features: [] }],
    ['Lots/MapServer/7', { features: [{ attributes: {}, geometry: { rings: sq } }] }],
  ]));
  assert.equal(r.status, 'ok');
  assert.equal(r.address, '2725 192 St, Surrey');
  assert.deepEqual(r.zones, [{ code: 'CD', name: 'Comprehensive Development Zone', bylaw: 'B/L 16074', link: 'https://cosmos.surrey.ca/x.pdf#nameddest=CD' }]);
  assert.equal(r.alr, false);
  assert.deepEqual(r.lot, { sqm: 5000, sqft: 53820, acres: 1.24 });
  assert.equal(r.guide, 'zd-surrey');
});

test('a link that is not the city\'s own is dropped', async () => {
  const r = await lookup('2725 192 St Surrey', mock([
    ['geocoder.api.gov.bc.ca', geo()],
    ['Planning/MapServer/18', { features: [{ attributes: { ZONING_TEXT: 'RA', WEBLINK: 'javascript:alert(1)' } }] }],
    ['MapServer', { features: [] }],
  ]));
  assert.equal(r.zones[0].link, undefined);
});

test('block-level match: the municipality\'s own address data finds the lot, or no zone is shown', async () => {
  const blk = geo({ civicNumber: 1265, streetName: '235', localityName: 'Township of Langley', matchPrecision: 'BLOCK' });
  const calls = [];
  const ok = await lookup('1265 235 St Langley', mock([
    ['geocoder.api.gov.bc.ca', blk],
    ['where=', { features: [{ attributes: { HOUSE: 1265, STREET: '235 ST' }, centroid: { x: -122.5749, y: 49.0245 } }] }],
    ['Zoning/FeatureServer/0', { features: [{ attributes: { Zone: 'RU-3', ZoneCategory: 'Rural' } }] }],
    ['AgriculturalLandReserve', { features: [{ attributes: {} }] }],
    ['Parcels/FeatureServer/0', { features: [{ attributes: {}, geometry: { rings: sq } }] }],
  ], calls));
  assert.equal(ok.status, 'ok');
  assert.equal(ok.zones[0].code, 'RU-3');
  assert.equal(ok.alr, true);
  assert.ok(calls.some((u) => u.includes('geometry=-122.5749,49.0245')), 'zoning asked at the parcel, not the block point');

  const none = await lookup('1265 235 St Langley', mock([['geocoder.api.gov.bc.ca', blk], ['where=', { features: [] }]]));
  assert.equal(none.status, 'notfound');
  // "40 AVE%" also matching "40A AVE" is ambiguous: no answer.
  const two = await lookup('1265 235 St Langley', mock([['geocoder.api.gov.bc.ca', blk], ['where=', { features: [{ attributes: { STREET: '235 ST' }, centroid: { x: 1, y: 1 } }, { attributes: { STREET: '235A ST' }, centroid: { x: 2, y: 2 } }] }]]));
  assert.equal(two.status, 'notfound');
});

test('outside the covered municipalities, junk, and upstream failure', async () => {
  assert.equal((await lookup('100 Main St Vancouver', mock([['geocoder', geo({ localityName: 'Vancouver' })]]))).status, 'unsupported');
  assert.equal((await lookup('Surrey', mock([]))).status, 'bad');
  assert.equal((await lookup('x'.repeat(130) + '1', mock([]))).status, 'bad');
  assert.equal((await lookup('1 Nowhere Rd', mock([['geocoder', { features: [{ geometry: { coordinates: [0, 0] }, properties: { localityName: 'Surrey', matchPrecision: 'LOCALITY', civicNumber: '', streetName: '' } }] }]]))).status, 'notfound');
  assert.equal((await lookup('2725 192 St Surrey', mock([['geocoder', geo()], ['MapServer', { features: [] }]]))).status, 'nozone');
  const res = await handleZoning(new Request('https://jaredgibbons.ca/api/zoning?address=2725%20192%20St'), mock([]));
  assert.equal(res.status, 502);
  assert.equal(res.headers.get('cache-control'), 'no-store');
  assert.equal((await handleZoning(new Request('https://jaredgibbons.ca/api/zoning?address=x'), mock([]))).status, 400);
  assert.equal((await handleZoning(new Request('https://jaredgibbons.ca/api/zoning?address=1', { method: 'POST' }), mock([]))).status, 405);
});

test('the ALR layer failing does not hide the zone', async () => {
  const r = await lookup('2725 192 St Surrey', mock([['geocoder', geo()], ['Planning/MapServer/18', { features: [{ attributes: { ZONING_TEXT: 'RA' } }] }]]));
  assert.equal(r.status, 'ok');
  assert.equal(r.alr, null);
  assert.equal(r.lot, undefined);
});

test('area and sources', () => {
  assert.equal(ringArea(sq), 5000);
  for (const m of Object.values(MUNIS)) assert.match(m.zoning, /^https:\/\//);
  assert.deepEqual(Object.keys(MUNIS).sort(), ['Abbotsford', 'Langley', 'Surrey', 'Township of Langley', 'White Rock']);
});
