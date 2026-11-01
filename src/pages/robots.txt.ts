// Preview builds keep the site closed to crawlers. Setting PUBLIC_LAUNCH=1 at build time (a launch step that needs
// Jared's explicit approval, see docs/06) opens it and advertises the sitemap.
import type { APIRoute } from 'astro';

export const GET: APIRoute = () => {
  const launch = import.meta.env.PUBLIC_LAUNCH === '1';
  const body = launch
    ? 'User-agent: *\nAllow: /\nDisallow: /internal/\nDisallow: /api/\n\nSitemap: https://jaredgibbons.ca/sitemap.xml\n'
    : 'User-agent: *\nDisallow: /\n';
  return new Response(body, { headers: { 'content-type': 'text/plain; charset=utf-8' } });
};
