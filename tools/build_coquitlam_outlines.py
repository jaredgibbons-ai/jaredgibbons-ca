"""Draft outlines for the Coquitlam sub-areas -> src/data/maps/coquitlam.json

Source: Jared's Paragon map search, GVR Sub Areas 2022 layer with its labels switched on, screenshots of 2026-11-05 (frame A: central Coquitlam; frame B: the same
view panned north-east, registered to A by feature matching: B = A shifted by (-119.7, +269.8) px).  Names come from Paragon's Sub-Area/Community lookup (23 codes VCQBM to
VCQWS, which the layer shows as the last two letters).  Pixels are turned into latitude and longitude with a Web Mercator fit to seven Google Maps landmark coordinates
(Eagle Ridge Hospital, Lafarge Lake-Douglas and Inlet Centre stations, Port Coquitlam Community Centre, Poirier Sport & Leisure Complex, Sheffield Park, Bert Flinn Park);
the fit misses them by 60 m at worst (about 8.5 m per pixel).  Straight road edges are good to about 60 m; creek, river and curved edges to a block or two.
Clipped on purpose: Westwood Plateau and Hockaday run on north past the top of the screenshot, and Burke Mountain's polygon covers the whole watershed to the north and
east; each outline stops at the built-up area, so those three are partial shapes.  Westwood Summit (WS, no sales, no page) is not drawn.  Every area stays 'draft'.
  python3 -I tools/build_coquitlam_outlines.py [--check]"""
import json, math, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
LAND = [(513, 348, 49.285505, -122.8235798), (789, 357, 49.2856492, -122.7916212), (913, 682, 49.2601615, -122.7771112), (324, 750, 49.2549668, -122.8454949),
        (474, 467, 49.27721, -122.82819), (1207, 186, 49.2978027, -122.7430139), (339, 178, 49.2984595, -122.8437795)]
def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
def ls(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n; a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); return a, my - a * mx
(LX, LB) = ls([p[0] for p in LAND], [p[3] for p in LAND]); (MY, MB) = ls([p[1] for p in LAND], [merc(p[2]) for p in LAND])
def ll(px, py):
    lat = math.degrees(2 * math.atan(math.exp(MY * py + MB)) - math.pi / 2); return round(lat, 5), round(LX * px + LB, 5)
def residuals():
    return [(round((ll(p[0], p[1])[0] - p[2]) * 111200), round((ll(p[0], p[1])[1] - p[3]) * 73000)) for p in LAND]
SHIFT_B = (119.7, -269.8)      # frame B pixel + this = frame A pixel
def B(*pts): return [(x + SHIFT_B[0], y + SHIFT_B[1]) for x, y in pts]
# --- polygons in frame A pixels ---
WP_E = [(692, 110), (692, 191), (702, 193), (762, 241), (777, 378), (790, 396), (785, 411), (777, 488), (760, 531)]          # frame B: Westwood Plateau / Hockaday line
HO_E = [(855, 110), (855, 141), (877, 165), (872, 211), (845, 278), (842, 311), (834, 361), (860, 390), (863, 411)]  # frame B: Coquitlam River side of Hockaday
AREAS = [  # sold-aggregate key, page slug, display name, polygon
 ('Coquitlam|Westwood Plateau', 'westwood-plateau-coquitlam', 'Westwood Plateau',
  B((403, 110)) + B(*WP_E) + [(800, 261), (800, 241), (767, 218), (740, 211), (717, 217), (702, 228), (667, 238), (633, 244), (588, 241), (552, 213), (523, 206)]),
 ('Coquitlam|Hockaday', 'hockaday', 'Hockaday',
  B(*WP_E[:1]) + B(*HO_E) + [(986, 164), (988, 185), (982, 200), (988, 207), (970, 224), (940, 222), (936, 234), (930, 234), (915, 243), (897, 253)] + B(*WP_E[::-1][:-1])),
 ('Coquitlam|Summitt View', 'summitt-view-coquitlam', 'Summitt View', [(537, 246), (582, 244), (582, 280), (556, 296), (537, 294)]),
 ('Coquitlam|Upper Eagle Ridge', 'upper-eagle-ridge-coquitlam', 'Upper Eagle Ridge',
  [(582, 244), (635, 245), (638, 265), (633, 285), (620, 311), (618, 328), (630, 345), (647, 361), (648, 368), (633, 371), (600, 388), (580, 386), (558, 376), (537, 368), (537, 294), (556, 296), (582, 280)]),
 ('Coquitlam|Scott Creek', 'scott-creek-coquitlam', 'Scott Creek',
  [(635, 245), (667, 238), (702, 228), (702, 365), (648, 368), (647, 361), (630, 345), (618, 328), (620, 311), (633, 285), (638, 265)]),
 ('Coquitlam|Canyon Springs', 'canyon-springs', 'Canyon Springs', [(702, 228), (717, 217), (740, 211), (767, 218), (800, 241), (800, 365), (702, 365)]),
 ('Coquitlam|North Coquitlam', 'north-coquitlam', 'North Coquitlam', [(800, 261), (880, 261), (818, 450), (800, 452), (798, 513), (738, 480), (700, 465), (702, 365), (800, 365)]),
 ('Coquitlam|New Horizons', 'new-horizons-coquitlam', 'New Horizons',
  [(880, 261), (897, 253), (915, 243), (930, 234), (936, 234), (940, 250), (955, 270), (960, 300), (966, 332), (960, 347), (945, 368), (925, 400), (920, 422), (923, 451), (820, 451)]),
 ('Coquitlam|River Springs', 'river-springs-coquitlam', 'River Springs',
  [(936, 234), (940, 222), (970, 224), (988, 207), (998, 237), (1035, 260), (1032, 262), (1031, 307), (1001, 307), (1001, 451), (923, 451), (920, 422), (925, 400), (945, 368), (960, 347), (966, 332), (960, 300), (955, 270), (940, 250)]),
 ('Coquitlam|Park Ridge Estates', 'park-ridge-estates-coquitlam', 'Park Ridge Estates',
  [(988, 164), (1030, 164), (1034, 169), (1022, 192), (1051, 222), (1051, 270), (1041, 270), (1040, 262), (1035, 259), (998, 236), (988, 206), (982, 200), (988, 185)]),
 ('Coquitlam|Burke Mountain', 'burke-mountain', 'Burke Mountain',
  B((900, 330), (1180, 330), (1180, 625), (928, 625), (928, 578), (931, 540), (931, 492), (902, 462), (914, 439), (900, 439))),
 ('Coquitlam|Eagle Ridge CQ', 'eagle-ridge-cq', 'Eagle Ridge',
  [(537, 368), (558, 376), (580, 386), (600, 388), (633, 371), (648, 368), (702, 365), (702, 463), (512, 462), (515, 428), (537, 413)]),
 ('Coquitlam|Ranch Park', 'ranch-park-coquitlam', 'Ranch Park',
  [(512, 462), (600, 462), (700, 465), (738, 480), (728, 487), (728, 655), (700, 685), (677, 695), (673, 688), (597, 688), (580, 698), (566, 657), (512, 653), (512, 588), (521, 587), (521, 553), (512, 552)]),
 ('Coquitlam|Meadow Brook', 'meadow-brook-coquitlam', 'Meadow Brook', [(738, 481), (798, 513), (798, 680), (764, 687), (728, 655), (728, 487)]),
 ('Coquitlam|Chineside', 'chineside', 'Chineside', [(409, 522), (511, 522), (511, 553), (521, 553), (521, 587), (511, 589), (511, 652), (395, 651), (395, 543)]),
 ('Coquitlam|Harbour Place', 'harbour-place-coquitlam', 'Harbour Place', [(318, 529), (401, 530), (395, 543), (395, 651), (265, 651), (265, 554), (318, 554)]),
 ('Coquitlam|Harbour Chines', 'harbour-chines', 'Harbour Chines', [(128, 554), (265, 554), (265, 650), (126, 650)]),
]
def trimmed():
    """Hand-read edges leave slivers where two outlines meet; the later area gives up any overlap with an earlier one."""
    from shapely.geometry import Polygon
    done = []; out = []
    for key, slug, name, poly in AREAS:
        g = Polygon(poly)
        for h in done: g = g.difference(h) if g.intersects(h) and g.intersection(h).area < 400 else g
        done.append(g)
        ring = list(g.exterior.coords) if g.geom_type == 'Polygon' else list(max(g.geoms, key=lambda x: x.area).exterior.coords)
        out.append((key, slug, name, ring[:-1]))
    return out
def main():
    if '--check' in sys.argv: print('landmark residuals (m north, m east):', residuals())
    pts = []; areas = []
    for key, slug, name, poly in trimmed():
        r = [list(ll(x, y)) for x, y in poly]; r.append(r[0]); pts += r
        areas.append({'id': slug, 'name': name, 'href': f'/{slug}.html', 'status': 'draft', 'sold': key, 'rings': [r]})
    pad = 0.004; bbox = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    out = {'region': 'coquitlam', 'name': 'Coquitlam', 'center': {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}, 'bbox': bbox, 'areas': areas}
    json.dump(out, open(os.path.join(ROOT, 'src/data/maps/coquitlam.json'), 'w'), separators=(',', ':'))
    print(len(areas), 'areas', bbox)
if __name__ == '__main__': main()
