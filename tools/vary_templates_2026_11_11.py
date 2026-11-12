#!/usr/bin/env python3
"""Generated-page wording, page by page (D-227, Nov 11, 2026). Jared asked to lift the 104 pages still under 0.76 unique.

Those pages (type pages, school pages, price bands, stats) were written by generators that put each page's own numbers into the same
sentence. The numbers differ but the wording around them was identical on hundreds of pages, and that wording is what the uniqueness
check counts. This rewrites the ten most-repeated templates into three wordings each, picked per page from the page's slug (same page,
same wording every run), with the same facts and numbers. It also fixes "between November 1, 2025 to October 22, 2026", and drops the
scope question "Does this page include townhomes or duplexes?" (the H1 says houses) and the generic contact questions ("Can I book a private showing…", "Who can help me buy or sell…", "How do I find out what my home is worth?")
from a page's FAQ where it keeps 5 or more other questions (the contact box on every page says the same).
Idempotent: rewritten sentences no longer match the originals. python3 -I tools/vary_templates_2026_11_11.py"""
import glob, hashlib, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
DATES = 'November 1, 2025 to October 22, 2026'
T = {
 'sold5': (r"^(?P<n>[\d,]+) (?P<t>[a-z ]+?) sold in (?P<x>.+?) over those 5 months, out of (?P<m>[\d,]+) in all of (?P<c>.+?)\.$", [
    "{n} {t} sold in {x} over those 5 months, out of {m} in all of {c}.",
    "Between June and October 2026, {n} {t} sold in {x}; {c} as a whole recorded {m}.",
    "{x} accounted for {n} of the {m} {t} sold across {c} from June to October 2026."]),
 'incl': (r"^No\. The figures are for detached houses only\. Condos and townhomes are counted on their own page\.$", [
    "No. The figures are for detached houses only. Condos and townhomes are counted on their own page.",
    "No, only detached houses are counted here; condos and townhomes have their own page.",
    "It doesn’t. These numbers cover detached houses, and condos and townhomes are on a separate page."]),
 'price': (r"^(?P<n>[\d,]+) (?P<t>[a-z ]+?) sold in (?P<x>.+?) between November 1, 2025 to October 22, 2026, with a median price of (?P<p>\$[\d,]+)\.$", [
    "{n} {t} sold in {x} from " + DATES + ", at a median price of {p}.",
    "The median {t1} sale in {x} was {p}, across {n} sales from " + DATES + ".",
    "From November 2025 to late October 2026, {x} recorded {n} {t1} sales at a median of {p}."]),
 'dom': (r"^The median was (?P<d>\d+) days from listing to sale, and homes sold at a median (?P<r>[\d.]+)% of the last list price \((?P<a>\d+)% sold above list\), for sales November 1, 2025 to October 22, 2026\.$", [
    "The median was {d} days from listing to sale, and homes sold at a median {r}% of the last list price ({a}% sold above list), for sales " + DATES + ".",
    "Half sold in {d} days or less, at a median {r}% of the last list price; {a}% went over asking (sales from " + DATES + ").",
    "Typical time on the market was {d} days. At the median, sale prices were {r}% of list, and {a}% of sales closed above list (" + DATES + ")."]),
 'count': (r"^At the end of October 2026 the (?P<b>.+?) figures showed (?P<n>[\d,]+) (?P<t>[a-z ]+?) listed in (?P<x>.+?)\. That is a month-end count and it moves daily; ask Jared what is on the market today\.$", [
    "At the end of October 2026 the {b} figures showed {n} {t} listed in {x}. That is a month-end count and it moves daily; ask Jared what is on the market today.",
    "The {b} counted {n} {t} listed in {x} at the end of October 2026. The number changes daily, so ask Jared for today’s count.",
    "{N}, in the {b} month-end figures for October 2026. Listings change every day; Jared can tell you what is available now."]),
 'ratio': (r"^In October 2026, (?P<t>[a-z ]+?) in (?P<x>.+?) had a sales ratio of (?P<r>\d+)%, which the reports’ scale reads as (?P<art>an?) (?P<m>[a-z’ ]+?) market\. On the reports’ scale under 12% favours buyers, 12% to 20% is balanced and over 20% favours sellers\.$", [
    "In October 2026, {t} in {x} had a sales ratio of {r}%, which the reports’ scale reads as {art} {m} market. On the reports’ scale under 12% favours buyers, 12% to 20% is balanced and over 20% favours sellers.",
    "{X1} {t} sold at a sales ratio of {r}% in October 2026, {art} {m} market on the reports’ scale (under 12% favours buyers, over 20% favours sellers).",
    "With a sales ratio of {r}% in October 2026, {t} in {x} sat in {art} {m} market. The reports read under 12% as a buyers’ market and over 20% as a sellers’ market."]),
 'srch': (r"^It lists active homes whose listing text names (?P<s>.+?), so a nearby home that leaves the name out will not show\.$", [
    "It lists active homes whose listing text names {s}, so a nearby home that leaves the name out will not show.",
    "It matches the school’s name in the listing text. A home near {s} whose listing doesn’t mention it won’t appear.",
    "By name: a listing shows up when its description mentions {s}. Ask Jared to watch for nearby homes that leave the school out."]),
 'fast': (r"^Within 1 km of (?P<s>.+?) the median was (?P<d>\d+) days on the market, closing at (?P<r>[\d.]+)% of the list price, with (?P<a>\d+)% of sales above the list price for the (?P<n>[\d,]+) homes within 1 km\.$", [
    "Within 1 km of {s} the median was {d} days on the market, closing at {r}% of the list price, with {a}% of sales above the list price for the {n} homes within 1 km.",
    "For the {n} homes that sold within 1 km of {s}, the median time on the market was {d} days and the median sale was {r}% of list; {a}% sold above list.",
    "Near {s} (1 km), homes took a median {d} days to sell and closed at {r}% of the list price, with {a}% over asking, across {n} sales."]),
 'listfell': (r"^Listings of (?P<t>[a-z ]+?) in (?P<x>.+?) (?P<dir>fell|rose) from (?P<a>[\d,]+) in June to (?P<b>[\d,]+) in October \((?P<pc>[−+\-]?[\d.]+%)\), and (?P<n>[\d,]+) sold across the 5 months\. In October the community held (?P<sh>[\d.]+%) of (?P<c>.+?)’s (?P<m>[\d,]+) (?P<t2>[a-z ]+?) listed\.$", [
    "Listings of {t} in {x} {dir} from {a} in June to {b} in October ({pc}), and {n} sold across the 5 months. In October the community held {sh} of {c}’s {m} {t2} listed.",
    "{X1} went from {a} {t} listed in June to {b} in October ({pc}), with {n} sales over the 5 months. That was {sh} of the {m} {t2} listed in {c} in October.",
    "From June to October the number of {t} listed in {x} {dir} from {a} to {b} ({pc}); {n} sold in that time. In October, {x} had {sh} of {c}’s {m} listed {t2}."]),
}
T = {k: (re.compile(p), v) for k, (p, v) in T.items()}
GENERIC = re.compile(r'^(Does this page include townhomes or duplexes in .+\?|Can I book a private showing with Jared\?|How do I find out what my home is worth\?|Who can help me buy or sell in .+\?|Can Jared show me homes in .+\?|How do I find out what my home in .+ is worth\?)$')


def pick(slug, key, n=3): return int(hashlib.sha1(f'{slug}|{key}'.encode()).hexdigest(), 16) % n


def rewrite(s, slug, cnt):
    for k, (r, vs) in T.items():
        m = r.match(s)
        if not m: continue
        g = m.groupdict(); v = vs[pick(slug, k)]
        g['t1'] = ' '.join(w[:-2] if w.endswith('xes') else w[:-1] if w.endswith('s') and w != 'and' else w for w in g.get('t', '').split())   # "condos and townhomes" -> "condo and townhome"
        g['X1'] = g['x'][0].upper() + g['x'][1:] if g.get('x') else ''
        g['N'] = g.get('n', '')
        out = v.format(**g)
        if out != s: cnt[k] += 1
        return out
    return s


def walk(o, slug, cnt):
    if isinstance(o, dict): return {k: (walk(v, slug, cnt) if k not in ('h', 'href', 'id', 'gen', 'slug') else v) for k, v in o.items()}
    if isinstance(o, list): return [walk(v, slug, cnt) for v in o]
    if isinstance(o, str): return rewrite(o, slug, cnt)
    return o


def main():
    import collections
    cnt = collections.Counter(); files = 0
    for f in sorted(glob.glob('src/data/local/*.json')):
        raw = open(f, encoding='utf-8').read(); slug = os.path.basename(f)[:-5]
        d = json.loads(raw); before = json.dumps(d, ensure_ascii=False, sort_keys=True)
        d = walk(d, slug, cnt)
        fq = d.get('faq')
        if isinstance(fq, list):
            gen = [q for q in fq if GENERIC.match(q.get('q', ''))]
            if gen and len(fq) - len(gen) >= 5: d['faq'] = [q for q in fq if not GENERIC.match(q.get('q', ''))]; cnt['generic contact FAQ removed'] += len(gen)
        if json.dumps(d, ensure_ascii=False, sort_keys=True) == before: continue
        ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
        open(f, 'w', encoding='utf-8').write((json.dumps(d, ensure_ascii=False, indent=ind) if ind else json.dumps(d, ensure_ascii=False, separators=(',', ':'))) + ('\n' if raw.endswith('\n') else ''))
        files += 1
    print('files', files, dict(cnt))


if __name__ == '__main__': main()
