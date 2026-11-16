#!/usr/bin/env python3
"""Rewrites the existing local-notes headings ("<Topic>: streets and boundaries" and seven more, gen 'uq') in src/data/local
with tools/heading_voice.py (D-308). Text-only edit of the heading strings, so every file keeps its own JSON layout.
Safe to run again: a heading that no longer has the old pattern is left alone.
    python3 -I tools/plain_headings.py [--dry]"""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from heading_voice import heading, KEYS  # noqa: E402
ROOT = os.path.dirname(HERE)
PAT = re.compile(r'^(.+): (' + '|'.join(map(re.escape, KEYS)) + r')$')
seo = json.load(open(os.path.join(ROOT, 'src/data/seo-final.json')))
changed = files = 0
for f in sorted(glob.glob(os.path.join(ROOT, 'src/data/local/*.json'))):
    slug = os.path.basename(f)[:-5]
    raw = open(f, encoding='utf8').read(); d = json.loads(raw)
    heads = [b for b in d.get('blocks', []) if b.get('t') == 'h' and b.get('gen') == 'uq' and PAT.match(b.get('text') or '')]
    if not heads: continue
    pg = os.path.join(ROOT, 'src/data/pages', f'{slug}.json')
    other = [b.get('text', '') for b in d.get('blocks', []) if b.get('t') == 'h' and b not in heads]
    if os.path.exists(pg): other += [b.get('text', '') for b in json.load(open(pg)).get('blocks', []) if b.get('t') == 'h']
    taken = {x.lower() for x in other if x}
    new = raw
    for b in heads:
        topic, sec = PAT.match(b['text']).groups()
        h = heading(slug, topic, sec, frozenset(taken)); taken.add(h.lower())
        if h == b['text']: continue
        for form in (json.dumps(b['text']), json.dumps(b['text'], ensure_ascii=False)):
            n = new.count(f'"text": {form}') + new.count(f'"text":{form}')
            if n:
                assert n == 1, (slug, b['text'], n)
                new = new.replace(f'"text": {form}', f'"text": {json.dumps(h, ensure_ascii=False) if form == json.dumps(b["text"], ensure_ascii=False) else json.dumps(h)}').replace(f'"text":{form}', f'"text":{json.dumps(h, ensure_ascii=False)}')
                break
        else:
            raise SystemExit(f'{slug}: heading not found as text: {b["text"]}')
        changed += 1
    if new != raw:
        json.loads(new); files += 1
        if '--dry' not in sys.argv: open(f, 'w', encoding='utf8').write(new)
print(f'{changed} headings in {files} files' + (' (dry run)' if '--dry' in sys.argv else ''))
