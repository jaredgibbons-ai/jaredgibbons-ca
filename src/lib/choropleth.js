// Shading for the neighbourhood hub map: each area is coloured by one of our own closed-sales figures (median price, price per sq ft, days on market).
// Figures come from src/data/sold/sold-12m.json (Paragon closed sales, grouped; raw rows are never stored). An area needs MIN_SALES closed sales of a
// property type before any figure is shown for it. Pure functions only: the Google Maps calls stay in src/components/AreaMap.astro.

export const MIN_SALES = 5;
export const TYPES = [['house', 'Houses'], ['condo', 'Condos'], ['townhome', 'Townhomes']];
export const METRICS = [['price', 'Median sold price'], ['ppsf', 'Median price per sq ft'], ['dom', 'Median days on market']];

export function fmt(metric, v) {
  if (v == null || !Number.isFinite(v)) return '';
  const n = Math.round(v).toLocaleString('en-CA');
  return metric === 'dom' ? `${n} days` : `$${n}`;
}

/** { house:{n,price,ppsf,dom}|null, condo:..., townhome:... } from one sold-12m sub-area entry. A type with fewer than MIN_SALES sales is null. */
export function figures(sub) {
  const out = {};
  for (const [g] of TYPES) {
    const x = sub && sub.groups && sub.groups[g];
    const ok = x && x.n >= MIN_SALES && [x.price, x.ppsf, x.dom].every((v) => Number.isFinite(v));
    out[g] = ok ? { n: x.n, price: x.price, ppsf: x.ppsf, dom: x.dom } : null;
  }
  return out;
}

/** Split the values into up to k groups with about the same number of areas in each. Returns { cuts, k, classOf(v) } with class 0 = lowest. */
export function classify(values, k = 5) {
  const v = values.filter(Number.isFinite).sort((a, b) => a - b);
  const distinct = new Set(v).size;
  const kk = Math.max(1, Math.min(k, distinct));
  const cuts = [];
  for (let i = 1; i < kk; i++) { const t = v[Math.floor((i * v.length) / kk)]; if (cuts.length === 0 || t > cuts[cuts.length - 1]) cuts.push(t); }
  const classOf = (x) => { let c = 0; for (const t of cuts) if (x >= t) c++; return c; };
  return { cuts, k: cuts.length + 1, classOf, min: v[0], max: v[v.length - 1] };
}

const lerp = (a, b, t) => Math.round(a + (b - a) * t);
const CREAM = [243, 237, 220], INK = [38, 38, 38];

/** Colour for class i of k: cream to near-black, so rank reads from lightness alone (works in greyscale and for colour-blind readers). */
export function rampColor(i, k) {
  const t = k <= 1 ? 0.5 : i / (k - 1);
  const [r, g, b] = [0, 1, 2].map((j) => lerp(CREAM[j], INK[j], t));
  return `rgb(${r},${g},${b})`;
}

export function luminance(rgb) {
  const [r, g, b] = rgb.match(/\d+/g).map(Number).map((c) => { const s = c / 255; return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4; });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}
export function contrast(a, b) { const [x, y] = [luminance(a), luminance(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); }
/** Label colour with at least 4.5:1 contrast on the given fill. */
export function textOn(fill) { return contrast(fill, 'rgb(17,17,17)') >= contrast(fill, 'rgb(255,255,255)') ? '#111111' : '#ffffff'; }

/** Legend rows: [{ color, from, to, label }] for the classes, using the metric's own formatting. */
export function legend(metric, cls) {
  const edges = [cls.min, ...cls.cuts, cls.max];
  return Array.from({ length: cls.k }, (_, i) => {
    const lo = edges[i], hi = edges[i + 1];
    return { color: rampColor(i, cls.k), from: lo, to: hi, label: cls.k === 1 ? fmt(metric, lo) : i === cls.k - 1 ? `${fmt(metric, lo)} and over` : i === 0 ? `Under ${fmt(metric, cls.cuts[0])}` : `${fmt(metric, lo)} to under ${fmt(metric, hi)}` };
  });
}

/** Short form for map labels: $1.96M, $785K, $489, 21 days. */
export function fmtShort(metric, v) {
  if (v == null || !Number.isFinite(v)) return '';
  if (metric !== 'price') return metric === 'dom' ? `${Math.round(v)} days` : `$${Math.round(v)}`;
  return v >= 1e6 ? `$${(v / 1e6).toFixed(2).replace(/0$/, '')}M` : `$${Math.round(v / 1000)}K`;
}
