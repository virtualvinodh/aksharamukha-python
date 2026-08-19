# -*- coding: utf-8 -*-

# Ugar's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def _FixUgarEncode(Strng, Source):
    Strng = Strng.replace("𐎒²","𐎝")
    Strng = Strng.replace(' ', '𐎟')

    return Strng

def _FixUgarDecode(Strng, Source):
    Strng = Strng.replace('𐎟', '')

    return Strng

def FixUgar(Strng, Source, reverse=False):
    return _FixUgarDecode(Strng, Source) if reverse else _FixUgarEncode(Strng, Source)
