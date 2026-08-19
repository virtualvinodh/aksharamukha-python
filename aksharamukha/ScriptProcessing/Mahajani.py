# -*- coding: utf-8 -*-

# Mahajani's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def _FixMahajaniEncode(Strng):
    Strng = Strng.replace('𑅰𑅳ʾ𑅭ʿ𑅑', '\U00011176')
    Strng = Strng.replace('\u02BE','').replace('\u02BF','')

    return Strng

def _FixMahajaniDecode(Strng):
    Strng = Strng.replace('\U00011176', '𑅰𑅳ʾ𑅭ʿ𑅑')

    return Strng

def FixMahajani(Strng, reverse=False):
    return _FixMahajaniDecode(Strng) if reverse else _FixMahajaniEncode(Strng)
