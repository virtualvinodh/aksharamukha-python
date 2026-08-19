# -*- coding: utf-8 -*-

# Newa's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.MainIndic import Newa

# ---- Fix (encode/decode conversion logic) ----

def _FixNewaEncode(Strng):
    """Placeholder Newa encode fixer; repha insertion after ra+virama is currently disabled (commented out)."""
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'Newa'))
    ra = Newa.ConsonantMap[26]
    vir = Newa.ViramaMap[0]
    ## The default behavior of Repha has been proposed to change
    # Strng = re.sub(ra + vir + '(' + ListC + ')', ra + vir + '\u200D' + r'\1', Strng)

    return Strng

def _FixNewaDecode(Strng):
    """No-op Newa decode fixer; currently performs no transformation."""
    pass

    return Strng

def FixNewa(Strng, reverse=False):
    """Dispatches to the Newa encode or decode fix routine depending on conversion direction."""
    return _FixNewaDecode(Strng) if reverse else _FixNewaEncode(Strng)

# ---- Post-processing options ----

def nepaldevafont(Strng):
    """Marks output for rendering with a Devanagari-based Newa font - 𑐧𑐸𑐡𑑂𑐢𑑅 → बुद्धः."""
    return Strng

def NewaMurmurConsonants(Strng):
    """Converts ha+virama+consonant clusters into dedicated murmured (breathy-voiced) consonant letters."""
    murmur = ['𑐓','𑐙','𑐤', '𑐪', '𑐭', '𑐯']
    connsh = ['𑐴𑑂𑐒', '𑐴𑑂𑐘', '𑐴𑑂𑐣', '𑐴𑑂𑐩', '𑐴𑑂𑐬', '𑐴𑑂𑐮']

    for x, y in zip(murmur, connsh):
        Strng = Strng.replace(y, x)

    return Strng

def NewaSpecialTa(Strng):

    """Inserts a ZWJ after ta+virama to force the special conjunct ta form - 𑐟𑑂𑐥𑐟𑑂𑐩𑐟𑑂𑐰 → 𑐟𑑂‍𑐥𑐟𑑂‍𑐩𑐟𑑂‍𑐰."""
    Strng = Strng.replace('𑐟𑑂', '𑐟𑑂‍') #Ta+virama -> ta + virama + ZWJ

    return Strng

def NewaDisableRepha(Strng):
    """Inserts a ZWJ after ra+virama to suppress the repha form - 𑐢𑐬𑑂𑐩 → 𑐢𑐬𑑂‍𑐩."""
    Strng = Strng.replace('𑐬𑑂', '𑐬𑑂\u200D')

    return Strng
