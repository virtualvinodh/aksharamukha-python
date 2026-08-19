# -*- coding: utf-8 -*-

# GurmukhiLoC's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.MainIndic import Gurmukhi

def _FixGurmukhiLoCEncode(Strng):

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

def _FixGurmukhiLoCDecode(Strng):

    from .. import ConvertFix as CF

    from .. import PostProcess
    Strng = CF.CorrectRuLu(Strng,"Gurmukhi",True)

    ava = Gurmukhi.SignMap[0]
    avaA = '\u0028\u0A06\u0029'

    # Tippi/Bindu conversion options are optional. Look into PostProcess

    Strng = PostProcess.RetainIndicNumerals(Strng, 'Gurmukhi')
    Strng = Strng.replace(avaA,ava+ava)
    Strng = PostProcess.ReverseGeminationSign(Strng, 'Gurmukhi')
    #Strng = Strng.replace('ੰਨ','ਨ੍ਨ')
    #Strng = Strng.replace('ੰਮ','ਮ੍ਮ')
    # Replace Tippi by Bindu
    #Strng = PostProcess.GurmukhiYakaash(Strng, True)

    return Strng

def FixGurmukhiLoC(Strng,reverse=False):

    from .. import ConvertFix as CF

    from .. import PostProcess
    return _FixGurmukhiLoCDecode(Strng) if reverse else _FixGurmukhiLoCEncode(Strng)
