# -*- coding: utf-8 -*-

# Kaithi's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def _FixKaithiEncode(Strng):
    Strng = Strng.replace(' ', '⸱')

    return Strng

def _FixKaithiDecode(Strng):
    Strng = Strng.replace("⸱",' ')
    # Strng = re.sub('', '', Strng)

    return Strng

def FixKaithi(Strng, reverse=False):
    return _FixKaithiDecode(Strng) if reverse else _FixKaithiEncode(Strng)

def KaithiRetainSpace(Strng):
    Strng = Strng.replace('⸱', ' ')

    return Strng
