#!/usr/bin/env python3
""""The area now" for sold and leased listing pages (D-322). A sold listing page says what the home was; this adds what its
neighbourhood is like for a buyer today, from figures already in the repo: the Paragon 12-month closed-sales aggregate for the
listing's MLS® sub-area and home type (src/data/sold/sold-12m.json, 5-sale minimum), and links to the neighbourhood's live pages.

    python3 -I tools/build_listing_area.py   -> src/data/listing-area.json

The listing's sub-area comes from src/data/sold-paragon.json (Jared's Paragon sales, D-295 / D-309). No price of the home itself.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import build_sold_layer as S  # noqa: E402

norm = lambda s: re.sub(r'[^a-z0-9]', '', str(s).lower())
GROUP = {'House': 'house', 'Condo': 'condo', 'Townhouse': 'townhome', 'Townhome': 'townhome', 'Duplex': 'duplex', '1/2 Duplex': 'duplex',
         'Acreage': 'acreage', 'Manufactured': 'mobile', 'Land': 'land', 'Lot': 'land'}
NOUN = {'house': 'houses', 'condo': 'condos', 'townhome': 'townhomes', 'duplex': 'duplexes', 'acreage': 'houses with acreage', 'mobile': 'manufactured homes', 'land': 'lots'}


def label(name):
    n = S.clean_label(name)
    n = re.sub(r'\s+(MR|VE|VW)$', '', n)
    return n if n in ('Langley City', 'Fort Langley', 'North Surrey') else re.sub(r'\s+(Langley|Surrey)$', '', n)


def main():
    agg = S.load()
    subs = {norm(k.split('|', 1)[1]): k for k in agg['sub']}
    pages = {p.stem for p in (ROOT / 'src/data/local').glob('*.json')} | {p.stem for p in (ROOT / 'src/data/pages').glob('*.json')}
    sp = json.loads((ROOT / 'src/data/sold-paragon.json').read_text())['bySub']
    out = {}
    for sub, items in sp.items():
        k = subs.get(sub)
        if not k: continue
        area, name = k.split('|', 1)
        disp = label(name)
        base = norm(re.sub(r'\s+(Langley|Surrey|BC|MR)$', '', name))
        page = next((p for p in sorted(pages, key=len) if norm(p) in (base, norm(name), base + 'guide')), None)
        for it in items:
            if not it.get('slug'): continue
            g = GROUP.get(it.get('type'), 'house')
            s = agg['sub'][k]['groups'].get(g, {})
            rec = {'sub': disp, 'noun': NOUN[g], 'page': page}
            if s.get('n', 0) >= S.MIN_MED and 'price' in s:
                rec.update(n=s['n'], price=s['price'], dom=s['dom'], ratio=s.get('ratio'))
            out[it['slug']] = rec
    # Older listings not in the Paragon file: the archive's "Area Statistics" note names the sub-area ("... located in Aberdeen.").
    DT = {'Apartment/Condo': 'condo', 'Townhouse': 'townhome', '1/2 Duplex': 'duplex', 'Duplex': 'duplex', 'Manufactured': 'mobile', 'Manufactured with Land': 'mobile'}
    for f in sorted((ROOT / 'src/data/listings').glob('*.json')):
        d = json.loads(f.read_text())
        if d.get('status') == 'Active' or d['slug'] in out: continue
        name = next((m.group(1).strip() for b in d['blocks'] if b.get('t') == 'p' and b.get('parts')
                     for m in [re.search(r'located in (.+?) \. Average', ' '.join(x.get('t', '') for x in b['parts']))] if m), None)
        k = name and next((v for kk, v in subs.items() if kk in (norm(name), norm(name) + 'langley', norm(name) + 'surrey')), None)
        if not k: continue
        dt = next((it['v'][0] for b in d['blocks'] if b.get('t') == 'facts' for it in b['items'] if it['k'] == 'Dwelling Type:' and it['v']), '')
        g = DT.get(dt, 'house')
        s = agg['sub'][k]['groups'].get(g, {}); nm = k.split('|', 1)[1]
        base = norm(re.sub(r'\s+(Langley|Surrey|BC|MR)$', '', nm))
        rec = {'sub': label(nm), 'noun': NOUN[g], 'page': next((p for p in sorted(pages, key=len) if norm(p) in (base, norm(nm))), None)}
        if s.get('n', 0) >= S.MIN_MED and 'price' in s: rec.update(n=s['n'], price=s['price'], dom=s['dom'], ratio=s.get('ratio'))
        out[d['slug']] = rec
    # Still unplaced: Pete's Paragon lookup of the older pages (src/data/listing-subareas.json, D-358).
    extra = json.loads((ROOT / 'src/data/listing-subareas.json').read_text())['listings']
    for slug, name in extra.items():
        if slug in out: continue
        k = next((v for kk, v in subs.items() if kk in (norm(name), norm(name) + 'langley', norm(name) + 'surrey')), None)
        if not k: continue
        d = json.loads((ROOT / 'src/data/listings' / f'{slug}.json').read_text())
        dt = next((it['v'][0] for b in d['blocks'] if b.get('t') == 'facts' for it in b['items'] if it['k'] == 'Dwelling Type:' and it['v']), '')
        g = DT.get(dt, 'house')
        s = agg['sub'][k]['groups'].get(g, {}); nm = k.split('|', 1)[1]
        base = norm(re.sub(r'\s+(Langley|Surrey|BC|MR)$', '', nm))
        rec = {'sub': label(nm), 'noun': NOUN[g], 'page': next((p for p in sorted(pages, key=len) if norm(p) in (base, norm(nm), base + 'guide')), None)}
        if s.get('n', 0) >= S.MIN_MED and 'price' in s: rec.update(n=s['n'], price=s['price'], dom=s['dom'], ratio=s.get('ratio'))
        out[slug] = rec
    meta = {'_note': 'Neighbourhood figures for sold listing pages (D-322), from the Paragon 12-month aggregate. Built by tools/build_listing_area.py.', 'window': S.WINDOW}
    (ROOT / 'src/data/listing-area.json').write_text(json.dumps({**meta, 'listings': out}, ensure_ascii=False, indent=1) + '\n')
    print(len(out), 'listings;', sum(1 for v in out.values() if 'price' in v), 'with figures;', sum(1 for v in out.values() if v['page']), 'with a neighbourhood page')


if __name__ == '__main__':
    main()
