"""Draft outlines for the nine South Surrey / White Rock MLS sub-areas  ->  src/data/maps/south-surrey-white-rock.json

Our own drawing, from the boundary streets Jared read off Paragon's FVREB Sub Areas layer (2026-11-04).
Grid fitted to 7 street-intersection coordinates looked up on Google Maps (152 St & 16 Ave, 152 St & 40 Ave, 128 St & 24 Ave, 192 St & 24 Ave,
168 St & 32 Ave, 140 St & 28 Ave, 176 St & 20 Ave); every one of them landed within ~30 m of the fitted grid.  Coast and King George Blvd points are
hand-placed from a handful of named places and are DRAFT-quality (a block or two).  Every area stays status 'draft' until Jared confirms it.

  python3 -I tools/build_ssw_outlines.py
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def lat(a): return round(49.03117 + (a - 16) * 0.0018117, 5)
def lon(s): return round(-122.80112 + (s - 152) * (0.002743 if s >= 152 else 0.002762), 5)
BORDER = 49.0003
HW = 0.0025   # half-width of the King George Blvd strip, degrees of longitude

# King George Blvd centreline (lat, lng), north to south.  Google Maps intersection points at 40, 32, 28, 24, 20, 16 and 8 Ave plus the Peace Arch crossing.
KGB = [(lat(40), -122.8219), (lat(32), -122.8118), (lat(28), -122.8040), (lat(24), -122.7934), (lat(20), -122.7846), (lat(16), -122.7757), (lat(8), -122.7622), (BORDER, -122.7577)]
def kgb_lon(a):
    """KGB longitude at avenue a (linear between the placed points)."""
    la = lat(a)
    for (y0, x0), (y1, x1) in zip(KGB, KGB[1:]):
        if y1 <= la <= y0: return x0 + (x1 - x0) * (y0 - la) / (y0 - y1)
    raise ValueError(a)
def kgb_side(sign, pts_lat=None):
    return [(y, round(x + sign * HW, 5)) for y, x in KGB]

# Coast (lat, lng) west to east: Crescent Beach shore, Kwomais Point, White Rock shore, Semiahmoo.
W_COAST = [(49.0600, -122.8845), (49.0560, -122.8905), (49.0500, -122.8925), (49.0420, -122.8905), (49.0360, -122.8850), (49.0300, -122.8770), (49.0262, -122.8705)]  # Blackie Spit -> Kwomais Point
S_COAST = [(49.0262, -122.8705), (49.0262, -122.8640), (49.0252, -122.8560), (49.0240, lon(136)), (49.0228, -122.8310), (49.0215, -122.8180), (49.0203, -122.8057), (49.0185, -122.7960), (49.0178, -122.7860), (49.0166, lon(160))]
E_COAST = [(49.0166, lon(160)), (49.0147, -122.7777), (49.0090, -122.7700), (49.0030, -122.7620), (BORDER, -122.7600)]  # 160 St -> Semiahmoo FN -> Peace Arch

def close(p): return p + [p[0]]
def kgb_east(a_from, a_to):
    """KGB east edge going from avenue a_from (north) to a_to (south), including the placed points between."""
    out = []
    for y, x in kgb_side(+1):
        if lat(a_from) >= y >= lat(a_to) or (y == KGB[-1][0]): out.append((y, x))
    return out

A = {}
# Crescent Beach (incl. Ocean Park): N Blackie Spit / Nicomekl near Crescent Rd; E 128 St to 20 Ave then 136 St; S ocean at Kwomais Pt.
A['crescent-beach'] = close([(49.0598, -122.8845), (49.0585, -122.8790), (49.0560, -122.8730), (49.0545, lon(128)), (lat(20), lon(128)), (lat(20), lon(136)), (49.0240, lon(136))]
                            + list(reversed(S_COAST[:4]))[0:0] + [(49.0252, -122.8560), (49.0262, -122.8640)] + [(49.0262, -122.8705)] + list(reversed(W_COAST[:-1]))[0:0] + W_COAST[-2::-1])
# Elgin Chantrell: N 40 Ave; W 128 St below Crescent Rd then diagonal into Mud Bay; S 20 Ave (128-140) then 28 Ave (140-KGB); E 140 St to 28 Ave then W side of KGB to 40 Ave.
A['elgin-chantrell'] = close([(lat(40), lon(136)), (lat(40), round(-122.8219 - HW, 5)), (lat(32), round(-122.8118 - HW, 5)), (lat(28), lon(152)),
                              (lat(28), lon(140)), (lat(20), lon(140)), (lat(20), lon(128)), (49.0545, lon(128))])
# Sunnyside Park: N 28 Ave; W 140 St (28-20 Ave) then 136 St (20-16 Ave); S 16 Ave; E 152 St.
A['sunnyside-park'] = close([(lat(28), lon(140)), (lat(28), lon(152)), (lat(16), lon(152)), (lat(16), lon(136)), (lat(20), lon(136)), (lat(20), lon(140))])
# King George Corridor: strip along KGB; W 152 St (28-16 Ave) then 160 St to Marine Dr; E east edge of the highway; S border at Peace Arch.
A['king-george-corridor'] = close([(round(lat(40) - 0.0003, 5), round(-122.8219, 5)), (lat(32), round(-122.8118 - HW, 5)), (lat(28), lon(152)), (lat(16), lon(152)), (lat(16), lon(160)), (49.0166, lon(160))]
                                   + E_COAST[1:] + [(BORDER, -122.7552)] + [(y, (-122.7990 if y == lat(28) else x)) for y, x in reversed(kgb_side(+1)[1:-1])] + [(round(lat(40) - 0.0003, 5), round(-122.8219 + HW, 5))])
# White Rock: N 16 Ave; W ~136 St; E 160 St; S Semiahmoo Bay.
A['white-rock'] = close([(lat(16), lon(136)), (lat(16), lon(160)), (49.0166, lon(160))] + list(reversed(S_COAST[3:-1])) + [(49.0240, lon(136))])
# Morgan Creek: N 40 Ave; S 32 Ave; W KGB; E 168 St.
A['morgan-creek'] = close([(lat(40), round(-122.8219 + HW, 5)), (lat(40), lon(168)), (lat(32), lon(168)), (lat(32), round(-122.8118 + HW, 5))])
# Grandview Surrey: N 32 Ave; W east edge of KGB; E 176 St; S 20 Ave to 168 St then 24 Ave (168-176 St).
A['grandview'] = close([(lat(32), round(-122.8118 + HW, 5)), (lat(32), lon(176)), (lat(24), lon(176)), (lat(24), lon(168)), (lat(20), lon(168)), (lat(20), round(kgb_lon(20) + HW, 5)), (lat(24), round(kgb_lon(24) + HW, 5)), (lat(28), -122.7990)])
# Pacific Douglas: N 20 Ave (west of 168 St) and 24 Ave (east of it); W KGB; E 176 St; S US border.
A['pacific-douglas'] = close([(lat(20), round(kgb_lon(20) + HW, 5)), (lat(20), lon(168)), (lat(24), lon(168)), (lat(24), lon(176)), (BORDER, lon(176)), (BORDER, -122.7552), (lat(8), round(-122.7622 + HW, 5)), (lat(16), round(-122.7757 + HW, 5))])
# Hazelmere: N 32 Ave; W 176 St; E 192 St; S US border.
A['hazelmere'] = close([(lat(32), lon(176)), (lat(32), lon(192)), (BORDER, lon(192)), (BORDER, lon(176))])

META = [  # id, name, href, sold key, group
 ('crescent-beach', 'Crescent Beach & Ocean Park', '/crescent-bch-ocean-pk.html', 'Crescent Bch Ocean Pk.', True),
 ('elgin-chantrell', 'Elgin Chantrell', '/elgin-chantrell.html', 'Elgin Chantrell', False),
 ('sunnyside-park', 'Sunnyside Park', '/sunnyside-park-surrey.html', 'Sunnyside Park Surrey', False),
 ('king-george-corridor', 'King George Corridor', '/king-george-corridor.html', 'King George Corridor', False),
 ('white-rock', 'White Rock', '/white-rock.html', 'White Rock', False),
 ('morgan-creek', 'Morgan Creek', '/morgan-creek.html', 'Morgan Creek', False),
 ('grandview', 'Grandview Heights', '/grandview-surrey.html', 'Grandview Surrey', False),
 ('pacific-douglas', 'Pacific Douglas', '/pacific-douglas.html', 'Pacific Douglas', False),
 ('hazelmere', 'Hazelmere', '/hazelmere.html', 'Hazelmere', False),
]
areas = []
for i, n, h, s, g in META:
    ring = [[round(y, 5), round(x, 5)] for y, x in A[i]]
    a = {'id': i, 'name': n, 'href': h, 'status': 'draft', 'sold': 'South Surrey White Rock|' + s}
    if g: a['group'] = True
    a['rings'] = [ring]; areas.append(a)
allp = [p for a in areas for r in a['rings'] for p in r]
pad = 0.004
bbox = [round(min(p[0] for p in allp) - pad, 4), round(min(p[1] for p in allp) - pad, 4), round(max(p[0] for p in allp) + pad, 4), round(max(p[1] for p in allp) + pad, 4)]
out = {'region': 'south-surrey-white-rock', 'name': 'South Surrey and White Rock', 'center': {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}, 'bbox': bbox, 'areas': areas}
json.dump(out, open(os.path.join(ROOT, 'src/data/maps/south-surrey-white-rock.json'), 'w'), separators=(',', ':'))
print('wrote', len(areas), 'areas, bbox', bbox)
