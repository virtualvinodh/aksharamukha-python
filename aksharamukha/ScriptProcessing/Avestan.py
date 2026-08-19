# -*- coding: utf-8 -*-

# Avestan's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.Roman import Avestan

def _FixAvestanEncode(Strng):
    """Applies Avestan orthographic fixes: aM/AM ligatures, ya/va to long ii/uu after vowels or consonants, and TTE/BHA/ZHA/NGVA/AO ligature substitutions."""
    extraCons = ["\U00010B33","\U00010B32","\U00010B1D","\U00010B12", '𐬣', '𐬝']
    ListC = "|".join(GM.CrunchSymbols(GM.Consonants, "Avestan")+extraCons)
    ListV = "|".join(GM.CrunchSymbols(GM.Vowels,"Avestan"))

    ya = Avestan.ConsonantMap[25]
    va = Avestan.ConsonantMap[28]
    ii = Avestan.VowelMap[2] * 2
    uu = Avestan.VowelMap[4] * 2

    Strng = Strng.replace('𐬀𐬩', '𐬄') ## aM
    Strng = Strng.replace('𐬁𐬩', '𐬅') ## AM

    Strng = re.sub("(("+ListV+")"+"|"+"("+ListC+"))"+"("+ya+")",r'\1'+ii,Strng)
    Strng = re.sub("(("+ListV+")"+"|"+"("+ListC+"))"+"("+va+")",r'\1'+uu,Strng)

    Strng = Strng.replace(Avestan.ConsonantMap[15]  + '\u02BF', '\U00010B1D') ## TTE
    Strng = Strng.replace(va + '\u02BF', '\U00010B21') # BHA

    Strng = Strng.replace('𐬰\u02BF', '𐬲').replace('𐬱\u02BF', '𐬲') ## ZHA
    Strng = Strng.replace('𐬢\u02BF','𐬤') ## NGVA
    Strng = Strng.replace('𐬁_𐬋', '𐬃') ## AO

    Strng = Strng.replace('\u02BF', '')




    return Strng

def _FixAvestanDecode(Strng):
    """Reverses Avestan orthographic fixes, expanding the aM/AM, ii/uu, and TTE/BHA/ZHA/NGVA/AO ligatures back into their component sequences."""
    extraCons = ["\U00010B33","\U00010B32","\U00010B1D","\U00010B12", '𐬣', '𐬝']
    ListC = "|".join(GM.CrunchSymbols(GM.Consonants, "Avestan")+extraCons)
    ListV = "|".join(GM.CrunchSymbols(GM.Vowels,"Avestan"))

    ya = Avestan.ConsonantMap[25]
    va = Avestan.ConsonantMap[28]
    ii = Avestan.VowelMap[2] * 2
    uu = Avestan.VowelMap[4] * 2

    Strng = Strng.replace('𐬄', '𐬀𐬩')
    Strng = Strng.replace('𐬅', '𐬁𐬩')

    Strng = Strng.replace(ii, ya).replace(uu, va)

    #print('I am here')

    Strng = Strng.replace('\U00010B1D', Avestan.ConsonantMap[15]  + '\u02BF')
    Strng = Strng.replace('𐬣', Avestan.ConsonantMap[4])

    Strng = Strng.replace('\U00010B12', Avestan.ConsonantMap[1])
    Strng = Strng.replace('\U00010B33', Avestan.ConsonantMap[29])
    Strng = Strng.replace('𐬡', va + '\u02BF')

    Strng = Strng.replace('𐬲', '𐬰\u02BF') ## ZHA
    Strng = Strng.replace('𐬤', '𐬢\u02BF') ## NGVA
    Strng = Strng.replace('𐬃', '𐬁_𐬋') ## AO

    ## 𐬲𐬤𐬃  approximate this

    ### Replave JHA + Nukta as ZHA in Devanagari & Gujarati

    return Strng

def FixAvestan(Strng, reverse=False):
    """Dispatches to the Avestan encode or decode fix routine depending on the reverse flag."""
    return _FixAvestanDecode(Strng) if reverse else _FixAvestanEncode(Strng)
