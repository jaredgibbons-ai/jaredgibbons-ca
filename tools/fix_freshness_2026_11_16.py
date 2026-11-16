#!/usr/bin/env python3
"""Freshness fixes of 2026-11-16 (weekly freshness check, then Jared: "Fix everything").

Edits the raw file text, so each JSON file keeps its own format. Safe to rerun: a replacement is skipped when
its old text is gone. Every new fact below was read on 2026-11-16 from the primary source named next to it.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
L = 'src/data/local/'

ABB_25_URL = 'https://www.abbotsford.ca/sites/default/files/2025-05/Bylaw%203643-2025%20Tax%20Rates%20Bylaw%202025.pdf'
ABB_26_URL = ('https://www.abbotsford.ca/sites/default/files/2026-05/2026%20Tax%20Rates%20Bylaw%203727-2026%20Tax%20Rates%20Bylaw'
              '%202026%20%28Adopted%20%2B%20Signed%29%202026%2005%2012.pdf')
ABB_25_T = 'abbotsford.ca · Bylaw 3643 2025 Tax Rates Bylaw 2025'
ABB_26_T = 'abbotsford.ca · Tax Rates Bylaw 3727-2026'
MR_25_URL = 'https://www.mapleridge.ca/sites/default/files/2025-05/2025%20Property%20Tax%20Rates_1.pdf'
MR_26_URL = 'https://www.mapleridge.ca/media/file/2026-property-tax-rates'

FIXES = [
    # 1. Elections BC results, GE 2026-10-24: https://results.elections.bc.ca/Results_11684_GE-2026-10-24_Party.html
    ('src/data/posts/can-foreigners-buy-farmland-in-bc-fraser-valley-rules-9186434.json',
     'BC held a provincial election on October 24, 2026, and a Conservative majority government is forming.',
     'BC held a provincial election on October 24, 2026. The final count, completed November 9, gave the BC Conservatives 64 of 93 seats.'),

    # 2. Abbotsford Tax Rates Bylaw No. 3727-2026 (ABB_26_URL): Sumas Prairie dyking residential 0.58353 per $1,000 (Table 2),
    #    parcel tax $36.74/acre Zone A (s.10(b)) and $23.12/acre Zone B (s.10(c)).
    (L + 'abbotsford-houses-for-sale.json',
     'The 2025 bylaw is Bylaw No. 3643-2025, read a first and second time May 6, 2025.',
     'The 2026 bylaw is Bylaw No. 3727-2026.'),
    (L + 'abbotsford-55-plus-townhomes-for-sale.json',
     "Abbotsford's Tax Rates Bylaw, 2025 is Bylaw No. 3643-2025, and its rates are expressed per $1,000 of taxable value.",
     "Abbotsford's Tax Rates Bylaw, 2026 is Bylaw No. 3727-2026, and its rates are expressed per $1,000 of taxable value."),
    (L + 'central-abbotsford-houses-for-sale.json',
     'Bylaw No. 3643-2025 for 2025, per $1,000 of taxable value.', 'Bylaw No. 3727-2026 for 2026, per $1,000 of taxable value.'),
    (L + 'sumas-mountain-abbotsford-houses-for-sale.json',
     'Bylaw No. 3643-2025 for 2025, per $1,000 of taxable value.', 'Bylaw No. 3727-2026 for 2026, per $1,000 of taxable value.'),
    (L + 'poplar-abbotsford-houses-for-sale.json',
     'Tax Rates Bylaw No. 3643-2025 sets the 2025 rates per $1,000 of taxable value.',
     'Tax Rates Bylaw No. 3727-2026 sets the 2026 rates per $1,000 of taxable value.'),
    (L + 'sumas-prairie.json',
     'pay the dyking levy in Tax Rates Bylaw 3643-2025: residential 0.54199 per $1,000, plus $31.95 per acre (Zone A) or $20.10 per acre (Zone B) parcel tax.',
     'pay the dyking levy in Tax Rates Bylaw 3727-2026: residential 0.58353 per $1,000 for 2026, plus $36.74 per acre (Zone A) or $23.12 per acre (Zone B) parcel tax.'),
    (L + 'sumas-prairie.json',
     "Yes. Abbotsford's Tax Rates Bylaw 3643-2025 levies a separate Sumas Prairie Dyking and Drainage Area charge on parcels inside that area: a residential rate of 0.54199 per $1,000 plus a parcel tax of $31.95 per acre in Zone A or $20.10 per acre in Zone B.",
     "Yes. Abbotsford's Tax Rates Bylaw 3727-2026 levies a separate Sumas Prairie Dyking and Drainage Area charge on parcels inside that area: for 2026, a residential rate of 0.58353 per $1,000 plus a parcel tax of $36.74 per acre in Zone A or $23.12 per acre in Zone B."),

    # 3. City of Maple Ridge, 2026 Tax Rates (MR_26_URL): Class 1 mill rate 4.53578, general 2.86430, school levy 1.21480.
    (L + 'albion-maple-ridge-houses-for-sale.json',
     "Maple Ridge's 2025 total residential mill rate is 4.1895 per $1,000 of assessed value on the City's 2025 Property Tax Rate Summary, of which the City general rate is 2.6648.",
     "Maple Ridge's 2026 total residential mill rate is 4.53578 per $1,000 of assessed value on the City's 2026 tax rates sheet, of which the City general rate is 2.86430."),
    (L + 'albion-maple-ridge-houses-for-sale.json', '"2025 total residential mill rate"', '"2026 total residential mill rate"'),
    (L + 'albion-maple-ridge-houses-for-sale.json', '"4.1895 per $1,000"', '"4.53578 per $1,000"'),
    (L + 'northeast-maple-ridge-guide.json',
     'City of Maple Ridge 2025 tax-rate summary: municipal general rate for residential (Class 1) is 2.6648 per $1,000 of assessed value, and the provincial school levy for Class 1 is 1.1194 per $1,000 (2025).',
     'City of Maple Ridge 2026 tax rates: municipal general rate for residential (Class 1) is 2.86430 per $1,000 of assessed value, and the provincial school levy for Class 1 is 1.21480 per $1,000 (2026).'),
    (L + 'northeast-maple-ridge-guide.json', 'mapleridge.ca · 2025 Property Tax Rates 1', 'mapleridge.ca · 2026 property tax rates'),

    # 4. Village of Belcarra bylaws page (https://belcarra.ca/bylaws) lists "2026 Tax Rates Bylaw No. 641-2026".
    (L + 'belcarra-port-moody.json',
     "Belcarra sets its own tax rates: the 2025 rates were set by Village of Belcarra 2025 Tax Rates Bylaw No. 634, 2025, and",
     "Belcarra sets its own tax rates: the 2026 rates are set by Village of Belcarra 2026 Tax Rates Bylaw No. 641-2026; the 2025 rates were set by Bylaw No. 634, 2025, and"),

    # 5. Burnaby sports field status (https://www.burnaby.ca/recreation-and-arts/recreation-facilities/sports-fields/sports-field-status,
    #    updated Nov 12, 2026): "West Field #1 | OPEN", "West Field #2 | OPEN".
    (L + 'burnaby-lake-houses-for-sale.json',
     'fields 1 and 2 at the west complex were closed from May and June 2026 for turf refurbishment, scheduled to reopen in September 2026, as field closures change by season.',
     'fields 1 and 2 at the west complex were closed from May 2026 for turf refurbishment and were open again on the City\'s field status page in November 2026; closures change by season.'),

    # 6. City of Coquitlam park projects (https://coquitlam.ca/1415/Park-and-Facility-Projects): "Construction will begin in May 2026,
    #    with an estimated reopening in winter 2027." "The remainder of the park will remain open during construction."
    (L + 'maillardville-coquitlam.json',
     "Mackin Park's north ball diamond was scheduled to close for upgrades starting in May 2026, one of four ball diamonds in the park,",
     "Mackin Park's north ball diamond is being renewed, with construction from May 2026 and reopening estimated for winter 2027 (the rest of the park stays open); it is one of four ball diamonds in the park,"),

    # 7. City of Mission, Centennial Park Japanese Tea House
    #    (https://www.mission.ca/business-building/current-city-projects/centennial-park-japanese-tea-house-project):
    #    "Construction is anticipated to begin late 2026, with an opening event to be scheduled in spring 2027."
    ('src/data/pages/mission-west-mission-guide.json',
     'Work is expected to start in October 2026, and an opening event is planned for early 2027',
     'Construction is anticipated to begin in late 2026, with an opening event to be scheduled in spring 2027'),

    # 8. BC Hydro Partial Cable Replacement, Coquitlam (https://www.bchydro.com/energy-in-bc/projects/partial-cable-replacement-coquitlam.html,
    #    newest section June 2026): pre-work "expected to resume in August 2026"; construction "expected to begin in spring 2027 and take
    #    about two years to complete". Reworded so the past date reads as BC Hydro's plan, not a forecast.
    (L + 'ranch-park-coquitlam.json',
     'pre-work pruning and vegetation removal along the corridor was expected to resume in August 2026, ahead of the spring 2027 construction start.',
     'BC Hydro planned pruning and vegetation removal along the corridor from August 2026, and expects construction to begin in spring 2027 and take about two years.'),

    # 9. FVRD project page (https://haveyoursay.fvrd.ca/crvssra, last updated Dec 6, 2025): still announces a workshop "this winter";
    #    no later update. Dated so it no longer reads as this coming winter.
    (L + 'chilliwack-river-valley.json',
     'a community workshop in the valley is planned for this winter.',
     'in December 2025 the FVRD said it would hold a community workshop in the valley that winter, and the page has not been updated since.'),
    (L + 'river-valley-guide.json',
     'a community workshop planned in the valley this winter; page last updated December 6, 2025',
     'a community workshop the FVRD said it would hold in the valley in winter 2025-26; page last updated December 6, 2025'),

    # 10. Township of Langley SSMUH page (https://www.tol.ca/en/the-township/small-scale-multi-unit-housing.aspx, read Nov 16, 2026):
    #     "The review is expected to be completed in late 2025"; new SSMUH water and sewer connections on hold until it is done.
    (L + 'sell-my-house-in-langley.json',
     'that the Township was updating its water and sewer master plans, expected by the end of 2025, with new connections for these homes deferred until that review is complete.',
     'that the Township was updating its water and sewer master plans. As of November 16, 2026 the Township\'s small-scale multi-unit housing page still says the review was expected to be completed in late 2025 and that new water and sewer connections for these homes are on hold until it is done.'),

    # 11. Province, health capital projects (https://www2.gov.bc.ca/gov/content/health/accessing-health-care/capital-projects,
    #     updated Oct 30, 2026) lists under "Projects underway": "A new 200-bed long-term care home to replace the 109-bed Cottage
    #     Worthington Pavilion", with no completion date. The 2027 date could not be confirmed, so it is dropped.
    (L + 'central-abbotsford-55-plus-homes-for-sale.json',
     'will replace the 109 beds at Cottage and Worthington Pavilion and add 91 more; construction was expected to begin in 2025 with completion in 2027. A senior counting on the Cottage Lane pavilions as the long-term plan should know the replacement is already in procurement/construction.',
     'will replace the 109 beds at Cottage and Worthington Pavilion and add 91 more. The Province lists it as a project underway but gives no completion date (as of November 2026). A senior counting on the Cottage Lane pavilions as the long-term plan should know the replacement is coming.'),

    # 12. No current City of Surrey page for this project was found on Nov 16, 2026; the sentence is dated rather than guessed.
    (L + 'fleetwood-tynehead-surrey-houses-for-sale.json',
     "The Fleetwood Athletic Park is a City capital project for the area, with design planned to begin in 2022 per the City's community page — check its current status before treating it as an existing amenity.",
     "The City's community page listed a Fleetwood Athletic Park as a capital project, with design planned to begin in 2022. No current City project page for it was found in November 2026, so ask the City before counting on it."),

    # 13. The Warwick (Albion): the answer did not answer the question. Same fact, said plainly; no new claim.
    (L + 'albion-maple-ridge-condos-townhomes-for-sale.json',
     '"Both signals exist: the project package estimated completion in August 2025."',
     '"The presale package estimated completion in August 2025, so homes there may now be finished. Check the listing and the strata plan for occupancy before treating any home there as a presale."'),
]

# source links swapped everywhere in these files (title and URL)
SWAPS = [
    ([L + f for f in ('abbotsford-55-plus-townhomes-for-sale.json', 'central-abbotsford-houses-for-sale.json', 'poplar-abbotsford-houses-for-sale.json',
                      'sumas-mountain-abbotsford-houses-for-sale.json', 'sumas-prairie.json')],
     [(ABB_25_URL, ABB_26_URL), (ABB_25_T, ABB_26_T)]),
    ([L + 'northeast-maple-ridge-guide.json'], [(MR_25_URL, MR_26_URL)]),
]


def main():
    edits = {}
    for rel, old, new in FIXES:
        edits.setdefault(rel, []).append((old, new, False))
    for files, pairs in SWAPS:
        for rel in files:
            for old, new in pairs:
                edits.setdefault(rel, []).append((old, new, True))
    changed = 0
    for rel, pairs in edits.items():
        path = ROOT / rel
        text = orig = path.read_text(encoding='utf-8')
        for old, new, every in pairs:
            if old in text:
                text = text.replace(old, new) if every else text.replace(old, new)
            elif new not in text:
                print(f'WARNING: not found in {rel}: {old[:70]}')
        if text != orig:
            json.loads(text)  # still valid JSON
            path.write_text(text, encoding='utf-8')
            changed += 1
            print(f'fixed: {rel}')
    print(f'{changed} file(s) changed')


if __name__ == '__main__':
    main()
