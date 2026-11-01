"""Link each 'Sell my house in <city>' page from its city hub pages (homes for sale, neighbourhood guides, sub-area hubs).

A link block (gen 'sellerlink') is added to src/data/local/<hub>.json for every hub that exists in src/data/pages and every selling page
that exists in src/data/local. Blocks tagged gen 'sellerlink' are removed and rebuilt on every run.
    python3 -I tools/link_selling_pages.py
"""
import glob, json, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
UPDATED = '2026-11-01'
# selling page slug -> (link text, hub page slugs)
SELL = {
    'sell-my-house-in-maple-ridge': ('Sell my house in Maple Ridge: current prices, lot rules and a free home evaluation', ['maple-ridge-homes-for-sale', 'maple-ridge-neighbourhood-guides']),
    'sell-my-house-in-pitt-meadows': ('Sell my house in Pitt Meadows: current prices, lot rules and a free home evaluation', ['pitt-meadows-homes-for-sale', 'pitt-meadows-neighbourhood-guides']),
    'sell-my-house-in-mission': ('Sell my house in Mission: current prices, lot rules and a free home evaluation', ['mission-homes-for-sale', 'mission-neighbourhood-guides']),
    'sell-my-house-in-abbotsford': ('Sell my house in Abbotsford: current prices, lot rules and a free home evaluation', ['abbotsford-homes-for-sale', 'abbotsford-neighbourhood-guides', 'abbotsford-townhomes-for-sale']),
    'sell-my-house-in-delta': ('Sell my house in Delta: prices for Tsawwassen, Ladner and North Delta, lot rules and a free home evaluation', ['delta-homes-for-sale', 'delta-neighbourhood-guides', 'tsawwassen-homes-for-sale', 'ladner-homes-for-sale', 'north-delta-homes-for-sale', 'tsawwassen-townhomes-for-sale', 'ladner-townhomes-for-sale']),
    'sell-my-house-in-surrey': ('Sell my house in Surrey: current prices, the 2024 lot rules and a free home evaluation', ['surrey-homes-for-sale', 'surrey-neighbourhood-guides', 'surrey-townhomes-for-sale', 'cloverdale-neighbourhood-guides', 'cloverdale-townhomes-for-sale']),
    'sell-my-house-in-south-surrey-white-rock': ('Sell my house in South Surrey or White Rock: current prices, each City\'s 2024 rules and a free home evaluation', ['south-surrey-homes-for-sale', 'south-surrey-townhomes-for-sale', 'white-rock', 'south-surrey-school-catchments', 'south-surrey-white-rock-ocean-view-homes-for-sale', 'south-surrey-white-rock-waterfront-homes-for-sale']),
    'sell-my-house-in-langley': ('Sell my house in Langley: current prices, what the Township and the City did about the 2024 rules, and a free home evaluation', ['langley-homes-for-sale', 'langley-neighbourhood-guides', 'langley-townhomes-for-sale', 'city-of-langley-homes-for-sale', 'city-of-langley-townhomes-for-sale']),
}


def save(f, d):
    json.dump(d, open(f, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(f, 'a').write('\n')


def main():
    for f in glob.glob(os.path.join(ROOT, 'src/data/local/*.json')):
        d = json.load(open(f, encoding='utf-8'))
        if any(b.get('gen') == 'sellerlink' for b in d.get('blocks', [])):
            d['blocks'] = [b for b in d['blocks'] if b.get('gen') != 'sellerlink']
            if not d['blocks'] and d.get('status') == 'generated': os.remove(f); continue
            save(f, d)
    n = 0
    for slug, (text, hubs) in SELL.items():
        if not os.path.exists(os.path.join(ROOT, f'src/data/local/{slug}.json')): continue
        for h in hubs:
            if not os.path.exists(os.path.join(ROOT, f'src/data/pages/{h}.json')): continue
            f = os.path.join(ROOT, f'src/data/local/{h}.json')
            d = json.load(open(f, encoding='utf-8')) if os.path.exists(f) else {'status': 'generated', 'slug': h, 'updated': UPDATED, 'blocks': []}
            d['blocks'].append({'t': 'p', 'text': text, 'h': f'/{slug}.html', 'gen': 'sellerlink'}); save(f, d); n += 1
    print('added', n, 'selling-page links')


if __name__ == '__main__':
    main()
