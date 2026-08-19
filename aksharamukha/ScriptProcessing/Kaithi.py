# -*- coding: utf-8 -*-

# Kaithi's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def _FixKaithiEncode(Strng):
    """Replaces spaces with the Kaithi word separator ⸱ when encoding."""
    Strng = Strng.replace(' ', '⸱')

    return Strng

def _FixKaithiDecode(Strng):
    """Replaces the Kaithi word separator ⸱ with a space when decoding."""
    Strng = Strng.replace("⸱",' ')
    # Strng = re.sub('', '', Strng)

    return Strng

def FixKaithi(Strng, reverse=False):
    """Dispatches to the Kaithi encode or decode fix routine depending on conversion direction."""
    return _FixKaithiDecode(Strng) if reverse else _FixKaithiEncode(Strng)

def KaithiRetainSpace(Strng):
    """Restores plain spaces in place of the Kaithi word separator ⸱."""
    Strng = Strng.replace('⸱', ' ')

    return Strng
