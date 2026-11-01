"""Internal links for community pages and city hubs (gen: "communitylinks", placed at the end of the page).

 - every community page (archive page or generated page) gets a "More <city> real estate" list: city hub, market stats, home-type pages,
   selling page, schools list, its guide or area-page twin, and ten neighbouring communities (alphabetical ring, so every page is linked to
   from ten others);
 - every city hub gets a "<city> neighbourhoods" list linking all community pages in the city.
Minimum: a page ends up with at least 12 contextual links. Run after build_snapstats_layers.py and build_community_pages.py.

    python3 -I tools/link_communities.py
"""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_community_pages as C
import build_snapstats_layers as L

ROOT = L.ROOT


def main():
    mapping = json.load(open(os.path.join(ROOT, 'src/data/snapstats/_mapping.json')))['mapped']
    pages = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, 'src/data/pages/*.json'))}
    locals_ = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, 'src/data/local/*.json'))}
    exists = lambda s: s in pages or s in locals_
    prim, guide = {}, {}
    for sl, v in mapping.items():
        if '+' in str(v[1]): continue  # city / home-type pages
        (guide if sl.endswith('-guide') else prim)[(v[0], v[1])] = sl
    city_comms = {}
    for (ak, nm), sl in prim.items(): city_comms.setdefault(ak, []).append((nm, sl))
    for ak in city_comms: city_comms[ak].sort(key=lambda x: x[0])
    schools = {}
    for sl in pages:
        pass
    def block_list(ak, nm, slug):
        city = C.CITY[ak][0]; items = []
        def add(sl, text):
            if exists(sl): items.append([{'t': text, 'h': f'/{sl}.html'}])
        add(C.HUB[ak], f'{city} homes for sale'); add(f'{C.MARKET[ak]}-real-estate-market-stats', f'{city} real estate market stats')
        pre = 'south-surrey' if ak == 'south-surrey-white-rock' else C.CITY[ak][1]
        for role, label in C.TYPE_PAGES: add(f'{pre}-{role}-for-sale', f'{city} {label}')
        if ak in C.SELL: add(C.SELL[ak], f'Sell my house in {city}')
        add(f'schools-in-{C.CITY[ak][1]}-bc', f'Schools in {city}')
        twin = guide.get((ak, nm)) if slug == prim.get((ak, nm)) else prim.get((ak, nm))
        if twin and twin != slug: add(twin, f'{C.DISPLAY.get(nm, nm)} ' + ('neighbourhood guide' if twin.endswith('-guide') else 'homes and market figures'))
        ring = city_comms.get(ak, []); names = [n for n, _ in ring]
        if nm in names:
            i = names.index(nm); n = 0
            for k in range(1, len(ring)):
                o, osl = ring[(i + k) % len(ring)]
                if osl != slug and n < 10: items.append([{'t': f'{C.DISPLAY.get(o, o)} real estate', 'h': f'/{osl}.html'}]); n += 1
        return items
    wrote = 0
    for sl, v in mapping.items():
        if '+' in str(v[1]): continue
        lf = os.path.join(ROOT, 'src/data/local', sl + '.json')
        if not os.path.exists(lf): continue
        j = json.load(open(lf, encoding='utf-8'))
        if j.get('community'): continue  # generated pages carry their own list
        ak, nm = v; city = C.CITY[ak][0]
        j['blocks'] = [b for b in j['blocks'] if b.get('gen') != 'communitylinks']
        items = block_list(ak, nm, sl)
        if len(items) < 3: continue
        j['blocks'] += [{'t': 'h', 'level': 2, 'text': f'More {city} real estate', 'gen': 'communitylinks', 'pos': 'end'}, {'t': 'list', 'items': items, 'gen': 'communitylinks', 'pos': 'end'}]
        json.dump(j, open(lf, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(lf, 'a').write('\n'); wrote += 1
    # hubs
    hubs = 0
    for ak, hub in C.HUB.items():
        lf = os.path.join(ROOT, 'src/data/local', hub + '.json')
        if not os.path.exists(lf): continue
        j = json.load(open(lf, encoding='utf-8')); city = C.CITY[ak][0]
        j['blocks'] = [b for b in j['blocks'] if b.get('gen') != 'communitylinks']
        items = [[{'t': f'{C.DISPLAY.get(n, n)} real estate', 'h': f'/{s}.html'}] for n, s in city_comms.get(ak, [])]
        if not items: continue
        j['blocks'] += [{'t': 'h', 'level': 2, 'text': f'{city} neighbourhoods', 'gen': 'communitylinks', 'pos': 'end'}, {'t': 'list', 'items': items, 'gen': 'communitylinks', 'pos': 'end'}]
        json.dump(j, open(lf, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(lf, 'a').write('\n'); hubs += 1
    print('community pages linked:', wrote, '; hubs with neighbourhood lists:', hubs)


if __name__ == '__main__':
    main()
