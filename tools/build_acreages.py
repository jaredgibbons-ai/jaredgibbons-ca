"""Acreage, farm and rural-land sections from Jared's verified acreage notes (docs/research/local-notes-acreages/*.md, researched 2026-11-01/02),
plus the shared page /bc-acreage-buying-rules.

The program wrote one note for every research slug (503), but about 420 of them are urban or built-up areas whose acreage position is "none". Those get no page and no section.
Only the notes in RURAL below (farm, poultry and horse topics, and the neighbourhoods with real rural or farm ground) are published. Where each goes (mine; Jared sent no routing):
 - a farm / acreage / poultry topic note -> the page of the same name, if the site has one
 - a neighbourhood note -> that neighbourhood's guide or page (or the new guide the type-notes build made for it)
The provincial rules every acreage note repeats (ALR limits, farm class, GST on farm land) are written once on the rules page, with the ALC / BC Assessment / CRA pages as sources,
and left out of the community sections. Text is cleaned like build_55plus_notes; board counts, listing-feed snapshots and MLS numbers are dropped.
   python3 -I tools/build_acreages.py      (after build_typenotes.py)"""
import collections, glob, importlib.util, json, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
spec = importlib.util.spec_from_file_location('tn', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_typenotes.py'))
T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
N = T.N; LOCAL = N.LOCAL
NOTES = os.path.join(ROOT, 'docs/research/local-notes-acreages'); G = 'acre'; HUB = 'bc-acreage-buying-rules'
RURAL = set("""abbotsford-farms abbotsford-poultry-farms chilliwack-farms chilliwack-poultry-farms-for-sale cloverdale-farms ladner-farms langley-farms langley-farms-for-sale-acreages-agricultural-land-mls
langley-acreages-for-sale langley-horse-properties-equestrian-farms-for-sale-mls-listings langley-poultry-farms-for-sale maple-ridge-farms mission-farms south-surrey-farms surrey-farms tsawwassen-farms
fraser-valley-acreages-for-sale campbell-valley-acreages-farms-for-sale salmon-river-acreages-farms-for-sale farms poultry-farms-for-sale-bc broiler-farms-for-sale-bc chicken-farms egg-farms-for-sale-bc
turkey-farms-for-sale-bc buying-a-chicken-farm-bc
aberdeen abbotsford-west abbotsford-east agassiz albion barnston-island big-bend bradner campbell-valley chilliwack-mountain county-line-glen-valley durieu east-chilliwack east-delta eastern-hillsides
hatzic hazelmere kent ladner-rural matsqui mission-west mt-lehman north-maple-ridge north-meadows-pi northeast northwest-maple-ridge otter-district poplar port-guichon salmon-river serpentine silver-valley
stave-falls steelhead sumas-mountain sumas-prairie thornhill-mr websters-corners west-chilliwack west-meadows-pitt-meadows westham-island whonnock popkum lake-errock hope dewdney-deroche
cultus-lake-east cultus-lake-north cultus-lake-south tilbury fort-langley anmore-homes-for-sale tsawwassen-east tsawwassen-north cloverdale-bc south-meadows-pitt-meadows mid-meadows-pitt-meadows
central-meadows-pitt-meadows sardis-south sardis-east-vedder sardis-west-vedder fairfield-island lower-landing east-central west-central southwest-maple-ridge cottonwood-mr""".split())
# bullets / sentences that describe the research process, the listing feed or board statistics, not the land
LEAD_DROP = re.compile(r'Page identity|Topic scope|How people search|Market numbers|The feed|Attached|Detached|Assembl|COUNT HOMES|HELD OUT|Presale|cross-?ref|Honest market|Market (context|figures)|Bare-land strata (acreage )?(communities|—|:)|Proposals documented|Pad ground|Registry|Short-term|Property tax|Speculation|Foreclosure|First-home|Federal|Property transfer|PTT|Marketing board|Quota|^Schools?$|Census', re.I)
SENT_DROP = re.compile(r'\d+ / \d+ / (?:\d+%|NA)|\d+ / \d+ / \d+|Attached —|Detached —|SnapStats|\binventory\b|\bfeed\b|\bcards?\b|at reading|\bsnapshot\b|\bsold\b.*\bmedian\b|\bmedian\b|\bsales? counts?\b|UNVERIFIED.*\bnone\b|segment (figure|statistic)|[Ss]ibling|\bprogram\b|\bthis file\b|\bthe research\b|lots-and-land', re.I)
RULE_LEAD = re.compile(r'^(ALR (rules|conditional|position)|Farm class|GST|Property transfer|PTT|First-home|Federal|Foreclosure|Speculation|Registry|Property tax|BC strata|Pad ground|Short-term|Quota|Marketing board|Market context|Subdivision (and|/) servicing|OCP|SSMUH|Coach house)', re.I)
TOP_SKIP = re.compile(r'^(none|n/a)$', re.I)
# an item that is about what the research did or did not find, not about the land
META = re.compile(r"\b(stated|states|stating|documented|documents|carried|ledger|smoothed|none (is|are)|neither|research|batch|slug|topic file|this (file|topic|page|shelf)|sub-area itself|same ground|distinct pages?|not smoothed|cross-reference|verified in|no source|never asserted|asserted|imported|opened|reading|pass)\b|unconfirmed (until|in|on|for)|is unconfirmed|are unconfirmed|NOT unique|the sources|extracted|unverified|quoted|Market numbers|\bfeed\b|Timberlane|held out|counted", re.I)
def good(s): return len(s) >= 70 and not META.search(s) and s.count('(') == s.count(')') and not re.match(r'\d{4}\s+[A-Z]+\)', s) and not s[:1].islower()


def slugify(t): return T.slugify(t)


def loadnotes():
    notes = {}
    for f in sorted(glob.glob(f'{NOTES}/*-acreages-2026-11-01.md')):
        x = os.path.basename(f)[:-len('-acreages-2026-11-01.md')]; base = re.sub(r'-guide$', '', x)
        if base not in RURAL: continue
        title, pre, sec = T.parse_note(f, 'lots-and-land'); t = open(f, encoding='utf-8').read()
        m = re.search(r'## 2\. THE ACREAGE ITSELF\n(.*?)\n## 3', t, re.S); intro = ''
        if m:
            for ln in m.group(1).split('\n'):
                if ln.strip() and not ln.startswith('- '): intro = ln.strip(); break
        n = dict(x=base, path=f, title=title, sec=sec, intro=intro, size=len(t))
        if base not in notes or n['size'] > notes[base]['size']: notes[base] = n
    return notes


def newguide(x):
    """slug of a guide page the type-notes build made for a place Jared named (agassiz, kent, hope ...)."""
    if x not in T.PLACES: return None
    dn = T.PLACES[x][0]
    for p in sorted(glob.glob(f'{LOCAL}/*-guide.json')):
        j = json.load(open(p, encoding='utf-8'))
        if j.get('tn_page') and os.path.basename(p).startswith(slugify(dn) + '-'): return os.path.basename(p)[:-5]
    return None


def target(x):
    if T.exists(x) and (x in RURAL and re.search(r'farm|acreage|poultry', x)): return x
    for c in (x + '-acreages-for-sale', x + '-acreages-farms-for-sale'):
        if T.exists(c): return c
    ng = newguide(x)
    if ng: return ng
    cands = [T.ALIAS.get(x), x]
    for c in cands:
        if c and T.exists(c + '-guide') and (c + '-guide' in T.MAPPED or c in T.COMM): return c + '-guide'
        if c and T.exists(c) and c in T.COMM: return c
    for c in cands:
        if c and T.exists(c + '-guide'): return c + '-guide'
        if c and T.exists(c): return c
    return None


def sents(s):
    return [x for x in re.split(r'(?<=[.!?])(?<!\bSt\.)(?<!\bMt\.)(?<!\bDr\.)(?<!\bAve\.)(?<!\bNo\.)\s+', s) if x]


def tidy(s):
    """N.clean, then drop sentences that talk about the listing feed, board statistics or the research itself."""
    s = N.clean(s)
    s = ' '.join(x for x in sents(s) if not SENT_DROP.search(x))
    s = re.sub(r'\bUNVERIFIED\b', 'unconfirmed', s); s = re.sub(r'\bUNCONFIRMED\b', 'unconfirmed', s)
    s = re.sub(r'\s*\((?:Sections?|Section) [^)]*$', '', s)
    s = re.sub(r'\b(block|frame|rules?|bylaw|section) in (governs|applies|and|is)\b', r'\1 \2', s)
    for w in ('VERIFIED', 'NOT', 'NEVER', 'ONLY', 'NONE', 'ALWAYS'): s = re.sub(rf'\b{w}\b', w.lower(), s)
    s = re.sub(r'\s+(?:in|see|per|under)\.$', '.', re.sub(r'\s+', ' ', s).strip())
    return re.sub(r'\(Standing correction\.?\)', '', s).strip()


def J(b):
    nm, rest = N.split_bold(b)
    if nm is None: return tidy(b)
    nm, rest = re.sub(r'[\s—–:.-]+$', '', N.clean(nm)), tidy(rest)
    if not rest or len(rest) < 25: return ''
    if rest[:1] in '(;,': return ''
    if not nm: return rest
    nm = re.sub(r',? (as|only as) (the )?(research|official|sources?)[^:—]*$', '', nm).strip()
    if ' — ' in nm and len(nm) > 38: nm = nm.split(' — ')[0].strip()
    if SENT_DROP.search(nm) or LEAD_DROP.search(nm): return ''
    return f'{nm}: {rest}'


def H(t, l=2): return {**N.H(t, l), 'gen': G, 'pos': 'end'}
def P(t): return {**N.P(t), 'gen': G, 'pos': 'end'}
def LI(items): return {**N.LI(items), 'gen': G, 'pos': 'end'}
def LK(items): return {**N.LK(items), 'gen': G, 'pos': 'end'}


def section(n, seen, qshared):
    sec = n['sec']; area = n['title'].split(' — ')[0].strip(); name = re.sub(r'\s*\(.*?\)', '', area).split(',')[0].strip()
    name = re.sub(r'^(Acreages?|Farms?) (in|of) ', '', name)
    topic = bool(re.search(r'farm|acreage|poultry|horse|chicken|egg|turkey|broiler', name, re.I))
    bl = [H(f'{name}: what the ground is and what governs it' if topic else f'Acreage and rural land in {name}')]
    intro = tidy(re.sub(r'^\*\*(.*?)\*\*', r'\1', n['intro'])); isn = sents(intro)
    isn = [x for x in isn if good(x) or (len(x) > 50 and not META.search(x))]
    if isn: bl.append(P(' '.join(isn[:3])))
    def fresh(xs):
        out = []
        for x in xs:
            if x and good(x) and not LEAD_DROP.match(x) and x[:70] not in seen: seen.add(x[:70]); out.append(x)
        return out
    ground = []
    for b in sec.get(2, {}).get('_', []):
        nm, rest = N.split_bold(b)
        if not nm or not N.real(b) or LEAD_DROP.search(nm): continue
        ground.append(J(b))
    ground = fresh(ground)
    if ground: bl += [H('The ground' if topic else f'The ground in {name}', 3), LI(ground)]
    s1 = fresh([J(b) for b in T.bl4(sec, 1) if N.real(b) and not b.startswith(('Market figures', 'Market context')) and not LEAD_DROP.search(N.split_bold(b)[0] or '')])
    if s1: bl += [H('Scope and area context' if topic else f'Streets, schools and getting around {name}', 3), LI(s1)]
    s3 = fresh([J(b) for b in T.bl4(sec, 3) if N.real(b) and not RULE_LEAD.search(N.split_bold(b)[0] or '') and not LEAD_DROP.search(N.split_bold(b)[0] or '')])
    if s3: bl += [H('Local rules that affect acreage buyers' if topic else f'Local rules that affect acreage buyers in {name}', 3), LI(s3)]
    s5 = fresh([J(b) for b in T.bl4(sec, 5) if N.real(b) and not LEAD_DROP.search(N.split_bold(b)[0] or '')])
    if s5: bl += [H('Good to know' if topic else f'Good to know about {name}', 3), LI(s5)]
    bl.append(P('The BC rules that apply to every acreage purchase (Agricultural Land Reserve limits, farm class and GST on farm land) are explained once, with sources, on the page linked below.'))
    bl.append(LK([('BC acreage buying rules', f'/{HUB}.html')]))
    u = [x for k in (1, 2, 3, 4, 5) for b in T.bl4(sec, k) for x in N.urls(b)]
    sl = N.src_links([x for x in u if 'jaredgibbons.ca' not in x], skip=('age-restriction-bylaws', 'changes-to-legislation', 'alr-maps', 'housing-in-the-alr', 'gi-003', 'Apply-for-farm', 'ib_09', 'Classification_of_Land'))
    if sl: bl += [H(f'Sources for the acreage notes on {name}', 3), LK(sl[:12])]
    faq = []
    for b in T.bl4(sec, 4):
        m = re.match(r'\*\*Q:\s*(.*?)\*\*\s*(.*)', b)
        if not m: continue
        q = m.group(1).strip(); a = tidy(m.group(2))
        if T.qkey(q) in qshared or N.FQ_BAD.search(q) or re.search(r'stats|market stat|how many|median|sold|PTT|GST|foreclos|hold a lot|outbid|redemption', q, re.I) or len(a) < 60 or META.search(q) or re.search(r'\bpage\b|\bfile\b|quota|board', q, re.I) or META.search(a) or re.search(r'Bulletin 09|SPA s\.239|500 m²|ALR|SSMUH|farm class', q + a, re.I) and re.search(r'ALR|SSMUH|farm class|farm classification|residence|stratif', q, re.I): continue
        faq.append({'gen': G, 'q': q, 'a': a})
    return bl, faq[:4]


def hub():
    src = lambda *ks: [u for k in ks for u in [k]]
    ALC = 'https://www.alc.gov.bc.ca/use-of-alr-land/housing-in-the-alr/'; MAPS = 'https://www.alc.gov.bc.ca/alr-maps'
    IB9 = 'https://www.alc.gov.bc.ca/assets/alc/assets/legislation-and-regulation/information-bulletins/ib_09_subdivision_and_plans_that_cause_subdivision.pdf'
    FC = 'https://info.bcassessment.ca/Services-products/property-classes-and-exemptions/farm-land-assessment/farm-classification-in-british-columbia/Apply-for-farm-classification'
    REG = 'https://info.bcassessment.ca/about/Shared%20Documents/Classification_of_Land_as_a_Farm_Regulation.pdf'
    GST = 'https://www.canada.ca/en/revenue-agency/services/forms-publications/publications/gi-003/sales-vacant-land-individuals.html'
    TOL = 'https://www.tol.ca/en/the-township/small-scale-multi-unit-housing.aspx'
    bl = [{'t': 'notice', 'text': "Draft for Jared's approval. Built from the Agricultural Land Commission, BC Assessment and Canada Revenue Agency pages named under Sources, read November 1, 2026. Not legal or tax advice.", 'gen': G},
          {**N.P('These BC rules apply to every acreage, farm and rural-land purchase on this site, whichever area it is in. They are written once here; each area page covers only what is specific to that area.'), 'gen': G}, {'t': 'grid', 'gen': G},
          {**N.H('First question: is the parcel in the Agricultural Land Reserve?', 2), 'gen': G},
          {**N.P('Being in an area does not settle it. Whether a parcel is in the ALR is decided parcel by parcel, and the Agricultural Land Commission publishes ALR maps for checking before you write an offer. If the parcel is in the reserve, the rules below apply to it. If it is not, the municipal zoning bylaw is what governs the land.'), 'gen': G},
          {**N.H('How many homes you can have on ALR land', 2), 'gen': G},
          {**N.P('The Commission’s housing rules say ALR land may generally have no more than one residence per parcel unless the parcel qualifies for an additional one, and a local government can restrict residences further through zoning. A principal residence must have a total floor area of 500 m² or less, and no more than 1,000 m² of fill, including structural aggregate for foundations and driveways, can be placed to build it. A secondary suite is allowed only inside the principal residence. One additional residence, detached from the principal one, is allowed up to 90 m² on a property of 40 hectares or less, or up to 186 m² on a property over 40 hectares. A larger home, or more homes than that, needs the Commission’s approval.'), 'gen': G},
          {**N.H('Subdividing or stratifying ALR land', 2), 'gen': G},
          {**N.P('Subdividing land in the ALR requires the Agricultural Land Commission’s approval, and depositing a strata plan counts as a subdivision. So ALR residences cannot be stratified without the Commission’s permission (ALC Information Bulletin 09 s.6, Strata Property Act s.239, Agricultural Land Commission Act s.21(1)). That is a permission rule, not an absolute ban, but price an ALR parcel as one parcel unless that permission exists. A bare-land strata lot is strata tenure, with Form B, fees and bylaws, and is the opposite of a fee-simple acreage purchase.'), 'gen': G},
          {**N.H('Farm class and what it takes to keep it', 2), 'gen': G},
          {**N.P('BC Assessment’s farm classification lowers the property tax on land that is genuinely farmed, and it depends on farm income, not on how a listing describes the land. The minimum gross income at farm-gate prices is $2,500 if the farm operation is between 0.8 ha (1.98 acres) and 4 ha (10 acres); $2,500 plus 5% of the actual value of the area over 4 ha if the operation is larger than 4 ha; and $10,000 if it is under 0.8 ha. A new application must be submitted by October 31 to count for the next assessment and tax year. A buyer who plans to keep farming a farm-classified property submits a General Application for Farm Classification by October 31. BC Assessment removes the classification if a property stops meeting the requirements or the owner does not provide the supporting information it asks for.'), 'gen': G},
          {**N.H('GST on farm land and vacant land', 2), 'gen': G},
          {**N.P('Canada Revenue Agency Info Sheet GI-003 says most sales of vacant land by individuals are exempt, with personal-use land as the example. An individual’s sale can still be taxable where the land is capital property used mainly in a business, is sold in the course of a business, or is a subdivided parcel of more than two parts. Farmland is the caution: the CRA treats sales of farmland by individuals in a separate info sheet and generally as taxable, with limited exemptions, including certain transfers to a related person for personal use. For a working farm the land, barns, quota and residence can each carry a different GST position, so the contract should state it and the vendor’s status should be confirmed before subjects come off.'), 'gen': G},
          {**N.H('Small-scale multi-unit housing rarely applies to acreage', 2), 'gen': G},
          {**N.P('The province’s small-scale multi-unit housing rules are written for serviced urban lots. As one example, the Township of Langley’s bylaw (Bylaw 6020, adopted November 18, 2024) allows 3 or 4 units only on lots of 4,050 m² or smaller that are inside the Urban Containment Boundary and on municipal water and sewer, so most acreages fail on size and servicing alone. Every municipality has its own bylaw, so confirm what the zone allows for a second home, a shop or a suite before pricing any plan around extra units.'), 'gen': G},
          {**N.H('Wells, septic and what to test before removing subjects', 2), 'gen': G},
          {**N.P('Rural parcels are often on a well and a septic field rather than city water and sewer. Before removing subjects, test the well’s flow and water quality, have the septic system inspected, confirm the permits for outbuildings, suites and shops, and ask the municipality what the zone allows. Whether any given property is serviced is unconfirmed until those checks are done.'), 'gen': G},
          {**N.H('Flood, drainage and farm-business items', 2), 'gen': G},
          {**N.P('Much of the Fraser Valley’s best farmland sits on a floodplain behind dikes, so ask the municipality about dike, drainage and floodplain status for the specific parcel. Quota, barn standards and marketing-board rules for poultry, egg or other supply-managed operations are not covered by a verified source here; confirm them with the relevant marketing board and the vendor.'), 'gen': G}]
    sl = N.src_links([ALC, MAPS, IB9, FC, REG, GST, TOL])
    links = [('BC land buying rules', '/bc-land-buying-rules.html'), ('Farms for sale', '/farms.html'), ('Fraser Valley acreages for sale', '/fraser-valley-acreages-for-sale.html'), ('Buying a chicken farm in BC', '/buying-a-chicken-farm-bc.html'),
             ('Home evaluation', '/home-evaluation.html'), ('Mortgage calculator', '/mortgage-calculator.html'), ('Data and methodology', '/data-and-methodology.html'), ('Contact Jared', '/contact.html')]
    links = [(a, h) for a, h in links if T.exists(h[1:-5])]
    bl += [{**N.H('Sources', 2), 'gen': G}, {**N.LK(sl), 'gen': G}, {**N.H('More real estate', 2), 'gen': G, 'pos': 'end'}, {**N.LK(links), 'gen': G, 'pos': 'end'}]
    faq = [{'q': 'Is this parcel in the ALR, and what changes if it is?', 'a': 'ALR status is decided parcel by parcel, so check the Agricultural Land Commission’s ALR maps before writing an offer. If it is in the reserve, residences are limited (generally one principal residence of 500 m² or less, plus the additional-residence allowance), subdividing or stratifying needs the Commission’s approval, and local zoning applies on top.'},
           {'q': 'How many homes can I build on an ALR acreage?', 'a': 'Generally one principal residence of 500 m² or less (with no more than 1,000 m² of fill), a secondary suite only inside that residence, and one additional detached residence of up to 90 m² on properties of 40 ha or less, or up to 186 m² on properties over 40 ha. More or larger needs ALC approval, and local bylaws may be stricter.'},
           {'q': 'Can I stratify or subdivide an ALR acreage to sell pieces of it?', 'a': 'Only with the Agricultural Land Commission’s permission. Depositing a strata plan is a subdivision, and subdivision in the ALR requires Commission approval or must fall under the ALR General Regulation. Price the land as one parcel unless that permission exists.'},
           {'q': 'What farm income does a parcel need to keep farm class?', 'a': 'At farm-gate prices: $2,500 if the farm operation is 0.8 to 4 hectares; $2,500 plus 5% of the actual value of the area over 4 hectares if it is larger; and $10,000 if it is under 0.8 hectares. Applications to BC Assessment are due by October 31, including from a new owner who will keep farming.'},
           {'q': 'Will GST apply when I buy farmland or vacant land?', 'a': 'It depends on the seller and the land. Most sales of vacant land by individuals are exempt under CRA Info Sheet GI-003, but farmland is treated separately and is usually taxable with limited exemptions, and business or subdivided-parcel sales can be taxable. Have the contract state the GST position.'}]
    d = {'status': 'draft', 'slug': HUB, 'updated': '2026-11-02', 'acre_page': True, 'hand_edited': True, 'blocks': bl, 'faq': faq, 'faq_heading': 'BC acreage buying: your questions answered',
         'new_page': {'title': 'BC Acreage Buying Rules: ALR, Farm Class and GST | Jared Gibbons', 'description': 'BC acreage and farm buying rules: Agricultural Land Reserve limits, subdividing, farm class, GST on farmland, wells and septic, with sources. Jared Gibbons, REALTOR®.'[:158],
                      'h1': 'BC Acreage Buying Rules: ALR, Farm Class and GST'},
         'breadcrumbs': [{'name': 'Home', 'href': '/index.html'}, {'name': 'BC Acreage Buying Rules', 'href': f'/{HUB}.html'}], 'needs_from_muse': ['Jared’s review of the wording']}
    T.save(HUB, d)


def main():
    notes = loadnotes()
    # strip our old blocks everywhere
    for p in glob.glob(f'{LOCAL}/*.json'):
        j = json.load(open(p, encoding='utf-8'))
        if any(b.get('gen') == G for b in j.get('blocks', [])) or any(f.get('gen') == G for f in j.get('faq', [])):
            j['blocks'] = [b for b in j['blocks'] if b.get('gen') != G]; j['faq'] = [f for f in j.get('faq', []) if f.get('gen') != G]; T.save(os.path.basename(p)[:-5], j)
    # questions that repeat across the rural notes are answered once, on the rules page
    cq = collections.Counter()
    for n in notes.values():
        for b in T.bl4(n['sec'], 4):
            m = re.match(r'\*\*Q:\s*(.*?)\*\*', b)
            if m: cq[T.qkey(m.group(1))] += 1
    qshared = {k for k, c in cq.items() if c >= 4}
    # text already published elsewhere on the site is not repeated (first 70 characters)
    seen = set()
    for pth in glob.glob(f'{LOCAL}/*.json'):
        for b in json.load(open(pth, encoding='utf-8')).get('blocks', []):
            if b.get('t') == 'list':
                for it in b['items']: seen.add(it[0].get('t', '')[:70])
    tg = collections.defaultdict(list); skipped = []
    for x, n in sorted(notes.items()):
        t = target(x)
        if not t: skipped.append(x); continue
        tg[t].append(n)
    wrote = 0; links_in = collections.defaultdict(list)
    for t, ns in sorted(tg.items()):
        j = T.load(t); bl = []; faq = []
        for n in sorted(ns, key=lambda n: n['x']):
            b, f = section(n, seen, qshared); bl += b; faq += f
        for b in bl:
            if b['t'] == 'list': b['items'] = [i for i in b['items'] if i[0].get('h') or (len(i[0]['t']) >= 25 and not i[0]['t'].lower().startswith('none'))]
        bl = [b for b in bl if not (b['t'] == 'list' and not b['items'])]
        bl = [b for i, b in enumerate(bl) if not (b['t'] == 'h' and b['level'] >= 3 and (i + 1 == len(bl) or bl[i + 1]['t'] == 'h') and 'Sources' not in b['text'])]
        if sum(1 for b in bl if b['t'] == 'list' and b['items'] and 'acreage buying rules' not in b['items'][0][0]['t'].lower() and not b['items'][0][0].get('h')) < 1 and sum(len(b.get('text', '')) for b in bl if b['t'] == 'p') < 500:
            skipped.append(t); continue
        if len(bl) < 5: skipped.append(t); continue
        j['blocks'] = j.get('blocks', []) + bl
        have = {T.qkey(x['q']) for x in j.get('faq', [])}
        j['faq'] = j.get('faq', []) + [x for x in faq if T.qkey(x['q']) not in have][:6]
        j.setdefault('slug', t); T.save(t, j); wrote += 1
    hub()
    # the land rules page and the Fraser Valley acreage page point at the new rules page
    for s, lab in (('bc-land-buying-rules', 'BC acreage buying rules'), ('fraser-valley-acreages-for-sale', 'BC acreage buying rules')):
        if T.exists(s):
            j = T.load(s)
            j['blocks'] = j.get('blocks', []) + [{**N.H('Buying acreage or farm land?', 2), 'gen': G, 'pos': 'end'}, {**N.P('The Agricultural Land Reserve, farm class and GST on farm land are explained on their own page.'), 'gen': G, 'pos': 'end'}, {**N.LK([(lab, f'/{HUB}.html')]), 'gen': G, 'pos': 'end'}]
            T.save(s, j)
    print('acreage sections on', wrote, 'pages; notes', len(notes), 'skipped', len(skipped), skipped)


if __name__ == '__main__':
    main()
