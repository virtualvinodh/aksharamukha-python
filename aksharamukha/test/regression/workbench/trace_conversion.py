# -*- coding: utf-8 -*-
"""Dev tool: pretty-prints transliterate.process(..., trace=True) for one
conversion - shows the exact function call sequence and intermediate
text, including hops invisible from reading any single function - e.g.
Convert.py's _convert_to_semitic always pivots a non-Latin source
through the RomanSemitic intermediate before reaching a semitic target,
and the LoC/semiticISO option families are dispatched by runtime string
concatenation (transliterate.py's _apply_loc_option, ConvertFix.py's
globals()["Fix"+Target]) rather than a literal call anywhere.

The actual instrumentation (aksharamukha/_trace.py) lives in the main
package, not here - trace=True is a first-class part of
transliterate.process() now, this script is just a readable CLI over it.

Usage:
    python trace_conversion.py Tamil Sogd "some text"
    python trace_conversion.py Devanagari IAST "some text" --changes-only
    python trace_conversion.py Tamil RomanLoC "some text" --pre TamilNumeralSub --post TamilOmDisable
    python trace_conversion.py Kannada Telugu "some text" --no-nativize --max-depth 6
"""
import argparse
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
if REPO not in sys.path:
    sys.path.insert(0, REPO)


def short(x, max_len):
    s = repr(x)
    if len(s) > max_len:
        s = s[:max_len] + '...'
    return s


def format_args(args, kwargs, max_len):
    parts = [short(a, max_len) for a in args] + [k + '=' + short(v, max_len) for k, v in kwargs.items()]
    return ', '.join(parts)


def print_trace(entries, changes_only, max_depth, max_len):
    # Tracer appends each entry when the call RETURNS (its finally block),
    # so list order is completion order - a function with many nested
    # children ends up listed after all of them, despite being invoked
    # first. seq is assigned at call time, so sorting by it recovers true
    # invocation (processing) order.
    for e in sorted(entries, key=lambda e: e['seq']):
        if max_depth is not None and e['depth'] > max_depth:
            continue
        if changes_only and not e['changed'] and e['depth'] > 0:
            continue
        mark = '*' if e['changed'] else ' '
        mod = e['module'].replace('aksharamukha.', '')
        args_str = format_args(e['args'], e['kwargs'], max_len)
        print('%s%s[%d] %s.%s(%s) -> %s' % (
            '  ' * e['depth'], mark, e['seq'], mod, e['function'], args_str, short(e['result'], max_len)))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('source')
    p.add_argument('target')
    p.add_argument('text')
    p.add_argument('--pre', default='', help='comma-separated pre-option names')
    p.add_argument('--post', default='', help='comma-separated post-option names')
    p.add_argument('--no-nativize', action='store_true')
    p.add_argument('--changes-only', action='store_true', help='hide no-op calls (depth 0 always shown)')
    p.add_argument('--max-depth', type=int, default=None, help='hide calls nested deeper than this')
    p.add_argument('--max-len', type=int, default=60, help='truncate printed strings to this length')
    args = p.parse_args()

    from aksharamukha import transliterate

    pre_options = [x for x in args.pre.split(',') if x]
    post_options = [x for x in args.post.split(',') if x]

    result, entries = transliterate.process(
        args.source, args.target, args.text,
        nativize=not args.no_nativize,
        post_options=post_options, pre_options=pre_options,
        trace=True,
    )

    print('%s -> %s : %r -> %r' % (args.source, args.target, args.text, result))
    print('(%d calls traced, * = text changed)' % len(entries))
    print()
    print_trace(entries, args.changes_only, args.max_depth, args.max_len)


if __name__ == '__main__':
    main()
