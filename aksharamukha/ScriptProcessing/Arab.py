# -*- coding: utf-8 -*-

# Arab's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re

def _FixArabEncode(Strng, Source):

    from .. import ConvertFix as CF
    Strng = CF.PersoArabicPuntuation(Strng, False)
    pass
    #Strng = Strng.replace('â', 'ʾ')

    return Strng

def _FixArabDecode(Strng, Source):

    from .. import ConvertFix as CF
    Strng = CF.PersoArabicPuntuation(Strng, True)
    Strng = Strng.replace('آ', 'آ').replace('ـ', '')
    ## reverse shadda kasra
    Strng = Strng.replace('\u064E\u0651', '\u0651\u064E')

    return Strng

def FixArab(Strng, Source, reverse=False):

    from .. import ConvertFix as CF
    return _FixArabDecode(Strng, Source) if reverse else _FixArabEncode(Strng, Source)

def ArabicGimelJa(Strng):

    from .. import ConvertFix as CF
    Strng = Strng.replace("ج", "ڨ")

    return Strng

def ArabRemoveAdditions(Strng):

    from .. import ConvertFix as CF
    Strng = Strng.replace('ڨ', 'ج').replace('ڤ', 'ف').replace('پ', 'ف')

    return Strng

def arabicRemoveAdditionsPhonetic(Strng):

    from .. import ConvertFix as CF

    Strng = Strng.replace('ڨ', 'غ').replace('ڤ', 'ف').replace('پ', 'ب')

    return Strng

def ArabAtoAleph(Strng):

    from .. import ConvertFix as CF
    Strng = Strng.replace('أ', 'ا')


    return Strng
