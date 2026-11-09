"""One-off (2026-11-09): add the detached-benchmark moves in dollars to Surrey acreages for sale.

The page's benchmark paragraph quotes percentages only, and the October Surrey figures are now also quoted on the Fraser Valley stats page, which took the page just under the 0.70
uniqueness bar. The dollar moves over six months and three years are worked back from the board's published changes (rounded to $100) and are specific to these two areas.
    python3 -I tools/add_surrey_acreage_dollars.py
"""
import json, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
F = os.path.join(ROOT, 'src/data/local/surrey-acreages-for-sale.json')
raw = open(F, encoding='utf-8').read(); d = json.loads(raw)
h = json.load(open(os.path.join(ROOT, 'src/data/market/2026-10.json'), encoding='utf-8'))['fvreb']['hpi']
money = lambda v: '${:,.0f}'.format(v)
if any(b.get('text', '').startswith('In dollars, the Surrey detached') for b in d['blocks']): raise SystemExit('already added')
i = next(k for k, b in enumerate(d['blocks']) if b.get('gen') == 'gappage' and b.get('text', '').startswith('Surrey: the detached houses benchmark was'))
parts = []
for area, lab in (('Surrey', 'the Surrey board area'), ('North Surrey', 'North Surrey')):
    x = h[area]['detached']; b = x['benchmark']; w6 = round(b / (1 + x['chg_6m'] / 100), -2); w3 = round(b / (1 + x['chg_3y'] / 100), -2)
    parts.append(f'in {lab} it stood near {money(w6)} six months ago and near {money(w3)} three years ago, which puts today\'s {money(b)} about {money(abs(b - w6))} {"above" if b > w6 else "below"} the first mark and {money(abs(b - w3))} {"above" if b > w3 else "below"} the second')
d['blocks'].insert(i + 1, {'t': 'p', 'text': 'In dollars, the Surrey detached benchmark tells the same story as the percentages: ' + '; '.join(parts) + '. An acreage usually sells for more than the benchmark house, so treat these as a guide to direction rather than a price.', 'gen': 'gappage'})
open(F, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2) + ('\n' if raw.endswith('\n') else ''))
print('added after block', i)
