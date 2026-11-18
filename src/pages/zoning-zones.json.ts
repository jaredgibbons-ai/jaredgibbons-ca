// The zoning guide's zone summaries as one small file (D-352), so the address lookup can print what a zone allows right in its
// result, on any page, without carrying the whole guide in the page. Built from src/data/zonings.json.
import type { APIRoute } from 'astro';
import Z from '../data/zonings.json';

export const GET: APIRoute = () => {
  const out: Record<string, { n: string; t: string; f: [string, string][]; h: string; r: string }> = {};
  const slug = (c: string) => c.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  for (const m of (Z as any).munis) for (const z of m.zones) {
    out[z.id] = { n: z.name || '', t: z.type || '', f: z.fields || [], h: z.href || '', r: z.ref || '' };
    // A card that stands for several zones (`covers`, D-354) answers for each of them; `a` is the card to link to (D-360).
    for (const c of z.covers || []) { const k = `${m.id}-${slug(c)}`; if (!out[k]) (out as any)[k] = { ...out[z.id], a: z.id }; }
  }
  return new Response(JSON.stringify(out), { headers: { 'content-type': 'application/json; charset=utf-8' } });
};
