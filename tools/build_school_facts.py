#!/usr/bin/env python3
"""School facts for the "homes near a school" pages -> src/data/schools/facts.json

Source: the BC Data Catalogue "BC Schools - School Locations" dataset (DataBC, Open Government Licence - BC) plus each district's own website, as retrieved 2026-11-04/05
(bc_schools_all_districts_2026-11-05.zip, folders SD33-37 and SD38-93).  Names, addresses, coordinates, grades, programs, district school page and catchment page only.
No ratings, rankings or descriptions.   python3 -I tools/build_school_facts.py /path/to/unzipped/bc_schools_all_districts
"""
import csv, glob, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
src = sys.argv[1] if len(sys.argv) > 1 else '/tmp/sch'
out = []
for d in ('SD33-37', 'SD38-93'):
    cat = {}
    for f in glob.glob(f'{src}/{d}/sd*_catchments.csv'):
        for r in csv.DictReader(open(f, encoding='utf-8')):
            cat[(r['district_number'], r['school_name'])] = (r['catchment_page_url'], r['catchment_coverage'])
    for f in sorted(glob.glob(f'{src}/{d}/sd*_schools.csv') + glob.glob(f'{src}/{d}/sd*_independent_schools.csv')):
        indep = 'independent' in f
        for r in csv.DictReader(open(f, encoding='utf-8')):
            try: lat, lon = float(r['latitude']), float(r['longitude'])
            except (ValueError, KeyError): lat = lon = None
            cu, cc = cat.get((r['district_number'], r['school_name']), ('', ''))
            out.append(dict(name=r['school_name'], district=int(r['district_number']), district_name=r['district_name'], level=r['level'], grades=r['grades'], programs=r['programs'],
                            address=r['street_address'], city=r['city'], postal=r['postal_code'], lat=lat, lon=lon, url=r['school_url'], independent=indep, catchment_url=cu, catchment=cc))
seen=set(); out=[o for o in out if not ((o['name'],o['address']) in seen or seen.add((o['name'],o['address'])))]
fix = json.load(open('src/data/schools/coordinate-fixes.json')) if os.path.exists('src/data/schools/coordinate-fixes.json') else []   # schools the official dataset has no coordinates for, with the source of each fix
for o in out:
    for x in fix:
        if (o['lat'] is None or x.get('override')) and o['name'] == x['name'] and o['address'] == x['address']: o['lat'], o['lon'] = x['lat'], x['lon']
json.dump(out, open('src/data/schools/facts.json', 'w'), indent=0, ensure_ascii=False)
print(len(out), 'schools;', sum(1 for s in out if s['lat']), 'with coordinates')
