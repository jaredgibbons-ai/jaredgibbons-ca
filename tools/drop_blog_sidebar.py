#!/usr/bin/env python3
"""Drop the MyRealPage blog sidebar ("Blogs" category list and "Posts By Date" month list) from each post.
Its links pointed at month/category filter pages that are not rebuilt (and carried a doubled
/blog.html/blog.html prefix, so they were broken on the old site too). Idempotent."""
import json, glob
n = 0
for f in sorted(glob.glob('src/data/posts/*.json')):
    d = json.load(open(f))
    out, skip, ch = [], False, False
    for b in d['blocks']:
        if skip:
            skip = False
            if b.get('t') == 'list':
                ch = True
                continue
        if b.get('t') == 'p' and b.get('parts') and b['parts'][0].get('t') in ('Blogs', 'Posts By Date'):
            skip = True; ch = True
            continue
        out.append(b)
    if ch:
        d['blocks'] = out
        json.dump(d, open(f, 'w'), ensure_ascii=False, separators=(',', ':'))
        n += 1
print('posts changed', n)
