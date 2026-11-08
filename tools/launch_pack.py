#!/usr/bin/env python3
"""Launch approval pack: one row per new page (draft and generated), grouped into approval batches.

Writes docs/review/launch/launch-approval-<date>.csv and src/data/launch/holds.json (slug -> reason a page is held back at launch).
Needs a fresh `npm run build` (inbound links are counted in dist) and `python3 -I tools/uniqueness.py --csv /tmp/uq.csv`.
A hold only takes effect in the launch build (PUBLIC_PREVIEW=false): the page gets noindex and leaves the sitemap, the footer and generated link lists drop it,
and it is not deleted.  In the preview every held page shows a note saying why.
    python3 -I tools/launch_pack.py [--uq /tmp/uq.csv]
"""
import csv, glob, json, os, re, sys, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
DATE = '2026-11-07'
uq = {r['slug']: r for r in csv.DictReader(open(sys.argv[sys.argv.index('--uq') + 1] if '--uq' in sys.argv else '/tmp/uq.csv'))}
emb = json.load(open('src/data/idx-embeds.json'))['pages']
seo = json.load(open('src/data/seo-final.json'))
gate = json.load(open('src/data/inventory/gate.json'))
try: sold = json.load(open('src/data/schools/radius-sold.json'))
except Exception: sold = {}

# inbound links, counted on the built site
inb = collections.Counter()
for r, _, fs in os.walk('dist'):
    if r.startswith(('dist/internal', 'dist/_astro')): continue
    for f in fs:
        if not f.endswith('.html'): continue
        me = f[:-5]; seen = set()
        for m in re.finditer(r'<a [^>]*href="/([a-z0-9\-]+)\.html', open(os.path.join(r, f), encoding='utf-8').read()):
            if m.group(1) != me: seen.add(m.group(1))
        inb.update(seen)

GROUPS = [  # (label, regex on slug), first match wins
    ('School pages', r'^homes-near-'), ('Market stats pages', r'-real-estate-market-stats$'), ('Sell my house in a city', r'^sell-my-house-in-'),
    ('Presale and new construction', r'new-construction|presale'), ('55+ homes and condos', r'55-plus'), ('Bedroom searches', r'-\d-bedroom|-studio|bedroom'),
    ('Acreage, farms and land', r'acreage|farm|lots-land|-land$|equestrian|hobby'), ('Price searches', r'under-1|over-1|-luxury|condos-under|homes-under'),
    ('Condos and townhomes', r'condos|townhomes|duplex|penthouse|coach|laneway|suite|mobile|waterfront|golf'), ('Guides and rules', r'(^|-)guide$|buying-rules|-guide-'),
    ('Houses and homes for sale', r'(houses|homes)-for-sale$'),
]
def group(slug, j):
    sp = j.get('search_page'); sp = sp.get('kind') if isinstance(sp, dict) else sp
    if sp == 'price': return 'Price band searches'
    for lab, rx in GROUPS:
        if re.search(rx, slug): return lab
    return 'Neighbourhood and area pages'

APP = json.load(open('docs/review/launch/approvals.json')) if os.path.exists('docs/review/launch/approvals.json') else {'approved': []}
APPROVED_SLUGS = set(APP.get('slugs', []))   # pages Jared approved on the date in approvals.json; pages added later wait for his next approval
rows, holds = [], {}
for f in sorted(glob.glob('src/data/local/*.json')):
    j = json.load(open(f))
    if not j.get('new_page'): continue
    s = j['slug']; grid = any(b['t'] == 'grid' for b in j['blocks']); wired = s in emb
    g = group(s, j); u = uq.get(s, {}); uniq = float(u.get('unique') or 0); words = int(u.get('words') or 0)
    gp = gate['pages'].get(s); auto_noindex = ''
    if gp and gp['kind'] == 'feed':
        h = gp['history'][-3:]
        if len(h) >= 3 and sum(x['active'] for x in h) / len(h) < 5: auto_noindex = 'Yes: under 5 active listings (3-month average)'
    sold_state = ''
    if g == 'School pages':
        k = s[len('homes-near-'):]
        sold_state = 'Yes' if any(k == x or k + '-' in x or x == k for x in sold) else 'Waiting for Pete'
    reason, rec = '', 'Approve'
    if grid and not wired: rec, reason = 'Hold', "Waiting for Jerry's saved search (the page would show an empty listings box)"
    elif g == 'School pages' and sold_state != 'Yes': rec, reason = 'Hold', "Waiting for Pete's sold export for this school (the page has no sold figures yet)"
    elif uniq < 0.7: rec, reason = 'Hold', f'Under 70% unique wording ({uniq:.0%})'
    elif inb[s] < 2: rec, reason = 'Hold', f'Only {inb[s]} page(s) link here'
    if rec == 'Hold': holds[s] = reason
    batch = {'Approve': 'A. Approve now', 'Hold': 'B. Hold: waiting for Jerry' if 'Jerry' in reason else ('C. Hold: waiting for Pete' if 'Pete' in reason else 'D. Hold: fix first')}[rec]
    if j.get('status') == 'generated': batch = ('E. Auto-generated, goes live with the rest' if rec == 'Approve' else batch)
    rows.append([batch, g, s, f'https://jaredgibbons.ca/{s}.html', (seo.get(s) or j['new_page']).get('title', ''), j.get('status'), ('Wired' if wired else 'Not yet') if grid else 'No search on page',
                 sold_state, words, f'{uniq:.0%}', inb[s], auto_noindex, rec, reason, (f'Yes, {APP["date"]}' if s in APPROVED_SLUGS else 'Not yet')])
rows.sort(key=lambda r: (r[0], r[1], r[2]))
out = f'docs/review/launch/launch-approval-{DATE}.csv'
with open(out, 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['Batch', 'Group', 'Slug', 'URL', 'Page title', 'Status', 'Live search', 'School sold figures', 'Words', 'Unique wording', 'Pages linking here', 'Auto-noindex at launch', 'Recommendation', 'Why held', 'Approved by Jared']); w.writerows(rows)
json.dump(dict(sorted(holds.items())), open('src/data/launch/holds.json', 'w'), indent=1, ensure_ascii=False); open('src/data/launch/holds.json', 'a').write('\n')
c = collections.Counter((r[0], r[1]) for r in rows)
print(len(rows), 'pages;', len(holds), 'held')
for k, v in sorted(c.items()): print(f'{v:4d}  {k[0]}  |  {k[1]}')
