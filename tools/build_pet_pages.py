#!/usr/bin/env python3
"""Pet-friendly condo and townhome pages, South Surrey / White Rock and Langley (D-314).

    python3 -I tools/build_pet_pages.py   -> src/data/local/<slug>.json (4 pages)

The words here do not change with the data. The counts, the "no pets" and "cats, not dogs" lists and the table for every complex
are added at build time by GenericPage.astro from src/data/strata-rules.json (tools/build_strata_rules.py, Pete's workbook), so a
new workbook updates all four pages without touching this file.
BC rules are from the Province's strata pet bylaw page and BCFSA's note on Bill 44 (both read November 16, 2026).
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from build_post_rewrites import parts  # noqa: E402

LOCAL = ROOT / 'src/data/local'
DAY = '2026-11-16'
G = 'pet'
GOV = 'https://www2.gov.bc.ca/gov/content/housing-tenancy/strata-housing/operating-a-strata/bylaws-and-rules/pet-bylaws'
BCFSA = 'https://bcfsa.ca/about-us/news/news-release/bc-government-ends-rental-and-age-restrictions-strata-properties'


def P(t): return {'t': 'p', 'parts': parts(t), 'gen': G} if ('[' in t or '**' in t) else {'t': 'p', 'text': t, 'gen': G}
def H(t, level=2): return {'t': 'h', 'level': level, 'text': t, 'gen': G}
def L(*items): return {'t': 'list', 'items': [parts(i) for i in items], 'gen': G}


DATA = {'t': 'petdata', 'gen': G}   # replaced at build time (GenericPage.astro, D-314)
GRID = {'t': 'grid', 'gen': G}

AREAS = {
    'ss': {'name': 'South Surrey and White Rock', 'short': 'South Surrey', 'crumb': ('South Surrey', '/south-surrey-homes-for-sale.html'),
           'hoods': 'White Rock, Grandview Heights, the King George corridor, Morgan Creek, Sunnyside Park and Pacific Douglas',
           'condo': '/south-surrey-condos-for-sale.html', 'town': '/south-surrey-townhomes-for-sale.html',
           '55': ('/south-surrey-white-rock-55-plus-condos-for-sale.html', '/south-surrey-white-rock-55-plus-townhomes-for-sale.html')},
    'lan': {'name': 'Langley', 'short': 'Langley', 'crumb': ('Langley', '/langley-homes-for-sale.html'),
            'hoods': 'Willoughby, Langley City, Walnut Grove, Murrayville, Aldergrove and Fort Langley',
            'condo': '/langley-condos-for-sale.html', 'town': '/langley-townhomes-for-sale.html',
            '55': ('/langley-55-plus-condos-for-sale.html', '/langley-55-plus-townhomes-for-sale.html')},
}
KINDS = {
    'condos': {'Kind': 'Condos', 'one': 'condo building', 'many': 'condo buildings', 'home': 'condo'},
    'townhomes': {'Kind': 'Townhomes', 'one': 'townhouse complex', 'many': 'townhouse complexes', 'home': 'townhome'},
}
SLUGS = {('ss', 'condos'): 'south-surrey-white-rock-pet-friendly-condos-for-sale', ('ss', 'townhomes'): 'south-surrey-white-rock-pet-friendly-townhomes-for-sale',
         ('lan', 'condos'): 'langley-pet-friendly-condos-for-sale', ('lan', 'townhomes'): 'langley-pet-friendly-townhomes-for-sale'}
TITLES = {('ss', 'condos'): 'Pet-Friendly Condos for Sale in South Surrey & White Rock',
          ('ss', 'townhomes'): 'Pet-Friendly Townhomes for Sale in South Surrey & White Rock',
          ('lan', 'condos'): 'Pet-Friendly Condos for Sale in Langley',
          ('lan', 'townhomes'): 'Pet-Friendly Townhomes for Sale in Langley'}
META = {('ss', 'condos'): ('Pet-Friendly Condos South Surrey & White Rock', 'Pet-friendly condos for sale in South Surrey and White Rock: dogs, cats and how many pets each building allows, per MLS® listings.'),
        ('ss', 'townhomes'): ('Pet-Friendly Townhomes South Surrey & White Rock', 'Pet-friendly townhomes for sale in South Surrey and White Rock: dogs, cats and how many pets each complex allows, per MLS® listings.'),
        ('lan', 'condos'): ('Pet-Friendly Condos for Sale in Langley, BC', 'Pet-friendly Langley condos for sale: dogs, cats and how many pets each building in Willoughby, Langley City and Walnut Grove allows.'),
        ('lan', 'townhomes'): ('Pet-Friendly Townhomes for Sale in Langley, BC', 'Pet-friendly Langley townhomes for sale: dogs, cats and how many pets each complex in Willoughby, Walnut Grove and Murrayville allows.')}


def build(a, k):
    A, K, slug = AREAS[a], KINDS[k], SLUGS[(a, k)]
    other = SLUGS[(a, 'townhomes' if k == 'condos' else 'condos')]
    twin = SLUGS[('lan' if a == 'ss' else 'ss', k)]
    hub = A['condo'] if k == 'condos' else A['town']
    p55 = A['55'][0 if k == 'condos' else 1]
    title, desc = META[(a, k)]
    title = title + ' | Jared Gibbons' if len(title) <= 44 else title
    assert len(title) <= 60 and len(desc) <= 155, (slug, len(title), len(desc))
    blocks = [
        P(f'Most {K["many"]} in {A["name"]} allow a pet, but the limits differ: some take one dog or one cat, some two pets, and a few take no dogs or no pets at all. '
          f'Below is what the MLS® listings in each {K["one"]} say, so you can rule complexes in or out before you book a showing. It covers {A["hoods"]}.'),
        L(f'[Every {A["short"]} {K["home"]} for sale]({hub})', f'[Pet-friendly {"townhomes" if k == "condos" else "condos"} in {A["name"]}](/{other}.html)',
          f'[55+ {K["home"]}s in {A["name"]}]({p55})', '[Call or text Jared: 604-928-1361](tel:+16049281361)'),
        H(f'{A["name"]} {K["home"]}s for sale now'),
        P(f'These are all the {K["home"]}s for sale in {A["name"]}, not only pet-friendly ones. Check the complex in the tables below, then ask me for the bylaws before you write an offer.'),
        GRID,
        H('How to read the tables'),
        L('**Pets:** "Yes, with limits" means the listings say pets are allowed with restrictions; "No" means they say no pets; "Ask me" means listings in the same complex disagree; "Not stated" means none of them say.',
          '**Dogs and Cats:** what the listings\' dog and cat fields say. A dash means the listings leave them blank.',
          '**How many:** the number of pets the listings give, when they all give the same number.'),
        DATA,
        H('What "pets allowed, with limits" usually means'),
        L('**How many:** most listings that give a number say one or two pets. The Province\'s standard bylaw, which applies when a strata has not written its own, allows one dog or one cat, up to two caged birds, and a reasonable number of fish or small caged animals.',
          '**What kind:** a strata can limit the kind of pet, not just the number, and some limit dogs by size or weight.',
          '**Where:** leash rules, no pets in the pool or gym, and which elevator to use are in the bylaws and rules.',
          f'**Renting it out later:** your tenant is bound by the same pet bylaws. Since November 24, 2022 a BC strata cannot ban or cap long-term rentals ([BCFSA]({BCFSA})), so renting is allowed in every building on this page; short-term stays such as Airbnb can still be banned.'),
        H('BC strata pet rules every buyer should know'),
        L(f'**A pet already living there can stay.** If the strata passes a new pet bylaw, pets living in the home at that time are exempt, but a replacement pet has to meet the new bylaw ([Province of BC]({GOV})).',
          f'**Certified guide and service dogs are exempt.** Owners, tenants and visitors can keep a certified guide or service dog regardless of a strata\'s pet bylaws ([Province of BC]({GOV})).',
          '**The listing is not the bylaw.** Listing fields are filled in by the seller\'s agent and are sometimes out of date. The bylaws in the Form B package are what count, and rules passed at the last meeting are in the minutes.',
          '**Ask before you remove subjects.** Ask the strata manager in writing whether your pet, by kind, number and size, is allowed, and keep the answer with your offer. I can do this for you.'),
        P(f'Looking in {"Langley" if a == "ss" else "South Surrey and White Rock"} too? See [pet-friendly {k} there](/{twin}.html).'),
    ]
    faq = [
        {'q': f'Which {K["many"]} in {A["name"]} allow dogs?', 'a': f'Most do. The tables on this page show, for every {K["one"]} with recent MLS® listings, whether the listings say dogs and cats are allowed and how many pets. A short list of buildings say no pets or cats only. Confirm in the bylaws before you buy.'},
        {'q': f'Can a strata in BC ban pets?', 'a': 'Yes. A strata corporation can ban pets or limit their number and kind by bylaw. A pet already living in the home when a new bylaw passes can stay, and certified guide and service dogs are exempt from pet bylaws.'},
        {'q': 'How many pets are allowed in a BC strata?', 'a': 'It depends on the strata\'s bylaws. If it has not written its own, the Province\'s standard bylaw allows one dog or one cat, up to two caged birds, and a reasonable number of fish or small caged animals. Many complexes allow two pets.'},
        {'q': 'Where do I find the pet bylaws before I buy?', 'a': 'In the strata documents: the bylaws, the rules and the minutes, which come with the Form B. Before you remove subjects, ask the strata manager in writing whether your pet is allowed; Jared can do this for you.'},
        {'q': f'Can I rent out a {K["home"]} in {A["name"]}?', 'a': 'Long-term, yes. Since November 24, 2022 a BC strata cannot ban or cap long-term rentals. A strata can still ban short-term stays such as Airbnb, and your tenant must follow the pet bylaws.'},
        {'q': 'Can I book a private showing with Jared?', 'a': 'Yes. Jared Gibbons, REALTOR® with Royal LePage Little Oak Realty, books private showings across the Fraser Valley and Metro Vancouver. Call or text 604-928-1361, or use the contact form on this site.'},
    ]
    h1 = TITLES[(a, k)]
    return slug, {'status': 'draft', 'slug': slug, 'updated': DAY, 'hand_edited': True, 'pet_page': True,
                  'new_page': {'title': title, 'description': desc, 'h1': h1},
                  'breadcrumbs': [{'name': 'Home', 'href': '/'}, {'name': A['crumb'][0], 'href': A['crumb'][1]},
                                  {'name': f'{A["short"]} {K["Kind"].lower()}', 'href': hub}, {'name': h1.replace(' for Sale', ''), 'href': f'/{slug}.html'}],
                  'faq_heading': f'Pet-friendly {k} in {A["name"]}: your questions answered',
                  'faq': [dict(f, gen=G) for f in faq], 'blocks': blocks}


def main():
    for a in AREAS:
        for k in KINDS:
            slug, d = build(a, k)
            (LOCAL / f'{slug}.json').write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
            print('wrote', slug, d['new_page']['title'])


if __name__ == '__main__':
    main()
