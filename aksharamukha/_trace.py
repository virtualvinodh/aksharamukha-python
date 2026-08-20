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


class Tracer:
    def __init__(self):
        self.entries = []
        self._depth = 0
        self._seq = 0
        self._patches = []  # (module, attr_name, original_fn), for uninstrument()

    def _make_wrapper(self, mod_name, fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            self._seq += 1
            seq = self._seq
            depth = self._depth
            self._depth += 1
            try:
                result = fn(*args, **kwargs)
                return result
            finally:
                self._depth -= 1
                first = args[0] if args else None
                result_val = locals().get('result')
                changed = isinstance(first, str) and isinstance(result_val, str) and result_val != first
                self.entries.append({
                    'seq': seq, 'depth': depth, 'module': mod_name, 'function': fn.__name__,
                    'args': args, 'kwargs': dict(kwargs), 'result': result_val, 'changed': changed,
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
