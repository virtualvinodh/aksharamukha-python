# -*- coding: utf-8 -*-

# Bhaiksuki's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixBhaiksukiEncode(Strng):
    """Replaces the plain ASCII space with the Bhaiksuki word-divider punctuation mark."""
    Strng = Strng.replace(' ', '𑱃')

    return Strng

# internal
def _FixBhaiksukiDecode(Strng):
    """Replaces the Bhaiksuki word-divider punctuation mark with a plain ASCII space."""
    Strng = Strng.replace('𑱃', ' ')

    return Strng

# internal
def FixBhaiksuki(Strng, reverse=False):
    """Dispatches to the Bhaiksuki encode or decode fix routine depending on the reverse flag."""
    return _FixBhaiksukiDecode(Strng) if reverse else _FixBhaiksukiEncode(Strng)

# ---- Post-processing options ----

# frontend
def BhaiksukiRetainSpace(Strng):
    """Retains spaces in Bhaiksuki text by converting the word-divider mark back to a plain space."""
    Strng = Strng.replace('𑱃', ' ')

    return Strng
