#!/usr/bin/env python3
"""Photos for older sold listings from Jared's Drive deal folders (D-323). The site had 0 to 2 photos for these pages (the old
site's copies were lost); Jared's own listing photos are in Drive under SELLERS 2021 / Sellers 2022, "<address>/Photos & FP".

    python3 -I tools/add_deal_photos.py /home/claude/private-sales/photos-new/records.json

records.json (kept private, outside the repo): {drive_id: {"slug", "i" (order), "file" (downloaded original), "alt"}}.
Each photo becomes public/img/listings/<id>-480.webp and -1280.webp (id = first 16 hex of the original's SHA-256) and the
listing's src/data/listing-photos/<slug>.json is replaced by the new set, in order, each with its alt text ("cap", written
by looking at the photo). Served as static files rather than from R2, so no upload step is needed.
"""
import hashlib, json, os, sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'public/img/listings'


def main(rec_path):
    rec = json.loads(Path(rec_path).read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    by = {}
    for fid, r in rec.items():
        if r.get('skip'): continue
        by.setdefault(r['slug'], []).append(r)
    for slug, rs in sorted(by.items()):
        photos = []
        for p, r in enumerate(sorted(rs, key=lambda r: r['i']), 1):
            data = Path(r['file']).read_bytes()
            pid = hashlib.sha256(data).hexdigest()[:16]
            im = ImageOps.exif_transpose(Image.open(r['file'])).convert('RGB')
            sizes = {}
            for size, q in ((1280, 78), (480, 72)):
                f = OUT / f'{pid}-{size}.webp'
                a = im.copy(); a.thumbnail((size, size), Image.LANCZOS)
                if not f.exists(): a.save(f, 'WEBP', quality=q, method=5)
                sizes[size] = a.size
            w, h = sizes[1280]
            photos.append({'p': p, 'w': w, 'h': h, 'u': {'s': f'/img/listings/{pid}-480.webp', 'l': f'/img/listings/{pid}-1280.webp'}, 'cap': r['alt']})
        (ROOT / 'src/data/listing-photos' / f'{slug}.json').write_text(json.dumps(photos, ensure_ascii=False) + '\n')
        print(slug, len(photos))


if __name__ == '__main__':
    main(sys.argv[1])
