"""D-376: two more folds into the page Google already ranks, with a 301 (route.js MOVED). Jared, Nov 19 2026: "yes do 1-3 if you think
its beneficial for seo". Search Console (URL-prefix property, 90 days, bot searches removed):
  willoughby-townhomes-for-sale 29 impressions (29.7), willoughby-heights-langley-condos-townhomes-for-sale 7 (its searches were
  "townhomes for sale willoughby"), willoughby-condos-for-sale 1. The combined page's building-by-building notes move to the condo
  and townhome pages (neither had them); its 301 goes to the townhome page.
  new-construction-cloverdale-bc 0 impressions and 29 inbound links, new-construction-cloverdale 0 and 490; the -bc page's sold tables
  repeat the main page's, so it folds with no content to move (its three questions join the main page's where new).
Mission (mission-bc vs mission-homes-for-sale) is not folded: mission-bc is the area hub (map, drive times, photos, homes Jared sold),
so it is retitled to the area searches it gets ("mission bc realtors", "royal lepage mission bc") and leaves "homes for sale" to the
other page.
Run once from the repo root: python3 tools/fold_pages_2_2026_11_19.py
"""
import glob, json, os, re

FOLD = {'willoughby-heights-langley-condos-townhomes-for-sale': 'willoughby-townhomes-for-sale',
        'new-construction-cloverdale-bc': 'new-construction-cloverdale'}

_FMT = {}
def load(p):
    raw = open(p).read(); d = json.loads(raw)
    for st in (dict(indent=None, separators=(',', ':')), dict(indent=None), dict(indent=1), dict(indent=2), dict(indent=0)):
        for ea in (False, True):
            for tail in ('', '\n'):
                if json.dumps(d, ensure_ascii=ea, **st) + tail == raw: _FMT[p] = (st, ea, tail); return d
    _FMT[p] = (dict(indent=2), False, '\n'); print('format not matched:', p); return d
def save(p, d):
    st, ea, tail = _FMT[p]; open(p, 'w').write(json.dumps(d, ensure_ascii=ea, **st) + tail)
norm = lambda q: re.sub(r'[^a-z0-9]+', ' ', q.lower()).strip()

def sections(blocks, heads):
    out, on = [], False
    for b in blocks:
        if b['t'] == 'h' and b.get('level') == 2: on = b['text'] in heads
        if on: out.append(dict(b, gen='fold1119b'))
    return out

def add_faq(slug, items):
    p = f'src/data/local/{slug}.json'; d = load(p); have = {norm(f['q']) for f in d.get('faq', [])}
    for f in items:
        if norm(f['q']) not in have: d.setdefault('faq', []).append(dict(f, gen='fold1119b')); have.add(norm(f['q']))
    return p, d

# 1. Content moves first.
src = 'src/data/local/willoughby-heights-langley-condos-townhomes-for-sale.json'
if os.path.exists(src):
    w = load(src)
    condo = sections(w['blocks'], {'Condo buildings in Willoughby', 'Condo buildings in Willoughby Heights'})
    town = sections(w['blocks'], {'Townhome complexes in Willoughby', 'Townhome complexes in Willoughby Heights'})
    fq = {f['q']: f for f in w.get('faq', [])}
    for slug, blocks, qs in [('willoughby-condos-for-sale', condo, ['How many known condo projects does Willoughby have?', 'Is Willoughby mostly towers or low-rise?',
                                                                    'What are the compact-lot rules around the condo nodes?', 'Can I rent my Willoughby condo out?']),
                             ('willoughby-townhomes-for-sale', town, ['A listing for a Cascadia home calls it a condo. Is it an apartment?',
                                                                      'What did townhomes in Willoughby Heights sell for?', 'How long do townhomes take to sell in Willoughby Heights?'])]:
        p, d = add_faq(slug, [fq[q] for q in qs if q in fq])
        if not any(b.get('gen') == 'fold1119b' for b in d.get('blocks', [])): d.setdefault('blocks', []).extend(blocks)
        save(p, d)
src = 'src/data/local/new-construction-cloverdale-bc.json'
if os.path.exists(src):
    p, d = add_faq('new-construction-cloverdale', load(src).get('faq', [])); save(p, d)

# 2. Old pages go; index files drop them.
for o in FOLD:
    for p in (f'src/data/local/{o}.json', f'src/data/pages/{o}.json'):
        if os.path.exists(p): os.remove(p)
for p in ('src/data/seo-final.json', 'src/data/review-assign.json', 'src/data/breadcrumbs.json', 'src/data/explore.json'):
    d = load(p)
    for o in FOLD: d.pop(o, None)
    save(p, d)
d = load('src/data/idx-embeds.json')
for o in FOLD: d['pages'].pop(o, None)
save('src/data/idx-embeds.json', d)
d = load('src/data/strata-rules.json'); d['pages'].pop('willoughby-heights-langley-condos-townhomes-for-sale', None); save('src/data/strata-rules.json', d)
raw = open('src/data/lastmod.json').read()
for o in FOLD: raw = re.sub(r'"https://jaredgibbons\.ca/' + re.escape(o) + r'\.html":\{[^}]*\},\n', '', raw)
open('src/data/lastmod.json', 'w').write(raw)

# 3. Links point to the surviving pages; lists drop duplicates and self-links.
PAT = re.compile(r'(?<=/)(' + '|'.join(map(re.escape, FOLD)) + r')(?=\.html)')
def relink(v):
    if isinstance(v, dict): return {k: relink(x) for k, x in v.items()}
    if isinstance(v, list): return [relink(x) for x in v]
    return PAT.sub(lambda m: FOLD[m.group(1)], v) if isinstance(v, str) else v
def href_of(item):
    if isinstance(item, list) and len(item) == 2 and all(isinstance(x, str) for x in item): return item[1]
    if isinstance(item, list):
        hs = [x.get('h') for x in item if isinstance(x, dict) and x.get('h')]
        return hs[0] if len(hs) == 1 else None
    if isinstance(item, dict) and 'href' in item and 'label' in item: return item['href']
def dedupe(v, me):
    if isinstance(v, dict): return {k: dedupe(x, me) for k, x in v.items()}
    if isinstance(v, list):
        v = [dedupe(x, me) for x in v]; seen, out = set(), []
        for x in v:
            h = href_of(x)
            if h:
                k = re.sub(r'^https://jaredgibbons\.ca', '', h)
                if k in seen or (me and k == f'/{me}.html'): continue
                seen.add(k)
            out.append(x)
        return out
    return v
n = 0
for f in glob.glob('src/data/**/*.json', recursive=True):
    if f == 'src/data/lastmod.json': continue
    raw = open(f).read()
    if not any(f'/{o}.html' in raw for o in FOLD): continue
    d = load(f); x = relink(d)
    if f.startswith(('src/data/local/', 'src/data/pages/')):
        s = os.path.basename(f)[:-5]; x = dedupe(x, s if s in set(FOLD.values()) else None)
    elif f == 'src/data/explore.json': x = {k: dedupe(v, k) for k, v in x.items()}
    if x != d: save(f, x); n += 1
print('files relinked:', n)

# 4. Mission: the hub takes the area searches, the homes page keeps "homes for sale".
sf = load('src/data/seo-final.json')
sf['mission-bc']['title'] = 'Mission BC Real Estate | Neighbourhoods, Realtor & Commute'
save('src/data/seo-final.json', sf)
