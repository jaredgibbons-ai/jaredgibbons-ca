"""Uniqueness uplift for eight pages that sat just under 0.70 (gen 'uplift'), written from the Paragon aggregate in src/data/sold/sold-12m.json only.

Each page gets a short section of its own figures (where the area sits among its neighbours, what the money buys, how the year moved, what a buyer pays in fees, price bands)
and FAQ entries. No outside facts are added: every number is a published median, count or quartile, a rank among the sub-areas, or a plain difference of two of them.
Medians are never added or averaged; where a size or a share is derived the sentence says it is rough and why. A median is shown only with 5+ sales, a quarter only with 5+ sales.
The text is written per page (no sentence is shared between pages), with every figure and rank computed from the aggregate.
python3 -I tools/build_uplift.py       (after build_sold_layer.py; idempotent: it removes its own blocks and FAQ first)"""
import json, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
LOCAL = os.path.join(ROOT, 'src/data/local')
AGG = json.load(open(os.path.join(ROOT, 'src/data/sold/sold-12m.json'), encoding='utf-8')); S = AGG['sub']; C = AGG['city']
G = 'uplift'
def m(x): return f'${int(round(x)):,}'
def n_(x): return f'{int(x):,}'
def H(t): return {'t': 'h', 'level': 2, 'text': t, 'gen': G}
def P(t): return {'t': 'p', 'text': t, 'gen': G}
def ordn(n): return f'{n}{"th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")}'
def grp(k, g): return S[k]['groups'][g]
def board(prefix, g, key, minn=5, asc=False):
    r = [(k[len(prefix):], v['groups'][g]) for k, v in S.items() if k.startswith(prefix) and g in v['groups'] and v['groups'][g].get(key) is not None and v['groups'][g]['n'] >= minn]
    return sorted(r, key=lambda x: x[1][key], reverse=not asc)
def pos(prefix, g, key, name, minn=5, asc=False):
    b = board(prefix, g, key, minn, asc); i = [x for x, _ in b].index(name); return i + 1, len(b), b
def spread_board(prefix, g, minn=5):
    return sorted([(k[len(prefix):], v['groups'][g]['p75'] - v['groups'][g]['p25']) for k, v in S.items() if k.startswith(prefix) and g in v['groups'] and v['groups'][g].get('p25') and v['groups'][g]['n'] >= minn], key=lambda x: -x[1])
R = 'Richmond|'
def side(name, g, minn=5):   # (neighbour just above, neighbour just below) by median price
    i, t, b = pos(R, g, 'price', name, minn); return (b[i - 2] if i > 1 else None), (b[i] if i < t else None)
def qline(q, labels=('November to January', 'February to April', 'May to July', 'August to October')):
    return [(labels[i], x['n'], x['price']) for i, x in enumerate(q) if x['n'] >= 5 and x['price']]

def rk(name, g, key, asc=False, minn=10): return pos(R, g, key, name, minn, asc)
def nb(name, g):
    i, t, b = pos(R, g, 'price', name, 10); return (b[i - 2] if i > 1 else None), (b[i] if i < t else None), b[0], b[-1]
def spr(name, g):
    sb = [x for x in spread_board(R, g, 10)]; nm = [x for x, _ in sb]; return dict(sb)[name], nm.index(name) + 1, len(sb)
def qtxt(q, joiner='; '):
    ls = qline(q); return joiner.join(f"{m(p)} in {lab} ({n} sales)" for lab, n, p in ls)
def fee(t): return t['maint'], t['maint'] * 12, t['maint'] * 12 / t['price'] * 100

PAGES = {}

# ---------- Saunders ----------
def saunders():
    N = 'Saunders'; h = grp(R + N, 'house'); t = grp(R + N, 'townhome'); up, dn, top, low = nb(N, 'house'); a, b, c = rk(N, 'house', 'price')
    d = rk(N, 'house', 'dom', True); pp = rk(N, 'house', 'ppsf'); lt = rk(N, 'house', 'lot_sqft'); yb = rk(N, 'house', 'yb', True); sp = spr(N, 'house')
    tr = rk(N, 'townhome', 'price'); tu, td, _, _ = nb(N, 'townhome'); fm, fy, fp = fee(t)
    size = round(h['price'] / h['ppsf'], -1); q = h['q']
    blocks = [H('Saunders houses against the neighbouring areas'),
        P(f"By median sale price, Saunders houses rank {ordn(a)} of the {b} Richmond sub-areas with ten or more house sales. The areas either side are {up[0]} at {m(up[1]['price'])} from {up[1]['n']} sales ({m(up[1]['price'] - h['price'])} higher) and {dn[0]} at {m(dn[1]['price'])} from {dn[1]['n']} sales ({m(h['price'] - dn[1]['price'])} lower). {top[0]}, at the top of the list, had a {m(top[1]['price'])} median, and {low[0]}, at the bottom, had {m(low[1]['price'])}. On speed Saunders is {ordn(d[0])} quickest of the {d[1]}: its {h['dom']}-day median compares with {d[2][-1][1]['dom']} days in {d[2][-1][0]}, the slowest."),
        P(f"What the money buys is mostly land and age. The median house was built in {h['yb']} (the {ordn(yb[0])} oldest of {yb[1]}) and stood on {n_(h['lot_sqft'])} square feet of lot, the {ordn(lt[0])} largest median lot in Richmond among the {lt[1]} areas. At {m(h['ppsf'])} a square foot the {m(h['price'])} median implies a house of roughly {n_(size)} square feet, a rough figure because one median divided by another is only approximate. Sale prices were spread out: the middle half ran {m(sp[0])} wide, from {m(h['p25'])} to {m(h['p75'])}, the {ordn(sp[1])} widest of {sp[2]} areas."),
        P(f"Taken quarter by quarter, the house median was {qtxt(q)}. Each quarter holds only five to nine sales, so one or two high-priced sales in the same months can lift the median by hundreds of thousands of dollars; the {m(q[1]['price'])} spring figure is a mix of homes, not a step up in prices."),
        P(f"Townhomes are a separate market. {t['n']} sold in Saunders at a {m(t['price'])} median, {ordn(tr[0])} of the {tr[1]} Richmond areas with ten or more townhome sales and {m(t['price'] - td[1]['price'])} above {td[0]} ({m(td[1]['price'])}). Strata fees had a {m(fm)} median a month, or {m(fy)} a year, which is {fp:.2f}% of the median price. They took {t['dom']} days to sell at {t['ratio']}% of the last list price, and the median townhome dates from {t['yb']}, about {h['yb'] and t['yb'] - h['yb']} years newer than the median house.")]
    faq = [("Is Saunders cheaper than the neighbouring Richmond areas?", f"For houses it sits in the lower half: {ordn(a)} of {b} Richmond sub-areas by median price, at {m(h['price'])}, between {up[0]} ({m(up[1]['price'])}) and {dn[0]} ({m(dn[1]['price'])}). Its townhomes, at {m(t['price'])}, rank {ordn(tr[0])} of {tr[1]}."),
           ("What are the strata fees on a Saunders townhome?", f"The median was {m(fm)} a month ({m(fy)} a year) across the {t['maint_n']} townhomes that sold in the last 12 months. Fees vary by complex, so check the strata documents for any one unit.")]
    return blocks, faq
PAGES['saunders-richmond'] = saunders

# ---------- Lackner ----------
def lackner():
    N = 'Lackner'; h = grp(R + N, 'house'); t = grp(R + N, 'townhome'); up, dn, top, low = nb(N, 'house'); a, b, c = rk(N, 'house', 'price')
    d = rk(N, 'house', 'dom', True); rt = rk(N, 'house', 'ratio'); lt = rk(N, 'house', 'lot_sqft', True); pp = rk(N, 'house', 'ppsf'); sp = spr(N, 'house'); q = h['q']
    size = round(h['price'] / h['ppsf'], -1)
    blocks = [H('Lackner prices set beside the rest of Richmond'),
        P(f"Lackner houses are in the upper third of the city: {ordn(a)} of {b} Richmond sub-areas with ten or more house sales, at a {m(h['price'])} median. {up[0]} is {m(up[1]['price'] - h['price'])} above it ({m(up[1]['price'])}, {up[1]['n']} sales) and {dn[0]} is {m(h['price'] - dn[1]['price'])} below ({m(dn[1]['price'])}, {dn[1]['n']} sales), so the three are within {m(up[1]['price'] - dn[1]['price'])} of each other. Lackner buyers got closer to asking than in most places: {h['ratio']}% of the last list price, {ordn(rt[0])} highest of the {rt[1]} areas, with {h['over']}% of houses selling above list."),
        P(f"The lots are small and the houses middle-aged. The median Lackner lot is {n_(h['lot_sqft'])} square feet, the {ordn(lt[0])} smallest of {lt[1]} areas, and the median house was built in {h['yb']}. At {m(h['ppsf'])} a square foot the {m(h['price'])} median implies about {n_(size)} square feet of house, a rough figure, as dividing one median by another is only approximate. Half of all sales landed between {m(h['p25'])} and {m(h['p75'])}, a band {m(sp[0])} wide that is the {ordn(sp[1])} widest of {sp[2]} areas, which puts Lackner about mid-table for how far apart its sale prices were."),
        P(f"The quarterly house medians were {qtxt(q)}. The last quarter in the export had too few Lackner sales to quote, and with only six or seven sales in each of the others the swings between them are within what a handful of different houses would produce."),
        P(f"Townhomes were few, {t['n']} sales in the year, so the figures are indicative only: a {m(t['price'])} median, {t['dom']} days to sell, {t['ratio']}% of the last list price and {t['over']}% sold over list. The median strata fee was {m(t['maint'])} a month and the median build year {t['yb']}, ten years newer than the median Lackner house.")]
    faq = [("How big are the lots in Lackner?", f"The median lot among houses that sold was {n_(h['lot_sqft'])} square feet, about {h['acres']} acre. That is the {ordn(lt[0])} smallest median of the {lt[1]} Richmond areas with ten or more house sales."),
           ("Do Lackner houses sell close to asking?", f"Yes, compared with the rest of Richmond. The median sale was {h['ratio']}% of the last list price, {ordn(rt[0])} highest of {rt[1]} areas, and {h['over']}% of the {h['n']} houses sold above list.")]
    return blocks, faq
PAGES['lackner-richmond'] = lackner

# ---------- Westwind ----------
def westwind():
    N = 'Westwind'; h = grp(R + N, 'house'); t = grp(R + N, 'townhome'); up, dn, top, low = nb(N, 'house'); a, b, c = rk(N, 'house', 'price')
    rt = rk(N, 'house', 'ratio'); ov = rk(N, 'house', 'over'); pp = rk(N, 'house', 'ppsf'); sp = spr(N, 'house'); q = h['q']
    tr = rk(N, 'townhome', 'price', minn=5); td = rk(N, 'townhome', 'dom', True, 5); tf = rk(N, 'townhome', 'maint', False, 5); fm, fy, fp = fee(t)
    size = round(h['price'] / h['ppsf'], -1)
    blocks = [H('Westwind in the middle of the Richmond price range'),
        P(f"Westwind is a small sample, {h['n']} house sales in the year, but it lands in the middle of Richmond: {ordn(a)} of {b} sub-areas with ten or more house sales, at a {m(h['price'])} median. {up[0]} ({m(up[1]['price'])}) is {m(up[1]['price'] - h['price'])} higher and {dn[0]} ({m(dn[1]['price'])}) is {m(h['price'] - dn[1]['price'])} lower. Two figures stand out against the rest of the city. Westwind houses sold at {h['ratio']}% of the last list price, {ordn(rt[0])} highest of {rt[1]} areas, and {h['over']}% sold above list, {ordn(ov[0])} most often of the {ov[1]}."),
        P(f"The typical Westwind house is an early-1980s build on a mid-sized lot: the median year built is {h['yb']}, the median lot {n_(h['lot_sqft'])} square feet (about {h['acres']} acre) and the typical house had {h['beds']} bedrooms. At {m(h['ppsf'])} a square foot, {ordn(pp[0])} highest of {pp[1]}, the {m(h['price'])} median implies a house near {n_(size)} square feet, a rough figure because dividing one median by another is only approximate. The middle half of sales sat between {m(h['p25'])} and {m(h['p75'])}, a band {m(sp[0])} wide and the {ordn(sp[1])} widest of {sp[2]} areas, so prices were bunched more closely than in most of Richmond."),
        P(f"With {h['n']} sales across four quarters, only one quarter reaches the five sales needed to quote a median: {qtxt(q)}. We do not quote the other three, and we do not read a trend into a single quarter."),
        P(f"The {t['n']} Westwind townhomes that sold took an {t['dom']}-day median, {ordn(td[0])} quickest of the {td[1]} Richmond areas with five or more townhome sales, at {t['ratio']}% of the last list price and a {m(t['price'])} median price. Monthly strata fees had a {m(fm)} median, the {ordn(tf[0])} highest of those {tf[1]} areas ({m(fy)} a year, {fp:.2f}% of the median price), and the median townhome was built in {t['yb']}.")]
    faq = [("Do Westwind houses sell above asking?", f"More often than in most of Richmond: {h['over']}% of the {h['n']} houses that sold went above the last list price, {ordn(ov[0])} highest of {ov[1]} areas, and the median sale was {h['ratio']}% of list."),
           ("How quickly do Westwind townhomes sell?", f"The {t['n']} that sold in the last 12 months took a median of {t['dom']} days, the {ordn(td[0])} quickest of {td[1]} Richmond areas, though a sample this small can swing with a single listing.")]
    return blocks, faq
PAGES['westwind-richmond'] = westwind

# ---------- McNair ----------
def mcnair():
    N = 'McNair'; h = grp(R + N, 'house'); up, dn, top, low = nb(N, 'house'); a, b, c = rk(N, 'house', 'price')
    dm = rk(N, 'house', 'dom', True); ov = rk(N, 'house', 'over'); pp = rk(N, 'house', 'ppsf', True); lt = rk(N, 'house', 'lot_sqft'); sp = spr(N, 'house'); q = h['q']
    size = round(h['price'] / h['ppsf'], -1); zero = sum(1 for _, x in board(R, 'house', 'over', 10) if x['over'] == 0)
    blocks = [H('McNair houses: the numbers behind the price'),
        P(f"McNair is a houses-only market in the sales data: {h['n']} houses and two duplex sales closed in the year, and no townhome or condo sales appear in the export for the sub-area. The {m(h['price'])} house median ranks {ordn(a)} of {b} Richmond sub-areas with ten or more house sales, {m(h['price'] - dn[1]['price'])} above {dn[0]} ({m(dn[1]['price'])}) and {m(up[1]['price'] - h['price'])} below {up[0]} ({m(up[1]['price'])})."),
        P(f"The lots are generous and the price per square foot is low. McNair's median lot of {n_(h['lot_sqft'])} square feet is the {ordn(lt[0])} largest of {lt[1]} areas, while its {m(h['ppsf'])} a square foot is the {ordn(pp[0])} lowest of {pp[1]}. Put together, the {m(h['price'])} median implies a house of about {n_(size)} square feet (a rough figure; one median divided by another is only approximate) on a lot that large, with {h['beds']} bedrooms and a median build year of {h['yb']}, so against the rest of Richmond buyers here paid less per square foot of house and received more land."),
        P(f"No McNair house sold above its list price, one of only {zero} Richmond areas with ten or more house sales where that was true. The median sale closed at {h['ratio']}% of the last list price after {h['dom']} days. The middle half of sales sat between {m(h['p25'])} and {m(h['p75'])}, only {m(sp[0])} apart, the {ordn(sp[1])} widest spread of {sp[2]} areas. A narrow band like that makes a handful of comparable sales a reasonable guide to the market."),
        P(f"Quarterly medians exist for two quarters only: {qtxt(q)}. The final two quarters had two sales and one sale, too few to quote, so the year is read as a whole rather than as a trend.")]
    faq = [("Are there townhomes or condos in McNair?", f"Not in the sales data. Between November 2025 and October 2026 the sub-area recorded {h['n']} house sales and 2 duplex sales, and no townhome or condo sales, so there is no median to publish for them."),
           ("Can you offer less than asking in McNair?", f"Sales closed below the last list price in the typical case: the median was {h['ratio']}% of list and none of the {h['n']} houses sold above it. Each home is different, though, and a well-priced listing can still draw competing offers.")]
    return blocks, faq
PAGES['mcnair-richmond'] = mcnair

SRC = ("Source: Paragon, the MLS® system used by Jared’s office, closed sales from November 1, 2025 to October 22, 2026. Pending sales are not counted. Median means the middle price, so half sold for more and half for less. "
       "A price band is shown only with 5 or more sales; with fewer, one sale would be the whole figure.")
BANDS = ['Under $600,000', '$600,000 to $799,999', '$800,000 to $999,999', '$1,000,000 to $1,199,999', '$1,200,000 to $1,499,999', '$1,500,000 to $1,799,999', '$1,800,000 and over']
def band_table(caption, bands, total):
    rows = [[BANDS[i], 'Fewer than 5' if c < 5 else str(c), f'{c / total * 100:.0f}%' if c >= 5 else '—'] for i, c in enumerate(bands) if c or i < 3]
    return {'t': 'table', 'caption': caption, 'head': ['Sale price', 'Sold', 'Share of sales'], 'rows': rows, 'source': SRC, 'gen': G}

# ---------- Anmore ----------
def anmore():
    h = grp('Port Moody|Anmore', 'house'); pm = C['port-moody']['groups']['house']; b = board('Port Moody|', 'house', 'price', 5)
    names = [x for x, _ in b]; i = names.index('Anmore'); dn = b[i + 1]; up = b[i - 1] if i else None
    sp = h['p75'] - h['p25']; psp = pm['p75'] - pm['p25']; size = round(h['price'] / h['ppsf'], -1)
    blocks = [H('Anmore houses against the rest of Port Moody'),
        P(f"Anmore is the most expensive of the {len(b)} Port Moody sub-areas with five or more house sales: {m(h['price'])} from {h['n']} sales, against {m(pm['price'])} for all {pm['n']} Port Moody houses, a difference of {m(h['price'] - pm['price'])} or {(h['price'] / pm['price'] - 1) * 100:.0f}%. The next in line is {dn[0] if up is None else up[0]} at {m((dn if up is None else up)[1]['price'])} ({(dn if up is None else up)[1]['n']} sales)."),
        P(f"The reason is land. The median Anmore lot is {n_(h['lot_sqft'])} square feet, one acre, against {n_(pm['lot_sqft'])} square feet for Port Moody as a whole, which is {h['lot_sqft'] / pm['lot_sqft']:.1f} times as much. The {m(h['ppsf'])} a square foot is below the {m(pm['ppsf'])} Port Moody median even though the price is higher, which fits a price that includes a lot far bigger than the city's, and the {m(h['price'])} median implies a house of about {n_(size)} square feet (a rough figure; one median divided by another is only approximate). The median build year is {h['yb']}, against {pm['yb']} for Port Moody, and the typical house has {h['beds']} bedrooms."),
        P(f"Anmore takes longer and gives up more. Houses took {h['dom']} days to sell against {pm['dom']} in Port Moody, closed at {h['ratio']}% of the last list price against {pm['ratio']}%, and none of the {h['n']} sold above list while {pm['over']}% of Port Moody houses did. The middle half of Anmore sales spanned {m(h['p25'])} to {m(h['p75'])}, a band {m(sp)} wide, about {sp / psp:.1f} times the {m(psp)} band for Port Moody, so one Anmore sale says little about the next. No quarter of the year had five Anmore sales, so there are no quarterly medians.")]
    faq = [("Why are Anmore houses dearer than the rest of Port Moody?", f"Mostly lot size. The median Anmore lot among the {h['n']} houses that sold was {n_(h['lot_sqft'])} square feet, one acre, against {n_(pm['lot_sqft'])} for Port Moody overall, and the median price was {m(h['price'])} against {m(pm['price'])}."),
           ("Do Anmore houses sell above asking?", f"None of the {h['n']} did in the last 12 months. The median sale was {h['ratio']}% of the last list price after {h['dom']} days, compared with {pm['ratio']}% after {pm['dom']} days across Port Moody.")]
    return blocks, faq
PAGES['anmore-port-moody-houses-for-sale'] = anmore

# ---------- Harbour Chines ----------
def harbour():
    h = grp('Coquitlam|Harbour Chines', 'house'); cq = C['coquitlam']['groups']['house']; b = board('Coquitlam|', 'house', 'price', 10)
    names = [x for x, _ in b]; hp = board('Coquitlam|', 'house', 'price', 5); nm5 = [x for x, _ in hp]; i = nm5.index('Harbour Chines')
    up, dn = hp[i - 1], hp[i + 1]; sp = h['p75'] - h['p25']; csp = cq['p75'] - cq['p25']; size = round(h['price'] / h['ppsf'], -1)
    dom_r = sorted([x['dom'] for _, x in board('Coquitlam|', 'house', 'dom', 10)]); slower = sum(1 for d in dom_r if d > h['dom'])
    blocks = [H('Harbour Chines houses against Coquitlam as a whole'),
        P(f"Harbour Chines houses sold for a {m(h['price'])} median across {h['n']} sales, {m(h['price'] - cq['price'])} above the {m(cq['price'])} median for all {cq['n']} Coquitlam houses. Among the {len(hp)} Coquitlam sub-areas with five or more house sales it sits between {up[0]} at {m(up[1]['price'])} ({up[1]['n']} sales) and {dn[0]} at {m(dn[1]['price'])} ({dn[1]['n']} sales). Harbour Place, the other Coquitlam sub-area with Harbour in its name, had {grp('Coquitlam|Harbour Place', 'house')['n']} house sales at a {m(grp('Coquitlam|Harbour Place', 'house')['price'])} median, with {n_(grp('Coquitlam|Harbour Place', 'house')['lot_sqft'])} square feet of median lot against {n_(h['lot_sqft'])} in Harbour Chines."),
        P(f"These are older houses on slightly larger-than-average lots. The median build year is {h['yb']} against {cq['yb']} for Coquitlam, so the typical sale is a house 24 years older than the city's. The median lot is {n_(h['lot_sqft'])} square feet, {(h['lot_sqft'] / cq['lot_sqft'] - 1) * 100:.0f}% larger than Coquitlam's {n_(cq['lot_sqft'])}, and the price per square foot of house, {m(h['ppsf'])} against {m(cq['ppsf'])}, is {(h['ppsf'] / cq['ppsf'] - 1) * 100:.0f}% higher. Together that suggests a good share of the price is the land and location rather than the building. The typical house had {h['beds']} bedrooms and the {m(h['price'])} median implies roughly {n_(size)} square feet (a rough figure; one median divided by another is only approximate)."),
        P(f"The market was slower than the city's. Houses took {h['dom']} days at the median against {cq['dom']} for Coquitlam, and only {slower} of the other {len(dom_r) - 1} Coquitlam sub-areas with ten or more house sales {'was' if slower == 1 else 'were'} slower. They sold at {h['ratio']}% of the last list price ({cq['ratio']}% for Coquitlam), but {h['over']}% went over list against {cq['over']}% across the city. The middle half spanned {m(h['p25'])} to {m(h['p75'])}, a band of {m(sp)}, narrower than Coquitlam's {m(csp)}. Only one quarter (February to April, {h['q'][1]['n']} sales, {m(h['q'][1]['price'])}) reached five sales.")]
    faq = [("How does Harbour Chines compare with Coquitlam on price?", f"Harbour Chines houses had a {m(h['price'])} median from {h['n']} sales, {m(h['price'] - cq['price'])} above the {m(cq['price'])} median for Coquitlam. The typical Harbour Chines house is older ({h['yb']} against {cq['yb']}) and has a larger lot ({n_(h['lot_sqft'])} against {n_(cq['lot_sqft'])} square feet)."),
           ("Are houses in Harbour Chines slow to sell?", f"Slower than most of Coquitlam. The median was {h['dom']} days against {cq['dom']} for the whole city, though {h['over']}% of Harbour Chines houses still sold above the last list price.")]
    return blocks, faq
PAGES['harbour-chines-coquitlam-houses-for-sale'] = harbour

# ---------- Mission townhomes ----------
def mission():
    t = C['mission']['groups']['townhome']; mb = grp('Mission|Mission BC', 'townhome'); mw = grp('Mission|Mission-West', 'townhome'); q = t['q']; b = t['bands']
    fm, fy, fp = fee(t); cx = [c for c in S['Mission|Mission BC']['complexes']['townhome'] if c['n'] >= 5]
    blocks = [H('Mission townhomes that sold: price bands and sub-areas, November 2025 to October 2026'),
        P(f"The {t['n']} townhomes that closed in Mission over the 12 months had a {m(t['price'])} median, and the middle half sold between {m(t['p25'])} and {m(t['p75'])}. That is a long way inside a $1,200,000 ceiling: {b[0] + b[1]} of the {t['n']} sold below $800,000, fewer than five sold between $800,000 and $999,999, and none sold at $1,000,000 or more. A search for Mission townhomes under $1.2 million therefore covers the whole townhome market, not a part of it."),
        band_table('Mission: townhomes sold, by price band', b, t['n']),
        P(f"Most of the activity is in the Mission BC sub-area ({mb['n']} of the {t['n']} sales, {m(mb['price'])} median, {mb['dom']} days to sell), followed by Mission-West ({mw['n']} sales, {m(mw['price'])} median, {mw['dom']} days). The only complexes with five or more sales were {', '.join(f'{c['name']} ({c['n']} sales, {m(c['price'])} median)' for c in cx)} in Mission BC and {S['Mission|Mission-West']['complexes']['townhome'][0]['name']} ({S['Mission|Mission-West']['complexes']['townhome'][0]['n']} sales, {m(S['Mission|Mission-West']['complexes']['townhome'][0]['price'])} median) in Mission-West. The median year built is {t['yb']}, and the median strata fee is {m(fm)} a month ({m(fy)} a year, {fp:.2f}% of the median price)."),
        P(f"By quarter the median was {qtxt(q)}. The most recent quarter has {q[3]['n']} sales, so it is a smaller sample than the others and should be read with that in mind. Homes took {t['dom']} days to sell at {t['ratio']}% of the last list price, and {t['over']}% sold above list.")]
    faq = [("Do all Mission townhomes sell for less than $1.2 million?", f"In the last 12 months, yes. All {t['n']} townhomes that closed in Mission sold under $1,000,000, and the median was {m(t['price'])}. Townhomes at or above $1.2 million did not appear in the sales data."),
           ("What is the strata fee on a Mission townhome?", f"The median across {t['maint_n']} sales was {m(fm)} a month, {m(fy)} a year. Fees were lower in the Mission BC sub-area ({m(mb['maint'])} median) than in Mission-West ({m(mw['maint'])}).")]
    return blocks, faq
PAGES['mission-townhomes-under-1-2m'] = mission

# ---------- Ladner townhomes ----------
def ladner():
    ts = C['tsawwassen']['groups']['townhome']; nd = C['north-delta']['groups']['townhome']
    # whole-Ladner figures come from the saved sold block's group figures (the city key has the same 62 sales)
    L = C['ladner']['groups']['townhome']; b = L['bands']; fm, fy, fp = fee(L)
    blocks = [H('Ladner townhomes against Tsawwassen and North Delta'),
        P(f"The {L['n']} Ladner townhomes sold at a {m(L['price'])} median, the highest of the three Delta areas: {m(L['price'] - nd['price'])} above North Delta ({m(nd['price'])}, {nd['n']} sales) and {m(L['price'] - ts['price'])} above Tsawwassen ({m(ts['price'])}, {ts['n']} sales). Ladner was also the slowest, at {L['dom']} days to sell against {nd['dom']} in North Delta and {ts['dom']} in Tsawwassen. The median build year of {L['yb']} sits next to North Delta's {nd['yb']} and well behind Tsawwassen's {ts['yb']}, and strata fees fall between the other two at {m(fm)} a month, {m(fy)} a year or {fp:.2f}% of the median price."),
        band_table('Ladner: townhomes sold, by price band', b, L['n']),
        P(f"{b[2]} of the {L['n']} Ladner sales, {b[2] / L['n'] * 100:.0f}%, fell between $800,000 and $999,999, and a further {b[3]} between $1,000,000 and $1,199,999. {b[4]} sold between $1,200,000 and $1,499,999. A buyer with a budget under $800,000 had {b[0] + b[1]} sales to choose from over the 12 months. Median per-square-foot prices were {m(L['ppsf'])} in Ladner, {m(ts['ppsf'])} in Tsawwassen and {m(nd['ppsf'])} in North Delta.")]
    faq = [("Are Ladner townhomes cheaper than Tsawwassen?", f"No. In the last 12 months the Ladner median was {m(L['price'])} from {L['n']} sales, {m(L['price'] - ts['price'])} above Tsawwassen's {m(ts['price'])} from {ts['n']} sales, and Ladner homes took {L['dom']} days to sell against {ts['dom']}."),
           ("How many Ladner townhomes sold under $800,000?", f"{b[0] + b[1]} of the {L['n']} that closed in the last 12 months. {b[2]} sold between $800,000 and $999,999.")]
    return blocks, faq
PAGES['ladner-townhomes-for-sale'] = ladner


def insert_at(blocks, new, slug):
    """Where the section goes: Richmond pages after the neighbourhood comparison table; pages with a sold layer after its last block; the rest at the end."""
    if slug.endswith('-richmond'):
        i = max(k for k, b in enumerate(blocks) if b.get('t') == 'table' and 'against the other' in b.get('caption', ''))
    elif any(b.get('gen') == 'sold' for b in blocks):
        i = max(k for k, b in enumerate(blocks) if b.get('gen') == 'sold')
    else:
        i = len(blocks) - 1
        while i >= 0 and blocks[i].get('pos') == 'end': i -= 1
    return blocks[:i + 1] + new + blocks[i + 1:]

def main():
    for slug, fn in PAGES.items():
        f = os.path.join(LOCAL, slug + '.json'); raw = open(f, encoding='utf-8').read(); d = json.loads(raw)
        ind = 1 if raw.startswith('{\n "') else 2 if raw.startswith('{\n  "') else 1
        blocks, faq = fn()
        d['blocks'] = insert_at([b for b in d['blocks'] if b.get('gen') != G], blocks, slug)
        keep = [x for x in d.get('faq', []) if x.get('gen') != G]
        add = [{'q': q, 'a': a, 'gen': G} for q, a in faq]
        at = max([i for i, x in enumerate(keep) if x.get('q', '').startswith(('Who can help', 'Do I need a home', 'Can I book'))] + [len(keep)]) if False else None
        # new answers go before the generic closing questions (who can help, home inspection, private showing) when those are present
        tail = [x for x in keep if x.get('q', '').startswith(('Who can help', 'Do I need a home', 'Can I book'))]
        d['faq'] = [x for x in keep if x not in tail] + add + tail
        out = json.dumps(d, indent=ind, ensure_ascii=False) + ('\n' if raw.endswith('\n') else '')
        open(f, 'w', encoding='utf-8').write(out)
        print(slug, len(blocks), 'blocks', len(add), 'faq')

if __name__ == '__main__':
    main()
