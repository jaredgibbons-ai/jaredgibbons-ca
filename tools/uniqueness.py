"""Uniqueness + word count per page, counting archive blocks and the local layer (src/data/local).

    python3 -I tools/uniqueness.py [--slugs a,b,c] [--csv out.csv] [--min-unique 0.7] [--min-words 300]

Metric: of the 8-word shingles in a page's main content, the share that appear on no other page. Site-wide boilerplate
(shingles found on 40+ pages: contact block, reviews intro, disclaimers, related-link lists) is dropped from both sides, as search
engines do. `unique_all` keeps boilerplate in, for reference.
"""
import argparse, csv, glob, json, os, re, sys
from collections import Counter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')


def text_of(b):
    t = b.get('t')
    if 'parts' in b: return ' '.join(x['t'] for x in b['parts'])
    if t == 'h': return b['text']
    if t == 'p': return b.get('text', '')
    if t == 'list':
        if all(len(it) == 1 and it[0].get('h') for it in b['items']): return ''  # a list of nothing but links is navigation, not body text (search engines treat it as boilerplate)
        return ' '.join(' '.join(x['t'] for x in it) for it in b['items'])
    if t == 'table': return ' '.join([b.get('caption', '')] + b['head'] + [c for r in b['rows'] for c in r])
    if t == 'notice': return ''  # preview-only notes are not page content
    return ''


def page_text(slug, page, local):
    blocks = list(page['blocks'])
    if local and local.get('suppress'):
        keep, drop = [], False
        for b in blocks:
            if b['t'] == 'h' and b['level'] <= 2: drop = b['level'] == 2 and b['text'] in local['suppress']
            if not drop or b['t'] in ('reviews', 'grid', 'form'): keep.append(b)
        blocks = keep
    if local:
        blocks += local['blocks'] + [{'t': 'p', 'text': f['q'] + ' ' + f['a']} for f in local.get('faq', [])]
    return ' '.join(text_of(b) for b in blocks)


def words(s): return re.findall(r"[A-Za-z0-9$%'’.\-]+", s.lower())


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--slugs', default=''); ap.add_argument('--csv', default='')
    ap.add_argument('--write-gate', action='store_true'); ap.add_argument('--min-unique', type=float, default=0.7); ap.add_argument('--min-words', type=int, default=300)
    a = ap.parse_args()
    pages, shingles, cnt = {}, {}, Counter(); new_slugs = set()
    for f in glob.glob(os.path.join(ROOT, 'src/data/pages/*.json')):
        d = json.load(open(f)); lf = os.path.join(ROOT, 'src/data/local', d['slug'] + '.json')
        local = json.load(open(lf)) if os.path.exists(lf) else None
        w = words(page_text(d['slug'], d, local))
        sh = {' '.join(w[i:i + 8]) for i in range(max(0, len(w) - 7))}
        pages[d['slug']] = (d, len(w), local); shingles[d['slug']] = sh
        cnt.update(sh)
    for f in glob.glob(os.path.join(ROOT, 'src/data/local/*.json')):  # brand-new pages (no archive counterpart) are measured too
        l = json.load(open(f)); slug = os.path.basename(f)[:-5]
        if not l.get('new_page') or slug in pages: continue
        d = {'slug': slug, 'path': f'/{slug}.html', 'blocks': [{'t': 'h', 'level': 1, 'text': l['new_page']['h1']}]}
        w = words(page_text(slug, d, l)); sh = {' '.join(w[i:i + 8]) for i in range(max(0, len(w) - 7))}
        pages[slug] = (d, len(w), l); shingles[slug] = sh; cnt.update(sh); new_slugs.add(slug)
    rows = []
    for s, (d, n, local) in pages.items():
        sh = shingles[s]; ua = sum(1 for x in sh if cnt[x] == 1) / len(sh) if sh else 0
        core = [x for x in sh if cnt[x] < 40]; u = sum(1 for x in core if cnt[x] == 1) / len(core) if core else 0
        rows.append((s, d['path'], n, round(u, 3), round(ua, 3), 'local' if local else ''))
    want = set(a.slugs.split(',')) if a.slugs else None
    out = [r for r in rows if not want or r[0] in want]
    out.sort(key=lambda r: r[3])
    for r in out[:60 if not want else None]: print(*r)
    if a.csv:
        with open(a.csv, 'w', newline='') as f:
            w = csv.writer(f); w.writerow(['slug', 'path', 'words', 'unique', 'unique_all', 'layer']); w.writerows(rows)
    bad = [r for r in rows if r[0].endswith('-guide') and (r[3] < a.min_unique or r[2] < a.min_words)]
    print(f'guides under thresholds: {len(bad)}')
    newrows = [r for r in rows if r[0] in new_slugs]
    low = [r for r in newrows if r[3] < a.min_unique]
    print(f'new pages: {len(newrows)}; under {a.min_unique}: {len(low)}')
    if a.write_gate:  # launch gate: new pages under the threshold stay noindex and out of the sitemap until their copy is raised
        json.dump({'min_unique': a.min_unique, 'enforce': False, 'scores': {r[0]: r[3] for r in sorted(newrows)}}, open(os.path.join(ROOT, 'src/data/inventory/uniqueness.json'), 'w'), indent=1); open(os.path.join(ROOT, 'src/data/inventory/uniqueness.json'), 'a').write('\n')


if __name__ == '__main__':
    main()
