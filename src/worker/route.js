// Pure routing decision for jaredgibbons.ca (no Cloudflare APIs, so it is unit-testable).
// Input: URL + rules.json + assetExists(path). Output: one of
//   { type:'redirect', location, status } | { type:'asset', path } | { type:'notfound', reason }
// Rules come from the archive's redirects.csv (tools/build_rules.py). Nothing is guessed:
// conflicting archive rows serve 404, and unknown paths 404.

const TRACKING = /^(utm_[a-z]+|gclid|fbclid|msclkid|mc_cid|mc_eid|_ga|ref)$/i;
// Parent pages that also own nested paths (cannot be a file and a directory at once).
// Emitted under /internal/ (Astro ignores _-prefixed folders). Never served directly.
export const NESTED = [
  [/^\/blog\.html\/(.+)$/, (m) => `/internal/blog/${m[1]}.html`],
  [/^\/our-listings\.html\/(.+)$/, (m) => `/internal/listings/${m[1]}.html`],
];

export function buildIndex(rules, listingIds = {}) {
  const redirects = new Map(rules.redirects.map((r) => [r.from, r]));
  const gone = new Map(rules.gone.map((r) => [r.from, r.serve || 404]));
  const conflicts = new Set(rules.conflicts.map((r) => r.from));
  return { redirects, gone, conflicts, listingIds: new Map(Object.entries(listingIds)) };
}

// Old MyRealPage listing pages (D-231). MRP served an MLS® listing's detail page under any page of the site
// (/murrayville.html/listing.r3170030-49-21746-52-avenue-langley-bc-v2y-1l4.109921749, /recip.html/listing.…), and Google
// indexed about 800 of them (884 clicks in the 3 months to Nov 2026). The new search is a widget, so these addresses
// cannot be served. Jared's own listing (same MRP id) -> its page here; otherwise -> the page it hung under (the same
// area's live search), or the main search. Returns null when the path is not one of these.
// Blog posts that earn search clicks on the old site but were never in the archive (GSC, Nov 2026, D-231): each goes to the page on the same subject.
export const MOVED = {
  '/blog.html/30736-burgess-avenue-abbotsford-1975-acre-luxury-estate-sold-8922133': '/abbotsford-acreages-for-sale.html',
  '/blog.html/surrey-home-sold-419132-120-st-scott-plaza-8797791': '/our-listings.html',
  '/blog.html/sold-at-morgan-crossing-grandview-south-surrey-8988261': '/grandview-surrey.html',
  '/blog.html/just-sold-1265-235-st-langley-acreage-jared-gibbons-8713021': '/langley-acreages-for-sale.html',
  '/blog.html/condo-living-at-5020-221a-street-langley-8957146': '/langley-condos-for-sale.html',
};
export const MRP_LISTING = /^\/([^/]+\.html)\/(?:[^/]+\/)*listing\.[^/]*?(?:\.(\d{6,}))?(?:\.html)?\/?$/;
export function oldListing(path, index, assetExists) {
  const m = path.match(MRP_LISTING);
  if (!m) return null;
  const own = m[2] && index.listingIds.get(m[2]);
  if (own) return `/our-listings.html/${own}`;
  if (m[1] !== 'our-listings.html' && m[1] !== 'mylistings.html' && m[1] !== 'recip.html' && assetExists('/' + m[1])) return '/' + m[1];
  return m[1] === 'our-listings.html' || m[1] === 'mylistings.html' ? '/our-listings.html' : '/recip.html';
}

export function route(url, index, assetExists) {
  const u = new URL(url);
  // 1) host / protocol (the zone should also do this; kept here so previews behave the same)
  if (u.hostname === 'www.jaredgibbons.ca' || (u.protocol === 'http:' && u.hostname.endsWith('jaredgibbons.ca'))) {
    return { type: 'redirect', location: `https://jaredgibbons.ca${u.pathname}${u.search}`, status: 301 };
  }
  let path = u.pathname;
  // /404.html is the error page's own file; asking for it directly must not answer 200 (soft 404)
  if (path === '/404.html') return { type: 'notfound', reason: 'error page is not a page' };
  // internal build output is reachable only through its public URL
  if (path === '/internal' || path.startsWith('/internal/')) return { type: 'notfound', reason: 'internal path' };
  // 2) exact archive rules (path, then path+query)
  const full = path + u.search;
  for (const k of [full, path]) {
    if (index.conflicts.has(k)) return { type: 'notfound', reason: 'conflicting archive rows (OI-10)' };
    if (index.gone.has(k)) return { type: 'notfound', reason: 'broken at source', status: index.gone.get(k) };
    const r = index.redirects.get(k);
    // campaign parameters survive an archive redirect (a rule matched on the path alone, to a target with no query of its own)
    if (r) return { type: 'redirect', location: k === full && u.search ? r.to : (r.to.includes('?') ? r.to : r.to + u.search), status: r.status };
  }
  if (MOVED[path]) return { type: 'redirect', location: MOVED[path] + u.search, status: 301 };
  // 2b) legacy blog filter/month URLs (never rebuilt as pages; the old links carried a doubled prefix)
  if (/^\/blog\.html\/(blog\.html(\/.*)?|archives(\/.*)?)$/.test(path)) {
    return { type: 'redirect', location: '/blog.html', status: 301 };
  }
  // 3) tracking / CMS-preview / pagination params never change the page (served, not redirected,
  //    so analytics still sees the campaign parameters)
  // 4) trailing slash: /x/ -> /x when /x resolves
  if (path.length > 1 && path.endsWith('/')) {
    const stripped = path.replace(/\/+$/, '');
    const hit = resolveAsset(stripped, assetExists) || index.redirects.has(stripped);
    if (hit) return { type: 'redirect', location: stripped + u.search, status: 301 };
    return { type: 'notfound', reason: 'trailing slash, no such page' };
  }
  // 5) assets
  const asset = resolveAsset(path, assetExists);
  if (asset) return { type: 'asset', path: asset };
  // 5b) doubled prefix from relative links on the old site: /<page>.html/<other-page>.html -> /<other-page>.html when that page exists
  const dbl = path.match(/^\/[^/]+\.html\/([^/]+\.html)$/);
  if (dbl && assetExists('/' + dbl[1])) return { type: 'redirect', location: '/' + dbl[1] + u.search, status: 301 };
  // 5c) old MyRealPage listing detail pages (D-231)
  const ol = oldListing(path, index, assetExists);
  if (ol) return { type: 'redirect', location: ol + u.search, status: 301 };
  // 5d) anything else under the old search page (/recip.html/1272399.search/SearchResults.form ...) -> the search page
  if (/^\/recip\.html\/.+/.test(path)) return { type: 'redirect', location: '/recip.html' + u.search, status: 301 };
  // 6) extensionless page names: /contact -> /contact.html (only when that page exists)
  if (!/\.[a-z0-9]+$/i.test(path) && assetExists(path + '.html')) {
    return { type: 'redirect', location: path + '.html' + u.search, status: 301 };
  }
  return { type: 'notfound', reason: 'no such page' };
}

export function resolveAsset(path, assetExists) {
  if (path === '/') path = '/index.html';
  if (assetExists(path)) return path;
  for (const [re, f] of NESTED) {
    const m = path.match(re);
    if (m) { const p = f(m); if (assetExists(p)) return p; }
  }
  return null;
}

// Browser caching (D-240). Pages always revalidate (edits show at once). Build files with a content hash in the name
// (/_astro/) and the fonts never change, so browsers keep them a year; images a week; the search index an hour.
export function cacheFor(path, res) {
  if (res.status !== 200) return {};
  if (path.endsWith('.html')) return { 'cache-control': 'public, max-age=0, must-revalidate' };
  if (path.startsWith('/_astro/') || path.startsWith('/fonts/')) return { 'cache-control': 'public, max-age=31536000, immutable' };
  if (path.startsWith('/img/') || /\.(webp|jpe?g|png|svg|ico|avif)$/i.test(path)) return { 'cache-control': 'public, max-age=604800, stale-while-revalidate=86400' };
  if (path.startsWith('/pagefind/')) return { 'cache-control': 'public, max-age=3600, stale-while-revalidate=86400' };
  return {};
}
