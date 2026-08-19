# -*- coding: utf-8 -*-

# BatakSima's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

# ---- Fix (encode/decode conversion logic) ----

def _FixBatakSimaEncode(Strng):
    """Replaces the vowel-sign-U sequence ᯙᯮ with the Simalungun Batak equivalent ᯙᯯ when encoding."""
    Strng = Strng.replace('ᯙᯮ', 'ᯙᯯ')

    return Strng

def _FixBatakSimaDecode(Strng):
    """Replaces the Simalungun Batak sequence ᯙᯯ back with the standard vowel-sign-U form ᯙᯮ when decoding."""
    Strng = Strng.replace('ᯙᯯ', 'ᯙᯮ')

    return Strng

def FixBatakSima(Strng, reverse=False):
    """Dispatches to the Simalungun Batak encode or decode fix-up routine based on the reverse flag."""
    return _FixBatakSimaDecode(Strng) if reverse else _FixBatakSimaEncode(Strng)
