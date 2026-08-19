# -*- coding: utf-8 -*-

# Hebr-Ar's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def gainGimel(Strng):
    """Marks Hebrew qof with a two-dot diacritic to represent Arabic gimel/ghayn, e.g. עׄ ← ג."""
    return Strng.replace('ק','ק̈')

def tavTwodot(Strng):
    """Adds a two-dot diacritic to tav to represent a variant Arabic letter, e.g. ת ← ת̈."""
    return Strng.replace('ת','ת̈')

def tavThreedot(Strng):
    """Converts a dotted tav into tav with a three-dot-above diacritic mark, e.g. תׄ ← ת֒."""
    return Strng.replace('תׄ','ת֒')
