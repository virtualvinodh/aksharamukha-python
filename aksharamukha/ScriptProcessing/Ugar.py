# -*- coding: utf-8 -*-

# Ugar's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixUgarEncode(Strng, Source):
    """Merges a marked consonant+2 sequence into its dedicated Ugaritic letter and replaces spaces with the Ugaritic word-divider wedge character."""
    Strng = Strng.replace("𐎒²","𐎝")
    Strng = Strng.replace(' ', '𐎟')

    return Strng

# internal
def _FixUgarDecode(Strng, Source):
    """Strips the Ugaritic word-divider wedge character from the text."""
    Strng = Strng.replace('𐎟', '')

    return Strng

# internal
def FixUgar(Strng, Source, reverse=False):
    """Dispatches to the Ugaritic encode or decode fix routine depending on the reverse flag."""
    return _FixUgarDecode(Strng, Source) if reverse else _FixUgarEncode(Strng, Source)
