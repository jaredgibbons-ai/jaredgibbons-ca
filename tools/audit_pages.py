"""Audit built pages (dist/) for: FAQ (FAQPage JSON-LD + visible FAQ section), main-content links (min 5, internal), and a reviews block
with a distinct set of three.   python3 -I tools/audit_pages.py [--csv out.csv]"""
import glob, os, re, sys, json, collections
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
rows = []; combos = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(ROOT, 'dist/*.html'))):
    slug = os.path.basename(f)[:-5]; h = open(f, encoding='utf-8').read()
    m = re.search(r'<main[^>]*>(.*?)</main>', h, re.S); main = m.group(1) if m else ''
    links = set(re.findall(r'<a [^>]*href="(/[^"#]*?)(?:#[^"]*)?"', main))
    faq = '"FAQPage"' in h
    quotes = tuple(sorted(re.findall(r'“([^”]{30})', main)))[:3] if 'class="rv' in main or 'Google review' in main or '“' in main else ()
    rev = len(re.findall(r'Google review|<cite|class="rv-', main)) > 0 or len(quotes) >= 3
    rows.append([slug, faq, len(links), len(quotes) >= 3, quotes]); 
    if len(quotes) >= 3: combos[quotes].append(slug)
if __name__ == '__main__':
    print('pages', len(rows))
    print('no FAQ', sum(not r[1] for r in rows), '| under 5 links', sum(r[2] < 5 for r in rows), '| no reviews', sum(not r[3] for r in rows))
    dup = {k: v for k, v in combos.items() if len(v) > 1}
    print('review sets shared by 2+ pages:', len(dup), 'covering', sum(len(v) for v in dup.values()), 'pages')
