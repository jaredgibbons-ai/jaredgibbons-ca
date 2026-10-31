"""Build src/worker/rules.json from docs/archive-extracts/redirects.csv (81 archive rows).

Never guesses: conflicting rows (same From with both a redirect and a 404) and malformed
concatenated-URL rows are listed under `conflicts` / `ignored` with the reason; the Worker
serves 404 for conflicts until Jared decides (docs/05 OI-10).
"""
import csv, json, re, sys
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

host_rules, redirects, gone, conflicts, ignored = [], [], [], [], []
for frm, rs in by_from.items():
    # malformed: two URLs glued together
    if frm.count('http') > 1 or any(r['To URL'].count('http') > 1 for r in rs):
        ignored.append({'from': frm, 'rows': [dict(x) for x in rs], 'reason': 'two URLs concatenated in the archive crawl; not a real route'}); continue
    path, netloc = key(frm)
    if frm.startswith('http://') or netloc.startswith('www.'):
        host_rules.append({'from': frm, 'to': rs[0]['To URL'], 'status': int(rs[0]['Status']), 'rows': len(rs)}); continue
    statuses = {r['Status'] for r in rs}
    kinds = {('redirect' if r['Status'] in ('301', '302') else 'gone') for r in rs}
    if len(kinds) > 1:
        conflicts.append({'from': path, 'rows': [dict(x) for x in rs], 'serving': 404, 'reason': 'archive lists both a redirect and a 404 for this URL; serving 404 until decided (OI-10)'}); continue
    r = rs[0]
    if kinds == {'redirect'}:
        to, tnet = key(r['To URL'])
        redirects.append({'rows': len(rs), 'from': path, 'to': to, 'status': int(r['Status']), 'target_blocked_idx': to.startswith('/recip.html/listing.')})
    else:
        gone.append({'rows': len(rs), 'from': path, 'archive_status': int(r['Status'])})

rules = {
    'generated_from': SRC, 'rows': len(rows),
    'hostRules': host_rules, 'redirects': sorted(redirects, key=lambda x: x['from']),
    'gone': sorted(gone, key=lambda x: x['from']), 'conflicts': conflicts, 'ignored': ignored,
}
json.dump(rules, open(OUT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in rules.items()}))
accounted = sum(len(x['rows']) for x in conflicts + ignored) + sum(x['rows'] for x in host_rules + redirects + gone)
print('rows accounted for', accounted, 'of', len(rows))
