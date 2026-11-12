#!/usr/bin/env python3
"""Research-note wording, fifth pass (D-230, Nov 11, 2026), from the whole-site polish.

Drops the researchers' bookkeeping lines ("Cross-reference only", "the sub-area rows sum exactly to the community totals in
both splits", "Queue") and plain-words the source-grading asides ("(directory/listing-level data)", "A listing aggregator
records") without changing any fact. Idempotent; prints every change.
python3 -I tools/sweep_research_voice_pass5_2026_11_11.py"""
import glob, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)

DROP = [re.compile(p) for p in (   # whole strings that are bookkeeping
    r'^Cross-reference only\b.*$',
    r'^Cross-reference, no count taken here:.*$',
    r'^(?:The )?(?:\w+ )?sub-area rows sum (?:exactly )?to (?:those |the )?community totals in both splits\.$',
    r'^The named buildings sit in those two sub-areas.*$',
    r'^Fee-simple lots are the default form$',
    r'^Named buildings/complexes$',
    r'^ALR vs non-ALR split$',
    r'^Assemblies / proposals$',
)]
RX = [
    (r' ?(?:The )?(?:\w+ )?(?:board )?sub-area rows (?:still )?sum (?:exactly )?to the (?:\w+ )?community totals(?: in both splits)?(?: \([^)]*\))?\.', ''),
    (r' ?(?:—|-) ?and the (?:\w+ )?sub-area rows sum to the community totals in both splits\.', '.'),
    (r' The rows sum exactly to the community totals \(([^)]*)\)', r' (community total \1)'),
    (r'^The city as the page bounds it, in its own words: ', 'Boundaries: '),
    (r' \((?:directory/)?listing-level data(?: only)?\)', ''),
    (r' \(listing-level data — confirm on the Form B\)', ' (confirm on the Form B)'),
    (r',? ?(?:—|-) listing-level data(?: only)?(?:, confirm on the Form B)?\.', '.'),
    (r'; the pet and age positions are listing-level data, confirm on the Form B', '; confirm pet and age rules on the Form B'),
    (r'\bA listing aggregator records\b', 'Listings record'),
    (r'\(current listing aggregator\)', '(current listings)'),
    (r' \((?:building directory|presale source|directory), secondary source\)', ''),
    (r' \(secondary source\)', ''),
    (r', secondary\)', ')'),
    (r' \(see Tenure traps\)', ''),
    (r' \(see Checked and not 55\+ below\)', ''),
    (r'^Fee-simple lots — the default form: ', 'Fee-simple lots: '),
    (r'^Fee-simple lots — the default form$', 'Fee-simple lots'),
    (r' — the default form for land generally —', ','),
    (r'^SnapStats publishes medians at community level only\.\s*', ''),
    (r'(?<=\.) SnapStats publishes medians at community level only\.', ''),
]
RX = [(re.compile(a), b) for a, b in RX]


def fix(s):
    if any(r.match(s) for r in DROP): return ''
    o = s
    for r, b in RX: s = r.sub(b, s)
    return o if s == o else re.sub(r' {2,}', ' ', s).strip()


def walk(x, hits):
    if isinstance(x, dict): return {k: walk(v, hits) for k, v in x.items()}
    if isinstance(x, list): return [walk(v, hits) for v in x]
    if isinstance(x, str):
        y = fix(x)
        if y != x: hits.append((x, y))
        return y
    return x


def prune(o):
    if isinstance(o, dict):
        o = {k: prune(v) for k, v in o.items()}
        if isinstance(o.get('parts'), list): o['parts'] = [p for p in o['parts'] if not (isinstance(p, dict) and set(p) <= {'t'} and not str(p.get('t', '')).strip())]
        if isinstance(o.get('items'), list): o['items'] = [it for it in o['items'] if not (isinstance(it, list) and not ''.join(str(x.get('t', '')) for x in it if isinstance(x, dict)).strip())]
        return o
    if isinstance(o, list):
        out = [prune(v) for v in o]
        return [b for b in out if not (isinstance(b, dict) and b.get('t') in ('p', 'h', 'list') and not (b.get('text') or '').strip() and not b.get('parts') and not b.get('items'))]
    return o


def main():
    files = changed = 0
    for f in sorted(glob.glob('src/data/local/*.json')):
        raw = open(f, encoding='utf-8').read(); hits = []
        d = prune(walk(json.loads(raw), hits))
        if not hits: continue
        for a, b in hits: print(f'{os.path.basename(f)}\n  - {a[:260]}\n  + {b[:260]}')
        ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
        s = json.dumps(d, ensure_ascii=False, indent=ind) if ind else json.dumps(d, ensure_ascii=False, separators=(',', ':'))
        open(f, 'w', encoding='utf-8').write(s + ('\n' if raw.endswith('\n') else ''))
        files += 1; changed += len(hits)
    print('files', files, '| strings changed', changed)


if __name__ == '__main__': main()
