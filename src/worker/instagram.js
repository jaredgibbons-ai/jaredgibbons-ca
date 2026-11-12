// Instagram feed for the home page (D-237). The feed comes from a Behold JSON feed of @jaredgibbonsrealestate
// (behold.so, free plan: 6 posts, refreshed daily, 1,200 requests a month). The Worker asks Behold at most once an hour
// and serves its own cached copy, so visitors never count against that limit. Configure with the Worker variable
// INSTAGRAM_FEED_URL (https://feeds.behold.so/<id>; public, not a secret). Without it the endpoint answers 404 and the
// home-page section stays hidden.
const TTL = 3600;
export async function handleInstagram(request, env, ctx) {
  const notFound = () => new Response('Not found', { status: 404, headers: { 'cache-control': 'no-store' } });
  if (!env.INSTAGRAM_FEED_URL || !/^https:\/\/feeds\.behold\.so\/[\w-]+$/.test(env.INSTAGRAM_FEED_URL)) return notFound();
  if (request.method !== 'GET' && request.method !== 'HEAD') return notFound();
  const cache = caches.default;
  const key = new Request('https://jaredgibbons.ca/api/instagram.json?v=1');
  const hit = await cache.match(key);
  if (hit) return hit;
  try {
    const r = await fetch(env.INSTAGRAM_FEED_URL, { cf: { cacheTtl: TTL } });
    if (!r.ok) return notFound();
    const d = await r.json();
    const posts = (d.posts || []).slice(0, 6).map((p) => {
      const s = p.sizes || {};
      const img = (s.medium || s.small || s.large || {}).mediaUrl || (p.mediaType === 'VIDEO' ? p.thumbnailUrl : p.mediaUrl);
      return { url: p.permalink, img, w: (s.medium || {}).width || 700, h: (s.medium || {}).height || 700,
        alt: String(p.altText || p.prunedCaption || 'Instagram post').slice(0, 160), video: p.mediaType === 'VIDEO', when: p.timestamp };
    }).filter((p) => p.url && p.img && /^https:\/\/(www\.)?instagram\.com\//.test(p.url));
    const res = new Response(JSON.stringify({ username: d.username || 'jaredgibbonsrealestate', posts }), {
      headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': `public, max-age=${TTL}` } });
    if (posts.length) ctx?.waitUntil?.(cache.put(key, res.clone()));
    return res;
  } catch { return notFound(); }
}
