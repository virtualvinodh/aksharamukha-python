# -*- coding: utf-8 -*-

# Urdu's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

# ---- Fix (encode/decode conversion logic) ----

def FixUrdu(Strng, reverse=False):

    """Core Urdu encode/decode logic: delegate to the shared Shahmukhi orthography fixer."""
    from .. import ConvertFix as CF
    return CF.FixUrduShahmukhi("Urdu", Strng, reverse)

# ---- Pre-processing options ----

def UrduShortNotShown(Strng):
    """Mark that Urdu short vowels are not written, appending a flag consumed by later processing to suppress short-vowel signs."""
    Strng += "\u02BB\u02BB"

    return Strng

# ---- Post-processing options ----

def UrduAlternateUU(Strng):
    """Intended to replace a short-u+wow sequence with wow+hamza-below as an alternate Urdu spelling; the search string is a literal backslash-escaped text, not an actual Unicode sequence, so this currently has no effect."""
    Strng = Strng.replace("\\u064F\\u0648","\u0648\u0657")

    return Strng

def UrduRemoveShortVowels(Strng):
    """Remove short vowels - hindustan-with-marks -> hindustan (strips sukun, fatha, kasra, damma, and the Urdu small-v diacritics)."""
    ShortVowels = ['\u0652','\u064E','\u0650','\u064F', '\u0658']

    for vow in ShortVowels:
        Strng = Strng.replace(vow,"")

    return Strng

