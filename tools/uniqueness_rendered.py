#!/usr/bin/env python3
"""Uniqueness measured on the built pages, the way an outside crawler sees them (D-227).

tools/uniqueness.py measures the page data; it misses what components render (sold-price tables, quick facts, maps' captions) and counts
text a component hides. This reads dist/*.html: the <main> text minus the reviews carousel, then the same metric (8-word shingles,
boilerplate on 40+ pages dropped, share appearing on no other page). Covers the pages in src/data/pages and the new local pages.
python3 -I tools/uniqueness_rendered.py [dist] [--csv out.csv] [--below 0.76]"""
import collections, csv, glob, html, os, re, sys
D = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else 'dist'
OUT = sys.argv[sys.argv.index('--csv') + 1] if '--csv' in sys.argv else ''
BELOW = float(sys.argv[sys.argv.index('--below') + 1]) if '--below' in sys.argv else 0.76


def main_text(h):
    m = re.search(r'<main[^>]*>(.*)</main>', h, re.S); h = m.group(1) if m else h
    h = re.sub(r'<(script|style|noscript|nav)[^>]*>.*?</\1>', ' ', h, flags=re.S | re.I)
    h = re.sub(r'<section[^>]*class="[^"]*(?:reviews|rev\b|awm)[^"]*"[^>]*>.*?</section>', ' ', h, flags=re.S | re.I)
    h = re.sub(r'<(form|button|select|figure|blockquote)[^>]*>.*?</\1>', ' ', h, flags=re.S | re.I)   # client reviews are quotes, shown across pages
    h = re.sub(r'<p class="(?:rv__w|stars)"[^>]*>.*?</p>', ' ', h, flags=re.S)
    # navigation: lists whose items are only links (search engines treat link lists as boilerplate, as tools/uniqueness.py does)
    def navlist(m):
        items = re.findall(r'<li[^>]*>(.*?)</li>', m.group(0), re.S)
        if items and all(re.fullmatch(r'\s*(?:<[^a][^>]*>\s*)*<a\b[^>]*>.*?</a>\s*(?:<[^>]+>\s*)*[^<]{0,40}', it, re.S) for it in items): return ' '
        return m.group(0)
    h = re.sub(r'<(ul|ol)\b[^>]*>.*?</\1>', navlist, h, flags=re.S | re.I)
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h)))


words = lambda s: re.findall(r"[A-Za-z0-9$%'’.\-]+", s.lower())
S = {}; W = {}
for f in glob.glob(os.path.join(D, '*.html')):
    slug = os.path.basename(f)[:-5]
    if slug in ('404',): continue
    w = words(main_text(open(f, encoding='utf-8').read())); W[slug] = len(w)
    S[slug] = {' '.join(w[i:i + 8]) for i in range(max(0, len(w) - 7))}
cnt = collections.Counter(x for v in S.values() for x in v)
rows = []
for s, sh in S.items():
    core = [x for x in sh if cnt[x] < 40]
    rows.append((s, W[s], round(sum(1 for x in core if cnt[x] == 1) / len(core), 3) if core else 1.0))
rows.sort(key=lambda r: r[2])
low = [r for r in rows if r[2] < BELOW]
print(f'pages {len(rows)} | under {BELOW}: {len(low)} | under 0.70: {sum(1 for r in rows if r[2] < 0.7)}')
for r in low[:25]: print(' ', *r)
if OUT:
    with open(OUT, 'w', newline='') as fh: w = csv.writer(fh); w.writerow(['slug', 'words', 'unique']); w.writerows(rows)
if '--why' in sys.argv:   # most common shared passages on the pages under the bar
    lowset = {r[0] for r in low}
    c = collections.Counter(x for s in lowset for x in S[s] if 1 < cnt[x] < 40)
    for x, n in c.most_common(int(sys.argv[sys.argv.index('--why') + 1])): print(n, cnt[x], '|', x)
