# -*- coding: utf-8 -*-

# KhamtiShan's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from aksharamukha.ScriptMap.EastIndic import Burmese
from aksharamukha.ScriptMap.EastIndic import KhamtiShan

def _FixKhamtiShanEncode(Strng):
    """Converts virama+ra/ya/wa consonant sequences into Myanmar medial signs and reorders medial-sign combinations for Khamti Shan encoding."""
    Strng = Strng.replace('်ရ', 'ြ')
    Strng = Strng.replace('်ယ', 'ျ')
    Strng = Strng.replace('်ဝ', 'ွ')

    ## Maintain the order of the medials
    Strng = Strng.replace("\u103C\u103B", "\u103B\u103C")
    Strng = Strng.replace("\u103D\u103B", "\u103B\u103D")
    Strng = Strng.replace("ႂ\u103C", "\u103Cွ")

    return Strng

def _FixKhamtiShanDecode(Strng):
    """Reverses Khamti Shan medial sign conversions back into virama+ra/ya/wa consonant sequences."""
    Strng = Strng.replace('ꩳ', 'ရ')
    Strng = Strng.replace("\u103B\u103C", "\u103C\u103B")
    Strng = Strng.replace("\u103B\u103D", "\u103D\u103B")
    Strng = Strng.replace("\u103Cႂ", "ႂ\u103C")

    Strng = Strng.replace('ြ', '်ꩳ')
    Strng = Strng.replace('ꩳ', 'ရ')
    Strng = Strng.replace('ျ', '်ယ')
    Strng = Strng.replace('ွ', '်ဝ')

    return Strng

def FixKhamtiShan(Strng, reverse=False):
    """Dispatches to the Khamti Shan encode or decode fix-up routine based on the reverse flag."""
    return _FixKhamtiShanDecode(Strng) if reverse else _FixKhamtiShanEncode(Strng)

def KhamiShanMyanmarNumerals(Strng):
    """Converts Khamti Shan numerals into standard Myanmar/Burmese numerals, e.g. ႑႒႓ → ၁၂၃."""
    for x, y in zip(KhamtiShan.NumeralMap, Burmese.NumeralMap):
        Strng = Strng.replace(x, y)

    return Strng

def KhamtiShanRa(Strng):

    """Replaces the Khamti Shan letter ra (ရ) with the dedicated Khamti Shan ra glyph (ꩳ)."""
    Strng = Strng.replace('ရ', 'ꩳ')

    return Strng
