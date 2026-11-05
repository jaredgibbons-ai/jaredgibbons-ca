"""Draft outlines for the Mission (FVREB) sub-areas -> src/data/maps/mission.json

Source: Jared's Paragon map search (FVREB sub-area layer), four screenshots of 2026-11-05 (closeups/Mission).  Two zoom levels:
  'h' = Hatzic-1.jpg + Durieu-1.jpg (12.5 m per pixel; Durieu-1 is Hatzic-1 panned north, registered with shift (-5,-445), mosaic pixels = Hatzic-1 pixels),
  'd' = Dewdney-Deroche-2.jpg + Mission-overview-1.jpg (25 m per pixel; the overview is the same view panned west, shift (-452,142), mosaic pixels = Dewdney-Deroche-2 pixels).
Both were registered by SIFT feature matching (a 'd' pixel is 2.0 'h' pixels: h = 2d + (-56,-1063)).  Pixels become latitude and longitude through the same Web Mercator
fit that tools/build_chilliwack_outlines.py made from ten Google Maps landmarks (Chilliwack General Hospital ... Mt Woodside Launch; 27 m worst miss), reached by registering the 'd' frame
to the Chilliwack-region frames 03, 04, 05 and 08 (frame-02 pixel = 2.0 d + (-2248,-874); the four frames agree to 7 px, 90 m).  Check on that route: registering the same frames to the Abbotsford
screenshots (the 01-overview fit in tools/build_outlines.py, landmark fit under 20 m) puts every point within 17 m north and 38 m east of the Chilliwack route, and six OSM place nodes
(Hatzic, Durieu, Steelhead, Stave Falls, Deroche, Lake Errock) sit 0 to 360 m from their Google place labels, the labels being printed just below their nodes.  No Google Maps landmark could be
looked up for this job (Google Maps answered every lookup with a CAPTCHA), so there is no landmark residual of its own; --check prints a few converted points and the clash report.
Edges read off the screenshots are good to about 100 m on straight roads and a block or two on river banks and bush edges.
Areas that run past the top of the screenshots (Stave Falls, Steelhead, Durieu, Dewdney Deroche) are cut at the top of the 'd' frame (about 49.28 N), not at their true northern limit.
Dewdney Deroche is not cut on the east: it ends in a point below Lake Errock (the Lake Errock outline in agassiz-harrison.json) where the Fraser River takes over.
Not drawn: Hemlock (Hemlock Valley is far north of this frame, off screen).  Lake Errock is not redrawn (it lives in agassiz-harrison.json); Dewdney Deroche follows the Paragon line instead of giving way to it,
so it overlaps the existing Lake Errock outline by about 8 km2 (that outline runs about 500 m too far south along Highway 7 and squares off the south-west tip).
Every area stays 'draft'.   python3 -I tools/build_mission_outlines.py [--check]"""
import json, math, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
# --- Chilliwack fit (landmarks in frame-02 pixels, copied from tools/build_chilliwack_outlines.py)
LAND = [(875, 496, 49.166781, -121.9636126), (754, 287, 49.1906958, -121.9844822), (2279, 197, 49.2006216, -121.7226286), (2219, -269, 49.252988, -121.7330237),
        (1719, -366, 49.2637651, -121.8186462), (812, 1308, 49.0757817, -121.9743913), (1875, 657, 49.1489739, -121.7920615), (288, 814, 49.1312537, -122.0645375),
        (1866, 1288, 49.0779408, -121.7936216), (1319, -187, 49.2436064, -121.8874496)]
def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
def ls(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n; a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); return a, my - a * mx
LX, LB = ls([p[0] for p in LAND], [p[3] for p in LAND]); MY, MB = ls([p[1] for p in LAND], [merc(p[2]) for p in LAND])
def f02_ll(px, py): return math.degrees(2 * math.atan(math.exp(MY * py + MB)) - math.pi / 2), LX * px + LB
def d2f02(x, y): return 2.0 * x - 2248, 2.0 * y - 874          # Dewdney-Deroche-2 mosaic pixel -> Chilliwack frame-02 pixel
def h2d(x, y): return 0.5 * x + 28.2, 0.5 * y + 531.8          # Hatzic-1 mosaic pixel -> Dewdney-Deroche-2 mosaic pixel
def to_ll(frame, x, y):
    if frame == 'h': x, y = h2d(x, y)
    la, lo = f02_ll(*d2f02(x, y)); return round(la, 5), round(lo, 5)
def from_ll(frame, la, lo):                                     # inverse, for overlays
    py = (merc(la) - MB) / MY; px = (lo - LB) / LX; x, y = (px + 2248) / 2.0, (py + 874) / 2.0
    return ((x - 28.2) * 2, (y - 531.8) * 2) if frame == 'h' else (x, y)
def H(pts): return [('h', x, y) for x, y in pts]
def D(pts): return [('d', x, y) for x, y in pts]
# --- polygons -------------------------------------------------------------------------------------------------------------------------------------------------------------
# Hatzic-1 mosaic pixels ('h')
L_RIVER_EAST = [(1592, 639), (1575, 635), (1550, 620), (1517, 602), (1475, 581), (1442, 558), (1404, 527)]     # mid-river line, Dewdney (north) | Matsqui (south)
HATZIC = H([(1281, 236), (1516, 236), (1525, 267), (1534, 317), (1528, 333), (1537, 358), (1511, 380), (1519, 405), (1528, 427), (1544, 455), (1545, 492), (1542, 510), (1508, 520),
            (1467, 516), (1433, 506), (1408, 527), (1371, 513), (1337, 512), (1300, 533), (1267, 560), (1267, 243)])
MISSION_BC = H([(886, 99), (1280, 99), (1280, 236), (1268, 243), (1267, 560), (1234, 585), (1191, 620), (1155, 645), (1120, 670), (1084, 702), (1048, 735), (1013, 767), (984, 790), (948, 810),
                (898, 831), (863, 835), (827, 813), (784, 777), (748, 752), (727, 717), (698, 685), (663, 645), (634, 613), (619, 606), (654, 614), (713, 623), (763, 636), (763, 568),
                (759, 556), (780, 523), (791, 490), (797, 462), (813, 440), (825, 419), (886, 416)])
MISSION_WEST = H([(782, -119), (781, 190), (886, 190), (886, 416), (825, 419), (813, 440), (797, 462), (791, 490), (780, 523), (759, 556), (763, 568), (763, 636), (713, 623), (654, 614),
                  (619, 606), (601, 577), (578, 529), (560, 500), (536, 462), (501, 429), (448, 371), (395, 326), (380, 312), (382, 300), (382, 218), (386, 214), (401, 190), (425, 161),
                  (448, 137), (454, 108), (463, 90), (481, 73), (519, 61), (545, 66), (578, 64), (598, 73), (619, 61), (619, 46), (634, 31), (636, 8), (648, -10), (660, -26), (678, -30),
                  (713, -51), (736, -71), (760, -86)])
STAVE_H = H([(382, -245), (833, -245), (831, -221), (825, -186), (807, -160), (795, -139), (782, -119), (760, -86), (736, -71), (713, -51), (678, -30), (660, -26), (648, -10), (636, 8),
             (634, 31), (619, 46), (619, 61), (598, 73), (578, 64), (545, 66), (519, 61), (481, 73), (463, 90), (454, 108), (448, 137), (425, 161), (401, 190), (386, 214), (382, 218)])
STEEL_H = H([(833, -245), (831, -221), (825, -186), (807, -160), (795, -139), (782, -119), (781, 190), (886, 190), (886, 99), (1280, 99), (1278, -245)])
DURIEU_H = H([(1278, -245), (1553, -245), (1556, -212), (1547, -176), (1522, -137), (1503, -109), (1500, -87), (1522, -45), (1525, -12), (1522, 22), (1514, 55), (1503, 99), (1500, 133),
              (1508, 166), (1522, 194), (1522, 216), (1517, 227), (1514, 238), (1281, 238)])
# Dewdney-Deroche-2 mosaic pixels ('d'): the parts that run north of the Hatzic-1 frame, and Dewdney Deroche itself
STAVE_D = D([(263, 200), (458, 200), (441, 239), (427, 289), (430, 342), (441, 373), (437, 417), (427, 439), (423, 467), (222, 467), (222, 259), (263, 259)])
STEEL_D = D([(458, 200), (657, 200), (657, 258), (668, 258), (668, 467), (423, 467), (427, 439), (437, 417), (441, 373), (430, 342), (427, 289), (441, 239)])
DURIEU_D = D([(657, 200), (792, 200), (792, 252), (822, 285), (823, 300), (824, 327), (822, 373), (816, 400), (807, 417), (806, 433), (800, 450), (800, 467), (668, 467), (668, 258), (657, 258)])
DEWDNEY = (D([(792, 200), (1419, 200), (1406, 220), (1397, 236), (1350, 261), (1312, 273), (1281, 289), (1275, 320), (1259, 357), (1247, 376), (1253, 389), (1219, 411), (1187, 417),
              (1178, 436), (1144, 457), (1134, 483), (1112, 504), (1087, 550), (1275, 554), (1278, 582), (1312, 561), (1350, 539), (1387, 523), (1419, 500), (1450, 514), (1459, 520),
              (1500, 513), (1544, 507), (1512, 536), (1487, 557), (1462, 576), (1425, 606), (1387, 637), (1367, 653), (1360, 693), (1333, 727), (1307, 747), (1273, 765), (1247, 760),
              (1193, 763), (1140, 783), (1100, 797), (1060, 797), (1000, 803), (940, 817), (880, 830)])
           + H(L_RIVER_EAST + [(1433, 506), (1467, 516), (1508, 520), (1542, 510), (1545, 492), (1544, 455), (1528, 427), (1519, 405), (1511, 380), (1537, 358), (1528, 333), (1534, 317),
                               (1525, 267), (1516, 236), (1514, 238), (1517, 227), (1522, 216), (1522, 194), (1508, 166), (1500, 133), (1503, 99), (1514, 55), (1522, 22), (1525, -12),
                               (1522, -45), (1500, -87), (1503, -109), (1522, -137), (1547, -176), (1556, -212)])
           + D([(816, 400), (822, 373), (824, 327), (823, 300), (822, 285), (792, 252)]))
# (sold key, page slug, name, [parts]); parts of one area are unioned.  Earlier rows keep their ground where hand-read edges overlap.
ROWS = [
 ('Mission|Hatzic', 'hatzic', 'Hatzic', [HATZIC]),
 ('Mission|Mission BC', 'mission-bc', 'Mission BC', [MISSION_BC]),
 ('Mission|Mission-West', 'mission-west', 'Mission West', [MISSION_WEST]),
 ('Mission|Stave Falls', 'stave-falls', 'Stave Falls', [STAVE_H, STAVE_D]),
 ('Mission|Steelhead', 'steelhead', 'Steelhead', [STEEL_H, STEEL_D]),
 ('Mission|Durieu', 'durieu', 'Durieu', [DURIEU_H, DURIEU_D]),
 ('Mission|Dewdney Deroche', 'dewdney-deroche', 'Dewdney Deroche', [DEWDNEY]),
]
# --- geometry -----------------------------------------------------------------------------------------------------------------------------------------------------------
LAT0, LNG0 = 49.17, -122.2
KX, KY = 111320 * math.cos(math.radians(LAT0)), 110574          # metres per degree
def m_xy(la, lo): return ((lo - LNG0) * KX, (la - LAT0) * KY)
def ll_xy(x, y): return (round(LAT0 + y / KY, 5), round(LNG0 + x / KX, 5))
def poly_m(tagged):
    from shapely.geometry import Polygon
    g = Polygon([m_xy(*to_ll(f, x, y)) for f, x, y in tagged])
    return g if g.is_valid else g.buffer(0)
def build(rows, others, pad=60):
    """rows give way to 'others' (existing neighbours, metric polygons) and to earlier rows; gaps narrower than 2*pad against neighbours are closed.  Returns result list and a clash report."""
    from shapely.ops import unary_union
    done = []; out = []; report = []
    for key, slug, name, parts in rows:
        g = unary_union([poly_m(p) for p in parts]).buffer(25).buffer(-25)        # union of the frames' parts, small spikes closed
        nb = unary_union(done + others)
        if not nb.is_empty:
            over = g.intersection(nb).area
            gap = nb.union(g).buffer(pad).buffer(-pad).difference(nb.union(g)).intersection(g.buffer(2 * pad)).area
            report.append((slug, round(over / 1e6, 3), round(gap / 1e6, 3)))
            g = g.union(nb.union(g).buffer(pad).buffer(-pad).difference(nb.union(g)).intersection(g.buffer(2 * pad)))   # take up the narrow gaps
            g = g.difference(nb)
        g = g.buffer(-8).buffer(8).simplify(8)
        done.append(g)
        geoms = [g] if g.geom_type == 'Polygon' else list(g.geoms)
        out.append((key, slug, name, [x for x in geoms if x.area > 2e4]))
    return out, report
def main():
    from shapely.geometry import Polygon
    sold = json.load(open(os.path.join(ROOT, 'src/data/sold/sold-12m.json')))['sub']
    if '--check' in sys.argv:
        for (x, y) in [(700, 500), (1000, 800), (1267, 836), (1783, 337), (1018, 909), (1500, 600)]:
            print('d', (x, y), to_ll('d', x, y))
    others = []
    ah = os.path.join(ROOT, 'src/data/maps/agassiz-harrison.json')
    if os.path.exists(ah):
        for a in json.load(open(ah))['areas']:
            if a['id'] == 'lake-errock':
                for r in a['rings']: others.append(Polygon([m_xy(la, lo) for la, lo in r]).buffer(0))
    res, report = build(ROWS, [])
    if others:   # Lake Errock (drawn earlier, D-120, from the Chilliwack frame 08) is kept as it is; Dewdney Deroche gives way where the two overlap (about 8 km2)
        from shapely.ops import unary_union as _u
        le0 = _u(others); res = [(k, sl, n, [x for g in gs for x in ([g.difference(le0)] if sl == 'dewdney-deroche' else [g]) for x in (list(x.geoms) if x.geom_type == 'MultiPolygon' else [x]) if not x.is_empty]) for k, sl, n, gs in res]
    areas = []; pts = []
    for key, slug, name, geoms in res:
        assert key in sold, key
        rings = []
        for g in geoms:
            r = [ll_xy(*c) for c in list(g.exterior.coords)[:-1]]; r = [list(p) for p in r]; r.append(r[0]); rings.append(r); pts += r
        areas.append({'id': slug, 'name': name, 'href': f'/{slug}.html', 'status': 'draft', 'sold': key, 'rings': rings})
    pad = 0.004; bbox = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    out = {'region': 'mission', 'name': 'Mission', 'center': {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}, 'bbox': bbox, 'areas': areas}
    json.dump(out, open(os.path.join(ROOT, 'src/data/maps/mission.json'), 'w'), separators=(',', ':'))
    print('mission', len(areas), 'areas', bbox)
    if '--check' in sys.argv:
        print('overlap km2 / narrow gap closed km2 against earlier areas:', report)
        from shapely.ops import unary_union
        le = unary_union(others)
        for key, slug, name, geoms in res: print(slug, 'overlaps the existing Lake Errock outline by', round(unary_union(geoms).intersection(le).area / 1e6, 2), 'km2')
if __name__ == '__main__': main()
