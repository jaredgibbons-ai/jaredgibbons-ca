"""Draft outlines for the New Westminster sub-areas -> src/data/maps/new-westminster.json

Source: Jared's Paragon map search, GVR Sub Areas 2022 layer, two screenshots of 2026-11-05 (a close-up of the city and an overview that shows The Heights, Sapperton and
Queensborough in full), read by eye.  Codes on the layer: WE West End, MP Moody Park, UP Uptown, GN GlenBrooke North, QP Queens Park, FV Fraserview, TH The Heights,
SA Sapperton, DT Downtown, QY Quay, CH Connaught Heights, QB Queensborough (NA, the Stewardson Way strip, has no sales and no page, so it is not drawn).
Pixels are turned into latitude and longitude with a Web Mercator fit to five Google Maps landmark coordinates (tamasewtx Aquatic and Community Centre, Anvil Centre,
Nikkei National Museum, Edmonds and 22nd Street stations, Sapperton).  The overview is related to the close-up with a scale-and-shift fit to shared corners.
Straight street edges are good to about 100 m; the river shores, the top of Sapperton and the north end of The Heights are good to a block or two.  Every area stays 'draft'.
  python3 -I tools/build_nw_outlines.py [--check]"""
import json, math, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
# close-up screenshot (1280 x 800): icon centres and Google coordinates
LAND = [(679, 296.5, 49.2212863, -122.9081213), (655.5, 532.5, 49.2016438, -122.9112435), (240, 340, 49.2177915, -122.9645852),
        (281.5, 414, 49.2123184, -122.9591665), (360, 561, 49.199946, -122.9491205), (825, 266.5, 49.2246991, -122.8894176)]
def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
def ls(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n; a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); return a, my - a * mx
(LX, LB) = ls([p[0] for p in LAND], [p[3] for p in LAND]); (MY, MB) = ls([p[1] for p in LAND], [merc(p[2]) for p in LAND])
def ll(px, py):
    lat = math.degrees(2 * math.atan(math.exp(MY * py + MB)) - math.pi / 2); return round(lat, 5), round(LX * px + LB, 5)
def residuals():
    return [(round((ll(p[0], p[1])[0] - p[2]) * 111200), round((ll(p[0], p[1])[1] - p[3]) * 73000)) for p in LAND]
# frames: the polygons below were read off enlarged crops, so each vertex is converted to close-up pixels
def C(cx, cy): return (260 + cx / 2, 190 + cy / 2)                    # close-up crop, 2x, origin (260,190)
def o1(cx, cy): return (560 + cx / 5, 200 + cy / 5)                   # overview crop 1, 5x, origin (560,200) -> overview pixels
def o2(cx, cy): return (470 + cx / 5, 440 + cy / 5)                   # overview crop 2, 5x, origin (470,440) -> overview pixels
# overview pixels -> close-up pixels (shared corners: GlenBrooke top, Queens Park corners, Fraserview corners)
PAIRS = [((656, 335), C(697, 157)), ((690, 365), C(840, 282)), ((672, 436), C(790, 578)), ((644, 401), C(655, 428)), ((719, 414), C(958, 465)), ((703, 353), C(880, 235)), ((750, 358), C(1088, 255))]
(SX, SB) = ls([a[0] for a, b in PAIRS], [b[0] for a, b in PAIRS]); (SY, SC) = ls([a[1] for a, b in PAIRS], [b[1] for a, b in PAIRS])
def ov(p): return (SX * p[0] + SB, SY * p[1] + SC)
def pair_error(): return [(round(ov(a)[0] - b[0], 1), round(ov(a)[1] - b[1], 1)) for a, b in PAIRS]
def P(frame, pts): return [frame(*p) if frame in (C,) else ov(frame(*p)) for p in pts]
AREAS = [  # sold-aggregate key, page slug, display name, polygons (list of rings) in close-up pixels
 ('New Westminster|West End NW', 'west-end-new-westminster', 'West End', [P(C, [(158, 603), (378, 427), (385, 405), (470, 550), (360, 685), (255, 738)])]),
 ('New Westminster|Moody Park', 'moody-park', 'Moody Park', [P(C, [(385, 405), (500, 328), (548, 303), (592, 478), (470, 550)])]),
 ('New Westminster|Uptown NW', 'uptown-new-westminster', 'Uptown', [P(C, [(548, 303), (655, 428), (790, 578), (648, 727), (575, 697), (520, 668), (440, 652), (360, 685), (470, 550), (592, 478)])]),
 ('New Westminster|GlenBrooke North', 'glenbrooke-north', 'GlenBrooke North', [P(C, [(697, 157), (810, 248), (840, 282), (655, 428), (548, 303)])]),
 ('New Westminster|Queens Park', 'queens-park', "Queen's Park", [P(C, [(840, 282), (955, 445), (960, 470), (790, 578), (655, 428)])]),
 ('New Westminster|Fraserview NW', 'fraserview-nw', 'Fraserview', [P(C, [(880, 235), (1088, 255), (1085, 300), (1040, 400), (1000, 458), (965, 470), (955, 445), (840, 282)])]),
 ('New Westminster|Downtown NW', 'downtown-nw', 'Downtown', [P(C, [(790, 578), (958, 470), (1000, 478), (960, 540), (880, 615), (790, 690), (700, 735), (655, 728)])]),
 ('New Westminster|Quay', 'quay', 'Quay', [P(C, [(648, 727), (700, 735), (790, 692), (765, 745), (685, 778), (595, 773), (515, 738), (508, 700), (520, 668), (575, 697)])]),
 ('New Westminster|Connaught Heights', 'connaught-heights', 'Connaught Heights', [P(C, [(35, 708), (158, 603), (255, 738), (205, 792), (130, 800), (95, 760)])]),
 ('New Westminster|The Heights NW', 'the-heights-new-westminster', 'The Heights', [P(o1, [(485, 672), (568, 590), (905, 320), (912, 270), (945, 272), (945, 452), (835, 455), (830, 787), (716, 766), (642, 808), (555, 708)])]),
 ('New Westminster|Sapperton', 'sapperton-new-westminster', 'Sapperton', [P(o1, [(950, 340), (1195, 378), (950, 745), (950, 790), (830, 787), (835, 455), (945, 452)])]),
 ('New Westminster|Queensborough', 'queensborough', 'Queensborough', [P(o2, [(400, 300), (480, 285), (840, 315), (850, 335), (620, 570), (530, 680), (390, 790), (150, 890), (150, 520), (215, 470)]),
                                                                    P(o2, [(480, 240), (545, 205), (640, 205), (720, 245), (690, 262), (520, 255)])]),
]
def main():
    if '--check' in sys.argv: print('landmark residuals (m north, m east):', residuals(), '| overview fit error (px):', pair_error())
    pts = []; areas = []
    for key, slug, name, polys in AREAS:
        rings = []
        for poly in polys:
            r = [list(ll(x, y)) for x, y in poly]; r.append(r[0]); rings.append(r); pts += r
        areas.append({'id': slug, 'name': name, 'href': f'/{slug}.html', 'status': 'draft', 'sold': key, 'rings': rings})
    pad = 0.004; bbox = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    out = {'region': 'new-westminster', 'name': 'New Westminster', 'center': {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}, 'bbox': bbox, 'areas': areas}
    json.dump(out, open(os.path.join(ROOT, 'src/data/maps/new-westminster.json'), 'w'), separators=(',', ':'))
    print(len(areas), 'areas', bbox)
if __name__ == '__main__': main()
