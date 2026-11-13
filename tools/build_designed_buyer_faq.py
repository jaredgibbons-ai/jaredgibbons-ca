#!/usr/bin/env python3
"""FAQ for Home Buyers in BC as a designed page (D-266).

Reads the archive record src/data/pages/faq-for-home-buyers-in-bc.json (wording kept as archived; fragments that the capture split
mid-sentence are re-joined) and writes src/data/designed/faq-for-home-buyers-in-bc.json: one section per archive category, each an
accordion of questions with multi-paragraph answers and bullet lists, plus key numbers, a contents bar and a call-to-action.
    python3 -I tools/build_designed_buyer_faq.py
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'src/data/pages/faq-for-home-buyers-in-bc.json'
OUT = ROOT / 'src/data/designed/faq-for-home-buyers-in-bc.json'
CATS = {'The Offer & Subjects': 'offer', 'Money & Financing': 'money', 'Closing & Costs': 'closing', 'Taxes': 'taxes', 'Working With a REALTOR®': 'realtor'}

def txt(b):
    return ' '.join(p['t'] for p in b.get('parts', [])).strip()

def local(h):
    return re.sub(r'^https://jaredgibbons\.ca(?=/)', '', h)

def parts(b):
    return [{'t': p['t'], **({'h': local(p['h'])} if p.get('h') else {})} for p in b.get('parts', [])]


# Answers the capture flattened beyond repair by rule: same wording, laid out by hand.
def T(t, h=None, lead=False):
    d = {'t': t}
    if h: d['h'] = h
    if lead: d['lead'] = True
    return d
FIX = {
 'What is a subject?': [
  {'p': [T('Subjects are conditions in a purchase contract that must be met before the deal becomes firm. They exist to protect the buyer and allow time for due diligence. Common subjects include:')]},
  {'li': [[T('Subject to financing', lead=True), T('— confirming your mortgage is approved')], [T('Subject to inspection', lead=True), T('— having the home professionally inspected')],
          [T('Subject to property disclosure statement', lead=True), T("— reviewing the seller's disclosures")], [T('Subject to title search', lead=True), T('— verifying clear title')],
          [T('Subject to strata documents', lead=True), T('— reviewing strata minutes, financials, bylaws,'), T('depreciation report', '/blog.html/depreciation-reports-explained-what-every-strata-corporation-should-kn-8243026'), T(', and insurance')]]},
  {'p': [T('Subjects are completed during the subject removal period, which is the window of time you have to satisfy or waive each condition.')]}],
 'How much money do I need for a down payment?': [
  {'p': [T('The minimum down payment rules in Canada are:')]},
  {'li': [[T('$500,000 or less:', lead=True), T('5% minimum down payment')], [T('$500,001 to $1,499,999:', lead=True), T('5% on the first $500K + 10% on the balance')], [T('$1,500,000 or more:', lead=True), T('20% minimum down payment')]]},
  {'p': [T('For example, on a $750,000 home: 5% of $500K ($25,000) + 10% of $250K ($25,000) ='), T('$50,000 minimum', lead=True), T('.')]},
  'KEEP-LAST'],
 'Are there programs to help first-time home buyers?': 'SPLIT-TAIL',
 'What is the completion date, possession date, and adjustment date?': [
  {'p': [T('These are three key dates at the end of a real estate transaction:')]},
  {'li': [[T('Completion date:', lead=True), T('the day the purchase money is paid and the buyer gains title to the home')], [T('Possession date:', lead=True), T('the day you get the keys and can move in')],
          [T('Adjustment date:', lead=True), T('the day calculations for property taxes, utility accounts, rents, and strata fees are prorated between buyer and seller')]]},
  {'p': [T('In the Fraser Valley and Greater Vancouver, the possession and adjustment dates are typically the same day, with completion happening at least one day earlier.')]}],
 'What kind of closing costs should I expect?': [
  {'p': [T('Closing costs are the fees beyond your down payment that are due at completion. Common ones include:')]},
  {'li': [[T('Property transfer tax', lead=True), T('(unless exempt)')], [T('GST', lead=True), T('on new builds (5% of the purchase price)')], [T('Legal/notary fees')], [T('Property tax and utility adjustments')],
          [T('Strata maintenance fee adjustments (for strata properties)')], [T('Title insurance')], [T('Home insurance (required by your lender)')]]},
  'KEEP-LAST-2'],
 'How long does it take from accepted offer to closing?': [
  {'p': [T("There's no standard timeline — it depends on the situation and is negotiated between buyer and seller. That said,"), T('2–3 months', lead=True), T('from accepted offer to completion is common.')]},
  {'p': [T('Some factors that affect timing:')]},
  {'li': [[T("Vacant homes often close faster (the seller doesn't need to find somewhere to go)")], [T('Sellers who are also buying may want to align their completion dates')],
          [T('Tenanted properties require proper notice under BC tenancy rules')], [T('Pre-sale/new builds can have much longer timelines (1–3+ years)')]]},
  {'p': [T("I've seen deals close in as little as 2 weeks and as long as 9 months — it all depends on the circumstances.")]}],
 'Do I have to pay property transfer tax and how much is it?': [
  {'p': [T("Property transfer tax (PTT) is a BC provincial tax paid by the buyer at completion. It is not something you can blend into your mortgage — you'll need the funds available. The rates are:")]},
  {'li': [[T('1%', lead=True), T('on the first $200,000')], [T('2%', lead=True), T('on the portion from $200,001 to $2,000,000')], [T('3%', lead=True), T('on the portion above $2,000,000')], [T('An additional'), T('2%', lead=True), T('on residential property above $3,000,000')]]},
  'PTT-TAIL'],
}

ENDS = re.compile(r'[.!?:)]\s*$|→$')

def main():
    B = json.loads(SRC.read_text())['blocks']
    cats, cur, q = [], None, None
    i = 5
    while i < len(B):
        b = B[i]; t = txt(b)
        if b['t'] == 'p' and t in CATS:
            cur = {'id': CATS[t], 'title': t, 'items': []}; cats.append(cur); i += 1; continue
        if t.startswith('Have a question that'):
            break
        if b['t'] == 'p' and t.endswith('?') and len(b['parts']) == 1 and len(t) < 110:
            q = {'q': t, 'body': []}; cur['items'].append(q); i += 1; continue
        if b['t'] == 'list':
            q['body'].append({'li': [[{'t': ' '.join(x['t'] for x in it).replace(' (for strata properties)', ' (for strata properties)')}] for it in b['items']]})
            i += 1; continue
        q['body'].append({'p': parts(b)}); i += 1
    # re-join fragments: a paragraph that does not end a sentence continues into the next one
    for c in cats:
        for it in c['items']:
            out = []
            for x in it['body']:
                if 'p' in x and out and 'p' in out[-1] and not ENDS.search(' '.join(p['t'] for p in out[-1]['p'])):
                    out[-1]['p'] += x['p']
                else:
                    out.append(x)
            # a paragraph that carries "Label: value" or "Label — value" pairs (the capture flattened lists) is split into intro, items, tail
            def islabel(ps, k):
                t = ps[k]['t'].strip()
                if ps[k].get('h') or len(t) > 60: return False
                nxt = ps[k + 1]['t'].strip() if k + 1 < len(ps) else ''
                return (t.endswith(':') and len(t) < 45) or nxt.startswith('—')
            split = []
            for x in out:
                if 'p' not in x: split.append(x); continue
                ps = x['p']; labs = [k for k in range(len(ps)) if islabel(ps, k)]
                if len(labs) < 2 and not (len(labs) == 1 and labs[0] == 0 and len(ps) == 2):
                    split.append(x); continue
                if labs[0] > 0: split.append({'p': ps[:labs[0]]})
                items = []
                for j, k in enumerate(labs):
                    end = labs[j + 1] if j + 1 < len(labs) else len(ps)
                    seg = ps[k:end]
                    # a sentence after the last value ("For example ...", "An additional ...") is its own paragraph
                    tail = next((m for m in range(1, len(seg)) if re.match(r'^(For example|An additional|In the|Some factors)', seg[m]['t'])), None)
                    items.append([dict(seg[0], lead=True)] + seg[1:tail])
                    if tail is not None: split.append({'li': items}); items = []; split.append({'p': seg[tail:]})
                if items: split.append({'li': items})
            out = split
            # short "Label — text" paragraphs in a row are a bullet list
            res = []
            for x in out:
                isb = 'p' in x and len(x['p']) >= 2 and re.match(r'^[—:]|^\(', x['p'][1]['t'].strip()) is not None and len(x['p'][0]['t']) < 60
                isb = isb or ('p' in x and len(x['p']) >= 2 and x['p'][0]['t'].rstrip().endswith(':') and len(x['p'][0]['t']) < 40)
                if isb:
                    item = [dict(x['p'][0], lead=True)] + x['p'][1:]
                    if res and 'li' in res[-1] and res[-1].get('auto'): res[-1]['li'].append(item)
                    else: res.append({'li': [item], 'auto': True})
                else:
                    res.append(x)
            for x in res: x.pop('auto', None)
            it['a'] = res; del it['body']
            f = FIX.get(it['q'])
            if f == 'SPLIT-TAIL':   # the last list item swallowed the closing paragraph
                last = it['a'][-1]['li'][-1]; k = next(i for i, p in enumerate(last) if p['t'].startswith('These programs'))
                it['a'][-1]['li'][-1] = last[:k]; it['a'].append({'p': last[k:]})
            elif f:
                flat = [p for x in res if 'p' in x for p in x['p']]
                new = []
                for x in f:
                    if x == 'KEEP-LAST': new.append(res[-1])
                    elif x == 'KEEP-LAST-2': new += res[-2:]
                    elif x == 'PTT-TAIL':
                        k = next(i for i, p in enumerate(flat) if p['t'].startswith('First-time home buyers may qualify'))
                        new.append({'p': flat[k:]})
                    else: new.append(x)
                it['a'] = new
            # the archive's own wording, checked: every sentence of the answer is still in it
            got = ' '.join(p['t'] for x in it['a'] for p in (x.get('p') or [q for li in x.get('li', []) for q in li]))
            norm = lambda z: re.sub(r'[^a-z0-9$%]+', '', z.lower())
            src = norm(' '.join(txt(b) if b['t'] != 'list' else ' '.join(' '.join(y['t'] for y in li) for li in b['items']) for b in B))
            assert norm(got) and all(norm(w) in src for w in re.split(r'(?<=[.!?])\s+', got) if len(norm(w)) > 8), it['q']
    n = sum(len(c['items']) for c in cats)
    sections = [{'id': 'numbers', 'label': 'At a glance', 'h2': 'The numbers buyers ask about most', 'blocks': [{'type': 'tiles', 'items': [
        {'k': '5%', 't': 'Minimum down payment', 'd': 'On homes up to $500,000; 10% on the portion above, 20% from $1.5M'},
        {'k': '7 days', 't': 'Typical subject period', 'd': 'Often 5 business days plus the weekend; negotiable'},
        {'k': '1.5–4%', 't': 'Closing costs', 'd': 'Of the price, on top of your down payment'},
        {'k': '0.25%', 't': 'Rescission penalty', 'd': 'To walk away in the 3-business-day cooling-off period'},
    ]}]}]
    roman = ['I', 'II', 'III', 'IV', 'V']
    for k, c in enumerate(cats):
        sections.append({'id': c['id'], 'label': f"{roman[k]} · {len(c['items'])} questions", 'h2': c['title'], 'blocks': [{'type': 'faq', 'open': True, 'items': c['items']}]})
    sections.append({'id': 'more', 'label': 'Keep reading', 'h2': 'More for BC buyers', 'blocks': [{'type': 'cards', 'cols': 3, 'items': [
        {'n': '01', 't': 'First-time buyer FAQ', 'd': '12 more questions for your first purchase.', 'cta': 'Read it →', 'href': '/blog.html/first-time-buyer-faq-12-real-estate-questions-answered-8707214'},
        {'n': '02', 't': 'GST rebate in BC', 'd': 'The FTHB rebate on new homes, explained.', 'cta': 'Read it →', 'href': '/gst-rebate-in-bc.html'},
        {'n': '03', 't': 'The buying guide', 'd': 'How buying a home works, step by step.', 'cta': 'Read it →', 'href': '/buying.html'},
    ]}]})
    d = {
        'kind': 'faq', 'slug': 'faq-for-home-buyers-in-bc', 'crumb': 'Buyer FAQ',
        'nav': [{'label': 'At a glance', 'href': '#numbers'}] + [{'label': c['title'].replace('Working With a REALTOR®', 'Your REALTOR®'), 'href': '#' + c['id']} for c in cats],
        'hero': {
            'eyebrow': "Buyer's guide · British Columbia",
            'h1': 'FAQ for Home Buyers in BC',
            'tag': f'{n} questions answered · Updated 2026',
            'lead': 'Subjects and deposits, down payments, closing costs, taxes and what your REALTOR® does. Straight answers from Jared Gibbons, REALTOR®. Not covered here? Call or text 604-928-1361.',
            'ctas': [{'label': 'Call or text 604-928-1361', 'href': 'tel:+16049281361', 'primary': True}, {'label': 'Search homes', 'href': '/map-search.html'}],
            'image': {'src': '/img/selling/selling-03-kitchen', 'w': 1600, 'h': 1066, 'alt': 'Bright kitchen with an island in a Fraser Valley home'},
            'stats': [{'k': str(n), 'v': 'buyer questions answered'}, {'k': '11+ years', 'v': 'helping Fraser Valley buyers'}, {'k': 'Top 1%', 'v': 'of Fraser Valley REALTORS®'}],
        },
        'sections': sections,
        'close': {'label': 'Still have a question?', 'h2': 'Ask me directly', 'd': "Whether you're buying your first home or your fifth, I'm happy to help.", 'ctas': [{'label': 'Call 604-928-1361', 'href': 'tel:+16049281361'}, {'label': 'Email me', 'href': 'mailto:jaredgibbons@royallepage.ca'}]},
    }
    OUT.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
    print(n, 'questions in', len(cats), 'sections')
    for c in cats:
        for it in c['items']: print(' ', c['id'], '|', it['q'], '|', len(it['a']), 'blocks')

if __name__ == '__main__':
    main()
