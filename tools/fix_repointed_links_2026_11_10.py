"""Second look at the D-193 repointed outside links (D-200, 2026-11-10).

All 93 outside URLs that the D-193 link run added were opened again in Chrome. 91 load; two Safeway store pages moved again (404).
Several repoints went to a parent page when the exact page still exists under a new address (a "zoning bylaw" source pointing at a
general "Development Planning" page). Each rule below sends the link to the exact page, matched on the current URL and the link's label,
and fixes the label where it was a file name. Idempotent. python3 -I tools/fix_repointed_links_2026_11_10.py"""
import collections, glob, json, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
# (current url, label must match, new url, new label or None)
RULES = [
    ('https://www.abbotsford.ca/business-development/development-planning', r'zoning bylaw',
     'https://laws.abbotsford.ca/civix/content/coa/coabylaws/z/zoning/?xsl=/templates/browse.xsl', 'abbotsford.ca · Zoning Bylaw 2400-2014'),
    ('https://www.abbotsford.ca/business-development/community-planning', r'official community plan',
     'https://laws.abbotsford.ca/civix/content/coa/coabylaws/o/ocp/?xsl=/templates/browse.xsl', 'abbotsford.ca · Official Community Plan (Bylaw 2600-2016)'),
    ('https://www.mapleridge.ca/build-do-business/community-planning', r'zoning',
     'https://www.mapleridge.ca/build-do-business/community-planning/zoning-bylaw', 'mapleridge.ca · Zoning Bylaw'),
    ('https://www.portmoody.ca/business-development-and-planning/development/', r'zoning',
     'https://www.portmoody.ca/business-development-and-planning/zoning/', 'portmoody.ca · Zoning Bylaw'),
    ('https://www.portmoody.ca/business-development-and-planning/community-planning/', r'official community plan',
     'https://www.portmoody.ca/business-development-and-planning/official-community-plan/', 'portmoody.ca · Official Community Plan'),
    ('https://www.newwestcity.ca/city_hall/bylaws.php', r'zoning',
     'https://www.newwestcity.ca/zoning-bylaw', 'newwestcity.ca · Zoning Bylaw No. 6680, 2001'),
    ('https://www.delta.ca/parks-recreation/sports-activities/recreation-facilities', r'ladner leisure',
     'https://www.delta.ca/parks-recreation/parks-trails/park-and-amenity-search/ladner-leisure-centre', None),
    ('https://www.delta.ca/services/water-sewer-drainage', r'flood|^Source: delta\.ca$',
     'https://www.delta.ca/services/water-sewer-drainage/sanitary-sewer-drainage', None),
    ('https://www.surrey.ca/renovating-building-development/land-planning-development/land-use-planning', r'fleetwood',
     'https://www.surrey.ca/renovating-building-development/land-planning-development/land-use-planning/fleetwood-land-use-plans/fleetwood-town-centre-plan', 'surrey.ca · Fleetwood Town Centre Plan'),
    ('https://www.abbotsford.ca/roadclosures?page=2', r'.', 'https://www.abbotsford.ca/roadclosures', None),
    ('https://www.safeway.ca/find-a-store/store/4927-safeway-austin---marmont', r'.', 'https://www.safeway.ca/stores/safeway-austin-heights', 'safeway.ca · Safeway Austin Heights'),
    ('https://www.safeway.ca/find-a-store/store/4917-safeway-mcbride', r'.', 'https://www.safeway.ca/stores/safeway-mcbride', 'safeway.ca · Safeway McBride'),
    ('https://seasonsretirement.com/locations/seasons-wesbrook-village/', r'.', 'https://seasonsretirement.com/locations/seasons-wesbrook-village/', 'seasonsretirement.com · Chartwell Wesbrook Village'),
    ('https://www.cmhc-schl.gc.ca/en/nhs/first-time-home-buyer-incentive', r'^First-Time Home Buyer Incentive$',
     'https://www.cmhc-schl.gc.ca/en/nhs/first-time-home-buyer-incentive', 'First-Time Home Buyer Incentive (closed to new applications)'),
]
# words that went out of date with the links
TEXT = [(re.compile(r'\bthe Seasons Wesbrook Village retirement residence\b'), 'the Chartwell Wesbrook Village retirement residence (formerly Seasons Wesbrook)'),
        (re.compile(r'\bTapestry / Seasons Wesbrook Village retirement residence\b'), 'Tapestry / Chartwell Wesbrook Village retirement residence')]
stats = collections.Counter()


def walk(o):
    if isinstance(o, dict):
        h = o.get('h')
        for old, lab, new, newlab in RULES:
            label = str(o.get('t', ''))
            if h == old and re.search(lab, label, re.I):
                if new != old: o['h'] = new; stats['url ' + old.split('/')[2]] += 1
                if newlab and label != newlab: o['t'] = newlab; stats['label'] += 1
                break
        for k, v in list(o.items()):
            if isinstance(v, str) and k in ('t', 'text', 'a', 'q'):
                for rx, rep in TEXT:
                    v2, n = rx.subn(rep, v)
                    if n: o[k] = v = v2; stats['text'] += n
            else: walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)


changed = 0
for f in glob.glob(os.path.join(ROOT, 'src/data/**/*.json'), recursive=True):
    raw = open(f, encoding='utf-8').read()
    if not any(r[0] in raw for r in RULES) and 'Seasons Wesbrook' not in raw: continue
    d = json.loads(raw); before = json.dumps(d, ensure_ascii=False); walk(d)
    if json.dumps(d, ensure_ascii=False) != before:
        ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
        out = json.dumps(d, ensure_ascii=False, indent=ind) if ind else json.dumps(d, ensure_ascii=False, separators=(',', ':'))
        open(f, 'w', encoding='utf-8').write(out + ('\n' if raw.endswith('\n') else '')); changed += 1
print('files changed', changed, dict(stats))
