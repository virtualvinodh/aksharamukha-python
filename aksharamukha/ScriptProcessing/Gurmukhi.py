# -*- coding: utf-8 -*-

# Gurmukhi's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.MainIndic import Gurmukhi

# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixGurmukhiEncode(Strng):

    """Applies Gurmukhi encoding fixes: RU/LU vowel correction, doubled Aunkar to bracketed AA, gemination-sign insertion, Indic-numeral retention, and Vedic svara consonant doubling."""
    from .. import ConvertFix as CF

    from .. import PostProcess
    Strng = CF.CorrectRuLu(Strng,"Gurmukhi",False)

    ava = Gurmukhi.SignMap[0]
    avaA = '\u0028\u0A06\u0029'

    # Tippi/Bindu conversion options are optional. Look into PostProcess

    Strng = Strng.replace(ava+ava,avaA)
    Strng = PostProcess.InsertGeminationSign(Strng, 'Gurmukhi')
    Strng = PostProcess.RetainIndicNumerals(Strng, 'Gurmukhi', True)

    Vedicomp = '([' + ''.join(GM.VedicSvarasList) + '])'

    Strng = re.sub(Vedicomp + '\u0A71' + '(.)', r'\1' + r'\2' + Gurmukhi.ViramaMap[0] + r'\2' , Strng)


    return Strng

# internal
def _FixGurmukhiDecode(Strng):

    """Reverses Gurmukhi encoding fixes: RU/LU vowel correction, Indic numerals, gemination sign, nn/mm-halant normalization, Tippi-to-Bindu, and Yakaash conjuncts."""
    from .. import ConvertFix as CF

    from .. import PostProcess
    Strng = CF.CorrectRuLu(Strng,"Gurmukhi",True)

    ava = Gurmukhi.SignMap[0]
    avaA = '\u0028\u0A06\u0029'

    # Tippi/Bindu conversion options are optional. Look into PostProcess

    Strng = PostProcess.RetainIndicNumerals(Strng, 'Gurmukhi')
    Strng = Strng.replace(avaA,ava+ava)
    Strng = PostProcess.ReverseGeminationSign(Strng, 'Gurmukhi')
    Strng = Strng.replace('ੰਨ','ਨ੍ਨ')
    Strng = Strng.replace('ੰਮ','ਮ੍ਮ')
    # Replace Tippi by Bindu
    Strng = Strng.replace('\u0A70','\u0A02')
    Strng = PostProcess.GurmukhiYakaash(Strng, True)

    return Strng

# internal
def FixGurmukhi(Strng,reverse=False):

    """Dispatches to the Gurmukhi encode or decode fix routine depending on the reverse flag."""

    return _FixGurmukhiDecode(Strng) if reverse else _FixGurmukhiEncode(Strng)

# ---- Pre-processing options ----

# frontend
def SchwaFinalGurmukhi(Strng):

    """Deletes the schwa only in word-final position: ਰਾਮ → rām."""

    from .. import PreProcess as PP

    Strng = PP.RemoveFinal(Strng, 'Gurmukhi')

    return Strng

# ---- Post-processing options ----

# internal
def GurmukhiCandrabindu(Strng):

    """Replaces the Gurmukhi candrabindu sign (ਁ) with anusvara (ਂ), since Gurmukhi does not distinguish them."""

    Strng = Strng.replace('ਁ', 'ਂ')

    return Strng

# frontend
def GurmukhiYakaash(Strng, reverse=False):

    """Applies (or reverses) the Yakaash ligature: ਕ੍ਯ → ਕੵ."""

    if not reverse:
        Strng = Strng.replace('੍ਯ','ੵ')
    else:
        Strng = Strng.replace('ੵ', '੍ਯ')

    return Strng

# internal
def GurmukhiTippiBindu(Strng): # Check this Function
    """Converts Gurmukhi Bindu (ਂ) to Tippi (ੰ) after specific consonants, vowels, and vowel signs where Tippi is conventional."""
    Bindi = Gurmukhi.AyogavahaMap[1];
    Tippi = '\u0A70'
    ListTippi = '|'.join(GM.CrunchSymbols(GM.Consonants, 'Gurmukhi')+[Gurmukhi.VowelMap[x] for x in [0,2,4]]
        +[Gurmukhi.VowelSignMap[1]]+[Gurmukhi.VowelSignMap[3]]+[Gurmukhi.VowelSignMap[4]])

    Char = '|'.join(GM.CrunchSymbols(GM.Consonants, 'Gurmukhi') + GM.CrunchSymbols(GM.Vowels, 'Gurmukhi'))

    Strng = re.sub('(' + Gurmukhi.VowelSignMap[4] +')' + Bindi + '(?!'+ Char + ')',  r'\1' + Tippi, Strng)

    # Strng = '(' + Gurmukhi.VowelSignMap[4] +')' + Bindi + '(=!'+ Char + ')'

    Strng = re.sub('('+ListTippi+')'+'('+Bindi+')',r'\1'+Tippi, Strng)

    return Strng

# internal
def GurmukhiTippiGemination(Strng):

    """Replaces the Addak gemination mark (ੱ) with Tippi before ਨ or ਮ, reflecting pronunciation of geminated nasals."""

    n = Gurmukhi.ConsonantMap[19]
    m = Gurmukhi.ConsonantMap[24]
    vir = Gurmukhi.ViramaMap[0]
    Addak = 'ੱ'
    Tippi = '\u0A70'

    #print(Strng)

    Strng = Strng.replace(Addak + m , Tippi + m)
    Strng = Strng.replace(Addak + n, Tippi + n)

    #print(Strng)

    return Strng
