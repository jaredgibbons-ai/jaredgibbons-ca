"""Mobile and manufactured-home sections from Jared's verified notes (docs/research/local-notes-mobile-homes/*.md, researched 2026-11-01/02),
plus the shared page /bc-mobile-home-buying-rules.

The program wrote a note for every research slug (503); most say the area has no manufactured-home park, co-op or own-land community. Those get no page and no section.
Only the notes in MOBILE below, which hold the verified parks and communities (the program summary's roster by tenure form) and the mobile-home topic pages, are published.
Park and tenancy rules that every note repeats (the MHPTA block, the Registry, pad-rent caps, property tax, PTT/GST) are written once on the rules page and left out of the area sections.
Board counts, listing-feed snapshots, MLS numbers and pad-rent dollar figures are not published.   python3 -I tools/build_mobilehomes.py      (after build_acreages.py)"""
import collections, glob, importlib.util, json, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
HERE = os.path.dirname(os.path.abspath(__file__))
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
B = _load('acre', 'build_acreages.py'); T = B.T; N = B.N; LOCAL = N.LOCAL
NOTES = os.path.join(ROOT, 'docs/research/local-notes-mobile-homes'); G = 'mh'; HUB = 'bc-mobile-home-buying-rules'; SFX = '-mobile-homes-2026-11-01.md'
MOBILE = set("""abbotsford-mobile-homes surrey-mobile-homes south-surrey-mobile-homes chilliwack-mobile-homes maple-ridge-mobile-homes mission-mobile-homes langley-mobile-homes langley-mobile-home-communities
mobile-home-parks-fraser-valley cost-of-mobile-home-pad-rental-fees-in-langley cheap-mobile-homes-langley-under-500k how-to-buy-a-mobile-home-in-bc-guide
abbotsford-west abbotsford-east central-abbotsford poplar west-chilliwack east-central southwest-maple-ridge coquitlam-west fleetwood-tynehead queen-mary-park-surrey brookswood otter-district
mission-homes-for-sale cityofmission rosedale-homes-for-sale lindell-beach aldergrove-guide central-meadows-pitt-meadows nordel neilsen-grove sumas-mountain tsawwassen-east little-mountain lake-errock
bridal-falls-guide cultus-lake-south cultus-lake-east cultus-lake-north west-newton holly fairfield-island steelhead northeast""".split())
LEAD_DROP = re.compile(r'Home-as-chattel|Financing|Park rules|Pad-rent|Property tax|Park-owner consent|PTT|First-home|Assignment|MHPTA|Foreclosure|GST|Strata-form|Park closure|SSMUH|Directory|Secondary forms|Excluded|Cross-?ref|Candidate|Tenure record|Checked|Settled|Counts?\b|Market|Registry|Short-term|Speculation|Federal|Pad ground|Sibling|Servicing|Subdivision', re.I)
SKIPHEAD = re.compile(r'Cross|Candidate|Tenure record|Checked|rest of the ground|Excluded|roster|research|sibling|No park|No pad|No verified|None', re.I)


META2 = re.compile(r"\b(research|batch|slug|files?|siblings?|program|queued?|roster|counted|counts?|cross-?referenced?|this (topic|page)|home ground|never (re-)?count\w*|documented (at )?home|at home here|directory counts?)\b|NEITHER definition|commissioning|standing correction|do not import|\$\d[\d,]*\s*(/|per) ?month|listing-stated|\$\d[\d,]*\s+pad rent|pad rent\b[^.]{0,40}\$\d|appears a year apart|unverified|unconfirmed|backlog|locator|retry", re.I)
CAPS = {'THE TENURE LINE': 'The tenure line', 'RENTED PAD': 'rented pad', 'OWN-LAND': 'own-land', 'UNRESOLVED': 'unresolved', 'PAD RENTAL': 'pad rental', 'BARE-LAND STRATA': 'bare-land strata', 'TENURE RECORD ONLY': 'a tenure record only', 'TENURE RECORDS': 'tenure records', 'OPEN': 'open', 'CONFLICT': 'conflict', 'LISTING-STATED': 'listing-stated', 'DUAL BASIS': 'dual basis', 'FREEHOLD STRATA': 'freehold strata', 'FREEHOLD': 'freehold'}


def tidy2(s):
    s = N.clean(s)
    s = ' '.join(x for x in B.sents(s) if not B.SENT_DROP.search(x) and not META2.search(x))
    for a, b in CAPS.items(): s = re.sub(rf'\b{a}\b', b, s)
    s = re.sub(r'\bUNVERIFIED\b|\bUNCONFIRMED\b', 'unconfirmed', s)
    s = re.sub(r'\s*\((?:Sections?) [^)]*$', '', s)
    return re.sub(r'\s+', ' ', s).strip()


def J2(b):
    nm, rest = N.split_bold(b)
    if nm is None: return tidy2(b)
    nm, rest = re.sub(r'[\s—–:.-]+$', '', N.clean(nm)), tidy2(rest)
    if not rest or len(rest) < 30 or rest[:1] in '(;,': return ''
    if ' — ' in nm and len(nm) > 38: nm = nm.split(' — ')[0].strip()
    for a, c in CAPS.items(): nm = re.sub(rf'\b{a}\b', c, nm)
    if not nm or META2.search(nm) or B.SENT_DROP.search(nm): return rest
    return f'{nm}: {rest}'


def good2(s): return len(s) >= 50 and s.count('(') == s.count(')') and not s[:1].islower() and not re.search(r'unconfirmed', s[:60], re.I) and not re.match(r'(No |None|Zero)', s)


def H(t, l=2): return {**N.H(t, l), 'gen': G, 'pos': 'end'}
def P(t): return {**N.P(t), 'gen': G, 'pos': 'end'}
def LI(items): return {**N.LI(items), 'gen': G, 'pos': 'end'}
def LK(items): return {**N.LK(items), 'gen': G, 'pos': 'end'}


def loadnotes():
    notes = {}
    for f in sorted(glob.glob(f'{NOTES}/*{SFX}')):
        x = os.path.basename(f)[:-len(SFX)]; base = re.sub(r'-guide$', '', x)
        if base not in MOBILE and x not in MOBILE: continue
        title, pre, sec = T.parse_note(f, 'lots-and-land'); t = open(f, encoding='utf-8').read()
        m = re.search(r'## 2\..*?\n(.*?)\n## 3', t, re.S); intro = ''; s2 = []
        if m:
            cur = ''
            for ln in m.group(1).split('\n'):
                h = re.match(r'### (.*)', ln)
                if h: cur = h.group(1); continue
                if ln.strip() and not ln.startswith('- ') and not intro: intro = ln.strip()
                if ln.startswith('- **') and not SKIPHEAD.search(cur): s2.append(ln[2:])
        n = dict(x=base, path=f, title=title, sec=sec, intro=intro, s2=s2, size=len(t))
        if base not in notes or n['size'] > notes[base]['size']: notes[base] = n
    return notes


def target(x):
    if 'mobile-home' in x and T.exists(x): return x
    if x.endswith('-guide') and T.exists(x): return x
    ng = B.newguide(x)
    if ng: return ng
    for c in (T.ALIAS.get(x), x):
        if c and T.exists(c + '-guide') and (c + '-guide' in T.MAPPED or c in T.COMM): return c + '-guide'
        if c and T.exists(c) and c in T.COMM: return c
    for c in (T.ALIAS.get(x), x):
        if c and T.exists(c + '-guide'): return c + '-guide'
        if c and T.exists(c): return c
    return None


def section(n, seen, shared_b, shared_q):
    sec = n['sec']; area = n['title'].split(' — ')[0].strip(); name = re.sub(r'\s*\(.*?\)', '', area).split(',')[0].strip()
    name = re.sub(r'\s*(Mobile( and| &)? Manufactured Homes|Mobile Homes)\s*$', '', name).strip() or area
    topic = 'mobile-home' in n['x']
    bl = [H(f'{name}: how mobile and manufactured homes work here' if topic else f'Mobile and manufactured homes in {name}')]
    isn = [x for x in B.sents(tidy2(re.sub(r'^\*\*(.*?)\*\*', r'\1', n['intro']))) if len(x) > 50 and not re.search(r'tenure records', x, re.I)]
    if isn: bl.append(P(' '.join(isn[:3])))
    def fresh(xs):
        out = []
        for x in xs:
            if x and good2(x) and not LEAD_DROP.match(x) and x[:70] not in seen: seen.add(x[:70]); out.append(x)
        return out
    ground = fresh([J2(b) for b in n['s2'] if N.real(b) and not LEAD_DROP.search(N.split_bold(b)[0] or '')])
    if ground: bl += [H('The parks and communities' if not topic else 'The parks and the homes', 3), LI(ground)]
    s1 = fresh([J2(b) for b in T.bl4(sec, 1) if N.real(b) and not LEAD_DROP.search(N.split_bold(b)[0] or '')])
    if s1: bl += [H('Scope and area context' if topic else f'Streets, schools and getting around {name}', 3), LI(s1)]
    s3 = fresh([J2(b) for b in T.bl4(sec, 3) if N.real(b) and T.key(b) not in shared_b and not LEAD_DROP.search(N.split_bold(b)[0] or '')])
    if s3: bl += [H('Local rules that affect park-home buyers' if topic else f'Local rules that affect park-home buyers in {name}', 3), LI(s3)]
    s5 = fresh([J2(b) for b in T.bl4(sec, 5) if N.real(b) and not LEAD_DROP.search(N.split_bold(b)[0] or '')])
    if s5: bl += [H('Good to know' if topic else f'Good to know about {name}', 3), LI(s5)]
    bl.append(P('The BC rules for buying a home in a park (the pad tenancy, park-owner consent, pad-rent caps, the Manufactured Home Registry and park closures) are explained once, with sources, on the page linked below.'))
    bl.append(LK([('BC mobile home buying rules', f'/{HUB}.html')]))
    u = [x for k in (1, 2, 3, 4, 5) for b in T.bl4(sec, k) for x in N.urls(b)] + [x for b in n['s2'] for x in N.urls(b)]
    sl = N.src_links([x for x in u if 'jaredgibbons.ca' not in x], skip=('manufactured-homes', 'manufactured-home-registry', 'rtb10', 'age-restriction', 'annual-property-tax', '481_2003', '161_2000', '168_2009', 'depreciation', 'home-owner-grant'))
    if sl: bl += [H(f'Sources for the mobile-home notes on {name}', 3), LK(sl[:12])]
    faq = []
    for b in T.bl4(sec, 4):
        m = re.match(r'\*\*Q:\s*(.*?)\*\*\s*(.*)', b)
        if not m: continue
        q = m.group(1).strip(); a = tidy2(m.group(2))
        if T.qkey(q) in shared_q or N.FQ_BAD.search(q) or META2.search(q) or META2.search(a) or len(a) < 60 or re.search(r'\bpage\b|\bfile\b|stats|median|how many|sold|PTT|GST|foreclos|rent increase|10-day|consent|registry|closure|Form 10', q, re.I): continue
        faq.append({'gen': G, 'q': q, 'a': a})
    return bl, faq[:4]


def hub():
    U = lambda p: 'https://www2.gov.bc.ca/gov/content/housing-tenancy/residential-tenancies/manufactured-homes/' + p
    srcs = [U('manufactured-home-tenancy'), U('starting-tenancy-manufactured-homes'), U('rent-increases-for-manufactured-homes'), U('end-tenancy-manufactured-homes'), 'https://www2.gov.bc.ca/assets/gov/housing-and-tenancy/residential-tenancies/forms/rtb10.pdf',
            'https://www2.gov.bc.ca/assets/gov/housing-and-tenancy/residential-tenancies/information-sheets/assigment_of_mhp_tenancy_agreements.pdf', 'https://www2.gov.bc.ca/gov/content/housing-tenancy/owning-a-home/manufactured-home-registry',
            'https://www2.gov.bc.ca/gov/content/taxes/property-taxes/annual-property-tax/manufactured-home', 'https://www.gov.bc.ca/gov/content/taxes/property-taxes/annual-property-tax/home-owner-grant',
            'https://www2.gov.bc.ca/gov/content/housing-tenancy/strata-housing/operating-a-strata/bylaws-and-rules/age-restriction-bylaws', 'https://www.alc.gov.bc.ca/assets/alc/assets/legislation-and-regulation/policies/alc_-_policy_l-25_-_manufactured_homes_in_the_alr.pdf']
    s = lambda t: {**N.P(t), 'gen': G}; h = lambda t: {**N.H(t, 2), 'gen': G}
    bl = [{'t': 'notice', 'text': "Draft for Jared's approval. Built from the Residential Tenancy Branch, Manufactured Home Registry, BC Assessment and strata pages named under Sources, read November 1, 2026. Not legal advice.", 'gen': G},
          s('These BC rules apply to every manufactured-home or park-home purchase on this site, whichever area it is in. They are written once here; each area page covers only the parks and communities specific to that area.'), {'t': 'grid', 'gen': G},
          h('What you actually buy in a park: the home, not the land'),
          s('In a manufactured-home park the buyer owns the home as a chattel, a piece of personal property, and rents the pad it sits on. The buyer does not own the land. The Manufactured Home Park Tenancy Act (MHPTA) governs the pad tenancy. Other forms exist and work differently: a bare-land strata community, where the buyer owns the home and a strata lot and pays strata fees instead of pad rent; a co-operative, where you buy a share or membership; and a home on your own fee-simple land.'),
          h('Registering the sale and the CSA label'),
          s('In BC the sale, transfer or purchase of a manufactured home is only effective if it is registered with the Manufactured Home Registry, which keeps the central record of ownership, controls moves and gives lenders security. A home cannot be sold unless it carries its original CSA label. If the label is missing, the home must be re-certified, and Technical Safety BC has a licensed electrical contractor inspect it. A permit to move a home is issued by the Registry, a tax certificate for transport is required (except for a move to another pad in the same park), and the permit expires 30 days after it is issued.'),
          h('Buying in a park is an assignment, with the park owner’s consent'),
          s('Under section 28 of the MHPTA, a pad tenancy is transferred to the buyer by assignment. It needs the park owner’s prior written consent, a director’s order, or authority in the tenancy agreement. The seller asks for consent on RTB Form 10. The park owner has until the tenth day after receiving the request to respond; silence by the end of the tenth day is deemed consent, and no fee may be charged for it. Before asking, the seller must give the buyer written copies of the park rules and the relevant parts of the tenancy agreement. The buyer then becomes the tenant on the same terms, and the pad rent and the date of the next increase stay the same.'),
          h('Park rules and 55+ parks'),
          s('Park rules are part of the tenancy. A landlord can change them once a year with three full months’ notice, and a rule is enforceable only if it applies to every tenant fairly, is clear, is properly noticed and does not change a material term of the tenancy agreement. A park where every pad is reserved for tenants aged 55 or older has its own footing under section 10(2)(b)(i) of the Human Rights Code, and the park owner can refuse an assignment if no buyer meets the age requirement. That age rule is a park designation, not a strata bylaw. A 45+ rule is not a 55+ product.'),
          h('Pad-rent increases are capped'),
          s('Pad rent can go up once every 12 months, on at least three full months’ notice, by no more than the inflation rate (BC all-items CPI, 12-month average) plus a proportional amount for changes in local-government levies and regulated park utilities, divided by the number of sites in the park. The Residential Tenancy Branch states the cap as 2.3% plus the proportional amount for 2026 and 2.2% plus the proportional amount for 2027 (read November 1, 2026). Ask any park for its current pad rent in writing.'),
          h('Property tax and the Home Owner Grant'),
          s('The owner of a manufactured home is assessed and taxed like other residential owners, but the assessed value does not include the land when the home sits in a park that is not on reserve land, or on land someone else owns. A home that is the registered owner’s principal residence can qualify for the Home Owner Grant, applied for each year.'),
          h('Park closures and conversions'),
          s('A landlord converting all or a significant part of a park to a non-residential use, or to a residential use other than a manufactured-home park, must have all the necessary government permits and approvals in place before giving notice. The notice is 12 months, and the tenant must be paid $20,000 on or before the notice’s effective date. A tenant can move out early on at least 10 days’ written notice, and has 15 days to dispute the notice. The provincial pages describe further compensation routes in some cases; read them for the details.'),
          h('Property transfer tax, GST and first-home programs'),
          s('The one property transfer tax point the Province states for manufactured homes is that the newly built home exemption includes a manufactured home placed and affixed on a parcel of vacant land and not previously occupied. That helps a buyer placing a new home on their own land, not one buying a resale home on a rented pad. For a resale home the property transfer tax treatment is unconfirmed as a flat rule, and the GST position for a specific home depends on the vendor and the home, so the contract should state it. The first-time home buyers’ GST rebate is for new housing, and a resale park home is not new housing.'),
          h('Financing'),
          s('Lenders treat a chattel home on a rented pad differently from a home on land you own. Lender and insurer rules on age and foundation for manufactured homes are not set out in an official source here, so confirm the lender’s terms for the specific home before removing subjects.'),
          h('Bare-land strata communities'),
          s('Where the community is a bare-land strata, the strata rules apply. Ask for the Form B, which the strata must provide within 7 days of a request (maximum $35 plus up to 25¢ per page). Depreciation reports run on a five-year cycle for stratas with five or more lots, and the minimum contingency-reserve contribution is 10%. Rental-restriction bylaws have been void since November 24, 2022, and only age bylaws for 55+ are valid.'),
          h('Court-ordered sales'),
          s('Court-ordered sales follow the Supreme Court process (Rules 21-7 and 13-5, Practice Direction PD-66, Form 60). How Form B, property transfer tax and GST work for a specific park-home court sale is unconfirmed.')]
    sl = N.src_links(srcs)
    links = [(a, h2) for a, h2 in [('How to buy a mobile home in BC', '/how-to-buy-a-mobile-home-in-bc-guide.html'), ('Mobile home parks in the Fraser Valley', '/mobile-home-parks-fraser-valley.html'), ('BC 55+ strata rules', '/bc-55-plus-strata-rules.html'),
             ('Cost of pad rental in Langley', '/cost-of-mobile-home-pad-rental-fees-in-langley.html'), ('Mortgage calculator', '/mortgage-calculator.html'), ('Home evaluation', '/home-evaluation.html'), ('Data and methodology', '/data-and-methodology.html'), ('Contact Jared', '/contact.html')] if T.exists(h2[1:-5])]
    bl += [{**N.H('Sources', 2), 'gen': G}, {**N.LK(sl), 'gen': G}, {**N.H('More real estate', 2), 'gen': G, 'pos': 'end'}, {**N.LK(links), 'gen': G, 'pos': 'end'}]
    faq = [{'q': 'Do I own the land when I buy a mobile home in a park?', 'a': 'No. In a manufactured-home park you own the home as personal property and rent the pad. Only bare-land strata communities, co-operatives (as a share) and homes on your own land involve owning or holding an interest in the land.'},
           {'q': 'Can the park refuse a buyer?', 'a': 'The seller needs the park owner’s prior written consent to assign the tenancy, requested on RTB Form 10. The owner must reply by the tenth day, silence is deemed consent, and no fee can be charged. In a designated 55+ park the owner can refuse a buyer who does not meet the age requirement.'},
           {'q': 'How much can pad rent go up?', 'a': 'Once every 12 months on three full months’ notice, by no more than inflation plus a proportional amount for local-government levies and regulated utilities. The Residential Tenancy Branch states 2.3% plus that amount for 2026 and 2.2% plus that amount for 2027.'},
           {'q': 'What happens if the park closes?', 'a': 'The landlord needs all government permits first, then must give 12 months’ notice and pay the tenant $20,000 by the notice’s effective date. The tenant can leave early on 10 days’ notice and has 15 days to dispute.'},
           {'q': 'Do I pay property transfer tax on a mobile home in a park?', 'a': 'It is unconfirmed as a flat rule for a resale home on a rented pad. The Province states that the newly built home exemption includes a manufactured home placed and affixed on vacant land that has not been occupied. Have your lawyer confirm for the specific sale.'},
           {'q': 'Is a manufactured home registered?', 'a': 'Yes. The sale is only effective if registered with the Manufactured Home Registry, and the home needs its original CSA label to be sold.'}]
    d = {'status': 'draft', 'slug': HUB, 'updated': '2026-11-02', 'mh_page': True, 'hand_edited': True, 'blocks': bl, 'faq': faq, 'faq_heading': 'BC mobile home buying: your questions answered',
         'new_page': {'title': 'BC Mobile Home Buying Rules: Pad Rent and Registry | Jared Gibbons', 'description': 'BC mobile and manufactured home buying rules: pad tenancy, park-owner consent, pad-rent caps, the Registry, park closures and strata forms, with sources. Jared Gibbons, REALTOR®.'[:158],
                      'h1': 'BC Mobile Home Buying Rules: Pad Rent, Consent and the Registry'},
         'breadcrumbs': [{'name': 'Home', 'href': '/'}, {'name': 'BC Mobile Home Buying Rules', 'href': f'/{HUB}.html'}], 'needs_from_muse': ['Jared’s review of the wording']}
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
        t = target(x)
        if not t: skipped.append(x); continue
        tg[t].append(n)
    wrote = 0
    for t, ns in sorted(tg.items()):
        j = T.load(t); bl = []; faq = []
        for n in sorted(ns, key=lambda n: n['x']):
            b, f = section(n, seen, shared_b, shared_q); bl += b; faq += f
        for b in bl:
            if b['t'] == 'list': b['items'] = [i for i in b['items'] if i[0].get('h') or (len(i[0]['t']) >= 25 and not i[0]['t'].lower().startswith('none'))]
        bl = [b for b in bl if not (b['t'] == 'list' and not b['items'])]
        bl = [b for i, b in enumerate(bl) if not (b['t'] == 'h' and b['level'] >= 3 and (i + 1 == len(bl) or bl[i + 1]['t'] == 'h') and 'Sources' not in b['text'])]
        body = sum(1 for b in bl if b['t'] == 'list' and b['items'] and not b['items'][0][0].get('h'))
        if body < 1: skipped.append(t); continue
        j['blocks'] = j.get('blocks', []) + bl
        have = {T.qkey(x['q']) for x in j.get('faq', [])}
        j['faq'] = j.get('faq', []) + [x for x in faq if T.qkey(x['q']) not in have][:6]
        j.setdefault('slug', t); T.save(t, j); wrote += 1
    hub()
    for s in ('how-to-buy-a-mobile-home-in-bc-guide', 'mobile-home-parks-fraser-valley', 'bc-55-plus-strata-rules'):
        if T.exists(s):
            j = T.load(s)
            j['blocks'] = j.get('blocks', []) + [{**N.H('The rules for buying in a park', 2), 'gen': G, 'pos': 'end'}, {**N.P('Pad tenancy, park-owner consent, pad-rent caps and the Manufactured Home Registry are explained on their own page.'), 'gen': G, 'pos': 'end'}, {**N.LK([('BC mobile home buying rules', f'/{HUB}.html')]), 'gen': G, 'pos': 'end'}]
            T.save(s, j)
    print('mobile-home sections on', wrote, 'pages; notes', len(notes), 'skipped', len(skipped), skipped)


if __name__ == '__main__':
    main()
