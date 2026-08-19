# -*- coding: utf-8 -*-

# SoraSompeng's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM

# ---- Fix (encode/decode conversion logic) ----

def _FixSoraSompengEncode(Strng):
    """Drops the inherent schwa marker after consonants and expands a standalone schwa into its full vowel-letter sequence when encoding into Sora Sompeng."""
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, 'SoraSompeng')) + ')'

    Strng = re.sub(ListC + '(ə)', r'\1', Strng)
    Strng = Strng.replace('ə', '\U000110E6\U000110E8')

    return Strng

def _FixSoraSompengDecode(Strng):
    """Inserts an inherent schwa after consonants not followed by a vowel and collapses specific consonant+schwa+vowel-length sequences when decoding out of Sora Sompeng."""
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, 'SoraSompeng')) + ')'

    ListV = "(" + "|".join(GM.CrunchSymbols(GM.Vowels, 'SoraSompeng')) + ')'
    Strng = re.sub(ListC + '(?!' + ListV + ')', r'\1' + 'ə', Strng)

    Strng = Strng.replace('𑃔ə𑃨', '𑃔𑃨ə')

    Strng = Strng.replace('𑃦𑃨', 'ə')
    Strng = Strng.replace('ə𑃨', '𑃨')

    return Strng

def FixSoraSompeng(Strng, reverse=False):
    """Dispatches to the Sora Sompeng encode or decode fix routine based on the reverse flag."""
    return _FixSoraSompengDecode(Strng) if reverse else _FixSoraSompengEncode(Strng)
