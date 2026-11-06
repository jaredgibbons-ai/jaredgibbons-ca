#!/usr/bin/env python3
"""Builds src/data/designed/buying.json from the archived page record (src/data/pages/buying.json).
The archive flattened the designed "Buy better" page into plain text; this puts every block back into its section with the same wording.
Text is copied by block index, not retyped. Run: python3 tools/build_designed_buying.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(f'{ROOT}/src/data/pages/buying.json'))
B = d['blocks']
H = 'https://jaredgibbons.ca'
def parts(i):
    ps = [{k: (v.replace(H, '') if k == 'h' else v) for k, v in x.items() if k != 'lead'} for x in B[i]['parts']]
    # the archive dropped the space on either side of an inline link ("older homes,acreages, and"): put it back
    for a, b in zip(ps, ps[1:]):
        if 'h' not in a and 'h' in b and a['t'] and not a['t'].endswith((' ', '(', '—', '→')): a['t'] += ' '
        if 'h' in a and 'h' not in b and b['t'] and b['t'][0].isalnum(): b['t'] = ' ' + b['t']
    return ps
def S(i):
    b = B[i]
    if b['t'] == 'p': return ''.join(x['t'] for x in b['parts']).strip()
    if b['t'] == 'h': return b['text']
    if b['t'] == 'list': return ' '.join(x['t'] for it in b['items'] for x in it)
    raise SystemExit(f'block {i}: {b["t"]}')
def R(i):
    ps = parts(i)
    return ps[0]['t'] if len(ps) == 1 and 'h' not in ps[0] else ps
def L(i): return [''.join(x['t'] for x in it).strip() for it in B[i]['items']]
def link(i): return [(''.join(x['t'] for x in it), (it[0].get('h') or '').replace(H, '')) for it in B[i]['items']]
def card(i):
    c = B[i]; ln = [x['text'] for x in c['lines']]
    return {'n': ln[0], 't': ln[1], 'd': ln[2], 'cta': ln[3], 'href': c['href'].replace(H, '')}

nav = [{'label': 'Which buyer', 'href': '#which-buyer'}] + [{'label': t, 'href': h.replace('/buying.html', '')} for t, h in link(1) if h]
ctas = link(6)
tiers = [
    {'n': '01', 'range': parts(35)[0]['t'], 'what': parts(35)[1]['t'], 'result': L(36)[0]},
    {'n': '02', 'range': L(36)[2], 'what': S(37), 'result': L(38)[0]},
    {'n': '03', 'range': L(38)[2], 'what': S(39), 'result': S(40)},
    {'n': '04', 'range': parts(42)[0]['t'], 'what': parts(42)[1]['t'], 'result': L(43)[0]},
    {'n': '+', 'range': L(43)[2], 'what': S(44), 'result': S(45)},
]
est = L(83)
steps = []
for a, extra in [(56, 59), (60, None), (63, 66), (67, None), (70, None), (73, None), (76, None)]:
    s = {'n': S(a), 't': S(a + 1), 'd': S(a + 2)}
    if extra: s['do'] = parts(extra)[1]['t']
    steps.append(s)
costs = []
for name_i, desc, amt in [(None, 91, 92), (93, 94, 95), (96, 97, 98), (99, 100, 101), (102, 103, 104), (105, 106, 107), (108, 109, 110), (111, 112, 113)]:
    name = L(90)[3] if name_i is None else S(name_i)
    costs.append({'t': name, 'd': R(desc), 'v': S(amt)})
costs.append({'t': S(114), 'd': [{'t': S(115) + ' '}] + parts(116), 'v': S(117)})
strata = [
    {'t': S(122), 'd': S(123)}, {'t': S(124), 'd': S(125)},
    {'t': S(126), 'd': S(127), 'src': S(128)},
    {'t': S(129), 'd': S(130), 'src': 'Source: Act s.59 · Reg s.4.4'},
    {'t': L(132)[2], 'd': S(133)},
    {'t': S(134), 'd': S(135)},
    {'t': S(136), 'd': S(137), 'src': S(138)}, {'t': S(139), 'd': S(140), 'src': S(141)},
    {'t': S(142), 'd': S(143)},
    {'t': S(144), 'd': S(145), 'src': S(146)}, {'t': S(147), 'd': S(148), 'src': S(149)},
]
why = [{'n': S(a), 't': S(a + 1), 'd': S(a + 2)} for a in (155, 158, 161, 164)]
rv = parts(177)
quotes = [
    {'q': S(171), 'who': S(172), 'date': S(173), 'src': S(170).replace('★★★★★ ', '')},
    {'q': S(175), 'who': S(176), 'date': rv[0]['t'].strip(), 'src': S(174).replace('★★★★★ ', '')},
]
faq = [{'q': S(i), 'a': R(i + 1)} for i in range(205, 221, 2)]
out = {
    'kind': 'buying', 'slug': 'buying',
    'nav': nav,
    'hero': {'eyebrow': L(1)[-1], 'h1': S(2), 'tag': S(3), 'updated': S(4), 'lead': S(5),
             'ctas': [{'label': ctas[0][0], 'href': ctas[0][1], 'primary': True}, {'label': ctas[1][0], 'href': ctas[1][1]}],
             'stats': [{'k': L(6)[2], 'v': L(6)[3]}, {'k': L(6)[4], 'v': L(6)[5]}, {'k': L(6)[6], 'v': L(6)[7]}, {'k': L(6)[8], 'v': L(6)[9]}]},
    'sections': [
        {'id': 'realtor', 'label': L(6)[10], 'h2': S(7), 'lead': S(8), 'intro': S(9), 'blocks': [
            {'type': 'tiles', 'items': [{'k': S(10), 't': S(11), 'd': S(12)}, {'k': S(13), 't': S(14), 'd': S(15)}, {'k': S(16), 't': S(17), 'd': S(18)}]}]},
        {'id': 'which-buyer', 'label': S(19), 'h2': S(20), 'lead': S(21), 'intro': S(22), 'blocks': [{'type': 'cards', 'cols': 2, 'items': [card(i) for i in range(23, 27)]}]},
        {'id': 'ptt-exemption', 'label': S(27), 'h2': S(28), 'lead': S(29), 'intro': S(30), 'blocks': [
            {'type': 'stat', 'label': S(31), 'k': S(32), 'd': S(33), 'link': {'label': link(34)[0][0], 'href': link(34)[0][1]}},
            {'type': 'tiers', 'head': ['Tier', 'Price', 'What happens', 'Result'], 'rows': tiers},
            {'type': 'note', 'd': S(46)},
            {'type': 'band', 'lead': S(47).split('→')[0].strip() + ' →', 'btn': {'label': parts(47)[1]['t'], 'href': parts(47)[1]['h']}, 'alt': {'label': S(48), 'href': parts(48)[0]['h']}},
            {'type': 'fine', 'a': parts(49), 'b': S(50), 'c': parts(51)}]},
        {'id': 'process', 'label': S(52), 'h2': S(53), 'lead': S(54), 'intro': S(55), 'blocks': [{'type': 'steps', 'items': steps}]},
        {'id': 'calculator', 'label': S(79), 'h2': S(80), 'lead': S(81), 'intro': S(82), 'blocks': [
            {'type': 'estimate', 'rows': [[est[i], est[i + 1]] for i in range(4, 14, 2)], 'result': est[14], 'head': [est[0], est[1]], 'note': R(84), 'fine': S(85)}]},
        {'id': 'closing-costs', 'label': S(86), 'h2': S(87), 'lead': S(88), 'intro': S(89), 'blocks': [
            {'type': 'costs', 'head': L(90)[:3], 'rows': costs}, {'type': 'note', 'd': S(118)}]},
        {'id': 'strata-checklist', 'label': S(119), 'h2': S(120), 'intro': S(121), 'blocks': [{'type': 'checks', 'items': strata}, {'type': 'fine', 'a': S(150)}]},
        {'id': 'why', 'label': S(151), 'h2': S(152), 'lead': S(153), 'intro': S(154), 'blocks': [{'type': 'tiles', 'items': [{'k': w['n'], 't': w['t'], 'd': w['d']} for w in why]}]},
        {'id': 'reviews', 'label': S(167), 'h2': S(168), 'intro': R(169), 'blocks': [{'type': 'quotes', 'items': quotes, 'more': {'label': rv[1]['t'], 'href': rv[1]['h'].replace(H, '')}}]},
        {'id': 'regions', 'label': S(178), 'h2': S(179), 'lead': S(180), 'intro': [{'t': S(181) + ' '}, parts(182)[0], {'t': ' ' + parts(182)[1]['t']}], 'blocks': [{'type': 'cards', 'cols': 4, 'items': [card(i) for i in range(183, 191)]}]},
        {'id': 'library', 'label': S(191), 'h2': S(192), 'lead': S(193), 'intro': S(194), 'blocks': [{'type': 'cards', 'cols': 3, 'items': [card(i) for i in range(195, 201)]}]},
        {'id': 'faq', 'label': S(201), 'h2': S(202), 'lead': S(203), 'intro': R(204), 'blocks': [{'type': 'faq', 'items': faq}]},
    ],
    'close': {'label': S(221), 'h2': S(222), 'd': S(223), 'ctas': [{'label': t, 'href': h} for t, h in link(224)], 'foot': [parts(225)[1]['t'], S(226).lstrip('· ')], 'email': parts(225)[1]['h'].replace('mailto:', '')},
}
os.makedirs(f'{ROOT}/src/data/designed', exist_ok=True)
json.dump(out, open(f'{ROOT}/src/data/designed/buying.json', 'w'), ensure_ascii=False, indent=1)
print('ok', len(json.dumps(out)))
