"""Removes internal research file paths from published text (src/data/local/*.json): '(BC Ministry K-12 file, ~/workspace/.../x.csv, read 2026-11-01)' becomes '(BC Ministry K-12 file)',
and a parenthetical that was only a path ('(~/workspace/.../x.md, read 2026-11-01)', '(see ~/workspace/..., items 5 and 7f)') is removed. Only files that contain a path are rewritten,
each in its own indent and key order.   python3 -I tools/strip_file_paths.py [--dry]"""
import glob, json, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); LOCAL = os.path.join(ROOT, 'src/data/local')
PAREN = re.compile(r'\s*\(([^()]*~/workspace/[^()]*)\)')
PATH = re.compile(r'(?:see\s+)?~/workspace/\S+?\.(?:csv|md|xlsx|json|txt)', re.I)
n = {'paren': 0, 'files': 0}
def fix(s):
    def one(m):
        inner = PATH.sub('', m.group(1)); inner = re.sub(r',?\s*\bread \d{4}-\d\d-\d\d\b', '', inner); inner = re.sub(r',?\s*\bitems? [\w ,]+?(?=,|$)', '', inner)
        inner = re.sub(r'^[\s,;]+|[\s,;]+$', '', inner); inner = re.sub(r'\s*,\s*,', ',', inner); n['paren'] += 1
        return f' ({inner})' if inner else ''
    return re.sub(r'\s+([.,;:])', r'\1', PAREN.sub(one, s))
def walk(o, key=None):
    if isinstance(o, str): return fix(o) if '~/workspace/' in o and key not in ('gen', 'slug') else o
    if isinstance(o, list): return [walk(x, key) for x in o]
    if isinstance(o, dict): return {k: walk(v, k) for k, v in o.items()}
    return o
for f in sorted(glob.glob(os.path.join(LOCAL, '*.json'))):
    raw = open(f, encoding='utf-8').read()
    if '~/workspace/' not in raw: continue
    d = json.loads(raw); new = walk(d); ind = 1 if raw.startswith('{\n "') else 2
    out = json.dumps(new, indent=ind, ensure_ascii=False) + ('\n' if raw.endswith('\n') else '')
    n['files'] += 1
    if '--dry' not in sys.argv: open(f, 'w', encoding='utf-8').write(out)
print(n)
