"""Builds the area-photo layer (D-89): resizes the licence-checked public photos to web sizes and writes src/data/area-photos.json.

python3 -I tools/build_area_photos.py --src <folder with <area>/<photo>.jpg> --check <photo-licence-check csv> --log <SOURCING-LOG.csv> --titles <titles.json>
Only rows the licence check marked APPROVED are used. Alt text comes from tools/area_photo_alt.py; credits come from the sourcing log (licence and author were
re-confirmed against Commons on 2026-11-03). Images go to public/img/areas/<id>-640.webp and -1280.webp; originals never enter the repo.
Panoramas wider than 3.2:1 are centre-cropped to 3:1 (credit then says 'resized and cropped'); anything wider than 5.2:1 is skipped."""
import argparse, csv, json, os, re, sys, urllib.parse
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from area_photo_alt import ALT
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT_IMG = os.path.join(ROOT, 'public/img/areas'); OUT_JSON = os.path.join(ROOT, 'src/data/area-photos.json')
SKIP = {'north-surrey_01': 'equirectangular 360 image, distorted and shows a person', 'fraser-heights_03': 'strip panorama too thin to use', 'greendale_03': 'strip panorama too thin to use'}
# photo-log area slug -> page slug that carries the photos (neighbourhood page first; city-level areas use the city homes-for-sale page)
PAGE = {
 'abbotsford': 'abbotsford-homes-for-sale', 'belcarra': 'belcarra-port-moody', 'brentwood': 'brentwood-homes-for-sale', 'burnaby': 'burnaby-homes-for-sale',
 'capitol-hill': 'capitol-hill-bn', 'central-burnaby': 'central-burnaby-houses-for-sale', 'central-meadows': 'central-meadows-pitt-meadows', 'central-park': 'central-park-bs',
 'chilliwack': 'chilliwack-homes-for-sale', 'city-of-langley': 'city-of-langley-homes-for-sale', 'cloverdale': 'cloverdale-neighbourhood-guides', 'coquitlam': 'coquitlam-homes-for-sale',
 'downtown-new-westminster': 'downtown-new-westminster-condos-townhomes-for-sale', 'fraserview': 'fraserview-nw', 'glenwood': 'glenwood-port-coquitlam', 'grandview': 'grandview-heights-guide',
 'harbour-place': 'harbour-place-coquitlam', 'heritage-woods': 'heritage-woods-port-moody', 'highgate': 'highgate-burnaby', 'ladner': 'ladner-homes-for-sale',
 'lower-mary-hill': 'lower-mary-hill-port-coquitlam', 'maple-ridge': 'maple-ridge-homes-for-sale', 'metrotown': 'metrotown-homes-for-sale', 'mountain-meadows': 'mountain-meadows-port-moody',
 'north-surrey': 'north-surrey-homes-for-sale', 'oaklands': 'oaklands-burnaby', 'pitt-meadows': 'pitt-meadows-homes-for-sale', 'port-coquitlam': 'port-coquitlam-homes-for-sale',
 'river-valley': 'river-valley-guide', 'riverwood': 'riverwood-port-coquitlam', 'sapperton': 'sapperton-new-westminster', 'simon-fraser-university-area': 'simon-fraser-university-area-burnaby',
 'south-slope': 'south-slope-burnaby', 'south-surrey-white-rock': 'south-surrey-neighbourhoods', 'sullivan-heights': 'sullivan-heights-burnaby', 'sunnyside-park': 'sunnyside-park-surrey',
 'upper-deer-lake': 'upper-deer-lake-burnaby', 'west-vancouver': 'west-vancouver-homes-for-sale', 'westridge': 'westridge-burnaby', 'westwood-plateau': 'westwood-plateau-coquitlam',
 'woodland-acres': 'woodland-acres-port-coquitlam', 'surrey': 'surrey',
}
LIC = {'CC BY 2.0': 'https://creativecommons.org/licenses/by/2.0/', 'CC BY 2.5': 'https://creativecommons.org/licenses/by/2.5/', 'CC BY 3.0': 'https://creativecommons.org/licenses/by/3.0/',
       'CC BY 4.0': 'https://creativecommons.org/licenses/by/4.0/', 'CC BY-SA 2.0': 'https://creativecommons.org/licenses/by-sa/2.0/', 'CC BY-SA 2.5': 'https://creativecommons.org/licenses/by-sa/2.5/',
       'CC BY-SA 2.5 CA': 'https://creativecommons.org/licenses/by-sa/2.5/ca/', 'CC BY-SA 3.0': 'https://creativecommons.org/licenses/by-sa/3.0/', 'CC BY-SA 4.0': 'https://creativecommons.org/licenses/by-sa/4.0/',
       'CC0': 'https://creativecommons.org/publicdomain/zero/1.0/', 'Public domain': ''}


def author(a):
    a = re.sub(r'\s+from\s+.*$', '', a.strip()); return re.sub(r'^User:', '', a)


def page_title(slug):
    ov = json.load(open(os.path.join(ROOT, 'src/data/seo-overrides.json'), encoding='utf-8')).get(slug, {})
    t = ov.get('title')
    if not t:
        for d in ('pages', 'local'):
            f = os.path.join(ROOT, f'src/data/{d}/{slug}.json')
            if os.path.exists(f):
                j = json.load(open(f, encoding='utf-8')); t = j.get('title') or (j.get('new_page') or {}).get('title'); 
                if t: break
    return (t or slug).split(' | ')[0].strip()


def credits_page(pages):
    """src/data/local/photo-credits.json: every photo, its page, author, licence and source. Linked from the footer; kept out of the index and sitemap (isGated)."""
    items = []
    for slug in sorted(pages, key=lambda k: page_title(k).lower()):
        for ph in pages[slug]:
            lic = [{'t': ph['license'], 'h': ph['licenseUrl']}] if ph['licenseUrl'] else [{'t': 'public domain'}]
            items.append([{'t': page_title(slug), 'h': f'/{slug}.html'}, {'t': ': ' + ph['alt'] + '. Photo by '}, {'t': ph['author'], 'h': ph['source']}, {'t': ', '}, *lic, {'t': '.'}])
    blocks = [
        {'t': 'p', 'text': 'Some area pages on this site use photographs that other photographers have shared under open licences on Wikimedia Commons. Each photo carries its credit directly underneath it, and every photo is listed here with the photographer, the licence and a link to the original file.', 'gen': 'photocredits'},
        {'t': 'p', 'text': 'We resize and compress every photo for the web, and where a wide panorama had to be trimmed to fit the page we say so in its caption. Photos shared under a Creative Commons Attribution licence may be reused with credit; photos shared under a ShareAlike licence carry the same condition for anyone who adapts the image itself. Jared’s own photographs replace these as they are taken.', 'gen': 'photocredits'},
        {'t': 'p', 'text': 'If you took one of these photos and would like the credit changed or the photo removed, email jaredgibbons@royallepage.ca with the page and we will fix it.', 'gen': 'photocredits'},
        {'t': 'h', 'level': 2, 'text': 'Photos and credits by page', 'gen': 'photocredits'},
        {'t': 'list', 'items': items, 'gen': 'photocredits'},
    ]
    d = {'status': 'draft', 'slug': 'photo-credits', 'updated': '2026-11-03', 'blocks': blocks, 'faq': [], 'hand_edited': True,
         'new_page': {'title': 'Photo Credits | Jared Gibbons', 'description': 'Photographers, licences and source links for the open-licence area photos used on jaredgibbons.ca.', 'h1': 'Photo credits'},
         'breadcrumbs': [{'name': 'Home', 'href': '/index.html'}, {'name': 'Photo credits', 'href': '/photo-credits.html'}]}
    json.dump(d, open(os.path.join(ROOT, 'src/data/local/photo-credits.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def main():
    ap = argparse.ArgumentParser()
    for k in ('src', 'check', 'log', 'titles'): ap.add_argument('--' + k, required=True)
    a = ap.parse_args()
    check = {r['file']: r for r in csv.DictReader(open(a.check, encoding='utf-8'))}
    log = {r['filename'][:-4]: r for r in csv.DictReader(open(a.log, encoding='utf-8-sig'))}
    titles = json.load(open(a.titles, encoding='utf-8'))
    os.makedirs(OUT_IMG, exist_ok=True)
    pages = {}; problems = []; skipped = []
    for f, c in sorted(check.items()):
        if c['decision'] != 'APPROVED': continue
        if f in SKIP: skipped.append((f, SKIP[f])); continue
        area = c['area']; page = PAGE.get(area, area)
        if f not in ALT: problems.append(f'{f}: no alt text'); continue
        if not os.path.exists(f'src/data/pages/{page}.json') and not os.path.exists(f'src/data/local/{page}.json'): problems.append(f'{f}: page {page} does not exist'); continue
        src = f'{a.src}/{area}/{f}.jpg'; im = Image.open(src).convert('RGB'); w, h = im.size; ratio = w / h
        if ratio > 5.2: skipped.append((f, 'too wide')); continue
        cropped = False
        if ratio > 3.2:
            nw = int(h * 3); x0 = (w - nw) // 2; im = im.crop((x0, 0, x0 + nw, h)); w, h = im.size; cropped = True
        for tw in (640, 1280):
            th = round(h * tw / w); r = im.resize((tw, th), Image.LANCZOS); r.save(f'{OUT_IMG}/{f}-{tw}.webp', 'WEBP', quality=76, method=6)
        row = log[f]; t = re.sub(r'\?.*$', '', titles[f'{area}/{f}.jpg'])
        commons = 'https://commons.wikimedia.org/wiki/' + urllib.parse.quote(t.replace(' ', '_'), safe=':/()')
        lic = row['license'].strip()
        if lic not in LIC: problems.append(f'{f}: unknown licence {lic}'); continue
        pages.setdefault(page, []).append({'id': f, 'alt': ALT[f], 'w': 1280, 'h': round(h * 1280 / w), 'author': author(row['author']), 'license': lic, 'licenseUrl': LIC[lic], 'source': commons, 'cropped': cropped, 'wide': (w / h) > 2.2})
    for p in pages.values(): p.sort(key=lambda x: (x['wide'], x['id']))  # first entry = the page's main photo (never a panorama when an ordinary photo exists)
    json.dump(pages, open(OUT_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    credits_page(pages)
    print('pages', len(pages), 'photos', sum(len(v) for v in pages.values()))
    for s in skipped: print('skipped', *s)
    for p in problems: print('PROBLEM', p)


if __name__ == '__main__':
    main()
