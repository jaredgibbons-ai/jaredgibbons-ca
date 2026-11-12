import rules from './rules.json';
import listingIds from './listing-ids.json';
import { buildIndex, route, NESTED } from './route.js';
import { handleForm } from './forms.js';
import { handlePhoto } from './photos.js';
import { handleInstagram } from './instagram.js';

const index = buildIndex(rules, listingIds);
// Headers on every response, API and photo answers included. CSP here is frame protection only: a script allowlist needs the launch inventory of
// third-party scripts (Google Maps, Turnstile, MyRealPage, YouTube) and is a separate step (D-140).
const SECURITY = {
  'x-content-type-options': 'nosniff',
  'referrer-policy': 'strict-origin-when-cross-origin',
  'x-frame-options': 'SAMEORIGIN',
  'content-security-policy': "frame-ancestors 'self'; base-uri 'self'",
  'permissions-policy': 'camera=(), microphone=(), payment=(), usb=()',
  'strict-transport-security': 'max-age=31536000',
};
// Fail safe: pages are noindex unless INDEXABLE is exactly the string "true". A missing, mistyped or inherited setting keeps the site closed.
const indexable = (env) => env.INDEXABLE === 'true';

export default {
  async fetch(request, env, ctx) {
    const res = await handle(request, env, ctx);
    const h = new Headers(res.headers);
    for (const [k, v] of Object.entries(SECURITY)) if (!h.has(k)) h.set(k, v);
    if (!indexable(env)) h.set('x-robots-tag', 'noindex, nofollow');
    return new Response(res.body, { status: res.status, statusText: res.statusText, headers: h });
  },
};

async function handle(request, env, ctx) {
  {
    const pathname = new URL(request.url).pathname;
    if (pathname.startsWith('/api/forms/')) return handleForm(request, env);
    if (pathname.startsWith('/listing-photos/')) return handlePhoto(request, env, pathname);
    if (pathname === '/api/instagram.json') return handleInstagram(request, env, ctx);
    // Daily Google reviews copy, served by the jg-reviews Worker over a service binding (nothing public to configure).
    if (pathname === '/api/reviews.json') {
      if (!env.REVIEWS || (request.method !== 'GET' && request.method !== 'HEAD')) return new Response('Not found', { status: 404, headers: { 'cache-control': 'no-store' } });
      try {
        const r = await env.REVIEWS.fetch(new Request('https://jg-reviews/reviews.json'));
        // jg-reviews is still a placeholder until the Google Business Profile feed is connected (BL-03): pass through only a real JSON answer.
        if (r.ok && !/json/i.test(r.headers.get('content-type') || '')) return new Response('Not found', { status: 404, headers: { 'cache-control': 'no-store' } });
        return new Response(r.body, { status: r.status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': r.ok ? 'public, max-age=900' : 'no-store', 'x-content-type-options': 'nosniff' } });
      } catch { return new Response('Not found', { status: 404, headers: { 'cache-control': 'no-store' } }); }
    }
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return new Response('Method Not Allowed', { status: 405, headers: { allow: 'GET, HEAD' } });
    }
    // Existence check against the static assets binding, memoised per request.
    const seen = new Map();
    const exists = async (p) => {
      if (!seen.has(p)) {
        const r = await env.ASSETS.fetch(new Request(new URL(p, request.url), { method: 'HEAD' }));
        seen.set(p, r.status === 200);
      }
      return seen.get(p);
    };
    // route() is synchronous; prefetch the few candidate paths it can ask about.
    const u = new URL(request.url);
    const bare = u.pathname.replace(/\/+$/, '');
    const cands = new Set([u.pathname, u.pathname + '.html', '/index.html', bare, '/404.html']);
    for (const [re, f] of NESTED) {
      for (const pth of [u.pathname, bare]) { const m = pth.match(re); if (m) cands.add(f(m)); }
    }
    const dbl = bare.match(/^\/[^/]+\.html\/([^/]+\.html)$/); if (dbl) cands.add('/' + dbl[1]);
    const par = bare.match(/^\/([^/]+\.html)\/.*listing\./); if (par) cands.add('/' + par[1]);   // old MRP listing pages (D-231)
    for (const c of cands) await exists(c);
    const decision = route(request.url, index, (p) => seen.get(p) === true);

    const withHeaders = (res, extra = {}) => {
      const h = new Headers(res.headers);
      for (const [k, v] of Object.entries(extra)) h.set(k, v);
      return new Response(res.body, { status: res.status, headers: h });
    };
    if (decision.type === 'redirect') {
      // An hour, not forever: a browser keeps a bare 301 indefinitely, so a bad hop would stick for every visitor who met it.
      return withHeaders(new Response(null, { status: decision.status, headers: { location: decision.location, 'cache-control': 'public, max-age=3600' } }));
    }
    if (decision.type === 'asset') {
      const res = await env.ASSETS.fetch(new Request(new URL(decision.path, request.url), request));
      return withHeaders(res, decision.path.endsWith('.html') ? { 'cache-control': 'public, max-age=0, must-revalidate' } : {});
    }
    const nf = await env.ASSETS.fetch(new Request(new URL('/404.html', request.url), { method: 'GET' }));
    return withHeaders(new Response(nf.body, { status: decision.status || 404, headers: { 'content-type': 'text/html; charset=utf-8' } }), { 'cache-control': 'no-store' });
  }
}
