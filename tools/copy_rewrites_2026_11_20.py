#!/usr/bin/env python3
"""Copy rewrites Jared approved on Nov 20, 2026 ("approve copy"; doc "Copy rewrites for approval"), items 1-5 (D-393).
Items 6-8 (farm alert box, quiz and closing box) are in GenericPage / ListingAlert / SearchQuiz / Cta. Idempotent.
    python3 -I tools/copy_rewrites_2026_11_20.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
FARM = "I grew up on a 40-acre farm in Langley. That's where I learned how land, barns, wells and the ALR actually work, and it's why farm and acreage sales are a big part of my business today."
def load(f): raw = open(f).read(); return raw, json.loads(raw)
def save(f, raw, d):
    ind = 2 if raw.startswith('{\n  ') else (1 if raw.startswith('{\n ') else None)
    sep = (',', ':') if ind is None and '":"' in raw[:300] else None
    open(f, 'w').write(json.dumps(d, ensure_ascii=False, indent=ind, separators=sep) + ('\n' if raw.endswith('\n') else ''))
def tx(b): return b.get('text') if isinstance(b.get('text'), str) else ''.join(x.get('t', '') for x in b.get('parts', []))

# 1. Home evaluation intro: the two template paragraphs become one
f = 'src/data/pages/home-evaluation.json'; raw, d = load(f); bl = d['blocks']
i = next((i for i, b in enumerate(bl) if tx(b).startswith('The answers to your home-selling questions')), None)
if i is not None:
    bl[i] = {'t': 'p', 'parts': [{'t': "Tell me your address and I'll price your home off the closest recent sales in your neighbourhood, the same way I'd price it if you listed with me. "
                                      "You'll get a price range and the sales behind it, from me, the same day. As soon as you enter the address, the form also shows the property's zoning, lot size and ALR status from the city's own map. No obligation."}]}
    if tx(bl[i + 1]).startswith('Through the Comparative Market Analysis'): del bl[i + 1]
    save(f, raw, d)
# 2. About: the opening two sentences
f = 'src/data/pages/about.json'; raw, d = load(f)
for b in d['blocks']:
    if tx(b).startswith('Jared Gibbons is a highly regarded'):
        b.clear(); b.update({'t': 'p', 'parts': [{'t': 'Jared Gibbons sells homes in South Surrey, White Rock, Langley, Surrey, Ladner and Tsawwassen.'}]}); save(f, raw, d); break
# 3. Selling: the line under "Sell better"
f = 'src/data/designed/selling.json'; s = open(f).read()
s = s.replace('"tag": "Selling a home in South Surrey, White Rock, Langley and the Fraser Valley."',
              '"tag": "Selling in South Surrey, White Rock, Langley or the Fraser Valley? Every listing gets pro photos, drone, video, floor plans, ads and 5,000 postcards."')
open(f, 'w').write(s)
# 4. Poultry intro (Jared approved the off-market line too)
f = 'src/data/pages/poultry-farms-for-sale-bc.json'; raw, d = load(f)
for b in d['blocks']:
    if tx(b).startswith('The vast majority of BC poultry production'):
        b['parts'] = [{'t': "Most of BC's poultry production sits in one short stretch of the Fraser Valley: Abbotsford, Chilliwack and Langley. Most producing farms never reach the MLS®; they change hands privately between growers. "
                            "What's listed publicly is below. With the new entrant program closed, buying an existing farm or quota is effectively the only way into commercial poultry in BC, so if you're ready to buy, call or text me at 604-928-1361."}]
        save(f, raw, d); break
# 5. The 40-acre farm line, after each farm page's opening paragraph
for slug, after in [('poultry-farms-for-sale-bc', "Most of BC's poultry production"), ('langley-farms', 'Buying farmland in the Township of Langley'), ('buying-a-chicken-farm-bc', 'Buying a chicken farm in British Columbia')]:
    f = f'src/data/pages/{slug}.json'; raw, d = load(f); bl = d['blocks']
    if any(tx(b) == FARM for b in bl): continue
    i = next(i for i, b in enumerate(bl) if tx(b).startswith(after))
    bl.insert(i + 1, {'t': 'p', 'parts': [{'t': FARM}]}); save(f, raw, d)
print('done')
