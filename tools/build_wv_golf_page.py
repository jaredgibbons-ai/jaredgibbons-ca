#!/usr/bin/env python3
"""West Vancouver golf course homes page, from Pete's grouped export (src/data/sold/wv-golf.json, 2026-11-08).
Golf flag = Paragon Site Influences contains Golf Course Nearby and/or Golf Course Dev. Figures are grouped only (count, median, middle half, price per sq ft, days, sold-to-list).
Sub-area counts have no medians, so the neighbourhood table shows counts only.  The live search (Jerry, id 1451590) matches the word golf in listing remarks, not the flag; the page says so.
    python3 -I tools/build_wv_golf_page.py"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_new_searches as N
import build_extras_pages as X
from build_new_searches import P, H, L, tbl, money, num
from build_extras_pages import fit

G = 'golf'
D = json.load(open('src/data/sold/wv-golf.json'))
go, al, nb, dev = D['golf_nearby_or_dev'], D['all_west_vancouver_detached'], D['golf_course_nearby'], D['golf_course_dev']
subs = D['golf_any_by_sub_area']
SLUG = 'west-vancouver-golf-course-homes-for-sale'
SUBPAGE = {'British Properties': 'british-properties', 'Dundarave': 'dundarave-west-vancouver-guide', 'Caulfeild': 'caulfeild', 'Ambleside': 'ambleside', 'Chartwell': 'chartwell',
           'Cypress Park Estates': 'cypress-park-estates', 'Cedardale': 'cedardale', 'Chelsea Park': 'chelsea-park', 'Altamont': 'altamont', 'Bayridge': 'bayridge', 'Canterbury WV': 'canterbury-wv',
           'Whitby Estates': 'whitby-estates-west-vancouver-guide'}
DISP = {'Horseshoe Bay WV': 'Horseshoe Bay', 'Westmount WV': 'Westmount', 'Canterbury WV': 'Canterbury'}
pct = lambda a, b: round(100 * (a - b) / b)
f1 = lambda r: f'{100 * r:.1f}%'
share = round(100 * go['count'] / al['count']); prem = pct(go['median'], al['median']); ppsf_p = pct(go['median_psf'], al['median_psf'])
assert (go['count'], al['count']) == (128, 351)
NB = lambda s: {'t': DISP.get(s, s), 'h': f'/{SUBPAGE[s]}.html'} if s in SUBPAGE and N.exists(SUBPAGE[s]) else DISP.get(s, s)
top3 = subs[:3]; top3n = sum(n for _, n in top3)
SRCW = ('Source: Paragon closed and pending detached sales (class RD) in West Vancouver, accepted between November 1, 2025 and October 31, 2026. A pending sale is firm but has not completed, so its price can still change. '
        'Median means the middle price. The golf flag is the Paragon Site Influences field with Golf Course Nearby or Golf Course Dev., which the listing agent fills in.')

title = next(t for t in ('West Vancouver Golf Course Homes for Sale | Prices', 'West Vancouver Golf Course Homes for Sale') if 38 <= len(t) <= 60)
seo = dict(title=title, h1='Golf Course Homes for Sale in West Vancouver', crumb='Golf course homes',
           description=fit(*[f'{a} {b}' for a in ('Search West Vancouver golf course homes.', 'West Vancouver golf course homes for sale.', 'Search West Vancouver homes on or near a golf course.')
                              for b in (f'{go["count"]} sold over twelve months at a median of {money(go["median"])}, with counts by neighbourhood and what to check before you offer.',
                                        f'{go["count"]} sold in twelve months at a median of {money(go["median"])}. See counts by neighbourhood and what to check before you offer.',
                                        f'{go["count"]} sold in twelve months at a median of {money(go["median"])}, with counts by neighbourhood and what to check.')]),
           links_h='More West Vancouver searches')
rows = [['Sales', num(go['count']), num(al['count'])], ['Median price', money(go['median']), money(al['median'])],
        ['Middle half of prices', f'{money(go["p25"])} to {money(go["p75"])}', f'{money(al["p25"])} to {money(al["p75"])}'],
        ['Price per square foot', money(round(go['median_psf'])), money(round(al['median_psf']))], ['Days to sell', f'{go["median_dom"]:.0f}', f'{al["median_dom"]:.0f}'],
        ['Sold price as a share of list price', f1(go['median_ratio']), f1(al['median_ratio'])]]
srows = [[NB(s), num(n), f'{round(100 * n / go["count"])}%'] for s, n in subs if n >= 5]
rest = sum(n for s, n in subs if n < 5)
if rest: srows.append([f'{sum(1 for s, n in subs if n < 5)} other areas, under 5 sales each', num(rest), f'{round(100 * rest / go["count"])}%'])
bl = [{'t': 'notice', 'text': 'Draft for Jared’s approval. Sold figures come from Paragon closed and pending sales to October 31, 2026, grouped by Pete from a West Vancouver detached export. A pending sale is firm but has not completed, so its price can still change. The live search is not connected yet.', 'gen': G},
      P('This search lists detached houses for sale in West Vancouver whose listing remarks mention golf. That is a word search, so it also finds houses that name a course in the description without flagging it, and it can miss a house whose agent left the word out.'),
      P(f'West Vancouver had {al["count"]} detached sales between November 1, 2025 and October 31, 2026, and {go["count"]} of them ({share}%) carried a golf flag in Paragon. Those {go["count"]} sold for a median of {money(go["median"])}, {abs(prem)}% {"above" if prem >= 0 else "below"} the {money(al["median"])} median for all {al["count"]} detached sales.'),
      {'t': 'grid', 'gen': G}, H('What West Vancouver golf course homes sold for'),
      tbl('West Vancouver detached sales, golf flag and all detached homes', ['Measure', 'Golf flag', 'All detached homes'], rows, SRCW),
      P(f'Per square foot the flagged homes cost {money(round(go["median_psf"]))}, {abs(ppsf_p)}% {"more" if ppsf_p >= 0 else "less"} than the {money(round(al["median_psf"]))} for all detached homes. They took {go["median_dom"]:.0f} days to sell at a median, against {al["median_dom"]:.0f}, and closed at {f1(go["median_ratio"])} of the last list price, against {f1(al["median_ratio"])}. '
        'The export does not give floor area or lot size, so it cannot say how much of the price gap comes from bigger homes rather than the course.'),
      P(f'{nb["count"]} of the {go["count"]} sales were flagged Golf Course Nearby, with a median of {money(nb["median"])}. Only {dev["count"]} were flagged Golf Course Dev., in Eagle Harbour, Cypress Park Estates and the British Properties, so that group is too small to compare.'),
      H('West Vancouver neighbourhoods with golf course homes'),
      P(f'{subs[0][0]} had the most flagged sales, {subs[0][1]}, followed by {subs[1][0]} ({subs[1][1]}), {subs[2][0]} ({subs[2][1]}) and {subs[3][0]} ({subs[3][1]}). The top three areas together made up {round(100 * top3n / go["count"])}% of the {go["count"]} flagged sales, and {len(subs)} sub-areas had at least one.'),
      tbl('West Vancouver golf flag sales by neighbourhood', ['Neighbourhood', 'Golf flag sales', 'Share of flagged sales'], srows,
          'Source: Paragon closed and pending detached sales (class RD) in West Vancouver, November 1, 2025 to October 31, 2026. Neighbourhoods are the board’s MLS® sub-areas. Counts only: medians by neighbourhood are not shown.'),
      H('Before you offer on a West Vancouver golf course home'),
      L([f'Ask how close the lot is to the course and which side faces it. The flag showed on {go["count"]} West Vancouver sales, and a home flagged Golf Course Nearby can sit some distance from the course.',
         'Look at the windows, siding and deck on the course side for ball marks, and ask the seller about damage, netting or an insurance claim.',
         'Order the title. A right-of-way, covenant or setback can tie a lot to a course, and it shows on title, not on the listing.',
         f'Go at two different times of day. Mowing starts early and play changes the noise. The flagged homes took {go["median_dom"]:.0f} days at a median, so there is time for a second visit.',
         f'Set the price against similar unflagged homes: {money(go["median"])} for the flagged group and {money(al["median"])} for all detached sales. West Vancouver prices vary a great deal by sub-area, so compare within the same area.']),
      H('Estimate the payment on a West Vancouver golf course home'),
      P(f'The calculator starts at the West Vancouver golf flag median of {money(go["median"])}.'), {'t': 'calc', 'which': 'mortgage', 'price': go['median'], 'gen': G}]
faq = [('How much does a West Vancouver golf course home cost?', f'The {go["count"]} flagged detached homes that sold between November 1, 2025 and October 31, 2026 had a median of {money(go["median"])}, and the middle half sold between {money(go["p25"])} and {money(go["p75"])}. All {al["count"]} West Vancouver detached sales had a median of {money(al["median"])}.'),
       ('What counts as a golf course home in West Vancouver?', 'On the sold figures, a detached home whose Paragon Site Influences field lists Golf Course Nearby or Golf Course Dev. The listing agent enters it, so it covers homes near a course as well as on one. The live search above uses the word golf in the listing remarks instead.'),
       ('How fast do West Vancouver golf course homes sell?', f'{go["median_dom"]:.0f} days at a median, closing at {f1(go["median_ratio"])} of the last list price. All West Vancouver detached homes took {al["median_dom"]:.0f} days and closed at {f1(al["median_ratio"])}.'),
       ('Which West Vancouver neighbourhoods have the most golf course homes?', f'{subs[0][0]} had {subs[0][1]} flagged sales, {subs[1][0]} {subs[1][1]}, and {subs[2][0]} and {subs[3][0]} {subs[2][1]} each, between November 1, 2025 and October 31, 2026.')]
links = [('West Vancouver homes for sale', 'west-vancouver-homes-for-sale'), ('West Vancouver market stats', 'west-vancouver-real-estate-market-stats'), ('British Properties homes', 'british-properties'),
         ('Dundarave guide', 'dundarave-west-vancouver-guide'), ('Caulfeild homes', 'caulfeild'), ('Langley golf course homes', 'langley-golf-course-homes-for-sale'), ('Mortgage calculator', 'mortgage-calculator')]
N.NEW.update([SLUG])
j = N.finish(SLUG, seo, [('West Vancouver homes', 'west-vancouver-homes-for-sale')], faq, bl, 'West Vancouver golf course homes: your questions answered', links, dict(search_page=dict(kind='golf', city='west-vancouver'), lead='quiz'))
N.TITLE[SLUG] = j['new_page']['h1']; N.write_seo([j])
# inbound link on the West Vancouver homes page
f = 'src/data/local/west-vancouver-homes-for-sale.json'
raw = open(f).read(); d = json.loads(raw); nl = '\n' if raw.endswith('\n') else ''
line2 = raw.split('\n')[1] if '\n' in raw else ''; ind = len(line2) - len(line2.lstrip(' ')) or 1; asc = '\\u' in raw
d['blocks'] = [b for b in d['blocks'] if not (b.get('gen') == 'golflinks' and b.get('city') == 'west-vancouver')]
d['blocks'] += [{'t': 'h', 'level': 2, 'text': 'West Vancouver golf course homes', 'gen': 'golflinks', 'pos': 'end', 'city': 'west-vancouver'},
                {'t': 'list', 'items': [[N.lk(j['new_page']['h1'], SLUG)]], 'gen': 'golflinks', 'pos': 'end', 'city': 'west-vancouver'}]
open(f, 'w').write(json.dumps(d, indent=ind, ensure_ascii=asc) + nl)
print('built', SLUG, len(j['new_page']['description']), len(title))
