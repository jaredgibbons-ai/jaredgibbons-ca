#!/usr/bin/env python3
"""BC mobile home buying rules: details from the Manufactured Home Park Tenancy Regulation (D-315). Pete's park-rules workbook
("Bylaws & law" tab) pointed to them; each was read in the Regulation itself on November 16, 2026. Safe to re-run.

    python3 -I tools/add_mhpta_details_2026_11_16.py
"""
import json
from pathlib import Path

F = Path(__file__).resolve().parent.parent / 'src/data/local/bc-mobile-home-buying-rules.json'
REG = 'https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/481_2003'
G = 'mhpta2'
AFTER = {
    'Buying in a park is an assignment, with the park owner’s consent': [
        {'t': 'p', 'gen': G, 'text': 'The park owner can refuse consent only for the reasons in section 48 of the Manufactured Home Park Tenancy Regulation: in short, good reason to think the buyer will not follow the tenancy agreement or park rules or cannot pay the rent, a 55+ park where the buyer does not meet the age requirement, a buyer who will not use the home as a residence, unpaid rent or an unpaid order, or a home that does not meet housing, health and safety standards. If consent is refused for another reason, the seller can apply to the Residential Tenancy Branch.'},
        {'t': 'p', 'gen': G, 'text': 'Keep the sale an assignment. If the buyer signs a new tenancy agreement with the park instead, the park can set a new pad rent; with an assignment, the current rent and its next increase date carry over.'},
    ],
    'Park rules and 55+ parks': [
        {'t': 'p', 'gen': G, 'text': 'Two rules buyers ask about. A new park rule banning pets does not apply to a pet already living with a tenant (Regulation, section 31). And a park cannot charge a guest fee, whether or not the guest stays overnight (Regulation, section 3). Pet limits that were in the park rules when the tenancy started do apply, so read the rules before you write an offer.'},
    ],
}


def main():
    d = json.loads(F.read_text())
    blocks = [b for b in d['blocks'] if b.get('gen') != G]
    res = []
    pending = None   # new paragraphs go at the end of their section
    for b in blocks:
        if pending and b.get('t') != 'p':
            res += AFTER[pending]; pending = None
        res.append(b)
        if b.get('t') == 'h' and b.get('text') in AFTER: pending = b['text']
    if pending: res += AFTER[pending]
    for b in res:
        if b.get('t') == 'list' and any(REG in json.dumps(x) for x in b.get('items', [])): break
    else:
        src = next(i for i, b in enumerate(res) if b.get('t') == 'h' and b.get('text') == 'Sources')
        res[src + 1]['items'].append([{'t': 'bclaws.gov.bc.ca · Manufactured Home Park Tenancy Regulation', 'h': REG}])
    d['blocks'] = res
    d['updated'] = '2026-11-16'
    F.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
    print('ok', sum(1 for b in res if b.get('gen') == G))


if __name__ == '__main__':
    main()
