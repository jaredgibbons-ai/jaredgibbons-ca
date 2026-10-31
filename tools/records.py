"""Parser for archive page-text records (folder 09 / folder 02 .md files).

Each record has: a metadata list, "## Heading outline", "## Exact visible text",
"## Components in order of appearance". This module only parses; it never edits
wording. Whitespace is trimmed per line and blank lines are dropped, nothing else.
"""
from __future__ import annotations
import os, re
from dataclasses import dataclass, field

H_META = '## Heading outline'
H_TEXT = '## Exact visible text'
H_COMP = '## Components in order of appearance'


@dataclass
class Record:
    file: str
    url: str = ''
    kind: str = ''
    status: str = ''
    title: str = ''
    canonical: str = ''
    sha: str = ''
    meta: dict = field(default_factory=dict)
    outline: list = field(default_factory=list)   # [(level, text)]
    lines: list = field(default_factory=list)     # visible text, trimmed, no blanks
    raw_lines: list = field(default_factory=list) # visible text, untrimmed
    comps: list = field(default_factory=list)     # [(kind, label, target)]


_META = re.compile(r'^- ([^:]+): ?(.*)$')
_COMP = re.compile(r'^- (LINK|IMG|IMAGE|FORM|IFRAME|[A-Z]+)\s*(?:\[(.*?)\])?\s*(?:->|=>)?\s*(.*)$')


def parse(path: str) -> Record:
    t = open(path, encoding='utf-8').read()
    r = Record(file=os.path.basename(path))
    # Section order is not fixed across the archive; slice by actual positions.
    pos = sorted((t.index(h), h) for h in (H_META, H_TEXT, H_COMP))
    sect = {}
    for n, (p, h) in enumerate(pos):
        end = pos[n + 1][0] if n + 1 < len(pos) else len(t)
        sect[h] = t[p:end]
    head = t[:pos[0][0]]
    outline, text, comp = sect[H_META], sect[H_TEXT], sect[H_COMP]
    for ln in head.splitlines():
        m = _META.match(ln)
        if m:
            r.meta[m.group(1)] = m.group(2)
    r.url = r.meta.get('Final URL', '')
    r.kind = r.meta.get('Source sitemap/kind', '')
    r.status = r.meta.get('HTTP status', '')
    r.title = r.meta.get('Title', '')
    r.canonical = r.meta.get('Canonical', '')
    r.sha = r.meta.get('SHA-256 of source', '')
    for ln in outline.splitlines()[1:]:
        m = re.match(r'^(#{2,6}) (.*)$', ln)
        if m:
            r.outline.append((len(m.group(1)) - 1, m.group(2)))   # D-03: ## = H1
    body = text.split('\n', 1)[1] if '\n' in text else ''
    r.raw_lines = body.splitlines()
    r.lines = [x.strip() for x in r.raw_lines if x.strip()]
    for ln in comp.splitlines()[1:]:
        if not ln.startswith('- '):
            continue
        m = _COMP.match(ln)
        if m:
            r.comps.append((m.group(1), m.group(2) or '', m.group(3).strip()))
        else:
            r.comps.append(('?', '', ln[2:]))
    return r


def load_all(d: str):
    out = {}
    for f in sorted(os.listdir(d)):
        if f.endswith('.md'):
            out[f] = parse(os.path.join(d, f))
    return out
