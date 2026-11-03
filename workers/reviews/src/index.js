// jg-reviews: daily pull of Jared's own Google Business Profile reviews (read-only) -> KV -> GET /reviews.json.
//
// - Runs on a cron. Visitors never cause a Google call, so the 600/min quota cannot be hit by traffic.
// - Keeps only public review fields: display name, star rating, text, dates, and Jared's reply. No profile photos, no reviewer ids/emails.
// - Never overwrites a good copy with an empty or failed pull. A failed run only updates the status record.
// - Secrets come from the environment and are never logged or returned.
const TOKEN_URL = 'https://oauth2.googleapis.com/token';
const ACCOUNTS_URL = 'https://mybusinessaccountmanagement.googleapis.com/v1/accounts';
const locationsUrl = (account) => `https://mybusinessbusinessinformation.googleapis.com/v1/${account}/locations?readMask=name,title,metadata&pageSize=100`;
const reviewsUrl = (account, location, page) =>
  `https://mybusiness.googleapis.com/v4/${account}/${location}/reviews?pageSize=50&orderBy=updateTime%20desc${page ? `&pageToken=${encodeURIComponent(page)}` : ''}`;
const STARS = { ONE: 1, TWO: 2, THREE: 3, FOUR: 4, FIVE: 5 };
const MAX_PAGES = 10;
const MAX_REVIEWS = 300;
const KEY_DATA = 'reviews:v1';
const KEY_STATUS = 'status:v1';

export class FeedError extends Error {
  constructor(code, detail) { super(detail || code); this.code = code; }
}

// Google adds "(Translated by Google) ... (Original) ..." around non-English reviews; show the reviewer's own words.
export function cleanComment(raw) {
  if (typeof raw !== 'string') return '';
  let t = raw.replace(/\r\n/g, '\n');
  const orig = t.indexOf('(Original)');
  if (t.startsWith('(Translated by Google)') && orig !== -1) t = t.slice(orig + '(Original)'.length);
  return t.trim().slice(0, 4000);
}

export function normalizeReview(r) {
  const rating = STARS[r?.starRating];
  if (!rating) return null;
  const anon = r.reviewer?.isAnonymous === true || !r.reviewer?.displayName;
  const out = {
    name: anon ? 'A Google user' : String(r.reviewer.displayName).slice(0, 100),
    rating,
    text: cleanComment(r.comment),
    date: r.createTime || r.updateTime || null,
  };
  const reply = cleanComment(r.reviewReply?.comment);
  if (reply) out.reply = { text: reply, date: r.reviewReply.updateTime || null };
  return out;
}

async function getJson(fetchImpl, url, token) {
  const res = await fetchImpl(url, { headers: { authorization: `Bearer ${token}`, accept: 'application/json' } });
  if (res.status === 401 || res.status === 403) throw new FeedError('api_denied', `Google API ${res.status} for ${new URL(url).hostname}`);
  if (res.status === 429) throw new FeedError('rate_limited', 'Google API 429');
  if (!res.ok) throw new FeedError('api_error', `Google API ${res.status} for ${new URL(url).hostname}`);
  return res.json();
}

export async function accessToken(env, fetchImpl = fetch) {
  for (const k of ['GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET', 'GOOGLE_REFRESH_TOKEN']) {
    if (!env[k]) throw new FeedError('missing_secret', `${k} is not set`);
  }
  const res = await fetchImpl(TOKEN_URL, {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: env.GOOGLE_CLIENT_ID, client_secret: env.GOOGLE_CLIENT_SECRET,
      refresh_token: env.GOOGLE_REFRESH_TOKEN, grant_type: 'refresh_token',
    }),
  });
  if (!res.ok) {
    let err = ''; try { err = (await res.json()).error || ''; } catch { /* body is not JSON */ }
    // invalid_grant = refresh token revoked/expired: Jared redoes the OAuth Playground step. invalid_client = wrong id/secret.
    throw new FeedError(err === 'invalid_grant' ? 'token_invalid' : err === 'invalid_client' ? 'client_invalid' : 'token_error', `Token request failed (${res.status}${err ? ' ' + err : ''})`);
  }
  const j = await res.json();
  if (!j.access_token) throw new FeedError('token_error', 'No access token in response');
  return j.access_token;
}

export async function pullReviews(env, fetchImpl = fetch) {
  const token = await accessToken(env, fetchImpl);
  const accounts = (await getJson(fetchImpl, ACCOUNTS_URL, token)).accounts || [];
  if (!accounts.length) throw new FeedError('no_account', 'No Business Profile account on this login');
  let account = null; let loc = null;
  for (const a of accounts) {
    const locs = (await getJson(fetchImpl, locationsUrl(a.name), token)).locations || [];
    const want = env.GBP_LOCATION;
    const hit = want ? locs.find((l) => l.name === want || `locations/${l.name}` === want) : null;
    if (hit) { account = a; loc = hit; break; }
    if (!want && locs.length === 1 && !loc) { account = a; loc = locs[0]; }
    else if (!want && locs.length > 1) throw new FeedError('multiple_locations', `Several locations found (${locs.map((l) => l.title).join(', ')}); set GBP_LOCATION`);
  }
  if (!loc) throw new FeedError('no_location', 'No matching location');
  const reviews = []; let avg = null; let total = null; let page = '';
  for (let i = 0; i < MAX_PAGES; i++) {
    const j = await getJson(fetchImpl, reviewsUrl(account.name, loc.name, page), token);
    if (j.averageRating != null) avg = Number(j.averageRating);
    if (j.totalReviewCount != null) total = Number(j.totalReviewCount);
    for (const r of j.reviews || []) { const n = normalizeReview(r); if (n) reviews.push(n); }
    page = j.nextPageToken || '';
    if (!page || reviews.length >= MAX_REVIEWS) break;
  }
  return {
    fetchedAt: new Date().toISOString(),
    averageRating: Number.isFinite(avg) ? avg : null,
    totalReviewCount: Number.isFinite(total) ? total : reviews.length,
    profileUrl: loc.metadata?.mapsUri || null,
    reviewUrl: loc.metadata?.newReviewUri || null,
    reviews: reviews.slice(0, MAX_REVIEWS),
  };
}

export async function refresh(env, fetchImpl = fetch) {
  const ran = new Date().toISOString();
  try {
    const data = await pullReviews(env, fetchImpl);
    if (!data.reviews.length) throw new FeedError('empty', 'Google returned no reviews; keeping the previous copy');
    await env.REVIEWS_KV.put(KEY_DATA, JSON.stringify(data));
    await env.REVIEWS_KV.put(KEY_STATUS, JSON.stringify({ ran, ok: true, count: data.reviews.length }));
    return { ok: true, count: data.reviews.length };
  } catch (e) {
    const code = e instanceof FeedError ? e.code : 'unexpected';
    await env.REVIEWS_KV.put(KEY_STATUS, JSON.stringify({ ran, ok: false, code, detail: e instanceof FeedError ? e.message : 'Unexpected error' }));
    console.error(`reviews refresh failed: ${code}`);   // code only; no tokens or response bodies
    return { ok: false, code };
  }
}

const JSON_HEADERS = { 'content-type': 'application/json; charset=utf-8', 'x-content-type-options': 'nosniff' };

export async function handle(request, env) {
  const { pathname } = new URL(request.url);
  if (request.method !== 'GET' && request.method !== 'HEAD') return new Response('Method Not Allowed', { status: 405, headers: { allow: 'GET, HEAD' } });
  if (pathname === '/reviews.json') {
    const body = await env.REVIEWS_KV.get(KEY_DATA);
    if (!body) return new Response(JSON.stringify({ error: 'not_ready' }), { status: 404, headers: { ...JSON_HEADERS, 'cache-control': 'no-store' } });
    return new Response(body, { headers: { ...JSON_HEADERS, 'cache-control': 'public, max-age=900', 'access-control-allow-origin': 'https://jaredgibbons.ca' } });
  }
  if (pathname === '/health') {
    const status = JSON.parse((await env.REVIEWS_KV.get(KEY_STATUS)) || 'null');
    return new Response(JSON.stringify({ status }), { headers: { ...JSON_HEADERS, 'cache-control': 'no-store' } });
  }
  return new Response('Not found', { status: 404 });
}

export default {
  fetch: (request, env) => handle(request, env),
  scheduled: (_event, env, ctx) => ctx.waitUntil(refresh(env)),
};
