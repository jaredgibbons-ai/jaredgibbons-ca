import test from 'node:test';
import assert from 'node:assert/strict';
import { MAP_STYLE } from '../src/lib/map-style.js';

const hex = (c) => [1, 3, 5].map((i) => parseInt(c.slice(i, i + 2), 16));
test('map style uses only black, white, cream and grey (no new colours)', () => {
  const cols = MAP_STYLE.flatMap((r) => r.stylers.map((s) => s.color).filter(Boolean));
  assert.ok(cols.length > 10);
  for (const c of cols) { assert.match(c, /^#[0-9a-f]{6}$/i, c); const [r, g, b] = hex(c); assert.ok(Math.max(r, g, b) - Math.min(r, g, b) <= 16, `${c} is too colourful`); }
});
test("Google's shop and restaurant pins and neighbourhood labels are off; parks and transit stations stay", () => {
  const find = (ft, el) => MAP_STYLE.find((r) => r.featureType === ft && (el === undefined || r.elementType === el));
  assert.deepEqual(find('poi').stylers, [{ visibility: 'off' }]);
  assert.deepEqual(find('administrative.neighborhood', 'labels').stylers, [{ visibility: 'off' }]);
  assert.ok(find('poi.park', 'labels.text').stylers.some((s) => s.visibility === 'on'));
  assert.ok(find('transit.station', 'labels.icon').stylers.some((s) => s.visibility === 'on'));
});
