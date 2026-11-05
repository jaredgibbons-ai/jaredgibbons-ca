// Listing photos: GET/HEAD /listing-photos/<16 hex>-<480|960|1600>.webp, served from the R2 bucket bound as PHOTOS
// (bucket jg-listing-photos; files made by tools/process_photos.py and uploaded by tools/upload_photos_r2.sh).
// Files are named by the SHA-256 of the original so a name never changes its picture: cache for a year.
const NAME = /^\/listing-photos\/([0-9a-f]{16}-(?:480|960|1600)\.webp)$/;

export function photoKey(pathname) {
  const m = NAME.exec(pathname);
  return m ? m[1] : null;
}

export async function handlePhoto(request, env, pathname) {
  const key = photoKey(pathname);
  const miss = () => new Response('Not found', { status: 404, headers: { 'cache-control': 'no-store' } });
  if (!key || !env.PHOTOS) return miss();
  const method = request.method;
  if (method !== 'GET' && method !== 'HEAD') return new Response('Method Not Allowed', { status: 405, headers: { allow: 'GET, HEAD' } });
  const obj = method === 'HEAD' ? await env.PHOTOS.head(key) : await env.PHOTOS.get(key);
  if (!obj) return miss();
  const headers = new Headers({
    'content-type': 'image/webp',
    'cache-control': 'public, max-age=31536000, immutable',
    'x-content-type-options': 'nosniff',
    etag: obj.httpEtag || `"${obj.etag}"`,
  });
  if (typeof obj.size === 'number') headers.set('content-length', String(obj.size));
  if (request.headers.get('if-none-match') === headers.get('etag')) return new Response(null, { status: 304, headers });
  return new Response(method === 'HEAD' ? null : obj.body, { status: 200, headers });
}
