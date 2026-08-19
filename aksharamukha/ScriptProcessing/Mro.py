# -*- coding: utf-8 -*-

# Mro's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def _FixMroEncode(Strng):
    """Merges specific Mro consonant + diacritic sequences into their dedicated precomposed consonant letters."""
    extracons = ['\U00016A4E', '\U00016A59', '\U00016A5A', '\U00016A5B', '\U00016A5C', '\U00016A5E']
    consnormaldig = ['𖩃𖩢', '𖩌𖩢', '𖩍𖩢', '𖩍𖩣', '𖩉𖩢', '𖩀𖩢']
    consnormal = ['𖩃', '𖩌', '𖩍', '𖩍', '𖩉', '𖩀']

    for x, y in zip(consnormaldig, extracons):
        Strng = Strng.replace(x, y)

    return Strng

def _FixMroDecode(Strng):
    """Expands the dedicated Mro precomposed consonant letters back to their base consonant forms."""
    extracons = ['\U00016A4E', '\U00016A59', '\U00016A5A', '\U00016A5B', '\U00016A5C', '\U00016A5E']
    consnormaldig = ['𖩃𖩢', '𖩌𖩢', '𖩍𖩢', '𖩍𖩣', '𖩉𖩢', '𖩀𖩢']
    consnormal = ['𖩃', '𖩌', '𖩍', '𖩍', '𖩉', '𖩀']

    for x, y in zip(extracons, consnormal):
        Strng = Strng.replace(x, y)

    return Strng

def FixMro(Strng, reverse=False):
    """Dispatches to the Mro encode or decode fix routine depending on conversion direction."""
    return _FixMroDecode(Strng) if reverse else _FixMroEncode(Strng)
