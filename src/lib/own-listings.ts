// Card data for Jared's own listing pages (src/data/listings/*.json), used on /our-listings.html and /sold-properties.html
// so every listing page has a link from the site, not only from the MyRealPage widget.
import { titleCaseAddress } from './seo';

export type OwnCard = { slug: string; href: string; street: string; city: string; price: string; priceNum: number; beds?: string; baths?: string; sqft?: string; type?: string; status: string; mls?: string; soldDate?: string; soldTs: number; year: string };


// The slug is the one consistent source of a listing's address (titles are sometimes marketing text, the H1 is an MLS string such as
// "12451 20TH AVENUE Crescent Bch Ocean Pk. Surrey"). "listing.r2765639-d201-8150-207-street-langley-bc-v2y-4j5.104776820" -> 
// { street: "D201 8150 207 Street", city: "Langley" }. Returns null when no known city ends the address.
const CITIES = ['new westminster', 'north vancouver', 'west vancouver', 'port coquitlam', 'port moody', 'pitt meadows', 'maple ridge', 'white rock', 'harrison hot springs', 'lindell beach', 'cultus lake',
  'vancouver', 'langley', 'surrey', 'delta', 'abbotsford', 'rosedale', 'richmond', 'coquitlam', 'mission', 'princeton', 'chilliwack', 'burnaby', 'penticton', 'squamish', 'kelowna', 'agassiz', 'hope', 'tsawwassen', 'ladner', 'aldergrove', 'cloverdale', 'sardis', 'whistler', 'edson'];
const SMALL = new Set(['of', 'and', 'the']);
function pretty(tok: string): string {
  if (/^\d+(st|nd|rd|th)$/.test(tok)) return tok;
  if (/^(nw|ne|sw|se)$/.test(tok)) return tok.toUpperCase();
  if (/^[a-z]?\d+[a-z]?$/.test(tok) && /\d/.test(tok)) return tok.toUpperCase();
  if (tok === 'e' || tok === 'w' || tok === 'n' || tok === 's') return tok.toUpperCase();
  return tok.charAt(0).toUpperCase() + tok.slice(1);
}
export function parseListingSlug(slug: string): { street: string; city: string } | null {
  let b = String(slug).replace(/^listing\./, '').replace(/\.\d+$/, '');
  b = b.replace(/-[vV]\d[a-z]-\d[a-z]\d$/, '').replace(/-bc$/, '');            // postal code, province
  b = b.replace(/-(commercial-lease|for-lease|for-sale)$/, '').replace(/-([rhcf]\d{6,8}|\d{7,9})$/, '');   // trailing mls number / descriptor
  b = b.replace(/-bc$/, '');
  b = b.replace(/^([rhcf]\d{6,8}|\d{8,9})-(?=.)/, '');                         // leading mls number
  const toks = b.split('-');
  for (const c of CITIES.slice().sort((x, y) => y.split(' ').length - x.split(' ').length)) {
    const ct = c.split(' ');
    if (toks.length > ct.length + 1 && ct.every((t, i) => toks[toks.length - ct.length + i] === t)) {
      const st = toks.slice(0, toks.length - ct.length);
      return { street: st.map((t, i) => (i > 0 && SMALL.has(t) ? t : pretty(t))).join(' '), city: ct.map((t) => t.charAt(0).toUpperCase() + t.slice(1)).join(' ') };
    }
  }
  return null;
}

const MONTHS: Record<string, number> = { Jan: 0, Feb: 1, Mar: 2, Apr: 3, May: 4, Jun: 5, Jul: 6, Aug: 7, Sep: 8, Oct: 9, Nov: 10, Dec: 11 };

export function ownCards(): OwnCard[] {
  const mods = import.meta.glob('../data/listings/*.json', { eager: true, import: 'default' }) as Record<string, any>;
  const out: OwnCard[] = [];
  for (const p of Object.values(mods)) {
    const f: Record<string, string> = {};
    for (const b of p.blocks) if (b.t === 'facts') for (const it of b.items) { const k = String(it.k).replace(/[:.]/g, '').trim(); if (!(k in f) && it.v?.[0]) f[k] = String(it.v[0]); }
    const sum = p.blocks.find((b: any) => b.t === 'summary');
    const price = f['Price'] || (sum?.lines || []).find((l: string) => /^\$[\d,]+/.test(l)) || '';
    const title = String(p.title || '').replace(/ [–|-] MLS .*$/, '').replace(/ \| MLS .*$/, '').trim();
    const parts = title.split(', ').map((x) => x.trim());
    let street = parts[0], city = '';
    if (parts.length >= 2) city = parts.length > 2 && /^(BC|[A-Z]\d[A-Z] ?\d[A-Z]\d)$/.test(parts[parts.length - 1]) ? parts[parts.length - 2] : parts[1];
    else { const m = /^(.*?)\s+([A-Z][A-Za-z .'-]+?)\s+BC$/.exec(title); if (m) { street = m[1]; city = m[2]; } }
    const sd = f['Sold Date'] ? /^(\w{3}) (\d{1,2}), (\d{4})$/.exec(f['Sold Date']) : null;
    const soldTs = sd ? Date.UTC(Number(sd[3]), MONTHS[sd[1]] ?? 0, Number(sd[2])) : 0;
    const ps = parseListingSlug(p.slug);
    out.push({
      slug: p.slug, href: `/our-listings.html/${p.slug}`, street: ps ? ps.street : titleCaseAddress(street), city: ps ? ps.city : city, price, priceNum: Number(price.replace(/[^\d]/g, '')) || 0,
      beds: f['Bedrooms'], baths: f['Bathrooms'], sqft: f['Floor Area'] || f['Living Area'], type: f['Dwelling Type'] || f['Property Type'] || f['Prop Type'],
      status: p.status, mls: f['MLS® Num'] || f['MLS Num'], soldDate: f['Sold Date'], soldTs, year: sd ? sd[3] : '',
    });
  }
  return out;
}
