// sitemap.xml for the launch site: every indexable canonical URL (pages, posts, own listings that are not expired).
// Preview builds still emit it, but robots.txt keeps the whole preview closed (see robots.txt.ts).
import type { APIRoute } from 'astro';

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

export const GET: APIRoute = () => {
  const groups = [
    import.meta.glob('../data/pages/*.json', { eager: true, import: 'default' }),
    import.meta.glob('../data/posts/*.json', { eager: true, import: 'default' }),
    import.meta.glob('../data/listings/*.json', { eager: true, import: 'default' }),
  ] as Record<string, any>[];
  const urls = new Set<string>();
  for (const g of groups) {
    for (const p of Object.values(g)) {
      if (p.status === 'Expired') continue; // A-03: expired listings stay reachable but noindexed
      const robots = String(p.seo?.['Meta robots'] ?? '');
      if (/noindex/i.test(robots)) continue;
      if (p.canonical) urls.add(p.canonical);
    }
  }
  for (const [f, l] of Object.entries(import.meta.glob('../data/local/*.json', { eager: true, import: 'default' }) as Record<string, any>)) {
    if (l.new_page && l.status !== 'hold') urls.add(`https://jaredgibbons.ca/${f.split('/').pop()!.replace(/\.json$/, '')}.html`);
  }
  urls.add('https://jaredgibbons.ca/');
  const body = [...urls].sort().map((u) => `  <url><loc>${esc(u)}</loc></url>`).join('\n');
  return new Response(`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`, {
    headers: { 'content-type': 'application/xml; charset=utf-8' },
  });
};
