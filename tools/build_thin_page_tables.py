"""Adds an 'at a glance' table to the Fraser Valley short-term rental and suite rules page, built only from what that page already states
(bylaw numbers, dates, caps). Idempotent.  python3 -I tools/build_thin_page_tables.py"""
import json, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
f = os.path.join(ROOT, 'src/data/local/fraser-valley-short-term-rental-and-suite-rules.json'); raw = open(f, encoding='utf-8').read(); d = json.loads(raw)
d['blocks'] = [b for b in d['blocks'] if b.get('gen') != 'glance']
rows = [
 ['Chilliwack', 'Bylaw No. 5141 (adopted November 24, 2021): stays of 28 days or less, up to 3 sleeping units and 8 guests, in your principal residence or an accessory dwelling on the same lot; the Business Licence number goes on every ad', 'Zoning Bylaw Amendment Bylaw 2024, No. 5395 (readings June 4, 2024): up to 4 units on lots over 280 m² inside the urban growth boundary'],
 ['Abbotsford', 'Business Licence Bylaw 1551-2006, section 11.30, plus section 140 of the Zoning Bylaw: proof of principal residence, a fire safety plan and a parking plan before a licence is issued', 'Zoning amendments adopted June 2024 (day and bylaw number not confirmed on an official page)'],
 ['Mission', 'Not covered on this page', 'Zoning Amending Bylaw 6299-2024-5949(163), adopted July 17, 2024 by a 4 to 2 vote'],
 ['Maple Ridge', 'Not covered on this page', 'Zone Amending Bylaw No. 7998-2024, adopted June 25, 2024'],
 ['Pitt Meadows', 'Not permitted anywhere in the city; bed and breakfasts are allowed under section 5.6 of Zoning Bylaw No. 2505, 2011', 'Zoning Amendment Bylaw No. 2986, 2024, adopted June 25, 2024; secondary suites must be registered with the City'],
 ['White Rock', 'Allowed under section 5.8 of Zoning Bylaw 2024, No. 2506, but only one accessory use at a time (a registered suite and a short-term rental cannot both be in place)', 'Not covered on this page'],
]
tbl = {'t': 'table', 'caption': 'Short-term rental and multi-unit rules at a glance, as stated by each city', 'head': ['City', 'Short-term rentals', 'Multi-unit (small-scale housing) bylaw'], 'rows': rows, 'gen': 'glance',
       'source': "Source: each city's own bylaw, council record or website, read November 1, 2026. Bylaws change, so confirm the current version with the city. Hope and Harrison Hot Springs are covered further down."}
at = next(i for i, b in enumerate(d['blocks']) if b.get('t') == 'h' and b.get('text') == 'Chilliwack')
d['blocks'][at:at] = [{'t': 'h', 'level': 2, 'text': 'The rules at a glance', 'gen': 'glance'}, tbl]
for kw in (dict(indent=2, ensure_ascii=False), dict(indent=1, ensure_ascii=False), dict(separators=(',', ':'), ensure_ascii=False)):
    if json.dumps(json.loads(raw), **kw) in (raw, raw.rstrip('\n')): out = json.dumps(d, **kw) + ('\n' if raw.endswith('\n') else ''); break
else: out = json.dumps(d, indent=2, ensure_ascii=False) + '\n'
open(f, 'w', encoding='utf-8').write(out); print('ok')
