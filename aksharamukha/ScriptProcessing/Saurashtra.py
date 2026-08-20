# -*- coding: utf-8 -*-

# Saurashtra's own Fix/post-option logic, consolidated out of
# ConvertFix.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from aksharamukha.ScriptMap.MainIndic import Saurashtra

# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixSaurashtraEncode(Strng):
    """Inserts a ZWNJ within the ksha conjunct to prevent unwanted ligation when encoding into Saurashtra, e.g. ꢒ꣄ꢰ → ꢒ꣄‍ꢰ."""
    Strng = Strng.replace('ꢒ꣄ꢰ', 'ꢒ꣄‍ꢰ') # Ksha

    return Strng

# internal
def _FixSaurashtraDecode(Strng):
    """Expands the precomposed Saurashtra ha-virama letter into its virama-plus-ha sequence when decoding, e.g. ꢴ → ꣄ꢲ."""
    Strng = Strng.replace('ꢴ','꣄ꢲ')

    return Strng

# internal
def FixSaurashtra(Strng, reverse=False):
    """Dispatches to the Saurashtra encode or decode fix-up routine based on the reverse flag."""
    return _FixSaurashtraDecode(Strng) if reverse else _FixSaurashtraEncode(Strng)

# ---- Post-processing options ----

# internal
def SaurashtraHaru(Strng):

    """Replaces specific Saurashtra consonant+virama+ha clusters with the dedicated haru (below-base h) sign."""
    ListC = '|'.join([Saurashtra.ConsonantMap[x] for x in [19,24,26,27]])
    vir = Saurashtra.ViramaMap[0]
    ha = Saurashtra.ConsonantMap[32]

    Strng = re.sub('('+ListC+')'+vir+ha,r'\1'+'\uA8B4',Strng)

    return Strng

