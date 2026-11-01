// Two launch gates that keep thin pages out of the index without deleting them (pages stay reachable and linked):
//  1. Listing gate (src/data/inventory/gate.json): a feed page is gated only when the average of its last `min_months` monthly Paragon counts is under `min_active`.
//  2. Uniqueness gate (src/data/inventory/uniqueness.json, written by tools/uniqueness.py --write-gate): a brand-new page under `min_unique` stays out until its copy is raised.
import gate from '../data/inventory/gate.json';
import uniq from '../data/inventory/uniqueness.json';

const g = gate as any;
const pages = g.pages as Record<string, { kind: string; history: { month: string; active: number }[] }>;
const listingGated = (slug: string) => {
  const p = pages[slug];
  if (!p || p.kind !== 'feed') return false;
  const h = p.history.slice(-g.min_months);
  return h.length >= g.min_months && h.reduce((a, b) => a + b.active, 0) / h.length < g.min_active;
};
const u = uniq as any;
// `enforce` is off until Jared and I have reviewed the pages under the threshold together: nothing is held out of the sitemap before then.
const uniquenessHeld = (slug: string) => u.enforce === true && typeof u.scores[slug] === 'number' && u.scores[slug] < u.min_unique;
export const isGated = (slug: string) => listingGated(slug) || uniquenessHeld(slug);
