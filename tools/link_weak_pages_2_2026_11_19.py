"""D-378 (links): pages with only 1-2 inbound links in main content (site-wide scan, Nov 19 2026) get links from the pages a buyer
would come from. Same "Also worth comparing:" line under the introduction as D-373/374 (gen lnk1119), link text = target H1.
Run from the repo root after a build: python3 tools/link_weak_pages_2_2026_11_19.py
"""
import html, json, os, re

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

def h1(s):
    t = open(f'dist/{s}.html').read(); m = re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S)
    return html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()

ADD = {
    'white-rock-condos-for-sale': ['white-rock-townhomes-for-sale'],
    'white-rock-guide': ['white-rock-townhomes-for-sale'],
    'white-rock-2-bedroom-condos-for-sale': ['white-rock-townhomes-for-sale'],
    'white-rock-south-surrey-houses-for-sale': ['white-rock-townhomes-for-sale'],
    'willoughby-heights': ['yorkson-langley-guide'],
    'willoughby-houses-for-sale': ['yorkson-langley-guide'],
    'willoughby-townhomes-for-sale': ['yorkson-langley-guide'],
    'willoughby-condos-for-sale': ['yorkson-langley-guide'],
    'first-time-home-buyer-program': ['fhsa-first-home-savings-account-bc', 'rrsp-home-buyers-plan-bc', 'minimum-down-payment-canada', 'bc-newly-built-home-exemption'],
    'first-time-buyer-calculator': ['fhsa-first-home-savings-account-bc', 'rrsp-home-buyers-plan-bc'],
    'how-much-is-property-transfer-tax-in-bc': ['bc-newly-built-home-exemption', 'can-foreigners-buy-property-in-bc', 'bc-home-buyer-rescission-period'],
    # buying.html and selling.html are designed pages that do not render local blocks, so the selling-side guides go on the city selling pages.
    'sell-my-house-in-surrey': ['bc-home-flipping-tax', 'speculation-and-vacancy-tax-surrey-langley'],
    'sell-my-house-in-langley': ['bc-home-flipping-tax', 'speculation-and-vacancy-tax-surrey-langley'],
    'sell-my-house-in-south-surrey-white-rock': ['bc-home-flipping-tax', 'how-to-appeal-bc-assessment'],
}
READ = {'first-time-home-buyer-program', 'first-time-buyer-calculator', 'how-much-is-property-transfer-tax-in-bc', 'sell-my-house-in-surrey', 'sell-my-house-in-langley', 'sell-my-house-in-south-surrey-white-rock'}
n = 0
for s, ts in ADD.items():
    p = f'src/data/local/{s}.json'
    if not os.path.exists(p): print('no local file, skipped:', s); continue
    d = load(p); blocks = d.setdefault('blocks', [])
    line = next((b for b in blocks if b.get('gen') == 'lnk1119'), None)
    have = {x.get('h') for x in (line or {}).get('parts', [])}
    new = [(t, h1(t)) for t in ts if f'/{t}.html' not in have]
    if not new: continue
    items = ([(x['h'][1:-5], x['t']) for x in line['parts'] if x.get('h')] if line else []) + new
    lead = 'Also worth reading: ' if s in READ else 'Also worth comparing: '
    parts = [{'t': lead}]
    for i, (t, label) in enumerate(items):
        if i: parts.append({'t': ' and ' if i == len(items) - 1 else ', '})
        parts.append({'t': label, 'h': f'/{t}.html'})
    parts.append({'t': '.'})
    if line: line['parts'] = parts
    else: blocks.append({'t': 'p', 'pos': 'after-intro', 'gen': 'lnk1119', 'parts': parts})
    save(p, d); n += len(new); print('linked', s, '->', [t for t, _ in new])
print('links added:', n)
