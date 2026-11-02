"""FAQ sections from Muse's area research workbook (docs/research/muse-area-research-master-2026-11-01.xlsx, tab "7 FAQs").

Rules (Jared, 2026-11-01: Muse is reference only): an answer is used only if it carries no UNVERIFIED / cannot / not-confirmed wording, is under 700
characters, and does not depend on a monthly market number (we compute those ourselves, so they never go stale). Source links in brackets are lifted
out of the answer text into a "Sources" list at the end of the page. Pages that end up with fewer than 3 questions get the honest generic pair below.
Every FAQ written here carries gen:"muse" so a re-run replaces it.        python3 -I tools/build_muse_faq.py
"""
import glob, json, os, re, sys
from urllib.parse import urlparse
import openpyxl
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
EXEMPT = {'testimonials', '404', 'privacy', 'subscribe-to-our-newsletter', 'reviews', 'index', 'blog', 'about', 'thank-you', 'contact', 'unsubscribe', 'terms', 'accessibility'}
import csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trend as TR
import scrub_research_wording as SC
import build_snapstats_layers as L
import build_community_pages as C
AREA = {r['slug']: r['area'] for r in csv.DictReader(open(os.path.join(ROOT, 'docs/research/muse-keywords-2026-11-01.csv'), encoding='utf-8'))}
BAD = re.compile(r'UNVERIFIED|cannot|not confirmed|not published|could not', re.I)
DATED = re.compile(r'as of (January|February|March|April|May|June|July|August|September|October) 20\d\d', re.I)   # market answers are kept only when they say which month they describe
MARKET = re.compile(r'SnapStats|September 2026|August 2026|sales ratio|inventory', re.I)
PAREN = re.compile(r'\s*\((?:https?://[^()]*|[^()]*https?://[^()]*)\)')
URL = re.compile(r'https?://[^\s,;)]+')


BANK = {
 '55+': [("What does 55+ mean for a home in {n}?", "Most 55+ strata communities in BC set an age rule in their bylaws, commonly that at least one resident is 55 or older, and many also limit children and rentals. The rules differ from one building to the next, so read the bylaws and the Form B Information Certificate before you make an offer on a unit in {n}."),
         ("Can I rent out a 55+ unit in {n}?", "Whether a unit can be rented depends on the strata's current bylaws and the provincial rules that apply to them, and many 55+ buildings restrict rentals. Ask for the bylaws and the strata minutes before you buy a unit in {n} as an investment.")],
 'mobile': [("Do I own the land under a mobile home in {n}?", "Usually not. In most parks you own the home and pay monthly pad rent to the park owner, and the tenancy falls under BC's Manufactured Home Park Tenancy Act. Ask for the tenancy agreement, the current pad rent and the park rules before you make an offer."),
            ("Can I get a mortgage on a mobile home in {n}?", "Lenders look at the age of the home, whether it carries a CSA certification label and the terms of the pad tenancy, and some will not finance older homes. Speak to a mortgage broker before you write an offer, not after.")],
 'duplex': [("What kinds of duplex are for sale in {n}?", "A duplex can be one property on a single title, a side-by-side with two separate freehold titles, or a strata duplex where each side is its own strata lot. The type of title changes how it is financed and insured and which rules apply, so confirm it on the title search."),
            ("Can I live in one side of a duplex in {n} and rent the other?", "Often yes, but zoning and, for a strata duplex, the bylaws decide. Check both before you make an offer if renting out the second side is part of your plan.")],
 'penthouse': [("What makes a penthouse different from other condos in {n}?", "A penthouse is a top-floor unit, usually with more floor area, higher ceilings and larger outdoor space than the units below. Strata fees and property taxes usually follow the size, so compare the full monthly cost, not just the price."),
               ("What should I check before buying a penthouse in {n}?", "Read the Form B, the bylaws, the strata minutes and the depreciation report, and ask about roof, balcony and window repairs, since top-floor units are the ones exposed to them.")],
 'farm': [("What is the ALR and does it apply to farms in {n}?", "The Agricultural Land Reserve is farmland protected by the provincial Agricultural Land Commission. Farm use is generally allowed on ALR land, but subdividing, adding homes or using the land for non-farm purposes usually needs approval, so check a property's ALR status before you offer."),
          ("What should I check before buying a farm in {n}?", "Check the ALR status, water source and licences, drainage and flood history, the buildings and any quota or production licences that do or do not transfer with the land. Poultry and egg production in BC are supply-managed, so a sale of the farm does not automatically include quota.")],
 'acreage': [("Can I subdivide an acreage in {n}?", "It depends on the zoning, whether the land is in the Agricultural Land Reserve, servicing and the minimum lot size, and it needs municipal approval. Ask the municipality before you buy with a subdivision in mind."),
             ("Do acreages in {n} have wells and septic?", "Many do. Ask for the well flow test and water quality results, and the septic filing and inspection records, before you remove conditions.")],
 'foreclosure': [("What is a court-ordered sale in {n}?", "It is a sale of a property supervised by the court after a lender has taken legal action, and the sale needs court approval. Offers are usually made subject to that approval, and other buyers can sometimes bid higher at the hearing."),
                 ("Can I put conditions on an offer for a foreclosure in {n}?", "Conditions such as financing or inspection may be limited or not accepted, depending on the lender's and the court's terms. Speak to Jared and your lawyer before you write an offer.")],
 'condo': [("What do strata fees cover on a condo in {n}?", "Strata fees pay for upkeep and insurance of the common property and the contingency reserve fund, and in some buildings heat, hot water or other services. The Form B Information Certificate lists exactly what a unit's fee covers."),
           ("What should I read before buying a condo in {n}?", "The Form B, the bylaws, the last two years of strata minutes, the depreciation report and the contingency reserve fund balance. They show planned repairs, special levies and rules on pets and rentals.")],
 'townhome': [("Are townhomes in {n} freehold or strata?", "Most are strata, either a building strata or a bare-land strata, with monthly fees and bylaws. Some are freehold row homes with no strata. The title search tells you which, and it decides which costs and rules apply."),
              ("What should I check on a townhome in {n}?", "Read the Form B, the bylaws, the strata minutes and the depreciation report, and ask about exterior repairs, pet and rental rules and who looks after the fences, roofs and yards.")],
 'house': [("Can I add a suite or coach house to a house in {n}?", "BC's small-scale multi-unit housing rules allow more homes on many urban lots, but each municipality sets the details and many lots are excluded. Check the lot's zoning with the municipality before you plan a suite or coach house."),
           ("Do I need a home inspection when buying in {n}?", "It is strongly recommended. Make the offer subject to an inspection so a qualified inspector can look at the roof, structure, drainage, electrical and heating before you remove conditions.")],
 'guide': [("How do I find out which school serves an address in {n}?", "School catchments are set by address, so use the school district's catchment locator with the exact address. Catchment lines change, so check before you write an offer."),
           ("Who can help me buy or sell in {n}?", "Jared Gibbons, REALTOR® with Royal LePage Little Oak Realty, works across the Fraser Valley and Metro Vancouver. Call or text 604-928-1361 or use the contact form on this site.")],
}


def bank_kind(s):
    for rx, k in ((r'55-plus', '55+'), (r'mobile', 'mobile'), (r'duplex', 'duplex'), (r'penthouse', 'penthouse'), (r'farm|poultry|egg-|turkey|broiler|chicken', 'farm'), (r'acreage', 'acreage'),
                  (r'foreclos', 'foreclosure'), (r'condos|presale|apartment', 'condo'), (r'townhome', 'townhome'), (r'houses-for-sale|homes-for-sale|homes-under|homes-over', 'house'), (r'guide|neighbourhood', 'guide')):
        if re.search(rx, s): return k
    return None


REGION_NAMES = ['North Vancouver', 'West Vancouver', 'New Westminster', 'Port Coquitlam', 'Port Moody', 'Pitt Meadows', 'Maple Ridge', 'South Surrey', 'White Rock', 'Vancouver', 'Richmond', 'Burnaby', 'Coquitlam', 'Surrey', 'Langley', 'Abbotsford', 'Mission', 'Chilliwack', 'Delta', 'Ladner', 'Tsawwassen', 'Fort Langley', 'Aldergrove', 'Cloverdale']


STOP = {'guide', 'guides', 'homes', 'home', 'for', 'sale', 'houses', 'house', 'condos', 'condo', 'townhomes', 'townhouses', 'townhome', 'farms', 'farm', 'mobile', 'duplexes', 'penthouses', 'acreages', 'acreage',
        'foreclosures', 'court', 'ordered', 'sales', 'under', 'over', 'plus', '55', 'neighbourhood', 'neighbourhoods', 'real', 'estate', 'lots', 'land', 'poultry', 'chicken', 'egg', 'turkey', 'broiler', 'and', 'communities', 'parks', 'bc', 'with', 'coach', 'luxury', 'in', 'a', 'buying', 'court-ordered', 'ocean', 'view', 'waterfront', 'development', 'elementary', 'rural'}
PLACE_FIX = {'southsurrey': 'South Surrey', 'cloverale': 'Cloverdale', 'buying': 'this area', 'mission-mission': 'Mission'}


def place_for(s, title, mapping):
    parts = [p for i, p in enumerate(s.split('-')) if i == 0 or p != s.split('-')[i - 1]]      # drop a repeated word (mission-mission)
    parts = [PLACE_FIX.get(p, p) if p in PLACE_FIX else p for p in parts]
    typed = any(t in STOP or re.fullmatch(r'\d+\w*', t) for t in parts)
    toks = [t for t in parts if t not in STOP and not re.fullmatch(r'\d+\w*', t)]
    if typed:      # slug carries a home type or a price: take the place words only ("abbotsford-homes-over-1-8m" -> Abbotsford)
        if toks: return ' '.join(PLACE_FIX.get(t, t.capitalize()) if t not in ('of', 'and') else t for t in toks)
        return 'BC' if s.endswith('bc') else 'this area'
    if s in AREA: return AREA[s]
    v = mapping.get(s)
    if v and isinstance(v[1], str) and '+' not in v[1]: return v[1]
    return ' '.join(t if t in ('of', 'and') else t.capitalize() for t in parts)


def snap_faqs(slug, mapping, months, disp):
    """Questions computed from the SnapStats line for this page's community or city cut; None when the page is not in the reports."""
    v = mapping.get(slug)
    if not v: return None
    keys = list(months); last, first = keys[-1], keys[0]; mn = L.month_name(last)
    ak = v[0]; area = months[last]['areas'][ak]; board = L.BOARD_NAME[area['board']]; city = C.CITY[ak][0]
    out = []
    if isinstance(v[1], str) and '+' not in v[1]:
        nm = v[1]; guide = slug.endswith('-guide'); S = {t: dict(L.series(months, ak, t, nm)) for t in L.TL}
        act = {t: any((r or {}).get('inventory') or (r or {}).get('sales') for r in S[t].values()) for t in L.TL}
        cur = {t: S[t][last] or {} for t in L.TL}; noun = {'detached': 'houses', 'condo_townhome': 'condos and townhomes'}
        if not any(act.values()): return None
        if not guide:
            out.append((f'How many homes are for sale in {disp}?', f'At the end of {mn} {last[:4]} the {board} figures showed ' + ' and '.join(f'{L.num(cur[t].get("inventory"))} {noun[t]} listed with {L.num(cur[t].get("sales"))} sold in the month' for t in L.TL if act[t]) + f' in {disp}. Those are month-end counts and move daily; ask Jared what is on the market today.'))
            bits = [f'{noun[t]} had a sales ratio of {L.pct(cur[t]["ratio"])}' + (f', {L.kind(cur[t]["ratio"])}' if cur[t].get('inventory', 0) >= 10 else ' on too few listings to read as a market type') for t in L.TL if act[t] and cur[t].get('ratio') is not None]
            if bits: out.append((f'Is {disp} a buyers’ or sellers’ market?', f'In {mn} {last[:4]}, ' + '; '.join(bits) + '. On the reports’ scale under 12% favours buyers, 12% to 20% is balanced and over 20% favours sellers.'))
        else:
            ch = []
            for t in L.TL:
                a, b = (S[t][first] or {}).get('inventory'), cur[t].get('inventory')
                if act[t] and a is not None and b is not None: ch.append(f'{noun[t]} ' + TR.count_move(a, b, L.month_name(first), L.month_name(last)))
            if ch: out.append((f'Are there more or fewer homes for sale in {disp} than in {L.month_name(first)}?', f'In {disp}, listings of ' + '; '.join(ch) + '.'))
            sh = []
            for t in L.TL:
                tot = area[t]['total']
                if act[t] and cur[t].get('inventory') is not None and tot['inventory']: sh.append(f'{100 * cur[t]["inventory"] / tot["inventory"]:.1f}% of the {L.num(tot["inventory"])} {noun[t]} listed in {city}')
            if sh: out.append((f'How big is {disp} compared with the rest of {city}?', f'In {mn} {last[:4]}, {disp} held ' + ' and '.join(sh) + '.'))
            tt = sum((cur[t].get('sales') or 0) for t in L.TL)
            tot_s = ' and '.join(f'{sum((r or {}).get("sales") or 0 for r in S[t].values())} {noun[t]}' for t in L.TL if act[t])
            out.append((f'How many homes sold in {disp} from {L.month_name(first)} to {mn} {last[:4]}?', f'{tot_s} sold in {disp} over those {len(keys)} months.'))
    else:
        t = 'condo_townhome' if '_c' in v[1].split('+')[0] else 'detached'; tot = area[t]['total']; sm = area[t]['summary']; noun = {'detached': 'houses', 'condo_townhome': 'condos and townhomes'}[t]
        out.append((f'How many {noun} are for sale in {city}?', f'At the end of {mn} {last[:4]} the {board} figures showed {L.num(tot["inventory"])} {noun} listed in {city} and {L.num(tot["sales"])} sold in the month, a sales ratio of {L.pct(tot["ratio"])}. Month-end counts move daily; ask Jared what is on the market today.'))
        sp, dm, sl_ = sm.get('Sale Price'), sm.get('Days on Market'), sm.get('Sale to List Price Ratio')
        if sp and sp.get('cur') and sp.get('prev'): out.append((f'What is the reported sale price for {noun} in {city}?', f'The {mn} report gave ${sp["cur"]:,} for {noun} in {city}, against ${sp["prev"]:,} the month before. The reports give one sale-price figure and do not say whether it is an average or a median, so use it for direction, not as a valuation of your own home.'))
        if dm and dm.get('cur') is not None: out.append((f'How long do {noun} take to sell in {city}?', f'The {mn} report showed {dm["cur"]} days on market for {noun} in {city}' + (f' and a sale-to-list price ratio of {sl_["cur"]}%' if sl_ and sl_.get('cur') else '') + (f', against {dm["prev"]} days the month before' if dm.get('prev') is not None else '') + '.'))
    return out


def clean(a):
    urls = [u.rstrip('.,') for p in PAREN.findall(a) for u in URL.findall(p)]
    a = PAREN.sub('', a); a = re.sub(r'\s+([.,;])', r'\1', a); a = re.sub(r'\s{2,}', ' ', a).strip()
    return a, urls


def main():
    wb = openpyxl.load_workbook(os.path.join(ROOT, 'docs/research/muse-area-research-master-2026-11-01.xlsx'), read_only=True, data_only=True)
    muse = {}
    for r in list(wb['7 FAQs'].iter_rows(values_only=True))[1:]:
        items = []
        for c in r[2:]:
            m = re.match(r'Q:\s*(.*?)\nA:\s*(.*)', c or '', re.S)
            if not m: continue
            q, a = m.group(1).strip(), m.group(2).strip()
            if BAD.search(a) or len(a) > 700 or (MARKET.search(q + a) and not DATED.search(a)) or re.search(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December) 20\d\d\b', q): continue   # a question about one month's figures goes stale; we compute our own
            a0 = a; a, urls = clean(a); a = SC.scrub(a); q = SC.scrub(q)   # no research wording reaches a page
            if 'http' in a or len(a) < 40 or len(a) < 0.6 * len(a0): continue
            items.append({'q': q, 'a': a, 'gen': 'muse', 'urls': urls})
        muse[r[0]] = items
    pages = {os.path.basename(f)[:-5]: json.load(open(f, encoding='utf-8')) for f in glob.glob(os.path.join(ROOT, 'src/data/pages/*.json'))}
    n_new = n_ext = n_gen = 0
    months = L.load_months()
    mapping = json.load(open(os.path.join(ROOT, 'src/data/snapstats/_mapping.json')))['mapped']
    seen = set()      # Muse repeats the same question on an area page and its guide; each question is used once so twin pages do not share text
    slugs = sorted(set(pages) | {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, 'src/data/local/*.json'))}, key=lambda x: (x.endswith('-guide'), x))
    for s in slugs:
        if s in EXEMPT:
            lf0 = os.path.join(ROOT, 'src/data/local', s + '.json')
            if os.path.exists(lf0):
                j0 = json.load(open(lf0, encoding='utf-8')); keep = [f for f in j0.get('faq', []) if f.get('gen') not in ('muse', 'muse-generic', 'snap-faq', 'bank-faq')]
                if len(keep) != len(j0.get('faq', [])):
                    j0['faq'] = keep; j0['blocks'] = [b for b in j0.get('blocks', []) if b.get('gen') != 'musefaq']
                    if not keep: j0.pop('faq')
                    json.dump(j0, open(lf0, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(lf0, 'a').write('\n')
            continue
        lf = os.path.join(ROOT, 'src/data/local', s + '.json')
        j = json.load(open(lf, encoding='utf-8')) if os.path.exists(lf) else None
        if j and j.get('hand_edited'): continue
        title = (pages[s]['title'] if s in pages else j['new_page']['title']) if (s in pages or (j and j.get('new_page'))) else None
        if title is None: continue
        if j is None: j = {'status': 'draft', 'slug': s, 'updated': '2026-11-01', 'blocks': []}
        own = [f for f in j.get('faq', []) if f.get('gen') not in ('muse', 'muse-generic', 'snap-faq', 'bank-faq')]
        want = 5 if not own else 3
        pick = []
        for p_ in muse.get(s, []):
            key = (re.sub(r'\W+', ' ', p_['q'].lower()).strip(), re.sub(r'\W+', ' ', p_['a'].lower())[:80])
            if key[0] in {k[0] for k in seen} or key[1] in {k[1] for k in seen}: continue
            pick.append(p_); seen.add(key)
            if len(pick) == want: break
        faq = own + [{k: v for k, v in p.items() if k != 'urls'} for p in pick]
        name = AREA.get(s) or re.sub(r'^(Homes|Houses|Condos|Townhomes|Acreages?|Farms?|Land|Lots)( & \w+)* (for Sale )?(in|near) ', '', re.split(r'\s[|:–-]\s|,', title)[0].strip())
        name = re.sub(r'\s+(Homes|Houses|Condos|Townhomes|Acreages?|Real Estate|Guide|Listings)\b.*$', '', name).strip() or name
        disp = re.sub(r'\b(\w+) \1\b', r'\1', place_for(s, title, mapping))
        if len(faq) < 4:
            sf = snap_faqs(s, mapping, months, disp) or []
            faq += [{'q': q, 'a': a, 'gen': 'snap-faq'} for q, a in sf[:3]]
        if len(faq) < 4:
            h0 = sum(map(ord, s)); bk = bank_kind(s); bank = BANK[bk] if bk else []; second = (BANK['guide'] if bk != 'guide' else BANK['house']) if bk else []
            for k in range(len(bank)):
                q, a = bank[(h0 + k) % len(bank)]; faq.append({'q': q.format(n=disp), 'a': a.format(n=disp), 'gen': 'bank-faq'})
            if len(faq) < 4 and second: q, a = second[h0 % len(second)]; faq.append({'q': q.format(n=disp), 'a': a.format(n=disp), 'gen': 'bank-faq'})
        if len(faq) < 4:
            where = f' in {name}' if s in AREA else ''
            for q, a in ((f'Can Jared show me homes{where}?' if s in AREA else 'Can I book a private showing with Jared?', 'Yes. Jared Gibbons, REALTOR® with Royal LePage Little Oak Realty, books private showings across the Fraser Valley and Metro Vancouver. Call or text 604-928-1361, or use the contact form on this site.'),
                         (f'How do I find out what my home{where} is worth?', 'Jared prepares a home evaluation from recent comparable sales and the condition of your home. Contact him on 604-928-1361 or through the form on this site to arrange one.')):
                if len(faq) < 4: faq.append({'q': q, 'a': a, 'gen': 'muse-generic'})
            n_gen += 1
        if faq == (j.get('faq') or []): continue   # rewrite when the list changed, so stale generated FAQs (a past month's figures) are cleared
        j['faq'] = faq
        urls = []
        for p in pick:
            for u in p['urls']:
                if 'jaredgibbons.ca' not in u and u not in urls: urls.append(u)
        j['blocks'] = [b for b in j.get('blocks', []) if b.get('gen') != 'musefaq']
        if urls:
            j['blocks'] += [{'t': 'h', 'level': 2, 'text': 'Sources', 'gen': 'musefaq', 'pos': 'end'},
                            {'t': 'list', 'items': [[{'t': 'Source: ' + urlparse(u).netloc.lower().replace('www.', '') + (f' ({i + 1})' if sum(urlparse(x).netloc.lower() == urlparse(u).netloc.lower() for x in urls[:6]) > 1 else ''), 'h': u}] for i, u in enumerate(urls[:6])], 'gen': 'musefaq', 'pos': 'end'}]
        if os.path.exists(lf): n_ext += 1
        else: n_new += 1
        json.dump(j, open(lf, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(lf, 'a').write('\n')
    print('new local files', n_new, '| extended existing', n_ext, '| generic fill', n_gen)


if __name__ == '__main__':
    main()
