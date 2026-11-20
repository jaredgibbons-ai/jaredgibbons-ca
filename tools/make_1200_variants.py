#!/usr/bin/env python3
"""1200px copies of the large photos on the designed pages (mobile audit, Nov 20 2026).

A phone at 3x density asks for about 1,170px for a full-width photo, so with only 800w and 1600w on offer it downloaded the 1600px file
(250-280 KB each on /selling.html). A 1200w step in between is about 40% lighter. Only images 1,400px wide or more get one; existing
files are left alone (idempotent).

    python3 -I tools/make_1200_variants.py
"""
import glob, re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
srcs = set()
for f in glob.glob(str(ROOT / 'src/data/designed/*.json')):
    srcs.update(re.findall(r'"src":\s*"(/img/[^"]+)"', Path(f).read_text()))
for s in sorted(srcs):
    full, out = ROOT / f'public{s}.webp', ROOT / f'public{s}-1200.webp'
    if not full.exists() or out.exists():
        continue
    im = Image.open(full)
    if im.size[0] < 1400:
        continue
    im.resize((1200, round(im.size[1] * 1200 / im.size[0])), Image.LANCZOS).save(out, 'WEBP', quality=75, method=6)
    print('wrote', out.relative_to(ROOT), out.stat().st_size // 1024, 'KB')
