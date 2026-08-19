# -*- coding: utf-8 -*-

# Rejang's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.EastIndic import Rejang

def _FixRejangEncode(Strng):
    vir = Rejang.ViramaMap[0]

    r = Rejang.ConsonantMap[26] + vir
    n = Rejang.ConsonantMap[19] + vir
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants + GM.Vowels + GM.VowelSignsNV,'Rejang'))

    Strng = re.sub('(' + ListC + ')' + r, r'\1' + '\uA951', Strng)
    Strng = re.sub('(' + ListC + ')' + n, r'\1' + '\uA950', Strng)

    return Strng

def _FixRejangDecode(Strng):
    vir = Rejang.ViramaMap[0]

    r = Rejang.ConsonantMap[26] + vir
    n = Rejang.ConsonantMap[19] + vir
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants + GM.Vowels + GM.VowelSignsNV,'Rejang'))

    # Reverse above
    Strng = Strng.replace('\uA951',r)
    Strng = Strng.replace('\uA950',n)

    return Strng

def FixRejang(Strng, reverse=False):
    return _FixRejangDecode(Strng) if reverse else _FixRejangEncode(Strng)
