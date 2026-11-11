#!/usr/bin/env python3
"""Data fixes from the Cursor site audit, Nov 11, 2026 (D-221). Idempotent.
python3 -I tools/fix_cursor_audit_2026_11_11.py

1. Listing R2722542 (20543 28th Avenue, Langley) carried another property's photo alt text ("Luxury Lakefront Home – 20441 2 Ave,
   Brookswood"). Its title and description are fixed in src/data/post-listing-seo.json; the alt text is fixed here.
2. 18 blog posts link to WordPress preview URLs (jaredgibbons.ca/?p=…&preview=true) that never worked for visitors. The links are
   removed and their words kept.
3. Six guides' "Schools" jump link pointed at #<slug>-schools, but the schools heading had a different id. The heading gets that id.
4. BC landlord and tenant page: four card links pointed at headings with no id. The headings get the ids; "Starting a tenancy"
   points at the tenancy agreement section (RTB-1), which already has one.
"""
import glob, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
n = {'alts': 0, 'preview links': 0, 'school ids': 0, 'landlord ids': 0}


def save(f, d): open(f, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, separators=(',', ':')))


# 1
f = 'src/data/listings/listing.r2722542-20543-28th-avenue-langley-bc.102314752.json'
d = json.load(open(f, encoding='utf-8')); al = d.get('photos', {}).get('alts', [])
for i, a in enumerate(al):
    if '20441 2 Ave' in a: al[i] = re.sub(r':.*$', ': 20543 28th Avenue, Brookswood, Langley', a); n['alts'] += 1
for k in ('Title', 'OG title', 'Meta description', 'OG description'):
    if '20441' in str(d['seo'].get(k, '')): d['seo'][k] = ''
if '20441' in d.get('title', ''): d['title'] = 'Sold: 20543 28th Avenue, Brookswood, Langley BC'
save(f, d)

# 2
PREV = re.compile(r'^(https?://(www\.)?jaredgibbons\.ca)?/\?(p|post_type)=[^"]*preview=true')
def unlink(o):
    if isinstance(o, dict):
        if 'h' in o and PREV.match(str(o['h'])): o.pop('h'); n['preview links'] += 1
        for v in o.values(): unlink(v)
    elif isinstance(o, list):
        for v in o: unlink(v)
for f in glob.glob('src/data/posts/*.json'):
    s = open(f, encoding='utf-8').read()
    if 'preview=true' not in s: continue
    d = json.loads(s); unlink(d); save(f, d)

# 3
for g in ('aberdeen', 'english-bluff', 'hawthorne', 'holly', 'poplar', 'port-guichon'):
    f = f'src/data/local/{g}-guide.json'; d = json.load(open(f, encoding='utf-8'))
    for b in d.get('blocks', []):
        if b.get('gen') == 'schools' and b.get('t') == 'h' and b.get('level') == 2 and b.get('id') != f'{g}-guide-schools':
            b['id'] = f'{g}-guide-schools'; n['school ids'] += 1
    open(f, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')

# 4
f = 'src/data/pages/bc-landlord-tenant-resources.json'; d = json.load(open(f, encoding='utf-8'))
IDS = {'Rent increases (RTB-7)': 'jgl-rent-increases', 'Tenant\'s notice to end a tenancy': 'jgl-ending', 'Buying or selling a tenanted property': 'jgl-buying-selling'}
for b in d['blocks']:
    if b.get('t') == 'h' and not b.get('id'):
        for k, v in IDS.items():
            if b.get('text', '').startswith(k): b['id'] = v; n['landlord ids'] += 1
def repoint(o):
    if isinstance(o, dict):
        for k in ('h', 'href'):
            if str(o.get(k, '')).endswith('#jgl-starting'): o[k] = o[k].replace('#jgl-starting', '#jgl-rtb1'); n['landlord ids'] += 1
        for v in o.values(): repoint(v)
    elif isinstance(o, list):
        for v in o: repoint(v)
repoint(d); save(f, d)
print(n)

# 5. A broken host (otterco-op.crs) and a mirror link (retrosearch.org) replaced by the real sites; raw-URL link text in posts and
#    pages becomes "site · page" (the style the sources lists already use).
n['source links'] = n['url text'] = 0
FIXH = {'http://otterco-op.crs/': ('https://www.otterco-op.com/', 'otterco-op.com'),
        'http://retrosearch.org/browse?url=https://www.translink.ca/schedules-and-maps/skytrain': ('https://www.translink.ca/schedules-and-maps/skytrain', 'translink.ca · skytrain')}
from urllib.parse import urlparse, unquote
def pretty(u):
    p = urlparse(u); host = p.netloc.lower().removeprefix('www.')
    seg = [s for s in unquote(p.path).split('/') if s]
    last = re.sub(r'\.(html?|php|aspx?|pdf)$', '', seg[-1]) if seg else ''
    last = re.sub(r'[-_]+', ' ', last).strip()
    if re.fullmatch(r'[0-9a-f ]+', last.lower()) or re.fullmatch(r'[\d ]+', last): last = ''   # ids, not words
    return f'{host} · {last}' if last and len(last) <= 50 else host
def fixlinks(o):
    if isinstance(o, dict):
        h = o.get('h')
        if isinstance(h, str) and h in FIXH: o['h'], o['t'] = FIXH[h]; n['source links'] += 1
        t = o.get('t')
        if isinstance(h, str) and isinstance(t, str) and re.match(r'^(https?://|www\.)\S+$', t.strip()): o['t'] = pretty(h if h.startswith('http') else t); n['url text'] += 1
        for v in o.values(): fixlinks(v)
    elif isinstance(o, list):
        for v in o: fixlinks(v)
for f in glob.glob('src/data/local/*.json') + glob.glob('src/data/posts/*.json') + glob.glob('src/data/pages/*.json'):
    raw = open(f, encoding='utf-8').read()
    if not ('otterco-op.crs' in raw or 'retrosearch.org' in raw or re.search(r'"t": ?"(https?://|www\.)', raw)): continue
    before = dict(n); d = json.loads(raw); fixlinks(d)
    if n == before: continue
    ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
    s = json.dumps(d, ensure_ascii=False, indent=ind) if ind else json.dumps(d, ensure_ascii=False, separators=(',', ':'))
    open(f, 'w', encoding='utf-8').write(s + ('\n' if raw.endswith('\n') else ''))
print(n)
