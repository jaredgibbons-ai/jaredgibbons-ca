import test from 'node:test';
import assert from 'node:assert/strict';
import { PLACE_FIELDS, NEARBY, nearbyRequest, radiusFor, distanceM, describePlaces, kmLabel, MAX_RESULTS } from '../src/lib/nearby-places.js';

test('only name and position are requested: no ratings, hours or photos', () => {
  assert.deepEqual(PLACE_FIELDS, ['displayName', 'location']);
  for (const c of NEARBY) { const r = nearbyRequest(c, { lat: 49.1, lng: -122.7 }, 1500); assert.deepEqual(r.fields, PLACE_FIELDS); assert.equal(r.maxResultCount, MAX_RESULTS); assert.equal(r.rankPreference, 'DISTANCE'); }
});
test('three categories, each with its own letter and types', () => {
  assert.deepEqual(NEARBY.map((c) => c.pin), ['P', 'C', 'G']);
  assert.deepEqual(NEARBY.map((c) => c.id), ['park', 'cafe', 'grocery']);
  assert.ok(NEARBY.every((c) => c.types.length >= 1));
});
test('radius is half the shorter side, between 500 m and 5 km', () => {
  assert.equal(radiusFor(3000, 2000), 1000);
  assert.equal(radiusFor(200, 300), 500);
  assert.equal(radiusFor(60000, 40000), 5000);
  assert.equal(radiusFor(NaN, 100), 1000);
});
test('distance: one degree of latitude is about 111 km', () => {
  const d = distanceM({ lat: 49, lng: -122 }, { lat: 50, lng: -122 });
  assert.ok(d > 111000 && d < 111400, String(d));
});
class LL { constructor(a, b) { this._a = a; this._b = b; } lat() { return this._a; } lng() { return this._b; } }
test('places come back nearest first, unnamed or position-less ones dropped', () => {
  const c = { lat: 49.1, lng: -122.7 };
  const rows = describePlaces([
    { displayName: { text: 'Far Park' }, location: new LL(49.12, -122.7) },
    { displayName: 'Near Park', location: { lat: 49.101, lng: -122.7 } },
    { displayName: { text: '' }, location: { lat: 49.1, lng: -122.7 } },
    { displayName: { text: 'No spot' } },
  ], NEARBY[0], c);
  assert.deepEqual(rows.map((r) => r.name), ['Near Park', 'Far Park']);
  assert.equal(rows[0].label, 'Park');
});
test('distance labels', () => { assert.equal(kmLabel(450), '450 m'); assert.equal(kmLabel(1500), '1.5 km'); assert.equal(kmLabel(2000), '2 km'); });
