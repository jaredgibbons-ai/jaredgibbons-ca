"""Draft outlines for the outer Abbotsford sub-areas (Bradner, Matsqui, Sumas Mountain, Sumas Prairie) -> ADDED to src/data/maps/abbotsford.json

Source: Jared's Paragon map search (FVREB sub-area layer), screenshots of 2026-11-05 (closeups/Abbotsford).  The five areas already in abbotsford.json (Abbotsford West, Central, Aberdeen,
Poplar, Abbotsford East) are not touched; the new ones give way to them.  Frames (pixels as in the screenshots):
  'a' = mosaic of Abbotsford-center-and-east-edges-1 (reference), Bradner-Matsqui-1 (shift -487,-266) and Sumas-Mountain-1 (shift +772,-251), 12.5 m per pixel, registered by SIFT matching;
  'b' = Bradner-MtLehman-Matsqui-2 (25 m per pixel; a 'b' pixel is half an 'a' pixel: a = 2b + (-1473,-821)), used for the river banks that run past the top of the 'a' frames;
  'p' = Sumas-Prairie-1 (native 1280 px screen), used for the south end of Sumas Prairie down to the US border.
Pixels become latitude and longitude through the fit already used for the five existing areas (tools/build_outlines.py: Paragon 6-Abbotsford/01-overview fitted to Google coordinates of Abbotsford
International Airport, Abbotsford Recreation Centre, Silverbrook Farm, Gurdwara Kalgidhar Darbar Sahib and Castle Fun Park, under 20 m): 'a' pixel -> 01-overview pixel = 0.66667 a + (88.7,99.3)
(436 SIFT inliers), 'p' pixel -> 01-overview pixel = p + (523.5,384.4) (203 inliers); the 'b' frame is chained through 'a'.  Because every frame is tied to the same fit the new outlines line up with the
existing five.  No fresh Google Maps landmark lookup was possible (Google Maps answered every request with a CAPTCHA), so there is no landmark residual of its own: the same pixels land about 40 m east and
10 m north of where the Chilliwack-region fit puts them, which is the cross-check made.  --check prints the clash report.
Edges read off the screenshots are good to about 100 m on straight roads and a block or two on river banks and bush edges.  Bradner is one outline: the screenshots print both BRADNER and
MT LEHMAN inside the same fill and show no line between them, so Mt Lehman has no polygon of its own here.  Sumas Prairie's east edge is the FVREB/CADREB board line.
  python3 -I tools/build_abbotsford_outer_outlines.py [--check]"""
import json, math, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
_A1 = -math.radians(0.0001687) / math.cos(math.radians(49.06556))
def ov_ll(x, y):                                                      # 6-Abbotsford/01-overview pixel -> lat, lng (the fit in tools/build_outlines.py, with Mercator latitude)
    return math.degrees(2 * math.atan(math.exp(merc(49.06556) + _A1 * (y - 372))) - math.pi / 2), -122.4273 + (x - 162) * 0.0002575
def a2ov(x, y): return x * 2 / 3 + 88.67, y * 2 / 3 + 99.30
def b2a(x, y): return 2 * x - 1473, 2 * y - 821
def to_ll(f, x, y):
    if f == 'b': x, y = b2a(x, y); f = 'a'
    ox, oy = a2ov(x, y) if f == 'a' else (x + 523.48, y + 384.37)
    la, lo = ov_ll(ox, oy); return round(la, 5), round(lo, 5)
def from_ll(f, la, lo):                                               # inverse, for overlays
    oy = (merc(la) - merc(49.06556)) / _A1 + 372; ox = (lo + 122.4273) / 0.0002575 + 162
    if f == 'p': return ox - 523.48, oy - 384.37
    x, y = (ox - 88.67) * 1.5, (oy - 99.30) * 1.5
    return ((x + 1473) / 2, (y + 821) / 2) if f == 'b' else (x, y)
def A(pts): return [('a', x, y) for x, y in pts]
def B(pts): return [('b', x, y) for x, y in pts]
def P(pts): return [('p', x, y) for x, y in pts]
# --- polygons -------------------------------------------------------------------------------------------------------------------------------------------------------------
# Bradner (with the MT LEHMAN label): west edge is 272 St (the Langley line), south edge Highway 1 and Downes Rd, north edge the Fraser River bank
BRADNER = [A([(-77, -266), (-77, 225), (7, 275), (114, 336), (193, 379), (243, 414), (300, 450), (371, 493), (377, 494), (377, 339), (502, 339), (502, 241), (519, 241), (519, 80), (498, 80),
              (498, -52), (473, -84), (444, -116), (409, -156), (380, -188), (351, -216), (326, -256), (309, -263), (305, -266)]),
           B([(697, 139), (725, 142), (748, 144), (775, 154), (800, 161), (821, 184), (839, 202), (862, 220), (880, 241), (894, 264), (895, 285), (697, 285)])]
# Matsqui: river line on the north (Mission BC | Matsqui), Bradner on the west, Downes Rd on the south, Sumas Mountain on the east
MATSQUI = [A([(498, -52), (530, -24), (573, 12), (609, 34), (644, 30), (694, 9), (730, -11), (759, -34), (794, -66), (830, -99), (866, -131), (901, -156), (937, -181), (980, -216),
              (1009, -238), (1051, -263), (1101, -291), (1143, -287), (1165, -275), (1182, -249), (1250, -202), (1314, -174), (1337, -163), (1337, 205), (1321, 209), (1300, 230),
              (1282, 246), (1250, 259), (1229, 262), (1207, 284), (1202, 301), (1175, 310), (1154, 298), (1136, 284), (1107, 276), (1079, 279), (1077, 339), (502, 339), (502, 241),
              (519, 241), (519, 80), (498, 80)])]
# Sumas Mountain: north edge the mid-river line, east edge the Highway 1 diagonal, tip at the Highway 1 / Sumas Mountain Rd corner
SUMAS_MTN = [A([(1337, -163), (1380, -165), (1431, -172), (1480, -186), (1527, -205), (1577, -228), (1647, -246), (1727, -259), (1827, -272), (1877, -271), (1927, -257), (1987, -241),
                (2027, -227), (2041, -221), (2033, -150), (2040, -100), (2042, -88), (2001, -33), (1972, 12), (1950, 63), (1920, 115), (1890, 175), (1874, 204), (1820, 258), (1737, 333),
                (1678, 392), (1620, 446), (1587, 475), (1528, 517), (1478, 550), (1435, 578), (1407, 539), (1397, 512), (1396, 484), (1399, 429), (1399, 379), (1403, 300), (1403, 207),
                (1337, 205)])]
# Sumas Prairie: Highway 1 diagonal on the north-west, the Abbotsford / Chilliwack board line on the east, the US border on the south
SUMAS_PRAIRIE = [A([(2025, -84), (2058, -40), (2092, 12), (2121, 52), (2132, 68), (2132, 484), (2174, 489)])
                 + P([(1014, 109), (972, 111), (972, 155), (927, 156), (927, 279), (841, 284), (841, 370), (328, 370), (328, 228), (345, 219), (345, 189), (384, 184), (412, 175), (444, 156),
                      (481, 128), (519, 100), (569, 69), (612, 38), (650, 6)])
                 + A([(1678, 392), (1737, 333), (1820, 258), (1874, 204), (1890, 175), (1920, 115), (1950, 63), (1972, 12), (2001, -33)])]
ROWS = [
 ('Abbotsford|Bradner', 'bradner', 'Bradner', BRADNER),
 ('Abbotsford|Matsqui', 'matsqui', 'Matsqui', MATSQUI),
 ('Abbotsford|Sumas Mountain', 'sumas-mountain', 'Sumas Mountain', SUMAS_MTN),
 ('Abbotsford|Sumas Prairie', 'sumas-prairie', 'Sumas Prairie', SUMAS_PRAIRIE),
]
# --- geometry -----------------------------------------------------------------------------------------------------------------------------------------------------------
LAT0, LNG0 = 49.05, -122.3
KX, KY = 111320 * math.cos(math.radians(LAT0)), 110574
def m_xy(la, lo): return ((lo - LNG0) * KX, (la - LAT0) * KY)
def ll_xy(x, y): return (round(LAT0 + y / KY, 5), round(LNG0 + x / KX, 5))
def poly_m(tagged):
    from shapely.geometry import Polygon
    g = Polygon([m_xy(*to_ll(f, x, y)) for f, x, y in tagged])
    return g if g.is_valid else g.buffer(0)
def build(rows, existing, pad=60):
    """rows give way to the existing neighbours and to earlier rows; gaps narrower than 2*pad next to them are closed.  Returns result list and a clash report (km2)."""
    from shapely.ops import unary_union
    done = []; out = []; report = []
    for key, slug, name, parts in rows:
        g = unary_union([poly_m(p) for p in parts]).buffer(25).buffer(-25)
        nb = unary_union(existing + done)
        over = g.intersection(nb).area
        fill = nb.union(g).buffer(pad).buffer(-pad).difference(nb.union(g)).intersection(g.buffer(2 * pad))
        report.append((slug, 'overlap', round(over / 1e6, 3), 'gap closed', round(fill.area / 1e6, 3)))
        g = g.union(fill).difference(nb).buffer(-8).buffer(8).simplify(8)
        done.append(g)
        geoms = [g] if g.geom_type == 'Polygon' else list(g.geoms)
        out.append((key, slug, name, [x for x in geoms if x.area > 2e4]))
    return out, report
def main():
    from shapely.geometry import Polygon
    path = os.path.join(ROOT, 'src/data/maps/abbotsford.json')
    sold = json.load(open(os.path.join(ROOT, 'src/data/sold/sold-12m.json')))['sub']
    data = json.load(open(path)); mine = {r[1] for r in ROWS}
    data['areas'] = [a for a in data['areas'] if a['id'] not in mine]        # idempotent: drop an earlier run of this script
    existing = [Polygon([m_xy(la, lo) for la, lo in r]).buffer(0) for a in data['areas'] for r in a['rings']]
    res, report = build(ROWS, existing)
    for key, slug, name, geoms in res:
        assert key in sold, key
        rings = []
        for g in geoms:
            r = [list(ll_xy(*c)) for c in list(g.exterior.coords)[:-1]]; r.append(r[0]); rings.append(r)
        data['areas'].append({'id': slug, 'name': name, 'href': f'/{slug}.html', 'status': 'draft', 'sold': key, 'rings': rings})
    pts = [p for a in data['areas'] for r in a['rings'] for p in r]; pad = 0.004
    data['bbox'] = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    data['center'] = {'lat': round((data['bbox'][0] + data['bbox'][2]) / 2, 4), 'lng': round((data['bbox'][1] + data['bbox'][3]) / 2, 4)}
    json.dump(data, open(path, 'w'), separators=(',', ':'))
    print('abbotsford', len(data['areas']), 'areas', data['bbox'])
    if '--check' in sys.argv:
        print('against the existing five and earlier rows:', report)
if __name__ == '__main__': main()
