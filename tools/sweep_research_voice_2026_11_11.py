#!/usr/bin/env python3
"""Research-note wording left on public pages (D-213, Nov 11, 2026).

The condo, townhome and area notes still carried the researchers' working voice in places: "Queued, counted nowhere", "Held here as a
named candidate", "verify fresh", "Board geography:", "(expressly not X's own figures)", "per the directory's market report",
"per listing text". This rewrites those phrases in plain words without changing any fact. Idempotent; prints what it changed.
python3 -I tools/sweep_research_voice_2026_11_11.py"""
import glob, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)

EXACT = [   # one-off sentences first
    (' Held here as a named candidate, not counted, and no fact from any other Murrayville building may be carried to it.', ''),
    ('Held here as a named candidate, not counted, and no fact from any other Murrayville building may be carried to it.', ''),
    ('Queued, counted nowhere — ', ''),
    ('. Queued, counted nowhere', '.'),
    ('Queued, counted nowhere', ''),
    ('Name and townhouse form verify fresh: listings name', 'Listings name'),
    ('Form per listing text: duplex-style townhouses in a gated community, with clubhouse amenities per the directory (listing/directory copy, attributed as such).',
     'Listings describe duplex-style townhouses in a gated community, and the strata directory lists clubhouse amenities.'),
    ('"45+" per listing text is', '"45+" in the listings is'),
    ('amenities per listing text include', 'amenities in the listings include'),
    ('per the directory bylaw record and per listings', 'according to the strata directory and the listings'),
    ('carried as built 2014 per the directory', 'shown as built 2014 in the strata directory'),
    ('Board geography differs from City geography:', 'MLS® areas don’t match City boundaries:'),
    ('Board geography, with its caveat:', 'On MLS®, with one caveat:'),
]
RX = [
    (re.compile(r"per the directory's [A-Za-z\- ]*?(?:list|report|table|description of the complex set|description|headline|entry)\b"), 'according to the strata directory'),
    (re.compile(r'per the directory entry'), 'in the strata directory'),
    (re.compile(r'\bper the directory\b'), 'according to the strata directory'),
    (re.compile(r',? per listing text\b'), ', according to the listings'),
    (re.compile(r'Board geography:'), 'On MLS®:'),
    (re.compile(r'Community context only \(expressly not'), 'For context only (not'),
    (re.compile(r'Community context \(expressly not'), 'For context (not'),
    (re.compile(r'\bexpressly not\b'), 'not'),
]


def fix(s):
    o = s
    for a, b in EXACT: s = s.replace(a, b)
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


def main():
    files = changed = 0
    for f in sorted(glob.glob('src/data/local/*.json')):
        raw = open(f, encoding='utf-8').read(); hits = []
        d = walk(json.loads(raw), hits)
        if not hits: continue
        ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
        s = json.dumps(d, ensure_ascii=False, indent=ind) if ind else json.dumps(d, ensure_ascii=False, separators=(',', ':'))
        open(f, 'w', encoding='utf-8').write(s + ('\n' if raw.endswith('\n') else ''))
        files += 1; changed += len(hits)
    print('files', files, '| strings changed', changed)


if __name__ == '__main__': main()
