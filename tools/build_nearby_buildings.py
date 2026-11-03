"""Building-by-building 'What's nearby' sections (gen nbb) from Jared's phase-2 nearby notes (docs/research/local-notes-nearby-buildings/buildings/*.md, researched 2026-11-02).

One note per named building in the 55+, condo and townhome notes (995 in the roster). A note is published only when the building has a settled street address (24 are unresolved: the address is not in the notes
or two addresses conflict, so no time can be measured and the area-level facts would only repeat the area block). Each published building gets, under its area page (or its 55+ page for a 55+ building),
a short list of its nearest transit, parks, schools and shopping, and its measured walking and driving times (OpenStreetMap routing, measured 2026-11-02, start at the building's address) in one table per page.
Times: 1-90 minutes, walks up to 1.5 km, drives up to 10 km, believable speed. Not published: catchments, bus frequencies the note does not state, ratings, anything the note marks as a guess.
python3 -I tools/build_nearby_buildings.py      (after build_nearby.py)"""
import collections, glob, importlib.util, json, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); HERE = os.path.dirname(os.path.abspath(__file__))
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
NB = _load('nbmod', 'build_nearby.py'); T = NB.T; N = NB.N; LOCAL = N.LOCAL
NOTES = os.path.join(ROOT, 'docs/research/local-notes-nearby-buildings'); G = 'nbb'; SFX = '-nearby-2026-11-02.md'
HEAD = [(1, 'Transit', 3), (2, 'Parks and recreation', 2), (3, 'Schools', 3), (4, 'Shopping', 2)]


def parse(path):
    t = open(path, encoding='utf-8').read(); lines = t.split('\n')
    parts = [p.strip() for p in re.sub(r"\s*—\s*What's Nearby.*$", '', lines[0][2:]).split(' — ')]
    hdr = re.search(r'^Building: (.*)$', t, re.M); hdr = hdr.group(1) if hdr else ''
    m = re.search(r'\(([\w-]+); ([^)]*)\)', hdr)
    if not m or re.search(r'ADDRESS NOT IN NOTES|ADDRESS CONFLICT|NOT CONFIRMED', hdr): return None
    if len(parts) < 2 or not re.match(r'\d', parts[1]): return None
    sec = NB.sections(t); frm, rows = NB.times(sec.get(5, []))
    rows = [r for r in rows if NB.plausible(r[1], r[2], r[3])]
    seg = bool(re.search(r'segment|street point|not a building point|nearest point on', ' '.join(sec.get(5, [])[:1] + [x for x in sec.get(9, []) if re.search(r'origin|building-point|building point', x, re.I)]), re.I))
    return dict(name=re.sub(r'\s*\(.*?\)', '', parts[0]).strip() or parts[0], addr=parts[1], home=m.group(1), progs=m.group(2), sec=sec, rows=rows, seg=seg, size=len(t), file=os.path.basename(path))


def facts(n):
    out = []; urls = []
    for k, label, cap in HEAD:
        items = []
        for b in n['sec'].get(k, []):
            if re.match(r'Area-level', b): continue
            urls += N.urls(b); t = NB.tidy(b)
            if len(t) >= 25 and not re.match(r'(None|No data)', t): items.append(t)
        if items: out.append((label, items[:cap]))
    return out, urls


def H(t, l=3): return {**N.H(t, l), 'gen': G, 'pos': 'end'}
def P(t): return {**N.P(t), 'gen': G, 'pos': 'end'}
def LI(items): return {**N.LI(items), 'gen': G, 'pos': 'end'}
def LK(items): return {**N.LK(items), 'gen': G, 'pos': 'end'}


def page_block(ns):
    bl = [H("What's nearby, building by building", 2),
          P("For each building named below, the nearest transit, parks, schools and shopping come from TransLink or BC Transit, the municipality, the Ministry of Education and Child Care and the retailers’ own pages, listed under Sources. "
            "Walking and driving times were measured on November 2, 2026 on OpenStreetMap routing, starting at the building’s street address (or the nearest point on its street where the map has no point for the building itself, marked in the table). Facts that neighbouring buildings share are listed once, under the first of them. School catchments are not confirmed for these addresses: confirm with the school district before relying on one.")]
    urls = []; rows = []; seen = set()
    for n in sorted(ns, key=lambda n: n['name'].lower()):
        fs, u = facts(n); urls += u
        fs = [(lab, [x for x in its if x not in seen]) for lab, its in fs]; fs = [(lab, its) for lab, its in fs if its]
        for lab, its in fs: seen.update(its)
        if not fs and not n['rows']: continue
        title = n['name'] if n['name'].lower() == n['addr'].lower() else f"{n['name']}, {n['addr']}"
        if fs: bl.append(H(title))
        if fs: bl.append(LI([f'{lab}: ' + ' '.join(x if x.endswith(('.', '!', '?')) else x + '.' for x in its) for lab, its in fs]))
        rs = sorted({(a, m, round(mi), round(km, 1)) for a, m, mi, km in n['rows']}, key=lambda r: (r[1] != 'Walk', r[2]))[:3]
        lab = n['name'] + (' (from the street)' if n['seg'] else '')
        rows += [[lab, a, m, str(mi), f'{km:.1f}'] for a, m, mi, km in rs]
    if not any(b['t'] == 'list' for b in bl): return []
    bl = [b for b in bl if not (b['t'] == 'list' and not b['items'])]
    if rows:
        bl.append(H('Measured walking and driving times from each building'))
        bl.append({'t': 'table', 'caption': 'Measured on November 2, 2026 with OpenStreetMap routing (OSRM for driving, routed-foot for walking), starting at each building’s address', 'head': ['Building', 'To', 'How', 'Minutes', 'Distance (km)'], 'rows': rows, 'gen': G, 'pos': 'end'})
    sl = N.src_links([x for x in urls if 'jaredgibbons.ca' not in x])
    if sl: bl += [H('Sources for what’s nearby each building'), LK(sl[:16])]
    return bl


def home_page(n):
    h = n['home']; progs = n['progs']
    if '55-plus' in progs:
        for c in (h, re.sub(r'-guide$', '', h)):
            if T.exists(f'{c}-55-plus-homes-for-sale'): return f'{c}-55-plus-homes-for-sale'
    return NB.target(h)


def main():
    pages = collections.defaultdict(list); unres = []; notarget = []
    for f in sorted(glob.glob(f'{NOTES}/*{SFX}')):
        n = parse(f)
        if not n: unres.append(os.path.basename(f)); continue
        tg = home_page(n)
        if not tg: notarget.append(n['home']); continue
        pages[tg].append(n)
    for p in glob.glob(f'{LOCAL}/*.json'):
        j = json.load(open(p, encoding='utf-8'))
        if any(b.get('gen') == G for b in j.get('blocks', [])):
            j['blocks'] = [b for b in j['blocks'] if b.get('gen') != G]; T.save(os.path.basename(p)[:-5], j)
    wrote = nb = 0
    for tg, ns in sorted(pages.items()):
        bl = page_block(ns)
        if not bl: continue
        j = T.load(tg); j['blocks'] = j.get('blocks', []) + bl; j.setdefault('slug', tg); T.save(tg, j); wrote += 1; nb += sum(1 for b in bl if b['t'] == 'h' and b['level'] == 3 and 'Sources' not in b['text'] and 'Measured' not in b['text'])
    print('building nearby sections on', wrote, 'pages;', nb, 'buildings; unresolved/skipped', len(unres), '; no page for', len(notarget), sorted(set(notarget)))


if __name__ == '__main__':
    main()
