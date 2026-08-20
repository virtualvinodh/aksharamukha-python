# -*- coding: utf-8 -*-

# Devanagari's LoC (Library of Congress) romanization logic. See
# ScriptProcessing/HOW_TO_ADD_LOC.md for the naming convention this
# follows and how to add a new script. Renamed from RomanLoCDevanagari.py
# for consistency with the rest of ScriptProcessing/ (one file per
# script, <Script>LoC.py).
#
# HindiMarathiRomanLoCFix_pre/_post is a genuinely standalone option
# (never part of the auto-applied RomanLoC default bundle) - still
# independently re-exported under its own unsuffixed name, same as
# before. DevanagariRomanLoCFix_pre/_post, by contrast, WAS part of the
# default bundle - it's now purely internal, called only from
# RomanLocToDevanagariPre/DevanagariToRomanLocPost below, no longer
# independently re-exported.

import re

# frontend
def HindiMarathiRomanLoCFix_pre(Strng):
    """Substitutes 'sh'→ṣ, ḷ→ḻ, and l̤→l̳ before Hindi/Marathi Library of Congress romanization."""
    Strng = Strng.replace('sh', 'ṣ')
    Strng = Strng.replace('ḷ', 'ḻ')
    Strng = Strng.replace('l̤', 'l̳')

    return Strng

# internal
def DevanagariRomanLoCFix_pre(Strng):
    """Normalize nukta-marked digraphs (g̳h̳, t̤, s̤, h̤) to their LoC diacritic forms for Devanagari romanization."""
    Strng = Strng.replace('g̳h̳', 'gḧ').replace('t̤', 'ṭ̈').replace('s̤', 's̈')\
        .replace('h̤', 'ḧ')

    return Strng

# frontend
def HindiMarathiRomanLoCFix_post(Strng):
    """Reverses the Hindi/Marathi LoC substitutions: ṣ→'sh', ḻ→ḷ, l̳→l̤."""
    Strng = Strng.replace('ṣ', 'sh')
    Strng = Strng.replace('ḻ', 'ḷ')
    Strng = Strng.replace('l̳', 'l̤')

    return Strng

# internal
def DevanagariRomanLoCFix_post(Strng):
    """Fixes Devanagari LoC romanization diaeresis-marked digraphs: g-h-diaeresis -> g-underdot h-underdot, t-diaeresis -> t-underdot, s-diaeresis -> s-underdot, h-diaeresis -> h-underdot."""
    Strng = Strng.replace('gḧ', 'g̳h̳').replace('ṭ̈', 't̤').replace('s̈', 's̤')\
        .replace('ḧ', 'h̤')

    return Strng

# ---- Pre-processing options ----

# internal
def RomanLocToDevanagariPre(Strng):
    """Applies candrabindu and nukta-digraph LoC fixes before converting LoC Roman text to Devanagari."""
    from .RomanLoC import RomanLoCChandrabindu_pre
    Strng = RomanLoCChandrabindu_pre(Strng)
    Strng = DevanagariRomanLoCFix_pre(Strng)

    return Strng

# ---- Post-processing options ----

# internal
def DevanagariToRomanLocPost(Strng):
    """Applies anusvara-to-nasal, candrabindu, and nukta-digraph LoC fixes after converting Devanagari to LoC Roman."""
    from .RomanLoC import RomanLoCChandrabindu_post
    from .. import PostProcess
    Strng = PostProcess.AnusvaratoNasalASTISO(Strng)
    Strng = RomanLoCChandrabindu_post(Strng)
    Strng = DevanagariRomanLoCFix_post(Strng)

    return Strng
