# -*- coding: utf-8 -*-
"""Runtime call tracing behind transliterate.debug(). Two halves:

1. Tracer - monkey-patches every function in PreProcess/PostProcess/
   ConvertFix/Convert/transliterate and every ScriptProcessing/*.py
   module with a logging wrapper for the duration of one traced call,
   then restores the originals - so an ordinary (non-debug) call pays
   zero overhead. GeneralMap is deliberately excluded: its helpers
   (CrunchSymbols/CrunchList/resolve/...) run in tight per-character
   loops on non-string arguments and would drown the trace in noise
   unrelated to what happened to the text.

   Not thread-safe / not reentrant: instrumentation patches shared
   module state for the duration of the call. Don't run two debug()
   conversions concurrently, or call debug() recursively from within
   an already-traced call.

2. print_trace() and its helpers - format a Tracer's collected entries
   into readable step-by-step output. Lives here (not in a dev-only
   script) because transliterate.debug() calls it directly - see
   RETURN_SHAPES below for the one place this pulls in hand-verified,
   can-go-stale-safely knowledge in exchange for much more readable
   output.
"""
import functools
import importlib
import inspect
import pkgutil

# The parameter name actually carrying the text being converted, by
# established codebase convention - almost every ScriptProcessing/Pre/
# PostProcess/ConvertFix function names it `Strng`, transliterate.py's
# internal layer names it `txt`. Looked up BY NAME anywhere in the
# signature (not just position 0) - transliterate.py's own stage
# functions take it as their 3rd parameter (src, tgt, txt, ...). A
# function with none of these names (e.g. Convert._om_boundary_class
# (Source) - a regex-builder keyed on a SCRIPT NAME) has no text
# argument at all, and is left out of the text-level trace for that
# reason, not because nothing happened.
#
# Order matters: it's a priority list, not just a membership set. Two
# late-stage functions in transliterate.py - _apply_nativize_defaults
# and _apply_final_postprocessing - use `transliteration` for the value
# actually being transformed through the rest of their body, while
# _apply_final_postprocessing ALSO keeps the untouched original as
# `txt` (needed for exactly one special case, a Tamil->IPA external API
# call - see its body). Scanning txt/text before transliteration picked
# the wrong one there: comparing the ORIGINAL Burmese input against the
# already-fully-converted Latin output produced a false "changed" that
# had nothing to do with what this function itself did. `transliteration`
# has to outrank `txt`/`text` for that reason - caught by the user
# reading a step whose displayed input was still in the source script
# right before the final output.
TEXT_PARAM_NAMES = ('Strng', 'transliteration', 'txt', 'text')

# Pipeline state threaded through transliterate.py's convert() chain,
# tracked from CALL arguments only (bound by name via inspect.signature,
# which is genuinely reliable) - never from a function's return value.
# The _resolve_*/_apply_*/_prepare_* stage functions each return a
# tuple, but NOT in their own declared parameter order or even a
# consistent subset of it - e.g. _apply_indic_dandas_preoption(src,
# tgt, txt, preoptions, postoptions) returns (txt, preoptions,
# postoptions) - so zipping a return tuple against a function's own
# param names is not a real correspondence, just a coincidence of
# length (tried once, produced nonsense like 'src' being reported as
# the TEXT). Every updated value still becomes visible correctly, one
# hop later, at the next call it's passed into by name - convert()'s
# body always does `src, tgt, ... = _resolve_x(...)` and then passes
# THAT src/tgt on to the next traced call.
#
# preoptions/postoptions (the internal-layer names) and pre_options/
# post_options (the public process()/convert_default() names) are the
# same concept under two different spellings, and Convert.py's own
# layer names src/tgt Source/Target instead (convertScript(Strng,
# Source, Target, ctx), _convert_to_semitic(Strng, Source, Target,
# ctx), ...) - all normalized to one canonical display name each, so a
# pivot hop through Convert.py (e.g. Tamil -> RomanSemitic before
# reaching a semitic target) actually shows tgt changing instead of
# silently keeping the outer tgt on display because the inner layer
# spelled the parameter differently.
CANONICAL_STATE_NAME = {
    'src': 'src', 'Source': 'src', 'tgt': 'tgt', 'Target': 'tgt',
    'ctx': 'ctx', 'nativize': 'nativize',
    'preoptions': 'pre_options', 'pre_options': 'pre_options',
    'postoptions': 'post_options', 'post_options': 'post_options',
}


class Tracer:
    def __init__(self):
        self.entries = []
        self._depth = 0
        self._seq = 0
        self._patches = []  # (module, attr_name, original_fn), for uninstrument()
        self._state_values = {}  # canonical name -> current actual value

    def _snapshot_state(self, new_values):
        """Merge new_values (canonical name -> value) into the running
        pipeline state, then return {name: repr(value)} for every
        tracked field seen so far - not just the ones this call
        provided. Computed now, not deferred: ctx is the same object
        mutated in place throughout the whole conversion, so its repr
        has to be captured at this instant to reflect what was actually
        true at this point, not whatever it mutates to later."""
        self._state_values.update(new_values)
        return {name: repr(value) for name, value in self._state_values.items()}

    def _make_wrapper(self, mod_name, fn):
        # Logs 'call' and 'return' as two separate events, not one entry
        # covering both - a call's args are known when it's invoked, but
        # its result is only known later (after every nested call it makes
        # has already run). Bundling both onto one call-time-ordered entry
        # means an outer function - invoked first, but returning last -
        # shows its final result on the very first line of the trace,
        # before anything has actually been computed from the reader's
        # point of view. Two events, both carrying the true seq of when
        # they actually happened, avoids that.
        try:
            sig = inspect.signature(fn)
        except (TypeError, ValueError):
            sig = None

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            self._seq += 1
            depth = self._depth

            bound = {}
            if sig is not None:
                try:
                    bound = sig.bind_partial(*args, **kwargs).arguments
                except TypeError:
                    bound = {}

            text_param = next((n for n in TEXT_PARAM_NAMES if n in bound), None)
            text_in = bound.get(text_param) if text_param else None

            new_state = {CANONICAL_STATE_NAME[k]: v for k, v in bound.items() if k in CANONICAL_STATE_NAME}
            call_state = self._snapshot_state(new_state)

            self.entries.append({
                'event': 'call', 'seq': self._seq, 'depth': depth,
                'module': mod_name, 'function': fn.__name__, 'args': args, 'kwargs': dict(kwargs),
                'text_param': text_param, 'text_in': text_in, 'state': call_state,
            })
            self._depth += 1
            try:
                result = fn(*args, **kwargs)
                return result
            finally:
                self._depth -= 1
                self._seq += 1
                result_val = locals().get('result')
                changed = (
                    text_param is not None and isinstance(text_in, str)
                    and isinstance(result_val, str) and result_val != text_in
                )
                return_state = self._snapshot_state({})  # re-read now: ctx may have mutated during nested calls

                self.entries.append({
                    'event': 'return', 'seq': self._seq, 'depth': depth,
                    'module': mod_name, 'function': fn.__name__, 'result': result_val,
                    'text_param': text_param, 'text_in': text_in, 'changed': changed, 'state': return_state,
                })
        return wrapper

    def _instrument_module(self, mod):
        mod_name = mod.__name__
        for attr_name in list(vars(mod)):
            if attr_name.startswith('__'):
                continue
            fn = getattr(mod, attr_name)
            if inspect.isfunction(fn):
                self._patches.append((mod, attr_name, fn))
                setattr(mod, attr_name, self._make_wrapper(mod_name, fn))

    def instrument_everything(self):
        from . import transliterate, Convert, ConvertFix, PreProcess, PostProcess
        from . import ScriptProcessing as SP

        sp_modules = []
        for _finder, name, _ispkg in pkgutil.iter_modules(SP.__path__):
            sp_modules.append(importlib.import_module('aksharamukha.ScriptProcessing.' + name))

        for mod in [PreProcess, PostProcess, ConvertFix, Convert, transliterate] + sp_modules:
            self._instrument_module(mod)

    def uninstrument(self):
        for mod, attr_name, original_fn in self._patches:
            setattr(mod, attr_name, original_fn)
        self._patches = []


# ---- formatting: turns a Tracer's entries into readable step output ----

STATE_FIELDS = ('src', 'tgt', 'pre_options', 'post_options', 'nativize', 'ctx')

# transliterate.py's _resolve_*/_apply_*/_prepare_*/_run_* stage
# functions each return a tuple - but NOT in their own declared
# parameter order or even a consistent subset of it (see
# TEXT_PARAM_NAMES's comment above for the bug that came from assuming
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


def params_diff(call_e, return_e, max_len):
    """Only the STATE_FIELDS (+ any extra fields like tgtOld/srcOld from
    a decoded return tuple) that actually differ between this step's
    call and return - '' if nothing tracked changed. Prefers the
    function's own decoded return-tuple state (authoritative, straight
    from its actual return value) when RETURN_SHAPES recognizes it;
    otherwise falls back to the general running-state snapshot the
    Tracer keeps on every call/return regardless of function (so a step
    whose only effect was mutating ConversionContext, say, still shows
    it - not just the 9 functions with a known tuple shape)."""
    state_fields, _ = decode_return_tuple(return_e['function'], return_e['result'])
    candidate = {k: repr(v) for k, v in state_fields.items()} if state_fields is not None else return_e['state']
    call_state = call_e['state']
    diffs = [(name, value) for name, value in candidate.items() if call_state.get(name) != value]
    if not diffs:
        return ''
    order = {name: i for i, name in enumerate(STATE_FIELDS)}
    diffs.sort(key=lambda kv: order.get(kv[0], len(STATE_FIELDS)))
    return ', '.join('%s=%s' % (name, truncate(value, max_len)) for name, value in diffs)


def text_changed(return_e):
    """True if the text this step is actually about differs between
    input and output. The Tracer's own 'changed' flag can never be True
    for any of the 9 RETURN_SHAPES functions - they always return a
    tuple, never a bare string, and the Tracer deliberately doesn't
    guess a tuple's contents (see TEXT_PARAM_NAMES's comment). Decode
    the tuple here, where RETURN_SHAPES' hand-verified knowledge
    actually lives, and compare the extracted text field instead.
    Caught by a user noticing _run_core_conversion - which really does
    turn Burmese into Latin - was silently missing from a changed-only
    view entirely."""
    if return_e['changed']:
        return True
    _, text_value = decode_return_tuple(return_e['function'], return_e['result'])
    if isinstance(text_value, str) and isinstance(return_e['text_in'], str):
        return text_value != return_e['text_in']
    return False


def step_changed(call_e, return_e, max_len):
    return text_changed(return_e) or bool(params_diff(call_e, return_e, max_len))


def print_open(indent, step_no, mod, e, max_len):
    print('%s-> step %d: %s.%s' % (indent, step_no, mod, e['function']))
    params = format_params(e['state'], max_len)
    if params:
        print('%s     input_params: %s' % (indent, params))
    print('%s     input  = %s' % (indent, truncate(repr(e['text_in']), max_len)))


def print_close(indent, step_no, mod, call_e, return_e, max_len, arrow='<-'):
    if arrow == '<-':
        print('%s<- step %d: %s.%s' % (indent, step_no, mod, return_e['function']))
    diff = params_diff(call_e, return_e, max_len)
    if diff:
        print('%s     *output_params: %s' % (indent, diff))
    _, text_value = decode_return_tuple(return_e['function'], return_e['result'])
    output_value = text_value if text_value is not None else return_e['result']
    star = '*' if text_changed(return_e) else ' '
    print('%s     %soutput = %s' % (indent, star, truncate(repr(output_value), max_len)))
    print()


def _print_trace_events(entries, max_depth, max_len, should_show):
    # A call's args are known when it's invoked; its result is only
    # known later, once every nested call it makes has already run - so
    # an outer function is invoked FIRST but finishes LAST. A single
    # merged block (input+output together, positioned by call time) was
    # tried for the changed-only view, but for any WRAPPING step -
    # _process_dispatch, convert, etc, which can't return before
    # everything nested inside them completes - that meant showing the
    # final answer at the very top of the list, before any of the steps
    # that produce it. Showing '->' (call) and '<-' (return) as
    # separate lines, each at its own true seq, fixes this for good: a
    # step's output is only ever printed once it's actually known.
    # Paired by a stack so a step keeps the same number at both ends
    # regardless of what's interleaved - this also makes nesting
    # visible (ConvertFix.FixIndicOutput calling ShiftDiacritics
    # internally shows as parent-then-nested-child, not two flat
    # siblings). Step numbers are assigned at call time, so a parent
    # always has a lower number than the children nested inside it -
    # only the position of the '<-' line itself is in return order,
    # because that's genuinely when a nested call finishes.
    entries = sorted(entries, key=lambda e: e['seq'])
    mod_of = lambda e: e['module'].replace('aksharamukha.', '')
    step_no = 0
    call_stack = []  # (step_no or None, call_event), one per open call

    for e in entries:
        depth_ok = max_depth is None or e['depth'] <= max_depth
        indent = '  ' * e['depth']

        if e['event'] == 'call':
            show = depth_ok and e['text_param'] is not None and should_show(e)
            this_step = None
            if show:
                step_no += 1
                this_step = step_no
                print_open(indent, this_step, mod_of(e), e, max_len)
                print()
            call_stack.append((this_step, e))
        else:
            this_step, call_e = call_stack.pop()
            if this_step is None:
                continue
            print_close(indent, this_step, mod_of(e), call_e, e, max_len)


def print_trace_full(entries, max_depth, max_len):
    _print_trace_events(entries, max_depth, max_len, should_show=lambda e: True)


def print_trace_changes(entries, max_depth, max_len):
    # "Changed" isn't knowable until a call's return is seen (need the
    # result to compare against the input) - but the full trace is
    # already sitting in memory, not a live stream, so a first pass can
    # determine which call/return pairs changed before the real
    # (shared, seq-ordered) printing pass decides what to show.
    sorted_entries = sorted(entries, key=lambda e: e['seq'])

    call_stack = []
    changed_call_ids = set()
    for e in sorted_entries:
        if e['event'] == 'call':
            call_stack.append(e)
            continue
        call_e = call_stack.pop()
        if max_depth is not None and e['depth'] > max_depth:
            continue
        if e['text_param'] is None:
            continue
        if step_changed(call_e, e, max_len):
            changed_call_ids.add(id(call_e))

    _print_trace_events(entries, max_depth, max_len, should_show=lambda e: id(e) in changed_call_ids)


def print_trace(entries, changes_only, max_depth=None, max_len=120):
    if changes_only:
        print_trace_changes(entries, max_depth, max_len)
    else:
        print_trace_full(entries, max_depth, max_len)
