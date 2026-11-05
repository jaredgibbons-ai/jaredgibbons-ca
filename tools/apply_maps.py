"""Put the neighbourhood map and drive-time blocks on the pages named in src/data/maps/<region>.json.

  python3 -I tools/apply_maps.py

Hub page: a map of every area in the region (hub mode, shaded by our own sold figures).  Each area page: its own outline (area mode) and the drive-time box.
Generated blocks carry "gen": "areamap"; they are removed and rebuilt on every run, so re-running is safe.  Region -> hub page is HUBS below.
"""
import glob, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HUBS = {'south-surrey-white-rock': 'south-surrey-neighbourhoods', 'surrey': 'surrey-neighbourhood-guides', 'cloverdale': 'cloverdale-neighbourhood-guides', 'langley': 'langley-neighbourhood-guides',
        'delta': 'delta-neighbourhood-guides', 'maple-ridge': 'maple-ridge-neighbourhood-guides', 'pitt-meadows': 'pitt-meadows-neighbourhood-guides', 'abbotsford': 'abbotsford-neighbourhood-guides'}
# Pages that are hand-built Astro files rather than src/data/local data (no blocks to add): they still get an outline on their hub map.
BESPOKE = {'fort-langley'}

def load(slug):
    p = os.path.join(ROOT, 'src/data/local', slug + '.json')
    raw = open(p, encoding='utf-8').read()
    lines = raw.split('\n')
    indent = len(lines[1]) - len(lines[1].lstrip(' ')) if len(lines) > 1 else 1   # keep each file's own layout so diffs stay small
    return p, json.loads(raw), (indent or 1, raw.endswith('\n'))

def save(p, d, fmt):
    with open(p, 'w', encoding='utf-8') as fh:
        json.dump(d, fh, ensure_ascii=False, indent=fmt[0])
        if fmt[1]: fh.write('\n')

def blocks_for(region, area=None):
    G = 'areamap'
    if area is None:
        return [{'t': 'h', 'level': 2, 'text': f'{region["name"]} neighbourhood map', 'gen': G}, {'t': 'areamap', 'region': region['region'], 'mode': 'hub', 'gen': G}]
    return [{'t': 'h', 'level': 2, 'text': f'Where {area["name"]} sits', 'gen': G}, {'t': 'areamap', 'region': region['region'], 'mode': 'area', 'current': area['id'], 'gen': G},
            {'t': 'h', 'level': 2, 'text': f'Drive time to {area["name"]}', 'gen': G}, {'t': 'commute', 'region': region['region'], 'current': area['id'], 'gen': G}]

def main():
    for f in sorted(glob.glob(os.path.join(ROOT, 'src/data/maps/*.json'))):
        region = json.load(open(f, encoding='utf-8'))
        todo = [(HUBS[region['region']], None)] if region['region'] in HUBS else []
        todo += [(a['href'][1:-5], a) for a in region['areas']]
        for slug, area in todo:
            if slug in BESPOKE or not os.path.exists(os.path.join(ROOT, 'src/data/local', slug + '.json')):
                print('skip (hand-built or guide-only page, outline on the hub map only) ->', slug); continue
            p, d, fmt = load(slug)
            keep = [b for b in d['blocks'] if b.get('gen') != 'areamap']
            at = 0
            if area is not None:   # after the first paragraph, so the page opens with its own words
                at = next((i + 1 for i, b in enumerate(keep) if b['t'] == 'p'), len(keep))
            d['blocks'] = keep[:at] + blocks_for(region, area) + keep[at:]
            save(p, d, fmt); print('map blocks ->', slug, 'at', at)

if __name__ == '__main__':
    main()
