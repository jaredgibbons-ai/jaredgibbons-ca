#!/usr/bin/env python3
"""Blog post lead photos (D-259).

Each post on the old MyRealPage blog named one lead photo (its og:image; 198 of the 200 posts had one). Those addresses stopped
loading when the site moved, so the new blog had no pictures. This tool turns the originals into the sizes the site serves and
records them in src/data/post-images.json, which the blog index, the post pages and the share tags read.

    python3 -I tools/build_post_images.py --orig DIR [--alts FILE] [--fresh] [--only SLUG ...]

DIR holds one original per post, named <post slug>.bin (JPEG, PNG or WebP). tools/post_images/sources.tsv lists where each came
from (post slug <tab> address), so they can be fetched again while the MyRealPage account is open. The originals are not in the
repository (about 300 MB).

Written for each post:
  public/img/blog/<slug>-<width>.webp   480, 800 and 1200 px wide, never larger than the original (a small original keeps its own width)
  public/img/blog/<slug>-og.jpg         the share card, 1200 x 630 (originals 600 px wide and up): a centre crop for photos,
                                        the whole picture on a matching background for graphics (`fit: contain`)
  src/data/post-images.json             { slug: { alt, w, h, widths, og, fit?, bg?, pos?, share? } }

`alt`, `fit`, `pos` and `share` are written by hand and kept on a re-run; --alts FILE ({slug: {alt, fit?, pos?, share?}}) sets them
the first time (with --fresh the data file's own values are dropped first).
  fit: "contain"    a graphic whose words must not be cropped: cards and the share card show all of it, on the `bg` colour
                    taken from its own edges (the share card uses a blurred copy of the picture when the edges are not one colour)
  pos: "100% 50%"   where the crop sits (across, down) when a card or the share card cannot show the whole photo
  share: "whole"    only the share card shows all of the picture (a title at the top that the 1.9:1 crop would cut)
Colour profiles are converted to sRGB, transparency is flattened on white, and no metadata is copied.
"""
import argparse, io, json, os, sys
from multiprocessing import Pool
from pathlib import Path
from PIL import Image, ImageCms, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'public/img/blog'
DATA = ROOT / 'src/data/post-images.json'
STEPS = (480, 800, 1200)
OG_W, OG_H = 1200, 630
NEUTRAL = '#e9e9e9'
EDGE_FLAT = 10   # mean distance from the median edge colour (0 to 255) under which the edges count as one colour
SRGB = ImageCms.createProfile('sRGB')


def widths_for(w: int) -> list[int]:
    """The sizes to write: each step well under the top size, then the top size itself (the original's width, at most 1200)."""
    top = min(w, STEPS[-1])
    return [s for s in STEPS if s < top and top / s >= 1.15] + [top]


def load(path: Path) -> tuple[Image.Image, str]:
    im = Image.open(path)
    fmt = im.format or ''
    im = ImageOps.exif_transpose(im)
    icc = im.info.get('icc_profile')
    if im.mode in ('RGBA', 'LA', 'PA') or (im.mode == 'P' and 'transparency' in im.info):
        rgba = im.convert('RGBA')
        flat = Image.new('RGB', rgba.size, 'white')
        flat.paste(rgba, mask=rgba.getchannel('A'))
        im = flat
    elif im.mode != 'RGB':
        im = im.convert('RGB')
    if icc:
        try:
            src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
            if 'srgb' not in ImageCms.getProfileDescription(src).lower():
                im = ImageCms.profileToProfile(im, src, SRGB, outputMode='RGB')
        except Exception:   # an unreadable profile: keep the pixels as they are
            pass
    return im, fmt


def edge_colour(im: Image.Image, sides: str) -> str:
    """The colour of the picture's own edges (top and bottom, or left and right) when they are one flat colour; else a neutral grey."""
    w, h = im.size
    t = max(2, round(min(w, h) * 0.02))
    strips = [im.crop((0, 0, w, t)), im.crop((0, h - t, w, h))] if sides == 'tb' else [im.crop((0, 0, t, h)), im.crop((w - t, 0, w, h))]
    raw = b''.join(s.resize((64, 4) if sides == 'tb' else (4, 64), Image.BOX).tobytes() for s in strips)
    px = [raw[i:i + 3] for i in range(0, len(raw), 3)]
    med = [sorted(c[i] for c in px)[len(px) // 2] for i in range(3)]
    spread = sum(sum(abs(c[i] - med[i]) for i in range(3)) for c in px) / (3 * len(px))
    return '#%02x%02x%02x' % tuple(med) if spread < EDGE_FLAT else NEUTRAL


def save_webp(im: Image.Image, path: Path, quality: int) -> None:
    im.save(path, 'WEBP', quality=quality, method=6)


def one(job: tuple[str, str, dict]) -> tuple[str, dict]:
    slug, src, hand = job
    im, fmt = load(Path(src))
    graphic = fmt == 'PNG' or hand.get('fit') == 'contain'   # flat colour and lettering: a higher quality keeps the edges clean
    ws = widths_for(im.width)
    top = None
    for w in ws:
        r = im if w == im.width else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        q = 84 if graphic else (78 if w <= 480 else 76 if w <= 800 else 72)
        save_webp(r, OUT / f'{slug}-{w}.webp', q)
        top = r
    rec: dict = {'alt': hand.get('alt', ''), 'w': top.width, 'h': top.height, 'widths': ws, 'og': False}
    if hand.get('fit') == 'contain':
        rec['fit'] = 'contain'
        rec['bg'] = edge_colour(top, 'tb' if top.width / top.height > 1.5 else 'lr')
    for k in ('pos', 'share'):
        if hand.get(k):
            rec[k] = hand[k]
    # The share card: 1200 x 630, or smaller in the same shape when the original is smaller (never enlarged; under 600 wide there is none).
    og = OUT / f'{slug}-og.jpg'
    ar = OG_W / OG_H
    px, py = [float(v.rstrip('%')) / 100 for v in str(hand.get('pos', '50% 50%')).split()]
    whole = (rec.get('fit') == 'contain' or hand.get('share') == 'whole') and abs(im.width / im.height / ar - 1) > 0.03
    if whole:   # all of the picture: on its own edge colour, or (no flat edge) on a blurred, darkened copy of itself
        ch = min(OG_H, im.height); cw = round(ch * ar)
        if cw >= 600:
            colour = edge_colour(top, 'tb' if im.width / im.height > ar else 'lr')
            if colour == NEUTRAL:
                canvas = ImageEnhance.Brightness(ImageOps.fit(im, (cw, ch), Image.BILINEAR).filter(ImageFilter.GaussianBlur(cw / 40))).enhance(0.55)
            else:
                canvas = Image.new('RGB', (cw, ch), colour)
            fitted = ImageOps.contain(im, (cw, ch), Image.LANCZOS)
            canvas.paste(fitted, ((cw - fitted.width) // 2, (ch - fitted.height) // 2))
    else:       # the largest 1.9:1 crop, centred or on `pos`
        bw = min(im.width, round(im.height * ar))
        cw = min(OG_W, bw); ch = round(cw / ar)
        if cw >= 600:
            canvas = ImageOps.fit(im, (cw, ch), Image.LANCZOS, centering=(px, py))
    if cw >= 600:
        canvas.save(og, 'JPEG', quality=84 if graphic else 78, optimize=True, progressive=True, subsampling=0 if graphic else 2)
        rec['og'] = [cw, ch]
    elif og.exists():
        og.unlink()
    # drop sizes left over from an earlier run with other settings
    for old in OUT.glob(f'{slug}-*.webp'):
        if old.name not in {f'{slug}-{w}.webp' for w in ws}:
            old.unlink()
    return slug, rec


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--orig', required=True)
    ap.add_argument('--alts')
    ap.add_argument('--only', nargs='*')
    ap.add_argument('--fresh', action='store_true', help='take alt, fit, pos and share from --alts alone, not from the data file')
    a = ap.parse_args()
    posts = {p.stem for p in (ROOT / 'src/data/posts').glob('*.json')}
    data = json.loads(DATA.read_text()) if DATA.exists() else {}
    hand = json.loads(Path(a.alts).read_text()) if a.alts else {}
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = []
    for f in sorted(Path(a.orig).glob('*.bin')):
        slug = f.stem
        if a.only and slug not in a.only:
            continue
        if slug not in posts:
            sys.exit(f'{slug}: no such post in src/data/posts')
        h = {} if a.fresh else {k: v for k, v in data.get(slug, {}).items() if k in ('alt', 'fit', 'pos', 'share')}
        h.update(hand.get(slug, {}))
        if not h.get('alt'):
            sys.exit(f'{slug}: no alt text (give --alts or write it into {DATA.name})')
        jobs.append((slug, str(f), h))
    with Pool(os.cpu_count() or 2) as pool:
        for i, (slug, rec) in enumerate(pool.imap_unordered(one, jobs), 1):
            data[slug] = rec
            if i % 20 == 0:
                print(f'  {i}/{len(jobs)}', flush=True)
    # one post per line, so a change to one alt text is a one-line diff
    DATA.write_text('{\n' + ',\n'.join(f' {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}' for k, v in sorted(data.items())) + '\n}\n')
    size = sum(f.stat().st_size for f in OUT.iterdir())
    print(f'{len(jobs)} posts processed, {len(data)} recorded, {len(list(OUT.iterdir()))} files, {size / 1048576:.1f} MB in {OUT.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
