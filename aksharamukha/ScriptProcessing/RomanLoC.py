# -*- coding: utf-8 -*-

# Generic/shared LoC (Library of Congress) romanization logic that isn't
# exclusive to any one script - consolidated out of ConvertFix.py/
# PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this
# follows).
#
# RomanLoCChandrabindu is used by Telugu/Kannada/Malayalam/Sinhala/Oriya/
# Assamese/Bengali/Gujarati/Devanagari. KhandaTaRomanLoC is used by
# Assamese/Bengali. Both independently define the SAME option name in
# both PreProcess.py and PostProcess.py as genuinely different functions
# - suffixed _pre/_post here, same convention used everywhere else.

import re

# ---- Pre-processing options ----

def RomanLoCChandrabindu_pre(Strng):
    """Normalize candrabindu written as n̐ to m̐ for Library of Congress romanization."""
    Strng = re.sub('n̐', 'm̐', Strng)

    return Strng

def KhandaTaRomanLoC_pre(Strng):
    """Render Bengali khanda ta (ৎ) as ṯ in Library of Congress romanization."""
    Strng = Strng.replace('ৎ', 'ṯ')

    return Strng

def RomanLoCLaUnderscoreDoubleDot_pre(Strng):
    """Convert ḻ to l̤ (or back to ḻ) for Library of Congress romanization depending on direction; note: the forward variant (line 37) is missing its return statement, a likely bug."""
    Strng = Strng.replace('l̤', 'ḻ')

    return Strng

def RomanLoCSasha_pre(Strng):
    """Replace sh with ṣ for Library of Congress romanization."""
    Strng = Strng.replace('sh', 'ṣ')

    return Strng

def RomanLoCVaWa_pre(Strng):
    """Replace w with v for Library of Congress romanization, reflecting the va/wa merger."""
    Strng = Strng.replace('w', 'v')
    return Strng

# ---- Post-processing options ----

def LoCMarc8(Strng):
    """Decomposes combining diacritics into MARC-8-compatible NFD form and swaps the ring-above for a dot-above."""
    import unicodedata
    Strng = unicodedata.normalize('NFD', Strng)
    Strng = Strng.replace('\u02DA', '\u02D9')
    return Strng

def RomanLoCChandrabindu_post(Strng):
    #Strng = Strng.replace('ṁ', 'ṃ')

    """Converts chandrabindu-marked m before consonants into chandrabindu-marked n, per LoC romanization convention."""
    Strng = re.sub('(m̐)(k|g)', 'n̐' + r'\2', Strng)
    Strng = re.sub('(m̐)(c|j)', 'n̐' + r'\2', Strng)
    Strng = re.sub('(m̐)(ṭ|ḍ)', 'n̐' + r'\2', Strng)
    Strng = re.sub('(m̐)(t|d)', 'n̐' + r'\2', Strng)
    Strng = re.sub('(m̐)(p|b)', 'n̐' + r'\2', Strng)

    return Strng

def KhandaTaRomanLoC_post(Strng):
    """Converts LoC romanized t-line into the Bengali khanda ta letter."""
    Strng = Strng.replace('ṯ', 'ৎ')

    return Strng

def RomanLoCLaUnderscoreDoubleDot_post(Strng):
    """Replaces l-line-below with l-double-underdot, per LoC romanization convention."""
    Strng = Strng.replace('ḻ', 'l̤')

    return Strng

def RomanLoCSasha_post(Strng):
    """Replaces s-dot-below (sa) with sh, per LoC romanization convention."""
    Strng = Strng.replace('ṣ', 'sh')
    return Strng

def RomanLoCVaWa_post(Strng):
    """Replaces v with w, per LoC romanization convention for scripts where va is rendered as w."""
    Strng = Strng.replace('v', 'w')
    return Strng

