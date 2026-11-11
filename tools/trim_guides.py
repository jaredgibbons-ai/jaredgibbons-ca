"""Trim the longest neighbourhood guides (D-202, Jared approved 2026-11-10).

The bulk of the longest guides is the home-type sections (condos, townhomes, lots and land, acreage, mobile homes, duplexes). Each one
repeats the same four sub-sections: "Streets, schools and getting around", "Local rules that affect … buyers", "Good to know" and
"Sources" — so a guide with six home types says the city's rules six times, and Cultus Lake says them for three sub-areas each.

What this does, per guide:
- Keeps each type section's lead, its building / complex entries and its "What trades here / The ground / The parks" notes.
- Keeps the good-to-know notes, and the rules paragraphs that are about this neighbourhood (they name it, a street address, or one
  of its buildings), once each, in the type section they came from.
- Moves the paragraphs that are city-wide (they name none of the above) to one shared page per city (BC-wide rules such as
  Form B, ALR, transfer tax and GST are already on the BC rules pages the guides link to, so they are not repeated there),
  /<city>-home-buying-rules.html, grouped by home type, each paragraph once. The guide links there from every type section.
- "Streets, schools and getting around" lines stay with their type section; a line another type section already said is dropped.
- Merges every type section's sources into the guide's own sources list (each link once) and the city page gets them too.
- Merges a type that appears twice under two spellings of the area ("Aldergrove" / "Aldergrove Langley"), entries once each.
Nothing is reworded. Run once per guide: a trimmed guide carries "trimmed": "<date>" and is skipped next time.
python3 -I tools/trim_guides.py [slug …]     (no slugs: the 20 longest built guides; --all: every guide with a city)"""
import collections, glob, json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
LOCAL = os.path.join(ROOT, 'src/data/local')
TODAY = '2026-11-10'
TYPES = [('condo', 'Condo buildings', 'Condos'), ('townhome', 'Townhome complexes', 'Townhomes'), ('lots', 'Lots and land', 'Lots and land'),
         ('acreage', 'Acreage and rural land', 'Acreage and rural land'), ('mobile', 'Mobile and manufactured homes', 'Mobile and manufactured homes'),
         ('duplex', 'Duplexes and half duplexes', 'Duplexes and half duplexes')]
TYPE_RX = re.compile(r'^(' + '|'.join(re.escape(t[1]) for t in TYPES) + r') in (.+)$')
CITY = {  # guide base -> (city slug, city name, breadcrumb hub)
    **{b: ('pitt-meadows', 'Pitt Meadows', '/pitt-meadows-homes-for-sale.html') for b in ['central-meadows-pitt-meadows', 'mid-meadows-pitt-meadows', 'south-meadows-pitt-meadows', 'north-meadows-pitt-meadows', 'west-meadows-pitt-meadows']},
    **{b: ('maple-ridge', 'Maple Ridge', '/maple-ridge-homes-for-sale.html') for b in ['north-maple-ridge', 'southwest-maple-ridge', 'websters-corners', 'northeast-maple-ridge', 'east-central-maple-ridge', 'west-central-maple-ridge', 'northwest-maple-ridge', 'cottonwood-maple-ridge', 'albion', 'silver-valley', 'thornhill-maple-ridge', 'whonnock']},
    **{b: ('langley', 'the Township of Langley', '/langley-homes-for-sale.html') for b in ['aldergrove', 'fort-langley', 'brookswood', 'murrayville', 'walnut-grove', 'willoughby', 'salmon-river', 'otter-district', 'county-line-glen-valley', 'campbell-valley']},
    **{b: ('delta', 'Delta', '/delta-homes-for-sale.html') for b in ['tsawwassen-east', 'tsawwassen-north', 'tsawwassen-central', 'beach-grove', 'cliff-drive', 'boundary-beach', 'english-bluff', 'hawthorne', 'neilsen-grove', 'delta-manor', 'ladner-elementary', 'holly', 'port-guichon', 'ladner-rural', 'east-delta', 'westham-island', 'annieville', 'nordel', 'scottsdale', 'sunshine-hills-woods']},
    **{b: ('abbotsford', 'Abbotsford', '/abbotsford-homes-for-sale.html') for b in ['poplar', 'central-abbotsford', 'abbotsford-east', 'abbotsford-west', 'aberdeen', 'bradner', 'matsqui', 'sumas-mountain', 'sumas-prairie']},
    **{b: ('chilliwack', 'Chilliwack', '/chilliwack-homes-for-sale.html') for b in ['chilliwack-proper-east', 'chilliwack-proper-west', 'chilliwack-proper-south', 'chilliwack-downtown', 'sardis-east-vedder', 'sardis-west-vedder', 'sardis-south', 'vedder-crossing', 'promontory', 'garrison-crossing', 'fairfield-island', 'chilliwack-mountain', 'little-mountain', 'eastern-hillsides', 'greendale', 'yarrow', 'ryder-lake', 'rosedale', 'east-chilliwack', 'west-chilliwack', 'lower-landing', 'majuba-hill', 'vedder-mountain']},
    'cultus-lake': ('cultus-lake', 'Cultus Lake', '/cultus-lake.html'),
    **{b: ('surrey', 'Surrey', '/surrey-homes-for-sale.html') for b in ['bear-creek-green-timbers', 'bolivar-heights', 'bridgeview', 'cedar-hills', 'east-newton', 'fleetwood-tynehead', 'fraser-heights',
       'guildford', 'panorama-ridge', 'queen-mary-park-surrey', 'royal-heights', 'sullivan-station', 'west-newton', 'whalley', 'clayton', 'cloverdale-bc', 'serpentine',
       'crescent-beach-ocean-park', 'elgin-chantrell', 'grandview-heights', 'hazelmere', 'king-george-corridor', 'morgan-creek', 'pacific-douglas', 'sunnyside-park-surrey', 'barnston-island-surrey']},
    **{b: ('mission', 'Mission', '/mission-bc-mission-guide.html') for b in ['dewdney-deroche-mission', 'durieu-mission', 'hatzic-mission', 'hemlock-valley-mission', 'lake-errock-mission',
       'mission-bc-mission', 'mission-west-mission', 'stave-falls-mission', 'steelhead-mission']},
}
TOPICS = [  # city page sections, first match wins
    ('taxes', 'Property taxes, transfer tax and GST in {city}', re.compile(r'\btax|\bPTT\b|\bGST\b|levy|exemption|rebate|FHSA|Home Buyers|penalt', re.I)),
    ('flood', 'Floodplain, farmland and environmental rules in {city}', re.compile(r'flood|\bdike|diking|\bALR\b|Agricultural Land|riparian|streamside|watercourse|slope|geotech|hazard', re.I)),
    ('strata', 'Strata, co-op and age rules in {city}', re.compile(r'strata|Form B|depreciation|co-op|co-operative|age-restrict|55\+|rental restriction|\bpets?\b|leasehold|land use contract', re.I)),
    ('zoning', 'Zoning, suites and small-scale housing in {city}', re.compile(r'zon|SSMUH|small-scale|subdivi|\bOCP\b|Official Community Plan|suite|coach house|lot area|density|area plan|rezon|development permit', re.I)),
    ('servicing', 'Water, sewer and servicing in {city}', re.compile(r'sewer|septic|\bwater\b|\bwells?\b|servic|drainage|hydro|internet', re.I)),
    ('other', 'Other things to know about buying in {city}', re.compile(r'.', re.S)),
]
HERE = re.compile(r'\bthis (?:sub-area|area|pocket|neighbourhood|community)\b|\bnot theirs\b|\bthe sub-area\b|\bthe (?:area|village|core)\b|\b(?:west|east|north|south)[- ](?:edge|side)\b|\bedge lots\b', re.I)
PROVINCIAL = re.compile(r'Strata Property Act|\bSPA s\.|Form B|depreciation report|\bALC\b|Agricultural Land Commission|ALR residences|[Pp]roperty transfer tax|\bPTT\b|\bGST\b|FHSA|Home Buyers|CMHC|REDMA|rescission|Manufactured Home Park Tenancy|MHPTA|GWELLS|gwells|Sewerage System Regulation|[Ss]peculation|vacancy tax|Bill 44|rental-restriction')
NUM = re.compile(r'\$?\d[\d,]*(?:\.\d+)?%?|\b(?:19|20)\d\d\b')
RESEARCHY = re.compile(r'contested citation|flagged|pointer complexes|no known case|as the (?:jurisdiction|FVRD frame) states|carries none of this|SnapStats|covered forms|is an error|two live versions|likely lineage|sources differ|Apply only after|redirect case|Anchors:|worked example|INCLUDING|never flat|\(inputs|Counted|stated for|per a building-data source|this page|this guide|below\b|above\b', re.I)
KEEP_WHOLE = {'abbotsford-west-guide'}   # its rules text is most of what makes it unique (would fall to 0.697): left whole
SUBCAT = [('streets', r'^Streets, schools'), ('rules', r'^Local rules'), ('gtk', r'^Good to know'), ('sources', r'^Sources for')]
ADDR = re.compile(r'\b\d{3,6}[A-Z]? (?:[A-Z][a-z]+ ){0,3}(?:Street|St|Road|Rd|Avenue|Ave|Drive|Dr|Highway|Hwy|Way|Crescent|Cres|Place|Pl|Boulevard|Blvd|Lane|Trail|Close|Court|Ct|Mall)\b')


def text(b): return ' '.join(re.findall(r'"(?:t|text)": "((?:[^"\\]|\\.)*)"', json.dumps(b, ensure_ascii=False)))


def shingles(s):
    w = re.findall(r"[a-z0-9$%'’]+", s.lower()); return {' '.join(w[i:i + 7]) for i in range(max(0, len(w) - 6))}


def near_dup(s, kept, th=0.6):
    S = shingles(s)
    return bool(S) and any(len(S & k) / len(S) >= th for k in kept)


def subsec_cat(h):
    for k, rx in SUBCAT:
        if re.match(rx, h): return k
    return None


def split_items(b):
    """A list block is several facts; a paragraph is one. Returns [(item_block, text)]."""
    if b.get('t') == 'list' and isinstance(b.get('items'), list):
        return [({**b, 'items': [it]}, text(it)) for it in b['items']]
    return [(b, text(b))]


def trim(slug, city_store):
    path = os.path.join(LOCAL, slug + '.json')
    d = json.load(open(path, encoding='utf-8'))
    if d.get('trimmed'): return None
    base = slug[:-6]
    if base not in CITY: print('  skip (no city):', slug); return None
    cslug, cname, hub = CITY[base]
    blocks = d['blocks']
    # sections
    secs, cur = [], None
    for b in blocks:
        if b.get('t') == 'h' and b.get('level') == 2:
            cur = {'h': b, 'blocks': []}; secs.append(cur)
        elif cur is None: secs.append({'h': None, 'blocks': [b]}); cur = secs[-1]
        else: cur['blocks'].append(b)
    names = set()
    for s in secs:
        m = s['h'] and TYPE_RX.match(s['h']['text'])
        if m: names.add(re.sub(r'\s+(Guide|PI|MR|Pitt Meadows Guide)$', '', m.group(2)).strip())
    names |= {re.sub(r'\s+(Pitt Meadows|Maple Ridge|Langley|Abbotsford|Chilliwack|Mission)$', '', n) for n in list(names)}
    names = {n for n in names if len(n) > 3}
    entries = set()
    for s in secs:
        for b in s['blocks']:
            if b.get('t') == 'h' and b.get('level') == 3 and not subsec_cat(b['text']):
                nm = re.split(r'\s+[—–-]\s+|\.\s|,', b['text'])[0].strip()
                if len(nm) > 3: entries.add(nm)
    local_rx = re.compile('|'.join(re.escape(n) for n in sorted(names | entries, key=len, reverse=True)) or r'^\b$')
    is_local = lambda t: bool(local_rx.search(t) or ADDR.search(t) or HERE.search(t))

    out, kept_local, streets_best, sources, moved = [], [], None, [], collections.Counter()
    type_seen = {}
    first_type_at = None
    for s in secs:
        m = s['h'] and TYPE_RX.match(s['h']['text'])
        if not m:
            out.append(s); continue
        tkey = next(t[0] for t in TYPES if t[1] == m.group(1))
        # subsections
        lead, subs, cs = [], [], None
        for b in s['blocks']:
            if b.get('t') == 'h' and b.get('level') == 3: cs = {'h': b, 'cat': subsec_cat(b['text']), 'blocks': []}; subs.append(cs)
            elif cs is None: lead.append(b)
            else: cs['blocks'].append(b)
        keep_subs, local_paras = [], []
        for sub in subs:
            c = sub['cat']
            if c is None:                                     # an entry (building, complex, park) or "What trades here"
                keep_subs.append(sub); continue
            if c == 'sources':
                for b in sub['blocks']:
                    for it, _ in split_items(b): sources.append(it)
                continue
            if c == 'streets':                               # where the stock sits, streets, schools: kept unless another type section already said it
                for bb in sub['blocks']:
                    for it, t in split_items(bb):
                        if not t.strip(): continue
                        if near_dup(t, kept_local): moved['streets repeat dropped'] += len(t.split()); continue
                        local_paras.append(('streets', it)); kept_local.append(shingles(t))
                continue
            for b in sub['blocks']:                           # rules / good to know: split local from city-wide
                for it, t in split_items(b):
                    if not t.strip(): continue
                    pointer = 'linked below' in t or any(isinstance(x, dict) and str(x.get('h', '')).startswith(('/', 'https://jaredgibbons.ca')) for x in (it.get('items') or [[]])[0] + it.get('parts', []))
                    if pointer or c == 'gtk' or is_local(t):   # pointers and good-to-know notes stay with the guide; only city-wide rules move
                        if not near_dup(t, kept_local): local_paras.append((c, it)); kept_local.append(shingles(t))
                        else: moved['local dup dropped'] += len(t.split())
                    else:
                        city_store[cslug]['types'][tkey].append((c, it, t, slug)); moved['to city page'] += len(t.split())
        # merge a type that appears twice (two spellings of the area)
        if tkey in type_seen:
            prev = type_seen[tkey]
            have = {re.split(r'\s+[—–-]\s+', x['h']['text'])[0].lower() for x in prev['subs']}
            prev['subs'] += [x for x in keep_subs if re.split(r'\s+[—–-]\s+', x['h']['text'])[0].lower() not in have]
            prev['local'] += local_paras; moved['duplicate type section merged'] += 1
            ls = [shingles(text(x)) for x in prev['lead']]       # the second spelling's lead keeps any line the first did not have
            for b in lead:
                t = text(b)
                if t.strip() and not near_dup(t, ls): prev['lead'].append(b); ls.append(shingles(t))
            a1, a2 = TYPE_RX.match(prev['h']['text']).group(2), m.group(2)   # one heading for both: the part of the names they share
            common = a1 if a2.startswith(a1) else re.sub(r'\s+\S*$', '', os.path.commonprefix([a1 + ' ', a2 + ' '])).strip()
            if len(common) > 3 and common != a1: prev['h']['text'] = f'{m.group(1)} in {common}'
            continue
        h = dict(s['h']); h['text'] = re.sub(r'\s+(Guide|Pitt Meadows Guide)$', '', h['text'])
        rec = {'h': h, 'lead': lead, 'subs': keep_subs, 'local': local_paras, 'type': tkey, 'gen': s['h'].get('gen'), 'pos': s['h'].get('pos')}
        type_seen[tkey] = rec
        out.append(rec)
        if first_type_at is None: first_type_at = len(out) - 1
    if not type_seen: return None
    # rebuild blocks
    new = []
    link = lambda label: {'t': 'p', 'parts': [{'t': f'The {cname.replace("the ", "")}-wide rules for {label.lower()} (zoning, strata, servicing, taxes) are on one page: '},
                                              {'t': f'buying a home in {cname.replace("the ", "")}: the rules', 'h': f'/{cslug}-home-buying-rules.html'}, {'t': '.'}], 'gen': 'trim', 'pos': 'end'}
    for i, s in enumerate(out):
        if 'type' in s:
            g = {'gen': s['gen'] or 'tn', 'pos': s['pos'] or 'end'}
            new.append(s['h']); new += s['lead']
            for sub in s['subs']: new.append(sub['h']); new += sub['blocks']
            if s['local']:
                loc = sorted(s['local'], key=lambda x: 0 if x[0] == 'streets' else 1)   # where it sits first, then the local rules
                new.append({'t': 'h', 'level': 3, 'text': 'Where it sits and what to know here', **g})
                new += [it for _, it in loc]
            label = next(t[2] for t in TYPES if t[0] == s['type'])
            new.append(link(label))
        else:
            if s['h']: new.append(s['h'])
            new += s['blocks']
    # sources: add to the guide's own last "Sources…" list, else a new end list
    seen = set(); src_items = []
    for it in sources:
        for item in it.get('items', [[]]):
            hrefs = [p.get('h') for p in item if isinstance(p, dict) and p.get('h')]
            k = hrefs[0] if hrefs else json.dumps(item, ensure_ascii=False)
            if k in seen: continue
            seen.add(k); src_items.append(item)
    city_store[cslug]['sources'] += src_items
    if src_items:
        new.append({'t': 'h', 'level': 2, 'text': 'Sources for the home-type notes', 'gen': 'trim', 'pos': 'end'})
        new.append({'t': 'list', 'items': src_items, 'gen': 'trim', 'pos': 'end'})
    city_store[cslug]['name'] = cname; city_store[cslug]['hub'] = hub; city_store[cslug]['guides'].append(slug)
    before = sum(len(text(b).split()) for b in blocks); after = sum(len(text(b).split()) for b in new)
    d['blocks'] = new; d['trimmed'] = TODAY
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return before, after, dict(moved)


def write_city(cslug, c):
    path = os.path.join(LOCAL, f'{cslug}-home-buying-rules.json')
    old = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else None
    if old and old.get('curated'):                            # rewritten by hand (D-214): later trims link here but never rewrite it
        return
    name = c['name']; short = name.replace('the ', '')
    kept = collections.defaultdict(list); shs = []
    if old:                                                   # keep what earlier runs moved here
        for b in old['blocks']:
            if b.get('gen') == 'cityrules-item': kept[b['topic']].append(b); shs.append(shingles(text(b)))
    # the same fact is written many ways across guides: two lines that share their figures (rates, bylaw numbers, dates) are one fact,
    # and the line that carries more of them is kept
    cand = []
    for tkey, items in c['types'].items():
        for cat, it, t, slug in items:
            if RESEARCHY.search(t): continue
            if PROVINCIAL.search(t) and not re.search(re.escape(c['name'].replace('the ', '')), t): continue   # BC-wide: on the BC rules pages already
            cand.append((len(NUM.findall(t)), len(t), it, t))
    cand.sort(key=lambda x: (-x[0], -x[1]))
    sigs = []
    for nn, ln, it, t in cand:
        sig = set(NUM.findall(t))
        if sig and any(len(sig & s) >= 2 and len(sig & s) >= 0.5 * min(len(sig), len(s)) for s in sigs): continue
        if near_dup(t, shs, 0.35): continue
        sigs.append(sig)
        shs.append(shingles(t)); topic = next(k for k, _, rx in TOPICS if rx.search(t))
        blk = {k: v for k, v in it.items() if k not in ('pos', 'type', 'from', 'gen')}
        kept[topic].append({**blk, 'gen': 'cityrules-item', 'topic': topic})
    guides = sorted(set(c['guides']) | set((old or {}).get('guides', [])))
    blocks = [{'t': 'notice', 'text': "Draft for Jared's approval. Collected word for word from the city-wide rules paragraphs of the neighbourhood guides "
               "listed at the bottom (D-202); nothing new was added. Each guide keeps what is specific to it and links here.", 'gen': 'cityrules'},
              {'t': 'p', 'text': f'The rules below apply across {name}, not just one neighbourhood: zoning and small-scale housing, strata rules, '
               f'servicing, land rules and taxes, grouped by topic. Each neighbourhood guide keeps what is specific to that area and links back here. '
               f'Rules change, so confirm anything that matters for a purchase with the City and your lawyer before you remove subjects.', 'gen': 'cityrules'}]
    for topic, h2, _ in TOPICS:
        if not kept[topic]: continue
        blocks.append({'t': 'h', 'level': 2, 'text': h2.format(city=short), 'id': topic, 'gen': 'cityrules'})
        blocks += kept[topic]
    if c['sources'] or old:
        oldsrc = [b for b in (old or {}).get('blocks', []) if b.get('gen') == 'cityrules-src']
        items, seen = [], set()
        for b in oldsrc:
            for item in b['items']: items.append(item)
        for item in c['sources']:
            hrefs = [p.get('h') for p in item if isinstance(p, dict) and p.get('h')]
            k = hrefs[0] if hrefs else json.dumps(item, ensure_ascii=False)
            if k in seen or any(json.dumps(item) == json.dumps(x) for x in items): continue
            seen.add(k); items.append(item)
        blocks.append({'t': 'h', 'level': 2, 'text': 'Sources', 'gen': 'cityrules'})
        blocks.append({'t': 'list', 'items': items, 'gen': 'cityrules-src'})
    glinks = []
    for g in guides:
        gp = os.path.join(ROOT, 'src/data/pages', g + '.json')
        title = json.load(open(gp, encoding='utf-8')).get('title', g).split('|')[0].strip() if os.path.exists(gp) else g
        glinks.append([{'t': title, 'h': f'/{g}.html'}])
    blocks.append({'t': 'h', 'level': 2, 'text': f'Neighbourhood guides that use this page', 'gen': 'cityrules'})
    blocks.append({'t': 'list', 'items': glinks, 'gen': 'cityrules'})
    page = {'status': 'draft', 'slug': f'{cslug}-home-buying-rules', 'updated': TODAY, 'guides': guides,
            'new_page': {'h1': f'Buying a Home in {name}: Zoning, Strata, Land and Tax Rules',
                         'title': f'{short} Home Buying Rules: Zoning, Strata & Taxes | Jared Gibbons'[:65].rstrip(),
                         'description': f'The rules that apply across {name} when you buy a condo, townhome, lot, acreage or mobile home: zoning, strata, servicing and taxes, with official sources.'[:158]},
            'breadcrumbs': [{'href': '/index.html', 'name': 'Home'}, {'href': c['hub'], 'name': short}, {'href': f'/{cslug}-home-buying-rules.html', 'name': 'Home buying rules'}],
            'blocks': blocks, 'faq': []}
    json.dump(page, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return sum(len(text(b).split()) for b in blocks)


def main():
    slugs = [a for a in sys.argv[1:] if a != '--all']
    if '--all' in sys.argv:
        slugs = sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(LOCAL, '*-guide.json')) if os.path.basename(f)[:-11] in CITY and os.path.basename(f)[:-5] not in KEEP_WHOLE)
    elif not slugs:
        built = [(os.path.getsize(f), os.path.basename(f)[:-5]) for f in glob.glob(os.path.join(ROOT, 'dist/*-guide.html'))]
        slugs = [s for _, s in sorted(built, reverse=True) if os.path.exists(os.path.join(LOCAL, s + '.json'))][:20]
    store = collections.defaultdict(lambda: {'types': collections.defaultdict(list), 'sources': [], 'guides': [], 'name': '', 'hub': ''})
    for s in slugs:
        r = trim(s, store)
        if r: print(f'{s:42} {r[0]:6} -> {r[1]:6} words  {r[2]}')
    for c, v in store.items():
        if v['guides']: print('city page', c, write_city(c, v), 'words')


if __name__ == '__main__': main()
