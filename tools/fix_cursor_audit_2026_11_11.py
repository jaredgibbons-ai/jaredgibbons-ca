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
