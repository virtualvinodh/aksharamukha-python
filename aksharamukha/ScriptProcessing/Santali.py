# -*- coding: utf-8 -*-

# Santali's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

# ---- Fix (encode/decode conversion logic) ----

def _FixSantaliEncode(Strng):
    """Ligates the Santali vowel-modifier+ahad sign combination into its dedicated letter and reorders the gaahlaa+ahad sequence."""
    Strng = Strng.replace('ᱹᱸ', 'ᱺ')
    Strng = Strng.replace('ᱻᱸ', 'ᱸᱻ')

    return Strng

def _FixSantaliDecode(Strng):
    """Expands the dedicated Santali ligature back to its component signs, maps the gitit sign to an apostrophe, and restores original ahad/gaahlaa order."""
    Strng = Strng.replace('ᱺ', 'ᱹᱸ')
    Strng = Strng.replace('ᱽ','’')
    Strng = Strng.replace('ᱸᱻ', 'ᱻᱸ')

    return Strng

def FixSantali(Strng, reverse=False):
    """Dispatches to the Santali encode or decode fix routine depending on conversion direction."""
    return _FixSantaliDecode(Strng) if reverse else _FixSantaliEncode(Strng)
