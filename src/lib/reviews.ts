// Picks which Google review excerpts a page shows. src/data/review-excerpts.json holds the whole pool (tools/build_review_pool.py,
// from Jared's Google 5-star export of Nov 1, 2026), each excerpt tagged from the words in the excerpt itself. A page shows three:
// the ones whose tags match what the page is about (condos, townhomes, selling, first-time buyers, commercial, an area), then a stable
// per-slug shuffle so neighbouring pages get different mixes. Wording is never edited.
const WANT: [RegExp, string, number][] = [
  [/condo|apartment|penthouse|presale|strata/, 'condo', 3], [/townho(me|use)/, 'townhome', 3], [/duplex/, 'duplex', 3],
  [/sell|selling|sold|evaluation|home-value|listing-presentation/, 'sell', 2.5], [/first-time|first-home|ftb|gst-rebate|ptt/, 'first', 2.5],
  [/commercial|lease|industrial/, 'commercial', 3], [/invest|rental/, 'invest', 3],
  [/langley|aldergrove|willoughby|walnut-grove|murrayville|brookswood/, 'langley', 1.5], [/surrey|white-rock|ocean-park|crescent|cloverdale|grandview|morgan|elgin/, 'surrey', 1.5],
  [/ladner|tsawwassen|delta/, 'ladner', 1.5], [/port-coquitlam|coquitlam|poco/, 'poco', 1.5], [/vancouver|burnaby|new-westminster/, 'vancouver', 1.2],
  [/homes-for-sale|houses|real-estate|guide|acreage|waterfront|ocean-view/, 'house', 0.8], [/homes-for-sale|buy|guide|real-estate/, 'buy', 0.6],
];
function hash(s: string) { let h = 0; for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0; return h; }
export function pickReviews(slug: string, items: any[], n = 3): any[] {
  if (!items?.length) return [];
  let seed = hash(slug) || 1;
  const rnd = () => { seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0; return seed / 4294967296; };
  const want = WANT.filter(([rx]) => rx.test(slug));
  const wantTags = new Map<string, number>(); for (const [, tag, w] of want) wantTags.set(tag, w);
  const sellPage = wantTags.has('sell');
  const scored = items.map((r) => {
    const tags: string[] = r.tags || [];
    let s = tags.reduce((a, t) => a + (wantTags.get(t) || 0), 0);
    // on a selling page, a buyer-only excerpt is a poor fit and vice versa
    if (sellPage && tags.includes('buy') && !tags.includes('sell')) s -= 2;
    if (!sellPage && tags.includes('sell') && !tags.includes('buy') && !wantTags.has('condo') && !wantTags.has('townhome') && !wantTags.has('duplex')) s -= 0.5;
    return { r, s: s + rnd() * 2.6 };       // the jitter spreads neighbouring pages across the matching excerpts
  }).sort((a, b) => b.s - a.s);
  return scored.slice(0, n).map((x) => x.r);
}
