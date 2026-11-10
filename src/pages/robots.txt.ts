// robots.txt follows the same single launch switch as every page's meta robots (D-200): preview builds keep the site closed
// to crawlers; the launch build (PUBLIC_PREVIEW=false, needs Jared's approval, docs/06) opens it and advertises the sitemap.
// Before D-200 this read a separate PUBLIC_LAUNCH flag that the launch checklist never set, so a launch build would have
// shipped "Disallow: /". The Worker's INDEXABLE header (see docs/06) still has to be switched on as well.
import type { APIRoute } from 'astro';
import { isPreview } from '../lib/preview';

export const GET: APIRoute = () => {
  const body = !isPreview
    ? 'User-agent: *\nAllow: /\nDisallow: /internal/\nDisallow: /api/\n\nSitemap: https://jaredgibbons.ca/sitemap.xml\n'
    : 'User-agent: *\nDisallow: /\n';
  return new Response(body, { headers: { 'content-type': 'text/plain; charset=utf-8' } });
};
