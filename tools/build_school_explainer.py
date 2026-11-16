#!/usr/bin/env python3
"""One page that explains what every "Homes for sale near <school>" page used to repeat (D-321): how the school searches and the
sold figures work, catchment versus distance, and the checklist before an offer. The 160 school pages now keep only what is
specific to their school and link here (GenericPage.astro).

    python3 -I tools/build_school_explainer.py   -> src/data/local/buying-a-home-near-a-school-bc.json
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from build_post_rewrites import parts  # noqa: E402

SLUG = 'buying-a-home-near-a-school-bc'
G = 'schoolx'
FIND = {'Surrey': 'https://mybaragar.com/index.cfm?event=page.SchoolLocatorPublic&DistrictCode=BC36',
        'Langley': 'https://mybaragar.com/index.cfm?event=page.SchoolLocatorPublic&DistrictCode=BC35',
        'Delta': 'https://mybaragar.com/index.cfm?event=page.SchoolLocatorPublic&DistrictCode=BC37',
        'Abbotsford': 'http://mybaragar.com/index.cfm?event=page.SchoolLocatorPublic&DistrictCode=BC34',
        'Francophone (CSF)': 'https://www.csf.bc.ca/transport/zones-de-frequentation/'}


def P(t): return {'t': 'p', 'parts': parts(t), 'gen': G} if ('[' in t or '**' in t) else {'t': 'p', 'text': t, 'gen': G}
def H(t, **k): return {'t': 'h', 'level': 2, 'text': t, 'gen': G, **k}
def L(*items): return {'t': 'list', 'items': [parts(i) for i in items], 'gen': G}


BLOCKS = [
    P('Most of my school pages answer one question: what is for sale near this school, and what do homes around it sell for? This page explains how those pages work and what to check before you write an offer on a home because of a school.'),
    H('How the school searches work', id='how-the-search-works'),
    P('MLS® listings are not tagged by school. Each school page shows the houses, townhomes and condos whose description names the school. So a home close to the school whose listing leaves the name out will not appear, and a listing that names the school can be some distance away. If you want a specific school, ask me to watch for homes near it that the search misses.'),
    H('How the sold prices are measured', id='how-the-sold-prices-work'),
    P('The sold figures on each school page come from Paragon, the MLS® system my office uses: closed and pending sales within 1 km of the school (2 km where few homes sold), for the twelve months shown on the page. A median is the middle price, so half sold for more and half for less, and it is shown only where at least 5 homes sold. A pending sale is firm but has not completed, so its price can still change. They are distance figures, not catchment figures: a home within 1 km may be in another school\'s catchment.'),
    H('Catchment is not distance', id='catchment'),
    P('Each school district draws its own catchment boundaries, and the nearest school is not always the one that serves an address. Confirm the exact address with the district before you offer:'),
    L(*[f'[{k} school catchment finder]({v})' for k, v in FIND.items()]),
    P('Districts review boundaries from time to time, and a school that is full may not take students from outside its catchment. If the school is the reason you are buying, ask the district about both before you remove subjects.'),
    H('Before you offer on a home near a school', id='before-you-offer'),
    L('**Confirm the catchment for the exact address**, on the district finder above. A home a few blocks from a school can sit in a different catchment.',
      '**Visit on a school day at drop-off and pick-up.** Traffic, parking and noise around 8:30 am and 3 pm are different from a Sunday showing.',
      '**Compare the price with similar homes farther from the school.** Each school page gives the median near the school; check whether size and age explain a gap before you pay for the location.',
      '**Look at the next-nearest school too.** Each school page lists the other schools within 3 km, so you can compare the two when you check which one serves the address.'),
    H('Schools by city'),
    L('[Schools in Surrey](/schools-in-surrey-bc.html)', '[Schools in Langley](/schools-in-langley-bc.html)', '[Schools in Delta](/schools-in-delta-bc.html)',
      '[Schools in Abbotsford](/schools-in-abbotsford-bc.html)', '[Buying a home in BC](/buying.html)'),
]
FAQ = [
    {'q': 'Does a home near a school guarantee a spot there?', 'a': 'No. The district sets the catchment, and the nearest school is not always the one that serves an address. Confirm the exact address on the district\'s catchment finder before you offer.'},
    {'q': 'Why does a listing near the school not appear on its page?', 'a': 'The school pages show listings whose MLS® description names the school. A home close by whose listing leaves the name out will not appear; Jared can watch for those.'},
    {'q': 'How are the sold prices near a school measured?', 'a': 'From Paragon closed and pending sales within 1 km of the school (2 km where few sold), over twelve months. A median is shown only where at least 5 homes sold.'},
    {'q': 'Can I book a private showing with Jared?', 'a': 'Yes. Jared Gibbons, REALTOR® with Royal LePage Little Oak Realty, books private showings across the Fraser Valley and Metro Vancouver. Call or text 604-928-1361, or use the contact form on this site.'},
]


def main():
    d = {'status': 'draft', 'slug': SLUG, 'updated': '2026-11-16', 'hand_edited': True,
         'new_page': {'title': 'Buying a Home Near a School in BC | Jared Gibbons',
                      'description': 'Buying near a school in BC: catchment versus distance, the district catchment finders, how school-area sold prices work, and what to check first.',
                      'h1': 'Buying a Home Near a School in BC'},
         'breadcrumbs': [{'name': 'Home', 'href': '/'}, {'name': 'Buying', 'href': '/buying.html'}, {'name': 'Buying a Home Near a School', 'href': f'/{SLUG}.html'}],
         'faq_heading': 'Buying near a school: your questions answered', 'faq': [dict(f, gen=G) for f in FAQ], 'blocks': BLOCKS}
    assert len(d['new_page']['description']) <= 155
    (ROOT / 'src/data/local' / f'{SLUG}.json').write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
    print('wrote', SLUG)


if __name__ == '__main__':
    main()
