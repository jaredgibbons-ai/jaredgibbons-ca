// Address -> zoning lookup for /zonings.html (D-285). GET /api/zoning?address=…
// 1) BC Address Geocoder (free, provincial) names the municipality and, when it knows the civic number, the parcel point.
// 2) When the province only matches to the block (common on acreages), the municipality's own address data finds the exact lot.
// 3) The municipality's public zoning, ALR and lot layers are asked what is at that point.
// Nothing is guessed: no exact address match -> no zone is shown, and the page offers to have Jared check it.
// Every source is a public open-data map service; no key, and the address is not stored.

const T = 'https://services5.arcgis.com/frpHL0Fv8koQRVWY/arcgis/rest/services';            // Township of Langley
const AB = 'https://services8.arcgis.com/ZYlQy38aWlfDG1Qh/arcgis/rest/services';           // City of Abbotsford
const SU = 'https://gisservices.surrey.ca/arcgis/rest/services';                           // City of Surrey
const LC = 'https://maps.langleycity.ca/server/rest/services/Maps/Open_Data/MapServer';    // City of Langley
const WR = 'https://maps.whiterockcity.ca/server/rest/services/opendata';                  // City of White Rock

// `guide` is the municipality's section id in the zoning guide (src/data/zonings.json), when it has one.
export const MUNIS = {
  'Surrey': { name: 'Surrey', guide: 'zd-surrey', zoning: `${SU}/Public/Planning/MapServer/18`, code: 'ZONING_TEXT', desc: 'ZONING', alr: `${SU}/Public/Planning/MapServer/0`, lot: `${SU}/Lots/MapServer/7`, map: 'https://cosmos.surrey.ca/' },
  'Township of Langley': { name: 'Township of Langley', guide: 'zd-langley', zoning: `${T}/Zoning/FeatureServer/0`, code: 'Zone', desc: 'ZoneCategory', alr: `${T}/OpenData_AgriculturalLandReserve/FeatureServer/0`, lot: `${T}/Parcels/FeatureServer/0`, map: 'https://www.tol.ca/en/services/geosource-maps.aspx' },
  'Langley': { name: 'City of Langley', guide: '', zoning: `${LC}/90`, code: 'ZONING', desc: '', alr: `${LC}/189`, lot: `${LC}/181`, map: 'https://www.langleycity.ca/' },
  'Abbotsford': { name: 'Abbotsford', guide: 'zd-abbotsford', zoning: `${AB}/Development_Layers_External_Feature/FeatureServer/45`, code: 'ZONING', desc: '', alr: `${AB}/Development_Layers_External_Feature/FeatureServer/1`, lot: `${AB}/Parcel_Layers_External_Feature/FeatureServer/0`, map: 'https://www.abbotsford.ca/' },
  'White Rock': { name: 'White Rock', guide: '', zoning: `${WR}/Zoning/MapServer/0`, code: 'ZONE_CODE', desc: 'ZONE_DESC', alr: '', lot: `${WR}/Parcel/MapServer/0`, map: 'https://www.whiterockcity.ca/' },
};

const json = (body, status = 200, cache = 'no-store') => new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': cache, 'x-content-type-options': 'nosniff' } });
const sql = (s) => String(s).replace(/'/g, "''").replace(/[%_\;]/g, '');

async function get(fetcher, url) {
  const r = await fetcher(url, { headers: { accept: 'application/json' }, signal: AbortSignal.timeout(9000) });
  if (!r.ok) throw new Error(`upstream ${r.status}`);
  const j = await r.json();
  if (j && j.error) throw new Error('upstream error');
  return j;
}
const at = (layer, [x, y], geom = false) => `${layer}/query?f=json&geometry=${x},${y}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=*&returnGeometry=${geom}${geom ? '&outSR=26910' : ''}`;

// Square metres of a polygon in UTM zone 10N (metres), holes subtracted (rings are signed).
export function ringArea(rings) {
  let a = 0;
  for (const r of rings || []) for (let i = 0; i < r.length - 1; i++) a += r[i][0] * r[i + 1][1] - r[i + 1][0] * r[i][1];
  return Math.abs(a / 2);
}

// The municipality's own address data, for when the province only knows the block. Returns [lng, lat] or null.
async function localPoint(fetcher, key, p) {
  const street = [p.streetName, p.streetType, p.streetDirection].filter(Boolean).join(' ');
  const line = `${p.civicNumber} ${street}`;
  if (key === 'Surrey' || key === 'Abbotsford') {
    const base = key === 'Surrey' ? `${SU}/Composite_Geocoder/GeocodeServer` : 'https://webgis.abbotsford.ca/arcgis/rest/services/NGWebMap/AddressPt_Locator/GeocodeServer';
    const j = await get(fetcher, `${base}/findAddressCandidates?f=json&SingleLine=${encodeURIComponent(line)}&outSR=4326&maxLocations=1`);
    const c = (j.candidates || [])[0];
    // Only an exact hit on the same civic number counts.
    return c && c.score >= 98 && String(c.address || '').startsWith(`${p.civicNumber} `) ? [c.location.x, c.location.y] : null;
  }
  if (key === 'Township of Langley') {
    const where = `HOUSE=${Number(p.civicNumber)} AND STREET LIKE '${sql(street).toUpperCase()}%'`;
    const j = await get(fetcher, `${T}/Parcels/FeatureServer/0/query?f=json&where=${encodeURIComponent(where)}&outFields=HOUSE,STREET&returnGeometry=false&returnCentroid=true&outSR=4326&resultRecordCount=3`);
    const f = (j.features || []).filter((x) => x.centroid);
    const streets = new Set(f.map((x) => x.attributes.STREET));
    return f.length && streets.size === 1 ? [f[0].centroid.x, f[0].centroid.y] : null;   // "40 AVE" must not also match "40A AVE"
  }
  return null;
}

export async function lookup(address, fetcher = fetch) {
  const q = String(address || '').replace(/\s+/g, ' ').trim();
  if (q.length < 5 || q.length > 120 || !/\d/.test(q)) return { status: 'bad' };
  const g = await get(fetcher, `https://geocoder.api.gov.bc.ca/addresses.json?addressString=${encodeURIComponent(q)}&maxResults=1&outputSRS=4326&locationDescriptor=parcelPoint&minScore=60&echo=false&brief=false&provinceCode=BC`);
  const f = (g.features || [])[0];
  const p = f && f.properties;
  if (!p || !p.civicNumber || !p.streetName) return { status: 'notfound' };
  const key = p.localityName;
  const m = MUNIS[key];
  const street = [p.streetName, p.streetType, p.streetDirection].filter(Boolean).join(' ');
  const shown = `${p.civicNumber}${p.civicNumberSuffix || ''} ${street}, ${m ? m.name : key}`;
  if (!m) return { status: 'unsupported', address: shown, locality: key };

  let pt = p.matchPrecision === 'CIVIC_NUMBER' ? f.geometry.coordinates : null;
  if (!pt) pt = await localPoint(fetcher, key, p).catch(() => null);
  if (!pt) return { status: 'notfound', address: shown, locality: m.name };

  const [z, a, l] = await Promise.all([
    get(fetcher, at(m.zoning, pt)),
    m.alr ? get(fetcher, at(m.alr, pt)).catch(() => null) : Promise.resolve({ features: [] }),
    m.lot ? get(fetcher, at(m.lot, pt, true)).catch(() => null) : Promise.resolve(null),
  ]);
  const seen = new Set();
  const zones = [];
  for (const x of z.features || []) {
    const code = String(x.attributes[m.code] || '').trim();
    if (!code || seen.has(code)) continue;
    seen.add(code);
    const zone = { code };
    const d = m.desc && String(x.attributes[m.desc] || '').trim();
    if (d) zone.name = d;
    const by = String(x.attributes.BY_LAW_01 || '').trim();   // Surrey: the CD bylaw number
    if (by) zone.bylaw = by;
    const link = String(x.attributes.WEBLINK || '');
    if (/^https:\/\/cosmos\.surrey\.ca\//.test(link)) zone.link = link;
    zones.push(zone);
  }
  if (!zones.length) return { status: 'nozone', address: shown, locality: m.name };
  const out = { status: 'ok', address: shown, locality: m.name, guide: m.guide, map: m.map, zones, alr: a ? (a.features || []).length > 0 : null };
  const lots = (l && l.features) || [];
  if (lots.length === 1 && lots[0].geometry) {
    const sqm = ringArea(lots[0].geometry.rings);
    if (sqm > 50 && sqm < 5e6) out.lot = { sqm: Math.round(sqm), sqft: Math.round(sqm * 10.7639), acres: Math.round((sqm / 4046.8564) * 100) / 100 };
  }
  return out;
}

export async function handleZoning(request, fetcher = fetch) {
  if (request.method !== 'GET') return json({ status: 'bad' }, 405);
  const address = new URL(request.url).searchParams.get('address') || '';
  try {
    const r = await lookup(address, fetcher);
    if (r.status === 'bad') return json(r, 400);
    // Zoning changes rarely: a found answer can sit in the browser and at the edge for a day.
    return json(r, 200, r.status === 'ok' ? 'public, max-age=86400' : 'no-store');
  } catch {
    return json({ status: 'error' }, 502);
  }
}
