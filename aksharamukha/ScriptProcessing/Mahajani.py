# -*- coding: utf-8 -*-

# Mahajani's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

# ---- Fix (encode/decode conversion logic) ----

def _FixMahajaniEncode(Strng):
    """Converts the multi-character Mahajani rupee-sign sequence into its single Unicode ligature and strips joiner marks."""
    Strng = Strng.replace('𑅰𑅳ʾ𑅭ʿ𑅑', '\U00011176')
    Strng = Strng.replace('\u02BE','').replace('\u02BF','')

    return Strng

def _FixMahajaniDecode(Strng):
    """Expands the Mahajani rupee-sign Unicode ligature back into its multi-character component sequence."""
    Strng = Strng.replace('\U00011176', '𑅰𑅳ʾ𑅭ʿ𑅑')

    return Strng

def FixMahajani(Strng, reverse=False):
    """Dispatches to the Mahajani encode or decode fix routine depending on the reverse flag."""
    return _FixMahajaniDecode(Strng) if reverse else _FixMahajaniEncode(Strng)
