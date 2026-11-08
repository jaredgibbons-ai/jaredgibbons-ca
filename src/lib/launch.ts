// Pages held back at launch (src/data/launch/holds.json, written by tools/launch_pack.py).  A hold only takes effect in the launch build
// (PUBLIC_PREVIEW=false): the page is noindex and out of the sitemap, and the footer and generated link lists stop pointing to it.
// In the preview nothing changes except a note on the held page saying why.
import holds from '../data/launch/holds.json';
import { isPreview } from './preview';

const H = holds as Record<string, string>;
export const holdReason = (slug: string): string | undefined => H[slug];
export const isHeld = (slug: string): boolean => !isPreview && slug in H;
export const slugOfHref = (href: unknown): string | null => {
  const m = String(href || '').replace(/^https:\/\/jaredgibbons\.ca(?=\/)/, '').match(/^\/([a-z0-9\-]+)\.html(?:[#?].*)?$/);
  return m ? m[1] : null;
};
export const isHeldHref = (href: unknown): boolean => { const s = slugOfHref(href); return !!s && isHeld(s); };
/** Link-only list items that point at a held page are dropped in the launch build. */
export const visibleItems = (items: any[][]): any[][] => items.filter((it) => !(it.length === 1 && it[0] && it[0].h && isHeldHref(it[0].h)));
