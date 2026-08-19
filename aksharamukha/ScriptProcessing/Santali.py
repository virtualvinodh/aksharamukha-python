# -*- coding: utf-8 -*-

# Santali's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def _FixSantaliEncode(Strng):
    Strng = Strng.replace('ᱹᱸ', 'ᱺ')
    Strng = Strng.replace('ᱻᱸ', 'ᱸᱻ')

    return Strng

def _FixSantaliDecode(Strng):
    Strng = Strng.replace('ᱺ', 'ᱹᱸ')
    Strng = Strng.replace('ᱽ','’')
    Strng = Strng.replace('ᱸᱻ', 'ᱻᱸ')

    return Strng

def FixSantali(Strng, reverse=False):
    return _FixSantaliDecode(Strng) if reverse else _FixSantaliEncode(Strng)
