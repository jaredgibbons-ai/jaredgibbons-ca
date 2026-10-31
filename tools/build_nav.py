"""Build src/data/nav.json from the archived homepage record (docs/archive-extracts/home.md).
Labels/hrefs are taken verbatim from the record. Nesting is inferred from the flat visible-text
order (see docs/decisions.md D-004); confirm against source.bin when baseline zips are available."""
import re, json, sys
P = 'docs/archive-extracts/home.md'
L = open(P, encoding='utf8').read().split('\n')
links = []
for l in L[41:617]:
    m = re.match(r'- LINK \[(.*)\] -> (.*)$', l)
    if m: links.append((m.group(1), m.group(2).replace('https://jaredgibbons.ca', '') or '/'))
# link sequence for the nav: from Home to Fraser Valley Market Stats
k0 = next(i for i, (t, h) in enumerate(links) if t == 'Home')
k1 = next(i for i, (t, h) in enumerate(links) if t == 'Fraser Valley Market Stats')
kb = next(i for i, (t, h) in enumerate(links) if t == 'Blog' and h == '/blog.html' and i > k0 + 100)
kf = next(i for i, (t, h) in enumerate(links) if t == 'FAQ for Home Sellers in BC | Jared Gibbons, REALTOR®')
K = links[k0:kf + 1] + links[kb:k1 + 1]
# visible text: first nav copy (lines 637..before second 'Home'), then tail from 'Blog'
raw = L[636:1052]
tail_start = next(i for i, l in enumerate(L) if i > 1400 and l.strip() == 'Blog')
raw += L[tail_start:tail_start + 120]
S = []
for l in raw:
    if l.strip() == '': continue
    S.append((l.strip(), len(l) - len(l.lstrip()) >= 8))
j = 0
flat = []  # (label, href|None, top)
stop = False
for label, top in S:
    if j < len(K) and K[j][0] == label:
        flat.append((label, K[j][1], top)); j += 1
        if label == 'Fraser Valley Market Stats': break
    else:
        # header (no link) -- only accept if next link appears soon, else stop
        if j >= len(K): break
        flat.append((label, None, top))
assert j == len(K), (j, len(K), flat[-3:])
nav = []
cur_top = None; parent = None; remaining = 0; grp = None
CHILDREN = {'Open Houses': 10, 'Farms': 12, 'Price Searches': 4, 'Land use plans': 9}
def add(item):
    global parent, remaining
    target = parent if (parent is not None and remaining > 0) else (grp if grp is not None else cur_top)
    if parent is not None and remaining > 0:
        parent['children'].append(item); remaining -= 1
        if remaining == 0: parent = None
    elif grp is not None:
        grp['children'].append(item)
    else:
        cur_top['children'].append(item)
for label, href, top in flat:
    item = {'label': label, **({'href': href} if href else {}), 'children': []}
    if top:
        cur_top = item; nav.append(item); parent = None; remaining = 0; grp = None; continue
    if cur_top['label'] == 'Communities' and href is None:
        grp = item; cur_top['children'].append(item); continue
    if label in CHILDREN and not (cur_top['label'] == 'Communities'):
        add(item); parent = item; remaining = CHILDREN[label]; continue
    add(item)
def prune(n):
    if not n['children']: del n['children']
    else:
        for c in n['children']: prune(c)
for n in nav: prune(n)
json.dump(nav, open('src/data/nav.json', 'w'), ensure_ascii=False, indent=1)
def show(n, d=0):
    print('  ' * d + n['label'] + (f"  -> {n['href']}" if 'href' in n else '  [no link]'))
    for c in n.get('children', []): show(c, d + 1)
if '-v' in sys.argv:
    for n in nav: show(n)
print('top-level:', [n['label'] for n in nav], 'links used:', j)
