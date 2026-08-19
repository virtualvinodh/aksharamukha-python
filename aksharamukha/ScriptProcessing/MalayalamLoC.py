# -*- coding: utf-8 -*-

# Malayalam's LoC (Library of Congress) romanization logic, consolidated
# out of PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this
# follows).
#
# MalayalamRomanLoCFix independently defines the SAME option name in
# both PreProcess.py and PostProcess.py as genuinely different functions
# - suffixed _pre/_post here, same convention used everywhere else.
# mDotBelowToAbove is post-only (no pre-option counterpart), so it stays
# unsuffixed.

# ---- Pre-processing options ----

def MalayalamRomanLoCFix_pre(Strng):
    """Normalize ṯṯ to ṟṟ and ȧ to ŭ in Malayalam Library of Congress romanization."""
    Strng = Strng.replace('ṯṯ', 'ṟṟ')
    Strng = Strng.replace('ȧ', 'ŭ')
    return Strng

# ---- Post-processing options ----

def MalayalamRomanLoCFix_post(Strng):
    """Fixes Malayalam LoC romanization: doubled r-line -> doubled t-line, u-breve -> a-overdot."""
    Strng = Strng.replace('ṟṟ', 'ṯṯ')
    Strng = Strng.replace('ŭ', 'ȧ')
    return Strng

def mDotBelowToAbove(Strng):
    """Converts dot-above anusvara back to dot-below (inverse of mDotAboveToBelow)."""
    Strng = Strng.replace('ṁ', 'ṃ')

    return Strng
