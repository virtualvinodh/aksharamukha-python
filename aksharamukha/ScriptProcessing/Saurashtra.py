# -*- coding: utf-8 -*-

# Saurashtra's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def _FixSaurashtraEncode(Strng):
    """Inserts a ZWNJ within the ksha conjunct to prevent unwanted ligation when encoding into Saurashtra, e.g. ꢒ꣄ꢰ → ꢒ꣄‍ꢰ."""
    Strng = Strng.replace('ꢒ꣄ꢰ', 'ꢒ꣄‍ꢰ') # Ksha

    return Strng

def _FixSaurashtraDecode(Strng):
    """Expands the precomposed Saurashtra ha-virama letter into its virama-plus-ha sequence when decoding, e.g. ꢴ → ꣄ꢲ."""
    Strng = Strng.replace('ꢴ','꣄ꢲ')

    return Strng

def FixSaurashtra(Strng, reverse=False):
    """Dispatches to the Saurashtra encode or decode fix-up routine based on the reverse flag."""
    return _FixSaurashtraDecode(Strng) if reverse else _FixSaurashtraEncode(Strng)
