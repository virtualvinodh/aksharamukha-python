# -*- coding: utf-8 -*-

# Urdu's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re

# ---- Fix (encode/decode conversion logic) ----

# internal
def FixUrdu(Strng, reverse=False, ctx=None):

    """Core Urdu encode/decode logic: delegate to the shared Shahmukhi orthography fixer."""
    from .. import ConvertFix as CF
    return CF.FixUrduShahmukhi("Urdu", Strng, reverse, ctx=ctx)

# ---- Pre-processing options ----

# frontend
def UrduShortNotShown(Strng):
    """Selects Urdu 'short vowels not shown' mode - a no-op here; transliterate.py sets ctx.transcription_mode directly from this name's presence in preoptions (same mechanism as ThaiPhonetic/LaoPhonetic/ThaiOrthography/LaoTranscription), read by ConvertFix._FixUrduShahmukhiDecode."""
    return Strng

# ---- Post-processing options ----

# unreferenced
def UrduAlternateUU(Strng):
    """Intended to replace a short-u+wow sequence with wow+hamza-below as an alternate Urdu spelling; the search string is a literal backslash-escaped text, not an actual Unicode sequence, so this currently has no effect."""
    Strng = Strng.replace("\\u064F\\u0648","\u0648\u0657")

    return Strng

# frontend
def UrduRemoveShortVowels(Strng):
    """Remove short vowels - hindustan-with-marks -> hindustan (strips sukun, fatha, kasra, damma, and the Urdu small-v diacritics)."""
    ShortVowels = ['\u0652','\u064E','\u0650','\u064F', '\u0658']

    for vow in ShortVowels:
        Strng = Strng.replace(vow,"")

    return Strng

