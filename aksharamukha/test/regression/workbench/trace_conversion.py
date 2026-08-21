# -*- coding: utf-8 -*-
"""Dev tool: pretty-prints transliterate.process(..., trace=True) for one
conversion - one block per step, each showing the function, its current
src/tgt/pre_options/post_options/nativize/ConversionContext, and its
text input/output - including hops invisible from reading any single
function, e.g. Convert.py's _convert_to_semitic always pivots a non-
Latin source through the RomanSemitic intermediate before reaching a
semitic target, and the LoC/semiticISO option families are dispatched
by runtime string concatenation rather than a literal call anywhere.

Only calls that actually take the text being converted as one of their
parameters are shown (by name - Strng/transliteration/txt/text, found
anywhere in the signature, not just position 0) - a helper keyed on
something else, e.g. Convert._om_boundary_class(Source) (a regex-
builder keyed on a script name), isn't a text-transforming step and
would just be noise.

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

STATE_FIELDS = ('src', 'tgt', 'pre_options', 'post_options', 'nativize', 'ctx')

# transliterate.py's _resolve_*/_apply_*/_prepare_*/_run_* stage
# functions each return a tuple - but NOT in their own declared
# parameter order or even a consistent subset of it (see _trace.py's
# TEXT_PARAM_NAMES comment for the bug that came from assuming
# otherwise). These shapes are the ACTUAL return statement of each
# function, read directly from transliterate.py, not inferred - if any
# of these functions' return statement changes, this goes stale and the
# label just won't apply (falls back to the plain repr below), it won't
# silently mislabel anything. The text-carrying field (txt, or
# transliteration for _run_core_conversion) is pulled out of the tuple
# and shown on its own output = line, same spot/label as every other
# function's text result - the rest becomes output_params:, mirroring
# input_params: on the call side.
RETURN_SHAPES = {
    '_apply_indic_dandas_preoption': ('txt', 'pre_options', 'post_options'),
    '_resolve_loc_when_source_is_loc_script': ('src', 'tgt', 'txt', 'pre_options', 'post_options', 'nativize'),
    '_resolve_loc_when_target_is_loc_script': ('src', 'tgt', 'txt', 'pre_options', 'post_options', 'nativize'),
    '_resolve_loc_dispatch': ('src', 'tgt', 'txt', 'pre_options', 'post_options', 'nativize'),
    '_resolve_semitic_iso_pivot': ('src', 'tgt', 'txt', 'pre_options', 'post_options', 'nativize'),
    '_resolve_semitic_indic_naming': ('src', 'tgt', 'txt', 'pre_options', 'post_options', 'nativize', 'tgtOld'),
    '_apply_target_renaming_postoptions': ('src', 'tgt', 'txt', 'pre_options', 'post_options', 'nativize'),
    '_prepare_for_core_conversion': ('src', 'tgt', 'txt', 'srcOld'),
    '_run_core_conversion': ('tgt', 'transliteration'),
}
TEXT_FIELD_NAMES = ('txt', 'transliteration')


def truncate(s, max_len):
    return s if len(s) <= max_len else s[:max_len] + '...'


def format_params(state, max_len):
    return ', '.join('%s=%s' % (f, truncate(state[f], max_len)) for f in STATE_FIELDS if f in state)


def decode_return_tuple(function, result):
    """(state_fields, text_value) for a known RETURN_SHAPES function
    whose result actually matches that shape - state_fields is an
    ordered dict of everything except the text field; (None, None) if
    this function/result isn't a recognized shape (caller falls back to
    treating result as the text value directly)."""
    shape = RETURN_SHAPES.get(function)
    if not shape or not isinstance(result, tuple) or len(result) != len(shape):
        return None, None
    fields = dict(zip(shape, result))
    text_value = None
    for name in TEXT_FIELD_NAMES:
        if name in fields:
            text_value = fields.pop(name)
            break
    return fields, text_value


def print_open(indent, step_no, mod, e, max_len):
    print('%s-> step %d: %s.%s' % (indent, step_no, mod, e['function']))
    params = format_params(e['state'], max_len)
    if params:
        print('%s     input_params: %s' % (indent, params))
    print('%s     input  = %s' % (indent, truncate(repr(e['text_in']), max_len)))


def print_close(indent, step_no, mod, e, max_len, arrow='<-'):
    if arrow == '<-':
        print('%s<- step %d: %s.%s' % (indent, step_no, mod, e['function']))
    state_fields, text_value = decode_return_tuple(e['function'], e['result'])
    if state_fields is not None:
        state_str = ', '.join('%s=%s' % (name, truncate(repr(value), max_len)) for name, value in state_fields.items())
        if state_str:
            print('%s     output_params: %s' % (indent, state_str))
        output_value = text_value
    else:
        output_value = e['result']
    mark = '  *changed*' if e['changed'] else ''
    print('%s     output = %s%s' % (indent, truncate(repr(output_value), max_len), mark))
    print()


def print_trace(entries, changes_only, max_depth, max_len):
    # A call's args are known when it's invoked; its result is only
    # known later, once every nested call it makes has already run - so
    # an outer function is invoked FIRST but finishes LAST. Printing
    # only completed (return) events in a flat list hides that: it looks
    # like sibling steps in sequence when one is actually a PARENT that
    # opened long before, with the other running nested inside it (this
    # is exactly what made ConvertFix.FixIndicOutput's internal
    # ShiftDiacritics call look like a preceding sibling step instead of
    # a child). Showing both '->' (call) and '<-' (return) - paired by a
    # stack so a step keeps the same number at both ends regardless of
    # what else is interleaved - makes the nesting visible again, the
    # way a real call-stack trace would.
    entries = sorted(entries, key=lambda e: e['seq'])
    mod_of = lambda e: e['module'].replace('aksharamukha.', '')
    step_no = 0
    call_stack = []  # step_no (or None if this call wasn't shown), one per open call

    for e in entries:
        depth_ok = max_depth is None or e['depth'] <= max_depth
        indent = '  ' * e['depth']

        if e['event'] == 'call':
            show = depth_ok and e['text_param'] is not None and not changes_only
            this_step = None
            if show:
                step_no += 1
                this_step = step_no
                print_open(indent, this_step, mod_of(e), e, max_len)
                print()
            call_stack.append(this_step)
        else:
            this_step = call_stack.pop()
            if changes_only:
                if not depth_ok or e['text_param'] is None or not e['changed']:
                    continue
                step_no += 1
                print_open(indent, step_no, mod_of(e), e, max_len)
                print_close(indent, step_no, mod_of(e), e, max_len, arrow=None)
            else:
                if this_step is None:
                    continue
                print_close(indent, this_step, mod_of(e), e, max_len)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('source')
    p.add_argument('target')
    p.add_argument('text')
    p.add_argument('--pre', default='', help='comma-separated pre-option names')
    p.add_argument('--post', default='', help='comma-separated post-option names')
    p.add_argument('--no-nativize', action='store_true')
    p.add_argument('--changes-only', action='store_true', help='only show steps that actually changed the text')
    p.add_argument('--max-depth', type=int, default=None, help='hide calls nested deeper than this')
    p.add_argument('--max-len', type=int, default=120, help='truncate printed strings to this length')
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
    print('(%d calls traced)' % (len(entries) // 2))
    print()
    print_trace(entries, args.changes_only, args.max_depth, args.max_len)


if __name__ == '__main__':
    main()
