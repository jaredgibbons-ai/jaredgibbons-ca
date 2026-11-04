"""'Areas near X' block (gen 'near2') from the neighbourhood centre points in src/data/area-coordinates.csv (Muse research of 2026-11-03: OpenStreetMap, Wikipedia, municipal pages).

Only precise points are used: a row whose point is a municipal-hall / city-level fallback, a point shared by two areas, or a whole-city entry is skipped, because a distance
from a fallback point would be invented precision. A page gets the block when it has a precise point and at least 3 other precise areas within 25 km.
Distances are straight-line (great circle) between centre points, shown nearest first with the compass direction; they are not driving distances and the text says so.
Links go only to pages that exist. Re-runnable: removes its own blocks first.   python3 -I tools/build_area_near.py [--dry]"""
import csv, glob, json, math, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
LOCAL = os.path.join(ROOT, 'src/data/local'); PAGES = os.path.join(ROOT, 'src/data/pages'); GEN = 'near2'
FB = re.compile(r'fallback|municipal hall|municipal point|municipality point|city hall|city coordinates|city point|wikipedia city|point for burnaby|point for new west', re.I)
MAXKM, NEED, SHOW = 25.0, 3, 8
def hav(a, b):
    p1, p2 = math.radians(a[0]), math.radians(b[0]); dl = math.radians(b[1] - a[1]); dp = p2 - p1
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 6371.0 * 2 * math.asin(math.sqrt(h))
def bearing(a, b):
    p1, p2 = math.radians(a[0]), math.radians(b[0]); dl = math.radians(b[1] - a[1])
    x = math.sin(dl) * math.cos(p2); y = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    deg = (math.degrees(math.atan2(x, y)) + 360) % 360
    return ['north', 'north-east', 'east', 'south-east', 'south', 'south-west', 'west', 'north-west'][int((deg + 22.5) // 45) % 8]
def clean(name, city):
    n = re.sub(r',\s*' + re.escape(city) + r'$', '', name.strip()); return re.sub(r'\s*\([^)]*\)$', '', n)
def km(d): return f'{d:.1f} km' if d < 10 else f'{round(d)} km'
def load():
    rows = list(csv.DictReader(open(os.path.join(ROOT, 'src/data/area-coordinates.csv'), encoding='utf-8')))
    dup = {}
    for r in rows: dup[(r['lat'], r['lon'])] = dup.get((r['lat'], r['lon']), 0) + 1
    out = []
    for r in rows:
        if FB.search(r['point_is']) or dup[(r['lat'], r['lon'])] > 1: continue
        if clean(r['area'], r['city']).lower() == r['city'].lower(): continue          # a whole city, not a neighbourhood
        out.append({**r, 'name': clean(r['area'], r['city']), 'pt': (float(r['lat']), float(r['lon']))})
    return out
def main():
    dry = '--dry' in sys.argv; P = load()
    slugs = {os.path.basename(p)[:-5] for p in glob.glob(PAGES + '/*.json')} | {os.path.basename(p)[:-5] for p in glob.glob(LOCAL + '/*.json')}
    P = [r for r in P if r['page'] in slugs]
    by = {}
    for r in P:
        near = sorted(((hav(r['pt'], o['pt']), o) for o in P if o['page'] != r['page']), key=lambda x: x[0])
        near = [(d, o) for d, o in near if d <= MAXKM][:SHOW]
        if len(near) >= NEED: by[r['page']] = (r, near)
    print('precise areas', len(P), '| pages with a block', len(by))
    if dry: return
    for p in glob.glob(LOCAL + '/*.json'):
        d = json.load(open(p, encoding='utf-8'))
        if any(b.get('gen') == GEN for b in d.get('blocks', [])) and os.path.basename(p)[:-5] not in by:
            d['blocks'] = [b for b in d['blocks'] if b.get('gen') != GEN]; json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for page, (r, near) in by.items():
        p = os.path.join(LOCAL, page + '.json')
        d = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {'status': 'draft', 'slug': page, 'updated': '2026-11-03', 'blocks': [], 'faq': []}
        d['blocks'] = [b for b in d.get('blocks', []) if b.get('gen') != GEN]
        items = [[{'t': o['name'], 'h': f"/{o['page']}.html"}, {'t': f": {km(dd)} to the {bearing(r['pt'], o['pt'])}, in {o['city']}."}] for dd, o in near]
        d['blocks'] += [{'t': 'h', 'level': 2, 'text': f"Areas near {r['name']}", 'gen': GEN, 'pos': 'end'},
                        {'t': 'p', 'text': f"These are the {len(items)} closest neighbourhoods we cover to the centre point we use for {r['name']} in {r['city']}, nearest first. "
                                           "Distances are straight-line between centre points, so the drive is longer.", 'gen': GEN, 'pos': 'end'},
                        {'t': 'list', 'items': items, 'gen': GEN, 'pos': 'end'},
                        {'t': 'p', 'text': 'Centre points: OpenStreetMap contributors and Wikipedia.', 'gen': GEN, 'pos': 'end'}]
        json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('written', len(by))
if __name__ == '__main__': main()
