// "Drive time to your work" helpers (pure, tested). The Google Routes call lives in src/components/CommuteTime.astro and runs in the visitor's browser.
// Nothing the visitor types is sent to us or stored. Departure times are worked out in Pacific time so "weekday 8:00 a.m." means the same for everyone.
const TZ = 'America/Vancouver';

function parts(date, tz) {
  const f = new Intl.DateTimeFormat('en-CA', { timeZone: tz, hourCycle: 'h23', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' });
  return Object.fromEntries(f.formatToParts(date).map((x) => [x.type, x.value]));
}

/** Minutes the zone is ahead of UTC at this moment (Vancouver is -480 in winter, -420 in summer). */
export function tzOffsetMinutes(date, tz = TZ) {
  const p = parts(date, tz);
  const asUtc = Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute, +p.second);
  return Math.round((asUtc - Math.floor(date.getTime() / 1000) * 1000) / 60000);
}

/** The next Monday to Friday occurrence of `hour`:00 in Pacific time that is more than a minute after `from`. */
export function nextWeekdayAt(hour, from = new Date(), tz = TZ) {
  for (let i = 0; i < 9; i++) {
    const probe = new Date(from.getTime() + i * 86400000);
    const p = parts(probe, tz);
    const y = +p.year, m = +p.month, d = +p.day;
    const dow = new Date(Date.UTC(y, m - 1, d)).getUTCDay();
    if (dow < 1 || dow > 5) continue;
    const guess = Date.UTC(y, m - 1, d, hour, 0, 0);
    const t = new Date(guess - tzOffsetMinutes(new Date(guess), tz) * 60000);
    if (t.getTime() > from.getTime() + 60000) return t;
  }
  return null;
}

/** { minutes, km, text } for a route result. */
export function formatTrip(durationMillis, distanceMeters) {
  const minutes = Math.max(1, Math.round(durationMillis / 60000));
  const km = Math.round(distanceMeters / 100) / 10;
  const h = Math.floor(minutes / 60), m = minutes % 60;
  const time = h ? `${h} h${m ? ` ${m} min` : ''}` : `${minutes} min`;
  return { minutes, km, text: `${time} (${km.toLocaleString('en-CA', { minimumFractionDigits: 1, maximumFractionDigits: 1 })} km)` };
}

export const LEAVE_OPTIONS = [['now', 'Now (current traffic)'], ['am', 'Weekday 8:00 a.m.'], ['pm', 'Weekday 5:00 p.m.']];
