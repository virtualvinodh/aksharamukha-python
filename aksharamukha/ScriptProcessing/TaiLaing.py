# -*- coding: utf-8 -*-

# TaiLaing's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

# ---- Fix (encode/decode conversion logic) ----

def _FixTaiLaingEncode(Strng):
    """Converts virama+medial ra/ya/wa sequences into their dedicated Tai Laing medial signs and reorders medial-sign combinations to the correct rendering order."""
    Strng = Strng.replace('်ꩺ', 'ြ')
    Strng = Strng.replace('်ယ', 'ျ')
    Strng = Strng.replace('်ဝ', 'ႂ')

    ## Maintain the order of the medials
    Strng = Strng.replace("\u103C\u103B", "\u103B\u103C")
    Strng = Strng.replace("\u103D\u103B", "\u103B\u103D")
    Strng = Strng.replace("ႂ\u103C", "\u103Cႂ")

    Strng = Strng.replace('ႂျ','်၀ျ')


    return Strng

def _FixTaiLaingDecode(Strng):
    """Reverses medial-sign ordering and expands the Tai Laing medial ra/ya/wa signs back to virama+consonant sequences."""
    Strng = Strng.replace("\u103B\u103C", "\u103C\u103B")
    Strng = Strng.replace("\u103B\u103D", "\u103D\u103B")
    Strng = Strng.replace("\u103Cႂ", "ႂ\u103C")

    Strng = Strng.replace('ြ', '်ꩺ')
    Strng = Strng.replace('ျ', '်ယ')
    Strng = Strng.replace('ႂ', '်ဝ')

    return Strng

def FixTaiLaing(Strng, reverse=False):
    """Dispatches to the Tai Laing encode or decode fix routine depending on conversion direction."""
    return _FixTaiLaingDecode(Strng) if reverse else _FixTaiLaingEncode(Strng)
