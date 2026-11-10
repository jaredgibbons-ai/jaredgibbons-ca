// Turns the research layer's source links ("surrey.ca · sunnyside park") into a publisher name, a readable title and a type tag.
// Pure functions, no network: titles come from the link text and the URL path, publishers from the map below (host fallback otherwise).
const PUB: Record<string, string> = {
  'www2.gov.bc.ca': 'Province of BC', 'gov.bc.ca': 'Province of BC', 'news.gov.bc.ca': 'BC Government News', 'archive.news.gov.bc.ca': 'BC Government News', 'bclaws.gov.bc.ca': 'BC Laws',
  'studentsuccess.gov.bc.ca': 'BC Ministry of Education and Child Care', 'alc.gov.bc.ca': 'Agricultural Land Commission', 'surreylangleyskytrain.gov.bc.ca': 'Surrey Langley SkyTrain Project',
  'infomaps.translink.ca': 'TransLink', 'translink.ca': 'TransLink', 'buzzer.translink.ca': 'TransLink Buzzer', 'maps.translink.ca': 'TransLink', 'bctransit.com': 'BC Transit',
  'surrey.ca': 'City of Surrey', 'surreyschools.ca': 'Surrey School District', 'surreylibraries.ca': 'Surrey Libraries', 'mapleridge.ca': 'City of Maple Ridge', 'engage.mapleridge.ca': 'City of Maple Ridge',
  'burnaby.ca': 'City of Burnaby', 'city.burnaby.bc.ca': 'City of Burnaby', 'yourvoice.burnaby.ca': 'City of Burnaby', 'pub-burnaby.escribemeetings.com': 'City of Burnaby council', 'burnabyschools.ca': 'Burnaby School District',
  'coquitlam.ca': 'City of Coquitlam', 'coqlibrary.ca': 'Coquitlam Public Library', 'portcoquitlam.ca': 'City of Port Coquitlam', 'portmoody.ca': 'City of Port Moody', 'engage.portmoody.ca': 'City of Port Moody',
  'delta.ca': 'City of Delta', 'maps.delta.ca': 'City of Delta', 'letstalk.delta.ca': 'City of Delta', 'delta.civicweb.net': 'City of Delta council', 'deltasd.bc.ca': 'Delta School District',
  'hdp-ca-prod-app-delta-letstalk-files.s3.ca-central-1.amazonaws.com': 'City of Delta', 'tol.ca': 'Township of Langley', 'langleycity.ca': 'City of Langley',
  'abbotsford.ca': 'City of Abbotsford', 'laws.abbotsford.ca': 'City of Abbotsford bylaws', 'abbotsford.civicweb.net': 'City of Abbotsford council', 'letstalkabbotsford.ca': 'City of Abbotsford', 'abbyschools.ca': 'Abbotsford School District',
  'mission.ca': 'District of Mission', 'chilliwack.com': 'City of Chilliwack', 'pittmeadows.ca': 'City of Pitt Meadows', 'richmond.ca': 'City of Richmond', 'citycouncil.richmond.ca': 'City of Richmond council',
  'newwestcity.ca': 'City of New Westminster', 'newwestschools.ca': 'New Westminster Schools', 'vancouver.ca': 'City of Vancouver', 'bylaws.vancouver.ca': 'City of Vancouver bylaws', 'covapp.vancouver.ca': 'City of Vancouver',
  'app.vancouver.ca': 'City of Vancouver', 'opendata.vancouver.ca': 'City of Vancouver Open Data', 'guidelines.vancouver.ca': 'City of Vancouver', 'vsb.bc.ca': 'Vancouver School Board', 'vpl.ca': 'Vancouver Public Library',
  'westvancouver.ca': 'District of West Vancouver', 'westvancouverschools.ca': 'West Vancouver Schools', 'cnv.org': 'City of North Vancouver', 'docs.dnv.org': 'District of North Vancouver', 'geoweb.dnv.org': 'District of North Vancouver',
  'nvrc.ca': 'North Vancouver Recreation and Culture', 'sd42.ca': 'Maple Ridge–Pitt Meadows Schools (SD 42)', 'sd33.bc.ca': 'Chilliwack Schools (SD 33)', 'sd35.bc.ca': 'Langley Schools (SD 35)', 'sd38.bc.ca': 'Richmond Schools (SD 38)',
  'sd43.bc.ca': 'Coquitlam Schools (SD 43)', 'sd78.bc.ca': 'Fraser-Cascade Schools (SD 78)', 'fvrd.ca': 'Fraser Valley Regional District', 'haveyoursay.fvrd.ca': 'Fraser Valley Regional District', 'pub-fvrd.escribemeetings.com': 'Fraser Valley Regional District',
  'fvrl.bc.ca': 'Fraser Valley Regional Library', 'metrovancouver.org': 'Metro Vancouver', 'cultuslake.bc.ca': 'Cultus Lake Park Board', 'kentbc.ca': 'District of Kent', 'bcparks.ca': 'BC Parks',
  'fraserhealth.ca': 'Fraser Health', 'vch.ca': 'Vancouver Coastal Health', 'canada.ca': 'Government of Canada', 'cmhc-schl.gc.ca': 'CMHC', 'www12.statcan.gc.ca': 'Statistics Canada', 'statcan.gc.ca': 'Statistics Canada',
  'info.bcassessment.ca': 'BC Assessment', 'bcassessment.ca': 'BC Assessment', 'bcrea.bc.ca': 'BC Real Estate Association', 'bcfsa.ca': 'BC Financial Services Authority', 'fvreb.bc.ca': 'Fraser Valley Real Estate Board', 'news.fvreb.bc.ca': 'Fraser Valley Real Estate Board',
  'cadreb.com': 'Chilliwack and District Real Estate Board', 'chf.bc.ca': 'Co-operative Housing Federation of BC', 'jaredgibbons.ca': 'Jared Gibbons', 'pagesarchive.blackpress.ca': 'Black Press archive',
  'paxlaw.ca': 'Pax Law', 'equitylawgroup.ca': 'Equity Law Group', 'homehappy.ca': 'HomeHappy', 'homecalc.ca': 'HomeCalc', 'danmarusin.com': 'Dan Marusin', 'mikestewart.ca': 'Mike Stewart', 'mybaragar.com': 'Baragar Systems',
  'bccondosandhomes.com': 'BC Condos & Homes', 'vancouvernewcondos.com': 'Vancouver New Condos', 'polyhomes.com': 'Polygon Homes', 'onni.com': 'Onni', 'saveonfoods.com': 'Save-On-Foods', 'safeway.ca': 'Safeway', 'walmart.ca': 'Walmart',
  'shoppersdrugmart.ca': 'Shoppers Drug Mart', 'thriftyfoods.com': 'Thrifty Foods', 'realcanadiansuperstore.ca': 'Real Canadian Superstore', 'heritageburnaby.ca': 'Heritage Burnaby', 'search.heritageburnaby.ca': 'Heritage Burnaby',
  'tsawwassensprings.ca': 'Tsawwassen Springs',
};
const ACR = new Set(['ocp', 'bc', 'pdf', 'alr', 'gst', 'hst', 'ptt', 'nvrc', 'fvrd', 'fvreb', 'cmhc', 'tod', 'toa', 'sd', 'ssmuh', 'rs', 'rt', 'rm', 'cd', 'ra', 'rf', 'lu', 'ocp,', 'faq', 'faqs', 'bcfsa', 'fcl', 'rcmp', 'bcaa', 'ubc', 'sfu', 'ii', 'iii', 'iv', 'ib', 'pyp', 'ssp', 'ltcap', 'tfn', 'icbc', 'id', 'xv', 'wr']);
const GENERIC = /^(document|page|store|details|redirect|information|info|view|show|index|default|home|main|content|detail|display|item|file|filestream|download|ashx|aspx)$/i;
const host = (u: string) => { try { return new URL(u).hostname.replace(/^www\./i, '').toLowerCase(); } catch { return ''; } };
export const publisher = (url: string): string => { const h = host(url); return PUB[h] || PUB[h.replace(/^[^.]+\./, '')] || h; };
const smart = (s: string) => s.split(' ').map((w, i) => { const lw = w.toLowerCase(); if (ACR.has(lw)) return lw.toUpperCase(); if (/^\d/.test(w) || /[A-Z]/.test(w.slice(1))) return w; if (i > 0 && /^(of|the|and|for|to|in|on|a|an|at|by|vs)$/.test(lw)) return lw; return lw.charAt(0).toUpperCase() + lw.slice(1); }).join(' ');
const clean = (s: string) => s.replace(/\.(aspx?|pdf|html?|php|ashx|pptx?|docx?)\b/gi, ' ').replace(/[_+]+/g, ' ').replace(/\s*-\s*/g, ' ').replace(/%20/g, ' ').replace(/\s+/g, ' ').trim();
// Titles for sources whose file names read badly as titles ("News122 Excise…", "OCP 2024 web", "Node", "96448 01"); matched on part of the URL.
const TITLE_BY_URL: [string, string][] = [
  ['news122/news122-excise', 'Excise and GST/HST News No. 122'], ['OCP_2024_web.pdf', 'Official Community Plan (2024)'],
  ['pittmeadows.ca/ocp', 'Official Community Plan'], ['Park%20Amenities.pdf', 'Park amenities list'], ['ZBA%5F5000', 'Zoning Bylaw No. 5000 (2020)'],
  ['2020-07-28-zoning-bylaw-7600', 'Zoning Bylaw No. 7600-2019'], ['statreg/96448_01', 'Taxation (Rural Area) Act'], ['statreg/98043', 'Strata Property Act'],
  ['crbc/481_2003', 'Manufactured Home Park Tenancy Regulation'], ['search.heritageburnaby.ca/list', 'Heritage Burnaby landmark search'],
  ['dp-pd/prof/index.cfm', 'Census Profile, 2021 Census'], ['geoweb.dnv.org/data', 'GeoWeb open data'], ['area-neighbourhood-plans/town', 'Town Centre Area Plan'],
  ['area-neighbourhood-plans-0', 'Hammond Area Plan'], ['Tax%5FRates%5Ffor%5Fthe%5FWeb', 'Property tax rates'], ['2026%20Tax%20Rates%20Bylaw', '2026 Tax Rates Bylaw No. 3727-2026'],
  ['service-improvements-in-chilliwack-and-agassiz-harrison', 'Service improvements in Chilliwack and Agassiz-Harrison (December 2025)'],
  ['pitt-meadows_business-plan_2020', 'Pitt Meadows Business Plan 2020'], ['haveyoursay.fvrd.ca/cultus-lake', 'Cultus Lake engagement: questions and answers'],
  ['chw_rg_jan2024', 'Chilliwack transit rider guide (January 2024)'], ['Notice-of-Election-by-Voting', 'Notice of election by voting'], ['2020%20McKee%20Profile', 'McKee neighbourhood profile (2020)'],
  ['FAQ_-_Small-Scale_Housing', 'Small-scale housing: questions and answers (July 2025)'], ['Historic%20Downtown%20Neighbourhood%20Plan', 'Historic Downtown Neighbourhood Plan event boards'],
  ['General%20Guide%20to%20Subdivision', 'General guide to the subdivision process'], ['DP2%5FGuide', 'Development permit area 2 guide (March 2026)'],
];
export function sourceInfo(text: string, url: string) {
  const h = host(url);
  const fixed = TITLE_BY_URL.find(([k]) => url.includes(k));
  if (fixed) return { pub: publisher(url), title: fixed[1], kind: /\.pdf($|\?)/i.test(url) ? 'PDF' : 'Web page', host: h };
  let t = text.replace(/^Source:\s*/i, '').replace(/\s*\(\d{1,2}\)\s*$/, '').trim();   // the notes numbered repeat links: 'chilliwack.com (2)'
  const parts = t.split(' · ');
  let title = parts.length > 1 ? parts.slice(1).join(' · ').trim() : (t.toLowerCase().replace(/^www\./, '') === h ? '' : t);
  title = clean(title);
  const m = /^tt(\w+)$/i.exec(title);
  if (/translink\.ca$/.test(h) && m) title = `Route ${m[1]} timetable`;
  if (!title || GENERIC.test(title) || /^[a-z]\d{3,}[a-z]?$/i.test(title) && !m) {
    let seg = '';
    try { const p = new URL(url).pathname.split('/').filter(Boolean); seg = decodeURIComponent(p[p.length - 1] || ''); } catch { /* keep empty */ }
    seg = clean(seg);
    title = seg && !GENERIC.test(seg) && !/^\d+$/.test(seg) ? seg : /civicweb|escribe/.test(h) ? 'Council document' : /\.pdf($|\?)/i.test(url) ? 'Official document' : 'Official page';
  }
  // Some source labels were cut at about 48 characters in the notes ("... Official Community Plan New Westmi"). When the address ends in the full wording, use that.
  if (title && !GENERIC.test(title)) {
    let seg = '';
    try { const p = new URL(url).pathname.split('/').filter(Boolean); seg = clean(decodeURIComponent(p[p.length - 1] || '')).replace(/\s\d{1,3}$/, ''); } catch { /* keep the label */ }
    const norm = (x: string) => x.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
    const nt = norm(title), ns = norm(seg);
    if (nt.length >= 8 && ns.length > nt.length && ns.startsWith(nt)) title = seg;
  }
  title = title.replace(/\s*\([^)]*$/, '').trim();   // a label cut inside a bracket ("... as of June 30 2022 (Co")
  title = title.replace(/\s+(?:pdf|web(?: full\d*)?|final)$/i, '').trim();   // file-name tails: "… PDF", "… web", "… Final"
  const zone = /maps\.delta\.ca\/Utilities\/ZoningPDF\/([A-Z0-9-]+)\.pdf/i.exec(url), route = /Route_Diagrams\/\d+\/r(\d+)\.pdf/i.exec(url);
  if (zone) title = `Zoning Bylaw: ${zone[1].toUpperCase()} zone`;
  else if (route) title = `Route ${route[1]} map`;
  else if (/^OCP$/i.test(title)) title = 'Official Community Plan';
  else if (/^FAQS?$/i.test(title)) title = 'Questions and answers';
  if (/^[\d\s_]+$/.test(title) || /^(node|list|data|prof|park|town|term|york|atms|\d+\.aspx)$/i.test(title))
    title = /bclaws/.test(h) ? 'BC law or regulation' : /\.pdf($|\?)/i.test(url) ? 'Official document' : 'Official page';
  if (title === title.toLowerCase() || title === title.toUpperCase()) title = smart(title);
  // spelling slips in publishers' own file names and in the notes' labels
  title = title.replace(/\bMillenium\b/g, 'Millennium').replace(/\bOakrige\b/g, 'Oakridge').replace(/\bCarraige\b/g, 'Carriage').replace(/\bTsawassen\b/g, 'Tsawwassen')
    .replace(/\bWhats Happening\b/g, "What's Happening").replace(/\bGuidlines\b/g, 'Guidelines').replace(/\bCommunitiy\b/g, 'Community').replace(/\bBulding\b/g, 'Building')
    .replace(/\bAbbottsford\b/g, 'Abbotsford').replace(/\b([Aa])ssigment\b/g, '$1ssignment');
  if (title.length > 90) title = title.slice(0, 88).replace(/\s+\S*$/, '') + '…';
  const kind = /\.pdf($|\?)/i.test(url) ? 'PDF' : /\.(xlsx?|csv)($|\?)/i.test(url) ? 'Spreadsheet' : /\.pptx?($|\?)/i.test(url) ? 'Slides' : 'Web page';
  return { pub: publisher(url), title, kind, host: h };
}
export const isSourcesHeading = (t: string) => /^sources?\b/i.test(String(t).trim());
