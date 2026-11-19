"""D-378: writer instructions that leaked into live copy ("never cite 18020 as current", "(cite the number)", "cite it as adopted"),
rewritten as plain statements of the same fact. No fact changes. Found by a site-wide scan of built pages, Nov 19 2026.
Run once from the repo root: python3 tools/fix_writer_notes_2026_11_19.py
"""
import glob, json, re

_FMT = {}
def load(p):
    raw = open(p).read(); d = json.loads(raw)
    for st in (dict(indent=None, separators=(',', ':')), dict(indent=None), dict(indent=1), dict(indent=2), dict(indent=0)):
        for ea in (False, True):
            for tail in ('', '\n'):
                if json.dumps(d, ensure_ascii=ea, **st) + tail == raw: _FMT[p] = (st, ea, tail); return d
    raise SystemExit(f'format not matched: {p}')
def save(p, d):
    st, ea, tail = _FMT[p]; open(p, 'w').write(json.dumps(d, ensure_ascii=ea, **st) + tail)

FIX = [
    (' — never cite the replaced Bylaw No. 18020 as current.', '; it replaced Bylaw No. 18020.'),
    (' — never cite 18020 as current.', '; it replaced Bylaw 18020.'),
    (' — Bylaw 18020 is replaced and is never cited as current.', '; it replaced Bylaw 18020.'),
    (' — Bylaw 18020 is replaced and never cited as current.', '; it replaced Bylaw 18020.'),
    (', which is never cited as current for Burnaby.', '.'),
    (' The former 1965 No. 4742 is superseded and is never cited as current.', ' It replaced the 1965 bylaw, No. 4742.'),
    (', repealing Bylaw No. 2955 — 2955 is never cited as current.', ', repealing Bylaw No. 2955.'),
    ('repeals Bylaw No. 2955 — never cite 2955 as current)', 'repeals Bylaw No. 2955)'),
    ('repeals Bylaw No. 2955 — 2955 is never cited as current)', 'repeals Bylaw No. 2955)'),
    (' do not apply east of Lynn Creek and are never cited for this area.', ' do not apply east of Lynn Creek.'),
    ('The Lougheed corridor reading changed in January 2026 — cite it as adopted. Any older note calling the corridor plan merely proposed is superseded.',
     'The Lougheed Transit Corridor Area Plan was adopted in January 2026, so it is no longer only a proposal.'),
    ('Lougheed Transit Corridor — adopted position, with the correction stated: cite the corridor as adopted January 27, 2026 per the City record — ',
     'Lougheed Transit Corridor: adopted by the City on January 27, 2026. '),
    ('No. 3300: (cite the number), which repeals', 'No. 3300, which repeals'),
    ('Zoning Bylaw 2025 No. 3300 — cite the number.', 'Zoning Bylaw 2025 No. 3300.'),
    (" Don't use North or Northeast figures for Northwest.", ' Figures for North or Northeast Maple Ridge do not describe Northwest.'),
]
COLON = re.compile(r'(\b(?:No\. \d{3,5}|\d{3,5}, \d{4})): \((adopted|consolidated) ')

def fix(v, hits):
    if isinstance(v, dict): return {k: fix(x, hits) for k, x in v.items()}
    if isinstance(v, list): return [fix(x, hits) for x in v]
    if isinstance(v, str):
        o = v
        for a, b in FIX: v = v.replace(a, b)
        v = COLON.sub(r'\1 (\2 ', v)
        if v != o: hits.append(1)
    return v

total = 0
for p in glob.glob('src/data/**/*.json', recursive=True):
    raw = open(p).read()
    if not any(a in raw or a.replace('—', '\\u2014').replace("'", "'") in raw for a, _ in FIX) and not re.search(r'\d{3,5}: \((?:adopted|consolidated)', raw): continue
    d = load(p); hits = []; n = fix(d, hits)
    if hits: save(p, n); total += len(hits); print(len(hits), p)
print('strings fixed:', total)
