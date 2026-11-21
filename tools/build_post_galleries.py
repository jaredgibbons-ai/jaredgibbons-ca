#!/usr/bin/env python3
"""Listing photos inside the old listing blog posts (D-394).

The old posts only ever showed one lead photo plus Jared's headshot. The listing photos for 13 of those properties are in
Jared's Google Drive deal folders; four per property were picked by looking at them (no people, no paperwork, no family
photos, no other brokerages' signs) and given plain alt text. This tool turns the picked originals into web sizes and
writes src/data/post-galleries.json, which GenericPage.astro shows as a small "Photos from this listing" grid in each post.

    python3 -I tools/build_post_galleries.py --picks PICKS.json [PICKS.json ...]

PICKS.json = {property: [{id, file, alt}, ...]}  (id = Drive file id, file = local original).
Written: public/img/blog/gallery/<property>-<n>-{480,960}.webp   and   src/data/post-galleries.json
         { post-slug: [{src480, src960, w, h, alt}] }
Originals are not kept in the repository. Colour profiles are converted to sRGB and no metadata is copied.
"""
import argparse, io, json
from pathlib import Path
from PIL import Image, ImageCms, ImageOps

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'public/img/blog/gallery'
DATA = ROOT / 'src/data/post-galleries.json'
SRGB = ImageCms.createProfile('sRGB')

# property -> the posts about it (checked against each post's own address).
POSTS = {
    'saddlehorn': ['sold-stunning-custom-home-at-4543-saddlehorn-crescent-8660216'],
    'helc': ['new-listing-145-2853-helc-place-grandview-surrey-townhome-for-sale-8895553'],
    '4657-208a': ['4657-208a-street-langley-4-bedroom-split-level-home-with-large-lot-8814843', 'just-listed-4657-208a-street-langley-8777216'],
    'evans': ['new-listing-in-sardis-chilliwack-404-7694-evans-road-condo-for-sale-8888665'],
    'croydon': ['new-listing-220-15735-croydon-drive-south-surrey-condo-for-sale-8886776', 'price-reduced-south-surrey-2-bedroom-condo-8934352'],
    'rowland': ['new-listing-104-2109-rowland-st-port-coquitlam-8996885'],
    '5327-192': ['for-sale-flexible-warehouse-office-space-at-12-5327-192-street-8876121'],
    'royal': ['2-bed-condo-on-royal-avenue-white-rock-9072037'],
    '9072-fleetwood': ['115-9072-fleetwood-way-599k-8919895'],
    'calgary': ['penticton-4-plex-investment-116-calgary-ave-8749199', 'penticton-fourplex-investment-116-calgary-ave-9142471'],
    '8929-202': ['1-bed-den-at-the-grove-walnut-grove-469k-9028946', 'walnut-grove-1-bed-den-drops-to-439000-the-grove-9111628', 'walnut-grove-condo-price-drop-a218-8929-202-st-langley-9160362'],
    'miller': ['just-sold-renovated-home-at-8316-miller-crescent-mission-8692568'],
    'enterprise': ['industrial-unit-for-lease-in-cloverdale-104-19232-enterprise-way-8897647'],
}


def load(path: str) -> Image.Image:
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)
    icc = im.info.get('icc_profile')
    im = im.convert('RGB')
    if icc:
        try:
            im = ImageCms.profileToProfile(im, ImageCms.ImageCmsProfile(io.BytesIO(icc)), SRGB, outputMode='RGB')
        except Exception:
            pass
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--picks', nargs='+', required=True)
    a = ap.parse_args()
    picks = {}
    for p in a.picks:
        picks.update(json.load(open(p)))
    OUT.mkdir(parents=True, exist_ok=True)
    data = {}
    for prop, slugs in POSTS.items():
        items = []
        for n, pk in enumerate(picks.get(prop, []), 1):
            im = load(pk['file'])
            out = {}
            for w in (480, 960):
                t = im.copy()
                t.thumbnail((w, w * 2), Image.LANCZOS)
                name = f'{prop}-{n}-{w}.webp'
                t.save(OUT / name, 'WEBP', quality=76 if w == 960 else 72, method=6)
                out[w] = (name, t.size)
            items.append({'src480': '/img/blog/gallery/' + out[480][0], 'src960': '/img/blog/gallery/' + out[960][0],
                          'w': out[960][1][0], 'h': out[960][1][1], 'alt': pk['alt'].strip()})
        if items:
            for s in slugs:
                assert (ROOT / 'src/data/posts' / f'{s}.json').exists(), s
                data[s] = items
    DATA.write_text(json.dumps(data, indent=1, ensure_ascii=False) + '\n')
    print(len(data), 'posts,', sum(len(v) for v in data.values()), 'photo slots')


if __name__ == '__main__':
    main()
