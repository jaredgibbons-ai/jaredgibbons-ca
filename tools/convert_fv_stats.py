"""One-off: the archived Fraser Valley market-stats page was captured as flat paragraphs and one-item-per-cell lists (an interactive widget flattened to text).
Rebuild those parts as real stat cards and tables. Wording and numbers are unchanged; only the structure changes. Run once; it is a no-op on a converted page."""
import json, re, sys
P = 'src/data/pages/fraser-valley-market-stats.json'
d = json.load(open(P)); B = d['blocks']
if any(b['t'] in ('stats', 'chips') for b in B): print('already converted'); sys.exit(0)
T = lambda it: ''.join(p['t'] for p in it).strip()
cells = lambda b: [T(it) for it in b['items']]
def ptxt(b): return ' '.join(p['t'] for p in b['parts']).strip()
def anchor(h): return '#' + h.split('#')[-1]
out = B[:5]                       # H1, intro, byline, stats-for, "Latest market numbers"
# market chips (areas link to their section further down)
chips = [{'t': 'Fraser Valley', 'h': '#latest', 'now': True}, {'t': 'Langley', 'h': '#langley'}]
for it in B[7]['items'][:6]: chips.append({'t': T(it), 'h': anchor(it[0]['h'])})
out.append({'t': 'chips', 'label': 'Jump to an area', 'items': chips})
bench = cells(B[7])[11]                                                       # $861,300
out.append({'t': 'stats', 'items': [
    {'label': 'Benchmark price', 'value': bench, 'sub': ptxt(B[8]), 'delta': '-1.0%'},
    {'label': 'Benchmark, 1-year change', 'value': ptxt(B[10]).split(' ')[0], 'sub': 'vs same month last year', 'delta': '-7.2%'},
    {'label': 'Sales', 'value': ptxt(B[12]), 'sub': ptxt(B[13]), 'delta': '-4.2%'},
    {'label': 'Active listings', 'value': ptxt(B[15]), 'sub': ptxt(B[16]), 'delta': '-0.2%'},
    {'label': 'Sales-to-active ratio', 'value': cells(B[17])[1], 'sub': cells(B[17])[2]},
    {'label': 'Days to sell (average)', 'value': cells(B[17])[4].replace('Detached ', '') + ' days', 'sub': 'Detached. ' + cells(B[17])[5].replace(' · ', ', ').replace('Townhouse ', 'Townhouse ').replace('Apartment ', 'Apartment ')},
]})
out.append(B[18])                                                             # showing / new listings note
out.append({'t': 'h', 'level': 3, 'text': 'Benchmark price trend, last 13 monthly reports: Fraser Valley', 'id': 'trend'})
tr = cells(B[20])[1:]                                                         # skip the "Benchmark trend table" label
out.append({'t': 'table', 'caption': 'Fraser Valley benchmark price by home type over the last 13 monthly reports', 'head': tr[:6], 'rows': [tr[i:i + 6] for i in range(6, len(tr), 6)]})
out.append(B[21])
out.append(B[22])
c = cells(B[23])
out.append({'t': 'table', 'caption': 'Fraser Valley benchmark price, sales and days to sell by home type', 'head': c[:7], 'rows': [c[i:i + 7] for i in range(7, len(c), 7)]})
out.append(B[24])
# compare areas: header list, then rows split across h3 headings
head = cells(B[25]); names = {26: 'Langley', 28: 'Cloverdale', 30: 'South Surrey / White Rock', 32: 'North Delta', 34: 'Abbotsford', 36: 'Mission'}
rows = []
l27 = cells(B[27]); rows.append([names[26]] + l27[:6]); rows.append(l27[6:13])
for hi in (28, 30, 32, 34, 36): rows.append([names[hi]] + cells(B[hi + 1]))
out.append({'t': 'table', 'caption': 'Benchmark price by area and home type, with sales-to-active ratio', 'head': head, 'rows': rows})
for i in range(38, 42): out.append(B[i])                                      # "Where prices are changing most" + source
out.append({'t': 'h', 'level': 2, 'text': 'Market stats by area', 'id': 'areas'})
# per-area sections
i = 43; slug = lambda n: re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-')
while i < 94:
    b = B[i]
    if b['t'] == 'list' and len(b['items']) == 3: name, comp = cells(b)[0], cells(b)[2]; chg = ptxt(B[i + 1]).split(' ')[0]; j = i + 2
    elif b['t'] == 'h' and b['level'] == 3: name, comp = b['text'], ptxt(B[i + 2]); chg = ptxt(B[i + 3]).split(' ')[0]; j = i + 4
    else: raise SystemExit(f'unexpected block {i}: {b}')
    L = cells(B[j]); sale, sales_m = L[1], L[2]
    tb = L[3:]
    out.append({'t': 'h', 'level': 3, 'text': name, 'id': {'South Surrey / White Rock': 'south-surrey-white-rock'}.get(name, slug(name))})
    out.append({'t': 'stats', 'small': True, 'items': [
        {'label': 'Composite benchmark', 'value': comp, 'sub': 'vs last year', 'delta': chg},
        {'label': 'Homes for sale', 'value': sale, 'sub': 'active listings'},
        {'label': 'Sales this month', 'value': sales_m.replace(' sales this month', ''), 'sub': 'closed this month'},
    ]})
    out.append({'t': 'table', 'caption': f'{name} benchmark price, sales and active listings by home type', 'head': tb[:5], 'rows': [tb[k:k + 5] for k in range(5, len(tb), 5)]})
    i = j + 1
    while i < 94 and B[i]['t'] == 'p' and not (B[i]['parts'][0]['t'] in ('Composite benchmark',)): out.append(B[i]); i += 1
    # stop when the next area begins
    if i < 94 and B[i]['t'] == 'p': raise SystemExit(f'stray p at {i}')
for k in range(94, len(B)): out.append(B[k])
# the heading "Latest market numbers" gets an anchor
out[4] = dict(out[4], id='latest')
d['blocks'] = out
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2)
print('converted', len(B), '->', len(out))
