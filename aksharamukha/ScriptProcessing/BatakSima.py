# -*- coding: utf-8 -*-

# BatakSima's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def _FixBatakSimaEncode(Strng):
    Strng = Strng.replace('ᯙᯮ', 'ᯙᯯ')

    return Strng

def _FixBatakSimaDecode(Strng):
    Strng = Strng.replace('ᯙᯯ', 'ᯙᯮ')

    return Strng

def FixBatakSima(Strng, reverse=False):
    return _FixBatakSimaDecode(Strng) if reverse else _FixBatakSimaEncode(Strng)
