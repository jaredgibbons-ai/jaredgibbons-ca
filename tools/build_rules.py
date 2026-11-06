"""Build src/worker/rules.json from docs/archive-extracts/redirects.csv (81 archive rows).

Never guesses: conflicting rows (same From with both a redirect and a 404) and malformed
concatenated-URL rows are listed under `conflicts` / `ignored` with the reason; the Worker
serves 404 for conflicts until Jared decides (docs/05 OI-10).
"""
import csv, json, os, re, sys
from collections import defaultdict
from urllib.parse import urlsplit

SRC = 'docs/archive-extracts/redirects.csv'
OUT = 'src/worker/rules.json'
HOST = 'jaredgibbons.ca'

def key(u):
    s = urlsplit(u)
    return s.path + (('?' + s.query) if s.query else ''), s.netloc

rows = list(csv.DictReader(open(SRC, encoding='utf-8', newline='')))
by_from = defaultdict(list)
for r in rows:
    by_from[r['From URL']].append(r)

host_rules, redirects, gone, conflicts, ignored, doubled = [], [], [], [], [], []
for frm, rs in by_from.items():
    # malformed: two URLs glued together
    if frm.count('http') > 1 or any(r['To URL'].count('http') > 1 for r in rs):
        ignored.append({'from': frm, 'rows': [dict(x) for x in rs], 'reason': 'two URLs concatenated in the archive crawl; not a real route'}); continue
    path, netloc = key(frm)
    if path == '/this-page-does-not-exist-archive-check':
        continue   # the crawler's own 404 probe, not a route (D-140)
    if frm.startswith('http://') or netloc.startswith('www.'):
        host_rules.append({'from': frm, 'to': rs[0]['To URL'], 'status': int(rs[0]['Status']), 'rows': len(rs)}); continue
    statuses = {r['Status'] for r in rs}
    kinds = {('redirect' if r['Status'] in ('301', '302') else 'gone') for r in rs}
    if len(kinds) > 1:
        conflicts.append({'from': path, 'rows': [dict(x) for x in rs], 'serving': 404, 'reason': 'archive lists both a redirect and a 404 for this URL; serving 404 until decided (OI-10)'}); continue
    r = rs[0]
    # D-140: a 403 row shaped /<page>.html/<other-page>.html is a doubled relative-link prefix on the old site (a blocked crawl, not a dead page);
    # route.js redirects it to /<other-page>.html when that page exists, so it is not a 404 row.
    if kinds == {'gone'} and r['Status'] == '403' and re.fullmatch(r'/[^/]+\.html/[^/]+\.html', path):
        doubled.append(path); continue
    if kinds == {'redirect'}:
        to, tnet = key(r['To URL'])
        blocked = to.startswith('/recip.html/listing.')
        # D-140: /recip.html/listing.* cannot resolve (the MLS search is a widget), so 23 rows pointed at a 404. They go to the search page.
        redirects.append({'rows': len(rs), 'from': path, 'to': '/recip.html' if blocked else to, 'status': int(r['Status']), 'target_blocked_idx': blocked})
    else:
        gone.append({'rows': len(rs), 'from': path, 'archive_status': int(r['Status'])})

# Redirects seen on the live site after the archive was taken (docs/05 OI-25). The archive wins on any conflict.
LIVE = 'docs/archive-extracts/live-observed-redirects.csv'
known = {r['from'] for r in redirects} | {g['from'] for g in gone} | {c['from'] for c in conflicts}
live_added = 0
if os.path.exists(LIVE):
    for r in csv.DictReader(open(LIVE, encoding='utf-8', newline='')):
        path, _ = key(r['From URL']); to, _ = key(r['To URL'])
        if path in known:
            continue
        redirects.append({'rows': 1, 'from': path, 'to': to, 'status': int(r['Status']), 'target_blocked_idx': False, 'source': 'live-observed'})
        live_added += 1

# D-140 overrides (each a decision, not a guess). A redirect row whose source is in here is repointed; a gone row becomes a redirect or a 410.
REPOINT = {
    '/langley-condos-under-700k.html': '/langley-condos-for-sale.html',   # was -under-499k, a lower price band than the one asked for
}
for r in redirects:
    if r['from'] in REPOINT: r['to'] = REPOINT[r['from']]
GONE_TO_REDIRECT = {'/bc-property-transfer-tax-calculator.html': '/first-time-buyer-calculator.html'}   # page had inbound equity; the PTT, GST and FHSA calculator is the live answer
for g in list(gone):
    if g['from'] in GONE_TO_REDIRECT:
        gone.remove(g); redirects.append({'rows': g['rows'], 'from': g['from'], 'to': GONE_TO_REDIRECT[g['from']], 'status': 301, 'target_blocked_idx': False})
# An RSS feed URL that was never a feed here: 410 Gone, not a 301 to HTML (a feed reader would choke on it).
for r in list(redirects):
    if r['from'] == '/blog.html/blog.feed':
        redirects.remove(r); gone.append({'rows': r['rows'], 'from': r['from'], 'archive_status': 410, 'serve': 410})

rules = {
    'generated_from': SRC, 'rows': len(rows), 'live_observed_rows': live_added, 'doubled_prefix_paths': sorted(doubled),
    # Rows handled in code, not in the tables: http/www host redirects (route.js), the crawler's 404 probe (dropped), doubled-prefix pages (route.js 2c).
    'rows_in_code': {'host_http_www': sum(x['rows'] for x in host_rules), 'crawler_probe': 1, 'doubled_prefix': len(doubled)},
    'redirects': sorted(redirects, key=lambda x: x['from']),
    'gone': sorted(gone, key=lambda x: x['from']), 'conflicts': conflicts, 'ignored': ignored,
}
json.dump(rules, open(OUT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in rules.items()}))
accounted = sum(len(x['rows']) for x in conflicts + ignored) + sum(x['rows'] for x in redirects + gone) + sum(rules['rows_in_code'].values())
print('live-observed redirects added', live_added)
print('rows accounted for', accounted - live_added, 'of', len(rows))
