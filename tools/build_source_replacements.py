#!/usr/bin/env python3
"""Sources on other agents' sites -> developer, government or plain-text sources (D-204, Nov 10, 2026).

About 1,050 source links pointed at other real estate agents' and listing portals' pages (bccondosandhomes.com building pages,
Mike Stewart and other presale pages, homehappy.ca, danmarusin.com ...). They are swapped at render time by SourceList.astro from
src/data/source-replacements.json, so every layer (local notes, presale data, regenerated pages) is covered without rewriting 900 files:
  - government replacements for the general pages (BC first-time buyers' program, property transfer tax, manufactured homes);
  - presale and project pages -> the developer's own website, where the developer is on record (src/data/presale, the presale master
    list, or "by <developer>" in the page address) and the developer's site was opened and checked in Chrome on Nov 10, 2026;
    a developer project page already on record for that project wins over the home page;
  - building-directory pages (bccondosandhomes.com) -> one plain line saying the building facts come from MLS® listing records and
    strata directory entries (no link: those records are not public pages);
  - index and search pages on those sites (area lists, tag pages) -> dropped;
  - anything left -> a plain line naming the project and saying the details come from the developer's sales materials.
Re-run after new research adds sources. python3 -I tools/build_source_replacements.py"""
import csv, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
OUT = 'src/data/source-replacements.json'
AGENTS = r'bccondosandhomes\.com|mikestewart\.ca|homehappy\.ca|danmarusin\.com|vancouvernewcondos\.com|livabl\.com|rew\.ca|presalesbc\.com|bentruscottrealestate\.com|rennie\.com|zolo\.ca'
AG = re.compile(AGENTS, re.I)
SECONDARY = re.compile(AGENTS + r'|presale|carrietsang|realty|realtor|lumon\.com|nestpresales|strawhomes|youlive|goodmanreport|tmbrealestate|storeys\.com|bchomeworld|mdre\.ca|staging\.', re.I)
CHECKED = 'checked November 1, 2026'
PROJECT = 'Presale details: the developers’ own sales materials.'
BUILDING = 'Building facts: MLS® listing records and strata directories.'   # short on purpose: one line repeated on 300 pages must not add shared wording
GOV = {
    'homehappy.ca/bc-first-time-buyer-programs': [{'t': 'gov.bc.ca · First time home buyers’ program', 'h': 'https://www2.gov.bc.ca/gov/content/taxes/property-taxes/property-transfer-tax/exemptions/first-time-home-buyers'}],
    'danmarusin.com/blog/bc-property-transfer-tax-2026': [{'t': 'gov.bc.ca · Property transfer tax', 'h': 'https://www2.gov.bc.ca/gov/content/taxes/property-taxes/property-transfer-tax'}],
    'bentruscottrealestate.com/manufactured-homes.html': [{'t': 'gov.bc.ca · Manufactured or mobile homes', 'h': 'https://www2.gov.bc.ca/gov/content/housing-tenancy/owning-a-home/manufactured-home-registry'}],
}
# developer websites opened in Chrome on Nov 10, 2026 (host as served, name)
DEV = [l.split('|') for l in '''allureventures.ca|Allure Ventures
aquilinidevelopment.com|Aquilini Development
www.beedie.ca|Beedie
bosaproperties.com|Bosa Properties
centurygroup.ca|Century Group
www.concordpacific.com|Concord Pacific
conwest.com|Conwest
cressey.com|Cressey Development Group
davadevelopments.com|Dava Developments
www.dawsonsawyer.ca|Dawson + Sawyer
www.diverseproperties.com|Diverse Properties
domushomes.ca|Domus Homes
www.enrichdevelopments.com|Enrich Developments
anthemproperties.com|Anthem Properties
apcongroup.ca|Apcon Group
executivegroupdevelopment.com|Executive Group Development
fabricliving.ca|Fabric Living
www.forge.ca|Forge Properties
formwerks.ca|Formwerks
genaris.ca|Genaris Properties
www.gryphonliving.com|Gryphon Development
heinrichsdevelopments.com|Heinrichs Developments
holborn.ca|Holborn
hudsonprojects.ca|Hudson Projects
infinityproperties.ca|Infinity Properties
intergulf.com|Intergulf Development
www.landaglobal.com|Landa Global Properties
marcon.ca|Marcon
mosaichomes.com|Mosaic Homes
www.novaraproperties.com|Novara Properties
onni.com|Onni Group
parkridgehomes.ca|Park Ridge Homes
polyhomes.com|Polygon Homes
primaproperties.ca|Prima Properties
quadrahomes.com|Quadra Homes
www.qualex.ca|Qualex-Landmark
www.raicon.ca|Raicon Developments
redekopfaye.com|Redekop Faye
shape.ca|Shape Properties
www.streetsidedevelopments.com|StreetSide Developments
townline.com|Townline
vestaproperties.com|Vesta Properties
wesgroup.ca|Wesgroup Properties
www.wesmont.com|Wesmont
zenterra.ca|Zenterra Developments
caliberprojects.com|Caliber Projects
www.threeshores.ca|Three Shores Development'''.splitlines()]
KEY = {'beedie': 'Beedie', 'dawson': 'Dawson + Sawyer', 'shape': 'Shape Properties', 'qualex': 'Qualex-Landmark', 'redekop': 'Redekop Faye', 'streetside': 'StreetSide Developments',
       'three shores': 'Three Shores Development', 'park ridge': 'Park Ridge Homes', 'polygon': 'Polygon Homes', 'cressey': 'Cressey Development Group', 'executive group': 'Executive Group Development'}


def norm(u): return re.sub(r'^https?://(www\.|embed\.)?', '', u.strip()).split('#')[0].rstrip('/').lower()


def dev_site(raw):
    r = (raw or '').lower()
    for k, name in KEY.items():
        if k in r: return next(d for d in DEV if d[1] == name)
    for host, name in DEV:
        first = name.lower().split()[0]
        if len(first) > 3 and re.search(r'\b' + re.escape(first) + r'\b', r): return [host, name]
    return None


def main():
    proj = {}   # normalized URL -> (project name, developer)
    for pr in json.load(open('src/data/presale/2026-11-01.json'))['projects']:
        good = [s for s in pr.get('sources', []) if not SECONDARY.search(s)]
        for s in pr.get('sources', []): proj.setdefault(norm(s), (pr['name'], pr.get('developer') or '', good))
    for r in csv.DictReader(open('docs/research/presale-master-list-2026-11-01.csv')):
        ss = [s for s in re.split(r'[;\s|]+', r['Source URLs']) if s.startswith('http')]
        good = [s for s in ss if not SECONDARY.search(s)]
        for s in ss: proj.setdefault(norm(s), (r['Project name'], r['Developer'] or '', good))
    urls = set()
    for base, _, files in os.walk('src/data'):
        for f in files:
            if f.endswith('.json'):
                for m in re.finditer(r'https?://[^\s"\'<>]+', open(os.path.join(base, f), encoding='utf-8').read()):
                    if AG.search(m.group(0)): urls.add(norm(m.group(0)))
    out = {}; stats = {}
    def put(u, kind, v): out[u] = v; stats[kind] = stats.get(kind, 0) + 1
    for u in sorted(urls):
        if u in GOV: put(u, 'government page', {'items': GOV[u]}); continue
        if 'bccondosandhomes.com' in u: put(u, 'building records line', {'text': BUILDING}); continue
        if re.search(r'rew\.ca/(buildings|developments)/(areas|search)|/zones/|/local/|/tag/|livabl\.com/[a-z-]+-bc$|livabl\.com/articles/\?p=|mikestewart\.ca/\?p=|presalesbc\.com|zolo\.ca|rennie\.com|mikestewart\.ca/presale$', u):
            put(u, 'index page dropped', {'drop': True}); continue
        name, dev, good = proj.get(u, ('', '', []))
        if not dev:
            m = re.search(r'-by-(?:the-)?([a-z0-9-]+)', u.split('/')[-1]); dev = m.group(1).replace('-', ' ') if m else ''
        if good:
            put(u, 'project page on record', {'items': [{'t': norm(g).split('/')[0], 'h': g} for g in good[:2]]}); continue
        site = dev_site(dev) if dev else None
        if site:
            put(u, 'developer website', {'items': [{'t': f'{site[0]} · {site[1]} (developer’s website)', 'h': f'https://{site[0]}/'}]}); continue
        put(u, 'plain project line', {'text': PROJECT})
    json.dump(dict(sorted(out.items())), open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); open(OUT, 'a').write('\n')
    print(len(out), 'URLs mapped:', stats)


if __name__ == '__main__': main()
