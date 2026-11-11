#!/usr/bin/env python3
"""City rules said once (D-213, Nov 11, 2026), finishing D-202.

D-202 moved the city-wide rules paragraphs of the 20 longest guides to one page per city (/<city>-home-buying-rules.html). The
same paragraphs were still on other guides and area pages, so five rules pages failed the launch pack's 70% unique-wording check
(Maple Ridge 50%, Chilliwack 60%, Abbotsford and Cultus Lake 68%, Surrey 70%).

What this does:
  - For every other local page, a paragraph or list item is removed when at least 70% of its 8-word runs are on a city rules page
    (and it has at least 12 of them). That is the city-wide rule, word for word; anything written about the neighbourhood itself has
    its own words and stays. A heading left with nothing under it goes too.
  - A page that lost a rule and does not already link to that city's rules page gets one line there, where the first removed rule was.
  - Each rules page's opening paragraph, which was the same template on all eight, is rewritten from its own topics and its own
    authority, so it is not shared either.
Idempotent. python3 -I tools/dedupe_city_rules_2026_11_11.py"""
import glob, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)

CITIES = {'abbotsford': ('Abbotsford', 'the City of Abbotsford'), 'chilliwack': ('Chilliwack', 'the City of Chilliwack'),
          'cultus-lake': ('Cultus Lake', 'the Cultus Lake Park Board or the Fraser Valley Regional District, depending on the lot'),
          'delta': ('Delta', 'the City of Delta'), 'langley': ('the Township of Langley', 'the Township of Langley'),
          'maple-ridge': ('Maple Ridge', 'the City of Maple Ridge'), 'pitt-meadows': ('Pitt Meadows', 'the City of Pitt Meadows'),
          'surrey': ('Surrey', 'the City of Surrey')}


def words(s): return re.findall(r"[A-Za-z0-9$%'’.\-]+", s.lower())
def sh(s): w = words(s); return {' '.join(w[i:i + 8]) for i in range(max(0, len(w) - 7))}
def txt(b): return b.get('text') or ''.join(x.get('t', '') for x in b.get('parts', []))
def itxt(it): return ''.join(x.get('t', '') for x in it)


def load(f): raw = open(f, encoding='utf-8').read(); return raw, json.loads(raw)
def save(f, raw, d):
    ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
    open(f, 'w', encoding='utf-8').write((json.dumps(d, ensure_ascii=False, indent=ind) if ind else json.dumps(d, ensure_ascii=False, separators=(',', ':'))) + ('\n' if raw.endswith('\n') else ''))


def intro(slug, d):
    name, auth = CITIES[slug]
    topics = [re.sub(r' in (the )?(Township of )?' + re.escape(name.replace('the ', '')) + r'$', '', b['text']).lower()
              for b in d['blocks'] if b.get('t') == 'h' and b.get('level') == 2 and not re.match(r'(Sources|Neighbourhood guides|Other things)', b['text'])]
    topics = [t.replace('gst', 'GST') for t in topics]
    lst = ', '.join(topics[:-1]) + ' and ' + topics[-1] if len(topics) > 1 else topics[0]
    return (f'Buying anywhere in {name}? These are the rules that apply city-wide, by topic: {lst}. The neighbourhood guides cover what is '
            f'specific to each area. Rules change, so check anything that matters for your purchase with {auth} and your lawyer before you remove subjects.')


def main():
    rules = {c: f'src/data/local/{c}-home-buying-rules.json' for c in CITIES}
    rsh, titles = {}, {}
    for c, f in rules.items():
        raw, d = load(f)
        ip = next(i for i, b in enumerate(d['blocks']) if b.get('t') == 'p')
        if d['blocks'][ip].get('text', '').startswith(('The rules below apply across', 'Buying anywhere in')):
            new = intro(c, d)
            if d['blocks'][ip]['text'] != new: d['blocks'][ip]['text'] = new; save(f, raw, d)
        rsh[c] = set().union(*(sh(txt(b)) for b in d['blocks'] if b.get('t') == 'p'),
                             *(sh(itxt(it)) for b in d['blocks'] if b.get('t') == 'list' for it in b['items']))
    removed = pages = 0
    for f in sorted(glob.glob('src/data/local/*.json')):
        if f in rules.values() or not f.endswith('.json'): continue
        raw, d = load(f); bl = d.get('blocks')
        if not isinstance(bl, list): continue
        def city_of(s):
            ss = sh(s)
            if len(ss) < 12: return None
            for c, R in rsh.items():
                if len(ss & R) / len(ss) >= 0.7: return c
        def empty_heads(blocks):
            return {id(b) for i, b in enumerate(blocks) if b.get('t') == 'h' and (i + 1 == len(blocks) or (blocks[i + 1].get('t') == 'h' and blocks[i + 1].get('level', 2) <= b.get('level', 2)))}
        was_empty = empty_heads(bl)
        out, hit, first, fpos = [], set(), {}, {}
        for b in bl:
            if b.get('t') == 'p':
                c = city_of(txt(b))
                if c: hit.add(c); first.setdefault(c, len(out)); fpos.setdefault(c, b.get('pos')); removed += 1; continue
            elif b.get('t') == 'list':
                keep = []
                for it in b['items']:
                    c = city_of(itxt(it))
                    if c: hit.add(c); first.setdefault(c, len(out)); fpos.setdefault(c, b.get('pos')); removed += 1
                    else: keep.append(it)
                if not keep: continue
                if len(keep) != len(b['items']): b = {**b, 'items': keep}
            out.append(b)
        if not hit: continue
        # headings left with nothing under them before the next heading of the same or a higher level
        now_empty = empty_heads(out)
        clean = [b for b in out if not (id(b) in now_empty and id(b) not in was_empty)]
        text = json.dumps(clean, ensure_ascii=False)
        for c in sorted(hit, key=lambda c: -first[c]):
            if f'/{c}-home-buying-rules.html' in text: continue
            at = min(first[c], len(clean))
            clean.insert(at, {'t': 'p', 'parts': [{'t': f'The rules that apply across {CITIES[c][0]} (zoning, suites, strata, land and taxes) are on one page: '},
                                                  {'t': f'buying a home in {CITIES[c][0]}: the rules', 'h': f'/{c}-home-buying-rules.html'}, {'t': '.'}],
                              'gen': 'rulesonce', **({'pos': fpos[c]} if fpos.get(c) else {})})
        d['blocks'] = clean; save(f, raw, d); pages += 1
    print('rules removed from other pages:', removed, '| pages changed:', pages)


if __name__ == '__main__': main()
