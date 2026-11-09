"""Adds Jared's own listing photos (Drive folder 'Website Area Photos - Jared listings', 2026-11-09) to the area-photo layer (D-191).

python3 -I tools/build_own_area_photos.py --src "<unzipped folder>"

For each entry: EXIF-transpose, optional blur boxes (addresses / unit numbers on signs), resize to 640 and 1280 px WebP (q76, method 6) into public/img/areas/<id>-<w>.webp,
then merge {id, alt, w, h, own, cropped, wide} into src/data/area-photos.json ahead of any photo a page already has (Jared's own photo leads; public-licence photos stay in the gallery).
Each photo id sits on exactly one page (tests/data-rules.test.mjs). Safe to re-run: earlier entries with the same id are replaced, not duplicated.
Left out on purpose (see docs D-191): interiors, red lot-outline overlays (Brookswood), Murrayville R3066794 (sub-area unverified), near-duplicates, rear-lane unit shots with numbers.
Photo ids avoid street addresses; the four listings with no MLS number yet use area words (own-whiterock-02 etc.).
"""
import argparse, glob, json, os
from PIL import Image, ImageFilter, ImageOps

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT_IMG = os.path.join(ROOT, 'public/img/areas'); OUT_JSON = os.path.join(ROOT, 'src/data/area-photos.json')

# (page slug, photo id, folder prefix, file name, alt text, blur boxes [(x0,y0,x1,y1) on the 3000 px original])
P = []
def add(page, pid, folder, fn, alt, blur=()):
    P.append((page, pid, folder, fn, alt, tuple(blur)))

# Campbell Valley (acreage, horse and farm country)
add('campbell-valley', 'own-R2971965-05', 'Langley - Campbell Val', 'R2971965-5.jpg', 'Aerial view over Campbell Valley acreages with paddocks, outbuildings and tall forest between the properties')
add('campbell-valley', 'own-R2971965-06', 'Langley - Campbell Val', 'R2971965-6.jpg', 'Aerial view across Campbell Valley acreage properties and green fields toward the mountains')
add('campbell-valley-acreages-farms-for-sale', 'own-R2971965-01', 'Langley - Campbell Val', 'R2971965-1.jpg', 'Aerial view of a Campbell Valley acreage road with large lots, hobby farms and forest')
add('campbell-valley-acreages-farms-for-sale', 'own-C8067336-99', 'Langley - Campbell Val', 'C8067336-99.jpg', 'Covered cattle barn and fenced paddock on a Campbell Valley farm with open fields beyond')
add('campbell-valley-acreages-farms-for-sale', 'own-R2971965-02', 'Langley - Campbell Val', 'R2971965-2.jpg', 'Aerial view of Campbell Valley hobby farms, barns and fenced fields among tall trees')
add('campbell-valley-houses-for-sale', 'own-C8067336-04', 'Langley - Campbell Val', 'C8067336-4.jpg', 'Two-storey acreage home set back across a wide lawn in Campbell Valley')
add('campbell-valley-houses-for-sale', 'own-C8067336-05', 'Langley - Campbell Val', 'C8067336-5.jpg', 'Gravel driveway leading to a country home with fruit trees on a Campbell Valley acreage')
# Murrayville
add('murrayville', 'own-R3158487-01', 'Langley - Murrayville', 'R3158487-1.jpg', 'Aerial view of Murrayville townhome and condo complexes with the village shops and the valley behind')
add('murrayville', 'own-R3158487-02', 'Langley - Murrayville', 'R3158487-2.jpg', 'Aerial view over Murrayville townhome rows and a small shopping plaza at the edge of the village')
add('murrayville-townhomes-for-sale', 'own-R3158487-04', 'Langley - Murrayville', 'R3158487-4.jpg', 'Aerial view of a Murrayville townhome and low-rise condo complex with a landscaped courtyard')
add('murrayville-townhomes-for-sale', 'own-R3158487-06', 'Langley - Murrayville', 'R3158487-6.jpg', 'Aerial view across Murrayville townhome complexes toward the village and Langley beyond')
# Aldergrove
add('aldergrove', 'own-R3172529-04', 'Langley - Aldergrove', 'R3172529-4.jpg', 'Aerial view down the main street of Aldergrove with new mid-rise buildings and the town centre')
add('aldergrove', 'own-R3172529-02', 'Langley - Aldergrove', 'R3172529-2.jpg', 'Aerial view of new mid-rise apartment buildings in Aldergrove with snow-capped mountains behind')
add('aldergrove-condos-for-sale', 'own-R3172529-05', 'Langley - Aldergrove', 'R3172529-5.jpg', 'Aerial view of Aldergrove mid-rise condo buildings beside shops and parking')
add('aldergrove-condos-for-sale', 'own-R3172529-06', 'Langley - Aldergrove', 'R3172529-6.jpg', 'Aerial view of an Aldergrove condo building by the town centre with parks and neighbourhoods behind')
# Walnut Grove
add('walnut-grove', 'own-R3158924-50', 'Langley - Walnut Grove', 'R3158924-50.jpg', 'Aerial view of a Walnut Grove school, playing field and surrounding homes with mountains behind')
add('walnut-grove', 'own-R3158924-49', 'Langley - Walnut Grove', 'R3158924-49.jpg', 'Aerial view of a Walnut Grove condo complex and pond beside Highway 1')
add('walnut-grove-condos-for-sale', 'own-R3158924-03', 'Langley - Walnut Grove', 'R3158924-3.jpg', 'Condo building framed by trees on a Walnut Grove street')
add('walnut-grove-condos-for-sale', 'own-R3158924-04', 'Langley - Walnut Grove', 'R3158924-4.jpg', 'Paved entrance court of a brick-and-timber Walnut Grove condo building')
add('walnut-grove-guide', 'own-R3158924-48', 'Langley - Walnut Grove', 'R3158924-48.jpg', 'Aerial view of a low-rise Walnut Grove residential complex with parking and trees and the Golden Ears mountains behind')
# Willoughby (sign address lines blurred)
add('willoughby-heights', 'own-R3154380-02', 'Langley - Willoughby', 'R3154380-2.jpg', 'Corner of a brick-and-siding townhome complex with a landscaped entrance sign in Willoughby Heights', [(1010, 1636, 1450, 1712)])
add('willoughby-townhomes-for-sale', 'own-R3154380-01', 'Langley - Willoughby', 'R3154380-1.jpg', 'Row of modern three-storey townhomes behind a low fence and young trees in Willoughby, Langley')
add('willoughby-townhomes-for-sale', 'own-R3154380-38', 'Langley - Willoughby', 'R3154380-38.jpg', 'Children’s climbing frame on a rubber-surfaced playground inside a Willoughby townhome complex')
add('willoughby-townhomes-for-sale', 'own-R3154380-39', 'Langley - Willoughby', 'R3154380-39.jpg', 'Paved entrance road into a Willoughby townhome complex with a landscaped sign and brick end units', [(1870, 1492, 2240, 1570)])
# Mission
add('mission-bc', 'own-R3064596-45', 'Mission', 'R3064596-45.jpg', 'Aerial view over Mission’s older streets and tree-lined blocks toward the Fraser River and the mountains')
add('mission-bc', 'own-R3064596-47', 'Mission', 'R3064596-47.jpg', 'Aerial view of Mission residential streets with a school roof and forested hills beyond')
add('mission-bc', 'own-R2841067-62', 'Mission', 'R2841067-62.jpg', 'Aerial view of the Mission shopping district along the highway with parking lots and the rail line')
add('mission-homes-for-sale', 'own-R3064596-46', 'Mission', 'R3064596-46.jpg', 'Aerial view of Mission neighbourhood streets with detached homes, the river and the mountains behind')
add('mission-condos-for-sale', 'own-R2841067-61', 'Mission', 'R2841067-61.jpg', 'Aerial view of a new low-rise condo building under construction beside the highway in Mission')
add('mission-mobile-homes', 'own-missionmh-50', 'Mission - Mobile Home', 'MLSTBD-38-9960Wilson-50.jpg', 'Aerial view of a mobile home park on the Fraser River bank in Mission with the mountains behind')
add('mission-mobile-homes', 'own-missionmh-51', 'Mission - Mobile Home', 'MLSTBD-38-9960Wilson-51.jpg', 'Aerial view of rows of mobile homes in a Mission riverside park beside tidal flats')
# Abbotsford East (three own photos already on the page)
add('abbotsford-east-houses-for-sale', 'own-R3169448-01', 'Abbotsford East', 'R3169448-1.jpg', 'Aerial view of Abbotsford East houses beside a main road with new townhomes going up and the mountains behind')
add('abbotsford-east-houses-for-sale', 'own-R3169448-03', 'Abbotsford East', 'R3169448-3.jpg', 'Aerial view of Abbotsford East streets and detached homes below a forested hill')
add('abbotsford-east-guide', 'own-R3169448-04', 'Abbotsford East', 'R3169448-4.jpg', 'Aerial view of a main road through Abbotsford East with houses on both sides and the valley behind')
add('abbotsford-east-guide', 'own-R3169448-06', 'Abbotsford East', 'R3169448-6.jpg', 'Wide aerial view over Abbotsford East rooftops, schools and tree-lined streets toward the valley')
# White Rock
add('white-rock', 'own-whiterock-02', 'White Rock', 'MLSTBD-101-15219Royal-2.jpg', 'Aerial view of a curved brick condo building and newer low-rise blocks in White Rock with high-rise towers behind')
add('white-rock', 'own-whiterock-04', 'White Rock', 'MLSTBD-101-15219Royal-4.jpg', 'Aerial view of a White Rock condo corner and street with a parking lot beside it')
add('white-rock-condos-for-sale', 'own-whiterock-03', 'White Rock', 'MLSTBD-101-15219Royal-3.jpg', 'Aerial view of a White Rock low-rise condo complex with balconies and landscaped frontage')
# South Surrey: Morgan Creek / Rosemary Heights, Grandview / Sunnyside, Ocean Park / Crescent Heights
add('morgan-creek-guide', 'own-R3168794-01', 'South Surrey - Morgan', 'R3168794-1.jpg', 'Aerial view of Morgan Creek townhome rows beside a main road with a playing field behind')
add('morgan-creek-guide', 'own-R3168794-58', 'South Surrey - Morgan', 'R3168794-58.jpg', 'Outdoor lap pool with a timber pergola and lounge deck at a Morgan Creek townhome complex')
add('morgan-creek-south-surrey-condos-townhomes-for-sale', 'own-R3168794-05', 'South Surrey - Morgan', 'R3168794-5.jpg', 'Aerial view of clustered Morgan Creek townhomes with shake-style roofs and mature landscaping')
add('grandview-south-surrey-houses-for-sale', 'own-R3153853-03', 'South Surrey - Grandvi', 'R3153853-3.jpg', 'Aerial view over Grandview Heights forest and farm lots with Boundary Bay and the new neighbourhoods beyond')
add('grandview-south-surrey-houses-for-sale', 'own-R3153853-04', 'South Surrey - Grandvi', 'R3153853-4.jpg', 'Aerial view of Grandview Heights rural lots, tilled fields and the Highway 99 corridor')
add('grandview-surrey', 'own-R3153853-05', 'South Surrey - Grandvi', 'R3153853-5.jpg', 'Aerial view along a Grandview road with farm lots on one side and new townhome developments on the other')
add('ocean-park-homes-for-sale', 'own-oceanpark-01', 'South Surrey - Ocean P', 'MLSTBD-1846-127A-1.jpg', 'West-coast style Ocean Park home with a stone chimney and tall cedars along the driveway')
add('ocean-park-homes-for-sale', 'own-oceanpark-02', 'South Surrey - Ocean P', 'MLSTBD-1846-127A-2.jpg', 'Front of a cedar-clad Ocean Park house with picture windows under mature trees')
# Surrey: Fleetwood, Clayton
add('fleetwood-tynehead', 'own-R3065812-05', 'Surrey - Fleetwood', 'R3065812-5.jpg', 'Aerial view of Fleetwood white-and-grey townhomes along a quiet complex street')
add('fleetwood-tynehead', 'own-R3065812-03', 'Surrey - Fleetwood', 'R3065812-3.jpg', 'Aerial view of rows of Fleetwood townhomes with back patios and green landscaping between the buildings')
add('fleetwood-tynehead-surrey-condos-townhomes-for-sale', 'own-R3065812-01', 'Surrey - Fleetwood', 'R3065812-1.jpg', 'Overhead view of parallel townhome rows and lanes in a Fleetwood complex among autumn trees')
add('clayton-cloverdale-condos-townhomes-for-sale', 'own-R2979540-02', 'Cloverdale - Clayton', 'R2979540-2.jpg', 'Mid-rise condo building with a stone fountain in the entry court and timber-frame porte-cochère')
add('clayton-guide', 'own-R2979540-03', 'Cloverdale - Clayton', 'R2979540-3.jpg', 'Stone water feature and brick-paved entry circle in front of a Cloverdale condo building')
# Chilliwack: Rosedale, Sardis
add('rosedale-homes-for-sale', 'own-R3123828-03', 'Chilliwack - Rosedale', 'R3123828-3.jpg', 'Rosedale house with a double garage and gravel drive beside open fields and the mountains')
add('rosedale-homes-for-sale', 'own-R3123828-04', 'Chilliwack - Rosedale', 'R3123828-4.jpg', 'Small Rosedale house on a corner lot with farmland and the mountain range behind')
add('rosedale-guide', 'own-R3123828-01', 'Chilliwack - Rosedale', 'R3123828-1.jpg', 'Rosedale home with a landscaped yard, cedar hedge and open pasture on the edge of the village')
add('sardis-homes-for-sale', 'own-sardis-04', 'Chilliwack - Sardis', 'MLSTBD-3-46000Thomas-4.jpg', 'Aerial view of single-level homes in a Sardis complex with a fenced lane and forest behind')
add('sardis-houses-for-sale', 'own-sardis-05', 'Chilliwack - Sardis', 'MLSTBD-3-46000Thomas-5.jpg', 'Aerial view over rows of Sardis single-level homes with landscaped yards and a quiet complex road')
# Maple Ridge: West Central, Albion
add('west-central', 'own-R2996688-30', 'Maple Ridge - West Central', 'R2996688-30.jpg', 'Grassy courtyard and cedar-fenced patios behind a West Central Maple Ridge townhome row')
add('albion', 'own-R2897151-54', 'Maple Ridge - Albion', 'R2897151-54.jpg', 'Aerial view of Albion rows of detached homes with the Fraser River and valley behind')
add('albion', 'own-R2897151-55', 'Maple Ridge - Albion', 'R2897151-55.jpg', 'Aerial view over Albion’s planned streets, forest edge and the river valley')
add('albion-maple-ridge-houses-for-sale', 'own-R2897151-49', 'Maple Ridge - Albion', 'R2897151-49.jpg', 'Aerial view of Albion small-lot homes along tree-lined streets beside a green belt')
add('albion-maple-ridge-houses-for-sale', 'own-R2897151-52', 'Maple Ridge - Albion', 'R2897151-52.jpg', 'Aerial view of long rows of Albion detached homes with lane access and mountains in the distance')
# Langley City
add('langley-city', 'own-R2919589-46', 'Langley City', 'R2919589-46.jpg', 'Aerial view of Langley City’s downtown core with low-rise condo buildings and the North Shore mountains')
add('city-of-langley-condos-for-sale', 'own-R2919589-47', 'Langley City', 'R2919589-47.jpg', 'Aerial view of Langley City low-rise condo buildings among mature trees')
# Delta: North Delta, Ladner
add('north-delta-homes-for-sale', 'own-R3060138-05', 'Delta - North Delta', 'R3060138-5.jpg', 'Aerial view of North Delta streets with a mix of newer and older detached homes and large back gardens')
add('north-delta-homes-under-1-2m', 'own-R3060138-01', 'Delta - North Delta', 'R3060138-1.jpg', 'Overhead view of a North Delta block of detached homes with deep lots and a side street')
add('ladner-homes-for-sale', 'own-R2715710-61', 'Ladner', 'R2715710-61.jpg', 'Aerial view of Ladner detached homes and quiet streets with farmland and the mountains beyond')
add('ladner-homes-for-sale', 'own-R2715710-62', 'Ladner', 'R2715710-62.jpg', 'Aerial view over a Ladner neighbourhood with farmland and mountains on the horizon')
add('ladner-houses-for-sale', 'own-R3178883-01', 'Ladner', 'R3178883-1.jpg', 'Aerial view of a Ladner cul-de-sac with large detached homes in autumn colour and the North Shore mountains')
add('ladner-rural', 'own-R3178883-04', 'Ladner', 'R3178883-4.jpg', 'Aerial view of a Ladner neighbourhood bordering farm fields, one planted red, with the delta flatlands beyond')
# Abbotsford: Sumas Mountain
add('sumas-mountain', 'own-R3168865-20', 'Abbotsford - Sumas Mountain', 'R3168865-20.jpg', 'Aerial view of Sumas Mountain’s forested slope above the Fraser Valley farmland with the mountains beyond')
add('sumas-mountain', 'own-R3168865-15', 'Abbotsford - Sumas Mountain', 'R3168865-15.jpg', 'Aerial view of a road and rail line curving along the base of Sumas Mountain beside barns and fields')
add('sumas-mountain-abbotsford-houses-for-sale', 'own-R3168865-05', 'Abbotsford - Sumas Mountain', 'R3168865-5.jpg', 'Aerial view of a Sumas Mountain acreage with a horse barn, riding arena and pasture')
add('sumas-mountain-abbotsford-houses-for-sale', 'own-R3168865-10', 'Abbotsford - Sumas Mountain', 'R3168865-10.jpg', 'Aerial view of farm fields and tree lines on the lower slopes of Sumas Mountain')


def process(src, folder, fn, pid, blur):
    g = glob.glob(os.path.join(src, folder + '*', fn))
    assert len(g) == 1, f'{pid}: {folder}/{fn} -> {g}'
    im = ImageOps.exif_transpose(Image.open(g[0])).convert('RGB')
    for box in blur:
        reg = im.crop(box).filter(ImageFilter.GaussianBlur(18)); im.paste(reg, box[:2])
    w, h = im.size
    for tw in (640, 1280):
        im.resize((tw, round(h * tw / w)), Image.LANCZOS).save(f'{OUT_IMG}/{pid}-{tw}.webp', 'WEBP', quality=76, method=6)
    return round(h * 1280 / w)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--src', required=True); a = ap.parse_args()
    ids = [p[1] for p in P]; assert len(ids) == len(set(ids)), 'duplicate id'
    data = json.load(open(OUT_JSON, encoding='utf-8'))
    for slug in list(data):  # idempotent: drop earlier entries of this run
        data[slug] = [e for e in data[slug] if e['id'] not in ids]
    new = {}
    for page, pid, folder, fn, alt, blur in P:
        assert 20 <= len(alt) <= 150, f'{pid}: alt length {len(alt)}'
        h = process(a.src, folder, fn, pid, blur)
        new.setdefault(page, []).append({'id': pid, 'alt': alt, 'w': 1280, 'h': h, 'own': True, 'cropped': False, 'wide': False})
    for page, lst in new.items():
        assert os.path.exists(os.path.join(ROOT, f'src/data/local/{page}.json')) or os.path.exists(os.path.join(ROOT, f'src/data/pages/{page}.json')), page
        data[page] = lst + data.get(page, [])
    for slug in [s for s in data if not data[s]]: del data[slug]
    json.dump(data, open(OUT_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{len(P)} photos on {len(new)} pages')


if __name__ == '__main__':
    main()
