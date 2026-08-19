# -*- coding: utf-8 -*-

# TaiLaing's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def _FixTaiLaingEncode(Strng):
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
    Strng = Strng.replace("\u103B\u103C", "\u103C\u103B")
    Strng = Strng.replace("\u103B\u103D", "\u103D\u103B")
    Strng = Strng.replace("\u103Cႂ", "ႂ\u103C")

    Strng = Strng.replace('ြ', '်ꩺ')
    Strng = Strng.replace('ျ', '်ယ')
    Strng = Strng.replace('ႂ', '်ဝ')

    return Strng

def FixTaiLaing(Strng, reverse=False):
    return _FixTaiLaingDecode(Strng) if reverse else _FixTaiLaingEncode(Strng)
