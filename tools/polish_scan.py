#!/usr/bin/env python3
"""Whole-site copy and markup polish scan on a built site (D-230, Nov 11, 2026). Every page, main content only.
Flags: template leftovers (undefined, NaN, [object, {{), spacing and punctuation slips, singular/plural mismatches with 1, a/an before
numbers, empty headings, duplicate headings on a page, headings with nothing under them, doubled ® marks, raw markdown, very long
sentences. python3 -I tools/polish_scan.py <dist> [--csv out.csv]"""
import collections, csv, glob, html, os, re, sys
D = sys.argv[1]; OUT = sys.argv[sys.argv.index('--csv') + 1] if '--csv' in sys.argv else ''
F = []
def add(kind, page, ev): F.append((kind, page, ev[:220]))
pages = sorted(glob.glob(os.path.join(D, '*.html')) + glob.glob(os.path.join(D, 'internal/*/*.html')))
CHECKS = [
    ('template leftover', re.compile(r'\b(undefined|NaN|null|None)\b(?! of)|\[object|\{\{|\}\}|\$\{')),
    ('space before punctuation', re.compile(r'\w \.(?![\d\w])|\w ,')),
    ('doubled punctuation', re.compile(r'(?<!\.)\.\.(?!\.)|,,|;;|::|\?\?|\(\s*\)')),
    ('one + plural', re.compile(r'(?<![\d,.$])\b1 (homes|houses|condos|townhomes|sales|listings|days|bedrooms|years|acres|schools|units|buildings)\b')),
    ('a/an before a number', re.compile(r'\ban [1-79]\d*\b(?!\s*(?:-|to)\s*\d)|\ba 8\d*\b|\ba 11\b|\ba 18\b')),
    ('doubled mark', re.compile(r'®®|MLS® ®|REALTOR® ®')),
    ('raw markdown', re.compile(r'\*\*\w|\]\(http|^#+ ', re.M)),
    ('lowercase after full stop', re.compile(r'[a-z]{3}\. (?!e\.g|i\.e|vs|etc|ft|sq|m²|km|ha)[a-z]{3,}')),
]
for f in pages:
    rel = os.path.relpath(f, D); h = open(f, encoding='utf-8').read()
    m = re.search(r'<main[^>]*>(.*)</main>', h, re.S); body = m.group(1) if m else h
    body = re.sub(r'<(script|style|noscript)[^>]*>.*?</\1>', ' ', body, flags=re.S | re.I)
    txt = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', body)))
    plain = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', body)))   # no spaces added at tag edges, for punctuation checks
    for kind, rx in CHECKS:
        src = plain if kind in ('space before punctuation', 'doubled punctuation', 'lowercase after full stop') else txt
        for mm in rx.finditer(src):
            add(kind, rel, src[max(0, mm.start() - 70):mm.end() + 50].replace('\n', ' '))
    hs = re.findall(r'<h([1-6])[^>]*>(.*?)</h\1>', body, re.S)
    texts = [html.unescape(re.sub(r'<[^>]+>', '', t)).strip() for _, t in hs]
    for t in texts:
        if not t: add('empty heading', rel, '')
    for t, n in collections.Counter(t for t in texts if t).items():
        if n > 1: add('duplicate heading', rel, f'{t} x{n}')
    # a heading followed directly by another heading of the same or higher level
    seq = re.findall(r'<(h[1-6]|p|ul|ol|table|div|section|details|figure|img|form|iframe|a)\b', body)
    for i in range(len(seq) - 1):
        if seq[i].startswith('h') and seq[i + 1].startswith('h') and int(seq[i + 1][1]) <= int(seq[i][1]) and seq[i] != 'h1':
            add('heading with nothing under it', rel, f'{seq[i]} then {seq[i + 1]}')
    for para in re.findall(r'<p\b[^>]*>(.*?)</p>', body, re.S):
        pt = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', para)))
        for s in re.split(r'(?<=[.!?])\s+', pt):
            if len(s.split()) > 60: add('very long sentence', rel, s)
by = collections.Counter(k for k, _, _ in F)
print('pages', len(pages), '| findings', len(F)); [print(f'  {n:6} {k}') for k, n in by.most_common()]
if OUT:
    with open(OUT, 'w', newline='') as fh: w = csv.writer(fh); w.writerow(['kind', 'page', 'evidence']); w.writerows(F)
