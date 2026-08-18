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

import warnings
from inspect import getmembers, isfunction
from . import PreProcess, PostProcess

PRE_OPTIONS = frozenset(name for name, _ in getmembers(PreProcess, isfunction))
POST_OPTIONS = frozenset(name for name, _ in getmembers(PostProcess, isfunction))

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
