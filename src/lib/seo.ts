// Search-snippet fitting, applied in layouts/Base.astro so every page gets it.
// Titles: search results show roughly 60-65 characters. When one runs over, trailing " | ..." segments (brand first) are dropped
// until it fits; a title with no segment to drop is left as written. Meta descriptions: kept under 160, cut at a sentence end where
// there is one, otherwise at a word with a closing "…".
export const TITLE_MAX = 65;
export const META_MAX = 158;

export function fitTitle(title: string | undefined): string | undefined {
  if (!title) return title;
  let t = title.trim();
  if (t.length <= TITLE_MAX) return t;
  t = t.replace(/ \| Jared Gibbons REALTOR®$/, ' | Jared Gibbons');
  while (t.length > TITLE_MAX) {
    const i = t.lastIndexOf(' | ');
    if (i < 25) break;
    t = t.slice(0, i);
  }
  return t;
}

export function fitMeta(desc: string | undefined): string | undefined {
  if (!desc) return desc;
  let d = desc.replace(/\s+/g, ' ').replace(/^\[SOLD\]:\s*/i, '').trim();
  if (d.length <= META_MAX) return d;
  const cut = d.slice(0, META_MAX);
  const end = Math.max(cut.lastIndexOf('. '), cut.lastIndexOf('! '), cut.lastIndexOf('? '));
  if (end >= 90) return cut.slice(0, end + 1);
  const sp = d.slice(0, META_MAX - 1).lastIndexOf(' ');
  return d.slice(0, sp).replace(/[\s,;:–—-]+$/, '') + '…';
}

// "27385 32 AVENUE" -> "27385 32 Avenue"; "12451 20TH AVENUE" -> "12451 20th Avenue"; NW/SW/NE/SE and unit letters stay upper
export function titleCaseAddress(s: string): string {
  return s.split(' ').map((w) => {
    if (!/[A-Z]{2,}/.test(w) || /[a-z]/.test(w)) return w;
    if (/^(NW|NE|SW|SE|N|S|E|W)$/.test(w)) return w;
    if (/^\d+(ST|ND|RD|TH)$/.test(w)) return w.toLowerCase();
    if (/\d/.test(w)) return w;
    return w.charAt(0) + w.slice(1).toLowerCase();
  }).join(' ');
}
