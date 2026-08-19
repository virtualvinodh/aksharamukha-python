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

def _FixGurmukhiEncode(Strng):

    from .. import ConvertFix as CF

    from .. import PreProcess as PP

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

def _FixGurmukhiDecode(Strng):

    from .. import ConvertFix as CF

    from .. import PreProcess as PP

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

def FixGurmukhi(Strng,reverse=False):

    from .. import ConvertFix as CF

    from .. import PreProcess as PP

    from .. import PostProcess
    return _FixGurmukhiDecode(Strng) if reverse else _FixGurmukhiEncode(Strng)

def SchwaFinalGurmukhi(Strng):

    from .. import ConvertFix as CF

    from .. import PreProcess as PP

    from .. import PostProcess

    Strng = PP.RemoveFinal(Strng, 'Gurmukhi')

    return Strng

def GurmukhiCandrabindu(Strng):

    from .. import ConvertFix as CF

    from .. import PreProcess as PP

    from .. import PostProcess
    Strng = Strng.replace('ਁ', 'ਂ')

    return Strng

def GurmukhiYakaash(Strng, reverse=False):

    from .. import ConvertFix as CF

    from .. import PreProcess as PP

    from .. import PostProcess
    if not reverse:
        Strng = Strng.replace('੍ਯ','ੵ')
    else:
        Strng = Strng.replace('ੵ', '੍ਯ')

    return Strng

def GurmukhiTippiBindu(Strng): # Check this Function
    Bindi = Gurmukhi.AyogavahaMap[1];
    Tippi = '\u0A70'
    ListTippi = '|'.join(GM.CrunchSymbols(GM.Consonants, 'Gurmukhi')+[Gurmukhi.VowelMap[x] for x in [0,2,4]]
        +[Gurmukhi.VowelSignMap[1]]+[Gurmukhi.VowelSignMap[3]]+[Gurmukhi.VowelSignMap[4]])

    Char = '|'.join(GM.CrunchSymbols(GM.Consonants, 'Gurmukhi') + GM.CrunchSymbols(GM.Vowels, 'Gurmukhi'))

    Strng = re.sub('(' + Gurmukhi.VowelSignMap[4] +')' + Bindi + '(?!'+ Char + ')',  r'\1' + Tippi, Strng)

    # Strng = '(' + Gurmukhi.VowelSignMap[4] +')' + Bindi + '(=!'+ Char + ')'

    Strng = re.sub('('+ListTippi+')'+'('+Bindi+')',r'\1'+Tippi, Strng)

    return Strng

def GurmukhiTippiGemination(Strng):

    from .. import ConvertFix as CF

    from .. import PreProcess as PP

    from .. import PostProcess
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
