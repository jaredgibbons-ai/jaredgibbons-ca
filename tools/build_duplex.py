"""Duplex and half-duplex sections from Jared's verified notes (docs/research/local-notes-duplex/*.md, researched 2026-11-01/02),
plus the shared page /bc-duplex-half-duplex-buying-rules.

The program wrote a note for every research slug (503). Most are honest zeros: no named fee-simple half-duplex subdivision and no named 2-lot strata duplex was verified, so the note
states the area's duplex form class (the zones, lot sizes and small-scale multi-unit housing rules that decide where a duplex can sit) and the questions buyers ask.
Only that area-specific content is published. The rules every note repeats (the two legal forms of a half duplex, strata diligence, property transfer tax, GST, age bylaws) are written once
on the rules page. Board counts, listing mentions, cross-references to other counts and process wording are left out.   python3 -I tools/build_duplex.py      (after build_mobilehomes.py)"""
import collections, glob, importlib.util, json, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
HERE = os.path.dirname(os.path.abspath(__file__))
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
M = _load('mh', 'build_mobilehomes.py'); B = M.B; T = M.T; N = M.N; LOCAL = N.LOCAL
NOTES = os.path.join(ROOT, 'docs/research/local-notes-duplex'); G = 'dx'; HUB = 'bc-duplex-half-duplex-buying-rules'; SFX = '-duplex-2026-11-01.md'

DX_DROP = re.compile(r"\b(siblings?|program|brief|ledger|asserted|nowhere|on disk|disk position|cross-?referenc\w*|counted|count (is )?taken|no count|researched|research file|home file|this file|this slug|slug|batch|queue\w*|jerry|zealty|snapstats|"
                     r"directory|feed|listing records?|records? only|carried|flagged|settled|conflation|contested|sweep|guide[- ]form|plain form|form class statement|named component|ground)\b|^\(?(Research|Program)|D1|FILE STATUS", re.I)
KEEP2 = re.compile(r'form class|lot-size|named (stock|farm|duplex)|why the zero|ordinary form|farm-residence|the band|in-band|what a', re.I)
KEEP3 = re.compile(r'SSMUH|small-scale|secondary suite|suite|community plan|official community|zoning|subdivision|lot|hazard|flood|ALR|agricultur|heritage|coach|garden|infill|housing|development permit|OCP|servicing|neighbourhood plan', re.I)
SKIP3 = re.compile(r'strata block|PTT|property transfer|first-home|GST|property tax|age restrict|program discipline|page-statement', re.I)
ACR = {'SSMUH', 'ALR', 'TOD', 'NCP', 'OCP', 'MLS', 'BCAA', 'CSA'}
TOPIC = re.compile(r'under-|over-|lots-land|lots-and-land|open-houses|farms?\b|presales|foreclos|real-estate-agent|condos-for|townhomes-for|houses-for|homes-for-sale-|acreages|poultry|new-construction|duplexes|coach|mobile|horse|plans$|^homepage|^communities|zonings?$|calculator|mortgage|first-time|evaluation|contact|privacy|reviews', re.I)
CAPS = {**M.CAPS, 'FORM CLASS': 'form class', 'FEE-SIMPLE': 'fee-simple', 'STRATA': 'strata', 'DUPLEX': 'duplex', 'HALF DUPLEX': 'half duplex', 'BASELINE': 'baseline'}


def tidy(s):
    s = N.clean(s)
    for a, b in CAPS.items(): s = re.sub(rf'\b{a}\b', b, s)
    s = ' '.join(x for x in B.sents(s) if not B.SENT_DROP.search(x) and not M.META2.search(x) and not DX_DROP.search(x))
    s = re.sub(r'\bUNVERIFIED\b|\bUNCONFIRMED\b', 'unconfirmed', s)
    s = re.sub(r'\s*\((?:Sections?|See) [^)]*$', '', s)
    s = re.sub(r'\((\w[\w ]*?) frame[^)]*\)', r'(\1)', s)
    s = re.sub(r'\b[A-Z]{4,}\b', lambda m: m.group(0) if m.group(0) in ACR else m.group(0).lower(), s)
    s = re.sub(r'\b(NO|NOT|ALL|ANY|NEVER|ONLY|AND)\b', lambda m: m.group(0).lower(), s)
    s = re.sub(r'(^|[.:] )([a-z])', lambda m: m.group(1) + m.group(2).upper(), s)
    return re.sub(r'\s+', ' ', s).strip()


def J(b):
    nm, rest = N.split_bold(b)
    if nm is None: return tidy(b)
    rest = tidy(rest)
    if not rest or len(rest) < 40 or rest[:1] in '(;,': return ''
    nm = re.sub(r'[\s—–:.-]+$', '', N.clean(nm))
    for a, c in CAPS.items(): nm = re.sub(rf'\b{a}\b', c, nm)
    nm = re.sub(r'\((\w[\w ]*?) frame[^)]*\)', r'(\1)', nm)
    nm = re.sub(r'\s+frame\b', '', nm); nm = re.sub(r'\b[A-Z]{4,}\b', lambda m: m.group(0) if m.group(0) in ACR else m.group(0).capitalize() if m.start() == 0 else m.group(0).lower(), nm)
    if re.search(r'form class', nm, re.I): nm = 'The usual duplex form'
    if re.search(r'why the zero', nm, re.I): nm = 'Why duplexes are limited here'
    if not nm or DX_DROP.search(nm) and not KEEP2.search(nm) or len(nm) > 60: return rest
    return f'{nm}: {rest}'


def good(s): return len(s) >= 60 and s.count('(') == s.count(')') and not s[:1].islower() and not re.match(r'(No |None|Zero|Unconfirmed)', s) and not re.search(r'unconfirmed', s[:50], re.I)


def H(t, l=2): return {**N.H(t, l), 'gen': G, 'pos': 'end'}
def P(t): return {**N.P(t), 'gen': G, 'pos': 'end'}
def LI(items): return {**N.LI(items), 'gen': G, 'pos': 'end'}
def LK(items): return {**N.LK(items), 'gen': G, 'pos': 'end'}


def loadnotes():
    notes = {}
    for f in sorted(glob.glob(f'{NOTES}/*{SFX}')):
        x = os.path.basename(f)[:-len(SFX)]; base = re.sub(r'-guide$', '', x)
        title, pre, sec = T.parse_note(f, 'lots-and-land'); size = os.path.getsize(f)
        n = dict(x=base, path=f, title=title, sec=sec, size=size)
        if base not in notes or size > notes[base]['size']: notes[base] = n
    return notes


def section(n, seen, shared_b, shared_q):
    sec = n['sec']; area = n['title'].split(' — ')[0].strip(); name = re.sub(r'\s*\(.*?\)', '', area).split(',')[0].strip() or area
    bl = [H(f'Duplexes and half duplexes in {name}')]
    def fresh(xs):
        out = []
        for x in xs:
            if x and good(x) and x[:70] not in seen: seen.add(x[:70]); out.append(x)
        return out
    stock = fresh([J(b) for b in T.bl4(sec, 2) if N.real(b) and KEEP2.search(N.split_bold(b)[0] or '') and not re.search(r'directory|age|cross|record|excluded', N.split_bold(b)[0] or '', re.I)])
    rules = fresh([J(b) for b in T.bl4(sec, 3) if N.real(b) and T.key(b) not in shared_b and KEEP3.search(N.split_bold(b)[0] or '') and not SKIP3.search(N.split_bold(b)[0] or '')])
    if stock: bl += [H(f'What a duplex looks like in {name}', 3), LI(stock[:5])]
    if rules: bl += [H(f'Local rules that affect duplexes in {name}', 3), LI(rules[:5])]
    bl.append(P('How a half duplex can legally be sold (strata duplex or fee-simple half duplex), the strata checks, and the tax points are explained once, with sources, on the page linked below.'))
    bl.append(LK([('BC duplex and half-duplex buying rules', f'/{HUB}.html')]))
    u = [x for k in (1, 2, 3, 4) for b in T.bl4(sec, k) for x in N.urls(b)]
    u = [x for x in u if re.search(r'zoning|ssmuh|small-scale|multi-unit|housing|bylaw|official-community|ocp|land-use|plan|suite|duplex|subdivision|flood|alr|agricultur|development', x, re.I)]
    sl = N.src_links([x for x in u if 'jaredgibbons.ca' not in x], skip=('property-transfer', 'age-restriction', 'strata-housing', 'news122', 'excise', 'canada.ca', 'cotala', 'canadashomesearch', 'translink', 'deltasd', 'sd3'))
    if sl: bl += [H(f'Sources for the duplex notes on {name}', 3), LK(sl[:10])]
    faq = []
    for b in T.bl4(sec, 4):
        m = re.match(r'\*\*Q:\s*(.*?)\*\*\s*(.*)', b)
        if not m: continue
        q = m.group(1).strip(); a = tidy(m.group(2))
        if T.qkey(q) in shared_q or N.FQ_BAD.search(q) or DX_DROP.search(q) or M.META2.search(q) or len(a) < 70 or re.search(r'\bpage\b|\bfile\b|stats|median|how many|sold|PTT|GST|foreclos|depreciation|rental|age|Form B|price|market|snapstats', q, re.I): continue
        faq.append({'gen': G, 'q': q, 'a': a})
    return bl, faq[:4]


def hub():
    U = 'https://www2.gov.bc.ca/gov/content/'
    srcs = [U + 'housing-tenancy/strata-housing', U + 'housing-tenancy/strata-housing/operating-a-strata/bylaws-and-rules/age-restriction-bylaws', U + 'taxes/property-taxes/property-transfer-tax',
            U + 'housing-tenancy/strata-housing/strata-property-act', 'https://www.canada.ca/en/revenue-agency/services/forms-publications/publications/gi-003/goods-services-tax-harmonized-sales-tax-gst-hst-new-housing-rebate.html']
    s = lambda t: {**N.P(t), 'gen': G}; h = lambda t: {**N.H(t, 2), 'gen': G}
    bl = [{'t': 'notice', 'text': "Draft for Jared's approval. Built from the BC Strata Property Act pages, the BC property transfer tax page and the CRA new-housing rebate guide named under Sources, read November 1, 2026. Not legal advice.", 'gen': G},
          s('These BC points apply to every duplex or half-duplex purchase on this site, whichever area it is in. They are written once here; each area page covers only the duplex form and local rules specific to that area.'), {'t': 'grid', 'gen': G},
          h('A duplex and a half duplex are not the same thing'),
          s('A duplex is one building with two dwelling units, usually on one lot under one title. A half duplex is one of the two units sold on its own. In BC that happens in two legal forms only: a strata duplex, where the pair is a two-lot strata plan and each half is a strata lot, or a fee-simple half duplex, where the parcel was subdivided so each half sits on its own lot. A duplex that was never strata-divided or subdivided cannot be bought by the half: the whole building and lot sell together.'),
          h('Strata duplex: what to check'),
          s('A strata half duplex is bought like any strata lot. Ask for the Form B information certificate, the bylaws and rules, the financial statements, the insurance and the meeting minutes. Depreciation reports run on a five-year cycle for stratas with five or more lots, so a two-lot strata falls below that threshold on lot count alone; still ask what reports the strata holds. The minimum contingency-reserve contribution is 10% of the operating budget. Rental-restriction bylaws have been void since November 24, 2022.'),
          h('Age restrictions'),
          s('Only a 55+ age bylaw is valid in a BC strata. A strata may restrict residents to age 55 or older under sections 123.1 and 123.2 of the Strata Property Act, and a bylaw set below 55 has been invalid since November 24, 2022. Nothing on this site presents a duplex as age-restricted unless the strata bylaw says so.'),
          h('Fee-simple half duplex: subdivision and the party wall'),
          s('Splitting a duplex lot into two titles needs subdivision approval through the municipality’s Approving Officer, against the zoning minimums in force. The two owners are tied together by the registered party-wall or easement agreement on both titles, so read both titles and the agreement before you remove subjects.'),
          h('Small-scale multi-unit housing does not split a duplex'),
          s('BC’s small-scale multi-unit housing (SSMUH) zoning lets many single-detached and duplex lots hold more units, including suites and coach houses where the municipality allows them. More units on a lot is not the same as separate titles: a separately owned half still needs a strata plan or a subdivision. Each municipality’s own rules are summarized on its area pages.'),
          h('Property transfer tax'),
          s('BC property transfer tax is 1% on the first $200,000, 2% from $200,000 to $2,000,000, 3% above $2,000,000, and a further 2% on the residential portion above $3,000,000. On a fully residential purchase with no exemption, $800,000 is $14,000, $1,000,000 is $18,000 and $2,000,000 is $38,000. A half duplex is taxed on its own purchase price as its own transfer. First-time buyer and newly built exemptions have their own tests, so check the Province’s page for your purchase.'),
          h('GST'),
          s('GST and the federal new-housing rebates apply to new housing. A resale duplex or half duplex is not new housing for those rebates. If you are buying a newly built half duplex, the contract should state whether GST is included, and who claims any rebate.')]
    sl = N.src_links(srcs)
    links = [(a, h2) for a, h2 in [('BC 55+ strata rules', '/bc-55-plus-strata-rules.html'), ('Townhomes for sale', '/townhomes-for-sale.html'), ('Mortgage calculator', '/mortgage-calculator.html'), ('Home evaluation', '/home-evaluation.html'),
                                  ('Data and methodology', '/data-and-methodology.html'), ('Contact Jared', '/contact.html')] if T.exists(h2[1:-5])]
    bl += [{**N.H('Sources', 2), 'gen': G}, {**N.LK(sl), 'gen': G}, {**N.H('More real estate', 2), 'gen': G, 'pos': 'end'}, {**N.LK(links), 'gen': G, 'pos': 'end'}]
    faq = [{'q': 'What is the difference between a duplex and a half duplex in BC?', 'a': 'A duplex is one building with two units, normally on one lot and one title. A half duplex is one of the two units sold separately, which in BC only happens as a strata lot in a two-lot strata plan or as a fee-simple lot created by subdivision.'},
           {'q': 'Can I buy just one half of a duplex?', 'a': 'Only if the two halves already have separate titles, either as strata lots or as subdivided fee-simple lots. If the duplex sits on one lot under one title, the whole building and lot sell together.'},
           {'q': 'Does a two-lot strata need a depreciation report?', 'a': 'The five-year depreciation-report cycle applies to stratas with five or more lots, so a two-lot strata is below that threshold on lot count. Ask the strata what reports it holds anyway.'},
           {'q': 'Does small-scale multi-unit housing zoning let me split a duplex into two titles?', 'a': 'No. It allows more units on a lot, not separate ownership. A separately titled half needs a strata plan or a subdivision.'},
           {'q': 'Can a strata ban rentals or set an under-55 age limit?', 'a': 'No. Rental-restriction bylaws have been void since November 24, 2022, and only a 55+ age bylaw is valid.'},
           {'q': 'How is property transfer tax calculated on a half duplex?', 'a': 'On the half’s own purchase price using the standard tiers: 1% to $200,000, 2% to $2,000,000, 3% above that, and a further 2% on the residential portion above $3,000,000, unless an exemption applies.'}]
    d = {'status': 'draft', 'slug': HUB, 'updated': '2026-11-02', 'dx_page': True, 'hand_edited': True, 'blocks': bl, 'faq': faq, 'faq_heading': 'BC duplex and half-duplex buying: your questions answered',
         'new_page': {'title': 'BC Duplex and Half-Duplex Buying Rules | Jared Gibbons', 'description': 'How a half duplex is legally sold in BC (strata or fee-simple), strata checks, 55+ bylaws, property transfer tax and GST, with sources. Jared Gibbons, REALTOR®.'[:158],
                      'h1': 'BC Duplex and Half-Duplex Buying Rules'},
         'breadcrumbs': [{'name': 'Home', 'href': '/'}, {'name': 'BC Duplex and Half-Duplex Buying Rules', 'href': f'/{HUB}.html'}], 'needs_from_muse': ['Jared’s review of the wording']}
    T.save(HUB, d)


def main():
    notes = loadnotes()
    for p in glob.glob(f'{LOCAL}/*.json'):
        j = json.load(open(p, encoding='utf-8'))
        if any(b.get('gen') == G for b in j.get('blocks', [])) or any(f.get('gen') == G for f in j.get('faq', [])):
            j['blocks'] = [b for b in j['blocks'] if b.get('gen') != G]; j['faq'] = [f for f in j.get('faq', []) if f.get('gen') != G]; T.save(os.path.basename(p)[:-5], j)
    cb, cq = collections.Counter(), collections.Counter()
    for f in glob.glob(f'{NOTES}/*{SFX}'):
        title, pre, sec = T.parse_note(f, 'x'); sb, sq = set(), set()
        for b in T.bl4(sec, 3): sb.add(T.key(b))
        for b in T.bl4(sec, 4):
            m = re.match(r'\*\*Q:\s*(.*?)\*\*', b)
            if m: sq.add(T.qkey(m.group(1)))
        cb.update(sb); cq.update(sq)
    shared_b = {k for k, c in cb.items() if c >= 8}; shared_q = {k for k, c in cq.items() if c >= 6}
    seen = set()
    for pth in glob.glob(f'{LOCAL}/*.json'):
        for b in json.load(open(pth, encoding='utf-8')).get('blocks', []):
            if b.get('t') == 'list':
                for it in b['items']: seen.add(it[0].get('t', '')[:70])
    tg = collections.defaultdict(list); skipped = []
    for x, n in sorted(notes.items()):
        t = M.target(x)
        if not t: skipped.append(x); continue
        if TOPIC.search(t): skipped.append(t); continue
        tg[t].append(n)
    for t in tg: tg[t] = [max(tg[t], key=lambda n: n['size'])]
    wrote = 0
    for t, ns in sorted(tg.items()):
        j = T.load(t); bl = []; faq = []
        for n in sorted(ns, key=lambda n: n['x']):
            b, f = section(n, seen, shared_b, shared_q); bl += b; faq += f
        for b in bl:
            if b['t'] == 'list': b['items'] = [i for i in b['items'] if i[0].get('h') or len(i[0]['t']) >= 40]
        bl = [b for b in bl if not (b['t'] == 'list' and not b['items'])]
        bl = [b for i, b in enumerate(bl) if not (b['t'] == 'h' and b['level'] >= 3 and (i + 1 == len(bl) or bl[i + 1]['t'] == 'h') and 'Sources' not in b['text'])]
        body = sum(1 for b in bl if b['t'] == 'list' and b['items'] and not b['items'][0][0].get('h'))
        if body < 1: skipped.append(t); continue
        j['blocks'] = j.get('blocks', []) + bl
        have = {T.qkey(x['q']) for x in j.get('faq', [])}
        j['faq'] = j.get('faq', []) + [x for x in faq if T.qkey(x['q']) not in have][:4]
        j.setdefault('slug', t); T.save(t, j); wrote += 1
    hub()
    for s in ('bc-55-plus-strata-rules', 'townhomes-for-sale'):
        if T.exists(s):
            j = T.load(s)
            j['blocks'] = j.get('blocks', []) + [{**N.H('Buying a duplex or half duplex', 2), 'gen': G, 'pos': 'end'}, {**N.P('How a half duplex is legally sold in BC, the strata checks and the tax points are explained on their own page.'), 'gen': G, 'pos': 'end'}, {**N.LK([('BC duplex and half-duplex buying rules', f'/{HUB}.html')]), 'gen': G, 'pos': 'end'}]
            T.save(s, j)
    print('duplex sections on', wrote, 'pages; notes', len(notes), 'skipped', len(skipped))


if __name__ == '__main__':
    main()
