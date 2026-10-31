import rules from './rules.json';
import { buildIndex, route, NESTED } from './route.js';

const index = buildIndex(rules);
const SECURITY = {
  'x-content-type-options': 'nosniff',
  'referrer-policy': 'strict-origin-when-cross-origin',
};

export default {
  async fetch(request, env) {
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
    const cands = new Set([u.pathname, u.pathname + '.html', '/index.html', u.pathname.replace(/\/+$/, ''), '/404.html']);
    for (const [re, f] of NESTED) {
      const m = u.pathname.match(re); if (m) cands.add(f(m));
    }
    for (const c of cands) await exists(c);
    const decision = route(request.url, index, (p) => seen.get(p) === true);

    const withHeaders = (res, extra = {}) => {
      const h = new Headers(res.headers);
      for (const [k, v] of Object.entries({ ...SECURITY, ...extra })) h.set(k, v);
      if (env.PREVIEW === 'true') h.set('x-robots-tag', 'noindex, nofollow');
      return new Response(res.body, { status: res.status, headers: h });
    };
    if (decision.type === 'redirect') {
      return withHeaders(new Response(null, { status: decision.status, headers: { location: decision.location } }));
    }
    if (decision.type === 'asset') {
      const res = await env.ASSETS.fetch(new Request(new URL(decision.path, request.url), request));
      return withHeaders(res, decision.path.endsWith('.html') ? { 'cache-control': 'public, max-age=0, must-revalidate' } : {});
    }
    const nf = await env.ASSETS.fetch(new Request(new URL('/404.html', request.url), { method: 'GET' }));
    return withHeaders(new Response(nf.body, { status: 404, headers: { 'content-type': 'text/html; charset=utf-8' } }), { 'cache-control': 'no-store' });
  },
};
