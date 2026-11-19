"""D-369: core "for sale" pages matched to their real searches, cannibalization fixes,
template headings rewritten in plain buyer wording, MLS abbreviations spelled out.

Run once from the repo root: python3 tools/core_pages_2026_11_19.py
Edits src/data in place (seo-final.json, explore.json, local/*.json, pages/*.json, strata-rules.json).
"""
import json, glob, re

_FMT = {}

def _styles():
    yield dict(indent=None, separators=(',', ':'))
    yield dict(indent=None)
    for i in (1, 2, 0):
        yield dict(indent=i)

def load(p):
    raw = open(p).read()
    d = json.loads(raw)
    for st in _styles():
        for ea in (False, True):
            out = json.dumps(d, ensure_ascii=ea, **st)
            for tail in ('', '\n'):
                if out + tail == raw:
                    _FMT[p] = (st, ea, tail); return d
    _FMT[p] = (dict(indent=1), False, '\n')
    print('format not matched, using indent=1:', p)
    return d

def save(p, d):
    st, ea, tail = _FMT[p]
    open(p, 'w').write(json.dumps(d, ensure_ascii=ea, **st) + tail)

# 1. Titles, H1s and descriptions from Search Console queries (URL-prefix property, Oct 22-Nov 18, bot searches removed).
SEO = {
    'surrey-presale-condos-and-townhomes': (
        'Surrey Presale & New Condos | Townhomes Completing 2027–29',
        'Surrey Presale Condos, New Condos and Townhomes, 2027–2029',
        'New condos and presale townhomes in Surrey: compare Bourna on 105A, Whalley Station, City Corners II and Larner Landing, completing 2027–2029.'),
    'surrey-homes-for-sale': (
        'Surrey Homes for Sale | Real Estate & MLS® Listings, BC',
        'Surrey Homes for Sale and Real Estate',
        'Surrey homes for sale on the MLS®: houses, townhomes and condos in Cloverdale, Fleetwood, Guildford, Newton, South Surrey and Whalley, with prices.'),
    'surrey-condos-for-sale': (
        'Condos for Sale in Surrey BC | SkyTrain & Strata Guide',
        'Condos for Sale in Surrey, BC',
        None),
    'south-surrey-homes-for-sale': (
        'South Surrey Homes for Sale | Real Estate & MLS® Listings',
        'South Surrey Homes for Sale and Real Estate',
        'South Surrey and White Rock real estate on the MLS®: homes for sale in Grandview Heights, Morgan Creek, Ocean Park and Crescent Beach, with market data.'),
    'south-surrey-condos-for-sale': (
        'South Surrey & White Rock Condos for Sale | Updated Daily',
        'Condos for Sale in South Surrey & White Rock, BC',
        'South Surrey and White Rock condos for sale on the MLS®, updated daily. Compare buildings in Grandview Heights, Morgan Crossing and White Rock by price.'),
    'surrey-townhomes-for-sale': (
        'Townhouses for Sale in Surrey BC | Townhomes & Complexes',
        'Townhouses and Townhomes for Sale in Surrey, BC',
        'Surrey townhouses and townhomes for sale on the MLS®, refreshed daily, from Fleetwood and Clayton to Grandview Heights. Compare complexes and strata rules.'),
    'langley-homes-for-sale': (
        'Langley Homes for Sale | Langley BC Real Estate & MLS®',
        'Langley Homes for Sale and Real Estate',
        'Langley real estate on the MLS®: homes for sale in the City and Township, from Willoughby condos to Walnut Grove and Brookswood houses and ALR acreages.'),
    'south-surrey-houses-for-sale': (
        'Houses for Sale in South Surrey BC | Detached Homes & Lots',
        None,
        'Detached houses for sale in South Surrey on the MLS®, updated daily. Compare Crescent Beach, Ocean Park and Morgan Creek lots and the new R1 to R5 zones.'),
    'guildford': (
        'Guildford Surrey Real Estate | Homes Near Town Centre',
        'Guildford Real Estate and Homes for Sale, Surrey',
        None),
    'guildford-surrey-houses-for-sale': (
        'Guildford Surrey Houses for Sale | Detached Homes & Lots',
        None,
        None),
}
sf = load('src/data/seo-final.json')
for slug, (t, h, d) in SEO.items():
    rec = sf[slug]
    assert len(t) <= 60, (slug, len(t))
    rec['title'] = t
    if h: rec['h1'] = h
    if d:
        assert len(d) <= 158, (slug, len(d))
        rec['description'] = d
save('src/data/seo-final.json', sf)

# 2. Template headings. "Surrey Condos: rules that affect buyers" reads like a form; say it the way a buyer searches.
TYPES = r'(55\+ Condos and Townhomes|55\+ Condos|55\+ Townhomes|55\+ Homes|Condos and Townhomes|Condos & Townhomes|Mobile Homes for Sale|Mobile Homes|Homes for Sale|Houses for Sale|Condos for Sale|Townhomes for Sale|Townhouses for Sale|Houses|Condos|Townhomes|Townhouses|Duplexes|Penthouses|Acreages|Farms|Ranchers|Homes)'
TYPED = re.compile(r'^(.+?) ' + TYPES + r'$')
SUF = ['streets and boundaries', 'the homes', 'rules that affect buyers', 'local details a buyer would not know',
       'development and new projects', 'costs and taxes', 'getting around', 'risks and due diligence']
HEAD = re.compile(r'^(.*): (' + '|'.join(SUF) + r')$')

def split(prefix):
    m = TYPED.match(prefix)
    if not m: return prefix, None
    t = re.sub(r' for Sale$', '', m.group(2))
    t = t.replace(' & ', ' and ')
    return m.group(1), ('55+ ' + t[4:].lower() if t.startswith('55+') else t.lower())

def rewrite(text):
    m = HEAD.match(text)
    if m:
        p, t = split(m.group(1)); s = m.group(2)
        if s == 'local details a buyer would not know': return f'{p}: details most buyers miss'
        if s == 'development and new projects': return f'{p}: new projects and development'
        if s in ('streets and boundaries', 'getting around'): return f'{p}: {s}'
        if not t:
            return {'the homes': f'{p}: the homes', 'rules that affect buyers': f'Rules for buyers in {p}',
                    'costs and taxes': f'{p}: costs and taxes', 'risks and due diligence': f'Buying in {p}: risks to check'}[s]
        return {'the homes': f'{t[0].upper() + t[1:]} in {p}: what you will find',
                'rules that affect buyers': f'Rules for buying {t} in {p}',
                'costs and taxes': f'Costs and taxes on {t} in {p}',
                'risks and due diligence': f'Buying {t} in {p}: risks to check'}[s]
    m = re.match(r'^How (.+) compares$', text)
    if m:
        p, t = split(m.group(1))
        return f'How {p} {t} compare' if t else text
    return text

changed = 0
for f in sorted(glob.glob('src/data/local/*.json')):
    d = load(f); hit = False
    for b in d.get('blocks', []):
        if b.get('t') == 'h' and isinstance(b.get('text'), str):
            n = rewrite(b['text'])
            if n != b['text']: b['text'] = n; hit = True; changed += 1
    if hit: save(f, d)
print('headings rewritten:', changed)

# 3. MLS abbreviations in visible text. Quoted MLS sub-area names (explaining the board's label) stay as they are.
REPL = [
    ('Crescent Bch Ocean Pk. (Crescent Beach and Ocean Park)', 'Crescent Beach and Ocean Park'),
    ('Grandview Aquatic Ctr', 'Grandview Heights Aquatic Centre'),
    ('Grandview Hts. Sec.', 'Grandview Heights Secondary'),
    ('Grandview Hts Secondary', 'Grandview Heights Secondary'),
    ('Central W.Rock', 'Central White Rock'),
]
ABBR = re.compile(r'(?<![\\"“] )(?<![\\"“])(?<!F53 )Crescent Bch Ocean Pk\.?')
SKIP_KEYS = {'slug', 'href', 'h', 'url', 'subarea', 'id', 'key', 'src'}

def fix(v, key=None):
    if isinstance(v, dict): return {k: fix(x, k) for k, x in v.items()}
    if isinstance(v, list): return [fix(x, key) for x in v]
    if isinstance(v, str) and key not in SKIP_KEYS:
        for a, b in REPL: v = v.replace(a, b)
        v = ABBR.sub('Crescent Beach & Ocean Park', v)
    return v

n = 0
for f in ['src/data/explore.json', 'src/data/strata-rules.json'] + glob.glob('src/data/local/*.json') + glob.glob('src/data/pages/*.json'):
    raw = open(f).read()
    if not any(a in raw for a, _ in REPL) and 'Crescent Bch Ocean Pk' not in raw: continue
    d = load(f); d2 = fix(d)
    if d2 != d: save(f, d2); n += 1
print('files with abbreviations fixed:', n)

# 4. The 55+ page was taking general condo searches ("condos for sale south surrey white rock") from the condo page.
# Point general condo buyers to the condo page near the top.
p = 'src/data/local/south-surrey-white-rock-55-plus-condos-for-sale.json'
d = load(p)
if not any(b.get('gen') == 'core1119' for b in d['blocks']):
    d['blocks'].insert(0, {'t': 'p', 'pos': 'after-intro', 'gen': 'core1119', 'parts': [
        {'t': 'This page covers buildings with a 55+ age bylaw. For every condo on the market, with no age limit, see '},
        {'t': 'South Surrey and White Rock condos for sale', 'h': '/south-surrey-condos-for-sale.html'},
        {'t': '.'}]})
    save(p, d)

# 5. explore.json column headings sit under the "h" key, which step 3 skips; fixed directly.
raw = open('src/data/explore.json').read()
open('src/data/explore.json', 'w').write(raw.replace('"Explore Crescent Bch Ocean Pk real estate"', '"Explore Crescent Beach & Ocean Park real estate"'))
