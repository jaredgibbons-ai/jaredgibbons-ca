"""D-371: fold near-duplicate pages into the page Google already ranks, with a 301 (route.js MOVED).
Jared, Nov 19 2026: "merge, fold and do the next batch".

Search Console (URL-prefix property, last 90 days, bot searches removed):
  willoughby-heights 20 impressions (27.6)          <- willoughby-homes-for-sale 8 (28.3)
  willoughby-houses-for-sale 6 (69.3)               <- willoughby-heights-langley-houses-for-sale 0
  crescent-bch-ocean-pk 111 (36.9)                  <- crescent-beach-homes-for-sale 6 (32), ocean-park-homes-for-sale 0

Run once from the repo root: python3 tools/fold_pages_2026_11_19.py
"""
import json, glob, os, re

FOLD = {
    'willoughby-homes-for-sale': 'willoughby-heights',
    'willoughby-heights-langley-houses-for-sale': 'willoughby-houses-for-sale',
    'crescent-beach-homes-for-sale': 'crescent-bch-ocean-pk',
    'ocean-park-homes-for-sale': 'crescent-bch-ocean-pk',
}

_FMT = {}

def load(p):
    raw = open(p).read(); d = json.loads(raw)
    for st in (dict(indent=None, separators=(',', ':')), dict(indent=None), dict(indent=1), dict(indent=2), dict(indent=0)):
        for ea in (False, True):
            out = json.dumps(d, ensure_ascii=ea, **st)
            for tail in ('', '\n'):
                if out + tail == raw: _FMT[p] = (st, ea, tail); return d
    _FMT[p] = (dict(indent=2), False, '\n'); print('format not matched:', p); return d

def save(p, d):
    st, ea, tail = _FMT[p]; open(p, 'w').write(json.dumps(d, ensure_ascii=ea, **st) + tail)

def ltext(b):
    return b.get('text') or ''.join(x.get('t', '') for x in b.get('parts', []))

# 1. Content the surviving page does not have yet moves over before the old files go.
def take_sections(slug, heads):
    """Each named level-2 section (heading and the blocks under it) from a local file, placed above the contact form (after the hub's own sections)."""
    out, on = [], False
    for b in load(f'src/data/local/{slug}.json')['blocks']:
        if b['t'] == 'h' and b.get('level') == 2: on = b['text'] in heads
        if on and b['t'] not in ('grid', 'notice'):
            b = {k: v for k, v in b.items() if k != 'pos'}; b['gen'] = 'fold1119'; b['pos'] = 'before-form'; out.append(b)
    return out

hub = 'src/data/local/crescent-bch-ocean-pk.json'
if os.path.exists('src/data/local/crescent-beach-homes-for-sale.json'):
    moved = take_sections('crescent-beach-homes-for-sale', {'The village, the beach and the parks', 'Flood rules, dykes and insurance'})
    moved += take_sections('ocean-park-homes-for-sale', {'Ocean Park landmarks and getting around', 'What to check on an Ocean Park home'})
    op = load('src/data/local/ocean-park-homes-for-sale.json')
    d = load(hub)
    if not any(b.get('gen') == 'fold1119' for b in d['blocks']):
        d['blocks'] = moved + d['blocks']
        d.setdefault('faq', []).extend(dict(f, gen='fold1119') for f in op.get('faq', []) if f['q'] == 'What is there to do in Ocean Park?')
        save(hub, d)

wh = 'src/data/local/willoughby-heights.json'
if os.path.exists('src/data/local/willoughby-homes-for-sale.json'):
    old = load('src/data/local/willoughby-homes-for-sale.json'); d = load(wh)
    have = {re.sub(r'[^a-z0-9]+', ' ', f['q'].lower()) for f in d.get('faq', [])}
    for f in old.get('faq', []):
        if re.sub(r'[^a-z0-9]+', ' ', f['q'].lower()) not in have: d.setdefault('faq', []).append(dict(f, gen='fold1119'))
    save(wh, d)

# 2. Old pages go.
for o in FOLD:
    for p in (f'src/data/local/{o}.json', f'src/data/pages/{o}.json'):
        if os.path.exists(p): os.remove(p)

# 3. Index files keyed by slug (or URL).
for p in ('src/data/seo-final.json', 'src/data/review-assign.json', 'src/data/breadcrumbs.json', 'src/data/explore.json'):
    d = load(p)
    for o in FOLD: d.pop(o, None)
    save(p, d)
d = load('src/data/lastmod.json')
for o in FOLD: d.pop(f'https://jaredgibbons.ca/{o}.html', None)
save('src/data/lastmod.json', d)
d = load('src/data/idx-embeds.json')
for o in FOLD: d['pages'].pop(o, None)
save('src/data/idx-embeds.json', d)
d = load('src/data/area-photos.json')
if 'ocean-park-homes-for-sale' in d: d.setdefault('crescent-bch-ocean-pk', d.pop('ocean-park-homes-for-sale'))
save('src/data/area-photos.json', d)

# 4. Every link to an old page points to the surviving one; lists drop the duplicates and self-links this leaves.
PAT = re.compile(r'(?<=/)(' + '|'.join(map(re.escape, FOLD)) + r')(?=\.html)')

def relink(v):
    if isinstance(v, dict): return {k: relink(x) for k, x in v.items()}
    if isinstance(v, list): return [relink(x) for x in v]
    if isinstance(v, str): return PAT.sub(lambda m: FOLD[m.group(1)], v)
    return v

def href_of(item):
    """The single link of a list item or link pair, if it has exactly one."""
    if isinstance(item, list) and len(item) == 2 and all(isinstance(x, str) for x in item): return item[1]
    if isinstance(item, list):
        hs = [x.get('h') for x in item if isinstance(x, dict) and x.get('h')]
        return hs[0] if len(hs) == 1 else None
    if isinstance(item, dict) and 'href' in item and 'label' in item: return item['href']   # nav entries
    return None

def dedupe(v, self_slug):
    if isinstance(v, dict): return {k: dedupe(x, self_slug) for k, x in v.items()}
    if isinstance(v, list):
        v = [dedupe(x, self_slug) for x in v]
        seen, out = set(), []
        for x in v:
            h = href_of(x)
            if h:
                key = re.sub(r'^https://jaredgibbons\.ca', '', h)
                if key in seen or (self_slug and key == f'/{self_slug}.html'): continue
                seen.add(key)
            out.append(x)
        return out
    return v

changed = 0
files = [f for f in glob.glob('src/data/**/*.json', recursive=True)]
for f in files:
    raw = open(f).read()
    if not any(f'/{o}.html' in raw for o in FOLD): continue
    d = load(f); n = relink(d)
    if f.startswith('src/data/local/') or f.startswith('src/data/pages/'):
        slug = os.path.basename(f)[:-5]
        n = dedupe(n, slug if slug in set(FOLD.values()) else None)
    elif f == 'src/data/explore.json':
        n = {k: dedupe(v, k) for k, v in n.items()}
    elif f == 'src/data/nav.json':
        n = dedupe(n, None)
    if n != d: save(f, n); changed += 1
print('files relinked:', changed)

# 5. Link text: a link to the Crescent Beach & Ocean Park page names both communities.
LBL = {'Ocean Park homes for sale': 'Crescent Beach & Ocean Park homes for sale', 'Crescent Beach homes for sale': 'Crescent Beach & Ocean Park homes for sale'}

def relabel(v):
    if isinstance(v, dict):
        if v.get('h', '').endswith('/crescent-bch-ocean-pk.html') and v.get('t') in LBL: v = dict(v, t=LBL[v['t']])
        return {k: relabel(x) for k, x in v.items()}
    if isinstance(v, list):
        if len(v) == 2 and all(isinstance(x, str) for x in v) and v[1].endswith('/crescent-bch-ocean-pk.html') and v[0] in LBL: return [LBL[v[0]], v[1]]
        return [relabel(x) for x in v]
    return v

for f in glob.glob('src/data/**/*.json', recursive=True):
    raw = open(f).read()
    if 'crescent-bch-ocean-pk.html' not in raw or not any(k in raw for k in LBL): continue
    d = load(f); n = relabel(d)
    if n != d: save(f, n); print('relabelled', f)

# 6. The surviving pages now carry the searches the folded pages were splitting (D-370 had ceded them).
sf = load('src/data/seo-final.json')
for slug, t, h in [
    ('crescent-bch-ocean-pk', 'Crescent Beach & Ocean Park Homes for Sale | Real Estate', 'Crescent Beach and Ocean Park Homes for Sale'),
    ('willoughby-heights', 'Willoughby Homes for Sale | Willoughby Heights, Langley', 'Willoughby Heights Homes for Sale, Langley'),
    ('willoughby-houses-for-sale', 'Willoughby Heights Houses for Sale | Langley Detached Homes', 'Willoughby Heights Houses for Sale'),
]:
    assert len(t) <= 60, t
    sf[slug]['title'] = t; sf[slug]['h1'] = h
save('src/data/seo-final.json', sf)
