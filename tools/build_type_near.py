"""'Condos / townhomes near X' block (gen 'near3') for type pages that have no neighbourhood of their own to measure from.

Centre = the precise point for the named area in src/data/area-coordinates.csv (Muse research 2026-11-03, OpenStreetMap). Candidates = existing pages of the same home type
(x-condos-for-sale, x-townhomes-for-sale, x-condos-townhomes-for-sale) whose area also has a precise point. Straight-line distance and compass direction, nearest 6 within 25 km.
    python3 -I tools/build_type_near.py      (after build_area_near.py)"""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_area_near as N
ROOT = N.ROOT; LOCAL = N.LOCAL; PAGES = N.PAGES; GEN = 'near3'
TARGETS = {'ladner-condos-for-sale': ('Ladner', 'condo'), 'ladner-townhomes-for-sale': ('Ladner', 'townhome')}
SFX = {'condo': ('-condos-for-sale', '-condos-townhomes-for-sale'), 'townhome': ('-townhomes-for-sale', '-condos-townhomes-for-sale')}
NOUN = {'condo': 'Condo', 'townhome': 'Townhome'}
def base(s): return re.sub(r'-(houses-for-sale|homes-for-sale|guide|condos-townhomes-for-sale|condos-for-sale|townhomes-for-sale)$', '', s)
def main():
    P = N.load(); slugs = {os.path.basename(p)[:-5] for p in glob.glob(PAGES + '/*.json')} | {os.path.basename(p)[:-5] for p in glob.glob(LOCAL + '/*.json')}
    for page, (area, typ) in TARGETS.items():
        centre = next((r for r in P if r['name'] == area), None)
        if not centre: print('no precise centre for', area); continue
        cand = {}
        for r in P:
            b = base(r['page'])
            for sf in SFX[typ]:
                t = b + sf
                if t in slugs and t != page and t not in cand: cand[t] = r
        near = sorted(((N.hav(centre['pt'], r['pt']), t, r) for t, r in cand.items()), key=lambda x: x[0]); near = [x for x in near if x[0] <= N.MAXKM][:6]
        if len(near) < 3: print('too few for', page); continue
        p = os.path.join(LOCAL, page + '.json'); d = json.load(open(p, encoding='utf-8'))
        d['blocks'] = [b for b in d.get('blocks', []) if b.get('gen') != GEN]
        items = [[{'t': r['name'] + ' ' + typ.replace('condo', 'condos').replace('townhome', 'townhomes'), 'h': f'/{t}.html'}, {'t': f": {N.km(dd)} to the {N.bearing(centre['pt'], r['pt'])}, in {r['city']}."}] for dd, t, r in near]
        d['blocks'] += [{'t': 'h', 'level': 2, 'text': f'{NOUN[typ]} pages near {area}', 'gen': GEN, 'pos': 'end'},
                        {'t': 'p', 'text': f"Looking at {typ.replace('condo', 'condos').replace('townhome', 'townhomes')} in {area}? These are the closest {typ.replace('condo', 'condo').replace('townhome', 'townhome')} searches we cover, measured in a straight line from the centre point we use for {area}. The drive is longer.", 'gen': GEN, 'pos': 'end'},
                        {'t': 'list', 'items': items, 'gen': GEN, 'pos': 'end'}, {'t': 'p', 'text': 'Centre points: OpenStreetMap contributors and Wikipedia.', 'gen': GEN, 'pos': 'end'}]
        json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print(page, len(items))
if __name__ == '__main__': main()
