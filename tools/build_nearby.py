"""'What's nearby' blocks from Jared's verified nearby notes (docs/research/local-notes-nearby/*-nearby-2026-11-02.md; researched 2026-11-02).

Each note has transit, parks and recreation, schools, grocery and shopping anchors, and measured walking and driving times (OpenStreetMap routing: OSRM for driving,
routed-foot for walking, measured 2026-11-02), plus a list of what could not be confirmed. A note becomes a "What's nearby" block (gen nb) on the area page, sub-area page or guide of the same name.
Where two notes land on one page (an area and its guide), the longer one is used. Facts are written as short statements; source URLs are collected once under the block.
Times are published only with the point they were measured from, between 1 and 90 minutes, walks up to 1.5 km, drives up to 10 km, at a believable speed.
Not published: anything the note itself marks as a guess, board data, ratings.   python3 -I tools/build_nearby.py      (after build_mobilehomes.py)"""
import collections, glob, importlib.util, json, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); HERE = os.path.dirname(os.path.abspath(__file__))
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
T = _load('tn', 'build_typenotes.py'); N = T.N; LOCAL = N.LOCAL
NOTES = os.path.join(ROOT, 'docs/research/local-notes-nearby'); G = 'nb'; SFX = '-nearby-2026-11-02.md'
HEAD = {1: 'Transit', 2: 'Parks and recreation', 3: 'Schools', 4: 'Groceries and shopping'}
DROP = re.compile(r'fetched text|\bas read\b|(?:list|listing|map|pages|page) read\b|\bread (?:names|shows)|timetables?(?: extract)? read|\bpages? read|\bsources? read|\bnot read\b|locator run|could not be read|\bread gave|\bread lists?|\bwas taken|were taken|this pass|rate limit|fetch hit|fetch failed|search results?\b|search hit|could not be fetched|page read|were read|was read|in this note|this note|\bsection \d|omitted|allowed source|in this pass|this batch|research file|\bslug\b|scratch|Nominatim|geocode|OSM data date|not published by the service|\bworker\b', re.I)


def sections(t):
    sec = {}; cur = None
    for ln in t.split('\n'):
        m = re.match(r'^## (\d)\.|^## (NOT CONFIRMED)', ln)
        if m: cur = int(m.group(1)) if m.group(1) else 9; sec[cur] = []; continue
        if cur and ln.startswith('- '): sec[cur].append(ln[2:].strip())
    return sec


def times(lines):
    frm = None; rows = []
    for ln in lines:
        m = re.search(r'[Ff]rom-?point[^:]*:\s*(.+?)(?: \(|\. |; |\.$|$)', ln) or re.search(r'\bFrom:\s*(.+?)(?: \(|\. |; |\.$|$)', ln) or re.search(r'[Mm]easured \d{4}-\d\d-\d\d from ([^(;.]+)', ln)
        if m and not frm: frm = m.group(1).strip().rstrip('.')
        mm = re.search(r'([\d.]+) minutes?, ([\d.]+) km', ln)
        if not mm: continue
        mode = 'Walk' if re.search(r'\bWalk|walking|routed-foot', ln) else 'Drive' if re.search(r'\bDrive|driving|drive|OSRM', ln) else None
        d = re.match(r'(?:Walk|Drive) to (.+?):', ln) or re.match(r'To (.+?): (?:drive|walk)', ln) or re.search(r' to ([^:]+?): [\d.]+ minutes', ln)
        pm = re.search(r'(?:OSRM demo|[Rr]outed-foot[^,]*|OpenStreetMap routed-foot|routing\.openstreetmap\.de routed-foot)[^,]*, (?:driving|walking), (.+?) to ', ln)
        if pm and not frm: frm = pm.group(1).strip()
        if mode and d: rows.append((d.group(1).strip(), mode, float(mm.group(1)), float(mm.group(2))))
    return frm, rows


def plausible(mode, mins, km):
    if mins < 1 or mins > 90 or km <= 0: return False
    sp = km / (mins / 60)
    return (mode == 'Walk' and km <= 1.5 and 3.5 <= sp <= 6.5) or (mode == 'Drive' and km <= 10 and 5 <= sp <= 90)


def tidy(s):
    s = re.sub(r'\s*\((?:address|addresses?)[^)]*(?:search result|searched|read)[^)]*\)', '', s)
    s = re.sub(r'\s*\(address: https?://[^)]*\)', '', s)
    s = re.sub(r'\s*\((?:[^()]*?(?:search result|own site|own page|own source|site search)[^()]*)\)', '', s)
    s = N.clean(s)
    s = ' '.join(x for x in re.split(r'(?<=[.!?])\s+', s) if not DROP.search(x))
    s = re.sub(r'\s*[;,]?\s*(?:none read|none stated) in this pass', '', s)
    s = re.sub(r'\s+', ' ', s).strip().rstrip(';,')
    return s


def target(x):
    if T.exists(x): return x
    ng = None
    try: ng = T.NEWSLUG.get(x)
    except Exception: pass
    for c in (T.ALIAS.get(x), x):
        if c and T.exists(c + '-guide'): return c + '-guide'
        if c and T.exists(c): return c
    for p in sorted(glob.glob(f'{LOCAL}/*-guide.json')):
        j = json.load(open(p, encoding='utf-8'))
        if j.get('tn_page') and x in T.PLACES and os.path.basename(p).startswith(T.slugify(T.PLACES[x][0]) + '-'): return os.path.basename(p)[:-5]
    return None


def H(t, l=3): return {**N.H(t, l), 'gen': G, 'pos': 'end'}
def P(t): return {**N.P(t), 'gen': G, 'pos': 'end'}
def LI(items): return {**N.LI(items), 'gen': G, 'pos': 'end'}
def LK(items): return {**N.LK(items), 'gen': G, 'pos': 'end'}


def block(n):
    sec = n['sec']; name = n['name']; bl = [H(f"What's nearby {name}", 2)]
    bl.append(P(f"Facts here come from the municipality, TransLink or BC Transit, the Ministry of Education and Child Care, and the retailers’ own pages, listed under Sources. Walking and driving times were measured on OpenStreetMap routing on November 2, 2026, from the point named under the table."))
    urls = []; any_ = False
    for k, title in HEAD.items():
        items = []
        for b in sec.get(k, []):
            urls += N.urls(b); t = tidy(b)
            if len(t) >= 25 and not re.match(r'(None|No data)', t): items.append(t)
        if items: bl += [H(title), LI(items)]; any_ = True
    frm, rows = n['frm'], n['rows']
    if frm and rows:
        rows = sorted({(a, m, round(mi), round(km, 1)) for a, m, mi, km in rows if plausible(m, mi, km)}, key=lambda r: (r[1] != 'Walk', r[2]))
        if len(rows) >= 2:
            fr = re.sub(r',?\s*geocoded.*$', '', re.sub(r'\s*\(.*?\)', '', frm), flags=re.I)[:110].strip()
            bl += [H('Measured walking and driving times'), {'t': 'table', 'caption': f'Measured on November 2, 2026 with OpenStreetMap routing (OSRM for driving, routed-foot for walking), from {fr}', 'head': ['To', 'How', 'Minutes', 'Distance (km)'],
                   'rows': [[a, m, str(mi), f'{km:.1f}'] for a, m, mi, km in rows[:12]], 'gen': G, 'pos': 'end'}]; any_ = True
    nc = [tidy(b) for b in sec.get(9, [])]; nc = [x for x in nc if len(x) >= 25]
    if nc: bl += [H('Not confirmed'), LI(nc[:6])]
    sl = N.src_links([u for u in urls if 'jaredgibbons.ca' not in u])
    if sl: bl += [H('Sources for what’s nearby'), LK(sl[:14])]
    return bl if any_ else []


def main():
    notes = {}
    for f in sorted(glob.glob(f'{NOTES}/*{SFX}')):
        x = os.path.basename(f)[:-len(SFX)]; t = open(f, encoding='utf-8').read(); title = t.split('\n')[0][2:].split(' — ')[0].strip()
        sec = sections(t); frm, rows = times(sec.get(5, []))
        name = re.sub(r'\s*\(.*?\)', '', title).split(',')[0].strip()
        tg = target(x)
        if not tg: notes.setdefault('_skip', []).append(x); continue
        n = dict(x=x, name=name, sec=sec, frm=frm, rows=rows, size=len(t))
        if tg not in notes or n['size'] > notes[tg]['size']: notes[tg] = n
    skipped = notes.pop('_skip', [])
    for p in glob.glob(f'{LOCAL}/*.json'):
        j = json.load(open(p, encoding='utf-8'))
        if any(b.get('gen') == G for b in j.get('blocks', [])):
            j['blocks'] = [b for b in j['blocks'] if b.get('gen') != G]; T.save(os.path.basename(p)[:-5], j)
    wrote = 0; empty = []
    for tg, n in sorted(notes.items()):
        bl = block(n)
        if not bl: empty.append(tg); continue
        j = T.load(tg); j['blocks'] = j.get('blocks', []) + bl; j.setdefault('slug', tg); T.save(tg, j); wrote += 1
    print("nearby blocks on", wrote, "pages; notes", len(notes), "skipped", len(skipped), skipped[:12], "empty", len(empty))


if __name__ == '__main__':
    main()
