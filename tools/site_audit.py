#!/usr/bin/env python3
"""Whole-site audit of a built output folder (D-218): the checks in docs/review/cursor-site-audit-prompt.md that can be run from HTML.

python3 -I tools/site_audit.py <built dir> [--csv out.csv]
Checks every .html page: title and meta description (present, length, cut-off, duplicates), one H1, canonical, meta robots, sitemap
(entries resolve, no noindex pages), internal links and #anchors, orphans, images (alt, width/height), JSON-LD (parses, FAQ answers
visible on the page, breadcrumb URLs resolve), leftover working text, doubled words, http:// links, other agents' links, preview-only
text in a launch build. Prints counts and writes one row per finding."""
import csv, glob, html, json, os, re, sys, collections
from urllib.parse import urlparse, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = sys.argv[1]; OUT = sys.argv[sys.argv.index('--csv') + 1] if '--csv' in sys.argv else None
AGENTS = json.load(open(os.path.join(ROOT, 'src/data/other-agent-domains.json')))
AGENTS = AGENTS if isinstance(AGENTS, list) else AGENTS.get('domains', [])
AG = re.compile(r'://(?:[a-z0-9-]+\.)*(?:' + '|'.join(re.escape(a) for a in AGENTS) + r')(?=[/:?#"]|$)', re.I)
WORK = re.compile(r'\b(counted nowhere|queued|not asserted|flagged|resolved nowhere|verify fresh|per listing text|Board geography|expressly not|D-\d{3}\b|TODO|TBD|lorem|\[NEEDS|NOT VERIFIED|placeholder|per the directory|Muse\b|named candidate)', re.I)
F = []
def add(sev, area, slug, issue, ev=''): F.append((sev, area, slug, issue, (ev or '')[:220]))

pages = {}
for f in sorted(glob.glob(os.path.join(D, '*.html'))):
    slug = os.path.basename(f)[:-5]; pages[slug] = open(f, encoding='utf-8').read()
# Blog posts and own listings are served at /blog.html/<slug> and /our-listings.html/<slug> (emitted under internal/).
for sub, pub in (('internal/blog', 'blog.html'), ('internal/listings', 'our-listings.html')):
    for f in sorted(glob.glob(os.path.join(D, sub, '*.html'))):
        pages[f'{pub}/{os.path.basename(f)[:-5]}'] = open(f, encoding='utf-8').read()
key = lambda path: (lambda q: q[:-5] if q.endswith('.html') else q)(unquote(path).strip('/')) or 'index'

def text_of(h):
    h = re.sub(r'<(script|style|noscript)[^>]*>.*?</\1>', ' ', h, flags=re.S | re.I)
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h)))

def main_html(h):
    m = re.search(r'<main[^>]*>(.*?)</main>', h, re.S | re.I); return m.group(1) if m else h

titles, metas = collections.defaultdict(list), collections.defaultdict(list)
inlinks = collections.Counter(); ids = {}
for slug, h in pages.items():
    ids[slug] = set(re.findall(r'\sid="([^"]+)"', h))
indexable = set()
for slug, h in pages.items():
    if slug == '404': continue
    robots = re.search(r'<meta name="robots" content="([^"]*)"', h); r = robots.group(1) if robots else ''
    if 'noindex' not in r: indexable.add(slug)
    t = re.search(r'<title>(.*?)</title>', h, re.S); t = html.unescape(t.group(1).strip()) if t else ''
    if not t: add('high', 1, slug, 'missing title')
    else:
        titles[t].append(slug)
        if len(t) > 60: add('medium', 1, slug, f'title {len(t)} chars (over 60)', t)
        if len(t) < 30: add('low', 1, slug, f'title {len(t)} chars (short)', t)
        if '…' in t or '...' in t: add('high', 1, slug, 'title cut off with an ellipsis', t)
        if re.search(r'(\||-|–|:)\s*$', t) or re.search(r'\bJared Gi?b?b?o?n?$', t) and not t.endswith('Gibbons'): add('high', 1, slug, 'title cut off', t)
    m = re.search(r'<meta name="description" content="([^"]*)"', h); m = html.unescape(m.group(1)) if m else ''
    if not m: add('high', 1, slug, 'missing meta description')
    else:
        metas[m].append(slug)
        if len(m) > 158: add('medium', 1, slug, f'meta {len(m)} chars (over 158)', m)
        if len(m) < 120: add('medium', 1, slug, f'meta {len(m)} chars (under 120)', m)
        if '…' in m or '...' in m: add('medium', 1, slug, 'meta cut off with an ellipsis', m[-60:])
        if not re.search(r'[.!?)®]$', m): add('medium', 1, slug, 'meta does not end a sentence (cut off?)', m[-60:])
    h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', h, re.S)
    if len(h1s) != 1: add('high', 1, slug, f'{len(h1s)} H1s')
    c = re.search(r'<link rel="canonical" href="([^"]+)"', h)
    if not c: add('high', 2, slug, 'no canonical')
    else:
        cu = c.group(1)
        if not cu.startswith('https://jaredgibbons.ca/'): add('critical', 2, slug, 'canonical not on jaredgibbons.ca', cu)
        else:
            cs = key(urlparse(cu).path)
            if cs != slug: add('medium', 2, slug, 'canonical points to another page', cu)
    body = main_html(h)
    for a in map(html.unescape, re.findall(r'<a\s[^>]*href="([^"]+)"', body)):
        if a.startswith(('mailto:', 'tel:', 'javascript:', 'sms:')): continue
        u = urlparse(a)
        if u.scheme in ('http', 'https') and u.netloc not in ('jaredgibbons.ca', 'www.jaredgibbons.ca'):
            if u.scheme == 'http': add('low', 3, slug, 'http:// link', a)
            if AG.search(a) and 'realtor.ca' not in a: add('high', 3, slug, 'link to another agent or portal', a)
            if 'workers.dev' in a or 'localhost' in a: add('critical', 3, slug, 'link to preview or localhost', a)
            continue
        if u.scheme in ('http', 'https'): path = u.path
        else: path = u.path
        frag = u.fragment if u.scheme else (a.split('#', 1)[1] if '#' in a else '')
        if not path or path == '/': tgt = 'index' if path == '/' else slug
        else:
            p = unquote(path).lstrip('/')
            if p.startswith(('listing-photos', 'api/', '_astro/', 'images/')): continue
            if '/' in p.replace('blog.html/', '').replace('our-listings.html/', ''): continue
            tgt = key(p)
        if tgt not in pages:
            if not re.search(r'\.(pdf|jpg|png|webp|svg|xml|txt)$', tgt): add('high', 3, slug, 'internal link to a missing page', a)
            continue
        if tgt != slug: inlinks[tgt] += 1
        if frag and frag not in ids.get(tgt, set()): add('medium', 3, slug, 'link to a missing #anchor', a)
    for img in re.findall(r'<img\s[^>]*>', body):
        if 'alt=' not in img: add('medium', 6, slug, 'image without alt', img[:120])
        if 'width=' not in img or 'height=' not in img: add('low', 6, slug, 'image without width/height', img[:120])
    for hh in re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', body, re.S):
        ht = text_of(hh).strip()
        if len(ht) > 8 and ht == ht.upper() and re.search(r'[A-Z]{4}', ht): add('low', 6, slug, 'ALL CAPS heading', ht[:80])
    for at, an in re.findall(r'<a\s[^>]*href="([^"]+)"[^>]*>(.*?)</a>', body, re.S):
        tx_ = text_of(an).strip()
        if re.match(r'(https?://|www\.)', tx_): add('low', 3, slug, 'raw URL as link text', tx_[:80])
    tx = text_of(body)
    for mm in WORK.finditer(tx):
        add('medium', 4, slug, f'working text: "{mm.group(0)}"', tx[max(0, mm.start() - 80):mm.end() + 60])
    for mm in re.finditer(r'\b([a-z]{3,})\s+\1\b', tx):
        if mm.group(1).lower() not in ('that', 'had', 'very', 'bye', 'is'): add('low', 4, slug, f'doubled word "{mm.group(1)}"', tx[max(0, mm.start() - 50):mm.end() + 30])
    if re.search(r'Draft for Jared|Draft written for Jared', tx): add('high', 9, slug, 'draft notice visible')
    for js in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try: data = json.loads(js)
        except Exception as e: add('high', 5, slug, 'JSON-LD does not parse', str(e)); continue
        for node in (data if isinstance(data, list) else [data]):
            if node.get('@type') == 'FAQPage':
                norm = lambda z: re.sub(r'\s+', ' ', re.sub(r'([(“‘])\s+', r'\1', re.sub(r'\s+([.,;:!?)’”])', r'\1', z)))
                full = norm(text_of(re.sub(r'<script.*?</script>', ' ', h, flags=re.S)))
                for q in node.get('mainEntity', []):
                    a_ = norm(q.get('acceptedAnswer', {}).get('text', ''))[:80]
                    if a_ and a_ not in full: add('high', 5, slug, 'FAQ answer in JSON-LD not visible on page', a_)
            if node.get('@type') == 'BreadcrumbList':
                for it in node.get('itemListElement', []):
                    iu = it.get('item', '')
                    if isinstance(iu, str) and iu.startswith('https://jaredgibbons.ca/'):
                        s2 = key(urlparse(iu).path)
                        if s2 not in pages: add('high', 5, slug, 'breadcrumb URL missing', iu)
    words = len(tx.split())
    if slug in indexable and words < 300: add('high', 4, slug, f'thin: {words} words in main content')

for t, sl in titles.items():
    if len(sl) > 1: add('high', 1, ','.join(sl[:6]), f'duplicate title x{len(sl)}', t)
for m, sl in metas.items():
    if len(sl) > 1: add('high', 1, ','.join(sl[:6]), f'duplicate meta description x{len(sl)}', m)
for s in indexable:
    if s not in ('index',) and inlinks[s] < 2: add('medium', 3, s, f'orphan: {inlinks[s]} internal links in')
sm = os.path.join(D, 'sitemap.xml')
if os.path.exists(sm):
    locs = re.findall(r'<loc>([^<]+)</loc>', open(sm).read())
    seen = collections.Counter(locs)
    for l, n in seen.items():
        if n > 1: add('medium', 2, l, 'duplicate sitemap entry')
        s = key(urlparse(l).path)
        if s not in pages: add('high', 2, s, 'sitemap URL has no page', l)
        elif s not in indexable: add('high', 2, s, 'noindex page in sitemap', l)
    for s in indexable:
        if f'https://jaredgibbons.ca/{s}' not in seen and f'https://jaredgibbons.ca/{s}.html' not in seen and not (s == 'index' and 'https://jaredgibbons.ca/' in seen): add('medium', 2, s, 'indexable page not in sitemap')

sev = collections.Counter(x[0] for x in F); kinds = collections.Counter((x[0], re.sub(r'\d+', 'N', x[3].split(':')[0].split('"')[0])) for x in F)
print('pages', len(pages), '| indexable', len(indexable), '| findings', len(F), dict(sev))
for (s, k), n in sorted(kinds.items(), key=lambda kv: ('critical', 'high', 'medium', 'low').index(kv[0][0])):
    print(f'  {s:8} {n:5}  {k}')
if OUT:
    with open(OUT, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['severity', 'area', 'slug', 'issue', 'evidence']); w.writerows(F)
