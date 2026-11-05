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

if __name__ == '__main__':
    only = sys.argv[1:] or list(REGIONS)
    for r in only:
        name, areas = REGIONS[r]
        out = build(r, name, areas)
        print(r, len(areas), 'areas', check(out))
