"""Draft outlines for Cultus Lake and the Chilliwack River Valley side -> ADDS to src/data/maps/chilliwack.json (existing areas are kept untouched).

Source: Jared's Paragon map search (CADREB sub-area layer, labels on), close-ups of 2026-11-05 (frames 01 02 03 04 10 11 of the Chilliwack-Hope-Harrison set; 1920x878,
Paragon toolbar cropped off the top 37 px and the Google footer off the bottom 10 px).
Three separate fits, each a Web Mercator (linear longitude vs x, Mercator latitude vs y) fit to Google Maps coordinates of POI icon centres:
  M1  frames 01+02+03 registered by SIFT (same zoom, about 12.2 m per pixel; shifts in the mosaic below); 8 landmarks, worst miss 32 m (Tamihi Creek Campground).
  M2  frames 10+11 registered by SIFT (same zoom, about 24.5 m per pixel, one zoom out); 10 landmarks, worst miss 37 m (Greendale Acres photo spot).
      Allison Pool Recreation Site (43 m north, 34 m west) was dropped as an outlier (the Google search hit is probably not the icon).
  F4  frame 04 alone (about 12.2 m per pixel, does not register with the others); 8 landmarks, worst miss 13 m.
Ring vertices are hand-read pixels in those three pixel systems, converted to lat/lng, then merged and trimmed in lat/lng.  Areas that span frames (Cultus Lake East, Chilliwack
River Valley) take their detail from the sharper M1/F4 frames and the rest from M2.
Drawn: Cultus Lake North, Cultus Lake South (contains Lindell Beach), Columbia Valley, Vedder Mountain, Majuba Hill, Ryder Lake (was missing), Eastern Hillsides, Cultus Lake East,
Chilliwack River Valley.  Not drawn: East Chilliwack (already in the file and it matches the cyan polygon of frame 11, so it is kept as it was).
Clipped on purpose where the screenshots stop: Chilliwack River Valley (east edge at the right edge of frame 10, north edge guessed between the Hope-side yellow polygon seen in
frames 04/11 and the orange polygon in frame 10), Cultus Lake East and Columbia Valley (south edge is the border line as Paragon draws it).
Each new area gives way to the areas already in the file where hand-read edges overlap by less than about 1 km2; a bigger overlap is left alone and printed.
Idempotent: re-running replaces only the areas with the ids below.  Every area stays 'draft'.
  python3 -I tools/build_cultus_outlines.py [--check]"""
import json, math, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'src/data/maps/chilliwack.json')
# (x, y, lat, lng, name): pixel is the icon centre in the mosaic pixel system
L1 = [(781, 193, 49.0963805, -122.0068297, 'Vedder River Campground'), (1007, 180, 49.098109, -121.9680021, 'Vedder Park'), (969, 378, 49.0757817, -121.9743913, 'Cultus Lake Waterpark'),
      (1337, 415, 49.0714953, -121.9112916, 'Liumchen Ecological Reserve'), (1531, 648, 49.0454595, -121.8778443, 'Windy Knob Trail'),
      (495, 641, 49.0461319, -122.0558682, 'Vedder Mountain Gliders Launch'), (1763, 416, 49.0711558, -121.8383437, 'Tamihi Creek Campground'), (20, 255, 49.0896602, -122.1374422, 'McDonald Park')]
L2 = [(84, 481, 49.0757817, -121.9743913, 'Cultus Lake Waterpark'), (615, 154, 49.1489739, -121.7920615, 'Chilliwack Community Forest'), (775, 311, 49.1141662, -121.7372605, "Widow's Peak"),
      (1173, 105, 49.16, -121.6005555, 'Welch Peak'), (1097, 368, 49.1010151, -121.6267115, 'Camp Foley'), (1198, 704, 49.0255555, -121.5919444, 'Slesse Mountain'),
      (-179, 232, 49.1312537, -122.0645375, 'Greendale Acres'), (-391, 419, 49.0896602, -122.1374422, 'McDonald Park'), (337, -268, 49.2436064, -121.8874496, 'Mt Woodside Launch'),
      (817, -75, 49.2006216, -121.7226286, 'Popkum Motor Park')]
L4 = [(463, 350, 49.1489739, -121.7920615, 'Chilliwack Community Forest'), (783, 659, 49.1141662, -121.7372605, "Widow's Peak"), (1199, 115, 49.1752777, -121.6658333, 'Lady Peak'),
      (1775, 126, 49.1741666, -121.5669444, 'Conway Peak'), (1579, 252, 49.16, -121.6005555, 'Welch Peak'), (1669, 253, 49.16, -121.585, 'Foley Peak'),
      (1427, 776, 49.1010151, -121.6267115, 'Camp Foley'), (1269, 768, 49.1019888, -121.6537869, 'Chipmunk Peninsula Campground')]
def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
def ls(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n; a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); return a, my - a * mx
def mk(L):
    LX, LB = ls([p[0] for p in L], [p[3] for p in L]); MY, MB = ls([p[1] for p in L], [merc(p[2]) for p in L])
    def ll(px, py): return (math.degrees(2 * math.atan(math.exp(MY * py + MB)) - math.pi / 2), LX * px + LB)
    return ll
f1 = mk(L1); f2 = mk(L2); f4 = mk(L4)
def residuals(L, f): return [(p[4], round((f(p[0], p[1])[0] - p[2]) * 111200), round((f(p[0], p[1])[1] - p[3]) * 73000)) for p in L]
def conv(f, pts): return [f(x, y) for x, y in pts]
# ---- polygons, M1 pixels (frame 01 pixels = mosaic pixels; frames 02 and 03 shifted by (-230,302) and (-434,-28)) ----
CLN = [(979, 304), (984, 330), (985, 345), (981, 372), (976, 381), (1044, 381), (1045, 430), (1050, 562), (1000, 577), (966, 584), (970, 560), (977, 500), (975, 475), (962, 460), (947, 440),
       (937, 425), (920, 425), (904, 417), (910, 400), (925, 390), (939, 377), (939, 355), (955, 335), (970, 312)]
CLS = [(763, 674), (746, 687), (724, 705), (699, 723), (677, 737), (659, 752), (663, 774), (668, 791), (704, 793), (727, 800), (752, 812), (777, 812), (785, 800), (774, 784), (767, 782),
       (767, 759), (771, 748), (761, 729), (758, 701)]
COLV = [(194, 1042), (212, 1001), (244, 962), (297, 915), (350, 886), (409, 862), (462, 836), (500, 824), (503, 806), (556, 756), (588, 739), (626, 765), (656, 754), (659, 752), (663, 774),
        (668, 791), (704, 793), (727, 800), (752, 812), (777, 812), (785, 800), (785, 1054), (400, 1048)]
MAJUBA = [(569, 380), (572, 396), (556, 429), (528, 459), (500, 493), (478, 523), (439, 548), (400, 568), (367, 579), (361, 589), (384, 587), (383, 529), (403, 507), (419, 482),
          (422, 469), (444, 446), (467, 423), (500, 409), (522, 396), (556, 383)]
VEDDER = [(1029, 200), (1033, 220), (1027, 234), (1015, 248), (1010, 264), (999, 289), (979, 304), (970, 312), (955, 335), (939, 355), (939, 377), (925, 390), (910, 400), (904, 417),
          (881, 453), (880, 483), (867, 517), (860, 548), (827, 573), (799, 612), (779, 646), (763, 673), (746, 687), (724, 705), (699, 723), (677, 737), (659, 752), (656, 754), (626, 765),
          (588, 739), (556, 756), (503, 806), (500, 824), (462, 836), (409, 862), (350, 886), (297, 915), (244, 962), (212, 1001), (194, 1042), (138, 1044), (136, 896), (139, 851),
          (156, 829), (203, 779), (217, 757), (242, 726), (258, 701), (278, 665), (300, 648), (333, 612), (361, 589), (367, 579), (400, 568), (439, 548), (478, 523), (500, 493),
          (528, 459), (556, 429), (572, 396), (569, 380), (573, 370), (620, 329), (667, 300), (713, 278), (753, 271), (800, 262), (827, 257), (867, 249), (907, 245), (947, 233),
          (971, 229), (984, 226), (987, 211), (1002, 203)]
# Cultus Lake East: north edge = river strip (M1), then M2 down the east side, border, M1 border west, up the east shore of the lake and around Cultus Lake North
CLE_A = [(1031, 201), (1034, 228), (1049, 242), (1074, 253), (1084, 259), (1085, 270), (1102, 286), (1121, 298), (1140, 325), (1159, 345), (1180, 370), (1200, 374), (1245, 372),
         (1275, 365), (1300, 355), (1350, 352), (1362, 389), (1381, 399), (1416, 405), (1434, 389), (1456, 380), (1506, 374), (1550, 377), (1600, 383), (1650, 389), (1688, 399),
         (1713, 402), (1762, 427), (1794, 433), (1797, 446), (1781, 467), (1762, 480), (1775, 492), (1819, 502), (1831, 530), (1837, 555)]
CLE_B = [(529, 601), (550, 666), (564, 709), (593, 744), (629, 780), (671, 816), (693, 837), (697, 839)]
CLE_C = [(1670, 1076), (1400, 1068), (1100, 1060), (785, 1054), (785, 800), (774, 784), (767, 782), (767, 759), (771, 748), (774, 736), (799, 730), (821, 734), (827, 748), (871, 707),
         (916, 668), (949, 623), (963, 587), (1000, 577), (1050, 562), (1045, 430), (1044, 381), (976, 381), (981, 372), (985, 345), (984, 330), (979, 304), (999, 289), (1010, 264),
         (1015, 248), (1027, 234), (1033, 220)]
# Chilliwack River Valley: strip beside the river (M1), the big mountain block (M2, F4 where it is sharper)
CRV_A = [(1031, 201), (1037, 207), (1043, 217), (1049, 223), (1065, 228), (1087, 231), (1115, 229), (1165, 226), (1166, 271), (1195, 276), (1215, 290), (1252, 326), (1300, 330),
         (1350, 330), (1487, 342), (1562, 355), (1675, 374), (1737, 383), (1787, 380), (1831, 349), (1875, 280)]
CRV_B = [(535, 409), (627, 441), (630, 337)]                       # M2: Ryder Lake's south-east lobe edge, then up its east edge to the Eastern Hillsides corner
CRV_F4 = [(492, 697), (634, 697), (634, 520), (750, 520), (825, 385), (875, 370), (1257, 375), (1257, 112), (1652, 173), (1845, 37)]
CRV_C = [(1410, 6), (1420, 37), (1717, 37), (1787, 160), (1915, 310), (1915, 833), (1312, 833), (697, 839)]     # M2: clipped north and east edges, border (south edge)
RYDER_M2 = [(280, 310), (340, 280), (393, 253)]; RYDER_F4 = [(111, 483), (112, 697), (492, 697)]; RYDER_M2B = [(627, 441), (535, 409)]   # then the sharper M1 river-side edge (CRV_A reversed), then (1165, 226) and back
EH = [(629, 94), (596, 111), (564, 129), (550, 151), (521, 169), (500, 201), (443, 247), (414, 265), (400, 267), (371, 261), (350, 269), (321, 290), (289, 308), (243, 313), (243, 379),
      (204, 397), (186, 433), (168, 447), (143, 469), (111, 483), (112, 697), (634, 697), (634, 90)]
def rings():
    ryder = conv(f2, RYDER_M2) + conv(f4, RYDER_F4) + conv(f2, RYDER_M2B) + conv(f1, list(reversed(CRV_A[9:]))) + conv(f1, [(1165, 226)]) + conv(f2, [(280, 400)])
    cle = conv(f1, CLE_A) + conv(f2, CLE_B) + conv(f1, CLE_C)
    crv = conv(f1, CRV_A) + conv(f2, CRV_B) + conv(f4, CRV_F4) + conv(f2, CRV_C)
    # strip's south side = Cultus Lake East's north edge, walked back west from the border to the bridge
    crv += conv(f2, [(671, 816), (629, 780), (593, 744), (564, 709), (550, 666), (529, 601)]) + conv(f1, list(reversed(CLE_A[1:])))
    return [  # id, name, href slug, sold key, ring
        ('cultus-lake-north', 'Cultus Lake North', 'cultus-lake', 'Cultus Lake & Area|Cultus Lake North', conv(f1, CLN)),
        ('cultus-lake-south', 'Cultus Lake South', 'cultus-lake', 'Cultus Lake & Area|Cultus Lake South', conv(f1, CLS)),
        ('columbia-valley', 'Columbia Valley', 'columbia-valley', 'Cultus Lake & Area|Columbia Valley', conv(f1, COLV)),
        ('majuba-hill', 'Majuba Hill', 'majuba-hill', 'Yarrow|Majuba Hill', conv(f1, MAJUBA)),
        ('vedder-mountain', 'Vedder Mountain', 'vedder-mountain', 'Cultus Lake & Area|Vedder Mountain', conv(f1, VEDDER)),
        ('ryder-lake', 'Ryder Lake', 'ryder-lake', 'Sardis|Ryder Lake', ryder),
        ('eastern-hillsides', 'Eastern Hillsides', 'eastern-hillsides', 'Chilliwack|Eastern Hillsides', conv(f4, EH)),
        ('cultus-lake-east', 'Cultus Lake East', 'cultus-lake', 'Cultus Lake & Area|Cultus Lake East', cle),
        ('chilliwack-river-valley', 'Chilliwack River Valley', 'chilliwack-river-valley', 'Sardis|Chilliwack River Valley', crv)]
def trim(rows, existing):
    """New areas give way to the existing ones, then to each other, where hand-read edges overlap by less than ~1 km2 (a bigger overlap is printed and left)."""
    from shapely.geometry import Polygon
    def proj(r): return [(lng * 73000, lat * 111200) for lat, lng in r]
    def back(c): return [(y / 111200, x / 73000) for x, y in c]
    done = [(a['id'], Polygon(proj(r)).buffer(0)) for a in existing for r in a['rings']]
    out = []
    for aid, name, slug, key, ring in rows:
        g = Polygon(proj(ring))
        if not g.is_valid: g = g.buffer(0)
        for oid, h in done:
            if g.intersects(h):
                ov = g.intersection(h).area
                if '--check' in sys.argv and ov > 2e4: print(f'  overlap {aid} / {oid}: {ov / 1e6:.2f} km2')
                if ov < 1.0e6: g = g.difference(h)
                elif ov > 1.0e4: print(f'  note: {aid} overlaps {oid} by {ov / 1e6:.2f} km2 (left as drawn)')
        done.append((aid, g))
        if g.is_empty: continue
        gg = g if g.geom_type == 'Polygon' else max(g.geoms, key=lambda x: x.area)
        c = list(gg.simplify(5).exterior.coords)
        r = [[round(a, 5), round(b, 5)] for a, b in back(c)]
        out.append((aid, name, slug, key, [r]))
    return out
def main():
    if '--check' in sys.argv: print('M1', residuals(L1, f1), '\nM2', residuals(L2, f2), '\nF4', residuals(L4, f4))
    sold = json.load(open(os.path.join(ROOT, 'src/data/sold/sold-12m.json')))['sub']
    d = json.load(open(OUT)); mine = {r[0] for r in rings()}
    base = [a for a in d['areas'] if a['id'] not in mine]
    new = trim(rings(), base)
    for aid, name, slug, key, rr in new:
        assert key in sold, key
        assert rr[0][0] == rr[0][-1], aid
        base.append({'id': aid, 'name': name, 'href': f'/{slug}.html', 'status': 'draft', 'sold': key, 'rings': rr})
    pts = [p for a in base for r in a['rings'] for p in r]; pad = 0.004
    bbox = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    d['areas'] = base; d['bbox'] = bbox; d['center'] = {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}
    json.dump(d, open(OUT, 'w'), separators=(',', ':')); print('chilliwack', len(base), 'areas', bbox)
if __name__ == '__main__': main()
