"""Draft outlines for Port Moody and Port Coquitlam, plus the Coquitlam leftovers -> src/data/maps/port-moody.json, src/data/maps/port-coquitlam.json and
src/data/maps/coquitlam.json (ADDITIVE for Coquitlam: the 17 areas not named below are untouched)

Source: ONE wide Paragon map screenshot of 2026-11-05 (GVR Sub Areas 2022 layer, code labels on, 1568 x 768; map pane y 153 to 748), 16.3 m per pixel east-west and
15.9 m per pixel north-south.  Port Moody, Port Coquitlam and all of Coquitlam south of Westwood Plateau are in it.  Vertices were read by eye from 3x to 8x crops (a saturation-boosted copy
shows the white polygon boundaries well); the colours are NOT boundaries (Paragon's tint over Google's parks and water changes the shade inside one polygon).
Calibration: Web Mercator fit (separate x and y scale, so a slightly non-square screenshot is absorbed) to eight landmark icons whose coordinates come from OpenStreetMap
(Nominatim; Google Maps is CAPTCHA-blocked): Rocky Point Park, Town Centre Park, SFU, Hume Park, Mt Burke, High Knoll, Como Lake (lake centre), Eagle Ridge Hospital, plus two
boundary corners (CW/CC and CC/ML slant) taken from the earlier, 3 m-per-pixel Coquitlam frame (build_coquitlam_more_outlines.py).  Misses up to ~70 m (4 px); `--check` prints them.
Dropped as outliers: Lafarge Lake (-140 m, blob read wrong), Moody Centre station icon (-125 m, icon not at the OSM node), Mundy Park label (label, not an icon).
Clipped on purpose: Anmore and Heritage Woods PM run north past the top of the map (y 153).  Not drawn: Belcarra (only a cut-off sliver at the top edge, if any), Ioco (code IO,
no sold key).  Westwood Summit CQ (WS) is drawn but HELD: it has no page (5 closed sales, below build_gvr_pages MIN_SALES).  Coquitlam West, Central Coquitlam and Maillardville
REPLACE the earlier partial slices (same ids, hrefs) that the now-retired build_coquitlam_more_outlines.py drew (see git history).  Every area stays 'draft'.
  python3 -I tools/build_pocomo_outlines.py [--check]"""
import json, math, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
MAPS = os.path.join(ROOT, 'src/data/maps')
LAND = [  # (pixel x, pixel y, lat, lng, name)
    (592.5, 307.5, 49.28519, -122.82432, 'Eagle Ridge Hospital'), (479.5, 343.8, 49.28039, -122.84948, 'Rocky Point Park'), (760.5, 281, 49.28931, -122.78644, 'Town Centre Park'),
    (160, 350, 49.27930, -122.92035, 'SFU'), (290, 664, 49.23517, -122.89051, 'Hume Park'), (1094.4, 158.1, 49.30765, -122.71125, 'Mt Burke'), (1187, 204, 49.30070, -122.69053, 'High Knoll'),
    (436.5, 490, 49.25995, -122.85817, 'Como Lake'),
    (392, 563, 49.24901, -122.86932, 'CW/CC corner (earlier frame)'), (374, 589, 49.24577, -122.87291, 'CC/ML slant corner (earlier frame)')]
def merc(l): return math.log(math.tan(math.pi / 4 + math.radians(l) / 2))
def ls(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n; a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); return a, my - a * mx
LX, LB = ls([p[0] for p in LAND], [p[3] for p in LAND]); MY, MB = ls([p[1] for p in LAND], [merc(p[2]) for p in LAND])
def ll(px, py): return round(math.degrees(2 * math.atan(math.exp(MY * py + MB)) - math.pi / 2), 5), round(LX * px + LB, 5)
def residuals(): return [(p[4], round((ll(p[0], p[1])[0] - p[2]) * 111200), round((ll(p[0], p[1])[1] - p[3]) * 73000)) for p in LAND]
T = 153   # top of the map pane
# ---------------- Port Moody (sold key, page slug, name, outline in screenshot pixels) ----------------
PORT_MOODY = [
 ('Port Moody|Anmore', 'anmore-homes-for-sale', 'Anmore',
  [(368, T), (550, T), (550, 179), (541, 179), (541, 222), (512, 222), (512, 180), (477, 180), (475, 165), (447, 166), (439, 177), (424, 181), (368, 181)]),
 ('Port Moody|Barber Street', 'barber-street-port-moody', 'Barber Street',
  [(447, 166), (475, 165), (476, 178), (475, 191), (465, 203), (459, 210), (456, 232), (458, 238), (463, 250), (457, 257), (448, 260), (437, 257), (420, 243), (408, 227), (400, 218), (397, 215),
   (398, 210), (408, 193), (423, 182), (439, 177)]),
 ('Port Moody|Heritage Mountain', 'heritage-mountain-port-moody', 'Heritage Mountain',
  [(477, 180), (512, 180), (512, 222), (541, 222), (541, 240), (590, 241), (589, 257), (580, 262), (580, 279), (578, 284), (565, 290), (560, 299), (554, 305), (551, 302), (549, 292), (543, 289),
   (538, 289), (538, 293), (528, 293), (520, 288), (509, 272), (502, 265), (492, 262), (482, 257), (472, 252), (463, 250), (458, 238), (456, 232), (459, 210), (465, 203), (475, 191), (476, 178)]),
 ('Port Moody|Heritage Woods PM', 'heritage-woods-port-moody', 'Heritage Woods',
  [(550, T), (600, T), (600, 240), (541, 240), (541, 179), (550, 179)]),
 ('Port Moody|Mountain Meadows', 'mountain-meadows-port-moody', 'Mountain Meadows',
  [(590, 241), (596, 241), (596, 257), (601, 257), (601, 289), (588, 281), (580, 280), (580, 262), (589, 257)]),
 ('Port Moody|North Shore Pt Moody', 'north-shore-port-moody', 'North Shore',
  [(368, 181), (424, 181), (408, 193), (398, 210), (397, 215), (400, 218), (408, 227), (420, 243), (437, 257), (448, 260), (457, 257), (463, 250), (472, 252), (482, 257), (492, 262), (502, 265),
   (509, 272), (520, 288), (528, 293), (538, 293), (538, 289), (543, 289), (549, 292), (551, 302), (554, 305), (560, 299), (565, 290), (578, 284), (580, 280), (588, 281), (601, 289), (601, 352),
   (592, 352), (592, 373), (576, 373), (575, 347), (571, 329), (545, 329), (540, 328), (538, 320), (524, 321), (524, 318), (517, 312), (509, 305), (503, 300), (498, 297), (488, 292), (480, 285),
   (467, 280), (458, 277), (448, 267), (443, 262), (432, 258), (420, 247), (415, 238), (407, 232), (402, 233), (400, 238), (396, 237), (392, 228), (387, 218), (382, 210), (372, 209), (371, 199),
   (370, 193)]),
 ('Port Moody|College Park PM', 'college-park-port-moody', 'College Park',
  [(279, 276), (293, 277), (305, 278), (319, 279), (330, 278), (348, 276), (361, 275), (372, 276), (383, 283), (390, 290), (396, 310), (397, 331), (391, 342), (389, 357), (392, 372), (394, 385),
   (391, 403), (392, 420), (339, 420), (339, 381), (281, 381), (279, 381)]),
 ('Port Moody|Glenayre', 'glenayre-port-moody', 'Glenayre', [(281, 381), (339, 381), (339, 420), (281, 420)]),
 ('Port Moody|Port Moody Centre', 'port-moody-centre', 'Port Moody Centre',
  [(383, 283), (390, 290), (401, 299), (408, 308), (415, 317), (424, 328), (433, 340), (441, 347), (452, 355), (465, 358), (470, 358), (483, 356), (495, 358), (505, 353), (512, 351), (523, 348),
   (534, 347), (541, 341), (540, 333), (545, 329), (571, 329), (575, 347), (576, 373), (592, 373), (592, 404), (539, 404), (535, 409), (492, 409), (492, 421), (464, 421), (463, 420), (392, 420),
   (394, 419), (391, 403), (394, 385), (392, 372), (389, 357), (391, 342), (397, 331), (396, 310), (390, 290)]),
]
# ---------------- Port Coquitlam ----------------
PORT_COQ = [
 ('Port Coquitlam|Woodland Acres PQ', 'woodland-acres-port-coquitlam', 'Woodland Acres', [(741, 368), (805, 368), (801, 400), (795, 416), (789, 428), (783, 429), (741, 401)]),
 ('Port Coquitlam|Glenwood PQ', 'glenwood-port-coquitlam', 'Glenwood', [(805, 368), (894, 368), (894, 497), (786, 430), (789, 428), (795, 416), (801, 400)]),
 ('Port Coquitlam|Oxford Heights', 'oxford-heights-port-coquitlam', 'Oxford Heights',
  [(845, 320), (994, 320), (981, 328), (963, 341), (951, 343), (936, 351), (929, 366), (917, 381), (907, 383), (894, 380), (894, 368), (845, 368)]),
 ('Port Coquitlam|Lincoln Park PQ', 'lincoln-park-port-coquitlam', 'Lincoln Park',
  [(894, 380), (907, 383), (917, 381), (929, 366), (936, 351), (951, 343), (963, 341), (981, 328), (994, 320), (994, 417), (894, 417)]),
 ('Port Coquitlam|Birchland Manor', 'birchland-manor-port-coquitlam', 'Birchland Manor',
  [(894, 417), (957, 417), (970, 424), (970, 440), (950, 446), (930, 455), (895, 462)]),
 ('Port Coquitlam|Riverwood', 'riverwood-port-coquitlam', 'Riverwood',
  [(994, 366), (1098, 366), (1092, 378), (1085, 399), (1080, 421), (1071, 442), (1061, 457), (1052, 480), (1042, 507), (1035, 521), (1019, 545), (1007, 566), (985, 554), (940, 524), (894, 497),
   (895, 462), (930, 455), (950, 446), (970, 440), (970, 424), (957, 417), (994, 417)]),
 ('Port Coquitlam|Central Pt Coquitlam', 'central-port-coquitlam', 'Central Port Coquitlam',
  [(741, 401), (786, 430), (894, 497), (940, 524), (985, 554), (1000, 565), (1013, 574), (998, 582), (976, 596), (946, 615), (924, 630), (891, 643), (861, 659), (858, 641), (860, 636),
   (867, 620), (867, 559), (846, 559), (846, 541), (818, 541), (807, 536), (797, 533), (783, 531), (750, 531), (742, 544), (743, 547), (737, 546), (722, 550), (719, 558), (719, 568),
   (716, 562), (711, 555), (708, 548), (707, 540), (705, 530), (707, 508), (707, 498), (706, 485), (706, 473), (722, 471), (733, 466), (741, 458)]),
 ('Port Coquitlam|Mary Hill', 'mary-hill-port-coquitlam', 'Mary Hill',
  [(750, 531), (783, 531), (797, 533), (807, 536), (818, 541), (818, 628), (816, 630), (802, 632), (800, 640), (745, 640), (744, 637), (750, 620), (760, 610), (765, 603), (771, 587), (773, 573),
   (757, 573), (757, 549), (743, 547), (742, 544)]),
 ('Port Coquitlam|Lower Mary Hill', 'lower-mary-hill-port-coquitlam', 'Lower Mary Hill',
  [(818, 541), (846, 541), (846, 559), (867, 559), (867, 620), (858, 635), (820, 636), (818, 630)]),
 ('Port Coquitlam|Citadel PQ', 'citadel-port-coquitlam', 'Citadel',
  [(743, 547), (757, 549), (757, 573), (773, 573), (771, 587), (765, 603), (760, 610), (750, 620), (744, 637), (745, 640), (800, 640), (802, 632), (816, 630), (818, 631), (820, 636), (858, 635),
   (861, 659), (857, 647), (844, 660), (831, 673), (820, 687), (810, 698), (792, 706), (770, 715), (757, 718), (744, 719), (727, 720), (705, 722), (692, 722), (677, 727), (670, 722), (669, 712),
   (676, 705), (684, 696), (694, 683), (698, 674), (699, 664), (692, 656), (678, 654), (667, 650), (667, 637), (665, 628), (669, 620), (685, 612), (691, 603), (686, 598), (688, 592), (700, 585),
   (704, 578), (708, 570), (719, 568), (719, 558), (722, 550), (737, 546)]),
]
# ---------------- Coquitlam leftovers (same ids as the earlier partial slices for CW, CC, ML) ----------------
COQ = [
 ('Coquitlam|Coquitlam West', 'coquitlam-west', 'Coquitlam West',
  [(283, 420), (392, 420), (392, 470), (392, 563), (374, 589), (374, 594), (373, 654), (345, 672), (335, 668), (320, 660), (300, 658), (285, 664), (283, 650)]),
 ('Coquitlam|Central Coquitlam', 'central-coquitlam', 'Central Coquitlam',
  [(392, 470), (590, 470), (590, 598), (587, 600), (580, 610), (546, 616), (546, 657), (544, 657), (520, 646), (500, 644), (476, 629), (464, 617), (463, 594), (374, 594), (374, 589), (392, 563)]),
 ('Coquitlam|Maillardville', 'maillardville-coquitlam', 'Maillardville',
  [(374, 594), (463, 594), (464, 617), (476, 629), (500, 644), (500, 742), (464, 743), (441, 734), (424, 731), (404, 731), (390, 729), (356, 729), (356, 677), (373, 659), (373, 654)]),
 ('Coquitlam|Cape Horn', 'cape-horn', 'Cape Horn',
  [(500, 644), (520, 646), (544, 657), (546, 646), (568, 647), (600, 643), (606, 649), (630, 637), (630, 716), (630, 727), (617, 729), (580, 735), (540, 740), (500, 741)]),
 ('Coquitlam|Coquitlam East', 'coquitlam-east', 'Coquitlam East',
  [(590, 470), (620, 471), (625, 493), (674, 493), (682, 487), (700, 477), (706, 473), (706, 485), (707, 498), (707, 508), (705, 530), (707, 540), (708, 548), (711, 555), (716, 562), (719, 568),
   (708, 570), (704, 578), (700, 585), (688, 592), (686, 598), (691, 603), (685, 612), (669, 620), (665, 628), (667, 637), (667, 650), (678, 654), (692, 656), (699, 664), (698, 674), (694, 683),
   (684, 696), (676, 705), (669, 712), (663, 710), (644, 717), (630, 716), (630, 637), (606, 649), (600, 643), (568, 647), (546, 646), (546, 616), (580, 610), (587, 600), (590, 598)]),
 ('Coquitlam|Westwood Summit CQ', 'westwood-summit-coquitlam', 'Westwood Summit',
  [(596, 241), (602, 241), (611, 246), (620, 250), (629, 254), (633, 258), (600, 257), (596, 254)]),
]
HELD = {'westwood-summit-coquitlam'}   # drawn, kept out of the JSON: no page (5 closed sales)
def to_geo(rings): return [[list(ll(x, y)) for x, y in r] for r in rings]
def build(areas, existing, region, name, out, keep_existing=None):
    from shapely.geometry import Polygon
    from shapely.validation import make_valid
    mine = {a[1] for a in areas}
    keep = [a for a in (keep_existing or []) if a['id'] not in mine]
    others = [(a['id'], [Polygon([(p[1], p[0]) for p in r]) for r in a['rings']]) for a in keep]
    new = []
    for key, slug, nm, poly in areas:
        ring = [list(ll(x, y)) for x, y in poly]
        g = Polygon([(p[1], p[0]) for p in ring])
        if not g.is_valid: g = make_valid(g).buffer(0)
        a0 = g.area
        for eid, polys in others:
            for h in polys:
                if g.intersects(h):
                    ov = g.intersection(h).area
                    if ov > 0.003 * a0: print(f'  {slug}: trimmed {100 * ov / a0:.1f}% against {eid}')
                    g = g.difference(h)
        parts = [g] if g.geom_type == 'Polygon' else sorted([x for x in g.geoms if x.geom_type == 'Polygon'], key=lambda x: -x.area)
        rings = []
        for part in parts:
            if part.area < 0.02 * a0: continue
            c = list(part.exterior.coords); rings.append([[round(y, 5), round(x, 5)] for x, y in c[:-1]] + [[round(c[0][1], 5), round(c[0][0], 5)]])
        if slug in HELD: print('  HELD (no page):', slug, key); others.append((slug, [g])); continue
        # later areas give way to earlier ones too
        others.append((slug, [g]))
        new.append({'id': slug, 'name': nm, 'href': f'/{slug}.html', 'status': 'draft', 'sold': key, 'rings': rings})
    allareas = keep + new
    pts = [p for a in allareas for r in a['rings'] for p in r]; pad = 0.004
    bbox = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    data = dict(existing or {}); data.update({'region': region, 'name': name, 'center': {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}, 'bbox': bbox, 'areas': allareas})
    data = {k: data[k] for k in ('region', 'name', 'center', 'bbox', 'areas') if k in data} | {k: v for k, v in data.items() if k not in ('region', 'name', 'center', 'bbox', 'areas')}
    json.dump(data, open(out, 'w'), separators=(',', ':'))
    print(out.split('/')[-1], len(allareas), 'areas', bbox)
def main():
    if '--check' in sys.argv: print('landmark residuals (name, m north, m east):', residuals())
    build(PORT_MOODY, None, 'port-moody', 'Port Moody', os.path.join(MAPS, 'port-moody.json'))
    build(PORT_COQ, None, 'port-coquitlam', 'Port Coquitlam', os.path.join(MAPS, 'port-coquitlam.json'))
    cq = os.path.join(MAPS, 'coquitlam.json'); ex = json.load(open(cq))
    build(COQ, ex, ex.get('region', 'coquitlam'), ex.get('name', 'Coquitlam'), cq, keep_existing=ex['areas'])
if __name__ == '__main__': main()
