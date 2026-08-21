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

import ast
import functools
import importlib
import inspect
import io
import pkgutil
import warnings
from inspect import getmembers, isfunction
from . import PreProcess, PostProcess
from . import ScriptProcessing as _SP

# '# ---- Pre-processing options ----' / '# ---- Post-processing options
# ----' mark a function as belonging to that script's option surface -
# the same convention every ScriptProcessing/<Script>.py file already
# uses (established by the batch migration that consolidated each
# script's Fix/option logic into its own file; verified identical
# across all 128 files, no variant spellings). Scanning for it here
# means a new option just needs to be written under the right header in
# the right script's file - no `from .ScriptProcessing.X import name`
# re-export line into PreProcess.py/PostProcess.py required just to
# make this module's reflection see it. (A re-export is still needed
# for a name that has to be directly reachable as PreProcess.name/
# PostProcess.name for some other reason, e.g. a genuinely
# multi-script-shared helper like PostProcess.ThaiLaoTranscription,
# called from Thai.py/Lao.py/LaoPali.py alike - those stay defined
# directly in PreProcess.py/PostProcess.py, never move into one
# script's file, so this scan never sees them either way.)
_SECTION_KIND = {
    '# ---- Pre-processing options ----': 'pre',
    '# ---- Post-processing options ----': 'post',
}

# A function named X_pre (under a Pre-processing options header) or
# X_post (under Post-processing options) is the codebase's established
# convention for "this needs the bare public name X, but can't literally
# be called that in its own file" - either a name collision with the
# opposite direction's function in the SAME file (Python doesn't allow
# two top-level `def X` in one module; the second silently shadows the
# first), or, since the semiticISO rename, a dispatch-required name
# (ISO233Target/ISO233Source/...) that bears no textual relation to the
# function's own descriptive name. Registering the STRIPPED name too
# (alongside the raw one, never instead of it - existing callers using
# the raw suffixed name directly still work) means the established
# suffix convention is itself enough to make a name auto-discoverable
# under its true public form, without also needing a
# `from .ScriptProcessing.X import name_pre as name` re-export just to
# perform that same stripping via an import alias.
_KIND_SUFFIX = {'pre': '_pre', 'post': '_post'}


def _scriptprocessing_option_funcs():
    """{name: fn} for every function found under a Pre-processing/Post-
    processing options header in any ScriptProcessing/<Script>.py file,
    for each kind - the ACTUAL source of truth for "is this a pre/post
    option", now read directly instead of inferred from what happens to
    be re-exported. Raises ImportError at import time (not silently,
    not just when someone happens to use the colliding name) if the
    same name - raw OR suffix-stripped - is defined under the same
    kind's header in two different scripts' files - previously this
    ambiguity was implicitly resolved by whichever `from
    .ScriptProcessing.X import name` re-export line happened to run
    last, silently overwriting the other in PreProcess.py's/
    PostProcess.py's namespace."""
    funcs = {'pre': {}, 'post': {}}
    owner = {'pre': {}, 'post': {}}

    def register(kind, name, mod_name, fn):
        if name in owner[kind] and owner[kind][name] != mod_name:
            raise ImportError(
                "%s-option '%s' is defined in both ScriptProcessing/%s.py and "
                "ScriptProcessing/%s.py - option names must be unique across "
                "scripts; rename one of them." % (kind, name, owner[kind][name], mod_name)
            )
        funcs[kind][name] = fn
        owner[kind][name] = mod_name

    for _finder, mod_name, _ispkg in pkgutil.iter_modules(_SP.__path__):
        module = importlib.import_module('aksharamukha.ScriptProcessing.' + mod_name)
        src = io.open(module.__file__, encoding='utf-8').read()
        lines = src.splitlines()
        tree = ast.parse(src)

        headers = []  # (lineno, kind_or_None-for-the-Fix-header)
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped in _SECTION_KIND:
                headers.append((i, _SECTION_KIND[stripped]))
            elif stripped.startswith('# ----'):
                headers.append((i, None))

        def kind_at(lineno):
            current = None
            for header_line, kind in headers:
                if header_line <= lineno:
                    current = kind
                else:
                    break
            return current

        for node in tree.body:
            if not isinstance(node, ast.FunctionDef):
                continue
            kind = kind_at(node.lineno)
            if kind is None:
                continue
            name = node.name
            fn = getattr(module, name)
            register(kind, name, mod_name, fn)
            suffix = _KIND_SUFFIX[kind]
            if name.endswith(suffix) and len(name) > len(suffix):
                register(kind, name[:-len(suffix)], mod_name, fn)

    return funcs['pre'], funcs['post']


_sp_pre_funcs, _sp_post_funcs = _scriptprocessing_option_funcs()

# Real function references, resolved once at import time, instead of a bare
# name string re-resolved via getattr() on every single dispatch call (the
# "stringly-typed options" pattern - see MARKERS.md/the code audit, pattern
# 05). PRE_OPTIONS/POST_OPTIONS are derived from these dicts' keys so the
# two can never drift apart. The ScriptProcessing-sourced dicts come first,
# so a function directly defined in PreProcess.py/PostProcess.py (a
# deliberately shared, multi-script helper, or simply a still-unmigrated
# one) can still shadow a same-named ScriptProcessing entry if it ever
# needs to - matches the priority the getmembers() scan alone already had.
_PRE_OPTION_FUNCS = {**_sp_pre_funcs, **dict(getmembers(PreProcess, isfunction))}
_POST_OPTION_FUNCS = {**_sp_post_funcs, **dict(getmembers(PostProcess, isfunction))}

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
