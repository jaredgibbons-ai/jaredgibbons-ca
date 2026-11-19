"""D-373: contextual links to core pages that few pages link to (counted in the built pages' <main>, Nov 19 2026):
notary fees 2, Panorama Ridge guide 8, North Surrey townhomes 10, South Surrey luxury 13, North Surrey houses 23, North Surrey homes 24.
Each source page gets one short line under its introduction (pos after-intro, gen lnk1119) naming the pages it does not link to yet.
Run from the repo root after a build (it reads dist/ to skip pages that already link): python3 tools/link_weak_pages_2026_11_19.py
"""
import glob, html, json, os, re

CORE = r'(south-surrey|white-rock|surrey|langley|cloverdale|clayton|willoughby|murrayville|walnut-grove|brookswood|aldergrove|fort-langley|crescent)'
TARGETS = [
    ('real-estate-lawyer-notary-fees-langley-surrey-white-rock', 'notary and lawyer fees in Surrey, Langley and White Rock',
     lambda s, txt: (s == 'first-time-home-buyer-program' or re.match(CORE + r'|sell-my-house-in-(surrey|langley|white-rock|south-surrey)', s))
                    and not re.search(r'pitt-meadows|maple-ridge|delta|mission', s) and re.search(r'\bnotary|\blawyer', txt, re.I)),
    ('panorama-ridge-guide', 'the Panorama Ridge neighbourhood guide',
     lambda s, txt: re.match(r'(panorama|west-newton|east-newton|newton|sullivan-station)', s) and 'burnaby' not in s),
    ('north-surrey-homes-for-sale', 'North Surrey homes for sale',
     lambda s, txt: re.match(r'(guildford|whalley|fraser-heights|bolivar|bridgeview|bear-creek|cedar-hills|queen-mary|port-kells|royal-heights)', s)),
    ('north-surrey-houses-for-sale', 'North Surrey houses for sale',
     lambda s, txt: re.match(r'(guildford|whalley|fraser-heights|bolivar|bridgeview|bear-creek|cedar-hills|queen-mary|port-kells|royal-heights)', s) and 'houses' in s or s in ('surrey-houses-for-sale', 'surrey-houses-with-suites-for-sale')),
    ('north-surrey-townhomes-for-sale', 'North Surrey townhouses for sale',
     lambda s, txt: re.match(r'(guildford|whalley|fraser-heights|bolivar|bridgeview|bear-creek|cedar-hills|queen-mary|port-kells|royal-heights)', s) and ('townhomes' in s or 'condos' in s) or s in ('surrey-townhomes-for-sale', 'surrey-townhomes-under-1-2m')),
    ('south-surrey-luxury-homes', 'South Surrey luxury homes',
     lambda s, txt: re.match(r'(south-surrey|white-rock|morgan-creek|elgin-chantrell|crescent|ocean-view-homes-crescent|hazelmere|grandview-heights|luxury-homes-for-sale-in-white-rock)', s)
                    and not re.search(r'condos|townhomes|55-plus|under-800k|pet-friendly|duplex|market-stats|school', s)),
]

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

add = {}
for f in sorted(glob.glob('dist/*.html')):
    s = os.path.basename(f)[:-5]
    if not os.path.exists(f'src/data/local/{s}.json') or s.startswith(('listing', 'blog')): continue
    m = re.search(r'<main.*?</main>', open(f, errors='ignore').read(), re.S)
    if not m: continue
    main = m.group(0); txt = html.unescape(re.sub('<[^>]+>', ' ', main))
    for t, label, ok in TARGETS:
        if s != t and f'/{t}.html"' not in main and ok(s, txt): add.setdefault(s, []).append((t, label))

n = 0
for s, links in add.items():
    p = f'src/data/local/{s}.json'; d = load(p)
    if any(b.get('gen') == 'lnk1119' for b in d.get('blocks', [])): continue
    parts = [{'t': 'Also worth comparing: '}]
    for i, (t, label) in enumerate(links):
        if i: parts.append({'t': ' and ' if i == len(links) - 1 else ', '})
        parts.append({'t': label, 'h': f'/{t}.html'})
    parts.append({'t': '.'})
    d.setdefault('blocks', []).append({'t': 'p', 'pos': 'after-intro', 'gen': 'lnk1119', 'parts': parts})
    save(p, d); n += 1
print('pages given a line:', n)
import collections; print(collections.Counter(t for v in add.values() for t, _ in v))
