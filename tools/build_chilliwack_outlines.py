"""Draft outlines for the Chilliwack region -> src/data/maps/chilliwack.json and src/data/maps/agassiz-harrison.json

Source: Jared's Paragon map search (FVREB sub-area layer), eleven screenshots of 2026-11-05 (Chilliwack-region closeups).  Frames 02 to 09 are the same zoom
panned around; they were registered to frame 02 by SIFT feature matching (shifts in OFF below, in pixels) and read off one stitched mosaic.  Frame 01 is the same view at
twice the zoom and gives the Downtown outline; frame 11 is Harrison Hot Springs at twice the zoom with its own fit.
Pixels are turned into latitude and longitude with a Web Mercator fit to ten Google Maps landmark coordinates (Chilliwack General Hospital, Island 22 Dog Park, Popkum Motor
Park, Seabird College, Agassiz Speedway, Cultus Lake Waterpark, Chilliwack Community Forest, Greendale Acres, Allison Pool, Mt Woodside Launch); the fit misses them by
27 m at worst (about 12.5 m per pixel).  Frame 11 uses five landmarks and misses by 4 m (6.3 m per pixel).  Edges read off the screenshots are good to about 100 m on straight roads
and a block or two on river banks and bush edges.
Clipped on purpose, because the screenshots stop there: Bridal Falls (its south-west corner runs on past the bottom of the frame), Agassiz (the district runs north past the top),
Lake Errock (runs west past the left edge).  Not drawn (not enough of the shape on screen): Ryder Lake, Eastern Hillsides, Majuba Hill, Vedder Mountain, Chilliwack River Valley,
Cultus Lake, Mt Woodside (no page), Harrison Mills (no polygon on the layer).  Every area stays 'draft'.
  python3 -I tools/build_chilliwack_outlines.py [--check]"""
import json, math, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
LAND = [(875, 496, 49.166781, -121.9636126), (754, 287, 49.1906958, -121.9844822), (2279, 197, 49.2006216, -121.7226286), (2219, -269, 49.252988, -121.7330237),
        (1719, -366, 49.2637651, -121.8186462), (812, 1308, 49.0757817, -121.9743913), (1875, 657, 49.1489739, -121.7920615), (288, 814, 49.1312537, -122.0645375),
        (1866, 1288, 49.0779408, -121.7936216), (1319, -187, 49.2436064, -121.8874496)]
LAND11 = [(698, 380, 49.3040111, -121.807554), (648, 664, 49.2880579, -121.8118737), (491, 701, 49.2860375, -121.8253594), (1051, 704, 49.2858676, -121.7772751), (913, 365, 49.3048051, -121.789141)]
def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
def ls(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n; a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); return a, my - a * mx
def mk(L):
    LX, LB = ls([p[0] for p in L], [p[3] for p in L]); MY, MB = ls([p[1] for p in L], [merc(p[2]) for p in L])
    def ll(px, py): return round(math.degrees(2 * math.atan(math.exp(MY * py + MB)) - math.pi / 2), 5), round(LX * px + LB, 5)
    return ll
ll = mk(LAND); ll11 = mk(LAND11)
def residuals(L, f): return [(round((f(p[0], p[1])[0] - p[2]) * 111200), round((f(p[0], p[1])[1] - p[3]) * 73000)) for p in L]
# frame k pixel + OFF[k] = frame 02 pixel (full-screenshot coordinates)
OFF = {'03': (105, -277), '04': (-49, 273), '05': (-83, 60), '06': (-13, 391), '07': (1139, -278), '08': (46, -712), '09': (1090, -747)}
def F(k, pts): return [(x + OFF[k][0], y + OFF[k][1]) for x, y in pts]
CITY = 'Chilliwack'
# --- polygons in frame-02 pixels (mosaic) ---
DOWNTOWN = [(910, 452), (942, 452), (958, 485), (960, 518), (945, 530), (895, 540), (895, 512), (902, 484)]
PROPER_EAST = [(938, 377), (1046, 361), (1081, 358), (1085, 382), (1173, 389), (1154, 392), (1155, 487), (1060, 500), (962, 513), (959, 486), (942, 452), (938, 448)]
PROPER_WEST = [(938, 377), (899, 374), (874, 380), (857, 399), (842, 402), (842, 470), (847, 507), (820, 530), (787, 584), (825, 579), (897, 552), (895, 540), (895, 512), (902, 484), (910, 452), (938, 449)]
PROPER_SOUTH = [(829, 581), (1057, 521), (1052, 555), (1050, 615), (1077, 620), (1077, 636), (917, 694), (916, 652), (880, 656), (867, 640), (860, 615), (835, 595)]
LOWER_LANDING = [(732, 470), (847, 470), (847, 507), (745, 507), (732, 490)]
FAIRFIELD = [(987, -31), (1351, 15), (1355, 96), (1350, 180), (1311, 219), (1246, 254), (1273, 327), (1254, 338), (1219, 329), (1108, 333), (1046, 361), (938, 377), (899, 374), (874, 380),
             (857, 399), (692, 399), (674, 396), (692, 377), (800, 174), (850, 127), (996, 58)]
LITTLE_MTN = [(1081, 358), (1108, 333), (1219, 329), (1254, 338), (1256, 358), (1235, 377), (1211, 389), (1173, 389), (1085, 382)]
CHW_MOUNTAIN = [(366, 671), (405, 605), (458, 563), (528, 528), (589, 517), (689, 528), (695, 559), (682, 586), (612, 636), (535, 675), (458, 705), (432, 736), (412, 717), (382, 678)]
WEST_CHW_1 = [(-80, 725), (12, 690), (112, 669), (208, 694), (305, 682), (366, 671), (382, 678), (412, 717), (432, 736), (358, 748), (243, 763), (108, 763), (-3, 748)]
WEST_CHW_2 = [(432, 736), (458, 705), (535, 675), (612, 636), (682, 586), (695, 559), (749, 607), (787, 584), (825, 579), (835, 595), (860, 615), (867, 640), (880, 656), (916, 652), (917, 694),
              (900, 710), (886, 709), (766, 713), (612, 711), (505, 721)]
EAST_CHW = [(1273, 327), (1351, 15), (1508, 12), (1510, 150), (1519, 298), (1542, 302), (1542, 411), (1652, 482), (1652, 695), (1615, 700), (1600, 740), (1520, 790), (1400, 840), (1300, 900),
            (1204, 940), (1136, 954), (1100, 1026), (1074, 1028), (1074, 946), (1024, 946), (1024, 880), (1020, 862), (1056, 818), (1055, 800), (1044, 770), (1004, 710), (980, 690),
            (917, 694), (1077, 636), (1077, 620), (1050, 615), (1052, 555), (1057, 521), (1155, 487), (1155, 392), (1173, 389), (1211, 389), (1235, 377), (1256, 358), (1254, 338)]
SARDIS_W = [(624, 720), (854, 719), (902, 722), (902, 904), (796, 904), (796, 946), (624, 946)]
SARDIS_E = [(887, 705), (917, 694), (980, 690), (1004, 710), (1044, 770), (1055, 800), (1056, 818), (1020, 862), (1024, 880), (902, 880), (902, 722)]
SARDIS_S = [(908, 880), (1024, 880), (1024, 946), (1074, 946), (1074, 1026), (996, 1026), (988, 1006), (906, 1006), (818, 1008), (818, 1074), (740, 1076), (740, 1130), (624, 1132), (624, 946),
            (796, 946), (796, 904), (908, 904)]
GARRISON = [(818, 1008), (906, 1008), (906, 1076), (872, 1076), (872, 1142), (740, 1142), (740, 1076), (818, 1076)]
VEDDER_X = [(906, 1008), (990, 1008), (990, 1030), (948, 1054), (906, 1076)]
PROMONTORY = [(906, 1076), (948, 1054), (990, 1030), (1074, 1028), (1100, 1026), (1136, 954), (1204, 940), (1204, 1066), (1208, 1128), (1168, 1148), (1080, 1122), (1012, 1128), (908, 1150)]
GREENDALE = [(111, 766), (349, 758), (472, 732), (622, 717), (623, 1118), (526, 1134), (480, 1157), (449, 1188), (357, 1215), (303, 1211), (272, 1180), (226, 1118), (195, 1065), (111, 903), (89, 865), (99, 811)]
YARROW = [(195, 1088), (226, 1118), (272, 1180), (303, 1211), (357, 1215), (449, 1188), (480, 1157), (526, 1134), (622, 1120), (695, 1134), (780, 1145), (649, 1180), (534, 1218), (465, 1272),
          (411, 1318), (299, 1357), (265, 1407), (257, 1430), (195, 1430)]
ROSEDALE = [(1511, 158), (1549, 146), (1619, 122), (1651, 74), (1699, 84), (1779, 118), (1839, 134), (1896, 154), (1899, 177), (1897, 327), (1964, 328), (1969, 300), (2034, 362), (2045, 390),
            (1979, 452), (1879, 542), (1779, 587), (1704, 610), (1654, 614), (1654, 482), (1544, 422), (1544, 300), (1511, 297)]
POPKUM = [(1900, 159), (2077, 141), (2214, 132), (2345, 148), (2250, 223), (2150, 314), (2047, 400), (2036, 350), (1968, 295), (1964, 327), (1900, 327)]
BRIDAL = [(2491, -6), (2673, 232), (2668, 682), (2286, 677), (2205, 750), (2047, 750), (2047, 400), (2150, 314), (2250, 223), (2373, 123), (2450, 68)]
AGASSIZ = [(1820, -499), (1880, -502), (1880, -547), (2530, -547), (2490, -487), (2445, -417), (2430, -317), (2426, -267), (2356, -191), (2321, -163), (2285, -135), (2252, -115), (2237, -54),
           (2171, 22), (2130, 66), (2107, 103), (1960, 148), (1890, 153), (1830, 103), (1730, 73), (1640, 75), (1510, 133), (1510, -297), (1530, -327), (1570, -357), (1660, -397), (1750, -422), (1815, -447)]
LAKE_ERROCK = [(631, -497), (1231, -512), (1146, -427), (976, -222), (886, -172), (711, -140), (816, -47), (861, -30), (891, 63), (836, 148), (691, 293), (346, 326), (304, 293), (304, 233), (46, 233),
               (46, 33), (121, -17), (191, -52), (256, -87), (311, -287), (346, -317), (486, -352), (556, -412)]
HHS_11 = [(770, 235), (790, 265), (850, 330), (900, 383), (950, 360), (1050, 358), (1085, 355), (1090, 302), (1143, 305), (1145, 468), (1198, 475), (1198, 812), (888, 815), (888, 740), (970, 740),
          (970, 650), (850, 650), (850, 448), (675, 448), (675, 420), (700, 375), (735, 320)]
CHW = [  # sold key, slug, name, rings (frame-02 pixels); earlier areas keep their ground where outlines overlap by hand-reading error
 ('Chilliwack|Chilliwack Downtown', 'chilliwack-downtown', 'Chilliwack Downtown', [DOWNTOWN]),
 ('Chilliwack|Chilliwack Proper East', 'chilliwack-proper-east', 'Chilliwack Proper East', [PROPER_EAST]),
 ('Chilliwack|Chilliwack Proper West', 'chilliwack-proper-west', 'Chilliwack Proper West', [PROPER_WEST]),
 ('Chilliwack|Chilliwack Proper South', 'chilliwack-proper-south', 'Chilliwack Proper South', [PROPER_SOUTH]),
 ('Chilliwack|Lower Landing', 'lower-landing', 'Lower Landing', [LOWER_LANDING]),
 ('Chilliwack|Little Mountain', 'little-mountain', 'Little Mountain', [LITTLE_MTN]),
 ('Chilliwack|Fairfield Island', 'fairfield-island', 'Fairfield Island', [FAIRFIELD]),
 ('Chilliwack|Chilliwack Mountain', 'chilliwack-mountain', 'Chilliwack Mountain', [CHW_MOUNTAIN]),
 (None, 'west-chilliwack', 'West Chilliwack', [WEST_CHW_1, WEST_CHW_2]),
 ('Chilliwack|East Chilliwack', 'east-chilliwack', 'East Chilliwack', [EAST_CHW]),
 ('Sardis|Sardis West Vedder', 'sardis-west-vedder', 'Sardis West Vedder', [SARDIS_W]),
 ('Sardis|Sardis East Vedder', 'sardis-east-vedder', 'Sardis East Vedder', [SARDIS_E]),
 ('Sardis|Sardis South', 'sardis-south', 'Sardis South', [SARDIS_S]),
 ('Sardis|Garrison Crossing', 'garrison-crossing', 'Garrison Crossing', [GARRISON]),
 ('Sardis|Vedder Crossing', 'vedder-crossing', 'Vedder Crossing', [VEDDER_X]),
 ('Sardis|Promontory', 'promontory', 'Promontory', [PROMONTORY]),
 ('Sardis|Greendale', 'greendale', 'Greendale', [GREENDALE]),
 ('Yarrow|Yarrow', 'yarrow', 'Yarrow', [YARROW]),
 ('East Chilliwack|Rosedale', 'rosedale-homes-for-sale', 'Rosedale', [ROSEDALE]),
 ('East Chilliwack|Popkum', 'popkum', 'Popkum', [POPKUM]),
 ('East Chilliwack|Bridal Falls', 'bridal-falls', 'Bridal Falls', [BRIDAL]),
]
AGH = [
 ('Agassiz|Agassiz', 'agassiz-bc-guide', 'Agassiz', [AGASSIZ], ll),
 ('Mission|Lake Errock', 'lake-errock', 'Lake Errock', [LAKE_ERROCK], ll),
 ('Harrison Lake|Harrison Hot Springs', 'harrison-hot-springs-bc-guide', 'Harrison Hot Springs', [HHS_11], ll11),
]
def trimmed(rows):
    """Hand-read edges leave slivers where two outlines meet; the later area gives up any overlap (under 900 px2, about 14 ha) with an earlier one."""
    from shapely.geometry import Polygon
    done = []; out = []
    for key, slug, name, rings in rows:
        newr = []
        for ring in rings:
            g = Polygon(ring)
            if not g.is_valid: g = g.buffer(0)
            for h in done:
                if g.intersects(h) and g.intersection(h).area < 900: g = g.difference(h)
            done.append(g)
            if g.is_empty: continue
            gg = g if g.geom_type == 'Polygon' else max(g.geoms, key=lambda x: x.area)
            newr.append(list(gg.exterior.coords)[:-1])
        out.append((key, slug, name, newr))
    return out
def write(region, name, areas_out, pts):
    pad = 0.004; bbox = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    out = {'region': region, 'name': name, 'center': {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}, 'bbox': bbox, 'areas': areas_out}
    json.dump(out, open(os.path.join(ROOT, f'src/data/maps/{region}.json'), 'w'), separators=(',', ':')); print(region, len(areas_out), 'areas', bbox)
def main():
    if '--check' in sys.argv: print('mosaic residuals (m north, m east):', residuals(LAND, ll), '| frame 11:', residuals(LAND11, ll11))
    sold = json.load(open(os.path.join(ROOT, 'src/data/sold/sold-12m.json')))['sub']
    pts = []; areas = []
    for key, slug, name, rings in trimmed(CHW):
        rr = []
        for ring in rings:
            r = [list(ll(x, y)) for x, y in ring]; r.append(r[0]); rr.append(r); pts += r
        a = {'id': slug, 'name': name, 'href': f'/{slug}.html', 'status': 'draft'}
        if key: assert key in sold, key; a['sold'] = key
        a['rings'] = rr; areas.append(a)
    write('chilliwack', 'Chilliwack', areas, pts)
    pts = []; areas = []
    for key, slug, name, rings, f in [(k, s, n, r, f) for (k, s, n, r, f) in AGH]:
        rr = []
        for ring in rings:
            r = [list(f(x, y)) for x, y in ring]; r.append(r[0]); rr.append(r); pts += r
        assert key in sold, key
        areas.append({'id': slug, 'name': name, 'href': f'/{slug}.html', 'status': 'draft', 'sold': key, 'rings': rr})
    write('agassiz-harrison', 'Agassiz and Harrison', areas, pts)
if __name__ == '__main__': main()
