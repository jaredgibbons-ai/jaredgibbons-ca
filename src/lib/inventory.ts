// Inventory gate (src/data/inventory/gate.json): slugs whose live-listing count is under the 5-listing rule and that are mostly a listing feed.
import gate from '../data/inventory/gate.json';

const pages = (gate as any).pages as Record<string, { action: string }>;
export const noindexSlugs = new Set(Object.entries(pages).filter(([, v]) => v.action === 'noindex').map(([k]) => k));
export const isGated = (slug: string) => noindexSlugs.has(slug);
