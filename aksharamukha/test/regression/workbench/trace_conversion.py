# -*- coding: utf-8 -*-
"""Dev tool: CLI wrapper around transliterate.debug() - the actual
tracing (aksharamukha/_trace.py) and formatting (also _trace.py, since
transliterate.debug() calls it directly) both live in the main package
now, not here. This script is just argparse plumbing.

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


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('source')
    p.add_argument('target')
    p.add_argument('text')
    p.add_argument('--pre', default='', help='comma-separated pre-option names')
    p.add_argument('--post', default='', help='comma-separated post-option names')
    p.add_argument('--no-nativize', action='store_true')
    p.add_argument('--changes-only', action='store_true', help='only show steps that changed the text or a tracked param')
    p.add_argument('--max-depth', type=int, default=None, help='hide calls nested deeper than this')
    p.add_argument('--max-len', type=int, default=120, help='truncate printed strings to this length')
    args = p.parse_args()

    from aksharamukha import transliterate

    pre_options = [x for x in args.pre.split(',') if x]
    post_options = [x for x in args.post.split(',') if x]

    transliterate.debug(
        args.source, args.target, args.text,
        nativize=not args.no_nativize,
        post_options=post_options, pre_options=pre_options,
        changes_only=args.changes_only, max_depth=args.max_depth, max_len=args.max_len,
    )


if __name__ == '__main__':
    main()
