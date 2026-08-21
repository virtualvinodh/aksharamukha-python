# -*- coding: utf-8 -*-
"""Runtime call tracing behind transliterate.process(..., trace=True).
Monkey-patches every function in PreProcess/PostProcess/ConvertFix/
Convert/transliterate and every ScriptProcessing/*.py module with a
logging wrapper for the duration of one traced call, then restores the
originals - so an ordinary (trace=False) call pays zero overhead.
GeneralMap is deliberately excluded: its helpers (CrunchSymbols/
CrunchList/resolve/...) run in tight per-character loops on non-string
arguments and would drown the trace in noise unrelated to what happened
to the text.

Not thread-safe / not reentrant: instrumentation patches shared module
state for the duration of the call. Don't run two trace=True
conversions concurrently, or call process(..., trace=True) recursively
from within an already-traced call.
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
TEXT_PARAM_NAMES = ('Strng', 'txt', 'text')

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
