"""Port Coquitlam 55+ page, rewritten from Jared's verified local notes (Port_Coquitlam_55_local_notes.md, researched 2026-11-01).
The page is a guide to 55+ living, not a listings page: one 55+ strata complex exists in the city; everything else with a seniors name is
rental, care or subsidized housing and is labelled that way. Only facts the notes source are used; listing-stated figures are labelled; unconfirmed items say so.
Run after build_gap_pages.py (which skips this page: notes_page).   python3 -I tools/build_poco_55plus.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_snapstats_layers as L
import build_gap_pages as GP

ROOT = L.ROOT; SLUG = 'port-coquitlam-55-plus-homes-for-sale'; G = 'poco55'
f = os.path.join(ROOT, 'src/data/local', SLUG + '.json'); j = json.load(open(f, encoding='utf-8'))
old = j['blocks']
H = lambda t, l=2, **k: {'t': 'h', 'level': l, 'text': t, 'gen': G, **k}
P = lambda t, **k: {'t': 'p', 'text': t, 'gen': G, **k}
def LI(items): return {'t': 'list', 'items': [[{'t': i}] for i in items], 'gen': G}
def LK(items): return {'t': 'list', 'items': [[{'t': a, 'h': h}] for a, h in items], 'gen': G}

months = L.load_months(); keys = list(months); last = keys[-1]; mn, yr = L.month_name(last), last[:4]
cc = months[last]['areas']['port-coquitlam']['condo_townhome']['total']
market = GP.snap_months(months, 'port-coquitlam', 'Port Coquitlam', 'condo_townhome', keys)
end = [b for b in old if b.get('pos') == 'end']
links = [b for b in old if b['t'] == 'list' and b.get('gen') == 'gappage' and b not in end]

sources = [
 ('BC Government: age restriction bylaws in strata', 'https://www2.gov.bc.ca/gov/content/housing-tenancy/strata-housing/operating-a-strata/bylaws-and-rules/age-restriction-bylaws'),
 ('BC Government: strata rental changes, November 2022', 'https://www2.gov.bc.ca/gov/content/housing-tenancy/strata-housing/legislation-and-changes/changes-to-legislation'),
 ('BC Government: age-bylaw exemptions news release, 2023', 'https://archive.news.gov.bc.ca/releases/news_releases_2020-2024/2023HOUS0038-000601.htm'),
 ('City of Port Coquitlam: Zoning Bylaw No. 3630', 'http://www.portcoquitlam.ca/media/file/3630-zoning-bylaw-2008pdf'),
 ('City of Port Coquitlam: Social Housing & Services Resource Guide, 2020', 'https://www.portcoquitlam.ca/media/file/social-housing-services-resource-guide-2020v4'),
 ('City of Port Coquitlam: new community centre', 'https://www.portcoquitlam.ca/our-government/media-centre/new-community-centre-brings-amenities-excitement-port-coquitlam'),
 ('City of Port Coquitlam: Cedar drainage pump station', 'https://www.portcoquitlam.ca/our-government/capital-projects/cedar-drainage-pump-station-0'),
 ('BC Assisted Living Registry: Port Coquitlam residences', 'https://connect.health.gov.bc.ca/assisted-living-residence'),
 ('BC Housing: Zone 4 seniors and adults with disabilities directory', 'https://learningondemand.bchousing.org/sites/default/files/media/documents/Zone-4-Seniors-and-Adults-with-Disabilities.pdf'),
 ('Hawthorne Seniors Care Community', 'https://hawthornecare.com/'),
 ('Aspira Astoria Retirement Living', 'https://www.aspiralife.ca/our-locations/british-columbia/port-coquitlam/aspira-astoria-retirement-living/'),
 ('Fraser Health: Eagle Ridge Hospital', 'https://www.fraserhealth.ca/Service-Directory/Locations/Port-Moody/eagle-ridge-hospital'),
 ('TransLink: West Coast Express timetable', 'https://infomaps.translink.ca/Public_Timetables/213/tt997.pdf'),
 ('TransLink: Transport 2050, 10-Year Priorities', 'https://roar-assets-auto.rbl.ms/files/53822/attachment-2-transport-2050-10-year-priorities-for-translink.pdf'),
 ('Building records for Mayfair Terrace, 2266 Atkins Ave (BC Condos & Homes)', 'https://www.bccondosandhomes.com/index.php/building/mayfair-terrace-2266-atkins-ave'),
 ('Kew Lifestyles at Montrose (architect’s project page)', 'https://www.soarchitects.com/portfolio/kew-lifestyles-at-montrose-condominiums/'),
]
tab = [
 ['Mayfair Terrace', '2266 Atkins Ave', '55+ strata ownership', '46 units, built 2000', 'Yes. The only 55+ strata ownership building found in the city'],
 ['Kew Lifestyles at Montrose', '2430 Mary Hill Rd', '55+ purpose-built rental', '56 units, completed 2023', 'No. Rental only'],
 ['Aspira Astoria Retirement Living', '2245 Kelly Ave', 'Rental retirement residence (independent and assisted living)', 'Unit count and year opened unconfirmed', 'No. Rental'],
 ['Hawthorne Seniors Care Community', '2111 Hawthorne Ave', 'Non-profit campus: assisted living (70 suites), long-term care (131 beds), secure dementia cottages', '70 suites and 131 beds', 'No. Publicly funded care'],
 ['Shaughnessy Seniors Community', '2250 Wilson Ave', 'Long-term care residence', 'Not stated in sources', 'No. Care only'],
 ['Dogwood Manor', '3155 Seymour St', 'Subsidized, rent-geared-to-income seniors apartments', '24 units, built 1960', 'No. Subsidized rental'],
 ['Dogwood Place', '3125 Seymour St', 'Subsidized, rent-geared-to-income seniors apartments', '31 units, built 1973', 'No. Subsidized rental'],
 ['RJ Kent Manor (Royal Canadian Legion Branch 133)', 'Street address unconfirmed', 'Supportive housing for low-income seniors', '54 units, 25 of them subsidized (2008 news release)', 'No. Supportive housing'],
]
bl = [
 {'t': 'notice', 'text': 'Draft for Jared\'s approval. Written from Jared\'s verified local notes (researched November 1, 2026) and the monthly SnapStats figures. Anything the sources do not state is marked unconfirmed. No live feed filtered to 55+ homes yet.', 'gen': G},
 P('Port Coquitlam has one 55+ strata complex that you can buy into: Mayfair Terrace, 46 homes on Atkins Avenue downtown. Almost everything else in the city with a seniors name on it is rental, assisted living, long-term care or subsidized housing. This page sorts out which is which, explains how BC’s 55+ rules work for buyers, and gives the market figures for condos and townhomes in the city.'),
 {'t': 'grid', 'gen': G},
 H('Mayfair Terrace, 2266 Atkins Avenue: the 55+ strata in Port Coquitlam'),
 P('Mayfair Terrace is a four-storey freehold strata (plan LMS4171) built in 2000 with 46 units, in the CD-19 comprehensive development zone created for the project. MLS® property data records the age restriction as 55+. Building records show pets allowed with restrictions, and current listings specify lap pets. Listings also state that rentals are allowed, secure underground parking and a storage locker come with units, and the amenities include a community dining room, games room, hair salon, exercise room, theatre and an outdoor greenhouse.'),
 P('The catch is a second monthly charge. An October 2026 listing for the building states a mandatory base service plan on top of the strata fee: $715 a month for the first resident and $400 for a second, covering daily breakfast plus 10 meals, weekly housekeeping, a 24-hour emergency response system, activities and transportation. These are listing-stated figures. Confirm the current amounts in the strata documents and the service agreement before you rely on them.'),
 P('The services side of the same complex is registered with BC’s Assisted Living Registry as Aspira Mayfair Retirement Living, 2267 Kelly Avenue, which is the Kelly Avenue frontage of the building. That means a unit is an independent-living home with services attached, not a standard condo with a large strata fee.'),
 H('Seniors housing in Port Coquitlam: what you can buy and what you cannot'),
 {'t': 'table', 'caption': 'Seniors housing in Port Coquitlam, by type', 'head': ['Name', 'Address', 'What it is', 'Size', 'Can you buy in?'], 'rows': tab,
  'source': 'Sources: building records and MLS® property data for Mayfair Terrace; the architect’s project page for Kew Lifestyles; BC’s Assisted Living Registry; the City of Port Coquitlam’s 2020 resource guide; Hawthorne Seniors Care Community; BC Government news release (2008). Listed in the Sources section below. Where no source states a figure it is marked unconfirmed.', 'gen': G},
 P('Kew Lifestyles at Montrose is the newest 55+ building in the city, a 56-unit, five-storey purpose-built rental by Quantum Properties completed in 2023 beside the Port Coquitlam Community Centre. It is rental only, with nothing to buy. No new age-restricted strata project appears in any source checked, so the supply of 55+ homes you can own is still Mayfair Terrace.'),
 H('Where 55+ housing is in Port Coquitlam'),
 P('It is concentrated downtown, within a few blocks of Wilson Avenue and the Community Centre: Atkins Avenue (Mayfair Terrace), Kelly Avenue (Aspira Astoria and Aspira Mayfair), Mary Hill Road (Kew Lifestyles) and Hawthorne Avenue. The exception is the two Dogwood buildings on Seymour Street in Lincoln Park on the north side. No source shows a 55+ complex on Prairie Avenue or along the Oxford Heights and Coast Meridian corridor, so a 55+ cluster there is unconfirmed.'),
 P('Some names look like 55+ housing here but are not. The Shaughnessy at 2789 Shaughnessy Street is a 26-storey, 167-unit market condo tower built in 2012 with no age restriction in any source. No manufactured-home park was found inside Port Coquitlam: Hideaway Park (55+) and Wildwood Park, which come up in searches, are both in the City of Coquitlam, and so are the 55+ buildings Marlborough House and Princess Gate.'),
 {'t': 'list', 'items': [[{'t': 'Coquitlam 55+ homes for sale', 'h': '/coquitlam-55-plus-homes-for-sale.html'}], [{'t': 'Coquitlam mobile homes for sale', 'h': '/coquitlam-mobile-homes-for-sale.html'}], [{'t': 'Port Coquitlam homes for sale', 'h': '/port-coquitlam-homes-for-sale.html'}]], 'gen': G},
 H('How BC’s 55+ rules work for buyers'),
 LI(['Only 55+ age bylaws are valid in a BC strata. Under sections 123.1 and 123.2 of the Strata Property Act a strata may restrict residents to age 55 or older, and any age bylaw set below 55 has been invalid since November 24, 2022.',
     'The bylaw limits who may live in a unit, not who may own it. The Province states that people under 55 can own a strata lot in a 55+ corporation but may not be able to live in it.',
     'Built-in exemptions apply to residents who were lawfully living in the unit when the bylaw passed, live-in caregivers and, since May 1, 2023, a younger spouse or partner, a child under 19 in the resident’s care, and an adult child the resident cared for before the child turned 19.',
     'Rental-restriction bylaws have been void across BC since November 24, 2022, but a tenant must still satisfy the age bylaw or an exemption, and a strata can still limit short-term rentals.',
     'Port Coquitlam’s zoning is set by Zoning Bylaw No. 3630. Mayfair Terrace sits in a site-specific CD-19 zone.']),
 H('Living downtown: what is close and what is not'),
 P('The $132-million Port Coquitlam Community Centre at 2150 Wilson Avenue, 205,000 square feet, fully opened on October 2, 2021 with three arenas, a leisure pool, a fitness centre and the Terry Fox Library, and it is walkable from every downtown 55+ building above. The West Coast Express stops at Port Coquitlam Station, 2125 Kingsway Avenue, but it is a commuter train: five trains each way on weekdays and none on weekends or holidays, per TransLink’s timetable effective January 5, 2026. Everyday transit is local bus.'),
 P('SkyTrain does not reach Port Coquitlam, and none is funded. TransLink’s Transport 2050 10-Year Priorities commit only to an exploratory business case for a Millennium Line extension, which the Mayors’ Council work plan of February 19, 2026 still lists as underway, with no route, stations, funding or dates. The nearest hospital is Eagle Ridge Hospital at 475 Guildford Way in Port Moody; Port Coquitlam has none of its own.'),
 P('Parts of low-lying Port Coquitlam sit behind the Pitt River dike system, and flood status has to be checked lot by lot. The City is rebuilding the Cedar Drainage Pump Station, with construction from summer 2026 to summer 2027 and completion expected in late summer 2027.'),
 H('Port Coquitlam condos and townhomes: the market, not only 55+'),
 P(f'The monthly reports cover every condo and townhome in the city, not just 55+ buildings, and do not flag age restrictions. In {mn} {yr} the city had {L.num(cc["inventory"])} condos and townhomes listed and {L.num(cc["sales"])} sold.'),
 *[b for b in market if b['t'] in ('table', 'p')],
 H('Before you buy a 55+ home'),
 LI(['Read the age bylaw itself and ask which exemptions the strata has recorded for the unit.', 'Ask for the service agreement if the building has a mandatory service plan, and for the current monthly amounts.', 'Ask for the Form B, the depreciation report, the meeting minutes and the bylaws.', 'Check parking and storage for the specific unit.']),
 *links,
 H('Sources'),
 P('Facts on this page come from these public sources, read on November 1, 2026.'),
 LK(sources),
 *end,
]
faq = [
 {'q': 'Is Port Coquitlam a buyers’ or sellers’ market for condos and townhomes?', 'a': f'In {mn} {yr} condos and townhomes in Port Coquitlam had a sales ratio of {L.pct(cc["ratio"])}, which the reports’ scale reads as {L.kind(cc["ratio"])}. On that scale under 12% favours buyers, 12% to 20% is balanced and over 20% favours sellers. The figure covers all condos and townhomes in the city, not only 55+ buildings.'},
 {'q': 'How many 55+ strata buildings are there in Port Coquitlam?', 'a': 'One was found: Mayfair Terrace, 2266 Atkins Avenue, built in 2000 with 46 units. Other seniors housing in the city is rental, assisted living, long-term care or subsidized housing, and no new age-restricted strata project appears in the sources checked.'},
 {'q': 'Is there a second mandatory monthly charge at Mayfair Terrace?', 'a': 'An October 2026 listing states a mandatory base service plan on top of the strata fee: $715 a month for the first resident and $400 for a second, covering meals, housekeeping, 24-hour emergency response, activities and transportation. These are listing-stated figures, so confirm the current amounts in the strata documents and the service agreement.'},
 {'q': 'My spouse is under 55. Can we both live in a 55+ strata?', 'a': 'Yes. Provincial rules require an exemption for a younger spouse or partner of a resident who meets the age requirement or holds a legacy exemption. Children are exempt in defined cases: a child under 19 in the resident’s care, and an adult child the resident cared for before the child turned 19.'},
 {'q': 'I am under 55. Can I buy in a 55+ building for a parent or as an investment?', 'a': 'Ownership is not age-restricted, but the bylaw governs who may live in the unit. The Province states that under-55s can own a strata lot in a 55+ corporation but may not be able to live in it, and a parent who is 55 or older can be the resident.'},
 {'q': 'Can I rent out my unit in a 55+ building?', 'a': 'Long-term rental bans are no longer valid in BC, and listings for Mayfair Terrace state that rentals are allowed. The tenant must still meet the 55+ bylaw or an exemption, and a strata can still restrict short-term rentals.'},
 {'q': 'Does the 55+ restriction shrink my resale buyer pool?', 'a': 'Yes. The next buyer must be able to live there under the bylaw: 55 or older, an exempt spouse, partner or caregiver, a legacy case, or someone who buys without living in the unit.'},
 {'q': 'Are pets allowed in Port Coquitlam 55+ buildings?', 'a': 'It is building by building. Building records for Mayfair Terrace show pets allowed with restrictions, and current listings specify lap pets. Aspira Astoria, the rental residence on Kelly Avenue, describes itself as pet-friendly.'},
 {'q': 'Is there a 55+ manufactured-home park in Port Coquitlam?', 'a': 'None was found inside the city. Hideaway Park (55+) and Wildwood Park, which come up in searches, are both in the City of Coquitlam.'},
 {'q': 'Where is the nearest hospital to downtown Port Coquitlam?', 'a': 'Port Coquitlam has no hospital of its own. The Tri-Cities hospital is Eagle Ridge Hospital at 475 Guildford Way in Port Moody, a Fraser Health community hospital with a 24/7 emergency department.'},
 {'q': 'What transit can I use day to day?', 'a': 'The West Coast Express stops at Port Coquitlam Station but runs only five trains each way on weekdays, with no weekend or holiday service. SkyTrain does not reach the city, so local buses are the everyday option.'},
 {'q': 'If I need more care later, can I stay in Port Coquitlam?', 'a': 'There is a ladder in the city: independent strata living with a service plan at Mayfair Terrace, rental independent and assisted living such as Aspira Astoria and the 70 assisted-living suites at Hawthorne Tower, then long-term care at Hawthorne Lodge (131 beds) and Shaughnessy Seniors Community. Hawthorne’s programs are publicly funded through Fraser Health.'},
]
j['blocks'] = bl; j['faq'] = faq; j['notes_page'] = True; j['gen_gap'] = True; j['hand_edited'] = True
j['new_page'] = {'title': 'Port Coquitlam 55+ Homes: Mayfair Terrace and Rules | Jared Gibbons', 'description': 'Port Coquitlam 55+ homes: the one 55+ strata complex, what is rental or care, BC age-bylaw rules and market figures. Jared Gibbons, REALTOR®.', 'h1': 'Port Coquitlam 55+ Homes for Sale | Metro Vancouver Real Estate'}
j['faq_heading'] = 'Port Coquitlam 55+ homes: your questions answered'
j['needs_from_muse'] = ['Jared’s own notes on Mayfair Terrace: how units sell, what buyers ask, any recent sales (the sold export has fewer than 3 closed sales there in the last 12 months, so none are quoted)', 'Current Mayfair Terrace service-plan amounts from the strata or service agreement', 'Street address of RJ Kent Manor, unit counts for Aspira Astoria and Shaughnessy Seniors Community', 'Live listing feed filtered to 55+ homes']
json.dump(j, open(f, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(f, 'a').write('\n')
print('wrote', SLUG, len(bl), 'blocks', len(faq), 'faq')
