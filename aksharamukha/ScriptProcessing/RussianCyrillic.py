# -*- coding: utf-8 -*-

# RussianCyrillic's own Fix/pre-option/post-option logic, consolidated out
# of ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# CyrillicPali independently defines the SAME option name in both
# PreProcess.py and PostProcess.py as two different functions - suffixed
# _pre/_post here, aliased back on re-export (see ScriptProcessing/
# DevanagariLimbu.py for the first script this pattern was used on).

import re

# ---- Pre-processing options ----

def CyrillicPali_pre(Strng):
    """Swaps the Cyrillic Pali l-with-dot-below diacritic (л̣) to a distinct combining form (л̤) before conversion."""
    Strng = Strng.replace('л̣', 'л̤',)

    return Strng

# ---- Post-processing options ----

def CyrillicPali_post(Strng):
    """Reverses the Cyrillic Pali l diacritic swap, л̤ → л̣, after conversion."""
    Strng = Strng.replace('л̤', 'л̣')

    return Strng

def removeDiacritics(Strng):
    """Strips combining diacritics from Cyrillic transliteration and simplifies long-vowel digraphs to base letters, e.g. сам̣кр̣там̣ → самкртам."""
    diacritics = ['\u0331', '\u0306', '\u0323', '\u035F', '\u0324', '\u035F', '\u0307', '\u0301', '\u0303', '\u0310', '\u0306', '\u0302', '\u0304']

    for dia in diacritics:
        Strng = Strng.replace(dia, '')

    vowelDia = ['а̄', 'ӣ', 'ӯ', 'ӗ']
    vowel = ['\u0430', '\u0438', '\u0443', '\u044D']

    for x, y in zip(vowelDia, vowel):
        Strng = Strng.replace(x, y)

    return Strng
