#!/usr/bin/env python3
"""Maple Ridge and Pitt Meadows directory blocks (D-224, Nov 11, 2026).

The archive repeats one "Explore Maple Ridge / Pitt Meadows Neighbourhoods & Property Types" section on 29 and 12 pages: a sub-area by
sub-area directory with a marketing line each (which also mislabels some areas), then the property-type links and Jared's credentials box.
The repeated directory text pulled those pages under 0.70 unique. On every page except the city page, the section is replaced (via the
local layer's `suppress`) by: one line linking the neighbourhood guides hub, the same property-type links, and the same credentials box.
Nothing else changes. Idempotent. python3 -I tools/trim_area_directories_2026_11_11.py"""
import glob, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
CITIES = {'Maple Ridge': ('maple-ridge-neighbourhood-guides', {'cityofmapleridge'}), 'Pitt Meadows': ('pitt-meadows-neighbourhood-guides', set())}


def main():
    n = 0
    for city, (hub, keep) in CITIES.items():
        H = f'Explore {city} Neighbourhoods & Property Types'
        for f in sorted(glob.glob('src/data/pages/*.json')):
            d = json.load(open(f)); slug = d['slug']
            if slug in keep or slug == hub: continue
            bl = d['blocks']; i = next((k for k, b in enumerate(bl) if b['t'] == 'h' and b.get('level') == 2 and b['text'] == H), -1)
            if i < 0: continue
            j = next((k for k in range(i + 1, len(bl)) if bl[k]['t'] == 'h' and bl[k].get('level', 9) <= 2), len(bl))
            sec = bl[i + 1:j]
            ptype = next((k for k, b in enumerate(sec) if b['t'] == 'h' and b['text'].startswith(f'Search {city} Homes by Property Type')), None)
            tail = sec[ptype:] if ptype is not None else [b for b in sec if b['t'] == 'list']
            lf = f'src/data/local/{slug}.json'
            raw = open(lf).read() if os.path.exists(lf) else None
            l = json.loads(raw) if raw else {'slug': slug, 'blocks': []}
            l['suppress'] = sorted(set(l.get('suppress', []) + [H]))
            l['blocks'] = [b for b in l.get('blocks', []) if b.get('gen') not in ('mrnav', 'areadir')]
            l['blocks'] += [{'t': 'h', 'level': 2, 'text': f'More {city} pages', 'gen': 'areadir', 'pos': 'end'},
                            {'t': 'p', 'gen': 'areadir', 'pos': 'end', 'parts': [{'t': f'Every {city} neighbourhood is compared in the '}, {'t': f'{city} neighbourhood guides', 'h': f'https://jaredgibbons.ca/{hub}.html'}, {'t': '.'}]}]
            l['blocks'] += [{**b, 'gen': 'areadir', 'pos': 'end'} for b in tail]
            ind = (1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)) if raw else 1
            s = json.dumps(l, ensure_ascii=False, indent=ind) if ind else json.dumps(l, ensure_ascii=False, separators=(',', ':'))
            open(lf, 'w').write(s + ('\n' if (raw or '\n').endswith('\n') else ''))
            n += 1
    # Three more pages just under 0.70 (archive sales copy repeated on sibling pages): the repeated paragraph is hidden on that page only.
    HIDE = {'abbotsford-duplexes-for-sale': ['Whether you are comparing strata buildings around Central Abbotsford'],
            'chilliwack-houses-for-sale': ['Every listing below updates directly from the Fraser Valley Real Estate Board', 'Listings on this page update directly from the Fraser Valley Real Estate Board']}
    for slug, hs in HIDE.items():
        lf = f'src/data/local/{slug}.json'; raw = open(lf).read(); l = json.loads(raw)
        l['hide'] = sorted(set(l.get('hide', []) + hs))
        ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
        open(lf, 'w').write((json.dumps(l, ensure_ascii=False, indent=ind) if ind else json.dumps(l, ensure_ascii=False, separators=(',', ':'))) + ('\n' if raw.endswith('\n') else ''))
    lf = 'src/data/local/cloverale-foreclosures-court-ordered-sales.json'; raw = open(lf).read(); l = json.loads(raw)   # its FAQ repeated "who can help" twice
    l['faq'] = [f for f in l['faq'] if f['q'] != 'Can I book a private showing with Jared?']
    ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
    open(lf, 'w').write((json.dumps(l, ensure_ascii=False, indent=ind) if ind else json.dumps(l, ensure_ascii=False, separators=(',', ':'))) + ('\n' if raw.endswith('\n') else ''))
    print('pages updated:', n)


if __name__ == '__main__': main()
