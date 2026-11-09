"""One-off (2026-11-09): move generated home-price blocks from September to October 2026 without regenerating whole pages.

The gap-page, new-search, extras and area-gap generators (tools/build_gap_pages.py, build_new_searches.py, build_extras_pages.py, build_area_gap_pages.py) quote the board
benchmark month inside their own text. Re-running them over the live tree would undo later hand fixes, so they are run in a scratch copy (month strings switched to October,
reading src/data/market/2026-10.json) and only the blocks and FAQ answers that still say "September 2026" are spliced into the live files.
A block is matched by type, gen tag and its text with digits and month names masked; anything without exactly one match is listed and left alone.

    python3 -I tools/refresh_hpi_blocks.py --scratch /tmp/scratch [--apply]
Without --apply it only reports. File formats are kept (indent, trailing newline) per file.
"""
import argparse, glob, json, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
GENS = {'gappage', 'nsrch', 'xtra', 'areagap'}  # generators that quote the board benchmark month
MASK = re.compile(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)|\d[\d,.]*%?')


def key(b):
    t = b.get('text') or b.get('caption') or ''
    if not t and b.get('parts'): t = ''.join(p.get('t', '') for p in b['parts'])
    return (b.get('t'), b.get('gen'), MASK.sub('#', t)[:48])


def fmt(raw):
    ind = None
    m = re.search(r'\n( +)"', raw)
    if raw.startswith('{\n') and m: ind = len(m.group(1))
    return ind


def full(b): return re.sub(r'[+−-](?=#)', '', MASK.sub('#', json.dumps(b, ensure_ascii=False, sort_keys=True)))  # signs too: a change can flip from + to -


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--scratch', required=True); ap.add_argument('--apply', action='store_true')
    ap.add_argument('--numbers', action='store_true', help='second pass: generated blocks that differ from the scratch copy only in digits and month names (the "against other home types" and "by community" paragraphs name no month, so the first pass cannot see them)')
    a = ap.parse_args()
    swapped = pages = 0; unmatched = []; wording = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'src/data/local/*.json'))):
        raw = open(f, encoding='utf-8').read()
        if not a.numbers and 'September 2026' not in raw: continue
        n = os.path.basename(f); g = os.path.join(a.scratch, 'src/data/local', n)
        if not os.path.exists(g): continue
        live = json.loads(raw); scr = json.loads(open(g, encoding='utf-8').read())
        if not any(b.get('gen') in GENS for b in live.get('blocks', [])): continue
        changed = False
        for kind, kf in (('blocks', key), ('faq', lambda q: MASK.sub('#', q.get('q', ''))[:70])):
            pool = {}
            for j, b in enumerate(scr.get(kind, [])): pool.setdefault(kf(b), []).append((j, b))
            for i, b in enumerate(live.get(kind, [])):
                if kind == 'blocks' and b.get('gen') not in GENS: continue
                if a.numbers:
                    if kind == 'faq' and b.get('gen') not in GENS: continue
                else:
                    if 'September 2026' not in json.dumps(b, ensure_ascii=False): continue
                    if kind == 'faq' and not re.search(r'benchmark|Home Price Index', json.dumps(b, ensure_ascii=False)): continue
                cands = [(j, c) for j, c in pool.get(kf(b), []) if c != b and (a.numbers and full(c) == full(b) or not a.numbers and 'September 2026' not in json.dumps(c, ensure_ascii=False))]
                if cands:
                    same = [x for x in cands if x[0] == i]; j, c = (same or cands)[0]
                    live[kind][i] = c; pool[kf(b)] = [x for x in pool[kf(b)] if x[0] != j]; changed = True; swapped += 1
                elif a.numbers:
                    d = [c for _, c in pool.get(kf(b), []) if c != b]
                    if d: wording.append((n, kind, i, str(kf(b))[:70]))
                else: unmatched.append((n, kind, str(kf(b))[:100]))
        if changed:
            pages += 1
            if a.apply:
                ind = fmt(raw)
                out = json.dumps(live, ensure_ascii=False, indent=ind) if ind is not None else json.dumps(live, ensure_ascii=False, separators=(',', ':'))
                open(f, 'w', encoding='utf-8').write(out + ('\n' if raw.endswith('\n') else ''))
    print(f'{swapped} blocks or FAQ answers on {pages} pages {"updated" if a.apply else "would change"}; {len(unmatched)} left (no single match)')
    for u in unmatched[:40]: print('  left:', u)
    if a.numbers:
        print(f'{len(wording)} generated blocks differ from the scratch copy in more than numbers (hand-edited or reworded; left alone)')
        for w in wording[:40]: print('  wording:', w)


if __name__ == '__main__':
    main()
