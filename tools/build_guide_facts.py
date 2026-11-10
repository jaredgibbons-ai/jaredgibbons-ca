"""Quick facts at the top of each neighbourhood guide (D-197) -> src/data/guide-facts.json {slug: {area, prices, mix, n}}.

From Jared's Paragon closed-sales export (src/data/sold/sold-12m.json): the median sale price by home type (5 sales needed) and what sold,
by type (3 needed to mention). The guide is matched to its MLS® sub-area by name; a guide that matches no sub-area, or more than one
(Mount Pleasant is both VE and VW), gets no price row rather than a guess. Rendered by GenericPage.astro above the guide's first section.
python3 -I tools/build_guide_facts.py"""
import collections, glob, json, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SUB = json.load(open(os.path.join(ROOT, 'src/data/sold/sold-12m.json'), encoding='utf-8'))['sub']
OUT = os.path.join(ROOT, 'src/data/guide-facts.json')
LABEL = [('house', 'Houses'), ('townhome', 'Townhomes'), ('condo', 'Condos'), ('duplex', 'Duplexes'), ('acreage', 'Acreages'), ('mobile', 'Manufactured homes'), ('land', 'Lots')]
MANUAL = {'aldergrove': 'Langley|Aldergrove Langley', 'brookswood': 'Langley|Brookswood Langley', 'crescent-beach-ocean-park': 'South Surrey White Rock|Crescent Bch Ocean Pk.',
          'grandview-heights': 'South Surrey White Rock|Grandview Surrey', 'north-meadows-pitt-meadows': 'Pitt Meadows|North Meadows PI', 'willoughby': 'Langley|Willoughby Heights',
          'east-chilliwack': 'Chilliwack|East Chilliwack'}
LOCAL = {'rosemary-heights-guide': ('radius', 'rosemary-heights-elementary', 'Within 1 km of Rosemary Heights Elementary'),
         'yorkson-langley-guide': ('radius', 'willoughby-elementary', 'Within 1 km of Willoughby Elementary'),
         'auguston-abbotsford-guide': ('sub', 'Abbotsford|Abbotsford East', 'Abbotsford East sub-area')}
SKIP = {'brookswood-real-estate-development', 'how-to-buy-a-mobile-home-in-bc', 'chilliwack-55-plus-neighbourhood'}
nz = lambda s: re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()


def money(v): return f'${v / 1e6:.2f}M'.replace('.00M', 'M') if v >= 1e6 else f'${v:,.0f}'


def index():
    idx = collections.defaultdict(list)
    for k in SUB:
        name = k.split('|', 1)[1]
        idx[nz(re.sub(r'\s+(PM|MR|PC|BN|BS|BE|NW|NV|VW|VE|RI|CQ|PQ|LA|SR|AB|MI|CH|PI)$', '', name))].append(k)
    return idx


def match(base, idx):
    if base in MANUAL: return MANUAL[base]
    words = nz(base.replace('-', ' ')).split()
    for n in range(len(words), 0, -1):
        ks = idx.get(' '.join(words[:n]))
        if not ks: continue
        if len(ks) > 1:
            rest = ' '.join(words[n:]); ks = [k for k in ks if nz(k.split('|')[0]) in rest] or ks
        return ks[0] if len(ks) == 1 else None
    return None


def main():
    idx = index(); out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, 'src/data/pages/*-guide.json'))):
        slug = os.path.basename(f)[:-5]; base = slug[:-6]
        if base in SKIP: continue
        k = match(base, idx)
        if not k: continue
        g = SUB[k]['groups']; name = k.split('|', 1)[1]
        prices = [[lab, money(g[t]['price'])] for t, lab in LABEL if t in g and g[t].get('n', 0) >= 5 and g[t].get('price')]
        sold = [(g[t]['n'], lab.lower()) for t, lab in LABEL if t in g and g[t].get('n', 0) >= 3]
        n = sum(v.get('n', 0) for v in g.values())
        if not prices and not sold: continue
        out[slug] = {'area': name, 'prices': prices, 'mix': ', '.join(f'{c:,} {l}' for c, l in sorted(sold, reverse=True)), 'n': n}
    # New local guides for neighbourhoods inside a larger sub-area (D-203): a 1 km circle around the neighbourhood school where one sits at
    # its centre (src/data/schools/radius-sold.json), else the sub-area it belongs to, named as such in the box.
    rad = json.load(open(os.path.join(ROOT, 'src/data/schools/radius-sold.json'), encoding='utf-8'))
    RLAB = [('house', 'Houses'), ('townhouse', 'Townhomes'), ('condo', 'Condos')]
    for slug, (kind, key, area) in LOCAL.items():
        if kind == 'radius':
            g = rad[key]['groups']
            prices = [[lab, money(g[t]['price'])] for t, lab in RLAB if g.get(t, {}).get('n', 0) >= 5 and g[t].get('price')]
            sold = [(g[t]['n'], lab.lower()) for t, lab in RLAB if g.get(t, {}).get('n', 0) >= 3]
            n = rad[key]['n']
        else:
            g = SUB[key]['groups']
            prices = [[lab, money(g[t]['price'])] for t, lab in LABEL if t in g and g[t].get('n', 0) >= 5 and g[t].get('price')]
            sold = [(g[t]['n'], lab.lower()) for t, lab in LABEL if t in g and g[t].get('n', 0) >= 3]
            n = sum(v.get('n', 0) for v in g.values())
        out[slug] = {'area': area, 'prices': prices, 'mix': ', '.join(f'{c:,} {l}' for c, l in sorted(sold, reverse=True)), 'n': n}
    json.dump(out, open(OUT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False); open(OUT, 'a').write('\n')
    print('guides with quick facts:', len(out), '| with a price row:', sum(1 for v in out.values() if v['prices']))


if __name__ == '__main__': main()
