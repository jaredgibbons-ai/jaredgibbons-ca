#!/usr/bin/env python3
"""Low-uniqueness pages from the Cursor audit (D-221, Nov 11, 2026).

Cursor measured eight pages under 0.70 unique. Three Maple Ridge pages are fixed in their local files (the archive's
"Explore Maple Ridge Neighbourhoods" directory, repeated on ~15 pages, is replaced by a link to the neighbourhood guides hub and the
property-type list). For the other five, this drops generated list items and paragraphs in the page's local layer (never Jared's
archive text) when 70% or more of their 8-word shingles also appear on another page, most-shared first, until the page clears 0.72.
The text stays on the page it came from. Idempotent. python3 -I tools/dedupe_low_unique_2026_11_11.py"""
import collections, glob, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT); sys.path.insert(0, 'tools')
import uniqueness as U
TARGETS = sys.argv[1:] or ['brownstones-at-morgan-crossing', 'greentree-village', 'ladner-condos-for-sale', 'abbotsford-duplexes-for-sale', 'aberdeen']
GOAL = 0.72


def load_all():
    pages = {}
    for f in glob.glob('src/data/pages/*.json'):
        d = json.load(open(f)); lf = f'src/data/local/{d["slug"]}.json'
        pages[d['slug']] = (d, json.load(open(lf)) if os.path.exists(lf) else None)
    for f in glob.glob('src/data/local/*.json'):
        l = json.load(open(f)); s = os.path.basename(f)[:-5]
        if l.get('new_page') and s not in pages: pages[s] = ({'slug': s, 'path': '', 'blocks': [{'t': 'h', 'level': 1, 'text': l['new_page']['h1']}]}, l)
    return pages


def shingles(text):
    w = U.words(text); return {' '.join(w[i:i + 8]) for i in range(max(0, len(w) - 7))}


def main():
    pages = load_all()
    sh = {s: shingles(U.page_text(s, d, l)) for s, (d, l) in pages.items()}
    cnt = collections.Counter(x for v in sh.values() for x in v)
    def uniq(S): core = [x for x in S if cnt[x] < 40]; return sum(1 for x in core if cnt[x] == 1) / len(core) if core else 0
    for s in TARGETS:
        d, l = pages[s]; before = uniq(sh[s]); dropped = 0
        cands = []
        for bi, b in enumerate(l['blocks']):
            if b.get('t') == 'list':
                for ii, it in enumerate(b['items']):
                    S = shingles(' '.join(x.get('t', '') for x in it))
                    if len(S) >= 6: cands.append((sum(1 for x in S if 1 < cnt[x] < 40) / len(S), bi, ii, S))
            elif b.get('t') == 'p' and b.get('gen'):
                S = shingles(U.text_of(b))
                if len(S) >= 6: cands.append((sum(1 for x in S if 1 < cnt[x] < 40) / len(S), bi, None, S))
        cands.sort(key=lambda c: -c[0])
        drop = set()
        cur = set(sh[s])
        for share, bi, ii, S in cands:
            if uniq(cur) >= GOAL or share < 0.7: break
            drop.add((bi, ii)); cur -= S; dropped += 1
        if not drop: print(s, round(before, 3), 'no change'); continue
        nb = []
        for bi, b in enumerate(l['blocks']):
            if (bi, None) in drop: continue
            if b.get('t') == 'list':
                b = {**b, 'items': [it for ii, it in enumerate(b['items']) if (bi, ii) not in drop]}
                if not b['items']: continue
            nb.append(b)
        l['blocks'] = nb
        f = f'src/data/local/{s}.json'; raw = open(f).read()
        ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
        open(f, 'w').write((json.dumps(l, ensure_ascii=False, indent=ind) if ind else json.dumps(l, ensure_ascii=False, separators=(',', ':'))) + ('\n' if raw.endswith('\n') else ''))
        print(s, round(before, 3), '->', round(uniq(cur), 3), '| dropped', dropped)


if __name__ == '__main__': main()
