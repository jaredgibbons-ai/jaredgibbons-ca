"""Buildings the MLS flags as 55+ (Restricted Age field on closed sales), added to the 55+ pages as a short table of names.

    python3 -I tools/build_mls55.py /path/Paragon_Closed_Sales_Remarks_*.csv     (rebuild the flagged list from a new export, then apply)
    python3 -I tools/build_mls55.py                                              (apply the saved list; run after build_55plus_notes)

Rules: a building is listed when its closed sales in the export carry the 55+ flag on at least half of its sales (the flag is typed by the listing agent,
so a building flagged on a minority of sales is treated as noise). Only building names, type and title are published: no counts, MLS numbers, addresses,
prices or listing remarks. Names already described on a 55+ page are not repeated. Names that clash with a building the notes checked and found NOT 55+ are held out (HOLD).
The export itself (listing remarks, MLS numbers) is not stored in the repo; only this aggregate is."""
import glob, json, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
LOCAL = os.path.join(ROOT, 'src/data/local'); PAGES = os.path.join(ROOT, 'src/data/pages')
STORE = os.path.join(ROOT, 'docs/research/mls-55plus/flagged-buildings.json')
GM = 'n55mls'
HUB = 'bc-55-plus-strata-rules'
HOLD = {'highgrove ii': 'the notes checked Highgrove (15055 20 Ave, Sunnyside Park) and found no age restriction; confirm whether Highgrove II is a separate strata before listing'}
SUBALIAS = {'cloverdale bc': 'cloverdale-bc', 'cottonwood mr': 'cottonwood-mr', 'sunnyside park surrey': 'sunnyside-park-surrey', 'queen mary park surrey': 'queen-mary-park-surrey',
            'aldergrove langley': 'aldergrove', 'central meadows': 'central-meadows-pitt-meadows', 'cliff drive': 'tsawwassen-central', 'crescent bch ocean pk.': 'crescent-bch-ocean-pk'}
CITYPAGE = {'Abbotsford': ('abbotsford-55-plus-condos-for-sale', 'abbotsford-55-plus-townhomes-for-sale'), 'Langley': ('langley-55-plus-condos-for-sale', 'langley-55-plus-townhomes-for-sale'),
            'Maple Ridge': ('maple-ridge-55-plus-condos-for-sale', 'maple-ridge-55-plus-townhomes-for-sale'), 'Pitt Meadows': ('pitt-meadows-55-plus-condos-for-sale', 'pitt-meadows-55-plus-townhomes-for-sale'),
            'South Surrey White Rock': ('south-surrey-white-rock-55-plus-condos-for-sale', 'south-surrey-white-rock-55-plus-townhomes-for-sale'),
            'Surrey': ('surrey-55-plus-homes-for-sale',) * 2, 'North Surrey': ('surrey-55-plus-homes-for-sale',) * 2, 'Cloverdale': ('surrey-55-plus-homes-for-sale',) * 2,
            'Coquitlam': ('coquitlam-55-plus-homes-for-sale',) * 2, 'Mission': ('mission-bc-55-plus-homes-for-sale',) * 2}
TITLE = {'Freehold Strata': 'Strata', 'Bare Land Strata': 'Bare-land strata', 'Leasehold prepaid-Strata': 'Prepaid leasehold strata', 'Leasehold prepaid-NonStrata': 'Prepaid leasehold',
         'Shares in Co-operative': 'Co-operative shares', 'Leasehold not prepaid-NonStrata': 'Leasehold (not prepaid)', 'Leasehold not prepaid-Strata': 'Leasehold strata (not prepaid)', 'Other': None, 'First Nations Lease': 'First Nations lease', 'Freehold NonStrata': 'Freehold'}
DW = {'Manufactured with Land': 'Manufactured home with land', 'Apartment/Condo': 'Condo', 'Townhouse': 'Townhome', 'House/Single Family': 'Detached home in a strata', 'Duplex': 'Duplex', 'Manufactured': 'Manufactured home'}


def key(x): return re.sub(r'[^a-z0-9]+', '', str(x).lower())
def norm(x): return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]+', ' ', str(x).lower())).strip()
def slugify(x): return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', x.lower())).strip('-')
def nice(n): return n.title().replace("'S", "'s") if n.isupper() or n.islower() else n
def load(slug):
    f = f'{LOCAL}/{slug}.json'; return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else None
def save(slug, j):
    with open(f'{LOCAL}/{slug}.json', 'w', encoding='utf-8') as f: json.dump(j, f, indent=2, ensure_ascii=False); f.write('\n')


def from_export(csv_path):
    import pandas as pd
    d = pd.read_csv(csv_path, dtype=str, encoding_errors='replace')
    d['cx'] = d['Complex/Subdivision Name'].fillna('').map(key); d['flag'] = d['Restricted Age'] == '55+'
    out = []
    for (area, cx), g in d[d.cx != ''].groupby(['Area', 'cx']):
        fl = int(g.flag.sum())
        if fl == 0 or fl / len(g) < 0.5 or len(cx) < 4: continue
        f = g[g.flag]; sub = f['Sub-Area/Community'].value_counts().index[0]
        names = f['Complex/Subdivision Name'].value_counts().index
        name = next((n for n in names if not n.isupper()), names[0])
        if key(name) in (key(sub), key(area)): continue
        out.append({'area': area.replace('N. Delta', 'North Delta'), 'sub': sub, 'name': nice(name.strip()),
                    'dwelling': sorted({DW.get(x, x) for x in f['Type of Dwelling'].dropna()}), 'title': sorted({TITLE.get(x, x) for x in f['Title to Land'].dropna()} - {None})})
    os.makedirs(os.path.dirname(STORE), exist_ok=True)
    json.dump({'source': 'Paragon closed sales, Nov 1 2025 to Oct 31 2026; Restricted Age = 55+ on at least half of a building\'s sales', 'buildings': sorted(out, key=lambda r: (r['area'], r['sub'], r['name']))}, open(STORE, 'w'), indent=1, ensure_ascii=False)
    print('saved', len(out), 'buildings')


def page_for(b):
    sub = b['sub']; s = SUBALIAS.get(norm(sub), slugify(sub))
    if os.path.exists(f'{LOCAL}/{s}-55-plus-homes-for-sale.json'): return [f'{s}-55-plus-homes-for-sale'] * 2, False
    cp = CITYPAGE.get(b['area'])
    return (list(cp), True) if cp else (None, False)


def main():
    data = json.load(open(STORE))['buildings']
    n55 = ''
    for f in glob.glob(f'{LOCAL}/*55-plus*.json'):
        j = json.load(open(f, encoding='utf-8'))
        n55 += ' ' + json.dumps([b for b in j['blocks'] if b.get('gen') not in (GM, 'gappage')] + j.get('faq', []), ensure_ascii=False)
    n55k = key(n55)
    place = {}; held = []; unplaced = []; seen = set()
    for b in data:
        k = key(b['name']).rstrip('s')
        if norm(b['name']) in HOLD: held.append(b['name']); continue
        if key(b['name']) in n55k or k in n55k or (area_k := (b['area'], k)) in seen: continue
        seen.add(area_k)
        pages, city = page_for(b)
        if not pages: unplaced.append(f"{b['name']} ({b['sub']})"); continue
        condo = 'Condo' in b['dwelling'] and 'Townhome' not in b['dwelling']
        slug = pages[0] if condo else pages[1]
        place.setdefault(slug, {}).setdefault(b['sub'] if city else None, []).append(b)
    for f in glob.glob(f'{LOCAL}/*55-plus*.json'):  # idempotent: strip the previous run
        j = json.load(open(f, encoding='utf-8'))
        if any(x.get('gen') == GM for x in j['blocks']): j['blocks'] = [x for x in j['blocks'] if x.get('gen') != GM]; save(os.path.basename(f)[:-5], j)
    n = 0
    for slug, groups in place.items():
        j = load(slug)
        if j is None: continue
        first = next(iter(groups.values()))[0]
        if None in groups: cityname = re.sub(r' (MR|BC|CQ|NW|VW|Surrey|Langley)$', '', first['sub'])
        else: cityname = slug.split('-55-plus')[0].replace('-', ' ').title().replace('Bc', 'BC')
        bl = []
        multi = None in groups and len(groups) == 1
        for sub, items in sorted(groups.items(), key=lambda kv: str(kv[0])):
            rows = [[nice(i['name']), ' / '.join(i['dwelling']) or '—', ' / '.join(t for t in i['title'] if t) or '—'] for i in sorted(items, key=lambda i: i['name'].lower())]
            nm = sub or cityname
            if sub is None:
                bl += [{'t': 'h', 'level': 2, 'text': f'More {cityname} buildings the MLS marks as 55+', 'gen': GM}]
            else:
                if not bl: bl += [{'t': 'h', 'level': 2, 'text': f'More {cityname} buildings the MLS marks as 55+, by community', 'gen': GM}]
                bl += [{'t': 'h', 'level': 3, 'text': sub, 'gen': GM}]
            bl += [{'t': 'p', 'text': f'In {nm}, closed sales of these buildings carry the 55+ restricted-age field. Confirm each building\'s bylaw in its Form B before relying on it.', 'gen': GM},
                   {'t': 'table', 'caption': f'Buildings in {nm} the MLS marks as 55+', 'head': ['Building', 'Type', 'Title'], 'rows': rows, 'gen': GM}]
        bl += [{'t': 'list', 'items': [[{'t': 'How to read the MLS 55+ flag', 'h': f'/{HUB}.html#mls-flag'}]], 'gen': GM}]
        at = next((i for i, b in enumerate(j['blocks']) if b.get('t') == 'h' and b.get('text') == 'Sources' and b.get('gen') in ('n55', 'n55city')), None)
        if at is None: at = next((i for i, b in enumerate(j['blocks']) if b.get('pos') == 'end'), len(j['blocks']))
        j['blocks'][at:at] = bl; save(slug, j); n += sum(len(v) for v in groups.values())
        print('added', sum(len(v) for v in groups.values()), 'to', slug)
    # hub explainer
    h = load(HUB)
    if h:
        h['blocks'] = [b for b in h['blocks'] if b.get('gen') != GM]
        add = [{'t': 'h', 'level': 2, 'id': 'mls-flag', 'text': 'How to read the MLS 55+ flag', 'gen': GM},
               {'t': 'p', 'text': 'Many 55+ buildings are marked in the MLS with a restricted-age field of 55+. The listing agent types that field, so it can be wrong or left blank, and it says nothing about the exemptions a strata allows or the building\'s own bylaws. Treat a flagged building as a lead worth checking, not as proof: the proof is the building\'s bylaws and its Form B.', 'gen': GM},
               {'t': 'p', 'text': 'Where a building has no flag on any recent sale, that is also a clue, not an answer. The notes behind this site checked several look-alike buildings whose listings say there is no age restriction, and the MLS field on their sales agrees.', 'gen': GM}]
        at = next((i for i, b in enumerate(h['blocks']) if b.get('t') == 'h' and b.get('text') == 'Sources'), len(h['blocks']))
        h['blocks'][at:at] = add; save(HUB, h)
    print('placed', n, 'held', held, 'unplaced', unplaced)


if __name__ == '__main__':
    if len(sys.argv) > 1: from_export(sys.argv[1])
    main()
