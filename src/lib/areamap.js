// Pure helpers for the neighbourhood map (src/components/AreaMap.astro). The Google Maps calls live in the component; everything testable lives here.
// Data format: src/data/maps/<region>.json  { region, name, center:{lat,lng}, bbox:[south,west,north,east], areas:[{ id, name, group?, href, status:'draft'|'confirmed', rings:[[[lat,lng],...]] }] }
// Outlines are our own (drawn from boundary streets and public data), never copied from another site; each stays 'draft' until Jared confirms it.

export function validateRegion(r) {
  const errs = [];
  if (!r || typeof r !== 'object') return ['region is not an object'];
  for (const k of ['region', 'name']) if (!r[k]) errs.push(`missing ${k}`);
  const bb = r.bbox;
  if (!Array.isArray(bb) || bb.length !== 4) errs.push('bbox must be [south, west, north, east]');
  const ids = new Set();
  for (const a of r.areas || []) {
    const t = `area ${a.id || '?'}`;
    if (!a.id || !/^[a-z0-9-]+$/.test(a.id)) errs.push(`${t}: bad id`);
    if (ids.has(a.id)) errs.push(`${t}: duplicate id`); ids.add(a.id);
    if (!a.name) errs.push(`${t}: missing name`);
    if (!/^\/[a-z0-9-]+\.html$/.test(a.href || '')) errs.push(`${t}: href must look like /page.html`);
    if (!['draft', 'confirmed'].includes(a.status)) errs.push(`${t}: status must be draft or confirmed`);
    if (!Array.isArray(a.rings) || !a.rings.length) errs.push(`${t}: no rings`);
    for (const ring of a.rings || []) {
      if (!Array.isArray(ring) || ring.length < 4) { errs.push(`${t}: a ring needs at least 4 points (first = last)`); continue; }
      const f = ring[0], l = ring[ring.length - 1];
      if (f[0] !== l[0] || f[1] !== l[1]) errs.push(`${t}: ring is not closed`);
      for (const [la, ln] of ring) {
        if (!(Math.abs(la) <= 90 && Math.abs(ln) <= 180)) errs.push(`${t}: point out of range`);
        else if (Array.isArray(bb) && bb.length === 4 && (la < bb[0] || la > bb[2] || ln < bb[1] || ln > bb[3])) errs.push(`${t}: point ${la},${ln} is outside the region bbox`);
      }
    }
  }
  return errs;
}

/** Popup text, same pattern as the brief: "<Area> - <Region>" and one link; grouped areas say "MLS® sub-area group". */
export function popupSpec(area, regionName) {
  return { title: `${area.name} - ${regionName}`, linkText: area.group ? 'View the neighbourhood page for this MLS® sub-area group' : 'View the neighbourhood page for this area', href: area.href };
}

/** Area-weighted centroid of the largest ring, [lat, lng]. Used for the label. */
export function centroid(rings) {
  let best = null, bestA = -1;
  for (const ring of rings) {
    const oy = ring[0][0], ox = ring[0][1];   // work relative to the first point so large coordinates do not lose precision
    let a = 0, cx = 0, cy = 0;
    for (let i = 0; i < ring.length - 1; i++) {
      const y0 = ring[i][0] - oy, x0 = ring[i][1] - ox, y1 = ring[i + 1][0] - oy, x1 = ring[i + 1][1] - ox, f = x0 * y1 - x1 * y0;
      a += f; cx += (x0 + x1) * f; cy += (y0 + y1) * f;
    }
    a /= 2;
    if (Math.abs(a) > bestA) { bestA = Math.abs(a); best = a === 0 ? ring[0] : [oy + cy / (6 * a), ox + cx / (6 * a)]; }
  }
  return best;
}

export function boundsOf(areas) {
  let s = 90, w = 180, n = -90, e = -180;
  for (const a of areas) for (const ring of a.rings) for (const [la, ln] of ring) { s = Math.min(s, la); n = Math.max(n, la); w = Math.min(w, ln); e = Math.max(e, ln); }
  return { south: s, west: w, north: n, east: e };
}
