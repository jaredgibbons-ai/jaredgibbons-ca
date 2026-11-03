"""Jared's "Area Thoughts" (his own words on 219 neighbourhoods, PDF of 2026-11-03) -> one "Jared's take" block on each area's main page.
One page per area (houses-for-sale first, then the area guide, then other pages) so the paragraph is not repeated across sibling pages (uniqueness).
Entries that state a checkable number, year or "only" claim are written to docs/review/area-thoughts-to-verify-2026-11-03.csv and are NOT published until checked.
Usage: python3 -I tools/build_area_thoughts.py <text from pdftotext -layout> [--apply]"""
import csv, glob, json, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
LOCAL = os.path.join(ROOT, 'src/data/local'); PAGES = os.path.join(ROOT, 'src/data/pages')
GEN = 'jtake'
CHECK = re.compile(r"\b(1[5-9]\d\d|20\d\d)s?\b|\d\s?%|\bpercent\b|square kilomet|\bkm\b|\bonly\b|\boldest\b|\blargest\b|\bsmallest\b|\bnewest\b|\bsince\b|\bnamed for\b|\bsettled\b|\b(one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+(?:of\s+)?(?:only\s+)?(?:\w+\s+){0,2}(schools?|parks?|years?|decades?|hectares?|acres?|homes?|units?|conservation areas?|neighbourhoods?|stations?|lakes?)\b", re.I)
def slugify(s): return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('&', ' and ')).strip('-')
def parse(txt):
    out = []; head = None; txt = txt.replace('\x0c', '\n\n')
    HEAD = re.compile(r'^(.*) \(([^()]+)\)$')
    blocks = [[' '.join(l.split()) for l in b.strip().split('\n') if l.strip()] for b in re.split(r'\n\s*\n', txt)]
    blocks = [b for b in blocks if b]
    def is_heading(lines): return len(lines[0]) < 95 and bool(HEAD.match(lines[0])) and not lines[0].endswith('.)')
    for i, lines in enumerate(blocks):
        first = lines[0]
        if is_heading(lines):                                  # "Area (City)", with or without the paragraph in the same block
            m = HEAD.match(first); head = (m.group(1).strip(), m.group(2).strip()); rest = ' '.join(lines[1:])
            if rest: out.append({'name': head[0], 'city': head[1], 'text': rest}); head = None
            continue
        t = ' '.join(lines)
        if len(lines) == 1 and len(t) < 95:                    # a bare heading: the section group ("Surrey") or a city entry (followed by prose)
            nxt = blocks[i + 1] if i + 1 < len(blocks) else None
            if t != 'Area Thoughts' and nxt and not is_heading(nxt) and not (len(nxt) == 1 and len(nxt[0]) < 95):
                head = (t, t)                                  # city-level entry: "Surrey" + its paragraph
            else: head = None
            continue
        if head: out.append({'name': head[0], 'city': head[1], 'text': t}); head = None
    return out
def all_slugs():
    s = set(os.path.basename(p)[:-5] for p in glob.glob(PAGES + '/*.json')) | set(os.path.basename(p)[:-5] for p in glob.glob(LOCAL + '/*.json'))
    return s
SUFFIX = ['-houses-for-sale', '', '-guide', '-condos-townhomes-for-sale', '-condos-for-sale', '-townhomes-for-sale', '-homes-for-sale']
OVERRIDE = {('Greenway', 'South Surrey'): 'greenway-townhomes-south-surrey', ('Jacobsen', 'South Surrey'): 'jacobsen-townhomes-south-surrey',
 ('Dewdney & Deroche', 'Mission'): 'dewdney-deroche', ('Capilano', 'North Vancouver'): 'capilano-nv', ('Canterbury, West Vancouver', 'West Vancouver'): 'canterbury-wv',
 ('Burnaby Hospital Area', 'Burnaby'): 'burnaby-hospital-houses-for-sale', ('Queen\u2019s Park', 'New Westminster'): 'queens-park-new-westminster-houses-for-sale',
 ('South Surrey / White Rock', 'South Surrey'): 'south-surrey-white-rock-ocean-view-homes-for-sale'}
def target(e, slugs):
    o = OVERRIDE.get((e['name'], e['city']))
    if o and o in slugs: return o
    base = slugify(re.sub(r',.*$', '', re.sub(r'\([^)]*\)', '', e['name'])))        # "Murrayville, Langley" -> murrayville
    city = slugify(e['city']); name = slugify(re.sub(r'\([^)]*\)', '', e['name']))
    stems = []
    for b in dict.fromkeys([base, base + '-' + city, name, name + '-' + city, base.replace('-heights', '') if False else base]):
        stems.append(b)
    for st in stems:
        for sf in SUFFIX:
            if st + sf in slugs: return st + sf
    return None
DATA = os.path.join(ROOT, 'src/data/area-thoughts.json')
def main():
    """With a text file: parse + match, write src/data/area-thoughts.json (Jared's words, the source of truth) and the verify CSV.
    With --apply: write the 'ready' entries into src/data/local/<page>.json (re-runnable; reads the JSON, no PDF needed)."""
    args = [a for a in sys.argv[1:] if not a.startswith('--')]; apply = '--apply' in sys.argv
    if args:
        ents = parse(open(args[0], encoding='utf-8').read()); slugs = all_slugs(); rows = []
        for e in ents:
            tgt = target(e, slugs)
            flags = sorted({m.group(0).strip() for m in CHECK.finditer(e['text'])})
            rows.append({**e, 'page': tgt, 'status': 'verify' if flags else 'ready', 'flags': flags} if tgt else {**e, 'page': None, 'status': 'no page', 'flags': flags})
        json.dump({'source': 'Area Thoughts - Jared Gibbons (PDF, 2026-11-03)', 'entries': rows}, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        with open(os.path.join(ROOT, 'docs/review/area-thoughts-to-verify-2026-11-03.csv'), 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f); w.writerow(['area', 'city', 'page', 'status', 'flags', 'text'])
            for r in rows:
                if r['status'] != 'ready': w.writerow([r['name'], r['city'], r['page'] or '', r['status'], '; '.join(r['flags']), r['text']])
    rows = json.load(open(DATA, encoding='utf-8'))['entries']
    from collections import Counter; print(len(rows), 'entries', dict(Counter(r['status'] for r in rows)))
    if not apply: return
    by = {}
    for r in rows:
        if r['status'] == 'ready' and r['page']: by.setdefault(r['page'], []).append(r)
    for p in glob.glob(LOCAL + '/*.json'):                      # drop stale blocks first (an entry that moved or was held)
        d = json.load(open(p, encoding='utf-8'))
        if any(b.get('gen') == GEN for b in d.get('blocks', [])) and os.path.basename(p)[:-5] not in by:
            d['blocks'] = [b for b in d['blocks'] if b.get('gen') != GEN]; json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for t, es in by.items():
        p = os.path.join(LOCAL, t + '.json')
        d = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {'status': 'draft', 'slug': t, 'updated': '2026-11-03', 'blocks': [], 'faq': []}
        d['blocks'] = [b for b in d.get('blocks', []) if b.get('gen') != GEN]
        for e in es:
            d['blocks'] += [{'t': 'h', 'level': 2, 'text': f"Jared's take on {e['name']}", 'gen': GEN}, {'t': 'p', 'text': e['text'], 'gen': GEN}]
        json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('pages written', len(by))
if __name__ == '__main__': main()
