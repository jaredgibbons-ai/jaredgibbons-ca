"""D-230: source links on the local layers. SUPERSEDED, DO NOT RE-RUN: dropping the items lost D-204's render-time swaps
(developer and government replacements); the drop was undone the same evening. Kept for the record.

Labels ("tol.ca · about the township.aspx" → "Township of Langley: About the Township") are made at render time by
Rich.astro with lib/sources.ts; relabel() here is kept for reference and not called.
Other agents' and listing portals' sites. Building facts were cross-checked on other REALTORS® and
   portals' pages; a link from Jared's site sends visitors and link equity to them. Source-list items that
   only point there are dropped (the "Building facts: MLS® listing records…" line already credits the
   records), and inline links to them keep their words but lose the link.

    python3 -I tools/polish_source_links_2026_11_11.py [--dry]
"""
import json, glob, re, sys, collections
from urllib.parse import urlparse, unquote

DRY = '--dry' in sys.argv

AGENT_HOSTS = {
 'bccondosandhomes.com', 'mikestewart.ca', 'danmarusin.com', 'homehappy.ca', 'condosurrey.com',
 'vancouvernewcondos.com', 'vancouverhomesearch.com', 'realestatenorthshore.com', 'tmbrealestate.com', 'faithwilson.com',
 'jimpilkington.com', 'murphyrealestategroup.ca', 'bentruscottrealestate.com', 'michaellepore.ca', 'rew.ca', 'zillow.com',
 'zumper.com', 'kijiji.ca', 'condos.ca', 'realestatevalley.ca', 'tomhassan.com', 'jasonhutchison.ca', 'eugenek.ca',
 'mattgul.com', 'coreyzach.com', 'chrisbrownrealestate.ca', 'balancerealestategroup.com', 'blurealty.com',
 'bernadettedunnigan.com', 'bryanvanhoepen.com', 'dorsetrealty.com', 'coronetrealty.ca', 'markdrelich.com',
 'merylhamdillah.com', 'michaeltudorie.com', 'placerealestate.ca', 'rodrhearyan.com', 'snapuprealestate.ca',
 'stanleylamprec.com', 'the-a-team.ca', 'thebrandrealestategroup.com', 'tetrarealty.ca', 'westeringhteam.ca',
 'vancity-realestate.com', 'vancouversold.com', 'realestatevancity.ca', 'thatagentkelly.substack.com',
 'jamiemacdougall.com', 'themacnabs.com', 'skytraincondo.ca', 'presalehomes.ca', 'nestpresales.com', 'presalesbc.com',
 'vancouverpresaleprojects.com', 'rennie.com', 'mynextcondo.com', 'listedbuy.com', 's.realtyninja.com',
 'vancouverrealestatepodcast.com', 'activerain.com', 'liv.rent', 'apartmenthomeliving.com', 'mybcrental.com',
 'rentboard.ca', 'urbanyvr.com', 'livabl.com', 'condotrend.com', 'burnabyhouse.com', 'inthehood.ca',
 'properties.lefigaro.com', 'commercialsearch.com', 'images1.cityfeet.com', 'images1.showcase.com',
 'images.loopnet.ca', 'images.loopnet.fr', 'nexthome.ca',
}

AGENT_HOSTS |= set(json.load(open('src/data/other-agent-domains.json'))['domains']) - {'realtor.ca'}

ORG = {
 'www2.gov.bc.ca': 'Province of BC', 'gov.bc.ca': 'Province of BC', 'news.gov.bc.ca': 'BC Gov News', 'archive.news.gov.bc.ca': 'BC Gov News',
 'bclaws.gov.bc.ca': 'BC Laws', 'studentsuccess.gov.bc.ca': 'BC Student Success', 'alc.gov.bc.ca': 'Agricultural Land Commission',
 'connect.health.gov.bc.ca': 'BC Ministry of Health', 'surreylangleyskytrain.gov.bc.ca': 'Surrey Langley SkyTrain',
 'infomaps.translink.ca': 'TransLink', 'translink.ca': 'TransLink', 'buzzer.translink.ca': 'TransLink Buzzer', 'maps.translink.ca': 'TransLink',
 'bctransit.com': 'BC Transit', 'surrey.ca': 'City of Surrey', 'burnaby.ca': 'City of Burnaby', 'city.burnaby.bc.ca': 'City of Burnaby',
 'bylaws.burnaby.ca': 'City of Burnaby', 'mapleridge.ca': 'City of Maple Ridge', 'engage.mapleridge.ca': 'City of Maple Ridge',
 'canada.ca': 'Government of Canada', 'coquitlam.ca': 'City of Coquitlam', 'publicdocs.coquitlam.ca': 'City of Coquitlam',
 'delta.ca': 'City of Delta', 'maps.delta.ca': 'City of Delta', 'letstalk.delta.ca': 'City of Delta', 'delta.civicweb.net': 'City of Delta council',
 'hdp-ca-prod-app-delta-letstalk-files.s3.ca-central-1.amazonaws.com': 'City of Delta',
 'fraserhealth.ca': 'Fraser Health', 'abbotsford.ca': 'City of Abbotsford', 'laws.abbotsford.ca': 'City of Abbotsford bylaws',
 'abbotsford.civicweb.net': 'City of Abbotsford council', 'letstalkabbotsford.ca': 'City of Abbotsford',
 'tol.ca': 'Township of Langley', 'e-connect.tol.ca': 'Township of Langley', 'facilities.tol.ca': 'Township of Langley',
 'newwestcity.ca': 'City of New Westminster', 'vancouver.ca': 'City of Vancouver', 'bylaws.vancouver.ca': 'City of Vancouver bylaws',
 'covapp.vancouver.ca': 'City of Vancouver', 'app.vancouver.ca': 'City of Vancouver', 'guidelines.vancouver.ca': 'City of Vancouver',
 'council.vancouver.ca': 'Vancouver City Council', 'opendata.vancouver.ca': 'City of Vancouver open data',
 'pittmeadows.ca': 'City of Pitt Meadows', 'mission.ca': 'City of Mission', 'engage.mission.ca': 'City of Mission',
 'portcoquitlam.ca': 'City of Port Coquitlam', 'westvancouver.ca': 'District of West Vancouver', 'portmoody.ca': 'City of Port Moody',
 'engage.portmoody.ca': 'City of Port Moody', 'chilliwack.com': 'City of Chilliwack', 'chilliwack.ca': 'City of Chilliwack',
 'fvrd.ca': 'Fraser Valley Regional District', 'haveyoursay.fvrd.ca': 'Fraser Valley Regional District',
 'fvrl.bc.ca': 'Fraser Valley Regional Library', 'bcrea.bc.ca': 'BCREA', 'metrovancouver.org': 'Metro Vancouver',
 'saveonfoods.com': 'Save-On-Foods', 'cmhc-schl.gc.ca': 'CMHC', 'richmond.ca': 'City of Richmond', 'citycouncil.richmond.ca': 'Richmond City Council',
 'docs.dnv.org': 'District of North Vancouver', 'dnv.org': 'District of North Vancouver', 'app.dnv.org': 'District of North Vancouver',
 'geoweb.dnv.org': 'District of North Vancouver', 'councilarchive.dnv.org': 'District of North Vancouver council',
 'vsb.bc.ca': 'Vancouver School Board', 'sd42.ca': 'School District 42', 'sd33.bc.ca': 'School District 33', 'sd35.bc.ca': 'School District 35',
 'sd38.bc.ca': 'Richmond School District', 'sd43.bc.ca': 'School District 43', 'sd78.bc.ca': 'School District 78', 'sd44.ca': 'North Vancouver School District',
 'deltasd.bc.ca': 'Delta School District', 'surreyschools.ca': 'Surrey Schools', 'burnabyschools.ca': 'Burnaby Schools',
 'abbyschools.ca': 'Abbotsford School District', 'westvancouverschools.ca': 'West Vancouver Schools', 'newwestschools.ca': 'New Westminster Schools',
 'langleycity.ca': 'City of Langley', 'cnv.org': 'City of North Vancouver', 'nvrc.ca': 'North Vancouver Recreation & Culture',
 'shoppersdrugmart.ca': 'Shoppers Drug Mart', 'walmart.ca': 'Walmart', 'realcanadiansuperstore.ca': 'Real Canadian Superstore',
 'safeway.ca': 'Safeway', 'thriftyfoods.com': 'Thrifty Foods', 'pharmasave.com': 'Pharmasave', 'pagesarchive.blackpress.ca': 'Black Press archive',
 'paxlaw.ca': 'Pax Law', 'equitylawgroup.ca': 'Equity Law Group', 'northam-law.com': 'Northam Law', 'bcparks.ca': 'BC Parks',
 'bchousing.org': 'BC Housing', 'learningondemand.bchousing.org': 'BC Housing', 'bchydro.com': 'BC Hydro', 'bcfsa.ca': 'BC Financial Services Authority',
 'info.bcassessment.ca': 'BC Assessment', 'bcassessment.ca': 'BC Assessment', 'vch.ca': 'Vancouver Coastal Health',
 'www12.statcan.gc.ca': 'Statistics Canada', 'commons.wikimedia.org': 'Wikimedia Commons', 'creativecommons.org': 'Creative Commons',
 'en.wikipedia.org': 'Wikipedia', 'surreylibraries.ca': 'Surrey Libraries', 'vpl.ca': 'Vancouver Public Library', 'coqlibrary.ca': 'Coquitlam Public Library',
 'nvdpl.ca': 'North Vancouver District Public Library', 'nwpl.ca': 'New Westminster Public Library', 'bpl.bc.ca': 'Burnaby Public Library',
 'yourlibrary.ca': 'Fraser Valley Regional Library', 'search.heritageburnaby.ca': 'Heritage Burnaby', 'chf.bc.ca': 'Co-op Housing Federation of BC',
 'chartwell.com': 'Chartwell', 'amica.ca': 'Amica', 'onni.com': 'Onni', 'polyhomes.com': 'Polygon Homes', 'cressey.com': 'Cressey',
 'yourvoice.burnaby.ca': 'City of Burnaby', 'pub-burnaby.escribemeetings.com': 'City of Burnaby council', 'pub-fvrd.escribemeetings.com': 'FVRD board',
 'kentbc.ca': 'District of Kent', 'harrisonhotsprings.ca': 'Village of Harrison Hot Springs', 'whiterockcity.ca': 'City of White Rock',
 'cultuslake.bc.ca': 'Cultus Lake Park', 'news.fvreb.bc.ca': 'Fraser Valley Real Estate Board', 'fvreb.bc.ca': 'Fraser Valley Real Estate Board',
 'goodmanreport.com': 'Goodman Report', 'storeys.com': 'STOREYS', 'homecalc.ca': 'HomeCalc', 'jaredgibbons.ca': 'Jared Gibbons',
 'bccourts.ca': 'BC Courts', 'ltsa.ca': 'LTSA', 'ltpm.ltsa.ca': 'LTSA', 'portvancouver.com': 'Port of Vancouver', 'pc.gc.ca': 'Parks Canada',
 'parks.canada.ca': 'Parks Canada', 'historicplaces.ca': 'Canada’s Historic Places', 'seniorsadvocatebc.ca': 'Office of the Seniors Advocate BC',
 'ic10.esolg.ca': 'District of Mission', 'lilwat.ca': 'Lil’wat Nation', 'kiwanisnorthshorehousing.org': 'Kiwanis North Shore Housing',
 'providencehealthcare.org': 'Providence Health Care', 'firerescue.richmond.ca': 'Richmond Fire-Rescue', 'cms.richmond.ca': 'City of Richmond',
}
for h in list(ORG):
    pass
SCHOOL_SUB = re.compile(r'^[a-z0-9-]+\.(abbyschools\.ca|sd33\.bc\.ca|sd35\.bc\.ca|sd38\.bc\.ca|sd42\.ca|sd44\.ca|deltasd\.bc\.ca|burnabyschools\.ca)$')
ESCRIBE = re.compile(r'^pub-([a-z]+)\.escribemeetings\.com$')

JUNK_PAGE = re.compile(r'^(default|index|home|searchresults(\.form)?|search|page|location|store|articles|facilities|en|view|details?|file|download|content|item|\d+|[a-f0-9-]{16,})(\s*\(\d+\))?$', re.I)
EXT = re.compile(r'\.(aspx?|pdf|html?|php|form|jsp|cfm)\b', re.I)

def host_of(url):
    h = (urlparse(url).hostname or '').lower()
    return h[4:] if h.startswith('www.') and h != 'www.gov.bc.ca' and not h.startswith('www2') else h

def org(h):
    if h in ORG: return ORG[h]
    m = SCHOOL_SUB.match(h)
    if m: return ORG.get(m.group(1), h)
    m = ESCRIBE.match(h)
    if m: return None
    return None

def tidy_page(pg):
    suffix = ''
    m = re.search(r'\s*\((\d+)\)$', pg)
    if m: suffix, pg = f' ({m.group(1)})', pg[:m.start()]
    pdf = bool(re.search(r'\.pdf\b', pg, re.I))
    pg = EXT.sub('', pg).replace('_', ' ').replace('+', ' ')
    pg = re.sub(r'\s+', ' ', pg).strip(' .-·')
    if not pg or JUNK_PAGE.match(pg): return None, pdf, suffix
    m = re.fullmatch(r'tt(\d+)', pg, re.I)
    if m: return 'bus timetable', True, suffix
    if pg.islower(): pg = pg[0].upper() + pg[1:]
    return pg, pdf, suffix

LABEL = re.compile(r'^([\w.-]+\.[a-z]{2,}(?::\d+)?) · (.+)$')
stats = collections.Counter()

def relabel(part):
    t, url = part.get('t'), part.get('h')
    m = LABEL.match(t or '')
    if not (m and isinstance(url, str)): return
    o = org(host_of(url))
    if not o: return
    pg, pdf, suffix = tidy_page(m.group(2))
    new = f'{o}: {pg}' if pg else o
    if pdf and not new.endswith('(PDF)'): new += ' (PDF)'
    new += suffix
    if new != t: part['t'] = new; stats['relabelled'] += 1

def is_agent(url):
    return isinstance(url, str) and host_of(url) in AGENT_HOSTS

def process(o):
    if isinstance(o, dict):
        if o.get('t') == 'list' and isinstance(o.get('items'), list):
            keep = []
            for it in o['items']:
                parts = it if isinstance(it, list) else [it]
                links = [p for p in parts if isinstance(p, dict) and 'h' in p]
                if links and all(is_agent(p['h']) for p in links) and all((not isinstance(p, dict)) or 'h' in p or not p.get('t', '').strip(' ·,;') for p in parts):
                    stats['source items dropped'] += 1; continue
                keep.append(it)
            o['items'] = keep
        if 'h' in o and is_agent(o.get('h')) and isinstance(o.get('t'), str):
            del o['h']; stats['inline links unlinked'] += 1
        for v in o.values(): process(v)
    elif isinstance(o, list):
        for v in o: process(v)

def drop_empty_lists(bl):
    # a source list emptied by the drop takes its lead-in paragraph with it only when that lead-in is the generic one
    out = []
    for b in bl:
        if isinstance(b, dict) and b.get('t') == 'list' and isinstance(b.get('items'), list) and not b['items']:
            stats['empty lists removed'] += 1; continue
        out.append(b)
    return out

files = 0
for p in sorted(glob.glob('src/data/local/*.json')):
    raw = open(p).read(); d = json.loads(raw); before = json.dumps(d, ensure_ascii=False)
    IND = len(re.match(r'\{\n( *)', raw).group(1)) if raw.startswith('{\n') else None
    process(d)
    if isinstance(d.get('blocks'), list): d['blocks'] = drop_empty_lists(d['blocks'])
    if json.dumps(d, ensure_ascii=False) != before:
        files += 1
        if not DRY: open(p, 'w').write(json.dumps(d, ensure_ascii=False, indent=IND) + ('\n' if raw.endswith('\n') else ''))
print('files', files, dict(stats))
