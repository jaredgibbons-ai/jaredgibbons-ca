"""D-374: every core-area page that fewer than 15 other pages link to (in their main content) gets links from up to 12 pages
in the same area. Each source page carries one "Also worth comparing: ..." line under its introduction (gen lnk1119, joined with
the D-373 line when the page has one), with at most 4 links. Link text is the target page's H1.
Run from the repo root after a build: python3 tools/link_weak_core_2026_11_19.py
"""
import collections, glob, html, json, os, re

AREAS = sorted('''south-surrey white-rock fort-langley walnut-grove city-of-langley langley-city north-surrey east-newton west-newton panorama-ridge
fraser-heights cedar-hills sullivan-station salmon-river campbell-valley grandview morgan-creek morgan-crossing crescent ocean-park elgin-chantrell
hazelmere sunnyside clayton cloverdale willoughby murrayville brookswood aldergrove guildford whalley fleetwood newton bolivar-heights bridgeview
bear-creek queen-mary-park port-kells royal-heights yorkson milner otter county-line surrey langley'''.split(), key=len, reverse=True)
def area(s):
    return next((a for a in AREAS if s == a or s.startswith(a + '-')), None)

_FMT = {}
def load(p):
    raw = open(p).read(); d = json.loads(raw)
    for st in (dict(indent=None, separators=(',', ':')), dict(indent=None), dict(indent=1), dict(indent=2), dict(indent=0)):
        for ea in (False, True):
            for tail in ('', '\n'):
                if json.dumps(d, ensure_ascii=ea, **st) + tail == raw: _FMT[p] = (st, ea, tail); return d
    _FMT[p] = (dict(indent=2), False, '\n'); return d
def save(p, d):
    st, ea, tail = _FMT[p]; open(p, 'w').write(json.dumps(d, ensure_ascii=ea, **st) + tail)

links, h1 = {}, {}
for f in glob.glob('dist/*.html'):
    s = os.path.basename(f)[:-5]
    t = open(f, errors='ignore').read(); m = re.search(r'<main.*?</main>', t, re.S)
    if not m: continue
    links[s] = set(re.findall(r'href="/([a-z0-9-]+)\.html"', m.group(0)))
    h = re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S)
    if h: h1[s] = html.unescape(re.sub(r'<[^>]+>', '', h.group(1))).strip()
inb = collections.Counter(x for s, ls in links.items() for x in ls if x != s)
ok_page = lambda s: area(s) and not s.startswith(('listing', 'blog')) and os.path.exists(f'src/data/local/{s}.json')
weak = sorted((s for s in links if ok_page(s) and inb[s] < 15 and s in h1), key=lambda s: inb[s])

BROAD = {'surrey', 'langley', 'south-surrey', 'white-rock', 'north-surrey'}
def family(s):
    for f, rx in (('55', r'55-plus'), ('condo', r'condo|penthouse|apartment'), ('town', r'townhome|townhouse|duplex'),
                  ('house', r'house|luxury|waterfront|hillside|ocean-view|golf|acreage|farm|lots-land|mobile'),
                  ('guide', r'guide|neighbourhood|checklist|rules|schools|realtor|market-stats|development')):
        if re.search(rx, s): return f
    return 'homes'
add = collections.defaultdict(list)
for t in weak:
    # same area; for a whole city (Surrey, Langley, South Surrey, White Rock) only pages of the same kind, so a condo page is not
    # offered on a farm page
    srcs = [s for s in sorted(links) if s != t and ok_page(s) and area(s) == area(t) and t not in links[s] and len(add[s]) < 4
            and (area(t) not in BROAD or family(s) == family(t))]
    srcs.sort(key=lambda s: (family(s) != family(t), len(s)))
    for s in srcs[:12]: add[s].append(t)

n = 0
for s, ts in add.items():
    p = f'src/data/local/{s}.json'; d = load(p); blocks = d.setdefault('blocks', [])
    line = next((b for b in blocks if b.get('gen') == 'lnk1119'), None)
    have = {x.get('h') for x in (line or {}).get('parts', [])}
    new = [(t, h1[t]) for t in ts if f'/{t}.html' not in have]
    if not new: continue
    items = ([(x['h'][1:-5], x['t']) for x in line['parts'] if x.get('h')] if line else []) + new
    parts = [{'t': 'Also worth comparing: '}]
    for i, (t, label) in enumerate(items):
        if i: parts.append({'t': ' and ' if i == len(items) - 1 else ', '})
        parts.append({'t': label, 'h': f'/{t}.html'})
    parts.append({'t': '.'})
    if line: line['parts'] = parts
    else: blocks.append({'t': 'p', 'pos': 'after-intro', 'gen': 'lnk1119', 'parts': parts})
    save(p, d); n += 1
print('weak core pages:', len(weak), '| source pages given links:', n, '| links added:', sum(len(v) for v in add.values()))
