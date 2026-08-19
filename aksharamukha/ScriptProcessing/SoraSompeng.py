# -*- coding: utf-8 -*-

# SoraSompeng's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM

def _FixSoraSompengEncode(Strng):
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, 'SoraSompeng')) + ')'

    Strng = re.sub(ListC + '(ə)', r'\1', Strng)
    Strng = Strng.replace('ə', '\U000110E6\U000110E8')

    return Strng

def _FixSoraSompengDecode(Strng):
    ListC = "(" + "|".join(GM.CrunchSymbols(GM.Consonants, 'SoraSompeng')) + ')'

    ListV = "(" + "|".join(GM.CrunchSymbols(GM.Vowels, 'SoraSompeng')) + ')'
    Strng = re.sub(ListC + '(?!' + ListV + ')', r'\1' + 'ə', Strng)

    Strng = Strng.replace('𑃔ə𑃨', '𑃔𑃨ə')

    Strng = Strng.replace('𑃦𑃨', 'ə')
    Strng = Strng.replace('ə𑃨', '𑃨')

    return Strng

def FixSoraSompeng(Strng, reverse=False):
    return _FixSoraSompengDecode(Strng) if reverse else _FixSoraSompengEncode(Strng)
