"""Uniqueness-program notes (docs/research/local-notes-uniqueness/*-extra-2026-11-03.md, researched 2026-11-03) -> sections on the page of the same slug (gen 'uq').

Each note has ten sections (streets and boundaries, housing stock, rules, buyer questions, local details, development, costs, getting around, risks, comparison table),
a NOT CONFIRMED list and internal-link suggestions. Every fact carries an official source URL; URLs are collected once under "Sources" and never appear in the text.
Cleaned like every notes builder (N.clean: no research wording, no file paths, no board data). Section 4 questions become FAQ entries (gen 'uq').
Quarantined, not published: notes that describe a different place than our page (QUARANTINE, found by comparing the note's own "Page:" line and place names with the page title).
Not published: lines about the research itself (brief, program, slug, pass, 'Jared to confirm'), anything marked a guess.
python3 -I tools/build_uniqueness.py      (after build_nearby_buildings.py)"""
import collections, glob, importlib.util, json, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); HERE = os.path.dirname(os.path.abspath(__file__))
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
NB = _load('nbmod', 'build_nearby.py'); T = NB.T; N = NB.N; LOCAL = N.LOCAL; PAGES = N.PAGES
NOTES = os.path.join(ROOT, 'docs/research/local-notes-uniqueness'); G = 'uq'; SFX = '-extra-2026-11-03.md'
# A note that describes another place than our page (checked against the note's Page: line and the page title) is held here. Holly and Hawthorne (Ladner) were redone on 2026-11-03 and now publish.
QUARANTINE = {'lower-landing': 'every note filed under this slug (uniqueness, nearby, types, acreages, 55+, Muse FAQs, 5 buildings) described London Landing in Steveston, Richmond; our page is Lower Landing, Chilliwack (a Paragon sub-area with no City-published boundary). Held until Jared supplies the Paragon sub-area boundary or streets.'}
SECS = {1: 'streets and boundaries', 2: 'the housing stock', 3: 'rules that affect buyers', 4: 'what buyers ask', 5: 'local details a buyer would not know', 6: 'development and new projects',
        7: 'costs and taxes', 8: 'getting around', 9: 'risks and due diligence', 10: 'how it compares'}
META = re.compile(r"\b(?:city|house|condo|townhome|area|guide|earlier|other|sibling|shared) notes?\b|\b(?:this|that|the) (?:note|file)\b|\b[a-z0-9]+(?:-[a-z0-9]+)+ (?:note|page|guide note)\b|\bnotes? for [a-z0-9]+(?:-[a-z0-9]+)+|\bfull entry in\b|\bcovered in full in\b|\b(?:brief|program(?:me)?|slug|this pass|in this pass|assigned|assignment|sibling|earlier file|earlier note|settled|Jared to confirm|Jared should|roster|batch|follows? the|was not followed|this note|the note|this file|see NOT CONFIRMED|NOT CONFIRMED|returned in this|no .{0,30} was returned|search (?:result|returned))\b", re.I)
READ = re.compile(r'^Read:\s*\d{4}-\d\d-\d\d\s*$')


def sections(t):
    sec = collections.OrderedDict(); cur = None
    for ln in t.split('\n'):
        m = re.match(r'^## (\d+)\.', ln)
        if m: cur = int(m.group(1)); sec[cur] = []; continue
        if re.match(r'^## NOT CONFIRMED', ln): cur = 'nc'; sec[cur] = []; continue
        if re.match(r'^## INTERNAL[ -]LINK', ln, re.I): cur = 'il'; sec[cur] = []; continue
        if cur is not None and ln.strip() and not READ.match(ln.strip()):
            if re.match(r'^- [a-z0-9]+(?:-[a-z0-9]+)* [—-] ', ln) and cur in ('nc', 'il'): sec.setdefault('il', []).append(ln.rstrip()); continue
            sec[cur].append(ln.rstrip())
    return sec


def tidy(s):
    s = re.sub(r'(?i)\bunconfirmed\b', 'not confirmed', s); s = re.sub(r'(?i)\bunverified\b', 'not verified', s)
    s = re.sub(r'\s*[—-]?\s*\(?see NOT CONFIRMED\)?', '', s)
    s = NB.tidy(s)
    s = ' '.join(x for x in re.split(r'(?<=[.!?])\s+', s) if not META.search(x))
    return re.sub(r'\s+', ' ', s).strip()


def bullets(lines):
    out = []; urls = []
    for ln in lines:
        if ln.startswith('|'): continue
        b = ln[2:].strip() if ln.startswith('- ') else ln.strip()
        if not b or b.startswith('#'): continue
        urls += N.urls(b); t = tidy(b)
        if len(t) >= 25 and not re.match(r'(None|No data|No active applications found)', t) and t not in out: out.append(t)
    return out, urls


def qa(lines):
    out = []; urls = []
    for ln in lines:
        m = re.match(r'^- \*\*Q:\*\*\s*(.+?)\s*\*\*A:\*\*\s*(.+)$', ln)
        if not m: continue
        urls += N.urls(m.group(2)); q = tidy(m.group(1)); a = tidy(m.group(2))
        if len(q) >= 12 and len(a) >= 60: out.append((q if q.endswith('?') else q + '?', a))
    return out, urls


def table(lines):
    rows = [[c.strip() for c in ln.strip().strip('|').split('|')] for ln in lines if ln.startswith('|')]
    rows = [r for r in rows if not all(re.fullmatch(r':?-+:?', c) for c in r)]
    if len(rows) < 3: return None, []
    urls = []; clean = []
    for r in rows:
        row = []
        for c in r:
            urls += N.urls(c); c = tidy(re.sub(r'https?://\S+', '', c)) if c else ''
            c = 'Not confirmed' if re.fullmatch(r'(?i)un(?:confirmed|verified)|not confirmed', c or '') else c
            row.append(c or '—')
        clean.append(row)
    w = len(clean[0]); clean = [r[:w] + ['—'] * (w - len(r)) for r in clean]
    return {'t': 'table', 'caption': '', 'head': clean[0], 'rows': clean[1:], 'gen': G, 'pos': 'end'}, urls


def title_of(s):
    try:
        o = json.load(open(os.path.join(ROOT, 'src/data/seo-overrides.json'), encoding='utf-8'))
        if s in o and o[s].get('title'): t = o[s]['title']
        else: t = json.load(open(f'{PAGES}/{s}.json', encoding='utf-8'))['seo']['Title']
    except Exception: return None
    t = re.split(r'\s+\|\s+Jared Gibbons', t)[0].strip()
    return t or None


def H(t, l=2): return {**N.H(t, l), 'gen': G, 'pos': 'end'}
def P(t): return {**N.P(t), 'gen': G, 'pos': 'end'}
def LI(items): return {**N.LI(items), 'gen': G, 'pos': 'end'}
def LK(items): return {**N.LK(items), 'gen': G, 'pos': 'end'}


def build(slug, t):
    lines0 = t.split('\n'); name = re.sub(r'\s*—\s*Extra Local Notes.*$', '', lines0[0][2:]).strip()
    name = re.sub(r'\s+(Neighbourhood|Area Guide|Guide)$', '', name, flags=re.I).strip() or name
    sec = sections(t); bl = []; urls = []; faq = []
    for k in range(1, 11):
        ls = sec.get(k, [])
        if k == 10:
            tb, u = table(ls)
            if tb: tb['caption'] = f'{name} compared'; bl += [H(f'How {name} compares'), tb]; urls += u
            continue
        if k == 4:
            f, u = qa(ls); faq += f; urls += u; continue
        items, u = bullets(ls); urls += u
        if len(items) >= 1 and sum(len(x) for x in items) >= 120:
            bl += [H(f'{name}: {SECS[k]}'), LI(items)]
    nc, u = bullets(sec.get('nc', []))
    nc = [x for x in nc if not re.search(r'\bParagon\b|sub-area code|catchment results|locator', x)][:5]
    if nc: bl += [H(f'What is not confirmed about {name}'), LI(nc)]
    rel = []
    for ln in sec.get('il', []):
        m = re.match(r'^- ([a-z0-9-]+)\b', ln)
        if m and m.group(1) != slug and T.exists(m.group(1)):
            tt = title_of(m.group(1))
            if tt: rel.append((tt, f'/{m.group(1)}.html'))
    if rel: bl += [H(f'Related pages'), LK(rel[:4])]
    sl = N.src_links([x for x in urls + [y for y in u] if 'jaredgibbons.ca' not in x])
    if sl: bl += [H(f'Sources for {name}'), LK(sl[:16])]
    return bl, faq[:4]


def rank(slug):
    if slug.endswith('-guide'): r = 1
    elif slug.endswith('-houses-for-sale'): r = 2
    elif re.search(r'-(?:condos|townhomes|condos-townhomes)-for-sale$|-55-plus', slug): r = 3
    elif re.search(r'-for-sale$|-for-sale-', slug): r = 4
    else: r = 0
    return (r, len(slug), slug)


def sents(x): return [y for y in re.split(r'(?<=[.!?])\s+', x) if y]
def nrm(x): return re.sub(r'[^a-z0-9]+', ' ', x.lower()).strip()


def dedupe(built):
    """A sentence that several pages' notes share (the same area facts repeated in a houses note, a condos note and the area guide) is kept on one page only:
    the area page, else its guide, else houses, else condos and townhomes. The other pages keep their own facts, so no two pages carry the same words."""
    def walk(bl, faq):
        for b in bl:
            if b['t'] == 'list':
                for it in b['items']:
                    if not it[0].get('h'):
                        for x in sents(it[0]['t']): yield x
        for q, a in faq:
            for x in sents(a): yield x
    def sh(x):
        w = re.findall(r"[a-z0-9$%'.\-]+", x.lower()); return {' '.join(w[i:i + 8]) for i in range(max(0, len(w) - 7))}
    where = collections.defaultdict(set)
    for slug, (bl, faq) in built.items():
        for x in walk(bl, faq):
            for k in sh(x): where[k].add(slug)
    owner = {k: min(v, key=rank) for k, v in where.items() if 1 < len(v) < 40}
    def ok_for(slug):
        def ok(x):
            ks = [k for k in sh(x) if k in owner]; allk = sh(x)
            return not allk or sum(1 for k in ks if owner[k] != slug) / len(allk) < 0.3
        return ok
    dropped = 0
    for slug, (bl, faq) in built.items():
        ok = ok_for(slug)
        for b in bl:
            if b['t'] != 'list': continue
            new = []
            for it in b['items']:
                if it[0].get('h'): new.append(it); continue
                ss = sents(it[0]['t']); kept = [x for x in ss if ok(x)]; dropped += len(ss) - len(kept)
                t = ' '.join(kept)
                if len(t) >= 25: new.append([{'t': t}])
            b['items'] = new
        faq[:] = [(q, ' '.join(x for x in sents(a) if ok(x))) for q, a in faq]; faq[:] = [(q, a) for q, a in faq if len(a) >= 60]
        i = 0; out = []
        for j, b in enumerate(bl):  # a heading with nothing under it goes
            if b['t'] == 'h' and (j + 1 >= len(bl) or bl[j + 1]['t'] == 'h' or (bl[j + 1]['t'] == 'list' and not bl[j + 1]['items'])): continue
            if b['t'] == 'list' and not b['items']: continue
            out.append(b)
        bl[:] = out
    print('shared sentences removed from the lower-priority pages:', dropped)


def main():
    for p in glob.glob(f'{LOCAL}/*.json'):
        j = json.load(open(p, encoding='utf-8')); ch = False
        if any(b.get('gen') == G for b in j.get('blocks', [])): j['blocks'] = [b for b in j['blocks'] if b.get('gen') != G]; ch = True
        if any(f.get('gen') == G for f in j.get('faq', [])): j['faq'] = [f for f in j['faq'] if f.get('gen') != G]; ch = True
        if ch: T.save(os.path.basename(p)[:-5], j)
    wrote = nfaq = 0; skipped = []; quarantined = []; thin = []; built = {}
    for f in sorted(glob.glob(f'{NOTES}/*{SFX}')):
        slug = os.path.basename(f)[:-len(SFX)]
        if slug in QUARANTINE: quarantined.append(slug); continue
        if not T.exists(slug): skipped.append(slug); continue
        built[slug] = build(slug, open(f, encoding='utf-8').read())
    dedupe(built)
    for slug, (bl, faq) in sorted(built.items()):
        if len([b for b in bl if b['t'] == 'h']) < 3: thin.append(slug); continue
        j = T.load(slug); j['blocks'] = j.get('blocks', []) + bl; j.setdefault('slug', slug)
        have = {x['q'] for x in j.get('faq', [])}
        add = [{'gen': G, 'q': q, 'a': a} for q, a in faq if q not in have]; j['faq'] = j.get('faq', []) + add; nfaq += len(add)
        T.save(slug, j); wrote += 1
    print('uniqueness sections on', wrote, 'pages;', nfaq, 'FAQ entries; no page', len(skipped), skipped[:10], '; thin', len(thin), thin[:10], '; quarantined', quarantined)


if __name__ == '__main__':
    main()
