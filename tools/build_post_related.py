#!/usr/bin/env python3
"""Related posts for every blog post (D-221, Nov 11, 2026).

The Cursor audit found 174 blog posts linked only from the blog index. Each post now ends with up to five related posts, picked by
the words their titles and H1s share (place names count double), so readers move between posts on the same area or topic and every
post gets links from other posts. A post that would end up with fewer than three links in is added to its closest matches' lists.
Writes src/data/post-related.json (slug -> [slugs]); internal/blog/[slug].astro renders it. Idempotent.
python3 -I tools/build_post_related.py"""
import collections, glob, json, math, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
STOP = set('''the a an of in for and to at on with is your you this new by from what how why are it its our bc home homes real estate
sale for listing listed just sold jared gibbons now here about more most one look inside need know things buyers buyer sellers
realtor guide update market news 2023 2024 2025 2026 vs top best right'''.split())
PLACES = set('''langley surrey south white rock abbotsford chilliwack mission maple ridge pitt meadows delta ladner tsawwassen cloverdale
willoughby walnut grove brookswood murrayville aldergrove fort fleetwood clayton morgan grandview crescent beach ocean park richmond
coquitlam vancouver burnaby princeton penticton sardis yorkson campbell valley fraser'''.split())


def toks(s):
    return [t for t in re.findall(r'[a-z0-9]+', s.lower()) if t not in STOP and len(t) > 2 and not t.isdigit()]


def main():
    posts = {}
    for f in glob.glob('src/data/posts/*.json'):
        d = json.load(open(f, encoding='utf-8'))
        if not d.get('canonical'): continue
        h1 = next((b.get('text', '') for b in d.get('blocks', []) if b.get('t') == 'h' and b.get('level') == 1), '')
        posts[d['slug']] = (toks(d.get('title', '') + ' ' + h1 + ' ' + d['slug'].replace('-', ' ')), str(d.get('seo', {}).get('Published', '')))
    df = collections.Counter(t for v, _ in posts.values() for t in set(v))
    N = len(posts)
    vec = {s: {t: (2 if t in PLACES else 1) * math.log(N / df[t]) for t in set(v)} for s, (v, _) in posts.items()}
    def sim(a, b):
        A, B = vec[a], vec[b]; num = sum(A[t] * B[t] for t in A.keys() & B.keys())
        return num / (math.sqrt(sum(x * x for x in A.values())) * math.sqrt(sum(x * x for x in B.values())) or 1)
    ranked = {s: sorted((o for o in posts if o != s), key=lambda o: (-sim(s, o), o)) for s in posts}
    rel = {s: ranked[s][:4] for s in posts}
    inbound = collections.Counter(o for v in rel.values() for o in v)
    for s in sorted(posts, key=lambda s: inbound[s]):
        for o in ranked[s]:
            if inbound[s] >= 3: break
            if s not in rel[o] and len(rel[o]) < 6: rel[o].append(s); inbound[s] += 1
    json.dump(dict(sorted(rel.items())), open('src/data/post-related.json', 'w', encoding='utf-8'), indent=1)
    print('posts', len(rel), '| fewest links in', min(inbound[s] for s in posts), '| avg list', round(sum(map(len, rel.values())) / len(rel), 1))


if __name__ == '__main__': main()
