import test from 'node:test';
import assert from 'node:assert/strict';
import { tzOffsetMinutes, nextWeekdayAt, formatTrip } from '../src/lib/commute.js';

// The expected values come from the zone data itself, so the tests stay right whatever BC's clock rules are (the 2026 tz data keeps Vancouver on UTC-7 all year).
const local = (d) => { const f = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Vancouver', hourCycle: 'h23', hour: '2-digit', minute: '2-digit', weekday: 'short' }).formatToParts(d); return Object.fromEntries(f.map((x) => [x.type, x.value])); };

test('offset agrees with Intl for winter and summer dates', () => {
  for (const iso of ['2026-01-15T20:00:00Z', '2026-07-15T20:00:00Z', '2026-11-04T20:00:00Z', '2027-01-15T20:00:00Z']) {
    const d = new Date(iso), off = tzOffsetMinutes(d), l = local(d);
    const wall = new Date(d.getTime() + off * 60000);
    assert.equal(String(wall.getUTCHours()).padStart(2, '0'), l.hour, iso);
  }
});

test('next weekday departure lands on the requested Pacific hour, on a weekday, in the future', () => {
  for (const [iso, hour] of [['2026-11-04T20:00:00Z', 8], ['2026-11-04T20:00:00Z', 17], ['2026-11-06T20:00:00Z', 8], ['2026-11-08T20:00:00Z', 8], ['2026-07-15T20:00:00Z', 8], ['2026-01-15T20:00:00Z', 17]]) {
    const from = new Date(iso), t = nextWeekdayAt(hour, from), l = local(t);
    assert.ok(t > from, iso);
    assert.equal(l.hour, String(hour).padStart(2, '0'), `${iso} ${hour}`); assert.equal(l.minute, '00');
    assert.ok(['Mon', 'Tue', 'Wed', 'Thu', 'Fri'].includes(l.weekday), `${iso} ${l.weekday}`);
    assert.ok(t - from < 5 * 86400000);
  }
  assert.equal(local(nextWeekdayAt(8, new Date('2026-11-06T20:00:00Z'))).weekday, 'Mon');   // Friday afternoon -> Monday
});

test('trip text', () => {
  assert.deepEqual(formatTrip(32 * 60000, 21400), { minutes: 32, km: 21.4, text: '32 min (21.4 km)' });
  assert.equal(formatTrip(65 * 60000, 80000).text, '1 h 5 min (80.0 km)');
  assert.equal(formatTrip(60 * 60000, 50000).text, '1 h (50.0 km)');
  assert.equal(formatTrip(10, 50).minutes, 1);
});
