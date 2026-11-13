// Instagram feed for the home page (D-237). The feed comes from a Behold JSON feed of @jaredgibbonsrealestate
// (behold.so, free plan: 6 posts, refreshed daily, 1,200 requests a month). The Worker asks Behold at most once an hour
// and serves its own cached copy, so visitors never count against that limit. Configure with the Worker variable
// INSTAGRAM_FEED_URL (https://feeds.behold.so/<id>; public, not a secret). Without it the endpoint answers 204 (empty) and the
// home-page section stays hidden. Set in wrangler.jsonc (D-254).
const TTL = 3600;
// Photo description: Instagram's own alt text when there is one, else the start of the caption, cut at a word (never mid-word).
function altOf(p) {
  const t = String(p.altText || p.prunedCaption || '').replace(/\s+/g, ' ').trim();
  if (!t) return 'Instagram post';
  if (t.length <= 140) return t;
  const cut = t.slice(0, 140), i = cut.lastIndexOf(' ');
  return (i > 80 ? cut.slice(0, i) : cut).replace(/[\s,;:.!\u2013\u2014-]+$/, '') + '\u2026';
}
export async function handleInstagram(request, env, ctx) {
  const notFound = () => new Response('Not found', { status: 404, headers: { 'cache-control': 'no-store' } });
  // No feed yet (or the feed is down): answer 204, empty, so the home page logs no error and simply keeps the section hidden (D-252).
  const empty = () => new Response(null, { status: 204, headers: { 'cache-control': 'no-store' } });
  if (request.method !== 'GET' && request.method !== 'HEAD') return notFound();
  if (!env.INSTAGRAM_FEED_URL || !/^https:\/\/feeds\.behold\.so\/[\w-]+$/.test(env.INSTAGRAM_FEED_URL)) return empty();
  const cache = caches.default;
  const key = new Request('https://jaredgibbons.ca/api/instagram.json?v=1');
  const hit = await cache.match(key);
  if (hit) return hit;
  try {
    const r = await fetch(env.INSTAGRAM_FEED_URL, { cf: { cacheTtl: TTL } });
    if (!r.ok) return empty();
    const d = await r.json();
    const posts = (d.posts || []).slice(0, 6).map((p) => {
      const s = p.sizes || {};
      const img = (s.medium || s.small || s.large || {}).mediaUrl || (p.mediaType === 'VIDEO' ? p.thumbnailUrl : p.mediaUrl);
      return { url: p.permalink, img, w: (s.medium || {}).width || 700, h: (s.medium || {}).height || 700,
        alt: altOf(p), video: p.mediaType === 'VIDEO', when: p.timestamp };
    }).filter((p) => p.url && p.img && /^https:\/\/(www\.)?instagram\.com\//.test(p.url));
    const res = new Response(JSON.stringify({ username: d.username || 'jaredgibbonsrealestate', posts }), {
      headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': `public, max-age=${TTL}` } });
    if (posts.length) ctx?.waitUntil?.(cache.put(key, res.clone()));
    return res;
  } catch { return empty(); }
}
