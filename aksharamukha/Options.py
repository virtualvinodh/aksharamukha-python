# -*- coding: utf-8 -*-

"""Precomputed, validated pre/post-option name sets.

Replaces two problems that used to live inline in
transliterate.convert_default(), run on every single conversion call:

1. Performance: inspect.getmembers(PreProcess, isfunction) /
   getmembers(PostProcess, isfunction) reflected over the entire module
   namespace on every call, to rebuild the same two lists every time.
   Same class of issue as GeneralMap.CrunchSymbols/CrunchList before
   Phase 1's lru_cache fix - now computed once at import time instead.

2. Correctness: a misspelled option name (e.g. 'ThaiPhnetic') doesn't
   case-insensitively match any real function name, so the old
   list-comprehension-based normalization just silently dropped it -
   pattern 05 from the code audit ("a typo in an option name silently
   no-ops"), live in the default API path every transliterate.process()
   call goes through. normalize_pre_options/normalize_post_options below
   now warn on any unrecognized name instead of ignoring it.
"""

import functools
import inspect
import warnings
from inspect import getmembers, isfunction
from . import PreProcess, PostProcess

# Real function references, resolved once at import time, instead of a bare
# name string re-resolved via getattr() on every single dispatch call (the
# "stringly-typed options" pattern - see MARKERS.md/the code audit, pattern
# 05). PRE_OPTIONS/POST_OPTIONS are derived from these dicts' keys so the
# two can never drift apart.
_PRE_OPTION_FUNCS = dict(getmembers(PreProcess, isfunction))
_POST_OPTION_FUNCS = dict(getmembers(PostProcess, isfunction))

PRE_OPTIONS = frozenset(_PRE_OPTION_FUNCS)
POST_OPTIONS = frozenset(_POST_OPTION_FUNCS)

_PRE_OPTIONS_LOWER = {name.lower(): name for name in PRE_OPTIONS}
_POST_OPTIONS_LOWER = {name.lower(): name for name in POST_OPTIONS}


def _normalize(options, lookup, kind):
    resolved = []
    for option in options:
        canonical = lookup.get(option.lower())
        if canonical is None:
            warnings.warn(
                kind + "-option '" + option + "' is not a recognized option "
                "name and will be ignored."
            )
        else:
            resolved.append(canonical)
    return resolved


def normalize_pre_options(options):
    return _normalize(options, _PRE_OPTIONS_LOWER, 'Pre')


def normalize_post_options(options):
    return _normalize(options, _POST_OPTIONS_LOWER, 'Post')


@functools.lru_cache(maxsize=None)
def _accepts_ctx(fn):
    try:
        return 'ctx' in inspect.signature(fn).parameters
    except (TypeError, ValueError):
        return False


def call_pre_option(name, txt, *extra, ctx=None):
    # Unknown name -> AttributeError, matching the getattr() failure mode
    # this replaces (a typo'd pre_options entry should fail loudly, not
    # silently no-op - see GeneralMap.resolve's optional=False default,
    # which this mirrors for the same reason).
    #
    # *extra mirrors call_post_option below - added for PreOptions.
    # ApplyPreProcessing (the pre-processing counterpart to PostOptions.
    # ApplyScriptDefaults), which needs to call pre-options that take more
    # than just txt. The general pre_options=[name] list a caller supplies
    # still only ever passes txt - there's no way to smuggle extra
    # positional args through a bare string, same as call_post_option's
    # *extra is unused by the equivalent postoptions=[name] list.
    fn = _PRE_OPTION_FUNCS.get(name)
    if fn is None:
        raise AttributeError("module 'aksharamukha.PreProcess' has no attribute '" + name + "'")
    if ctx is not None and _accepts_ctx(fn):
        return fn(txt, *extra, ctx=ctx)
    return fn(txt, *extra)


def call_post_option(name, txt, *extra, ctx=None):
    fn = _POST_OPTION_FUNCS.get(name)
    if fn is None:
        raise AttributeError("module 'aksharamukha.PostProcess' has no attribute '" + name + "'")
    if ctx is not None and _accepts_ctx(fn):
        return fn(txt, *extra, ctx=ctx)
    return fn(txt, *extra)
