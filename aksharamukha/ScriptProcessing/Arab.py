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

    """Applies Perso-Arabic punctuation normalization when encoding text into Arabic script."""
    from .. import ConvertFix as CF
    Strng = CF.PersoArabicPuntuation(Strng, False)
    pass
    #Strng = Strng.replace('â', 'ʾ')

    return Strng

def _FixArabDecode(Strng, Source):

    """Reverses Perso-Arabic punctuation, normalizes alef/tatweel, and reorders shadda-kasra when decoding from Arabic."""
    from .. import ConvertFix as CF
    Strng = CF.PersoArabicPuntuation(Strng, True)
    Strng = Strng.replace('آ', 'آ').replace('ـ', '')
    ## reverse shadda kasra
    Strng = Strng.replace('\u064E\u0651', '\u0651\u064E')

    return Strng

def FixArab(Strng, Source, reverse=False):

    """Dispatches to the Arabic encode or decode fix routine depending on conversion direction."""
    from .. import ConvertFix as CF
    return _FixArabDecode(Strng, Source) if reverse else _FixArabEncode(Strng, Source)

def ArabicGimelJa(Strng):

    """Represents /g/ using ڨ instead of jim ج - /ج/ as /g/."""
    from .. import ConvertFix as CF
    Strng = Strng.replace("ج", "ڨ")

    return Strng

def ArabRemoveAdditions(Strng):

    """Reverts extended Arabic letters back to their standard base forms: ڨ→ج, ڤ→ف, پ→ف."""
    from .. import ConvertFix as CF
    Strng = Strng.replace('ڨ', 'ج').replace('ڤ', 'ف').replace('پ', 'ف')

    return Strng

def arabicRemoveAdditionsPhonetic(Strng):

    """Maps extended phonetic letters to their nearest standard Arabic equivalents - /g j p b/ → /غ ج ب ب/ not /ج ج ف ب/."""
    from .. import ConvertFix as CF

    Strng = Strng.replace('ڨ', 'غ').replace('ڤ', 'ف').replace('پ', 'ب')

    return Strng

def ArabAtoAleph(Strng):

    """Converts hamza-carrying alif أ back to plain alif ا - أ/a/ to Alif /ا/."""
    from .. import ConvertFix as CF
    Strng = Strng.replace('أ', 'ا')


    return Strng
