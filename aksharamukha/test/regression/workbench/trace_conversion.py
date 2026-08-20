# -*- coding: utf-8 -*-
"""Dev tool: shows the exact function call sequence and intermediate text
for one real aksharamukha conversion, including hops invisible from
reading any single function - e.g. Convert.py's _convert_to_semitic
always pivots a non-Latin source through the RomanSemitic intermediate
before reaching a semitic target, and the LoC/semiticISO option families
are dispatched by runtime string concatenation
(transliterate.py's _apply_loc_option, ConvertFix.py's
globals()["Fix"+Target]) rather than a literal call anywhere.

How: monkey-patches every function in PreProcess/PostProcess/ConvertFix/
Convert/transliterate and every ScriptProcessing/*.py module with a
logging wrapper (in memory only - nothing is written to any source
file), runs one real transliterate.process(...) call, and prints the
nested call tree with the text before/after each step. GeneralMap is
deliberately not instrumented - its helpers (CrunchSymbols/CrunchList/
resolve/...) run in tight per-character loops on non-string arguments
and would drown the trace in noise unrelated to what happened to the
text.

Usage:
    python trace_conversion.py Tamil Sogd "some text"
    python trace_conversion.py Devanagari IAST "some text" --changes-only
    python trace_conversion.py Tamil RomanLoC "some text" --pre TamilNumeralSub --post TamilOmDisable
    python trace_conversion.py Kannada Telugu "some text" --no-nativize --max-depth 6
"""
import argparse
import functools
import importlib
import inspect
import pkgutil
import sys
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
if REPO not in sys.path:
    sys.path.insert(0, REPO)


def short(x, max_len):
    s = repr(x)
    if len(s) > max_len:
        s = s[:max_len] + '...'
    return s


class Tracer:
    def __init__(self, max_len):
        self.entries = []
        self.depth = 0
        self.seq = 0
        self.max_len = max_len

    def make_wrapper(self, mod_name, fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            self.seq += 1
            seq = self.seq
            depth = self.depth
            arg_str = ', '.join(
                [short(a, self.max_len) for a in args]
                + [k + '=' + short(v, self.max_len) for k, v in kwargs.items()]
            )
            self.depth += 1
            try:
                result = fn(*args, **kwargs)
                return result
            finally:
                self.depth -= 1
                first_arg_repr = args[0] if args and isinstance(args[0], str) else None
                result_repr = locals().get('result')
                changed = isinstance(result_repr, str) and first_arg_repr is not None and result_repr != first_arg_repr
                self.entries.append({
                    'seq': seq, 'depth': depth, 'mod': mod_name, 'name': fn.__name__,
                    'args': arg_str, 'result': short(locals().get('result', '<exception>'), self.max_len),
                    'changed': changed,
                })
        return wrapper

    def instrument_module(self, mod):
        # Wrap every function-valued attribute in THIS module's own
        # namespace, regardless of where it was originally defined.
        # Re-exported names (e.g. PostProcess.py's `from
        # .ScriptProcessing.Tamil import TamilDisableSHA`) are a separate,
        # already-bound reference distinct from ScriptProcessing.Tamil's
        # own copy - dispatch code (Options.py's getattr(PostProcess,
        # name)) calls THIS module's binding, so it has to be wrapped
        # here too, not just at its origin definition site.
        mod_name = mod.__name__
        for attr_name in list(vars(mod)):
            if attr_name.startswith('__'):
                continue
            fn = getattr(mod, attr_name)
            if inspect.isfunction(fn) and not getattr(fn, '_is_traced', False):
                wrapped = self.make_wrapper(mod_name, fn)
                wrapped._is_traced = True
                setattr(mod, attr_name, wrapped)


def instrument_everything(tracer):
    import aksharamukha  # noqa: F401
    from aksharamukha import transliterate, Convert, ConvertFix, PreProcess, PostProcess
    import aksharamukha.ScriptProcessing as SP

    sp_modules = []
    for _finder, name, _ispkg in pkgutil.iter_modules(SP.__path__):
        sp_modules.append(importlib.import_module('aksharamukha.ScriptProcessing.' + name))

    for mod in [PreProcess, PostProcess, ConvertFix, Convert, transliterate] + sp_modules:
        tracer.instrument_module(mod)

    return transliterate


def print_trace(entries, changes_only, max_depth):
    for e in entries:
        if max_depth is not None and e['depth'] > max_depth:
            continue
        if changes_only and not e['changed'] and e['depth'] > 0:
            continue
        mark = '*' if e['changed'] else ' '
        mod = e['mod'].replace('aksharamukha.', '')
        print('%s%s[%d] %s.%s(%s) -> %s' % (
            '  ' * e['depth'], mark, e['seq'], mod, e['name'], e['args'], e['result']))


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

    tracer = Tracer(args.max_len)
    transliterate = instrument_everything(tracer)

    pre_options = [x for x in args.pre.split(',') if x]
    post_options = [x for x in args.post.split(',') if x]

    result = transliterate.process(
        args.source, args.target, args.text,
        nativize=not args.no_nativize,
        post_options=post_options, pre_options=pre_options,
    )

    print('%s -> %s : %r -> %r' % (args.source, args.target, args.text, result))
    print('(%d calls traced, %s = text changed)' % (len(tracer.entries), '*'))
    print()
    print_trace(tracer.entries, args.changes_only, args.max_depth)


if __name__ == '__main__':
    main()
