# -*- coding: utf-8 -*-

# Devanagari's LoC (Library of Congress) romanization logic. See
# ScriptProcessing/HOW_TO_ADD_LOC.md for the naming convention this
# follows and how to add a new script. Renamed from RomanLoCDevanagari.py
# for consistency with the rest of ScriptProcessing/ (one file per
# script, <Script>LoC.py).
#
# HindiMarathiRomanLoCFix_pre/_post is a genuinely standalone option
# (never part of the auto-applied RomanLoC default bundle) - defined
# under the Pre-/Post-processing options headers below so Options.py's
# auto-discovery finds it directly, no re-export needed.
# DevanagariRomanLoCFix_pre/_post, by contrast, WAS part of the default
# bundle - it's purely internal, called only from
# RomanLocToDevanagari_pre/DevanagariToRomanLoc_post, so it's kept ahead
# of any options header (Options.py's scan only registers functions
# that appear at or after the first recognized header) to stay
# unregistered, same as before.

import re

# ---- Fix (encode/decode conversion logic) ----

# internal
def DevanagariRomanLoCFix_pre(Strng):
    """Normalize nukta-marked digraphs (g̳h̳, t̤, s̤, h̤) to their LoC diacritic forms for Devanagari romanization."""
    Strng = Strng.replace('g̳h̳', 'gḧ').replace('t̤', 'ṭ̈').replace('s̤', 's̈')\
        .replace('h̤', 'ḧ')

    return Strng

# internal
def DevanagariRomanLoCFix_post(Strng):
    """Fixes Devanagari LoC romanization diaeresis-marked digraphs: g-h-diaeresis -> g-underdot h-underdot, t-diaeresis -> t-underdot, s-diaeresis -> s-underdot, h-diaeresis -> h-underdot."""
    Strng = Strng.replace('gḧ', 'g̳h̳').replace('ṭ̈', 't̤').replace('s̈', 's̤')\
        .replace('ḧ', 'h̤')

    return Strng

# ---- Pre-processing options ----

# frontend
def HindiMarathiRomanLoCFix_pre(Strng):
    """Substitutes 'sh'→ṣ, ḷ→ḻ, and l̤→l̳ before Hindi/Marathi Library of Congress romanization."""
    Strng = Strng.replace('sh', 'ṣ')
    Strng = Strng.replace('ḷ', 'ḻ')
    Strng = Strng.replace('l̤', 'l̳')

    return Strng

# internal
def RomanLocToDevanagari_pre(Strng):
    """Applies candrabindu and nukta-digraph LoC fixes before converting LoC Roman text to Devanagari."""
    from .RomanLoC import RomanLoCChandrabindu_pre
    Strng = RomanLoCChandrabindu_pre(Strng)
    Strng = DevanagariRomanLoCFix_pre(Strng)

    return Strng

# ---- Post-processing options ----

# frontend
def HindiMarathiRomanLoCFix_post(Strng):
    """Reverses the Hindi/Marathi LoC substitutions: ṣ→'sh', ḻ→ḷ, l̳→l̤."""
    Strng = Strng.replace('ṣ', 'sh')
    Strng = Strng.replace('ḻ', 'ḷ')
    Strng = Strng.replace('l̳', 'l̤')

    return Strng

# internal
def DevanagariToRomanLoc_post(Strng):
    """Applies anusvara-to-nasal, candrabindu, and nukta-digraph LoC fixes after converting Devanagari to LoC Roman."""
    from .RomanLoC import RomanLoCChandrabindu_post
    from .. import PostProcess
    Strng = PostProcess.AnusvaratoNasalASTISO(Strng)
    Strng = RomanLoCChandrabindu_post(Strng)
    Strng = DevanagariRomanLoCFix_post(Strng)

    return Strng
