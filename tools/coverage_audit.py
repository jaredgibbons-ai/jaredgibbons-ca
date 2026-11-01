"""Coverage audit: which city x page-type combinations exist on the site, and which are missing.
    python3 -I tools/coverage_audit.py [--csv out.csv]
Reads slugs from src/data/pages and src/data/posts. Page types and city lists are the commercial-SEO checklist (docs/10)."""
import argparse, csv, glob, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
slugs = {os.path.basename(f)[:-5] for d in ('pages', 'posts') for f in glob.glob(os.path.join(ROOT, 'src/data', d, '*.json'))}

# city key -> (display, slug prefixes that mean this city)
CITIES = {
    'Surrey': ['surrey'], 'South Surrey': ['south-surrey'], 'White Rock': ['white-rock'], 'Langley (Township)': ['langley'],
    'Langley City': ['city-of-langley', 'langley-city'], 'Abbotsford': ['abbotsford'], 'Chilliwack': ['chilliwack'], 'Mission': ['mission'],
    'Maple Ridge': ['maple-ridge'], 'Pitt Meadows': ['pitt-meadows'], 'Delta (North)': ['north-delta', 'delta'], 'Ladner': ['ladner'],
    'Tsawwassen': ['tsawwassen'], 'Cloverdale': ['cloverdale'], 'Fort Langley': ['fort-langley'], 'Aldergrove': ['aldergrove'],
    'Walnut Grove': ['walnut-grove'], 'Willoughby': ['willoughby'], 'Murrayville': ['murrayville'], 'Brookswood': ['brookswood'],
    'Sardis': ['sardis'], 'Hope': ['hope'], 'Harrison Hot Springs': ['harrison'], 'Agassiz': ['agassiz'], 'Burnaby': ['burnaby'],
    'Richmond': ['richmond'], 'Coquitlam': ['coquitlam'], 'Port Coquitlam': ['port-coquitlam'], 'Port Moody': ['port-moody'],
    'New Westminster': ['new-westminster'], 'North Vancouver': ['north-vancouver'], 'West Vancouver': ['west-vancouver'], 'Vancouver': ['vancouver'],
    'Squamish': ['squamish'], 'Whistler': ['whistler'], 'Pemberton': ['pemberton'],
}
# page type -> slug suffixes (after the city prefix)
TYPES = {
    'homes for sale': ['homes-for-sale', 'houses-for-sale', 'real-estate'],
    'condos': ['condos-for-sale'], 'townhomes': ['townhomes-for-sale', 'townhouses-for-sale'], 'duplexes': ['duplexes-for-sale'],
    'acreages / farms': ['acreages-for-sale', 'farms', 'farms-for-sale'], 'mobile homes': ['mobile-homes', 'mobile-homes-for-sale'],
    '55+': ['55-plus-condos-for-sale', '55-plus-townhomes-for-sale'], 'luxury': ['luxury-homes', 'homes-over-1-8m'],
    'under-price pages': ['homes-under-1-8m', 'condos-under-800k', 'townhomes-under-1-2m'], 'new construction / presale': ['new-construction-presales', 'presale-condos'],
    'open houses': ['open-houses'], 'lots / land': ['lots-land'], 'foreclosure / court sales': ['foreclosures-court-ordered-sales'],
    'neighbourhood guides hub': ['neighbourhood-guides', 'neighbourhoods'],
    'SELL page': ['sell-my-house'], 'MOVING-TO page': ['moving-to'], 'SCHOOLS / catchments': ['school-catchments'],
    'MARKET-STATS page': ['market-stats', 'market-update'],
}

def has(city_prefixes, suffixes):
    for p in city_prefixes:
        for sfx in suffixes:
            if f'{p}-{sfx}' in slugs: return True
            if sfx.startswith('sell-my-house') and (f'sell-my-house-in-{p}' in slugs): return True
            if sfx == 'moving-to' and (f'moving-to-{p}' in slugs or any(s.startswith(f'moving-to-{p}') for s in slugs)): return True
            if sfx == 'market-update' and any(s.startswith(p) and 'market' in s for s in slugs): return True
    return False

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--csv'); a = ap.parse_args()
    rows = []; total = missing = 0
    for city, pre in CITIES.items():
        r = {'city': city}
        for t, sfx in TYPES.items():
            ok = has(pre, sfx); r[t] = 'Y' if ok else ''; total += 1; missing += 0 if ok else 1
        rows.append(r)
    for r in rows:
        have = sum(1 for t in TYPES if r[t]); print(f"{r['city']:<22} {have:>2}/{len(TYPES)}  missing: " + ', '.join(t for t in TYPES if not r[t])[:200])
    print(f'\ncells present: {total - missing} of {total}; missing: {missing}')
    if a.csv:
        with open(a.csv, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=['city'] + list(TYPES)); w.writeheader(); w.writerows(rows)

if __name__ == '__main__':
    main()
