# -*- coding: utf-8 -*-

# TibetanLoC's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.
#
# TibetanLoCRomanLoCFix independently defines the SAME option name in
# both PreProcess.py and PostProcess.py as genuinely different functions
# - suffixed _pre/_post here, same convention used everywhere else.

import re

# ---- Fix (encode/decode conversion logic) ----

def FixTibetanLoC(Strng,reverse=False):

    """Core Tibetan (LoC romanization variant) encode/decode logic: delegate to the shared Tibetan fixer without native-form swapping."""
    from .. import ConvertFix as CF
    return CF.FixTibetan(Strng,reverse, swapNative=False)

# ---- Pre-processing options ----

def TibetanLoCRomanLoCFix_pre(Strng):
    """Insert LoC prime marks after bare t and n consonants not already followed by a diacritic, for Tibetan romanization."""
    Strng = re.sub('t(?![ʹhs])', 'tʹ', Strng)
    Strng = re.sub('n(?![ʹy])', 'nʹ', Strng)

    return Strng

# ---- Post-processing options ----

def TibetanLoCRomanLoCFix_post(Strng):
    """Fixes Tibetan LoC romanization: drops the modifier apostrophe on t/n unless followed by s/y respectively, and joins j_h into jh."""
    Strng = re.sub('tʹ(?!s)', 't', Strng)
    Strng = re.sub('nʹ(?!y)', 'n', Strng)
    Strng = re.sub('j_h', 'jh', Strng)

    return Strng
