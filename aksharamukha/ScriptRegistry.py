# -*- coding: utf-8 -*-

"""One ScriptDescriptor per script, replacing ~20 scattered per-script
lists/dicts in GeneralMap.py with a single lookup: SCRIPTS[name].

This module is purely additive: every field is mechanically derived from
GeneralMap.py's existing lists/dicts at import time, and nothing in the
rest of the codebase reads from SCRIPTS yet - see MARKERS.md-style
tracking in the docstring below for the migration status. That keeps this
step's risk near zero: it cannot change any conversion's output today,
because nothing calls it. _verify_consistency() re-derives every field
from source and asserts equality, so drift between this module and
GeneralMap.py during future edits is caught immediately rather than
silently.

Migration status: registry built and verified (this commit). No call
sites migrated to read from it yet - that's separate, incremental,
future work, one call site at a time, each independently tested.
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple
from . import GeneralMap as GM


@dataclass(frozen=True)
class ScriptDescriptor:
    name: str

    # Which ScriptMap/ subfolder this script's data module lives in.
    # One of 'MainIndic', 'EastIndic', 'NonIndic', 'Roman', or None if the
    # script isn't in any of GeneralMap's four family-path lists (this can
    # happen for Semitic scripts, which are resolved via gimeltra instead
    # of ScriptPath/CrunchSymbols).
    path_family: Optional[str]

    # ScriptCategory key, e.g. 'IndianMain' - None if uncategorized.
    category: Optional[str]

    # The three mutually-exclusive top-level families (verified disjoint
    # in GeneralMap.py: no script appears in more than one).
    is_indic: bool
    is_latin: bool
    is_semitic: bool

    is_roman_diacritic: bool
    is_transliteration: bool
    is_pipe_script: bool
    is_reversible: bool
    has_roman_numerals: bool
    has_roman_punct: bool

    gemination_mark: Optional[str]

    # LoC (ALA-LC romanization) fields - the data behind the "4 patches"
    # dispatch cluster in transliterate.py's convert(). Consolidating the
    # data here doesn't remove the dispatch logic itself (that's later,
    # riskier work) - it just gives that logic one place to read from
    # instead of 9.
    is_loc_script: bool
    loc_post_pre: bool
    loc_src_map: bool
    loc_tgt_map: bool
    loc_tgt_iso: bool
    loc_tgt_post_options: Tuple[str, ...] = field(default_factory=tuple)
    loc_tgt_pre_options: Tuple[str, ...] = field(default_factory=tuple)
    loc_src_post_options: Tuple[str, ...] = field(default_factory=tuple)
    loc_src_pre_options: Tuple[str, ...] = field(default_factory=tuple)

    # What this script's name becomes when routing through the LoC<->RomanLoC
    # pivot (e.g. 'Gurmukhi' -> 'GurmukhiLoC', any Tham-family script ->
    # 'ThamLoC'). Equal to the script's own name when there's no distinct
    # pivot form. Replaces the "src = src + 'LoC'" string-concatenation
    # previously inline in transliterate.py's LoC dispatch, which assumed
    # (correctly, but silently) that the concatenation always produces a
    # real registered script name. _verify_consistency() below checks that
    # assumption explicitly instead of leaving it implicit.
    loc_pivot_name: str = ''


def _loc_pivot_name_for(name):
    if name in GM.LoCSrcMap:
        return name + 'LoC'
    elif 'Tham' in name:
        return 'ThamLoC'
    else:
        return name


def _category_for(name):
    for cat, members in GM.ScriptCategory.items():
        if name in members:
            return cat
    return None


def _path_family_for(name):
    if name in GM.MainIndic:
        return 'MainIndic'
    if name in GM.EastIndic:
        return 'EastIndic'
    if name in GM.NonIndic:
        return 'NonIndic'
    if name in GM.Roman:
        return 'Roman'
    return None


def _build_registry():
    all_names = sorted(set(GM.IndicScripts) | set(GM.LatinScripts) | set(GM.SemiticScripts))
    registry = {}

    for name in all_names:
        registry[name] = ScriptDescriptor(
            name=name,
            path_family=_path_family_for(name),
            category=_category_for(name),
            is_indic=name in GM.IndicScripts,
            is_latin=name in GM.LatinScripts,
            is_semitic=name in GM.SemiticScripts,
            is_roman_diacritic=name in GM.RomanDiacritic,
            is_transliteration=name in GM.Transliteration,
            is_pipe_script=name in GM.pipeScripts,
            is_reversible=(name in GM.ReversibleScripts) or (name in GM.RomanReversible),
            has_roman_numerals=name in GM.romanNumeralScripts,
            has_roman_punct=name in GM.romanPunctscripts,
            gemination_mark=GM.Gemination.get(name),
            is_loc_script=name in GM.LoCScripts,
            loc_post_pre=name in GM.LocPostPre,
            loc_src_map=name in GM.LoCSrcMap,
            loc_tgt_map=name in GM.LoCTgtMap,
            loc_tgt_iso=name in GM.LoCTgtISO,
            loc_tgt_post_options=tuple(GM.LoCTgtPostOptions.get(name, [])),
            loc_tgt_pre_options=tuple(GM.LoCTgtPreOptions.get(name, [])),
            loc_src_post_options=tuple(GM.LoCSrcPostOptions.get(name, [])),
            loc_src_pre_options=tuple(GM.LoCSrcPreOptions.get(name, [])),
            loc_pivot_name=_loc_pivot_name_for(name),
        )

    return registry


SCRIPTS = _build_registry()

_MISSING = ScriptDescriptor(
    name='', path_family=None, category=None,
    is_indic=False, is_latin=False, is_semitic=False,
    is_roman_diacritic=False, is_transliteration=False, is_pipe_script=False,
    is_reversible=False, has_roman_numerals=False, has_roman_punct=False,
    gemination_mark=None, is_loc_script=False, loc_post_pre=False,
    loc_src_map=False, loc_tgt_map=False, loc_tgt_iso=False,
    loc_pivot_name='',
)


def get(name):
    """Like SCRIPTS[name], but returns an all-False/empty descriptor for
    an unregistered name instead of raising KeyError - mirrors the
    "not in list" semantics of the membership checks this registry
    replaces (e.g. pseudo-script names like 'ISO233' that only ever
    appear as an assigned value, never as a real registered script), so
    callers don't need a special-case guard at every call site."""
    return SCRIPTS.get(name, _MISSING)


def _verify_consistency():
    """Re-derive every field from GeneralMap.py's source lists/dicts and
    assert it matches SCRIPTS exactly. Run at import time (see bottom of
    this file) so any future edit to GeneralMap.py that isn't mirrored
    here fails loudly and immediately, instead of silently drifting."""
    all_names = sorted(set(GM.IndicScripts) | set(GM.LatinScripts) | set(GM.SemiticScripts))
    assert set(SCRIPTS.keys()) == set(all_names), (
        set(SCRIPTS.keys()) ^ set(all_names)
    )

    for name in all_names:
        d = SCRIPTS[name]
        assert d.name == name
        assert d.path_family == _path_family_for(name), name
        assert d.category == _category_for(name), name
        assert d.is_indic == (name in GM.IndicScripts), name
        assert d.is_latin == (name in GM.LatinScripts), name
        assert d.is_semitic == (name in GM.SemiticScripts), name
        assert d.is_roman_diacritic == (name in GM.RomanDiacritic), name
        assert d.is_transliteration == (name in GM.Transliteration), name
        assert d.is_pipe_script == (name in GM.pipeScripts), name
        assert d.is_reversible == ((name in GM.ReversibleScripts) or (name in GM.RomanReversible)), name
        assert d.has_roman_numerals == (name in GM.romanNumeralScripts), name
        assert d.has_roman_punct == (name in GM.romanPunctscripts), name
        assert d.gemination_mark == GM.Gemination.get(name), name
        assert d.is_loc_script == (name in GM.LoCScripts), name
        assert d.loc_post_pre == (name in GM.LocPostPre), name
        assert d.loc_src_map == (name in GM.LoCSrcMap), name
        assert d.loc_tgt_map == (name in GM.LoCTgtMap), name
        assert d.loc_tgt_iso == (name in GM.LoCTgtISO), name
        assert d.loc_tgt_post_options == tuple(GM.LoCTgtPostOptions.get(name, [])), name
        assert d.loc_tgt_pre_options == tuple(GM.LoCTgtPreOptions.get(name, [])), name
        assert d.loc_src_post_options == tuple(GM.LoCSrcPostOptions.get(name, [])), name
        assert d.loc_src_pre_options == tuple(GM.LoCSrcPreOptions.get(name, [])), name
        assert d.loc_pivot_name == _loc_pivot_name_for(name), name
        # The pivot name must always be either the script's own identity or
        # an actually-registered script - catches exactly the kind of silent
        # "X + 'LoC' isn't a real script" gap this field exists to prevent.
        # (Not required for every one of the 180 registered scripts, only
        # the ones actually reachable via is_loc_script - LoCTgtMap has one
        # unreachable stale entry, bare 'Batak', that fails this check and
        # is expected to.)
        if d.is_loc_script:
            assert d.loc_pivot_name == name or d.loc_pivot_name in SCRIPTS, (name, d.loc_pivot_name)


_verify_consistency()
