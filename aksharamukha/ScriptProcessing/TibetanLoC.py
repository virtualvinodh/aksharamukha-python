# -*- coding: utf-8 -*-

# TibetanLoC's Fix logic and LoC (Library of Congress) romanization
# logic. See ScriptProcessing/HOW_TO_ADD_LOC.md for the naming
# convention this follows and how to add a new script.
# RomanLocToTibetanLoC_pre is a thin alias to TibetanLoCToRomanLoc_pre -
# the original underlying fix (inserting prime marks after bare t/n) is
# genuinely reused unchanged in both directions.
#
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

# ---- Fix (encode/decode conversion logic) ----

# internal
def FixTibetanLoC(Strng,reverse=False):

    """Core Tibetan (LoC romanization variant) encode/decode logic: delegate to the shared Tibetan fixer without native-form swapping."""
    from .. import Options
    return Options.call_fix('FixTibetan', Strng,reverse, swapNative=False)

# ---- Pre-processing options ----

# internal
def TibetanLoCToRomanLoc_pre(Strng):
    """Insert LoC prime marks after bare t and n consonants not already followed by a diacritic, for Tibetan romanization."""
    Strng = re.sub('t(?![ʹhs])', 'tʹ', Strng)
    Strng = re.sub('n(?![ʹy])', 'nʹ', Strng)

    return Strng

# internal
def RomanLocToTibetanLoC_pre(Strng):
    """Thin alias for TibetanLoCToRomanLoc_pre - the same prime-mark fix is reused unchanged for both directions."""
    return TibetanLoCToRomanLoc_pre(Strng)

# ---- Post-processing options ----

# internal
def TibetanLoCToRomanLoc_post(Strng):
    """Fixes Tibetan LoC romanization: drops the modifier apostrophe on t/n unless followed by s/y respectively, and joins j_h into jh."""
    Strng = re.sub('tʹ(?!s)', 't', Strng)
    Strng = re.sub('nʹ(?!y)', 'n', Strng)
    Strng = re.sub('j_h', 'jh', Strng)

    return Strng
