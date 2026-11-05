"""Draft outlines for the Surrey, North Surrey, Cloverdale and Langley sub-areas  ->  src/data/maps/<region>.json

Read from Jared's Paragon "FVREB Sub Areas" screenshots (Paragon-Sub-Area-Boundaries.zip, 2026-11-04) and his boundary-street table, placed on the street grid in
tools/outline_lib.py.  Vertices are (avenue, street).  Straight street edges are as good as the grid (about 70 m); diagonals, river banks and highway edges were read
off the screenshots by eye and are good to about one block (a few hundred metres).  Every area stays 'draft' until Jared confirms it.

  python3 -I tools/build_outlines.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from outline_lib import build, check

def A(i, n, h, board, sub, pts, **kw): return dict(id=i, name=n, href='/' + h + '.html', sold=f'{board}|{sub}', pts=pts, **kw)

REGIONS = {}
# ---------------------------------------------------------------- Surrey (central) + North Surrey
REGIONS['surrey'] = ('Surrey', [
 A('queen-mary-park', 'Queen Mary Park', 'queen-mary-park-surrey', 'Surrey', 'Queen Mary Park Surrey', [(96, 120), (96, 136), (80, 136), (80, 120)]),
 A('west-newton', 'West Newton', 'west-newton', 'Surrey', 'West Newton', [(80, 120), (80, 136), (64, 136), (64, 120)]),
 A('east-newton', 'East Newton', 'east-newton', 'Surrey', 'East Newton', [(80, 136), (79.3, 141), (78.5, 146), (79, 152), (64, 152), (64, 136)]),
 A('bear-creek-green-timbers', 'Bear Creek Green Timbers', 'bear-creek-green-timbers', 'Surrey', 'Bear Creek Green Timbers', [(96, 136), (96, 148.2), (91.3, 152), (79, 152), (78.5, 146), (79.3, 141), (80, 136)]),
 A('fleetwood-tynehead', 'Fleetwood Tynehead', 'fleetwood-tynehead', 'Surrey', 'Fleetwood Tynehead', [(96, 148.2), (96, 160), (103, 160), (97.2, 176), (75.3, 176), (75.3, 175), (71.1, 167.8), (70, 164.8), (70.2, 160.4), (68.8, 156.7), (64, 156.7), (64, 152), (91.3, 152)]),
 A('panorama-ridge', 'Panorama Ridge', 'panorama-ridge', 'Surrey', 'Panorama Ridge', [(64, 120), (64, 136), (62.7, 136), (59.6, 136.4), (56.8, 140.3), (55.4, 144), (52.9, 145.9), (51.5, 146), (51.5, 120)]),
 A('sullivan-station', 'Sullivan Station', 'sullivan-station', 'Surrey', 'Sullivan Station', [(64, 136), (64, 157.7), (62.8, 158.2), (60.8, 159.4), (59.4, 161.2), (57.8, 163.5), (57.4, 163.9), (54.4, 163.9), (54.4, 144.8), (55.4, 144), (56.8, 140.3), (59.6, 136.4), (62.7, 136)]),
 A('whalley', 'Whalley', 'whalley', 'North Surrey', 'Whalley', [(112.2, 128.2), (112.5, 132.2), (108, 136), (108, 144), (100, 144), (100, 140), (96, 140), (96, 132), (102, 132), (108.3, 128.1)]),
 A('guildford', 'Guildford', 'guildford', 'North Surrey', 'Guildford', [(108, 144), (108, 152.1), (103, 160), (96, 160), (96, 140), (100, 140), (100, 144)]),
 A('cedar-hills', 'Cedar Hills', 'cedar-hills', 'North Surrey', 'Cedar Hills', [(105.1, 120), (104.1, 124.9), (105.8, 125), (108.3, 128.1), (102, 132), (96, 132), (96, 120)]),
 A('royal-heights', 'Royal Heights', 'royal-heights', 'North Surrey', 'Royal Heights', [(101.3, 120), (101.2, 118.3), (97.5, 112), (96, 112), (96, 120)]),
 A('bridgeview', 'Bridgeview', 'bridgeview', 'North Surrey', 'Bridgeview', [(97.5, 112), (96.3, 108.1), (106.6, 111.8), (108.1, 113.3), (109.9, 120.9), (112.5, 125), (118.3, 132.3), (112.5, 132.2), (112.2, 128.2), (108.3, 128.1), (105.8, 125), (104.1, 124.9), (105.1, 120), (101.3, 120), (101.2, 118.3)]),
 A('bolivar-heights', 'Bolivar Heights', 'bolivar-heights', 'North Surrey', 'Bolivar Heights', [(118.3, 132.3), (117.2, 148.5), (108, 152.1), (108, 136), (112.5, 132.2)]),
 A('fraser-heights', 'Fraser Heights', 'fraser-heights', 'North Surrey', 'Fraser Heights', [(117.2, 148.5), (116.8, 155), (116.4, 165), (116, 176), (97.2, 176), (103, 160), (108, 152.1)]),
 A('port-kells', 'Port Kells', 'port-kells-surrey', 'North Surrey', 'Port Kells', [(116, 176), (114.5, 185), (113, 194), (112.5, 196), (80, 196), (80, 176)]),
])
# ---------------------------------------------------------------- Cloverdale
REGIONS['cloverdale'] = ('Cloverdale', [
 A('clayton', 'Clayton', 'clayton', 'Cloverdale', 'Clayton', [(80, 176.6), (80, 196), (61.2, 196), (75.3, 175)]),
 A('cloverdale-bc', 'Cloverdale', 'cloverdale-bc', 'Cloverdale', 'Cloverdale BC', [(68.8, 156.6), (70.2, 160.4), (70, 164.8), (71.1, 167.8), (75.3, 175), (61.2, 196), (44.5, 196), (50.1, 192.4), (52.1, 192.2), (52.1, 183.7), (53.9, 176.7), (54.4, 163.9), (57.4, 163.9), (57.8, 163.5), (59.4, 161.2), (60.8, 159.4), (62.8, 158.2), (64.4, 157.7), (66.5, 156.8)]),
 A('serpentine', 'Serpentine', 'serpentine', 'Cloverdale', 'Serpentine', [(54.4, 145), (54.4, 163.9), (53.9, 176.7), (52.1, 183.7), (52.1, 192.2), (50.1, 192.4), (44.5, 196), (32, 196), (32, 168.6), (40, 168.6), (40, 144.5)]),
])

# ---------------------------------------------------------------- Langley (City + Township)
# Highway 1 runs diagonally; read off the screenshots as a straight line through (82.5 Ave, 216.4 St) falling 0.6 avenue per street.
def H(s): return round(82.5 - 0.6 * (s - 216.4), 1)
BORDER = -0.81            # the US border sits at 49.0003 N, a little south of the avenue grid's "0 Ave"
# Fraser River south bank (Edgewater Bar and Fort Langley wharf checked on Google Maps, the rest read off the screenshots, good to about 300 m)
RIVER_W = [(112.5, 196), (113, 207), (113, 216.4)]
RIVER_FL = [(108, 222), (103, 225.5), (97, 229), (94, 231.6), (92, 236), (90.3, 240)]
RIVER_CL = [(88.3, 250), (88.3, 264), (88, 276)]
# Langley City outline notch and its eastern bump (Langley Bypass), shared with Willoughby, Murrayville, Brookswood and Salmon River
LC_NW = [(61.2, 196), (60.1, 197.7), (60.2, 197.9), (61.6, 197.9), (62, 198.5)]
LC_N = [(62, 208.1), (60.7, 209.0)]
LC_BUMP = [(60.1, 208.4), (58.2, 211.1), (56.1, 209.7), (56, 210.84)]
HWY_PT = (H(223.5), 223.5)
REGIONS['langley'] = ('Langley', [
 A('walnut-grove', 'Walnut Grove', 'walnut-grove', 'Langley', 'Walnut Grove', [(H(196), 196), (H(216.4), 216.4)] + RIVER_W[::-1]),
 A('fort-langley', 'Fort Langley', 'fort-langley', 'Langley', 'Fort Langley', [(H(216.4), 216.4), (113, 216.4)] + RIVER_FL + [(H(240), 240), HWY_PT]),
 A('county-line-glen-valley', 'County Line Glen Valley', 'county-line-glen-valley', 'Langley', 'County Line Glen Valley', [(H(240), 240), (90.3, 240)] + RIVER_CL + [(H(276), 276)]),
 A('willoughby-heights', 'Willoughby Heights', 'willoughby-heights', 'Langley', 'Willoughby Heights', [(H(196), 196), (H(216.4), 216.4), HWY_PT, LC_N[1], LC_N[0]] + LC_NW[::-1]),
 A('salmon-river', 'Salmon River', 'salmon-river', 'Langley', 'Salmon River', [HWY_PT, (H(240), 240), (H(276), 276), (40, 276), (40, 264.1), (33.7, 264.1), (33.7, 260.1), (39.8, 240.1), (45.4, 224), (56, 224), (56, 210.84)] + LC_BUMP[::-1][1:] + [LC_N[1]]),
 A('langley-city', 'Langley City', 'langley-city', 'Langley', 'Langley City', LC_NW + LC_N + LC_BUMP + [(47.9, 210.84), (47.9, 210.1), (47, 210.05), (45.1, 210), (45.1, 207.9), (44, 207.9), (44, 196)]),
 A('murrayville', 'Murrayville', 'murrayville', 'Langley', 'Murrayville', [(56, 210.84), (56, 224), (40, 224), (40, 213.8), (42.6, 213.1), (44.4, 212), (45.8, 211.2), (47.3, 211.1), (47.9, 210.84)]),
 A('brookswood', 'Brookswood', 'brookswood', 'Langley', 'Brookswood Langley', [(44, 196), (44, 207.9), (45.1, 207.9), (45.1, 210), (47, 210.05), (47.9, 210.1), (47.9, 210.84), (47.3, 211.1), (45.8, 211.2), (44.4, 212), (42.6, 213.1), (40, 213.8), (40, 216.3), (28, 216.3), (28, 208.2), (20, 208.2), (20, 204.2), (16, 204.6), (16, 196)]),
 A('campbell-valley', 'Campbell Valley', 'campbell-valley', 'Langley', 'Campbell Valley', [(40, 216.3), (40, 224), (45.4, 224), (39.8, 240.1), (BORDER, 240.1), (BORDER, 196), (16, 196), (16, 204.6), (20, 204.2), (20, 208.2), (28, 208.2), (28, 216.3)]),
 A('otter-district', 'Otter District', 'otter-district', 'Langley', 'Otter District', [(39.8, 240.1), (33.7, 260.1), (28, 260.1), (28, 264.1), (24, 264.1), (24, 276), (BORDER, 276), (BORDER, 240.1)]),
 A('aldergrove', 'Aldergrove', 'aldergrove', 'Langley', 'Aldergrove Langley', [(40, 264.1), (40, 276), (24, 276), (24, 264.1), (28, 264.1), (28, 260.1), (33.7, 260.1), (33.7, 264.1)]),
])

# ---------------------------------------------------------------- Maple Ridge and Pitt Meadows
# The Metro Vancouver street grid carries on east of Surrey, so these use the same lat/lng formulas.  Corners were read off a 2x enlargement of the Paragon
# close-up (c32a: left half, c32b: right half) and converted through two label-fitted formulas.  Only the polygons whose whole outline is on the screenshots are
# drawn: North Meadows, Silver Valley, Websters Corners and Northeast run off the top of the screenshots (north to Pitt Lake / Golden Ears Park), so they are not drawn.
def _ca(cx, cy):
    x, y = cx / 2, 190 + cy / 2
    return (round(132 - (y - 335) / 10.6, 2), round(240 + (x - 799) / 10.75, 2))
def _cb(cx, cy):
    x, y = 560 + cx / 2, 190 + cy / 2
    return (round(132 - (y - 335) / 10.6, 2), round(240 + (x - 799) / 10.75, 2))
a_ = lambda l: [_ca(*p) for p in l]
b_ = lambda l: [_cb(*p) for p in l]
TH_S, TH_SE = (94.3, 272.0), (94.2, 287.5)
REGIONS['maple-ridge'] = ('Maple Ridge', [
 A('north-maple-ridge', 'North Maple Ridge', 'north-maple-ridge-guide', 'Maple Ridge', 'North Maple Ridge', a_([(918, 190), (1095, 190), (1095, 127), (1256, 127), (1256, 288), (1018, 288), (918, 288)])),
 A('northwest-maple-ridge', 'Northwest Maple Ridge', 'northwest-maple-ridge', 'Maple Ridge', 'Northwest Maple Ridge', a_([(830, 288), (918, 288), (1018, 288), (1018, 545), (727, 545), (757, 522), (757, 415), (830, 413)])),
 A('west-central', 'West Central', 'west-central', 'Maple Ridge', 'West Central', a_([(1018, 288), (1256, 288), (1256, 655), (1018, 665), (1018, 545)])),
 A('southwest-maple-ridge', 'Southwest Maple Ridge', 'southwest-maple-ridge', 'Maple Ridge', 'Southwest Maple Ridge', a_([(727, 545), (1018, 545), (1018, 665), (1000, 668), (900, 700), (800, 748), (727, 795)])),
 A('east-central', 'East Central', 'east-central', 'Maple Ridge', 'East Central', a_([(1256, 288)]) + b_([(300, 286), (360, 300), (440, 350), (478, 420), (480, 550), (307, 550), (307, 748), (280, 765)]) + a_([(1256, 655)])),
 A('cottonwood', 'Cottonwood', 'cottonwood-mr', 'Maple Ridge', 'Cottonwood MR', b_([(307, 550), (655, 550), (655, 735), (600, 735), (530, 795), (470, 810), (390, 770), (340, 745), (307, 748)])),
 A('albion', 'Albion', 'albion', 'Maple Ridge', 'Albion', b_([(307, 748), (340, 745), (390, 770), (470, 810), (530, 795), (600, 735), (655, 735), (655, 1000), (612, 1072), (450, 990), (300, 880), (280, 765)])),
 A('thornhill', 'Thornhill', 'thornhill-mr', 'Maple Ridge', 'Thornhill MR', b_([(655, 735), (690, 705), (760, 652), (850, 660), (930, 695), (968, 735), (1010, 690), (1040, 650), (1100, 615), (1165, 610)]) + [TH_S] + b_([(612, 1072), (655, 1000)])),
 A('whonnock', 'Whonnock', 'whonnock', 'Maple Ridge', 'Whonnock', b_([(1165, 553)]) + [(120, 287.5), TH_SE, TH_S] + b_([(1165, 610)])),
])
REGIONS['pitt-meadows'] = ('Pitt Meadows', [
 A('west-meadows', 'West Meadows', 'west-meadows-pitt-meadows-guide', 'Pitt Meadows', 'West Meadows', a_([(240, 208), (482, 376), (482, 707), (380, 655), (250, 615), (100, 590), (20, 545), (8, 440), (40, 385), (130, 322), (200, 262)])),
 A('mid-meadows', 'Mid Meadows', 'mid-meadows-pitt-meadows', 'Pitt Meadows', 'Mid Meadows', a_([(482, 376), (757, 522), (727, 574), (487, 430)])),
 A('central-meadows', 'Central Meadows', 'central-meadows-pitt-meadows', 'Pitt Meadows', 'Central Meadows', a_([(487, 430), (727, 574), (727, 586), (567, 588), (567, 610), (487, 610)])),
 A('south-meadows', 'South Meadows', 'south-meadows-pitt-meadows', 'Pitt Meadows', 'South Meadows', a_([(487, 610), (567, 610), (567, 588), (727, 588), (727, 795), (600, 772), (487, 707)])),
])

# ---------------------------------------------------------------- Delta (North Delta and the Ladner core)
# North Delta: corners from a 6x enlargement of the overview screenshot (c21n); the avenues and streets there are Surrey's (120 St and 84/72/64 Ave edges line up with
# West Newton), so they are placed on the same grid.  Ladner: the close-up screenshot was fitted to Google coordinates of five landmarks (Boundary Bay Airport,
# Ladner Leisure Centre, Watershed Park, OWL, Brunswick Point; fit error under 10 m), corners read off a 4x enlargement (c22a).
def _cn(cx, cy): return (round(84 - (cy - 545) / 32, 2), round(120 + (cx - 637) / 32, 2))
def _cl(cx, cy):
    x, y = 380 + cx / 4, 330 + cy / 4
    la, lo = 49.0806 - (y - 519) * 0.000169, -123.0088 + (x - 751) * 0.0002575
    return (round((la - 49.001776) / 0.0018276, 2), round((lo + 123.220335) / 0.0027568, 2))
n_ = lambda l: [_cn(*p) for p in l]
def _cs(cx, cy):   # 4x enlargement of the right-hand strip of the Ladner close-up (c22s), same landmark fit as _cl
    x, y = 1040 + cx / 4, 190 + cy / 4
    la, lo = 49.0806 - (y - 519) * 0.000169, -123.0088 + (x - 751) * 0.0002575
    return (round((la - 49.001776) / 0.0018276, 2), round((lo + 123.220335) / 0.0027568, 2))
s_ = lambda l: [_cs(*p) for p in l]
H91 = [(90, 90), (95, 230), (100, 330), (105, 380), (130, 430), (190, 490), (260, 535), (330, 570), (400, 610), (440, 660), (480, 740), (520, 820), (560, 910), (600, 1000), (640, 1085)]   # Highway 91 edge
l_ = lambda l: [_cl(*p) for p in l]
REGIONS['delta'] = ('Delta', [
 A('annieville', 'Annieville', 'annieville', 'N. Delta', 'Annieville', n_([(245, 160), (637, 165), (637, 540), (380, 540), (380, 295), (345, 262), (225, 215)])),
 A('nordel', 'Nordel', 'nordel', 'N. Delta', 'Nordel', n_([(225, 215), (345, 262), (380, 295), (380, 935), (190, 935), (150, 880), (110, 800), (60, 640), (30, 525), (100, 400), (190, 300)])),
 A('scottsdale', 'Scottsdale', 'scottsdale', 'N. Delta', 'Scottsdale', n_([(380, 545), (637, 545), (637, 935), (380, 935)])),
 A('sunshine-hills', 'Sunshine Hills', 'sunshine-hills-woods', 'N. Delta', 'Sunshine Hills Woods', n_([(190, 935), (637, 935)]) + [(48.2, 120.0)] + s_(H91[::-1])),
 A('holly', 'Holly', 'holly', 'Ladner', 'Holly', l_([(733, 160), (1105, 398), (1078, 430), (1055, 742), (895, 788), (865, 783), (865, 742), (733, 742)])),
 A('hawthorne', 'Hawthorne', 'hawthorne', 'Ladner', 'Hawthorne', l_([(500, 235), (600, 345), (733, 398), (733, 565), (325, 563), (322, 500)])),
 A('delta-manor', 'Delta Manor', 'delta-manor', 'Ladner', 'Delta Manor', l_([(325, 563), (733, 565), (733, 742), (420, 742), (412, 740), (392, 645)])),
 A('ladner-elementary', 'Ladner Elementary', 'ladner-elementary', 'Ladner', 'Ladner Elementary', l_([(145, 595), (295, 495), (325, 563), (392, 645), (412, 740), (385, 815), (215, 815), (145, 740)])),
 A('neilsen-grove', 'Neilsen Grove', 'neilsen-grove', 'Ladner', 'Neilsen Grove', l_([(610, 10), (500, 235), (322, 500), (300, 492), (165, 548), (150, 525), (235, 430), (325, 395), (270, 350), (345, 290), (395, 205), (335, 100), (345, 40)])),
])

# ---------------------------------------------------------------- Abbotsford
# Only three FVREB sub-areas.  The two Paragon screenshots (overview ab1, close-up ab2) were fitted to Google coordinates of landmarks (Abbotsford International
# Airport, Abbotsford Recreation Centre, Silverbrook Farm, Gurdwara Kalgidhar Darbar Sahib, Castle Fun Park; fit error under 20 m).  Corners are good to about 100 m.
def _inv(la, lo): return (round((la - 49.001776) / 0.0018276, 3), round((lo + 123.220335) / 0.0027568, 3))
def _p1(x, y): return _inv(49.06556 - (y - 372) * 0.0001687, -122.4273 + (x - 162) * 0.0002575)
def _p2(x, y): return _inv(49.06556 - (y - 301) * 0.0000843, -122.37482 + (x - 332) * 0.0001288)
def _bd(x): return (round((49.0003 - 49.001776) / 0.0018276, 3), _inv(0, -122.4273 + (x - 162) * 0.0002575)[1])   # a point on the US border straight below pixel x
p1_ = lambda l: [_p1(*p) for p in l]
p2_ = lambda l: [_p2(*p) for p in l]
AB_CW = p2_([(720, 203), (720, 290), (793, 293), (793, 552), (747, 552), (747, 592), (793, 592), (795, 668)])    # Central's west edge (with the Mill Lake Park box)
AB_CE = p2_([(1022, 203), (1022, 330), (1085, 335), (1130, 375), (1143, 440), (1140, 520), (1135, 600), (1170, 688)])   # Central's east edge
AB_HWY_C = p2_([(935, 685)])
REGIONS['abbotsford'] = ('Abbotsford', [
 A('abbotsford-west', 'Abbotsford West', 'abbotsford-west', 'Abbotsford', 'Abbotsford West', p2_([(282, 200), (720, 200)]) + AB_CW[1:] + p2_([(645, 655), (282, 405)])),
 A('central-abbotsford', 'Central Abbotsford', 'central-abbotsford', 'Abbotsford', 'Central Abbotsford', AB_CW + AB_HWY_C + AB_CE[::-1]),
 A('aberdeen', 'Aberdeen', 'aberdeen', 'Abbotsford', 'Aberdeen', [_p1(37.5, 247), p2_([(282, 405)])[0], _p1(341.5, 540), _p1(250, 670), _bd(251.5), _bd(37.5)]),
 A('poplar', 'Poplar', 'poplar', 'Abbotsford', 'Poplar', p2_([(282, 405), (645, 655), (795, 668), (935, 685), (1170, 688)]) + [_p1(867.5, 573), _bd(867.5), _bd(251.5), _p1(250, 670), _p1(341.5, 540)]),
 A('abbotsford-east', 'Abbotsford East', 'abbotsford-east', 'Abbotsford', 'Abbotsford East', AB_CE + p1_([(900, 568), (1005, 515), (1045, 487), (1025, 455), (1025, 238), (810, 285), (810, 325)])),
])

if __name__ == '__main__':
    only = sys.argv[1:] or list(REGIONS)
    for r in only:
        name, areas = REGIONS[r]
        out = build(r, name, areas)
        print(r, len(areas), 'areas', check(out))
