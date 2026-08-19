# -*- coding: utf-8 -*-

# Saurashtra's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def _FixSaurashtraEncode(Strng):
    Strng = Strng.replace('ꢒ꣄ꢰ', 'ꢒ꣄‍ꢰ') # Ksha

    return Strng

def _FixSaurashtraDecode(Strng):
    Strng = Strng.replace('ꢴ','꣄ꢲ')

    return Strng

def FixSaurashtra(Strng, reverse=False):
    return _FixSaurashtraDecode(Strng) if reverse else _FixSaurashtraEncode(Strng)
