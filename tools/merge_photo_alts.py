"""Photo descriptions for the listing galleries (D-250). Written by looking at each photo (numbered contact sheets, in the
order of src/data/listing-photos/*.json, first appearance of each photo id). Input: a folder of "N|description" text files
and the order file the sheets were made from. Output: src/data/photo-alts.json {photo id: description}.
    python3 -I tools/merge_photo_alts.py <alts folder> <photo_order.json>"""
import glob, json, os, re, sys
d, order_f = sys.argv[1], sys.argv[2]
order = json.load(open(order_f))['order']
out = {}
for f in sorted(glob.glob(os.path.join(d, 'p*.txt'))):
    for line in open(f, encoding='utf-8'):
        m = re.match(r'^(\d+)\|(.+)$', line.strip())
        if not m: continue
        n, t = int(m.group(1)), m.group(2).strip()
        if 1 <= n <= len(order) and t: out[order[n - 1]] = t
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json.dump(dict(sorted(out.items())), open(os.path.join(root, 'src/data/photo-alts.json'), 'w'), ensure_ascii=False, indent=0)
print(len(out), 'of', len(order), 'photos described')
