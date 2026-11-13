#!/usr/bin/env python3
"""Rewritten blog posts (D-271).

Ten short posts were rewritten by hand with current facts (content/post-rewrites/<slug>.md). This turns each file into blocks for
src/pages/internal/blog/[slug].astro, which uses them in place of the archived body (the H1 and byline stay) and leaves out the
generic "area today" section those posts carried (D-267):

    python3 -I tools/build_post_rewrites.py      -> src/data/post-rewrites.json

File format: a front matter block (title, description, h1), then paragraphs separated by blank lines. "## " and "### " start headings,
"- " starts a list item, [text](url) is a link and **text** is bold (kept as plain text in the block, bold in the lead).
"""
import json, re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'content/post-rewrites'
OUT = ROOT / 'src/data/post-rewrites.json'
POSTS = ROOT / 'src/data/posts'
LINK = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def parts(text: str) -> list:
    """[text](url) links and **bold** runs (rendered as <strong>) as archive-style parts."""
    text = re.sub(r'(?<![\w*])\*([^*]+)\*(?![\w*])', r'\1', text)
    out = []
    for k, seg in enumerate(text.split('**')):
        if not seg:
            continue
        pos = 0
        for m in LINK.finditer(seg):
            if m.start() > pos:
                out.append({'t': seg[pos:m.start()], **({'lead': True} if k % 2 else {})})
            out.append({'t': m.group(1), 'h': m.group(2)})
            pos = m.end()
        if pos < len(seg):
            out.append({'t': seg[pos:], **({'lead': True} if k % 2 else {})})
    # Rich re-joins parts with a space: keep the words, drop the spaces at the joins
    for i, p in enumerate(out):
        p['t'] = p['t'].strip() if not p.get('h') else p['t']
    return [p for p in out if p['t']]


def convert(md: str) -> dict:
    m = re.match(r'---\n(.*?)\n---\n(.*)$', md, re.S)
    head = dict(line.split(': ', 1) for line in m.group(1).splitlines())
    blocks, items = [], []
    for para in re.split(r'\n\s*\n', m.group(2).strip()):
        lines = para.strip().splitlines()
        if all(l.startswith('- ') for l in lines):
            blocks.append({'t': 'list', 'items': [parts(l[2:]) for l in lines]})
        elif lines[0].startswith('### '):
            blocks.append({'t': 'h', 'level': 3, 'text': lines[0][4:]})
        elif lines[0].startswith('## '):
            blocks.append({'t': 'h', 'level': 2, 'text': lines[0][3:]})
        else:
            blocks.append({'t': 'p', 'parts': parts(' '.join(lines))})
    return {'title': head['title'], 'description': head['description'], 'h1': head['h1'], 'blocks': blocks}


def main() -> None:
    known = {p.stem for p in POSTS.glob('*.json')}
    old = json.loads(OUT.read_text()) if OUT.exists() else {}
    data = {}
    for f in sorted(SRC.glob('*.md')):
        slug = f.stem
        assert slug in known, f'{slug}: no such post'
        rec = convert(f.read_text())
        assert len(rec['title']) <= 60, (slug, len(rec['title']))
        assert len(rec['description']) <= 155, (slug, len(rec['description']))
        prev = old.get(slug, {})
        # the date only moves when the wording changes
        same = {k: v for k, v in prev.items() if k != 'updated'} == rec
        rec['updated'] = prev.get('updated') if same and prev.get('updated') else date.today().isoformat()
        words = sum(len(' '.join(p['t'] for p in (b.get('parts') or [])).split()) + len(' '.join(' '.join(x['t'] for x in it) for it in b.get('items', [])).split()) + len(b.get('text', '').split()) for b in rec['blocks'])
        print(f'{words:5d} words  {slug}')
        data[slug] = rec
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n')
    print(f'{len(data)} posts -> {OUT.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
