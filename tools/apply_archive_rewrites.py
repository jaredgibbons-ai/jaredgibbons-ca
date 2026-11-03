"""Apply approved rewrites of archived paragraphs (Jared approved 2026-11-03: rewrite archive wording where sibling pages repeat the same sentences).

Input:  docs/review/archive-rewrites/<slug>.json = {"slug":..., "items": {"<block index>": {"old": "...", "new": "..."}}}
Effect: replaces the paragraph at that index in src/data/pages/<slug>.json (plain-text paragraphs only; paragraphs with links are never touched).
Guards (a rewrite that fails any guard is NOT applied and is listed): the block's current text must equal "old" (so a rerun is safe and a changed page is not overwritten);
every number in the old text appears in the new; length within 60%-150%; no run of 8 consecutive words copied from the old text; no URL, markdown or emoji.
The originals stay in the JSON files and in git history.   python3 -I tools/apply_archive_rewrites.py [--dry]"""
import glob, json, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DIR = os.path.join(ROOT, 'docs/review/archive-rewrites'); PAGES = os.path.join(ROOT, 'src/data/pages')
def W(s): return re.findall(r"[a-z0-9$%'’.\-]+", s.lower())
def text_of(b): return ' '.join(x['t'] for x in b.get('parts', [])) if 'parts' in b else b.get('text', '')


def check(old, new):
    if not new or len(new) < 20: return 'empty'
    if re.search(r'https?://|[*_#`]|[\U0001F300-\U0001FAFF]|[“”"]\s*$', new): return 'markup'
    r = len(new) / len(old)
    if r < 0.6 or r > 1.5: return f'length {r:.2f}'
    nums_old = set(re.findall(r'\d[\d,.]*\d|\d', old)); nums_new = set(re.findall(r'\d[\d,.]*\d|\d', new))
    if nums_old - nums_new: return 'numbers lost: ' + ','.join(sorted(nums_old - nums_new))
    if nums_new - nums_old: return 'numbers added: ' + ','.join(sorted(nums_new - nums_old))
    wo, wn = W(old), W(new); so = {' '.join(wo[i:i + 8]) for i in range(max(0, len(wo) - 7))}
    if any(' '.join(wn[i:i + 8]) in so for i in range(max(0, len(wn) - 7))): return 'copies 8 words'
    return None


def main():
    dry = '--dry' in sys.argv; done = bad = 0; rep = []
    for f in sorted(glob.glob(f'{DIR}/*.json')):
        j = json.load(open(f, encoding='utf-8')); slug = j['slug']; pf = f'{PAGES}/{slug}.json'
        raw = open(pf, encoding='utf-8').read(); d = json.loads(raw); ch = False
        for k, it in j['items'].items():
            b = d['blocks'][int(k)]
            if b['t'] != 'p' or any(x.get('h') for x in b.get('parts', [])): rep.append((slug, k, 'not a plain paragraph')); bad += 1; continue
            cur = text_of(b)
            if cur == it['new']: continue
            if cur != it['old']: rep.append((slug, k, 'page text changed')); bad += 1; continue
            why = check(it['old'], it['new'])
            if why: rep.append((slug, k, why)); bad += 1; continue
            b.pop('text', None); b['parts'] = [{'t': it['new']}]; ch = True; done += 1
        if ch and not dry:
            indent = 1 if raw.startswith('{\n') else None
            open(pf, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=indent, separators=(',', ':') if indent is None else None))
    print('rewrites applied', done, '; not applied', bad)
    for r in rep: print('  ', *r)


if __name__ == '__main__':
    main()
