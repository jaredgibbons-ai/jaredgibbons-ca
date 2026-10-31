"""Build the route manifest from the archive URL inventory (urls-part1..3.csv; same rows as urls.csv in archive folder 01).
Usage: python3 -I tools/build_manifest.py
Writes: routes/manifest.csv (every inventoried URL, 1 row each), routes.json (summary + canonical page/blog routes).
Rules are in classify(); dispositions follow docs/04 (A-03 expired listings, BL-04 IDX)."""
import csv, io, json, re, collections
from urllib.parse import urlparse, parse_qs

SRC = [f'docs/archive-extracts/urls/part{i}.csv' for i in (1, 2, 3)]
IMPLEMENTED = {'/': 'implemented-preview', '/fort-langley.html': 'implemented-preview', '/reviews.html': 'implemented-preview'}

rows = []
for p in SRC:
    rows += list(csv.DictReader(open(p, encoding='utf-8', newline='')))

def classify(r):
    u = urlparse(r['URL']); path = u.path or '/'; q = parse_qs(u.query)
    host_ok = u.netloc == 'jaredgibbons.ca'
    if path == '/' and not u.query and u.netloc in ('jaredgibbons.ca', 'www.jaredgibbons.ca'):
        fam = 'home'
    elif path in ('', '/') or (not path.endswith('.html') and path.rstrip('/') == ''):
        fam = 'home-variant'
    elif 'listing.' in path.split('/')[-1] and '/' in path[1:]:
        parent = path.split('/')[1]
        fam = 'listing-own' if parent in ('our-listings.html', 'mylistings.html') else 'listing-idx'
    elif path.startswith('/recip.html/') and path.endswith('.form'):
        fam = 'idx-search-form'
    elif path.endswith('.feed'):
        fam = 'feed'
    elif path == '/blog.html':
        fam = 'blog-index'
    elif path.startswith('/blog.html/') and path.count('/') == 2 and not path.endswith('.html') and not path.endswith('.feed'):
        fam = 'blog-post'
    elif path.endswith('.html') and path.count('/') == 1:
        fam = 'page'
    elif path.endswith('.html') and path.count('/') >= 2:
        fam = 'nested-page-artifact'
    elif path.endswith('/'):
        fam = 'trailing-slash-legacy'
    else:
        fam = 'other'
    # query variants
    variant = None
    if u.query:
        if '_pg' in q: variant = 'pagination'
        elif 'preview' in q or 'p' in q: variant = 'cms-preview-noise'
        elif 'utm_source' in q: variant = 'tracking'
        elif 'cat' in q or 'blog' in q: variant = 'blog-filter'
        else: variant = 'other-query'
    return fam, variant, path

def disposition(r, fam, variant, path):
    st = r['HTTP status']; cap = r['Capture status']
    if cap == 'Broken at source' or st in ('403', '404') and fam != 'home':
        return 'serve-404', 'Broken or 404 at source; recorded, not rebuilt'
    if variant == 'pagination': return 'worker-pagination', '?_pg=N handled by routing Worker on the parent page'
    if variant == 'cms-preview-noise': return 'canonicalize-to-path', 'CMS preview parameters; not a real route'
    if variant == 'tracking': return 'canonicalize-to-path', 'Tracking parameter; canonical is the clean URL'
    if variant == 'blog-filter': return 'review', 'Blog filter query; confirm behaviour when blog.html is built'
    if cap == 'Redirect': return 'redirect', 'Archive observed redirect to Final URL; apply redirects.csv rules and flag conflicts'
    return {
        'home': ('rebuild', 'Homepage'),
        'home-variant': ('redirect', 'http/www/no-slash variants to https://jaredgibbons.ca/'),
        'page': ('rebuild', 'Page record in archive folder 02'),
        'blog-index': ('rebuild', 'Blog index'),
        'blog-post': ('rebuild', 'Blog post'),
        'feed': ('review', 'RSS feed; keep if feed is used by subscribers'),
        'listing-own': ('rebuild-own-listing', "Jared's own listing; A-03 (keep page; expired = noindex + similar listings)"),
        'listing-idx': ('blocked-idx', 'Other brokerages\' MLS listing; depends on IDX decision BL-04 and A-03'),
        'idx-search-form': ('blocked-idx', 'IDX search result form; does not transfer'),
        'nested-page-artifact': ('serve-404', 'Page slug nested under another page; recorded as archive artifact'),
        'trailing-slash-legacy': ('redirect', 'Legacy trailing-slash path'),
        'other': ('review', ''),
    }[fam]

out = []
for r in rows:
    fam, variant, path = classify(r)
    disp, note = disposition(r, fam, variant, path)
    base = path + (('?' + urlparse(r['URL']).query) if urlparse(r['URL']).query else '')
    status = 'not-started'
    if disp.startswith('blocked'): status = 'blocked'
    elif disp in ('serve-404', 'canonicalize-to-path', 'worker-pagination', 'redirect'): status = 'rule-pending'
    if base in IMPLEMENTED and r['URL'] == f'https://jaredgibbons.ca{base}': status = IMPLEMENTED[base]
    out.append({
        'url': r['URL'], 'path_query': base, 'source': r['Source'], 'http_status': r['HTTP status'],
        'final_url': r['Final URL'], 'capture_status': r['Capture status'],
        'family': fam, 'query_variant': variant or '', 'disposition': disp, 'status': status, 'note': note,
        'archive_note': r['Notes'],
    })

with open('routes/manifest.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)

C = collections.Counter
canon = sorted({(o['path_query'], o['family']) for o in out if o['family'] in ('page', 'blog-post', 'blog-index', 'home') and not o['query_variant'] and o['disposition'] in ('rebuild',)})
pages = [{'path': p, 'family': fam, 'status': IMPLEMENTED.get(p, 'not-started')} for p, fam in canon]
# unique listings
def lid(p):
    m = re.search(r'\.(\d+)$', p); return m.group(1) if m else p
listing_ids = {lid(o['path_query']) for o in out if o['family'].startswith('listing')}
summary = {
    'generated': '2026-10-31',
    'source': 'docs/archive-extracts/urls/part1..3.csv (21,014 rows, matches archive coverage report)',
    'note': 'Full per-URL manifest is routes/manifest.csv. This file lists canonical rebuildable pages/posts and the roll-up counts. Status values: not-started | implemented-preview | validated | blocked | rule-pending | failed.',
    'totals': {'inventoried_urls': len(out), 'unique_listing_ids': len(listing_ids)},
    'by_family': dict(C(o['family'] for o in out).most_common()),
    'by_disposition': dict(C(o['disposition'] for o in out).most_common()),
    'by_status': dict(C(o['status'] for o in out).most_common()),
    'by_capture_status': dict(C(o['capture_status'] for o in out).most_common()),
    'query_variants': dict(C(o['query_variant'] for o in out if o['query_variant']).most_common()),
    'canonical_pages_and_posts': len(pages),
    'routes': pages,
}
json.dump(summary, open('routes.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in summary.items() if k != 'routes'}, indent=1))
