#!/usr/bin/env python3
"""Raise every page to 0.76 unique (D-226, Nov 11, 2026).

After D-224 every page cleared 0.70, but 51 sat at 0.70–0.71. Jared asked to get them comfortably above. What repeats on the low pages is
text copied between sibling pages: archive template paragraphs (the same intro on the house, condo and townhome pages), building notes
(the same complex written up on the area page, the condos page and the guide) and FAQ answers. This keeps each repeated block in full on
one page and drops the copies, lowest-scoring page first, until the page reaches the target:
  - a unit is dropped only when 70% or more of its 8-word shingles are on another page and stay there (the last copy is never dropped);
  - archive paragraphs are hidden through the local layer's `hide`; local list items, paragraphs and FAQ items are removed;
  - a page never drops under 400 words or under 5 FAQ questions (8 on the city-wide 55+ pages); headings left with nothing under them go too.
Never touched: Jared's take, works/doesn't, reviews, sources and link lists, data sentences, headings, blog posts and listings.
Guides are handled last, so a block shared between a guide and a for-sale page stays on the guide.
Idempotent (a second run changes nothing once every page is at the target). python3 -I tools/raise_uniqueness_2026_11_11.py [--target 0.76] [--dry]"""
import collections, glob, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT); sys.path.insert(0, 'tools')
import uniqueness as U
TARGET = float(sys.argv[sys.argv.index('--target') + 1]) if '--target' in sys.argv else 0.76
DRY = '--dry' in sys.argv
MIN_WORDS = 400
MIN_FAQ = {f'{c}-55-plus-homes-for-sale': 8 for c in ('surrey', 'burnaby', 'coquitlam')}


def shingles(t):
    w = U.words(t); return {' '.join(w[i:i + 8]) for i in range(max(0, len(w) - 7))}


def joined(b):   # how GenericPage matches `hide` (parts joined with no space)
    return b.get('text') if b.get('text') is not None else ''.join(x.get('t', '') for x in b.get('parts', []))


def load():
    pages = {}
    for f in glob.glob('src/data/pages/*.json'):
        d = json.load(open(f)); lf = f'src/data/local/{d["slug"]}.json'
        pages[d['slug']] = [d, json.load(open(lf)) if os.path.exists(lf) else None, lf]
    for f in glob.glob('src/data/local/*.json'):
        l = json.load(open(f)); s = os.path.basename(f)[:-5]
        if l.get('new_page') and s not in pages:
            pages[s] = [{'slug': s, 'path': '', 'blocks': [{'t': 'h', 'level': 1, 'text': l['new_page']['h1']}]}, l, f]
    return pages


def visible_archive(d, l):
    """Archive blocks as page_text sees them (after hide/suppress), with their index."""
    out = []; drop = False
    for i, b in enumerate(d['blocks']):
        if b['t'] == 'h' and b.get('level', 9) <= 2 and l and l.get('suppress'): drop = b.get('level') == 2 and b['text'] in l['suppress']
        if drop: continue
        if l and l.get('hide') and b['t'] in ('p', 'h') and any(U.text_of(b).startswith(x) or joined(b).startswith(x) for x in l['hide']): continue
        out.append((i, b))
    return out


def units(slug, d, l):
    """Removable units: (kind, ref, text)."""
    us = []
    vis = visible_archive(d, l)
    for k, (i, b) in enumerate(vis):
        prev = vis[k - 1][1] if k else {}
        if prev.get('t') == 'p' and len(U.words(U.text_of(prev))) <= 4: continue   # the answer under a "Look at" / "Ask" label: keeps the card set whole
        if b['t'] == 'p' and len(U.words(U.text_of(b))) >= 12 and not any(x.get('h') for x in b.get('parts', [])[:1]):
            us.append(('hide', joined(b)[:70], U.text_of(b)))
    if l:
        for bi, b in enumerate(l.get('blocks', [])):
            if b.get('gen') in ('jvoice',) or b.get('t') == 'reviews': continue
            if b.get('t') == 'list':
                for ii, it in enumerate(b['items']):
                    if len(it) == 1 and it[0].get('h'): continue
                    t = ' '.join(x.get('t', '') for x in it)
                    if len(U.words(t)) >= 10: us.append(('item', (bi, ii), t))
            elif b.get('t') == 'p' and b.get('gen') and len(U.words(U.text_of(b))) >= 12:
                us.append(('lp', (bi, None), U.text_of(b)))
        for fi, f in enumerate(l.get('faq', [])):
            us.append(('faq', fi, f['q'] + ' ' + f['a']))
    return us


def main():
    pages = load()
    S = {s: shingles(U.page_text(s, d, l)) for s, (d, l, _) in pages.items()}
    W = {s: len(U.words(U.page_text(s, d, l))) for s, (d, l, _) in pages.items()}
    cnt = collections.Counter(x for v in S.values() for x in v)
    def uniq(s):
        core = [x for x in S[s] if cnt[x] < 40]
        return sum(1 for x in core if cnt[x] == 1) / len(core) if core else 1
    order = sorted(pages, key=lambda s: (s.endswith('-guide'), uniq(s)))   # guides keep their copy: sibling pages give theirs up first
    changed, report = set(), []
    for s in order:
        u0 = uniq(s)
        if u0 >= TARGET: continue
        d, l, lf = pages[s]
        if l is None: continue
        cands = []
        for kind, ref, t in units(s, d, l):
            X = shingles(t) & S[s]
            if len(X) < 6: continue
            share = sum(1 for x in X if 1 < cnt[x] < 40) / len(X)
            if share >= 0.7: cands.append((share * len(X), share, kind, ref, t, X))
        cands.sort(key=lambda c: -c[0])
        rm = []; faq_left = len(l.get('faq', []))
        for _, share, kind, ref, t, X in cands:
            if uniq(s) >= TARGET: break
            if W[s] - len(U.words(t)) < MIN_WORDS: continue
            if kind == 'faq' and faq_left <= MIN_FAQ.get(s, 5): continue        # pages keep at least 5 questions (8 on the city-wide 55+ pages)
            if kind == 'faq': faq_left -= 1
            if any(cnt[x] < 2 for x in X if 1 < cnt[x] < 40): continue
            for x in X: cnt[x] -= 1
            S[s] -= X; W[s] -= len(U.words(t)); rm.append((kind, ref))
        if not rm: report.append((s, round(u0, 3), round(uniq(s), 3), 0)); continue
        hide = [r for k, r in rm if k == 'hide']; items = {r for k, r in rm if k in ('item', 'lp')}; faqs = {r for k, r in rm if k == 'faq'}
        if hide: l['hide'] = sorted(set(l.get('hide', []) + hide))
        nb = []
        for bi, b in enumerate(l.get('blocks', [])):
            if (bi, None) in items: continue
            if b.get('t') == 'list':
                its = [it for ii, it in enumerate(b['items']) if (bi, ii) not in items]
                if not its: continue
                b = {**b, 'items': its}
            nb.append(b)
        # headings left with nothing under them (next block is a heading of the same or higher level, or the end)
        out = []
        for k, b in enumerate(nb):
            if b.get('t') == 'h':
                nxt = next((x for x in nb[k + 1:]), None)
                if nxt is None or (nxt.get('t') == 'h' and nxt.get('level', 9) <= b.get('level', 9)):
                    if b.get('gen'): continue
            out.append(b)
        l['blocks'] = out
        if faqs: l['faq'] = [f for fi, f in enumerate(l.get('faq', [])) if fi not in faqs]
        changed.add(s); report.append((s, round(u0, 3), round(uniq(s), 3), len(rm)))
    if not DRY:
        for s in changed:
            d, l, lf = pages[s]; raw = open(lf).read()
            ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
            open(lf, 'w').write((json.dumps(l, ensure_ascii=False, indent=ind) if ind else json.dumps(l, ensure_ascii=False, separators=(',', ':'))) + ('\n' if raw.endswith('\n') else ''))
    still = [r for r in report if r[2] < TARGET]
    print(f'pages under {TARGET}: {sum(1 for r in report)} | changed {len(changed)} | still under (estimate) {len(still)}')
    for r in still[:40]: print('  still', r)


if __name__ == '__main__': main()
