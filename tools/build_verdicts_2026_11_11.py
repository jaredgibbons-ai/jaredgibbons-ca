#!/usr/bin/env python3
"""Jared's verdicts on every guide, and the Nov 11 approvals (D-215).

Jared, Nov 11, on the list sent that morning: "Yes go ahead with 3, 4, 2 and 1. Use yours". That approves:
  1. the verdict sheet (docs/review/verdicts-for-jared-2026-11-11.csv, Drive: "For Jared: guide verdicts to approve"): 118 guides,
     each verdict his own Nov 9 words put together ("<Area> suits <who it suits>. <his catch line>"). The seven areas with no catch
     line get one taken from his own "what I'd tell a friend" text (CATCH below), as the sheet offered ("use yours").
  2. the Port Kells verdict as drafted.
  3. the Murrayville and Milner verdicts as drafted.
  4. launch approval for the five new guides and the eight rewritten city rules pages.
A guide that has no guide-format v2 entry gets a light one (verdict only), which shows the "Quick answer" box with Jared's verdict
at the top of the guide; works/doesn't, fit questions and drive times come later. Idempotent.
python3 -I tools/build_verdicts_2026_11_11.py"""
import csv, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
DATE = '2026-11-11'
CATCH = {   # from his own words in src/data/jared-voice.json ("friend")
    'Aberdeen': 'Out on a rural road, expect more driving and more upkeep.',
    'Bolivar Heights': 'A great view can come with less flat, usable yard than you’d think.',
    'Chilliwack Proper South': 'Check which way a unit faces: two units in the same building can feel completely different with the windows open.',
    'Hemlock Valley': 'The catch is getting up there on a snowy Friday night.',
    'Holly': 'The trade-off is driving into the village more often.',
    'Nordel': 'Right on Nordel Way it’s busy, so look a few turns off it.',
    'Port Guichon': '“Waterfront” can mean very different properties here, so check what the listing means.',
}
PORT_KELLS = 'Pick Port Kells for a business that runs on Highway 1. Look elsewhere if you want a regular neighbourhood with listings to choose from.'
NEW = ['rosemary-heights-guide', 'yorkson-langley-guide', 'auguston-abbotsford-guide', 'milner-langley-guide', 'port-kells-surrey-guide'] + \
      [f'{c}-home-buying-rules' for c in ('surrey', 'langley', 'delta', 'pitt-meadows', 'maple-ridge', 'abbotsford', 'chilliwack', 'cultus-lake')]


def main():
    p = 'src/data/guide-plus.json'; gp = json.load(open(p, encoding='utf-8'))
    gp['port-kells-surrey-guide']['verdict'] = PORT_KELLS
    for k, v in gp.items():
        if isinstance(v, dict) and k in ('murrayville-guide', 'milner-langley-guide', 'port-kells-surrey-guide'): v['status'] = 'approved'
    slug_of = {}
    for s in os.listdir('src/data/local'): slug_of[s[:-5]] = True
    rows = list(csv.DictReader(open('docs/review/verdicts-for-jared-2026-11-11.csv', encoding='utf-8')))
    n = 0
    for r in rows:
        slug = r['Page (preview)'].rsplit('/', 1)[1][:-5]
        verdict = (r['Your edit (leave blank if the draft is fine)'] or r['Draft verdict (your words put together)']).strip()
        if r['Area'] in CATCH: verdict = verdict.rstrip() + ' ' + CATCH[r['Area']]
        cur = gp.get(slug)
        if cur and not cur.get('lite'): continue      # a full v2 entry keeps its own verdict
        gp[slug] = {'status': 'approved', 'lite': True, 'name': r['Area'], 'sub': None, 'summary': None, 'verdict': verdict, 'vibe': None,
                    'commute': None, 'works': [], 'doesnt': [], 'fit': [], 'faq': [], 'video': None}
        n += 1
    open(p, 'w', encoding='utf-8').write(json.dumps(gp, ensure_ascii=False, indent=1) + '\n')
    a = json.load(open('docs/review/launch/approvals.json', encoding='utf-8'))
    a['later'] = [x for x in a.get('later', []) if x.get('date') != DATE or 'D-215' not in x.get('what', '')]
    a['later'].append({'date': DATE, 'what': 'Five new guides (Rosemary Heights, Yorkson, Auguston, Milner, Port Kells) and the eight rewritten city rules pages (D-215)', 'slugs': NEW})
    open('docs/review/launch/approvals.json', 'w', encoding='utf-8').write(json.dumps(a, ensure_ascii=False, indent=1) + '\n')
    print('verdicts added:', n, '| approved pages:', len(NEW))


if __name__ == '__main__': main()
