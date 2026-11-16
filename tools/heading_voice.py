"""Plain-English headings for the local-notes sections (gen 'uq', D-308).

The uniqueness notes used one pattern on about 500 pages: "<Topic>: streets and boundaries", "<Topic>: the housing stock",
"<Topic>: rules that affect buyers" and five more, word for word. Read across the site it looks generated, so each page now
gets its own wording, picked from a few plain phrasings by the page slug (stable from build to build) and never repeating a
heading already on the page. The place name stays in every heading.

heading(slug, topic, key, taken=set()) -> str. topic is the old prefix ("Hatzic Houses", "Murrayville", "Surrey Court-Ordered Sales").
"""
import hashlib, re

KEYS = {'streets and boundaries': 'streets', 'the housing stock': 'stock', 'rules that affect buyers': 'rules',
        'local details a buyer would not know': 'local', 'development and new projects': 'dev', 'costs and taxes': 'costs',
        'getting around': 'around', 'risks and due diligence': 'risks'}

TYPES = r'(?:\d+\+ )?(?:Acreages and Farms|Farms and Acreages|Neighbourhood Guides|Condos and Townhomes|Condos by Price Band|Townhomes|Condos|Houses|Homes|Lots and Land|Acreages|Court-Ordered Sales|Foreclosures and Court-Ordered Sales|Mobile Homes|Land Use Plans|Farms|Duplexes|Penthouses|Half Duplexes|Rural Properties|Poultry Farms|Horse Properties|Real Estate)(?: for Sale)?'


NOT_HOMES = re.compile(r'Court-Ordered Sales|Land Use Plans|Price Band|Neighbourhood Guides|Real Estate')


def split(topic):
    """'Hatzic Houses' -> ('Hatzic', 'houses'); 'Murrayville' -> ('Murrayville', ''); 'BC Egg Farms' -> (None, '') = keep as is."""
    if topic.startswith('BC ') or topic.endswith(' BC') or topic in ('Farms', 'Chicken Farms'):
        return None, ''
    m = re.match(rf'^(.+?)\s+({TYPES})(?:\s+(.+))?$', topic)
    if not m:
        return topic, ''
    place, kind, tail = m.group(1), re.sub(r' for Sale$', '', m.group(2)), m.group(3)
    if tail:                      # "Jacobsen Townhomes South Surrey": the complex name is the place
        return f'{place} {kind}', ''
    if NOT_HOMES.search(kind):
        return place, ''
    return place, kind.lower()


def variants(place, kind):
    k = kind or 'homes'
    what = f'{k} in {place}'
    return {
        'streets': [f'Where {place} is', f'{place} street by street', f'Where {place} starts and ends'],
        'stock': [f'What the {what} are like', f'The {what}', f'What {k} you will find in {place}'] if kind else [f'What the homes in {place} are like', f'The homes in {place}', f'What is built in {place}'],
        'rules': [f'Rules to know before you buy in {place}', f'Zoning and bylaws in {place}', f'What the rules allow in {place}'],
        'local': [f'Good to know about {place}', f'What locals know about {place}', f'Details buyers miss in {place}'],
        'dev': [f'What is changing in {place}', f'New projects and plans in {place}', f'What is being built in {place}'],
        'costs': [f'What it costs to own in {place}', f'Taxes, utilities and fees in {place}', f'Running costs in {place}'],
        'around': [f'Getting around from {place}', f'Commuting from {place}', f'Roads and transit in {place}'],
        'risks': [f'What to check before you buy in {place}', f'Checks before an offer in {place}', f'Questions to ask before buying in {place}'],
    }


def heading(slug, topic, section, taken=frozenset()):
    key = KEYS.get(section)
    if not key:
        return f'{topic}: {section}'
    place, kind = split(topic)
    if place is None:
        return f'{topic}: {section}'
    opts = variants(place, kind)[key]
    start = int(hashlib.sha1(f'{slug}|{key}'.encode()).hexdigest(), 16) % len(opts)
    for i in range(len(opts)):
        h = opts[(start + i) % len(opts)]
        if h.lower() not in taken:
            return h
    return f'{topic}: {section}'
