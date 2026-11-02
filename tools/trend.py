"""Thin-trend rule (Jared, 2026-11-01): we only call something a rise or a fall when the data can carry it.
  * a percentage change under MIN_PCT (1.5%) is "little changed", never a move;
  * a count-based change is not stated as a move when either count is under MIN_N (3), because one listing
    more or less is noise, not a trend.
Every generator that writes a direction in words goes through these helpers so the rule is applied one way."""
MIN_PCT = 1.5
MIN_N = 3
RULE = f'a change is called a rise or fall only at {MIN_PCT}% or more, and a count of fewer than {MIN_N} listings or sales is never described as a trend'


def signed(v):
    return f'{v:+.1f}%'.replace('-', '−')


def pct_move(v):
    """Phrase for a published % change, e.g. 'up 3.2%', 'down 2.0%', 'little changed at +0.4%'."""
    if v is None: return 'not published'
    if abs(v) < MIN_PCT: return f'little changed at {signed(v)}'
    return ('up ' if v > 0 else 'down ') + f'{abs(v):.1f}%'


def count_move(a, b, a_lab, b_lab, fmt=lambda n: f'{n:,}'):
    """Predicate for a count that went from a (in a_lab) to b (in b_lab); caller writes the subject.
    e.g. 'rose from 40 in June to 52 in September (+30.0%)'."""
    if a is None or b is None: return f'was not published for both {a_lab} and {b_lab}'
    if a < MIN_N or b < MIN_N:
        return f'was {fmt(a)} in {a_lab} and {fmt(b)} in {b_lab}, too few (under {MIN_N}) to call a rise or fall'
    ch = 100 * (b - a) / a
    if abs(ch) < MIN_PCT:
        return f'was little changed, {fmt(a)} in {a_lab} and {fmt(b)} in {b_lab} ({signed(ch)})'
    return f'{"rose" if b > a else "fell"} from {fmt(a)} in {a_lab} to {fmt(b)} in {b_lab} ({signed(ch)})'
