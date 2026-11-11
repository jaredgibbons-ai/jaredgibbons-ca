#!/usr/bin/env python3
"""Links in for three pages the launch pack held for having fewer than 2 pages linking to them (D-213, Nov 11, 2026):
Squamish and Whistler market stats (0 links), the Agassiz guide (1) and the Cultus Lake rules page (1). Each gets a short "Nearby" line on related pages.
python3 -I tools/link_orphans_2026_11_11.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
G = 'orphanlink'
ADD = {
    'furry-creek-bc-guide': [('Market figures for the area: ', 'Squamish real estate market stats', 'squamish-real-estate-market-stats')],
    'mount-currie-bc-guide': [('Market figures for the area: ', 'Whistler real estate market stats', 'whistler-real-estate-market-stats')],
    'west-vancouver-real-estate-market-stats': [('Up the Sea-to-Sky: ', 'Squamish market stats', 'squamish-real-estate-market-stats'),
                                                ('Further up: ', 'Whistler market stats', 'whistler-real-estate-market-stats')],
    'squamish-real-estate-market-stats': [('Further up the highway: ', 'Whistler market stats', 'whistler-real-estate-market-stats')],
    'whistler-real-estate-market-stats': [('Down the highway: ', 'Squamish market stats', 'squamish-real-estate-market-stats')],
    'harrison-hot-springs-bc-guide': [('Next door: ', 'Agassiz guide', 'agassiz-bc-guide')],
    'hope-bc-guide': [('Also in the area: ', 'Agassiz guide', 'agassiz-bc-guide')],
    'cultus-lake-guide': [('Leases, zoning, sewer and taxes at the lake: ', 'buying a home at Cultus Lake: the rules', 'cultus-lake-home-buying-rules')],
    'lindell-beach-bc-guide': [('Leases, zoning, sewer and taxes at the lake: ', 'buying a home at Cultus Lake: the rules', 'cultus-lake-home-buying-rules')],
    'cultus-lake': [('Leases, zoning, sewer and taxes at the lake: ', 'buying a home at Cultus Lake: the rules', 'cultus-lake-home-buying-rules')],
    'fraser-valley-commercial-market-report': [('Burnaby’s industrial area up close: ', 'Lake City industrial', 'lake-city-industrial')],
    'commercial': [('Industrial areas: ', 'Lake City, Burnaby', 'lake-city-industrial'), ('', 'Port Kells, Surrey', 'port-kells-surrey-guide')],
}
for slug, lines in ADD.items():
    f = f'src/data/local/{slug}.json'; raw = open(f, encoding='utf-8').read(); d = json.loads(raw)
    d['blocks'] = [b for b in d['blocks'] if b.get('gen') != G]
    d['blocks'] += [{'t': 'h', 'level': 2, 'text': 'Nearby', 'gen': G, 'pos': 'end'},
                    {'t': 'list', 'items': [[{'t': lead}, {'t': label, 'h': f'/{target}.html'}] for lead, label, target in lines], 'gen': G, 'pos': 'end'}]
    ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
    open(f, 'w', encoding='utf-8').write((json.dumps(d, ensure_ascii=False, indent=ind) if ind else json.dumps(d, ensure_ascii=False, separators=(',', ':'))) + ('\n' if raw.endswith('\n') else ''))
print('pages linked:', len(ADD))
