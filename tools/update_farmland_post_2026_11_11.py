#!/usr/bin/env python3
"""Farmland post update, Nov 11, 2026 (D-225): BC election final count and Budget 2026's proposed foreign-buyer-ban changes.
Text agreed with Jared; checked against Elections BC/BC Ballot (final count Nov 9, Return Day Nov 18, recounts in Kelowna Centre and
Ladysmith-Oceanside), the BC Greens' Oct 2, 2026 food and farming plan ("restrict foreign and corporate farmland ownership") and
Budget 2026 reporting (Nov 5). Idempotent. python3 -I tools/update_farmland_post_2026_11_11.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
F = 'src/data/posts/can-foreigners-buy-farmland-in-bc-fraser-valley-rules-9186434.json'
FED = ('Under current law it ends on January 1, 2027. Budget 2026 (November 5) proposes extending it to January 1, 2029 for existing homes '
       'and exempting new homes, but that is not law yet. Parliament still has to pass a bill, and the details have not been released.')
ELECTION = [{'t': 'BC held a provincial election on October 24, 2026. Elections BC finished the final count on November 9: the Conservative Party won 64 of 93 districts (BC NDP 27, BC Green 2), so a Conservative majority government is forming. Judicial recounts are still due in Kelowna Centre and Ladysmith-Oceanside, and results become official on November 18 ('},
            {'t': 'Elections BC', 'h': 'https://elections.bc.ca/2026-provincial-election/'},
            {'t': '). Farmland ownership came up during the campaign, and the BC Greens proposed restricting foreign and corporate ownership of farmland. As of November 11, 2026, no such limit exists and the new government has not announced one, but rules may change, so check the current rules before you make an offer.'}]


def main():
    raw = open(F, encoding='utf-8').read(); d = json.loads(raw); B = d['blocks']
    txt = lambda b: ''.join(x.get('t', '') for x in b.get('parts', []))
    for b in B:
        t = txt(b)
        if t.startswith('It covers a house of up to three units inside a census area.'):
            b['parts'] = [{'t': 'It covers a house of up to three units inside a census area. Vacant land is not covered. ' + FED}]
        elif t.startswith('BC held a provincial election on October 24, 2026, and a new government'):
            b['parts'] = [{'t': 'BC held a provincial election on October 24, 2026, and a Conservative majority government is forming. A new government can change the rules.'}]
        elif t.startswith('Set by the Government of Canada. It can stop a purchase'):
            b['parts'] = [{'t': 'Set by the Government of Canada. It can stop a purchase of a covered home in a census area. Breaking it can mean a fine of up to $10,000. ' + FED}]
        elif t.startswith('As of October 18, 2026, no decision on what comes next'):
            b['parts'] = [{'t': 'Budget 2026 (November 5) proposes extending the ban to January 1, 2029 for existing homes and exempting new homes, but that is not law yet. Parliament still has to pass a bill, and the details have not been released ('},
                          {'t': 'Budget 2026', 'h': 'https://budget.canada.ca/'}, {'t': '; '},
                          {'t': 'Daily Hive, November 5, 2026', 'h': 'https://dailyhive.com/vancouver/canada-foreign-buyers-ban-extension-proposal-2029'}, {'t': ').'}]
        elif t.startswith('BC held a provincial election on October 24, 2026 ('):
            b['parts'] = ELECTION
        elif t.startswith('Under current law it is repealed on January 1, 2027.'):
            b['parts'] = [{'t': FED + ' BC’s 20% tax and the SVT are separate and do not end on that date.'}]
    for b in B:
        for x in b.get('parts', []):
            x['t'] = x['t'].replace('As of October 26, 2026', 'As of November 11, 2026')
    # sources: Budget 2026 and the Daily Hive report, after the Global News entry
    if not any('Budget 2026' in txt(b) and txt(b).endswith(':') for b in B):
        i = next(k for k, b in enumerate(B) if txt(b).startswith('Elections BC, 2026 Provincial Election:'))
        B[i:i] = [{'t': 'p', 'parts': [{'t': 'Government of Canada, Budget 2026 (November 5, 2026):'}]}, {'t': 'p', 'parts': [{'t': 'budget.canada.ca', 'h': 'https://budget.canada.ca/'}]},
                  {'t': 'p', 'parts': [{'t': 'Daily Hive, “Canada proposes extending foreign buyer ban to 2029” (November 5, 2026):'}]},
                  {'t': 'p', 'parts': [{'t': 'dailyhive.com', 'h': 'https://dailyhive.com/vancouver/canada-foreign-buyers-ban-extension-proposal-2029'}]},
                  {'t': 'p', 'parts': [{'t': 'BC Green Party, food and farming plan (October 2, 2026):'}]},
                  {'t': 'p', 'parts': [{'t': 'bcgreens.ca', 'h': 'https://bcgreens.ca/launch-plan-to-support-local-food-production-and-farmers/'}]}]
    for b in B:
        if txt(b).startswith('Update log:') and 'November 11, 2026' not in txt(b):
            b['parts'] = [{'t': txt(b).rstrip('.') + '. November 11, 2026 – updated for the BC election final count and the Budget 2026 proposal to extend the federal ban.'}]
    d['seo']['Modified'] = '2026-11-11T19:00:00+00:00'
    open(F, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, separators=(',', ':')) + ('\n' if raw.endswith('\n') else ''))
    s = json.dumps(d, ensure_ascii=False)
    print('October 26 left:', s.count('October 26'), '| Budget 2026 mentions:', s.count('Budget 2026'))


if __name__ == '__main__': main()
