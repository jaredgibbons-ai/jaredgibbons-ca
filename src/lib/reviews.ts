// Picks which of the archived Google review excerpts a page shows. The archive repeats one set of six on 200 of 251 pages;
// now each page shows three from the pool of all 11 archived excerpts, chosen by a stable hash of its slug so the mix differs from
// page to page, with the selling-side excerpts and the buyer-side excerpts pinned to the pages where they fit. Wording is untouched.
const SELL = /(sell|condo|townhome|presale|55-plus|penthouse)/;
const BUY = /(homes-for-sale|houses|buy|waterfront|ocean-view|real-estate|guide)/;
const PINS: Record<string, RegExp> = { 'A.Y.': SELL, 'M.H.': SELL, 'K.H.': SELL, 'W.L.': BUY, 'S.E.': BUY };
function hash(s: string) { let h = 0; for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0; return h; }
export function pickReviews(slug: string, items: any[], n = 3): any[] {
  if (!items?.length) return [];
  // seeded shuffle (stable per slug), then selling- or buyer-side excerpts first on the pages where they fit
  let seed = hash(slug) || 1;
  const rnd = () => { seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0; return seed / 4294967296; };
  const a = [...items];
  for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
  const score = (r: any) => (PINS[r.who] && PINS[r.who].test(slug) ? 1 : 0);
  return a.sort((x, y) => score(y) - score(x)).slice(0, n);
}
