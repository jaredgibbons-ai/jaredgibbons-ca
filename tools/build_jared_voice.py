"""Jared's take on each neighbourhood guide (D-198) -> src/data/jared-voice.json {guide-slug: {name, suits, friend, tip, more?}}.

Sources (both Jared's own words, collected 2026-11-09):
  docs/research/jared-voice/core-tidied.json    the 19 core guides, tidied from his chat answers (facts checked; see area-notes)
  docs/research/jared-voice/area-notes-*.md      batches 1-5, his written answers, used verbatim apart from the EDITS below
EDITS holds the only changes made to his written answers: a claim that could not be confirmed is dropped, a typo is fixed.
Rendered by GenericPage.astro as a card right under the guide's quick-facts box. Where an older "Jared's take on X" block (gen 'jtake',
tools/build_area_thoughts.py) sits on the same guide, its heading becomes "More from Jared on X" so the page has one "Jared's take".
python3 -I tools/build_jared_voice.py"""
import glob, json, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DOCS = os.path.join(ROOT, 'docs/research/jared-voice')
OUT = os.path.join(ROOT, 'src/data/jared-voice.json')
BATCH = {
 '1': 'whalley fleetwood-tynehead sullivan-station guildford west-newton east-newton queen-mary-park-surrey - central-abbotsford abbotsford-east abbotsford-west mission-bc-mission east-central-maple-ridge west-central-maple-ridge cottonwood-maple-ridge sardis-south promontory chilliwack-proper-east garrison-crossing chilliwack-proper-south',
 '2': 'sunnyside-park-surrey fraser-heights bear-creek-green-timbers panorama-ridge cedar-hills bolivar-heights nordel scottsdale sunshine-hills-woods annieville tsawwassen-north albion southwest-maple-ridge silver-valley central-meadows-pitt-meadows chilliwack-proper-west sardis-west-vedder sardis-east-vedder vedder-crossing eastern-hillsides',
 '3': 'hawthorne neilsen-grove delta-manor ladner-elementary holly tsawwassen-central beach-grove cliff-drive boundary-beach poplar aberdeen mid-meadows-pitt-meadows south-meadows-pitt-meadows northwest-maple-ridge websters-corners hatzic-mission mission-west-mission fairfield-island chilliwack-mountain chilliwack-downtown',
 '4': 'otter-district county-line-glen-valley royal-heights bridgeview tsawwassen-east english-bluff bradner north-meadows-pitt-meadows thornhill-maple-ridge dewdney-deroche-mission lake-errock-mission stave-falls-mission little-mountain lower-landing east-chilliwack rosedale greendale ryder-lake yarrow columbia-valley',
 '5': 'serpentine east-delta ladner-rural westham-island port-guichon west-meadows-pitt-meadows north-maple-ridge northeast-maple-ridge whonnock durieu-mission steelhead-mission hemlock-valley-mission matsqui sumas-mountain sumas-prairie west-chilliwack majuba-hill vedder-mountain river-valley cultus-lake popkum bridal-falls'}
EDITS = {  # (field, old, new): the only changes to his written answers
 'hemlock-valley-mission-guide': [('friend', 'The upper section of Hemlock Valley Road is unpaved, and a drive up', 'A drive up')],   # road surface not confirmed
 'county-line-glen-valley-guide': [('friend', 'Glenn Valley', 'Glen Valley')],
 'neilsen-grove-guide': [('tip', ' And if you’re writing the guide, the school is spelled Neilson Grove Elementary, while the real estate area is Neilsen Grove.', '')],  # a note to me, not copy
}


def batches():
    t = open(sorted(glob.glob(os.path.join(DOCS, 'area-notes-*.md')))[-1], encoding='utf-8').read()
    out = {}
    for n, txt in re.findall(r'# Batch (\d).*?```text\n(.*?)\n```', t, re.S):
        ents = [e for e in re.split(r'\n(?=\d+\. )', txt) if re.match(r'\d+\. ', e)]
        slugs = BATCH[n].split(); assert len(ents) == len(slugs), (n, len(ents), len(slugs))
        for e, s in zip(ents, slugs):
            if s == '-' or 'Who it suits' not in e: continue          # skipped by Jared, or a note
            g = lambda lbl: (re.search(lbl + r'[.:]\s*(.*?)\s*(?=\n\S|$)', e, re.S) or [None, ''])[1].strip()
            name = re.sub(r',.*$', '', e.split('\n', 1)[0].split('. ', 1)[1]).strip()
            out[s + '-guide'] = {'name': name, 'suits': g('Who it suits'), 'friend': g('What I’d tell a friend'), 'tip': g('My tip')}
    return out


def main():
    data = batches() | json.load(open(os.path.join(DOCS, 'core-tidied.json'), encoding='utf-8'))
    for slug, eds in EDITS.items():
        for k, a, b in eds:
            assert a in data[slug][k], (slug, a); data[slug][k] = data[slug][k].replace(a, b).strip()
    for slug, v in data.items():
        assert os.path.exists(os.path.join(ROOT, 'src/data/pages', slug + '.json')) or \
            'new_page' in json.load(open(os.path.join(ROOT, 'src/data/local', slug + '.json'), encoding='utf-8')), slug   # archive guide or a new local guide (D-203)
        for k in ('suits', 'friend'): assert v.get(k), (slug, k)
        for k in ('suits', 'friend', 'tip'):
            if v.get(k): v[k] = re.sub(r'\s+', ' ', v[k].replace("'", '’')).strip()
        for m in v.get('more', []):
            for k in ('friend', 'tip'):
                if m.get(k): m[k] = m[k].replace("'", '’')
    json.dump(dict(sorted(data.items())), open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); open(OUT, 'a').write('\n')
    renamed = 0                                                       # one "Jared's take" per guide
    for slug in data:
        p = os.path.join(ROOT, 'src/data/local', slug + '.json')
        if not os.path.exists(p): continue
        d = json.load(open(p, encoding='utf-8')); hit = False
        for b in d.get('blocks', []):
            if b.get('gen') == 'jtake' and b.get('t') == 'h' and b['text'].startswith("Jared's take on "):
                b['text'] = 'More from Jared on ' + b['text'][len("Jared's take on "):]; hit = True
        if hit: json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); renamed += 1
    print('guides with Jared’s take:', len(data), '| older jtake headings renamed:', renamed)


if __name__ == '__main__': main()
