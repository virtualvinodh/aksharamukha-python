# -*- coding: utf-8 -*-

# Bhaiksuki's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def _FixBhaiksukiEncode(Strng):
    Strng = Strng.replace(' ', '𑱃')

    return Strng

def _FixBhaiksukiDecode(Strng):
    Strng = Strng.replace('𑱃', ' ')

    return Strng

def FixBhaiksuki(Strng, reverse=False):
    return _FixBhaiksukiDecode(Strng) if reverse else _FixBhaiksukiEncode(Strng)

def BhaiksukiRetainSpace(Strng):
    Strng = Strng.replace('𑱃', ' ')

    return Strng
