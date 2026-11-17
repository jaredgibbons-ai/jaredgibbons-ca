#!/usr/bin/env python3
"""BC-wide buying-rules pages: drop FAQs that belong to one town or building (D-338).

D-202 built these pages by moving rules paragraphs and FAQs out of the area guides, so several FAQs still answered
for one place (Mission's tax penalty, Dollarton schools, British Properties buses, Sullivan Station, Royal Court,
Manor Ridge, Shaughnessy, Surrey) or repeated another FAQ on the same page. They read wrongly on a page meant for
all of BC and feed the page's FAQ schema. Matched by question text. Safe to re-run.

    python3 -I tools/fix_bc_rule_faqs_2026_11_17.py
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent.parent / 'src/data/local'
DROP = {
    'bc-55-plus-strata-rules': [
        'My spouse is under 55. If we buy in a true 55+ strata nearby, can we both live there?',   # same as the fuller FAQ below
        'My spouse is under 55. Can we both live in a 55+ strata after we sell?',                   # Royal Court, The Wedgewood
        'Can I rent out my unit?',                                                                  # Manor Ridge; same as the rental FAQ
        'Older listings for Shaughnessy strata say "rentals not allowed." Can I rent out a unit I buy there now?',
        'Does a 55+ restriction shrink my resale buyer pool (at the nearest complexes)?',          # duplicate
    ],
    'bc-condo-buying-rules': [
        "What is the tax penalty if I miss Mission's July 2 deadline?",
    ],
    'bc-land-buying-rules': [
        'Which schools serve my address?',                                                          # Dollarton
        'Will GST apply to a newly subdivided lot bought from a developer?',                        # duplicates
        'Will GST apply if a developer sells me a newly subdivided lot here?',
        'Will GST apply if I buy a vacant parcel?',
    ],
    'bc-townhome-buying-rules': [
        'How do I get downtown without a car?',                                                     # British Properties
        'Strata or non-strata — which townhouse am I actually looking at in Sullivan Station?',
        'Can someone outbid my accepted offer?',                                                    # Surrey only
    ],
}

# The tn-page test wants at least 5 FAQs; the land page fell to 3, so two general ones go back, from rules already on the page.
ADD = {
    'bc-land-buying-rules': [
        {'q': 'How much property transfer tax will I pay on a lot?',
         'a': 'The general rates: 1% on the first $200,000, 2% from $200,000 to $2 million and 3% above, plus another 2% on the residential part above $3 million. The newly built home exemption is for new homes, not bare land, so a vacant lot usually pays the full tax; for example, a $500,000 lot pays $8,000.'},
        {'q': 'Can I subdivide or stratify ALR land?',
         'a': 'Only with the Agricultural Land Commission’s approval. Registering a strata plan counts as subdividing, so homes on ALR land can’t be stratified without the Commission’s permission. Price an ALR parcel as one parcel unless that permission exists.'},
    ],
}


def main():
    n = 0
    for slug, qs in DROP.items():
        f = D / f'{slug}.json'
        d = json.loads(f.read_text(encoding='utf-8'))
        keep = [x for x in d.get('faq', []) if x.get('q', '').strip() not in qs]
        n += len(d.get('faq', [])) - len(keep)
        have = {x.get('q') for x in keep}
        keep += [x for x in ADD.get(slug, []) if x['q'] not in have]
        if keep != d.get('faq', []):
            d['faq'] = keep
            f.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('removed', n)


if __name__ == '__main__':
    main()
