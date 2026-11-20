"""D-386: fixes from the outside full review of Nov 20 2026 (report only, sent by Jared: "heres a review: check out the errors").
Each finding was checked here first; only the confirmed ones are fixed.
  - 13 titles over 60 characters shortened (same words, no new claims).
  - Outbound links: the dead BC manufactured-home-parks page -> the Province's current "Starting a manufactured home site tenancy"
    page (opened in Chrome, 200); engagechilliwack.com/chwk2050 -> https://www.engagechilliwack.com/chwk2050 (the bare host's
    certificate is for another name); daidinfo.com and kerrisdalevillage.com dropped (both show a certificate error in Chrome, on
    www and the bare host).
The listings note ("The live listings did not load.") is now written by the script in src/components/IdxEmbed.astro, so it is not page
text unless the listings actually fail.
Run once from the repo root: python3 tools/review_1120_fixes.py
"""
import glob, json

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

TITLES = {
    'Speculation and Vacancy Tax in Surrey, Langley & Fraser Valley (2026)': 'Speculation and Vacancy Tax: Surrey, Langley & Fraser Valley',
    'Can Foreigners Buy a Home in BC? Federal Ban & 20% Foreign Buyer Tax': 'Can Foreigners Buy a Home in BC? Ban & Foreign Buyer Tax',
    'Property Transfer Tax on a New Home in BC: Newly Built Exemption': 'BC Newly Built Home Exemption: Property Transfer Tax',
    'FHSA Explained for BC Home Buyers: $8,000 a Year, $40,000 Total': 'FHSA for BC Home Buyers: $8,000 a Year, $40,000 Total',
    'BC Home Flipping Tax: 20% on Sales Within 2 Years (2026 Guide)': 'BC Home Flipping Tax: 20% on Sales Within 2 Years',
    "What Is the ALR? Buying Land in BC's Agricultural Land Reserve": "What Is the ALR? Buying in BC's Agricultural Land Reserve",
    'Clayton & East Clayton Surrey Guide | Homes, Schools, SkyTrain': 'Clayton & East Clayton, Surrey | Homes, Schools, SkyTrain',
    'How Much Is Property Transfer Tax in BC? 2026 Rates & Examples': 'How Much Is Property Transfer Tax in BC? Rates & Examples',
    'BC Home Owner Grant 2026: $2,075,000 Threshold & How to Claim': 'BC Home Owner Grant 2026: $2,075,000 Threshold, How to Claim',
    'BC Real Estate Questions Answered: Taxes, Down Payment & More': 'BC Real Estate Questions: Taxes, Down Payment & More',
    "What's My Home Worth? Home Evaluation, South Surrey & Langley": "What's My Home Worth? Evaluation, South Surrey & Langley",
    'Jared Gibbons Reviews | 5.0 on Google | South Surrey REALTOR®': 'Jared Gibbons Reviews | 5.0 on Google | South Surrey Realtor',
    "RRSP Home Buyers' Plan: $60,000 Limit & When You Repay (2026)": "RRSP Home Buyers' Plan: $60,000 Limit & When You Repay",
}
for a, b in TITLES.items(): assert len(b) <= 60, (len(b), b)
URLS = {
    'https://www2.gov.bc.ca/gov/content/housing-tenancy/residential-tenancies/manufactured-home-parks':
        'https://www2.gov.bc.ca/gov/content/housing-tenancy/residential-tenancies/manufactured-homes/starting-tenancy-manufactured-homes',
    'http://engagechilliwack.com/chwk2050': 'https://www.engagechilliwack.com/chwk2050',
    'https://engagechilliwack.com/chwk2050': 'https://www.engagechilliwack.com/chwk2050',
}
DROP = ('daidinfo.com', 'kerrisdalevillage.com')

def has_drop(v): return isinstance(v, str) and any(x in v for x in DROP)
def fix(v):
    if isinstance(v, dict):
        if has_drop(v.get('h')) or has_drop(v.get('href')) or has_drop(v.get('url')):
            if 'h' in v and 't' in v and len(v) <= 3 and not has_drop(v['t']): return {k: x for k, x in v.items() if k != 'h'}   # link inside a sentence: keep the words
            return None
        return {k: fix(x) for k, x in v.items()}
    if isinstance(v, list):
        out = []
        for x in v:
            y = fix(x)
            if y is None or y == []: continue
            out.append(y)
        return out
    if isinstance(v, str):
        if v in TITLES: return TITLES[v]
        for a, b in URLS.items(): v = v.replace(a, b)
    return v

n = 0
for p in glob.glob('src/data/**/*.json', recursive=True):
    raw = open(p).read()
    if not (any(t in raw or json.dumps(t)[1:-1] in raw for t in TITLES) or any(u in raw for u in URLS) or any(x in raw for x in DROP)): continue
    d = load(p); f = fix(d)
    if f != d: save(p, f); n += 1; print('fixed', p)
a = 'src/pages/reviews.astro'; s = open(a).read()
s2 = s.replace('title="Jared Gibbons Reviews | 5.0 on Google | South Surrey REALTOR®"', 'title="Jared Gibbons Reviews | 5.0 on Google | South Surrey Realtor"')
if s2 != s: open(a, 'w').write(s2); print('fixed', a)
print('files:', n)
