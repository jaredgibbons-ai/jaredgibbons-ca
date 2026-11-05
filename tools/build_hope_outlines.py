"""Draft outlines for Hope and Area -> src/data/maps/hope.json, plus Harrison Lake added (additively) to src/data/maps/agassiz-harrison.json

Source: Jared's Paragon map search (CADREB SUBAREAS layer, labels on), five close-ups of 2026-11-05 (05 Hope wide, 06 Hope town and Kawkawa Lake, 07 Sunshine Valley, 07b Laidlaw,
08 Harrison Lake wide), 1920x878 px with Paragon's toolbar (top 37 px) and Google footer (bottom 10 px) cut off.
Edges: Paragon draws every sub-area outline in one flat grey-purple (RGB 173,161,173).  Each polygon was found by flood-filling inside that outline colour on the screenshot
(extraction done in scratch; the resulting corner lists are the ring lists below, in frame pixels, reduced to a 2 px tolerance), so edges are good to 1 to 2 px of the frame
they came from.  Frames 06 and 07b are the same zoom (registered by feature matching, 07b + (-1179, 363) = 06; about 12.45 m per px); frame 07 is also 12.45 m per px but sits
east of them, so it has its own fit; frame 05 is 24.9 m per px; frame 08 is 99.8 m per px.
Calibration: Web Mercator fit per frame to Google Maps landmark coordinates read from Google Maps place pages (peaks, recreation sites, falls, FVRD airpark).  Google draws these
icons as pins whose tip is the true point, 16.5 px below the disc centre, so the tip is what is fitted.  Residuals (m north, m east): frame 06+07b 11 m worst (8 landmarks),
frame 07 8 m (8), frame 05 44 m (5), frame 08 18 m (6); `--check` prints them.  Dropped: Cascade Recreation Area (frame 07, the Google place is elsewhere), Mt Outram in the
frame-08 fit (66 m off, the icon sits on dark fill) but kept in frame 07.  Not fitted for lack of coordinates: Rainbow Falls, Garnet Creek Falls, First Blood trail, Wells Peak, Mt Dewdney.
Combining: Laidlaw (07b), Kawkawa Lake (06) and Sunshine Valley (07, with its top from frame 05) come from the sharpest frame that shows them whole.  Hope is frames 05 and 07b (its west,
north and north-east edges, and its west edge below Laidlaw) joined to frame 08 (its east and south edges; 99.8 m per px, so those edges are good to about 150 m).  Harrison Lake is frame 08 (the lake, 99.8 m per px)
with frames 05 and 07b for its south-east edge.  Where two frames overlap the later one is unioned in with a 300 m band; seams are closed with a small buffer.
Clipped on purpose, because the screenshots stop there: Hope's south end (frame 08 cuts it off at 49.149 N; the polygon continues south).
Hope is drawn as one solid outline; Kawkawa Lake and Sunshine Valley sit inside it and are drawn after it (Paragon's own Hope polygon has them as holes joined by a thin slit).
Laidlaw keeps its ground where it touches Hope; Harrison Lake gives way to the existing Agassiz and Harrison Hot Springs outlines.  Every area stays 'draft'.
Not drawn: Yale-Dogwood Valley, Fraser Canyon (out of scope), Harrison Hot Springs (already in agassiz-harrison.json).
  python3 -I tools/build_hope_outlines.py [--check]"""
import json, math, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
T = 16.5   # pin tip below the icon disc centre, in px
# landmarks: (name, px, py of disc centre, lat, lng) -- Google Maps place pages
F08 = [('Mt Breakenridge', 828.5, 215.3, 49.7197222, -121.9338888), ('Robertson Peak', 598.6, 298.3, 49.6461111, -122.2502777), ('Mt Clarke', 705.6, 425.3, 49.5330555, -122.1027777),
       ('Mt Robie Reid', 521.7, 539.3, 49.4316666, -122.3558333), ('Mt Judge Howay', 546.6, 454.3, 49.5072222, -122.3216666), ('Coquitlam Mountain', 266.5, 582.3, 49.3930555, -122.7069445)]
F07 = [('Mt Manson', 1093.5, 130.3, 49.3066666, -121.1733333), ('Johnson Peak', 904.6, 214.4, 49.2972222, -121.2058333), ('Mt Outram', 1181.6, 281.3, 49.2897222, -121.1583333),
       ('Mt Coulter', 336.6, 294.3, 49.2883333, -121.3033333), ('Mt Potter', 569.6, 443.4, 49.2716666, -121.2633333), ('Mt Ford', 1682.5, 616.3, 49.2522222, -121.0722222),
       ('West Gate Entrance Manning Park', 1000.5, 592.7, 49.2549696, -121.1894127), ('Eaton Peak', 83.5, 814.5, 49.23, -121.3466665)]
F05 = [('Mt McNair', 454.6, 124.3, 49.4666666, -121.6619445), ('Bear Creek Rec Site East Harrison', 155.5, 125.6, 49.4662474, -121.7645216),
       ('Cascade Peninsula Rec Site', 117.5, 249.6, 49.4386847, -121.7777086), ('FH Barber Provincial Park', 539.6, 812.5, 49.3135389, -121.6335111), ('MacLeod Peak', 1761.6, 750.3, 49.3266666, -121.2133333)]
SH = (-1179, 363)   # frame 07b pixel + SH = frame 06 pixel
F06 = [('Hope Mountain', 928.6, 597.3, 49.3475, -121.4177777), ('Mt Jarvis', 1737.6, 117.3, 49.4011111, -121.2788888), ('Flood Falls', 327, 497, 49.3586296, -121.5211495),
       ('FVRD Airpark CYHE', 481, 397, 49.369905, -121.4946541), ('Silver Peak (07b)', 1848.6 + SH[0], 621.3 + SH[1], 49.3041666, -121.4622222),
       ('Isolillock Peak (07b)', 1788.5 + SH[0], 663.3 + SH[1], 49.2994444, -121.4725001), ('Hunter Peak (07b)', 1586.7 + SH[0], 730.4 + SH[1], 49.2919444, -121.5072222),
       ('FH Barber Provincial Park (07b)', 850.6 + SH[0], 538.6 + SH[1], 49.3135389, -121.6335111)]
# polygon corners in frame pixels (flood-filled inside Paragon's outline colour)
KAWKAWA = [(966, 228), (964, 237), (970, 241), (967, 246), (962, 246), (963, 261), (954, 271), (954, 277), (970, 293), (975, 313), (989, 318), (1013, 318), (1032, 312), (1036, 308), (1044, 309), (1050, 306), (1059, 306), (1068, 311), (1095, 311), (1117, 307), (1116, 238), (1086, 238), (1083, 235), (1081, 220), (1036, 215), (1012, 208), (990, 210), (978, 216)]
LAIDLAW = [(1429, 90), (1338, 92), (1247, 106), (1201, 131), (1128, 156), (1110, 170), (1060, 188), (1015, 222), (966, 287), (936, 333), (897, 442), (892, 470), (877, 494), (864, 507), (834, 527), (755, 531), (718, 524), (692, 527), (656, 550), (627, 600), (613, 638), (596, 651), (583, 680), (589, 759), (607, 755), (638, 733), (677, 733), (697, 722), (910, 723), (1490, 718), (1490, 540), (1487, 480), (1491, 430), (1493, 212), (1423, 211)]
SV07 = [(467, 37), (478, 75), (533, 199), (556, 242), (575, 267), (570, 296), (595, 297), (703, 423), (710, 510), (727, 505), (769, 485), (804, 501), (857, 535), (950, 580), (957, 580), (982, 565), (982, 559), (941, 540), (870, 500), (752, 383), (645, 265), (623, 226), (571, 107), (536, 37)]
SV05 = [(1564, 797), (1568, 814), (1587, 859), (1624, 859), (1622, 849), (1597, 797)]
HOPE05 = [(1843, 38), (1658, 37), (1656, 58), (1645, 78), (1644, 96), (1639, 104), (1637, 127), (1631, 140), (1631, 147), (1638, 154), (1624, 174), (1623, 187), (1568, 252), (1518, 258), (1090, 255), (826, 259), (827, 599), (824, 653), (859, 654), (856, 782), (858, 867), (1919, 867), (1919, 149), (1858, 83)]
HOPE08 = [(1371, 480), (1355, 485), (1332, 485), (1325, 499), (1320, 526), (1305, 544), (1120, 546), (1120, 643), (1129, 644), (1128, 754), (1131, 829), (1194, 828), (1210, 840), (1222, 861), (1226, 862), (1225, 867), (1502, 867), (1501, 822), (1486, 789), (1475, 698), (1446, 575), (1377, 501)]
HOPE07B = [(1430, 37), (1430, 96), (1424, 212), (1494, 212), (1492, 416), (1488, 473), (1491, 553), (1488, 867), (1919, 867), (1919, 37)]
HL08 = [(619, 172), (619, 179), (626, 189), (655, 200), (671, 212), (681, 215), (694, 227), (712, 251), (749, 271), (761, 284), (783, 299), (790, 315), (833, 377), (852, 428), (858, 434), (873, 440), (872, 455), (878, 466), (890, 509), (897, 522), (902, 545), (901, 586), (911, 646), (924, 666), (928, 692), (936, 696), (947, 691), (949, 702), (952, 703), (952, 720), (958, 721), (966, 712), (987, 668), (1036, 667), (1035, 615), (1014, 611), (1012, 583), (1007, 177)]
HL05 = [(0, 37), (0, 679), (7, 694), (39, 736), (58, 792), (48, 827), (56, 841), (74, 861), (92, 865), (96, 858), (115, 857), (119, 865), (128, 864), (127, 845), (135, 844), (142, 847), (142, 867), (237, 867), (289, 750), (490, 748), (489, 538), (405, 528), (392, 293), (390, 37)]
HL07B = [(0, 37), (0, 620), (13, 621), (15, 636), (32, 632), (30, 594), (32, 592), (60, 596), (62, 675), (85, 680), (88, 845), (99, 843), (134, 824), (176, 783), (202, 750), (353, 405), (757, 401), (756, 37)]

def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
def ls(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n; a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); return a, my - a * mx
def mk(L):
    LX, LB = ls([p[1] for p in L], [p[4] for p in L]); MY, MB = ls([p[2] + T for p in L], [merc(p[3]) for p in L])
    def ll(px, py): return math.degrees(2 * math.atan(math.exp(MY * py + MB)) - math.pi / 2), LX * px + LB
    def inv(lat, lng): return (lng - LB) / LX, (merc(lat) - MB) / MY
    return ll, inv
l08, i08 = mk(F08); l07, i07 = mk(F07); l05, i05 = mk(F05); l06, i06 = mk(F06)
def residuals(L, f): return [(p[0], round((f(p[1], p[2] + T)[0] - p[3]) * 111200), round((f(p[1], p[2] + T)[1] - p[4]) * 71500)) for p in L]
def ring(px, f, shift=(0, 0)):
    """frame pixels -> [(lng, lat)] (shapely order)"""
    return [(f(x + shift[0], y + shift[1])[1], f(x + shift[0], y + shift[1])[0]) for x, y in px]
def poly(px, f, shift=(0, 0)):
    from shapely.geometry import Polygon
    g = Polygon(ring(px, f, shift))
    return g if g.is_valid else g.buffer(0)
def frame(f, shift=(0, 0)): return poly([(0, 37), (1919, 37), (1919, 867), (0, 867)], f, shift)
def biggest(g):
    return g if g.geom_type == 'Polygon' else max(g.geoms, key=lambda x: x.area)
def join(base, detail_polys, other, band=0.003):
    """detail frames win where they cover; the coarse polygon `other` fills the rest (outside the detail frames shrunk by `band` degrees)"""
    from shapely.ops import unary_union
    return unary_union(list(detail_polys) + [other.difference(unary_union([d.buffer(-band) for d in base]))]).buffer(0.0008, join_style=2).buffer(-0.0008, join_style=2)
def shapes():
    from shapely.ops import unary_union
    kaw = poly(KAWKAWA, l06); lai = poly(LAIDLAW, l06, SH); sv07 = poly(SV07, l07); sv05 = poly(SV05, l05)
    top = sv05.intersection(__import__('shapely.geometry', fromlist=['box']).box(-122, 49.3, -121, 49.4))
    sv = unary_union([sv07, top]).buffer(0.0004, join_style=2).buffer(-0.0004, join_style=2)
    fp05 = frame(l05); fp07b = frame(l06, SH)
    hope = join([fp05, fp07b], [poly(HOPE05, l05), poly(HOPE07B, l06, SH)], poly(HOPE08, l08)).difference(lai.buffer(0.00005))
    hl = join([fp05, fp07b], [poly(HL05, l05), poly(HL07B, l06, SH)], poly(HL08, l08))
    return {'hope': biggest(hope), 'kawkawa-lake': kaw, 'laidlaw': lai, 'sunshine-valley': biggest(sv), 'harrison-lake': biggest(hl)}
def to_ring(g, nd=5):
    c = list(g.exterior.coords); c = [[round(y, nd), round(x, nd)] for x, y in c]
    return c if c[0] == c[-1] else c + [c[0]]
def bbox_center(areas):
    pts = [p for a in areas for r in a['rings'] for p in r]; pad = 0.004
    bbox = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    return bbox, {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}
def main():
    from shapely.geometry import Polygon
    if '--check' in sys.argv:
        for n, L, f in [('05', F05, l05), ('06+07b', F06, l06), ('07', F07, l07), ('08', F08, l08)]: print(n, 'residuals (m north, m east):', residuals(L, f)[:12])
    sold = json.load(open(os.path.join(ROOT, 'src/data/sold/sold-12m.json')))['sub']
    S = shapes()
    HOPE = [('hope-bc-guide', 'Hope', 'Hope & Area|Hope', 'hope'), ('kawkawa-lake', 'Kawkawa Lake', 'Hope & Area|Kawkawa Lake', 'kawkawa-lake'), ('laidlaw', 'Laidlaw', 'Hope & Area|Laidlaw', 'laidlaw'),
            ('sunshine-valley', 'Sunshine Valley', 'Hope & Area|Sunshine Valley', 'sunshine-valley')]
    areas = []
    for id_, name, key, sk in HOPE:   # Hope first so the polygons inside it are drawn over it
        assert key in sold, key
        areas.append({'id': id_, 'name': name, 'href': '/hope-bc-guide.html', 'status': 'draft', 'sold': key, 'rings': [to_ring(S[sk])]})
    bbox, center = bbox_center(areas)
    json.dump({'region': 'hope', 'name': 'Hope & Area', 'center': center, 'bbox': bbox, 'areas': areas}, open(os.path.join(ROOT, 'src/data/maps/hope.json'), 'w'), separators=(',', ':')); print('hope', len(areas), 'areas', bbox)
    # --- Harrison Lake: additive into agassiz-harrison.json ---
    p = os.path.join(ROOT, 'src/data/maps/agassiz-harrison.json'); d = json.load(open(p))
    keep = [a for a in d['areas'] if a['id'] != 'harrison-lake']
    g = S['harrison-lake']
    for a in keep:   # the existing neighbours keep their ground
        for r in a['rings']:
            n = Polygon([(lng, lat) for lat, lng in r]); n = n if n.is_valid else n.buffer(0)
            if g.intersects(n): print('  harrison-lake overlaps', a['id'], round(g.intersection(n).area * 111.2 * 71.5, 2), 'km2 (trimmed)'); g = biggest(g.difference(n))
    key = 'Harrison Lake|Harrison Lake'; assert key in sold, key
    keep.append({'id': 'harrison-lake', 'name': 'Harrison Lake', 'href': '/harrison-hot-springs-bc-guide.html', 'status': 'draft', 'sold': key, 'rings': [to_ring(g)]})
    d['areas'] = keep; d['bbox'], d['center'] = bbox_center(keep)
    json.dump(d, open(p, 'w'), separators=(',', ':')); print('agassiz-harrison', len(keep), 'areas', d['bbox'])
if __name__ == '__main__': main()
