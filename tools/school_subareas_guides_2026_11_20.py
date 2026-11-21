#!/usr/bin/env python3
"""The 8 Paragon-confirmed schools whose page already had its own guide schools section (D-392) go into that section (D-393).
Jared, Nov 20 2026: "yes add the schools". One "Also in <area>" line per page, placed before the catchment note (or at the end of
the section). Grades are not given because the source sheet has none. Idempotent.   python3 -I tools/school_subareas_guides_2026_11_20.py"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_schools as B
P = json.load(open('src/data/schools/placements-2026-11-01.json'))
todo = {}
for p in P['tier1']:
    if 'not added: the page already has its own schools section' in p.get('reason', ''):
        todo.setdefault(p['published_on'], []).append(p)
MARK = '(MLS® sub-area confirmed in Paragon by address, November 2026)'
txt = lambda b: b.get('text') if isinstance(b.get('text'), str) else ''.join(x.get('t', '') for x in b.get('parts', []))
for slug, items in sorted(todo.items()):
    f = f'src/data/pages/{slug}.json'; raw = open(f).read(); d = json.loads(raw); bl = d['blocks']
    if MARK in raw: continue
    i = next(i for i, b in enumerate(bl) if b.get('t') == 'h' and b.get('level') == 2 and re.match(r'Schools (in|for) ', b.get('text') or ''))
    area = re.sub(r'^Schools (in|for) ', '', bl[i]['text'])
    j = next((k for k in range(i + 1, len(bl)) if bl[k].get('t') == 'h' and bl[k].get('level') == 2), len(bl))
    while j - 1 > i and bl[j - 1].get('t') == 'p' and len(txt(bl[j - 1])) < 40: j -= 1          # stay above the next section's label ("Parks and recreation")
    c = next((k for k in range(i + 1, j) if txt(bl[k]).startswith('Catchments are set')), j)
    lab = [f'{B.clean(p["name"])} ({B.addr(p["street_address"])})' if B.addr(p['street_address']) else B.clean(p['name']) for p in items]
    line = f'Also in {area} {MARK}: {B.oxford(lab)}.'
    bl.insert(c, {'t': 'p', 'parts': [{'t': line}]})
    ind = 2 if raw.startswith('{\n  ') else (1 if raw.startswith('{\n ') else None)
    sep = (',', ':') if ind is None and '":"' in raw[:300] else None
    open(f, 'w').write(json.dumps(d, ensure_ascii=False, indent=ind, separators=sep) + ('\n' if raw.endswith('\n') else ''))
    for p in items: p['reason'] = p['reason'].split('; not added')[0] + '; added to the page\'s own schools section (D-393)'
    print(slug, '|', line)
json.dump(P, open('src/data/schools/placements-2026-11-01.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open('src/data/schools/placements-2026-11-01.json', 'a').write('\n')
