"""Lifts the three archive guides that fell under 70% unique wording after the research-note cleanup (popkum-guide, bridal-falls-guide,
langley-city-guide) by dropping sentences that the same site already says word-for-word on a sibling page. Nothing site-wide is lost.
Idempotent.  python3 -I tools/dedupe_guides_2026_11_08.py"""
import json, re, glob, os, subprocess, csv, collections, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
TARGET = {'popkum-guide': 'bridal-falls-guide', 'bridal-falls-guide': None, 'langley-city-guide': 'langleycity', 'east-delta-guide': None, 'chilliwack-proper-east-guide': None, 'abbotsford-east': None, 'abbotsford-west': None, 'cloverdale-bc': None, 'cloverdale-bc-55-plus-homes-for-sale': None}
GOAL = 0.705
def sents(s): return [x for x in re.split(r'(?<=[.!?])\s+', s) if len(x.split()) >= 9]
def strings(d):
    for b in d.get('blocks', []):
        if b.get('t') == 'p' and isinstance(b.get('text'), str): yield b, 'text', b['text']
        if b.get('t') == 'list':
            for it in b.get('items', []):
                for p in it:
                    if isinstance(p, dict) and isinstance(p.get('t'), str) and not p.get('h'): yield p, 't', p['t']
def score(slug):
    out = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'tools/uniqueness.py'), '--slugs', slug], capture_output=True, text=True, cwd=ROOT).stdout
    m = re.search(r'^' + re.escape(slug) + r' \S+ (\d+) ([\d.]+)', out, re.M); return float(m.group(2)) if m else 0
local = {os.path.basename(f)[:-5]: json.load(open(f, encoding='utf-8')) for f in glob.glob(os.path.join(ROOT, 'src/data/local/*.json'))}
count = collections.Counter()
for sl, d in local.items():
    for _, _, s in strings(d):
        for x in set(sents(s)): count[x] += 1
for slug in TARGET:
    if score(slug) >= GOAL: print(slug, 'ok'); continue
    f = os.path.join(ROOT, f'src/data/local/{slug}.json'); raw = open(f, encoding='utf-8').read(); d = json.loads(raw)
    cand = [(o, k, x) for o, k, s in strings(d) for x in sents(s) if 2 <= count[x] <= 12]
    done = 0
    for o, k, x in cand:
        if x in o[k]:
            o[k] = o[k].replace(x, '', 1); o[k] = re.sub(r'\s{2,}', ' ', o[k]) if not o[k].startswith(' ') else o[k]; done += 1
        if done % 4 == 0:
            pass
    kws = [dict(indent=2, ensure_ascii=False), dict(indent=1, ensure_ascii=False), dict(separators=(',', ':'), ensure_ascii=False)]
    base = json.loads(raw); out = None
    for kw in kws:
        for tail in ('\n', ''):
            if json.dumps(base, **kw) + tail == raw: out = json.dumps(d, **kw) + tail
    # drop emptied pieces/blocks
    open(f, 'w', encoding='utf-8').write(out if out else json.dumps(d, indent=2, ensure_ascii=False) + '\n')
    print(slug, 'removed', done, 'shared sentences; unique now', score(slug))
