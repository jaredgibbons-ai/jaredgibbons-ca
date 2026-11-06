// Render-time structure upgrades for archive/local text blocks (data files are untouched).
// The archive and the guide generators flattened tables, label/value rows and "title + text" cards into runs of
// one-line paragraphs and one-cell lists. Left alone they read as a wall of words, so they are rebuilt here as
// real tables, stat cards, key/value cards and title cards. Every rule is strict: if the shape does not match
// exactly, the blocks are left as they were.

type Part = { t: string; h?: string; lead?: boolean };
type Block = any;

const text = (parts: Part[] = []) => parts.map((x) => x.t).join(' ').replace(/\s+/g, ' ').trim();
const bt = (b: Block) => (b?.t === 'p' ? text(b.parts) : '');
const hasLink = (parts: Part[] = []) => parts.some((x) => x.h);
const words = (s: string) => s.split(/\s+/).filter(Boolean).length;
const numLead = (s: string) => /^[~\-−+$€£]?\s*\d/.test(s.trim()) || /^(full|none|free)\b/i.test(s.trim());

// A short label: one text part, no link, up to 5 words / 34 characters, no sentence punctuation.
const labelLike = (parts: Part[]) => {
  if (!parts || parts.length !== 1 || parts[0].h) return false;
  const s = parts[0].t.trim();
  return s.length > 0 && s.length <= 34 && words(s) <= 5 && !/[.!?;]$/.test(s) && !/(^|\s)(the|a|an|of|and|to|in|for|with|or|our|my|your|this|that)$/i.test(s);
};

// ---- 1. Flat one-cell lists -> table or stat cards ----------------------------------------------------------------
function flatCells(b: Block): string[] | null {
  if (b?.t !== 'list' || !Array.isArray(b.items) || b.items.length < 4) return null;
  if (!b.items.every((it: Part[]) => it.length === 1 && !it[0].h && it[0].t.trim().length <= 60)) return null;
  return b.items.map((it: Part[]) => it[0].t.trim());
}

function asTable(cells: string[], caption: string): Block | null {
  const n = cells.length;
  const k = cells.findIndex(numLead);
  if (k < 2 || k > 6 || n % k !== 0 || n / k < 3) return null;
  const head = cells.slice(0, k);
  if (head.some(numLead) || head.some((h) => h.length > 34)) return null;
  const rows: string[][] = [];
  for (let r = 1; r < n / k; r++) rows.push(cells.slice(r * k, (r + 1) * k));
  // every body row must start with a figure, so a header row is never mistaken for a body row
  if (!rows.every((row) => numLead(row[0]))) return null;
  // the first column holds the figure the table is organised by, so it becomes the row header
  return { t: 'table', caption, head, rows, plain: true };
}

function asStats(cells: string[]): Block | null {
  if (cells.length < 4 || cells.length > 16 || cells.length % 2) return null;
  const vals = cells.filter((_, i) => i % 2 === 0), labs = cells.filter((_, i) => i % 2 === 1);
  if (vals.filter((v) => /\d/.test(v)).length / vals.length < 0.75) return null;
  if (!labs.every((l) => /[A-Za-z]{3}/.test(l) && l.length <= 44) || vals.some((v) => v.length > 18)) return null;
  return { t: 'stats', small: true, items: vals.map((v, i) => ({ label: labs[i], value: v })) };
}

function flatLists(bl: Block[]): Block[] {
  const out: Block[] = [];
  for (let i = 0; i < bl.length; i++) {
    const b = bl[i];
    const cells = flatCells(b);
    if (cells) {
      const prev = out[out.length - 1];
      const cap = prev?.t === 'h' && prev.level === 3 ? prev.text : '';
      const tbl = asTable(cells, cap);
      if (tbl) { if (cap) out.pop(); out.push(tbl); continue; }
      const st = asStats(cells);
      if (st) { out.push(st); continue; }
    }
    out.push(b);
  }
  return out;
}

// ---- 2. Label / value runs under a level-3 heading -> key/value cards ----------------------------------------------
// Scraped shape: [short kicker p] h3, then label, value, label, value ... as one-cell lists and paragraphs; the last
// odd label before the next h3 is that heading's kicker.
function tokensAfter(bl: Block[], from: number, split = false): { toks: Part[][]; end: number } {
  const toks: Part[][] = []; let j = from;
  while (j < bl.length && (bl[j].t === 'p' || bl[j].t === 'list') && !bl[j].cls) {
    if (bl[j].t === 'p') {
      const ps: Part[] = bl[j].parts || [];
      // a value and the next label sometimes arrive in one paragraph: ["Kindergarten to 7", "Note"]
      if (split && ps.length === 2 && !ps[0].h && !ps[1].h && labelLike([ps[1]]) && words(ps[1].t) <= 2 && !labelLike([ps[0]])) { toks.push([ps[0]], [ps[1]]); }
      else if (split && ps.length === 2 && !ps[0].h && !ps[1].h && labelLike([ps[1]]) && words(ps[1].t) <= 2) { toks.push([ps[0]], [ps[1]]); }
      else toks.push(ps);
    }
    else for (const it of bl[j].items) toks.push(it);
    j++;
  }
  return { toks, end: j };
}

function kvCards(bl: Block[]): Block[] {
  const out: Block[] = [];
  let kicker: Part[] | null = null; // pending kicker for the next h3
  for (let i = 0; i < bl.length; i++) {
    const b = bl[i];
    const isH3 = b.t === 'h' && b.level === 3 && !/\?\s*$/.test(b.text) && !b.href;
    if (!isH3) {
      // a short label paragraph right before an h3 is that card's kicker
      if (b.t === 'p' && !b.cls && labelLike(b.parts) && bl[i + 1]?.t === 'h' && bl[i + 1].level === 3) { kicker = b.parts; continue; }
      out.push(b); continue;
    }
    let toks: Part[][] = [], end = i + 1, next: Part[] | null = null, body: Part[][] = [], ok = false, trailing: Block | null = null;
    for (const split of [false, true]) {
      ({ toks, end } = tokensAfter(bl, i + 1, split));
      next = null; body = toks; trailing = null;
      if (toks.length % 2 === 1) {
        const last = toks[toks.length - 1];
        if (labelLike(last) && bl[end]?.t === 'h' && bl[end].level === 3) { next = last; body = toks.slice(0, -1); }
        else if (labelLike(last)) body = toks.slice(0, -1); // orphan label (it only repeated the next heading's topic)
        else if (bl[end - 1]?.t === 'p') { body = toks.slice(0, -1); trailing = bl[end - 1]; } // a closing note after the last row
      }
      ok = body.length >= 2 && body.length % 2 === 0;
      if (ok) for (let k = 0; k < body.length; k += 2) if (!labelLike(body[k]) || !body[k + 1]?.length) { ok = false; break; }
      if (ok) break;
    }
    const pairs = body.length / 2;
    if (!ok) {
      // shape does not match: keep the heading and everything under it exactly as it was
      if (kicker) { out.push({ t: 'p', parts: kicker }); kicker = null; }
      out.push(b);
      for (let k = i + 1; k < end; k++) out.push(bl[k]);
      i = end - 1; continue;
    }
    out.push({ t: 'kv', kicker: kicker ? text(kicker) : '', title: b.text, rows: Array.from({ length: pairs }, (_, k) => ({ l: text(body[2 * k]), v: body[2 * k + 1] })) });
    if (trailing) out.push(trailing);
    kicker = next; i = end - 1;
  }
  // group neighbours into one grid
  const grouped: Block[] = [];
  for (const b of out) {
    if (b.t === 'kv') { const p = grouped[grouped.length - 1]; if (p?.t === 'kvgrid') p.items.push(b); else grouped.push({ t: 'kvgrid', items: [b] }); }
    else grouped.push(b);
  }
  return grouped;
}

// ---- 3. "Label:" + bold lead runs -> one key/value card -------------------------------------------------------------
function colonRows(bl: Block[]): Block[] {
  const isRow = (b: Block) => b?.t === 'p' && !b.cls && b.parts?.length === 2 && /:$/.test(b.parts[0].t.trim()) && b.parts[0].t.trim().length <= 36 && words(b.parts[0].t) <= 4 && !b.parts[0].h;
  const out: Block[] = [];
  for (let i = 0; i < bl.length; i++) {
    if (isRow(bl[i])) {
      let j = i; while (j < bl.length && isRow(bl[j])) j++;
      if (j - i >= 3) {
        out.push({ t: 'kvgrid', items: [{ t: 'kv', kicker: '', title: '', rows: bl.slice(i, j).map((b) => ({ l: b.parts[0].t.trim().replace(/:$/, ''), v: [{ ...b.parts[1], lead: false }] })) }], wide: true });
        i = j - 1; continue;
      }
    }
    out.push(bl[i]);
  }
  return out;
}

// ---- 3b. "Label: text" paragraphs (one text part) under a heading -> one key/value card per heading ------------------
function inlineKv(bl: Block[]): Block[] {
  const re = /^([A-Z][A-Za-z0-9 &\/'’-]{2,26}):\s+(\S[\s\S]*)$/;
  const rowOf = (ps: Part[]) => { if (!ps?.length || ps[0].h) return null; const m = re.exec(ps[0].t.trim()); if (!m || words(m[1]) > 4) return null; return { l: m[1], v: [{ ...ps[0], t: m[2] }, ...ps.slice(1)] }; };
  // rows carried by one block: a paragraph is one row, a list is a run of rows (every item must match)
  const rowsOf = (b: Block): any[] | null => {
    if (b?.t === 'p' && !b.cls) { const r = rowOf(b.parts); return r ? [r] : null; }
    if (b?.t === 'list') { const rs = b.items.map((it: Part[]) => rowOf(it)); return rs.length && rs.every(Boolean) ? rs : null; }
    return null;
  };
  const out: Block[] = [];
  for (let i = 0; i < bl.length; i++) {
    const b = bl[i];
    const start = b.t === 'h' && b.level === 3 && !/\?\s*$/.test(b.text) ? i + 1 : rowsOf(b) ? i : -1;
    if (start >= 0) {
      const rows: any[] = []; let j = start;
      while (j < bl.length) { const r = rowsOf(bl[j]); if (!r) break; rows.push(...r); j++; }
      const labels = new Set(rows.map((r) => r.l.toLowerCase()));
      if (rows.length >= 3 && labels.size === rows.length) {
        out.push({ t: 'kvgrid', wide: true, items: [{ t: 'kv', kicker: '', title: b.t === 'h' ? b.text : '', rows }] });
        i = j - 1; continue;
      }
    }
    out.push(b);
  }
  return out;
}

// ---- 4. Runs of "short title / paragraph(s)" -> title cards ---------------------------------------------------------
function titleRuns(bl: Block[]): Block[] {
  const isTitle = (b: Block) => b?.t === 'p' && !b.cls && b.parts?.length === 1 && !b.parts[0].h && (() => { const s = b.parts[0].t.trim(); return s.length >= 3 && s.length <= 60 && words(s) <= 7 && !/[.!?:;,]$/.test(s); })();
  const isBody = (b: Block) => b?.t === 'p' && !b.cls && (text(b.parts).length >= 50 || hasLink(b.parts));
  const startsCard = (k: number) => isTitle(bl[k]) && isBody(bl[k + 1]);
  const out: Block[] = [];
  for (let i = 0; i < bl.length; i++) {
    if (startsCard(i)) {
      const items: { h: string; a: Block[] }[] = []; let j = i;
      while (startsCard(j)) {
        const a: Block[] = []; let k = j + 1;
        while (k < bl.length && (bl[k].t === 'p' || bl[k].t === 'list') && !startsCard(k) && isBodyish(bl[k])) a.push(bl[k++]);
        items.push({ h: bt(bl[j]), a }); j = k;
      }
      if (items.length >= 3) { out.push({ t: 'subs', items }); i = j - 1; continue; }
    }
    out.push(bl[i]);
  }
  function isBodyish(b: Block) { return b.t === 'list' || (b.t === 'p' && !b.cls); }
  return out;
}

// A section often ends with the next section's one-word topic label ("Schools", "Parks and recreation"), left over from the old card layout.
// It is dropped when it only repeats words of the next heading, or when it trails a list of links.
export function dropOrphans(bl: Block[], nextHeading = ''): Block[] {
  const sig = (x: string) => x.toLowerCase().split(/[^a-z]+/).filter((w) => w.length >= 4);
  const nh = new Set(sig(nextHeading));
  const out = bl.slice();
  const last = out[out.length - 1];
  if (last?.t === 'p' && !last.cls && labelLike(last.parts) && out.length >= 3 && (sig(text(last.parts)).some((w) => nh.has(w)) || (words(text(last.parts)) <= 4 && out[out.length - 2]?.t === 'p' && text(out[out.length - 2].parts).length >= 60))) out.pop();
  const l2 = out[out.length - 1];
  if (l2?.t === 'list' && l2.items.length >= 4) {
    const lastItem = l2.items[l2.items.length - 1];
    if (l2.items.slice(0, -1).every((it: Part[]) => it.length === 1 && it[0].h) && labelLike(lastItem) && sig(text(lastItem)).some((w) => nh.has(w) || true)) out[out.length - 1] = { ...l2, items: l2.items.slice(0, -1) };
  }
  return out;
}

// ---- 5. One list that alternates label / value ("Style", "Family-scale townhomes", "Location", "2955 156 Street") -> key/value card ----
function listKv(bl: Block[]): Block[] {
  return bl.map((b) => {
    if (b?.t !== 'list' || b.items.length < 6 || b.items.length > 40 || b.items.length % 2) return b;
    const its: Part[][] = b.items;
    const labs = its.filter((_, i) => i % 2 === 0), vals = its.filter((_, i) => i % 2 === 1);
    if (!labs.every((l) => labelLike(l) && words(text(l)) <= 3 && /^[A-Z]/.test(text(l)))) return b;
    if (new Set(labs.map((l) => text(l).toLowerCase())).size !== labs.length) return b;
    const avg = (xs: Part[][]) => xs.reduce((a, x) => a + text(x).length, 0) / xs.length;
    if (avg(vals) < 1.4 * avg(labs)) return b;
    return { t: 'kvgrid', wide: true, items: [{ t: 'kv', kicker: '', title: '', rows: labs.map((l, i) => ({ l: text(l), v: vals[i] })) }] };
  });
}

// Repeated "h3 + one or two short paragraphs with links" (neighbourhood and property-type directories) -> title cards.
function h3Cards(bl: Block[]): Block[] {
  const out: Block[] = [];
  const isH = (b: Block) => b?.t === 'h' && b.level === 3 && !/\?\s*$/.test(b.text || '') && !b.href;
  for (let i = 0; i < bl.length; i++) {
    if (isH(bl[i])) {
      const groups: { h: string; a: Block[] }[] = []; let j = i;
      while (isH(bl[j])) {
        const a: Block[] = []; let k = j + 1;
        while (k < bl.length && !isH(bl[k]) && bl[k].t === 'p' && !bl[k].cls && a.length < 3) a.push(bl[k++]);
        const len = a.reduce((n, x) => n + text(x.parts).length, 0);
        if (!a.length || len > 260 || !a.some((x) => hasLink(x.parts))) break;
        groups.push({ h: bl[j].text, a: a.map((x) => ({ ...x, parts: x.parts.map((q: Part, n: number) => (n === 0 ? { ...q, t: q.t.replace(/^[·•]\s*/, '') } : q)) })) }); j = k;
      }
      if (groups.length >= 4) { out.push({ t: 'subs', items: groups }); i = j - 1; continue; }
    }
    out.push(bl[i]);
  }
  return out;
}

// A label/value run that starts in a list and carries on in paragraphs (the value of one row landed in its own paragraph).
function streamKv(bl: Block[]): Block[] {
  const out: Block[] = [];
  const avg = (xs: Part[][]) => xs.reduce((a, x) => a + text(x).length, 0) / Math.max(xs.length, 1);
  for (let i = 0; i < bl.length; i++) {
    const b = bl[i];
    if (b?.t === 'list' && b.items.length >= 2 && labelLike(b.items[0]) && /^[A-Z]/.test(text(b.items[0]))) {
      const toks: Part[][] = []; let j = i;
      while (j < bl.length && (bl[j].t === 'list' || bl[j].t === 'p') && !bl[j].cls) { if (bl[j].t === 'p') toks.push(bl[j].parts || []); else toks.push(...bl[j].items); j++; }
      let body = toks;
      if (body.length % 2 === 1 && labelLike(body[body.length - 1])) body = body.slice(0, -1);
      const labs = body.filter((_, k) => k % 2 === 0), vals = body.filter((_, k) => k % 2 === 1);
      if (body.length >= 6 && body.length % 2 === 0 && labs.every((l) => labelLike(l) && words(text(l)) <= 3 && /^[A-Z]/.test(text(l)) && !l[0].h) && vals.every((v) => v.length) && new Set(labs.map((l) => text(l).toLowerCase())).size === labs.length && (avg(vals) >= 1.4 * avg(labs) || vals.filter((v) => /^\d+(\.\d+)?\s*(min|km|m)\b|drive|walk/i.test(text(v))).length / vals.length >= 0.75)) {
        out.push({ t: 'kvgrid', wide: true, items: [{ t: 'kv', kicker: '', title: '', rows: labs.map((l, k) => ({ l: text(l), v: vals[k] })) }] });
        i = j - 1; continue;
      }
    }
    out.push(b);
  }
  return out;
}

// The old site's breadcrumb trail was kept as text on some pages ("/ Maple Ridge Real Estate", "/", "Pitt Meadows Condos"); the page already has a real breadcrumb.
export function cleanArchive(bl: Block[]): Block[] {
  const out: Block[] = [];
  for (let i = 0; i < bl.length; i++) {
    const b = bl[i], n = bl[i + 1];
    if (b?.t === 'p' && b.parts?.[0]?.t.trim() === '/' && n?.t === 'list' && n.items?.[0]?.[0]?.t.trim() === '/') { i++; continue; }
    out.push(b);
  }
  return out;
}

// A link list that ends with one plain-text line (a tagline): the links stay a link list and the line becomes its own paragraph.
function splitTail(bl: Block[]): Block[] {
  return bl.flatMap((b) => {
    if (b?.t !== 'list' || b.items.length < 4) return [b];
    const it: Part[][] = b.items; const last = it[it.length - 1];
    if (it.slice(0, -1).every((x) => x.length === 1 && x[0].h) && last.every((x) => !x.h)) return [{ ...b, items: it.slice(0, -1) }, { t: 'p', parts: last }];
    return [b];
  });
}

export function upgradeBlocks(bl: Block[]): Block[] {
  let out = flatLists(splitTail(bl));
  out = inlineKv(out);
  out = kvCards(out);
  out = colonRows(out);
  out = streamKv(out);
  out = listKv(out);
  out = h3Cards(out);
  out = titleRuns(out);
  return out;
}
