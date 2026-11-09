"""Fraser Valley market-stats page (archive record src/data/pages/fraser-valley-market-stats.json) moved from September to October 2026 (2026-11-09).

Same precedent as tools/convert_fv_stats.py: the page was captured from an interactive widget and rebuilt as stat cards and tables, so it is edited in place by block.
Every number comes from src/data/market/2026-10.json (FVREB package, released November 3, 2026); days to sell come from the board's news release (detached 50, condo 44, townhome 37).
Earlier months in the trend table are worked back from the board's published 1-, 3-, 6- and 12-month changes and rounded to the nearest $1,000 (the package carries no table of past prices).
Each block is checked for its September text before it is replaced, so a second run stops instead of overwriting. The narrative sentences are written from the October rankings below.
    python3 -I tools/refresh_fv_stats_page.py
"""
import json, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
PAGE = os.path.join(ROOT, 'src/data/pages/fraser-valley-market-stats.json')
M = json.load(open(os.path.join(ROOT, 'src/data/market/2026-10.json'), encoding='utf-8'))['fvreb']
HPI, SUM = M['hpi'], M['summary']
DAYS = {'detached': 50, 'townhouse': 37, 'apartment': 44}
money = lambda v: '${:,.0f}'.format(v)
def pc(v): return ('+' if v > 0 else '-' if v < 0 else '') + '{:.1f}%'.format(abs(v))
page = json.load(open(PAGE, encoding='utf-8')); B = page['blocks']
def txt(b): return ' '.join(p['t'] for p in b['parts'])
def setp(i, new, must):
    assert must in txt(B[i]), (i, txt(B[i])[:80])
    B[i]['parts'] = [{'t': new}]

ALL = SUM['All Areas Combined']; fv = HPI['Fraser Valley Board']
sales = sum(ALL[t]['sales']['now'] for t in ('detached', 'townhouse', 'apartment'))
# the Fraser Valley totals on the package's page 1 include all property types
TOT = {'sales': 1051, 'sales_yoy': -6.4, 'new': 2551, 'new_yoy': -14.0, 'active': 9164, 'active_yoy': -9.5, 'active_mom': -6.1}
ratio = TOT['sales'] / TOT['active'] * 100

# header and cards
assert 'September 2026' in txt(B[3]); B[3]['parts'][1]['t'] = 'October 2026'
B[6]['items'] = [
    {'label': 'Benchmark price', 'value': money(fv['composite']['benchmark']), 'sub': f'{pc(fv["composite"]["chg_1m"])} vs last month', 'delta': pc(fv['composite']['chg_1m'])},
    {'label': 'Benchmark, 1-year change', 'value': pc(fv['composite']['chg_1y']), 'sub': 'vs same month last year', 'delta': pc(fv['composite']['chg_1y'])},
    {'label': 'Sales', 'value': f'{TOT["sales"]:,}', 'sub': f'{pc(TOT["sales_yoy"])} vs last year', 'delta': pc(TOT['sales_yoy'])},
    {'label': 'Active listings', 'value': f'{TOT["active"]:,}', 'sub': f'{pc(TOT["active_mom"])} vs last month', 'delta': pc(TOT['active_mom'])},
    {'label': 'Sales-to-active ratio', 'value': f'{ratio:.1f}%', 'sub': "Buyer's market" if ratio < 12 else 'Balanced market' if ratio <= 20 else "Seller's market"},
    {'label': 'Days to sell (average)', 'value': f'{DAYS["detached"]} days', 'sub': f'Detached. Townhouse {DAYS["townhouse"]} · Apartment {DAYS["apartment"]}'}]
setp(7, f'Showing Fraser Valley, all home types. New listings: {TOT["new"]:,} ({pc(TOT["new_yoy"])} vs last year). Active listings are {abs(TOT["active_yoy"]):.1f}% below October 2025. Ratio guide: under 12% buyer\'s market, 12% to 20% balanced, over 20% seller\'s market.', 'New listings')

# trend table: earlier months worked back from the published changes
def back(v, chg): return round(v / (1 + chg / 100), -3)
rows = []
for key, lab in (('composite', 'All types'), ('detached', 'Detached'), ('townhouse', 'Townhouse'), ('apartment', 'Apartment')):
    h = fv[key]; rows.append([lab, money(back(h['benchmark'], h['chg_1y'])), money(back(h['benchmark'], h['chg_6m'])), money(back(h['benchmark'], h['chg_3m'])), money(back(h['benchmark'], h['chg_1m'])), money(h['benchmark'])])
assert B[9]['t'] == 'table'
B[9]['caption'] = 'Fraser Valley benchmark price by home type, October 2026 and earlier months'
B[9]['head'] = ['Type', '1 year ago', '6 months ago', '3 months ago', '1 month ago', 'Latest']; B[9]['rows'] = rows
B[9]['source'] = 'Source: FVREB MLS® Home Price Index, October 2026. Earlier months are worked back from the board’s published one-, three-, six- and twelve-month changes and rounded to the nearest $1,000.'
setp(10, f'The Fraser Valley is in a buyer\'s market. FVREB recorded {TOT["sales"]:,} sales, {abs(TOT["sales_yoy"]):.1f}% fewer than the same month last year and 14.0% more than September, while {TOT["new"]:,} new listings came on and {TOT["active"]:,} homes were for sale at month end. The composite benchmark for a typical home was {money(fv["composite"]["benchmark"])}, {pc(fv["composite"]["chg_1m"])} on the month and {pc(fv["composite"]["chg_1y"])} on the year. Detached homes took {DAYS["detached"]} days to sell, townhouses {DAYS["townhouse"]} and apartments {DAYS["apartment"]}.', "The Fraser Valley is in a buyer's market")

# by type
rows = []
for key, lab in (('detached', 'Detached'), ('townhouse', 'Townhouse'), ('apartment', 'Apartment')):
    h = fv[key]; a = ALL[key]
    rows.append([lab, money(h['benchmark']), pc(h['chg_1m']), pc(h['chg_1y']), f'{a["sales"]["now"]:,}', f'{a["active"]["now"]:,}', str(DAYS[key])])
B[12]['rows'] = rows

# areas
AREAS = [('Langley', 'Langley', 'Langley'), ('Surrey (Central)', 'Surrey', 'Surrey - Central'), ('Cloverdale', 'Cloverdale', 'Surrey - Cloverdale'), ('South Surrey / White Rock', 'South Surrey & White Rock', 'White Rock / South Surrey'),
         ('North Delta', 'North Delta', 'Delta - North'), ('Abbotsford', 'Abbotsford', 'Abbotsford'), ('Mission', 'Mission', 'Mission')]
data = {}
for lab, hk, sk in AREAS:
    s = SUM[sk]; h = HPI[hk]
    tot_s = sum(s[t]['sales']['now'] for t in ('detached', 'townhouse', 'apartment')); tot_a = sum(s[t]['active']['now'] for t in ('detached', 'townhouse', 'apartment'))
    data[lab] = dict(comp=h['composite'], s=s, tot_s=tot_s, tot_a=tot_a, ratio=tot_s / tot_a * 100)
B[14]['rows'] = [[lab, money(v['comp']['benchmark']), pc(v['comp']['chg_1y']), money(v['s']['detached']['benchmark']['now']), money(v['s']['townhouse']['benchmark']['now']), money(v['s']['apartment']['benchmark']['now']), f'{v["ratio"]:.1f}%'] for lab, v in data.items()]
yoy = sorted(((v['comp']['chg_1y'], lab) for lab, v in data.items()))
assert yoy[0][1] == 'Mission' and yoy[-1][1] == 'Cloverdale'
setp(16, f'Over the past year, the composite benchmark fell the most in {yoy[0][1]} ({pc(yoy[0][0])}) and {yoy[1][1]} ({pc(yoy[1][0])}), and the least in {yoy[-1][1]} ({pc(yoy[-1][0])}) and {yoy[-2][1]} ({pc(yoy[-2][0])}). Small areas such as North Delta and Mission have few townhouse and apartment sales, so one month can move their figures more than in larger areas.', 'Over the past year')
assert [l for _, l in yoy[:2]] == ['Mission', 'Abbotsford'] and [l for _, l in yoy[-2:]] == ['South Surrey / White Rock', 'Cloverdale']
src = B[18]['parts']; assert 'Package202609.pdf' in src[0]['h']; src[0]['h'] = src[0]['h'].replace('202609', '202610')

START = {'Langley': 20, 'Surrey (Central)': 25, 'Cloverdale': 30, 'South Surrey / White Rock': 35, 'North Delta': 40, 'Abbotsford': 45, 'Mission': 50}
for lab, v in data.items():
    i = START[lab]; assert B[i]['t'] == 'h' and B[i]['text'].startswith(lab.split(' /')[0].split(' (')[0]), (lab, B[i])
    B[i + 1]['items'] = [{'label': 'Composite benchmark', 'value': money(v['comp']['benchmark']), 'sub': 'vs last year', 'delta': pc(v['comp']['chg_1y'])}, {'label': 'Homes for sale', 'value': f'{v["tot_a"]:,}', 'sub': 'active listings'}, {'label': 'Sales this month', 'value': str(v['tot_s']), 'sub': 'closed this month'}]
    B[i + 2]['rows'] = [[lab2, money(v['s'][t]['benchmark']['now']), pc(v['s'][t]['benchmark']['chg_year']), str(v['s'][t]['sales']['now']), f'{v["s"][t]["active"]["now"]:,}'] for t, lab2 in (('detached', 'Detached'), ('townhouse', 'Townhouse'), ('apartment', 'Apartment'))]

def S(a, t, k): return a['s'][t]['sales'][k]
L, Su, C, SS, ND, AB, MI = (data[k] for k in ('Langley', 'Surrey (Central)', 'Cloverdale', 'South Surrey / White Rock', 'North Delta', 'Abbotsford', 'Mission'))
# narrative: first sentences (geography) are kept; the data sentences are rewritten for October
def keep(i, n): return '. '.join(txt(B[i]).split('. ')[:n]).rstrip('.') + '.'
setp(23, keep(23, 1) + f' Langley held its value better than the board as a whole over the past twelve months ({pc(L["comp"]["chg_1y"])} against {pc(fv["composite"]["chg_1y"])}), and townhouses were the one type that sold more than a year ago ({S(L, "townhouse", "now")} sales against {S(L, "townhouse", "last_year")}). Apartments moved the most on price ({pc(L["s"]["apartment"]["benchmark"]["chg_year"])} on the year), so apartment buyers have the most room to negotiate here.', 'FVREB reports Langley as one area')
setp(28, keep(28, 3) + f' Detached sales in Central Surrey rose against last year ({S(Su, "detached", "now")} sales against {S(Su, "detached", "last_year")}) even as the detached benchmark fell {abs(Su["s"]["detached"]["benchmark"]["chg_year"]):.1f}%, a sign that buyers step in when prices adjust.', 'FVREB splits Surrey')
setp(33, keep(33, 2) + f' Its composite benchmark sits just above Central Surrey\'s and it had the smallest yearly price drop of any area ({pc(C["comp"]["chg_1y"])}).', 'Cloverdale is part of the City of Surrey')
ssw = SS['s']
setp(38, keep(38, 1) + f' It has the highest detached benchmark on the board ({money(ssw["detached"]["benchmark"]["now"])}). Sales were lower than last October in all three types, with townhouses down most ({S(SS, "townhouse", "now")} against {S(SS, "townhouse", "last_year")}). The townhouse benchmark fell {abs(ssw["townhouse"]["benchmark"]["chg_year"]):.1f}% over the year, the second-largest townhouse drop on the board after Abbotsford, while the townhouse and apartment benchmarks both rose on the month ({pc(HPI["South Surrey & White Rock"]["townhouse"]["chg_1m"])} and {pc(HPI["South Surrey & White Rock"]["apartment"]["chg_1m"])}).', 'This area takes in')
setp(43, keep(43, 3) + f' In October detached sales were {S(ND, "detached", "now")} against {S(ND, "detached", "last_year")} a year earlier, while townhouses ({S(ND, "townhouse", "now")}) and apartments ({S(ND, "apartment", "now")}) barely sold at all. With so few of those sales, one or two deals can swing the monthly figures.', 'North Delta is the only part of Delta')
ab = AB['s']
setp(48, keep(48, 1) + f' Detached prices fell {abs(ab["detached"]["benchmark"]["chg_year"]):.1f}% over the year even as detached sales rose to {S(AB, "detached", "now")} from {S(AB, "detached", "last_year")}, while townhouse and apartment sales were lower than a year ago.', 'Abbotsford has the lowest townhouse')
mi = MI['s']
setp(53, f'Mission has the lowest detached benchmark on the board, and its composite benchmark took the largest yearly drop of any area ({pc(MI["comp"]["chg_1y"])}). Its detached price fell {abs(mi["detached"]["benchmark"]["chg_year"]):.1f}%, level with Abbotsford. Most sales here are detached homes, many with bigger lots than you\'ll find closer to the border. Townhouse and apartment listings are up sharply on last year ({mi["townhouse"]["active"]["now"]} against {mi["townhouse"]["active"]["now"] * 100 // int(100 + mi["townhouse"]["active"]["chg_year"])} and {mi["apartment"]["active"]["now"]} against {mi["apartment"]["active"]["now"] * 100 // int(100 + mi["apartment"]["active"]["chg_year"])}), and with only a handful of sales those buyers have plenty to pick from.', 'Mission has the lowest detached benchmark')

# FAQ
setp(68, f'Yes, prices are lower than a year ago. By the FVREB benchmark, the composite price for a typical Fraser Valley home was {money(fv["composite"]["benchmark"])}, a change of {pc(fv["composite"]["chg_1y"])} from the same month last year and {pc(fv["composite"]["chg_1m"])} from the month before. The table on this page shows the benchmark for each home type a year ago, six, three and one month ago, and now.', 'Yes, prices are lower')
setp(70, f'FVREB compares monthly sales with the number of homes for sale, called the sales-to-active listings ratio, and treats 12% to 20% as balanced. With {TOT["sales"]:,} sales and {TOT["active"]:,} active listings, the ratio is {ratio:.1f}%, which is a buyer\'s market. Areas and home types can differ, so check yours in the area tables above.', 'FVREB compares monthly sales')
setp(76, f'FVREB reports average days on market by property type for the whole board. In the latest report, a detached home took about {DAYS["detached"]} days to sell, a townhouse about {DAYS["townhouse"]} days and an apartment about {DAYS["apartment"]} days. Homes priced in line with recent comparable sales tend to sell faster, and overpriced homes tend to sit longer.', 'FVREB reports average days on market')
json.dump(page, open(PAGE, 'w', encoding='utf-8'), indent=1 if open(PAGE).read(4) == '{\n "' else 2, ensure_ascii=False)
print('Fraser Valley stats page moved to October 2026;', {k: round(v['ratio'], 1) for k, v in data.items()})
