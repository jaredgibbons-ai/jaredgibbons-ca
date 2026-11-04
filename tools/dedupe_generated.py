"""One copy of a repeated generated block: keep it on its best page, drop it from the thin pages that only carry a copy.

Why: the 8-word-phrase uniqueness score (tools/uniqueness.py) and search engines both treat the same generated paragraph on several pages as duplicate text. Many generated
blocks (sold figures, bank/school FAQs, mobile-home rules, 55+ notes, duplex notes) are word-for-word the same on an area's houses page, condo page, guide and price-band pages,
or the same rules appear on every mobile-home page.

Rule: blocks and FAQ answers in src/data/local/*.json (not Jared's own words, not 'Areas near') are clustered when one contains >= 60% of the other's phrases.
The owner of a cluster is a hub page if one is in it, else a page that is not under the threshold, else the page with the shortest slug. Copies are dropped only from pages
currently under 0.7 unique, only if the page keeps >= 300 words, and each page that loses blocks gets one pointer line with a link to the owner pages. Re-runnable after the
builders (they re-add the blocks, this removes them again): run last in the chain, before the final build.
    python3 -I tools/dedupe_generated.py [--dry] [--scores /path/to/uniqueness.csv]"""
import csv, glob, json, os, re, sys
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
sys.path.insert(0, HERE)
import uniqueness as U
LOCAL = os.path.join(ROOT, 'src/data/local'); PAGES = os.path.join(ROOT, 'src/data/pages'); GEN = 'dedupe'
KEEP_GENS = {'jtake', 'near2', GEN}
HUBS = ['mobile-home-parks-fraser-valley']
MIN_WORDS, CONTAIN, MIN_BLOCK = 300, 0.6, 20
def sh_of(w): return {' '.join(w[i:i + 8]) for i in range(max(0, len(w) - 7))}
def load():
    pages, local = {}, {}
    for f in glob.glob(PAGES + '/*.json'):
        d = json.load(open(f, encoding='utf-8')); pages[d['slug']] = d
    for f in glob.glob(LOCAL + '/*.json'):
        local[os.path.basename(f)[:-5]] = json.load(open(f, encoding='utf-8'))
    for s, l in local.items():
        if l.get('new_page') and s not in pages:
            pages[s] = {'slug': s, 'path': f'/{s}.html', 'blocks': [{'t': 'h', 'level': 1, 'text': l['new_page']['h1']}]}
    return pages, local
def page_words_shingles(slug, pages, local, drop=()):
    d, l = pages[slug], local.get(slug)
    if l and drop:
        l = dict(l); l['blocks'] = [b for i, b in enumerate(l.get('blocks', [])) if ('B', i) not in drop]; l['faq'] = [f for i, f in enumerate(l.get('faq', [])) if ('F', i) not in drop]
    w = U.words(U.page_text(slug, d, l)); return w, sh_of(w)
def scores(pages, local, drops):
    full, words = {}, {}
    for s in pages:
        w, sh = page_words_shingles(s, pages, local, drops.get(s, ())); full[s] = sh; words[s] = len(w)
    cnt = Counter()
    for sh in full.values(): cnt.update(sh)
    out = {}
    for s, sh in full.items():
        core = [x for x in sh if cnt[x] < 40]; out[s] = sum(1 for x in core if cnt[x] == 1) / len(core) if core else 0
    return out, words, cnt
def main():
    dry = '--dry' in sys.argv
    pages, local = load()
    for s, l in local.items():                       # idempotent: remove our own pointer blocks first
        if any(b.get('gen') == GEN for b in l.get('blocks', [])): l['blocks'] = [b for b in l['blocks'] if b.get('gen') != GEN]
    base, bw, cnt = scores(pages, local, {})
    low = {s for s, v in base.items() if v < 0.7}
    items = []                                       # (slug, kind, index, shingles, words)
    for s, l in local.items():
        if s not in pages: continue
        for i, b in enumerate(l.get('blocks', [])):
            if b.get('gen') in KEEP_GENS or b['t'] in ('h', 'photo'): continue
            w = U.words(U.text_of(b))
            if len(w) >= MIN_BLOCK: items.append((s, 'B', i, {x for x in sh_of(w) if cnt[x] < 40}, len(w)))
        for i, f in enumerate(l.get('faq', [])):
            if f.get('gen') in KEEP_GENS: continue
            w = U.words(f['q'] + ' ' + f['a'])
            if len(w) >= MIN_BLOCK: items.append((s, 'F', i, {x for x in sh_of(w) if cnt[x] < 40}, len(w)))
    items = [it for it in items if it[3]]
    idx = defaultdict(list)
    for n, it in enumerate(items):
        for x in it[3]: idx[x].append(n)
    parent = list(range(len(items)))
    def find(a):
        while parent[a] != a: parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for n, it in enumerate(items):
        hits = Counter(m for x in it[3] for m in idx[x] if m != n and items[m][0] != it[0])
        for m, c in hits.items():
            if c / min(len(it[3]), len(items[m][3])) >= CONTAIN: parent[find(n)] = find(m)
    clusters = defaultdict(list)
    for n in range(len(items)): clusters[find(n)].append(n)
    drops = defaultdict(set); owners = defaultdict(set); ncl = 0
    for ms in clusters.values():
        slugs = {items[m][0] for m in ms}
        if len(slugs) < 2: continue
        ncl += 1
        pick = lambda s: (0 if s in HUBS else 1 if s not in low else 2, len(s), s)
        owner = min(slugs, key=pick)
        for m in ms:
            s, kind, i, _, _ = items[m]
            if s != owner and s in low: drops[s].add((kind, i)); owners[s].add(owner)
    # keep >= MIN_WORDS words on every page
    for s in list(drops):
        w, _ = page_words_shingles(s, pages, local, drops[s])
        if len(w) < MIN_WORDS:
            order = sorted(drops[s], key=lambda k: -len(U.words(json.dumps(local[s]['blocks'][k[1]] if k[0] == 'B' else local[s]['faq'][k[1]]))))
            while order and len(page_words_shingles(s, pages, local, set(order))[0]) < MIN_WORDS: order.pop(0)
            if order: drops[s] = set(order)
            else: del drops[s]
    # pointer lines
    def name(s):
        d = pages[s]; h = next((b['text'] for b in d['blocks'] if b['t'] == 'h' and b.get('level') == 1), None) or (local.get(s, {}).get('new_page') or {}).get('h1') or s
        return re.sub(r'\s*\|.*$', '', h)
    after = {s: set(v) for s, v in drops.items()}
    new, nw, _ = scores(pages, local, after)
    print('clusters across pages:', ncl, '| pages losing blocks:', len(drops), '| blocks dropped:', sum(len(v) for v in drops.values()))
    print('under 0.7 now:', sum(1 for v in base.values() if v < 0.7), '-> after drops:', sum(1 for v in new.values() if v < 0.7), '| min words among changed pages:', min([nw[s] for s in drops] or [0]))
    if dry: return
    for s, l in local.items():
        dr = drops.get(s, set()); changed = False
        if dr:
            l['blocks'] = [b for i, b in enumerate(l.get('blocks', [])) if ('B', i) not in dr]; l['faq'] = [f for i, f in enumerate(l.get('faq', [])) if ('F', i) not in dr]; changed = True
            l['blocks'] += [{'t': 'p', 'text': 'Notes that also apply here are written up once, on these pages:', 'gen': GEN, 'pos': 'end'},
                            {'t': 'list', 'items': [[{'t': name(o), 'h': f'/{o}.html'}] for o in sorted(owners[s])], 'gen': GEN, 'pos': 'end'}]
        if changed: json.dump(l, open(os.path.join(LOCAL, s + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
if __name__ == '__main__': main()
