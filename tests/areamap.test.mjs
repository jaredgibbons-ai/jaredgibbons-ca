import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { validateRegion, popupSpec, centroid, boundsOf, flyoverFor, draftsBlockLaunch } from '../src/lib/areamap.js';

const sq = (s, w, n, e) => [[s, w], [s, e], [n, e], [n, w], [s, w]];
const region = { region: 'test', name: 'Test Region', center: { lat: 49.05, lng: -122.8 }, bbox: [48.9, -123.1, 49.3, -122.5],
  areas: [{ id: 'a-one', name: 'A One', href: '/a-one.html', status: 'draft', rings: [sq(49.0, -122.9, 49.1, -122.8)] },
          { id: 'b-group', name: 'B Group', group: true, href: '/b-group.html', status: 'confirmed', rings: [sq(49.0, -122.8, 49.1, -122.7)] }] };

test('a valid region passes and bad ones are caught', () => {
  assert.deepEqual(validateRegion(region), []);
  const bad = JSON.parse(JSON.stringify(region));
  bad.areas[0].rings[0][4] = [49.0, -122.5]; bad.areas[1].href = 'b.html'; bad.areas[1].status = 'ok'; bad.areas.push({ ...bad.areas[0] });
  const e = validateRegion(bad).join('|');
  assert.match(e, /not closed/); assert.match(e, /href must look like/); assert.match(e, /status must be/); assert.match(e, /duplicate id/);
  const out = JSON.parse(JSON.stringify(region)); out.areas[0].rings[0][1] = [50, -122.9]; out.areas[0].rings[0][4] = out.areas[0].rings[0][0];
  assert.match(validateRegion(out).join('|'), /outside the region bbox/);
});

test('popup wording matches the brief, with the group variant', () => {
  assert.equal(popupSpec(region.areas[0], 'Test Region').title, 'A One - Test Region');
  assert.equal(popupSpec(region.areas[0], 'x').linkText, 'View the neighbourhood page for this area');
  assert.match(popupSpec(region.areas[1], 'x').linkText, /MLS® sub-area group/);
});

test('centroid and bounds', () => {
  const [la, ln] = centroid(region.areas[0].rings); assert.ok(Math.abs(la - 49.05) < 1e-9 && Math.abs(ln + 122.85) < 1e-9);
  assert.deepEqual(boundsOf(region.areas), { south: 49.0, west: -122.9, north: 49.1, east: -122.7 });
});

test('every map file in src/data/maps is valid and every link goes to a real page', () => {
  const dir = new URL('../src/data/maps/', import.meta.url);
  for (const f of fs.readdirSync(dir).filter((x) => x.endsWith('.json'))) {
    const r = JSON.parse(fs.readFileSync(new URL(f, dir), 'utf8'));
    assert.deepEqual(validateRegion(r), [], f);
    for (const a of r.areas) {
      const s = a.href.slice(1, -5);
      assert.ok(fs.existsSync(new URL(`../src/data/pages/${s}.json`, import.meta.url)) || fs.existsSync(new URL(`../src/data/local/${s}.json`, import.meta.url)), `${f}: ${a.href} has no page`);
    }
  }
});

test('sold keys and flyover settings are validated', () => {
  const ring = [[1, 1], [1, 2], [2, 2], [1, 1]];
  const base = { region: 'x', name: 'X', center: { lat: 1, lng: 1 }, bbox: [0, 0, 3, 3], areas: [{ id: 'a', name: 'A', href: '/a.html', status: 'draft', rings: [ring] }] };
  assert.deepEqual(validateRegion(base), []);
  assert.deepEqual(validateRegion({ ...base, areas: [{ ...base.areas[0], sold: 'South Surrey White Rock|Morgan Creek' }], flyover: { lat: 1, lng: 1, altitude: 100, range: 9000, tilt: 55 } }), []);
  assert.ok(validateRegion({ ...base, areas: [{ ...base.areas[0], sold: 'Morgan Creek' }] }).some((e) => /sold must look like/.test(e)));
  assert.ok(validateRegion({ ...base, flyover: { lat: 1, lng: 1 } }).some((e) => /flyover needs/.test(e)));
});

test('3D flyover is on by default, tunable, and can be turned off', () => {
  const r = { bbox: [48.9, -123.1, 49.3, -122.5] };
  const f = flyoverFor(r);
  assert.ok(Math.abs(f.lat - 49.1) < 1e-9 && Math.abs(f.lng + 122.8) < 1e-9);
  assert.ok(f.range >= 4000 && f.range <= 40000); assert.equal(f.tilt, 55);
  assert.equal(flyoverFor({ ...r, flyover: false }), null);
  assert.deepEqual(flyoverFor({ ...r, flyover: { lat: 1, lng: 2, range: 5000 } }), { lat: 1, lng: 2, range: 5000 });
  assert.equal(validateRegion({ region: 'x', name: 'X', bbox: [0, 0, 1, 1], areas: [], flyover: false }).length, 0);
});

test('draft outlines block a launch build but not the preview', () => {
  const r = { areas: [{ id: 'a', status: 'draft' }, { id: 'b', status: 'confirmed' }] };
  assert.deepEqual(draftsBlockLaunch(r, undefined), []);
  assert.deepEqual(draftsBlockLaunch(r, 'true'), []);
  assert.deepEqual(draftsBlockLaunch(r, 'false'), ['a']);
});
