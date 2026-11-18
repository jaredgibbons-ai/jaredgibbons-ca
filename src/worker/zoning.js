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
const MR = 'https://geoservices.mapleridge.ca/server/rest/services/DataCatalog';          // City of Maple Ridge
const DE = 'https://maps.delta.ca/arcgis/rest/services/DeltaMap';                          // City of Delta
const CH = 'https://maps.chilliwack.com/arcgis/rest/services/External';                    // City of Chilliwack
const MI = 'https://esri.mission.ca/ags/rest/services/Geocortex/Planning/MapServer';       // City of Mission
const BU = 'https://gis.burnaby.ca/arcgis/rest/services/OpenData';                              // City of Burnaby
const CQ = 'https://geodata.coquitlam.ca/arcgis/rest/services/DynamicServices';                // City of Coquitlam
const VA = 'https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/zoning-districts-and-labels';   // City of Vancouver (open data API, not a map server)
// The Province's ALR polygons, for a municipality whose own map service has no ALR layer (Mission).
const BC_ALR = 'https://delivery.maps.gov.bc.ca/arcgis/rest/services/whse/bcgw_pub_whse_legal_admin_boundaries/MapServer/23';

// `ocp` is the Official Community Plan land-use layer and its field; `flood` the city's mapped flood area (D-290). The Township publishes neither.
// `guide` is the municipality's section id in the zoning guide (src/data/zonings.json), when it has one.
export const MUNIS = {
  'Surrey': { name: 'Surrey', guide: 'zd-surrey', zoning: `${SU}/Public/Planning/MapServer/18`, code: 'ZONING_TEXT', desc: 'ZONING', alr: `${SU}/Public/Planning/MapServer/0`, lot: `${SU}/Lots/MapServer/7`, ocp: [`${SU}/Public/Planning/MapServer/14`, 'LAND_USE'], flood: `${SU}/Public/Planning/MapServer/4`, map: 'https://cosmos.surrey.ca/' },
  'Township of Langley': { name: 'Township of Langley', guide: 'zd-langley', zoning: `${T}/Zoning/FeatureServer/0`, code: 'Zone', desc: 'ZoneCategory', alr: `${T}/OpenData_AgriculturalLandReserve/FeatureServer/0`, lot: `${T}/Parcels/FeatureServer/0`, map: 'https://www.tol.ca/en/services/geosource-maps.aspx' },
  'Langley': { name: 'City of Langley', guide: 'zd-langleycity', zoning: `${LC}/90`, code: 'ZONING', desc: '', alr: `${LC}/189`, lot: `${LC}/181`, ocp: [`${LC}/191`, 'LANDUSE'], flood: `${LC}/163`, map: 'https://www.langleycity.ca/' },
  'Abbotsford': { name: 'Abbotsford', guide: 'zd-abbotsford', zoning: `${AB}/Development_Layers_External_Feature/FeatureServer/45`, code: 'ZONING', desc: '', alr: `${AB}/Development_Layers_External_Feature/FeatureServer/1`, lot: `${AB}/Parcel_Layers_External_Feature/FeatureServer/0`, ocp: [`${AB}/Development_Layers_External_Feature/FeatureServer/38`, 'Draft_OCP_LandUse'], flood: `${AB}/Development_Layers_External_Feature/FeatureServer/17`, map: 'https://www.abbotsford.ca/' },
  'Maple Ridge': { name: 'Maple Ridge', guide: 'zd-mapleridge', zoning: `${MR}/PlanningDevelopment/MapServer/6`, code: 'ZoningCode', desc: '', alr: `${MR}/PlanningDevelopment/MapServer/0`, lot: `${MR}/Property/MapServer/3`, ocp: [`${MR}/PlanningDevelopment/MapServer/4`, 'LandUseDescription'], map: 'https://www.mapleridge.ca/' },
  'Delta': { name: 'Delta', guide: 'zd-delta', zoning: `${DE}/Planning/MapServer/11`, code: 'ZONING', desc: 'ZONING_DESCRIPTION', link: 'ZONING_PDF', alr: `${DE}/Planning/MapServer/6`, lot: `${DE}/Property/MapServer/23`, map: 'https://www.delta.ca/' },
  'White Rock': { name: 'White Rock', guide: 'zd-whiterock', zoning: `${WR}/Zoning/MapServer/0`, code: 'ZONE_CODE', desc: 'ZONE_DESC', alr: '', lot: `${WR}/Parcel/MapServer/0`, ocp: [`${WR}/Landuse/MapServer/0`, 'OCP_Description'], flood: `${WR}/Flood_Plain_Areas/MapServer/0`, map: 'https://www.whiterockcity.ca/' },
  // Chilliwack (D-354): the map's ZONE field still holds codes from the 2001 bylaw; CalcField is the current Bylaw 5000 zone, the one printed on the city map.
  'Chilliwack': { name: 'Chilliwack', guide: 'zd-chilliwack', zoning: `${CH}/Dynamic_Zone/MapServer/3`, code: 'CalcField', desc: '', alr: `${CH}/Dynamic_ALR/MapServer/0`, lot: `${CH}/Dynamic_Parcels/MapServer/1`, ocp: [`${CH}/Dynamic_OCP2050/MapServer/3`, 'LandUse'], map: 'https://www.chilliwack.com/' },
  // Mission (D-354): no public parcel layer, so no lot size; ALR from the Province's layer.
  'Mission': { name: 'Mission', guide: 'zd-mission', zoning: `${MI}/2`, code: 'Zone_Class', desc: 'Zoning', alr: BC_ALR, lot: '', ocp: [`${MI}/24`, 'O2_Type_1'], map: 'https://www.mission.ca/' },
  // Vancouver, Burnaby and Coquitlam (D-355): ALR from the Province's layer. Vancouver's zoning comes from its open data API (`ods`).
  'Vancouver': { name: 'Vancouver', guide: 'zd-vancouver', zoning: VA, ods: true, code: 'zoning_district', desc: 'zoning_classification', alr: BC_ALR, lot: '', map: 'https://vancouver.ca/' },
  'Burnaby': { name: 'Burnaby', guide: '', zoning: `${BU}/OpenData1/MapServer/8`, code: 'ZONECODE', desc: '', alr: BC_ALR, lot: '', map: 'https://www.burnaby.ca/' },
  'Coquitlam': { name: 'Coquitlam', guide: 'zd-coquitlam', zoning: `${CQ}/Planning/MapServer/1`, code: 'ZONING', desc: '', alr: BC_ALR, lot: `${CQ}/Cadastral/MapServer/16`, map: 'https://www.coquitlam.ca/' },
};

const json = (body, status = 200, cache = 'no-store') => new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': cache, 'x-content-type-options': 'nosniff' } });
const sql = (s) => String(s).replace(/'/g, "''").replace(/[%_\;]/g, '');

// One retry: Surrey's map server now and then leaves a request hanging and answers the same one in 30 ms a moment later.
async function get(fetcher, url) {
  for (const ms of [3500, 6000]) {
    try {
      const r = await fetcher(url, { headers: { accept: 'application/json' }, signal: AbortSignal.timeout(ms) });
      if (!r.ok) throw new Error(`upstream ${r.status}`);
      const j = await r.json();
      if (j && j.error) throw new Error('upstream error');
      return j;
    } catch (e) { if (ms === 6000) throw e; }
  }
}
// ALR: count only. Asking Surrey's ALR layer for attributes times out (one very large polygon); a count answers in milliseconds.
const inAlr = (layer, [x, y]) => `${layer}/query?f=json&geometry=${x},${y}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnCountOnly=true`;
// An open data API (Vancouver) answers in its own shape; hand back the map-server shape the rest of the lookup reads.
async function zonesAt(fetcher, m, pt) {
  if (!m.ods) return get(fetcher, at(m.zoning, pt));
  const where = `intersects(geom, geom'POINT(${pt[0]} ${pt[1]})')`;
  const j = await get(fetcher, `${m.zoning}/records?limit=5&select=${m.code},${m.desc}&where=${encodeURIComponent(where)}`);
  return { features: (j.results || []).map((r) => ({ attributes: r })) };
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

  // UNIT: a suite in a building the province knows (102-3480 146A St); the point is the building's parcel.
  let pt = p.matchPrecision === 'CIVIC_NUMBER' || p.matchPrecision === 'UNIT' ? f.geometry.coordinates : null;
  if (!pt) pt = await localPoint(fetcher, key, p).catch(() => null);
  if (!pt) return { status: 'notfound', address: shown, locality: m.name };

  const [z, a, l, o, fl] = await Promise.all([
    zonesAt(fetcher, m, pt),
    m.alr ? get(fetcher, inAlr(m.alr, pt)).catch(() => null) : Promise.resolve({ count: 0 }),
    m.lot ? get(fetcher, at(m.lot, pt, true)).catch(() => null) : Promise.resolve(null),
    m.ocp ? get(fetcher, at(m.ocp[0], pt).replace('outFields=*', `outFields=${m.ocp[1]}`)).catch(() => null) : Promise.resolve(null),
    m.flood ? get(fetcher, inAlr(m.flood, pt)).catch(() => null) : Promise.resolve(null),
  ]);
  const seen = new Set();
  const zones = [];
  for (const x of z.features || []) {
    const code = String(x.attributes[m.code] || '').trim();
    if (!code || seen.has(code) || code === 'ROAD' || code === 'None') continue;
    seen.add(code);
    const zone = { code };
    const d = m.desc && String(x.attributes[m.desc] || '').trim();
    // Delta writes its zone names in capitals.
    if (d) zone.name = d === d.toUpperCase() ? d.toLowerCase().replace(/_/g, ' / ').replace(/\b[a-z]/g, (c) => c.toUpperCase()) : d;
    const by = String(x.attributes.BY_LAW_01 || '').trim();   // Surrey: the CD bylaw number
    if (by) zone.bylaw = by;
    const link = String(x.attributes[m.link || 'WEBLINK'] || '');
    if (/^https:\/\/(cosmos\.surrey\.ca|maps\.delta\.ca)\//.test(link)) zone.link = link;
    zones.push(zone);
  }
  if (!zones.length) return { status: 'nozone', address: shown, locality: m.name };
  const out = { status: 'ok', address: shown, locality: m.name, guide: m.guide, map: m.map, zones, alr: a && typeof a.count === 'number' ? a.count > 0 : null };
  const plan = [...new Set(((o && o.features) || []).map((x) => String(x.attributes[m.ocp[1]] || '').trim()).filter(Boolean))];
  if (plan.length) out.ocp = plan.join(' / ').slice(0, 120);
  if (fl && typeof fl.count === 'number') out.flood = fl.count > 0;
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
