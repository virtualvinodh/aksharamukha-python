# -*- coding: utf-8 -*-

# Malayalam's LoC (Library of Congress) romanization logic, consolidated
# out of PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this
# follows).
#
# MalayalamRomanLoCFix_pre/_post and mDotBelowToAbove were all part of
# the auto-applied RomanLoC default bundle (never independently
# selectable elsewhere) - now purely internal, called only from
# RomanLocToMalayalamPre/MalayalamToRomanLocPost below, no longer
# independently re-exported. See ScriptProcessing/HOW_TO_ADD_LOC.md for
# the naming convention this follows and how to add a new script.

def MalayalamRomanLoCFix_pre(Strng):
    """Normalize ṯṯ to ṟṟ and ȧ to ŭ in Malayalam Library of Congress romanization."""
    Strng = Strng.replace('ṯṯ', 'ṟṟ')
    Strng = Strng.replace('ȧ', 'ŭ')
    return Strng

def MalayalamRomanLoCFix_post(Strng):
    """Fixes Malayalam LoC romanization: doubled r-line -> doubled t-line, u-breve -> a-overdot."""
    Strng = Strng.replace('ṟṟ', 'ṯṯ')
    Strng = Strng.replace('ŭ', 'ȧ')
    return Strng

def mDotBelowToAbove(Strng):
    """Converts dot-above anusvara back to dot-below (inverse of mDotAboveToBelow)."""
    Strng = Strng.replace('ṁ', 'ṃ')

    return Strng

# ---- Pre-processing options ----

def RomanLocToMalayalamPre(Strng):
    """Applies candrabindu and Malayalam-specific LoC fixes before converting LoC Roman text to Malayalam."""
    from .RomanLoC import RomanLoCChandrabindu_pre
    Strng = RomanLoCChandrabindu_pre(Strng)
    Strng = MalayalamRomanLoCFix_pre(Strng)

    return Strng

# ---- Post-processing options ----

def MalayalamToRomanLocPost(Strng):
    """Applies anusvara-to-nasal, candrabindu, Malayalam-specific, and dot-placement LoC fixes after converting Malayalam to LoC Roman."""
    from .RomanLoC import RomanLoCChandrabindu_post
    from .. import PostProcess
    Strng = PostProcess.AnusvaratoNasalASTISO(Strng)
    Strng = RomanLoCChandrabindu_post(Strng)
    Strng = MalayalamRomanLoCFix_post(Strng)
    Strng = mDotBelowToAbove(Strng)

    return Strng
