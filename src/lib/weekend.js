// "This weekend" for the open-house pages (D-368): the Saturday and Sunday people mean on the day they search, in Vancouver time.
// Monday to Friday -> the coming weekend; Saturday and Sunday -> the current one. Used at build time and by the Worker on every request,
// so the date on the page is right even between builds.
const DAY = 86400000;
export function weekendLabel(now = new Date()) {
  const fmt = (d, o) => d.toLocaleDateString('en-CA', { timeZone: 'America/Vancouver', ...o });
  const wd = fmt(now, { weekday: 'short' });               // Mon..Sun in Vancouver
  const idx = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 }[wd];
  const toSat = idx === 0 ? -1 : 6 - idx;                  // Sunday belongs to the weekend that started yesterday
  const sat = new Date(now.getTime() + toSat * DAY), sun = new Date(sat.getTime() + DAY);
  const m1 = fmt(sat, { month: 'long' }), m2 = fmt(sun, { month: 'long' });
  const d1 = fmt(sat, { day: 'numeric' }), d2 = fmt(sun, { day: 'numeric' });
  return { text: `Saturday, ${m1} ${d1} and Sunday, ${m2} ${d2}`, short: m1 === m2 ? `${m1.slice(0, 3)} ${d1}–${d2}` : `${m1.slice(0, 3)} ${d1}–${m2.slice(0, 3)} ${d2}` };
}
