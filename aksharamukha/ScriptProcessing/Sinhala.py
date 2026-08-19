# -*- coding: utf-8 -*-

# Sinhala's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# SinhalaPali independently defines the SAME option name in both
# PreProcess.py and PostProcess.py, but unlike the other collisions in
# this batch it was never two independent implementations -
# PreProcess.SinhalaPali always just called
# PostProcess.SinhalaPali(Strng, reverse=True). Kept that relationship,
# now as a direct same-file call (SinhalaPali_pre -> SinhalaPali_post)
# instead of a cross-module one. SinhalaDefaultConjuncts had zero
# remaining callers elsewhere in PostProcess.py once Sinhala's own Fix
# functions (its only callers) moved here too - absorbed rather than
# left behind pointlessly qualified.
# RetainIndicNumerals stays shared (used by many scripts), called via
# PostProcess. as before.

import re
from aksharamukha.ScriptMap.MainIndic import Sinhala

# ---- Fix (encode/decode conversion logic) ----

def _FixSinhalaEncode(Strng):
    """Forms default Sinhala conjuncts, retains native numerals, and merges the ja-nya conjunct and doubled-a (ආ) notation."""
    from .. import PostProcess
    Strng = SinhalaDefaultConjuncts(Strng)

    Strng = PostProcess.RetainIndicNumerals(Strng, 'Sinhala', True)
    #Sinhala JNA
    Strng = Strng.replace("\u0DA2\u0DCA\u0DA4","\u0DA5")
    #sinhala
    Strng = Strng.replace("(අ)(අ)","(ආ)")


    return Strng

def _FixSinhalaDecode(Strng):
    """Reverses Sinhala conjunct formation, numeral retention, the ja-nya conjunct, and doubled-a notation, and strips ZWJ joiners."""
    from .. import PostProcess
    Strng = SinhalaDefaultConjuncts(Strng)

    #sinhala numerals
    Strng = PostProcess.RetainIndicNumerals(Strng, 'Sinhala')
    Strng = Strng.replace("\u0DA5","\u0DA2\u0DCA\u0DA4")
    ## Remove joiners
    Strng = Strng.replace("‍","")
    Strng = Strng.replace("(ආ)","(අ)(අ)")


    return Strng

def FixSinhala(Strng, reverse=False):
    """Dispatches to the Sinhala encode or decode fix-up routine based on the reverse flag."""
    return _FixSinhalaDecode(Strng) if reverse else _FixSinhalaEncode(Strng)

# ---- Pre-processing options ----

def SinhalaPali_pre(Strng):
    """Pre-converts Southern short e/o vowel forms to standard Sinhala long vowel forms before processing Pali text."""
    Strng = SinhalaPali_post(Strng, reverse=True)

    return Strng

# ---- Post-processing options ----

def SinhalaDefaultConjuncts(Strng):
    """Inserts ZWJ to form default Sinhala consonant conjuncts before ya/ra and other special consonant clusters."""
    vir = Sinhala.ViramaMap[0]
    YR = '|'.join(Sinhala.ConsonantMap[25:27])

    Strng = re.sub('('+vir+')'+'('+YR+')',r'\1'+'\u200D'+r'\2',Strng)
    Strng = re.sub('('+YR[2]+')'+'('+vir+')'+'('+'\u200D'+')'+'('+YR[0]+')',r'\1\3\2\3\4',Strng)

    Strng = Strng.replace(Sinhala.ConsonantMap[7]+Sinhala.ViramaMap[0]+Sinhala.ConsonantMap[9],'\u0DA5')
    Strng = Strng.replace(Sinhala.ConsonantMap[0]+vir+Sinhala.ConsonantMap[30],Sinhala.ConsonantMap[0]+vir+'\u200D'+Sinhala.ConsonantMap[30])

    ## KSHA

    Strng = Strng.replace('ර‍්‍ය', 'ර්ය')
    Strng = Strng.replace('ර්‍ර', 'ර්ර')

    return Strng

def SinhalaPali_post(Strng, reverse = False):
    """Swaps Sinhala long e/o vowel forms with the Southern short-vowel equivalents used for Pali, or reverses the swap."""
    EOLong = Sinhala.VowelMap[10:11]+Sinhala.VowelMap[12:13]+Sinhala.VowelSignMap[9:10]+Sinhala.VowelSignMap[11:12]
    EOShort = Sinhala.SouthVowelMap+Sinhala.SouthVowelSignMap

    for x,y in zip(EOLong,EOShort):
        if not reverse:
            Strng = Strng.replace(x,y)
        else:
            Strng = Strng.replace(y,x)

    return Strng

def SinhalaConjuncts(Strng):
    """Enables full Sinhala conjunct formation by inserting ZWJ between all consonant clusters, e.g. බුද්ධස්ස → බුද්‍ධස‍්ස."""
    ListC = Sinhala.ConsonantMap + [Sinhala.SouthConsonantMap[0]]
    vir = Sinhala.ViramaMap[0]
    ZWJ ="\u200D"

    conjoining =[(0, 28), (2, 18), (9, 5), (10, 11), (15, 16), (15, 28), (17, 18), (17, 28), (19, 16), (19, 17), (19, 18), (19, 28) ]

    for x, y in conjoining:
        Strng = Strng.replace(ListC[x] + vir + ListC[y], ListC[x] + vir + ZWJ + ListC[y])

    for x in ListC:
        Strng = Strng.replace(ListC[26] + vir + x, ListC[26] + vir + ZWJ + x)

    for x in ListC:
        for y in ListC:
            Strng = Strng.replace(x + vir + y, x + ZWJ + vir + y)

    Strng = Strng.replace('ර‍්‍ය', 'ර්‍ය')

    return Strng

def SinhalaChandrbinduAnusvara(Strng):
    """Converts the Sinhala chandrabindu sign into the anusvara sign."""
    Strng = Strng.replace('\u0D81', '\u0D82')

    return Strng
