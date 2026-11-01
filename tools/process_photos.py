"""Turn the listing-photo zip parts (Drive folder 10) into web-size images + per-listing photo lists.

    python3 -I tools/process_photos.py --parts /home/claude/photos/parts --manifest /home/claude/photos/manifest.csv \
        --out /home/claude/photos/out --meta src/data/listing-photos

For every photo in the manifest: verify the SHA-256 of the original, then write two WebP files named by the
first 16 hex digits of that hash (so the 199 photos shared by two listings are stored once):
    <id>-1600.webp (long edge 1600 px, q78)   <id>-960.webp (960 px, q76)   <id>-480.webp (480 px, q72)
Writes <meta>/<listing-slug>.json = [{"p": position, "id": id, "w": width, "h": height}] in page order, and
<out>/_report.json (counts, hash mismatches, missing parts). Originals are never modified and not kept.
Safe to re-run: existing outputs are skipped.
"""
import argparse, csv, hashlib, io, json, os, sys, zipfile
from collections import defaultdict
from multiprocessing import Pool
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = 120_000_000


def convert(args):
    data, pid, out = args
    full, mid, thumb = os.path.join(out, pid + '-1600.webp'), os.path.join(out, pid + '-960.webp'), os.path.join(out, pid + '-480.webp')
    im = ImageOps.exif_transpose(Image.open(io.BytesIO(data)))
    im = im.convert('RGB')
    w0, h0 = im.size
    if not os.path.exists(full):
        a = im.copy(); a.thumbnail((1600, 1600), Image.LANCZOS); a.save(full, 'WEBP', quality=78, method=4)
        w, h = a.size
    else:
        w, h = Image.open(full).size
    if not os.path.exists(mid):
        m = im.copy(); m.thumbnail((960, 960), Image.LANCZOS); m.save(mid, 'WEBP', quality=76, method=4)
    if not os.path.exists(thumb):
        t = im.copy(); t.thumbnail((480, 480), Image.LANCZOS); t.save(thumb, 'WEBP', quality=72, method=4)
    return pid, w, h, (w0, h0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--parts', required=True); ap.add_argument('--manifest', required=True)
    ap.add_argument('--out', required=True); ap.add_argument('--meta', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True); os.makedirs(a.meta, exist_ok=True)
    rows = list(csv.DictReader(open(a.manifest, encoding='utf-8')))
    by_part = defaultdict(list)
    for r in rows:
        by_part[r['zip_part']].append(r)
    dims, bad, missing_parts, seen = {}, [], [], set()
    sizes_cache = {}
    with Pool(2) as pool:
        for part, rs in sorted(by_part.items()):
            p = os.path.join(a.parts, part)
            if not os.path.exists(p):
                missing_parts.append(part); continue
            z = zipfile.ZipFile(p)
            jobs = []
            for r in rs:
                pid = r['sha256'][:16]
                if pid in dims or pid in seen:
                    continue
                data = z.read(r['file_in_zip'])
                if hashlib.sha256(data).hexdigest() != r['sha256']:
                    bad.append(r['file_in_zip']); continue
                seen.add(pid); jobs.append((data, pid, a.out))
            for pid, w, h, orig in pool.imap_unordered(convert, jobs):
                dims[pid] = (w, h)
    lists = defaultdict(list)
    for r in rows:
        pid = r['sha256'][:16]
        if pid in dims:
            lists[r['page_slug'].replace('our-listings.html__', '')].append({'p': int(r['photo_position']), 'id': pid, 'w': dims[pid][0], 'h': dims[pid][1]})
    for slug, items in lists.items():
        items.sort(key=lambda x: x['p'])
        json.dump(items, open(os.path.join(a.meta, slug + '.json'), 'w'), separators=(',', ':'))
    tot = {k: sum(os.path.getsize(os.path.join(a.out, f)) for f in os.listdir(a.out) if f.endswith(k)) for k in ('-1600.webp', '-960.webp', '-480.webp')}
    rep = {'photos_processed': len(dims), 'listings_with_photos': len(lists), 'hash_mismatches': bad, 'missing_parts': missing_parts, 'bytes': tot}
    json.dump(rep, open(os.path.join(a.out, '_report.json'), 'w'), indent=1)
    print({k: (len(v) if isinstance(v, list) else v) for k, v in rep.items()})


if __name__ == '__main__':
    main()
